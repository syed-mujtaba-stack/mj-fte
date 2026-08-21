import json
import os
import secrets
import webbrowser
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import time

from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

from mj.config.settings import settings


@dataclass
class OAuthToken:
    access_token: str
    refresh_token: Optional[str]
    token_type: str
    expires_in: int
    scope: str
    id_token: Optional[str] = None

    def to_credentials(self) -> Credentials:
        return Credentials(
            token=self.access_token,
            refresh_token=self.refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=settings.google_client_id,
            client_secret=settings.google_client_secret,
            scopes=settings.google_scopes,
        )

    @classmethod
    def from_credentials(cls, creds: Credentials) -> "OAuthToken":
        return cls(
            access_token=creds.token,
            refresh_token=creds.refresh_token,
            token_type="Bearer",
            expires_in=3600,
            scope=" ".join(creds.scopes) if creds.scopes else "",
            id_token=getattr(creds, "id_token", None),
        )


@dataclass
class UserInfo:
    sub: str
    email: str
    name: str
    picture: str
    given_name: str
    family_name: str
    locale: str


class CallbackHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, oauth_flow=None, **kwargs):
        self.oauth_flow = oauth_flow
        super().__init__(*args, **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/callback":
            query = parse_qs(parsed.query)
            if "code" in query:
                self.oauth_flow.authorization_code = query["code"][0]
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"""
                <html><body>
                <h2>Authentication successful!</h2>
                <p>You can close this window and return to the terminal.</p>
                </body></html>
                """)
            else:
                self.send_response(400)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass


class GoogleOAuth:
    SERVICE_NAME = "mj-fte"
    TOKEN_KEY = "google_oauth_token"
    USER_KEY = "google_user_info"

    def __init__(self):
        self._flow: Optional[Flow] = None
        self._server: Optional[HTTPServer] = None
        self._server_thread: Optional[threading.Thread] = None

    def _create_flow(self) -> Flow:
        return Flow.from_client_config(
            {
                "web": {
                    "client_id": settings.google_client_id,
                    "client_secret": settings.google_client_secret,
                    "redirect_uris": [settings.google_redirect_uri],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            },
            scopes=settings.google_scopes,
            redirect_uri=settings.google_redirect_uri,
        )

    def get_auth_url(self) -> str:
        self._flow = self._create_flow()
        self._flow.authorization_code = None
        auth_url, _ = self._flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt="consent",
        )
        return auth_url

    def _start_callback_server(self):
        def handler(*args, **kwargs):
            return CallbackHandler(*args, oauth_flow=self._flow, **kwargs)

        self._server = HTTPServer(("localhost", 8080), handler)
        self._server_thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._server_thread.start()

    def _stop_callback_server(self):
        if self._server:
            self._server.shutdown()
            self._server.server_close()
            self._server = None

    def exchange_code(self, code: str) -> OAuthToken:
        if not self._flow:
            self._flow = self._create_flow()
        self._flow.fetch_token(code=code)
        return OAuthToken.from_credentials(self._flow.credentials)

    def _token_to_dict(self, token: OAuthToken) -> dict:
        data = asdict(token)
        data.pop("id_token", None)
        return data

    @property
    def _token_file(self) -> Path:
        return settings.config_dir / "token.json"

    @property
    def _user_file(self) -> Path:
        return settings.config_dir / "user.json"

    def save_token(self, token: OAuthToken):
        settings.config_dir.mkdir(parents=True, exist_ok=True)
        self._token_file.write_text(json.dumps(self._token_to_dict(token)), encoding="utf-8")

    def load_token(self) -> Optional[OAuthToken]:
        if self._token_file.exists():
            try:
                return OAuthToken(**json.loads(self._token_file.read_text(encoding="utf-8")))
            except Exception:
                return None
        return None

    def delete_token(self):
        self._token_file.unlink(missing_ok=True)
        self._user_file.unlink(missing_ok=True)

    def save_user(self, user: UserInfo):
        settings.config_dir.mkdir(parents=True, exist_ok=True)
        self._user_file.write_text(json.dumps(asdict(user)), encoding="utf-8")

    def load_user(self) -> Optional[UserInfo]:
        if self._user_file.exists():
            try:
                return UserInfo(**json.loads(self._user_file.read_text(encoding="utf-8")))
            except Exception:
                return None
        return None

    def is_authenticated(self) -> bool:
        token = self.load_token()
        if not token:
            return False
        creds = token.to_credentials()
        if creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                self.save_token(OAuthToken.from_credentials(creds))
                return True
            except Exception:
                return False
        return not creds.expired

    def get_valid_credentials(self) -> Optional[Credentials]:
        token = self.load_token()
        if not token:
            return None
        creds = token.to_credentials()
        if creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                self.save_token(OAuthToken.from_credentials(creds))
            except Exception:
                return None
        return creds if not creds.expired else None

    def authenticate(self) -> bool:
        if self.is_authenticated():
            return True

        auth_url = self.get_auth_url()
        print(f"\n>> Opening browser for Google authentication...")
        print(f"If browser doesn't open, visit: {auth_url}\n")

        self._start_callback_server()
        webbrowser.open(auth_url)

        timeout = 120
        start = time.time()
        while self._flow and self._flow.authorization_code is None:
            if time.time() - start > timeout:
                self._stop_callback_server()
                print("[X] Authentication timed out.")
                return False
            time.sleep(0.5)

        self._stop_callback_server()

        if not self._flow or not self._flow.authorization_code:
            print("[X] No authorization code received.")
            return False

        try:
            token = self.exchange_code(self._flow.authorization_code)
            self.save_token(token)

            user = self.fetch_and_save_user()
            if user:
                print(f"[OK] Authenticated as {user.email}")
                return True
            print("[X] Authenticated but failed to fetch user info.")
            return True
        except Exception as e:
            print(f"[X] Authentication failed: {e}")
            return False

    def fetch_and_save_user(self) -> Optional[UserInfo]:
        token = self.load_token()
        if not token:
            return None
        try:
            import requests as _requests
            resp = _requests.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {token.access_token}"},
                timeout=15,
            )
            resp.raise_for_status()
            user_info = resp.json()

            user = UserInfo(
                sub=user_info["id"],
                email=user_info["email"],
                name=user_info.get("name", ""),
                picture=user_info.get("picture", ""),
                given_name=user_info.get("given_name", ""),
                family_name=user_info.get("family_name", ""),
                locale=user_info.get("locale", ""),
            )
            self.save_user(user)
            return user
        except Exception:
            return None

    def logout(self):
        self.delete_token()
        print(">> Logged out successfully.")
