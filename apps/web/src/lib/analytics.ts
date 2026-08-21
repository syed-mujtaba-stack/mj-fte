// Google Analytics 4
// 1. Create a property at https://analytics.google.com
// 2. Copy your Measurement ID (looks like "G-XXXXXXXXXX")
// 3. Paste it below — or set VITE_GA_MEASUREMENT_ID in Vercel env vars.
// Leave empty to keep analytics disabled.

const GA_MEASUREMENT_ID: string =
  (import.meta.env.VITE_GA_MEASUREMENT_ID as string | undefined) ||
  'G-WKSVZX6YXX';

declare global {
  interface Window {
    dataLayer?: unknown[];
    gtag?: (...args: unknown[]) => void;
  }
}

let initialized = false;

export function initAnalytics(): void {
  if (initialized || !GA_MEASUREMENT_ID) return;
  initialized = true;

  const script = document.createElement('script');
  script.async = true;
  script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`;
  document.head.appendChild(script);

  window.dataLayer = window.dataLayer || [];
  window.gtag = function gtag(...args: unknown[]) {
    window.dataLayer!.push(args);
  };
  window.gtag('js', new Date());
  // We send page_view manually on route change (SPA).
  window.gtag('config', GA_MEASUREMENT_ID, { send_page_view: false });
}

export function trackPageview(path: string): void {
  if (!window.gtag || !GA_MEASUREMENT_ID) return;
  window.gtag('event', 'page_view', {
    page_path: path,
    page_title: document.title,
    page_location: window.location.href,
  });
}

export function trackEvent(action: string, params: Record<string, unknown> = {}): void {
  if (!window.gtag || !GA_MEASUREMENT_ID) return;
  window.gtag('event', action, params);
}
