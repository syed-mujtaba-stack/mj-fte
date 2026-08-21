import { type ReactNode, useEffect, useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ErrorBoundary } from '@/components/error-boundary';
import { Toaster } from '@/components/ui/toaster';
import { TooltipProvider } from '@/components/ui/tooltip';
import NotFound from '@/pages/not-found';
import { trackPageview, trackEvent } from '@/lib/analytics';
import { Route, Switch, Link, useLocation, Router as WouterRouter } from 'wouter';
import {
  AlertTriangle,
  ArrowRight,
  BookOpen,
  Check,
  ChevronDown,
  CircleCheck,
  Clock3,
  Copy,
  Database,
  Download,
  ExternalLink,
  Eye,
  FileCode2,
  Github,
  History,
  KeyRound,
  LockKeyhole,
  Menu,
  ScanLine,
  ShieldCheck,
  Terminal,
  X,
  Wrench,
} from 'lucide-react';

const queryClient = new QueryClient();
const GITHUB = 'https://github.com/syed-mujtaba-stack/mj-fte';
const PYPI = 'https://pypi.org/project/mj-fte/';
const ISSUES = 'https://github.com/syed-mujtaba-stack/mj-fte/issues';
const CHANGELOG = 'https://github.com/syed-mujtaba-stack/mj-fte/blob/main/CHANGELOG.md';
const INSTALL = 'pip install mj-fte';

function ExternalAnchor({ href, children, className = '', label }: { href: string; children: ReactNode; className?: string; label?: string }) {
  return <a data-testid={label ?? 'link-external'} href={href} target="_blank" rel="noopener noreferrer" className={className} onClick={() => trackEvent('outbound_click', { label: label ?? 'link-external', url: href })}>{children}</a>;
}

function Logo() {
  return (
    <span className="flex items-center gap-2.5" data-testid="brand-mj-fte">
      <span className="relative flex h-7 w-7 items-center justify-center rounded-lg border border-cyan-200/35 bg-cyan-200/[.09] text-cyan-200">
        <span className="absolute h-3 w-3 rounded-[3px] border border-cyan-200/70" />
        <span className="absolute h-px w-5 bg-cyan-200/75" />
      </span>
      <span className="font-display text-[15px] font-semibold tracking-[-.02em] text-slate-100">mj-fte</span>
    </span>
  );
}

function Navbar({ docs = false }: { docs?: boolean }) {
  const [menuOpen, setMenuOpen] = useState(false);
  const close = () => setMenuOpen(false);
  return (
    <header className="glass-nav fixed inset-x-0 top-0 z-40">
      <div className="mx-auto flex h-[72px] max-w-7xl items-center justify-between px-5 lg:px-8">
        <Link href="/" onClick={close} className="no-underline" data-testid="link-logo"><Logo /></Link>
        <nav className="hidden items-center gap-7 md:flex" aria-label="Primary navigation">
          {docs ? (
            <>
              <a data-testid="link-docs-intro" href="#introduction" className="text-[13px] text-slate-400 transition hover:text-slate-100">Introduction</a>
              <a data-testid="link-docs-install" href="#installation" className="text-[13px] text-slate-400 transition hover:text-slate-100">Installation</a>
              <a data-testid="link-docs-commands" href="#commands" className="text-[13px] text-slate-400 transition hover:text-slate-100">Commands</a>
              <a data-testid="link-docs-safety" href="#safety" className="text-[13px] text-slate-400 transition hover:text-slate-100">Safety</a>
            </>
          ) : (
            <>
              <a data-testid="link-features" href="#features" className="text-[13px] text-slate-400 transition hover:text-slate-100">Why mj-fte</a>
              <a data-testid="link-safety" href="#safety" className="text-[13px] text-slate-400 transition hover:text-slate-100">Safety</a>
              <a data-testid="link-commands" href="#commands" className="text-[13px] text-slate-400 transition hover:text-slate-100">Commands</a>
              <a data-testid="link-faq" href="#faq" className="text-[13px] text-slate-400 transition hover:text-slate-100">FAQ</a>
            </>
          )}
        </nav>
        <div className="hidden items-center gap-3 md:flex">
          <ExternalAnchor href={GITHUB} label="link-github-nav" className="inline-flex items-center gap-2 rounded-md px-2 py-2 text-[13px] text-slate-400 transition hover:text-slate-100"><Github size={15} /> GitHub</ExternalAnchor>
          {docs ? <Link href="/#install" data-testid="link-install-nav" className="rounded-md bg-cyan-200 px-3.5 py-2 text-[13px] font-semibold text-[#10141e] transition hover:bg-cyan-100">Get started</Link> : <a href="#install" data-testid="link-install-nav" className="rounded-md bg-cyan-200 px-3.5 py-2 text-[13px] font-semibold text-[#10141e] transition hover:bg-cyan-100">Install now</a>}
        </div>
        <button type="button" data-testid="button-mobile-menu" onClick={() => setMenuOpen(!menuOpen)} className="rounded-md p-2 text-slate-300 md:hidden" aria-label="Toggle navigation">
          {menuOpen ? <X size={20} /> : <Menu size={20} />}
        </button>
      </div>
      {menuOpen && (
        <nav className="border-t border-white/[.08] px-5 pb-5 pt-3 md:hidden" aria-label="Mobile navigation">
          <div className="flex flex-col gap-1">
            {(docs ? [['#introduction', 'Introduction'], ['#installation', 'Installation'], ['#commands', 'Commands'], ['#safety', 'Safety']] : [['#features', 'Why mj-fte'], ['#safety', 'Safety'], ['#commands', 'Commands'], ['#faq', 'FAQ']]).map(([href, label]) => (
              <a key={href} data-testid={`link-mobile-${label.toLowerCase().replaceAll(' ', '-')}`} onClick={close} href={href} className="rounded-md px-2 py-3 text-sm text-slate-300 hover:bg-white/[.05]">{label}</a>
            ))}
            <ExternalAnchor href={GITHUB} label="link-github-mobile" className="flex items-center gap-2 rounded-md px-2 py-3 text-sm text-slate-300"><Github size={15} /> View on GitHub</ExternalAnchor>
          </div>
        </nav>
      )}
    </header>
  );
}

function Eyebrow({ children, icon: Icon = Terminal }: { children: ReactNode; icon?: typeof Terminal }) {
  return <div className="mb-5 flex items-center gap-2 font-mono text-[11px] font-medium uppercase tracking-[.18em] text-cyan-200/75"><Icon size={13} /> {children}</div>;
}

function SectionHeading({ eyebrow, title, body, icon }: { eyebrow: string; title: ReactNode; body?: string; icon?: typeof Terminal }) {
  return (
    <div className="max-w-2xl">
      <Eyebrow icon={icon}>{eyebrow}</Eyebrow>
      <h2 className="font-display text-3xl font-medium leading-[1.08] tracking-[-.04em] text-slate-100 sm:text-5xl">{title}</h2>
      {body && <p className="mt-5 max-w-xl text-[15px] leading-7 text-slate-400">{body}</p>}
    </div>
  );
}

function CopyButton({ value = INSTALL, compact = false }: { value?: string; compact?: boolean }) {
  const [copied, setCopied] = useState(false);
  const copy = async () => {
    try { await navigator.clipboard.writeText(value); } catch { /* clipboard may be unavailable in preview */ }
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1600);
  };
  return <button type="button" data-testid={`button-copy-${value.replaceAll(' ', '-')}`} onClick={copy} className={`inline-flex items-center gap-2 rounded-md border border-white/[.12] text-xs text-slate-300 transition hover:border-cyan-200/40 hover:text-cyan-100 ${compact ? 'px-2 py-1.5' : 'px-3 py-2'}`} aria-label={`Copy ${value}`}>
    {copied ? <Check size={13} className="text-cyan-200" /> : <Copy size={13} />} {copied ? 'Copied' : compact ? 'Copy' : 'Copy command'}
  </button>;
}

function TerminalWindow() {
  const lines = [
    { prompt: true, text: 'mj-fte scan --safe' },
    { prompt: false, text: 'mj-fte 0.4.0  /  safety mode enabled' },
    { prompt: false, text: '' },
    { prompt: false, text: 'Scanning user cache .................  1.84 GB' },
    { prompt: false, text: 'Scanning temp directories ............  632 MB' },
    { prompt: false, text: 'Scanning package residue ............  214 MB' },
    { prompt: false, text: '' },
    { prompt: false, text: 'Found 2.68 GB of safe-to-remove files.' },
    { prompt: false, text: 'No protected paths were touched.', accent: true },
    { prompt: false, text: '' },
    { prompt: true, text: 'mj-fte clean --dry-run' },
  ];
  const [visible, setVisible] = useState(0);
  useEffect(() => {
    const timer = window.setInterval(() => setVisible((current) => current < lines.length ? current + 1 : current), 380);
    return () => window.clearInterval(timer);
  }, [lines.length]);
  return (
    <div className="terminal-shadow float-slow overflow-hidden rounded-xl border border-white/[.13] bg-[#0a0d13]" data-testid="terminal-window">
      <div className="flex items-center justify-between border-b border-white/[.08] bg-white/[.025] px-4 py-3">
        <div className="flex items-center gap-1.5"><span className="h-2 w-2 rounded-full bg-[#ed6b75]" /><span className="h-2 w-2 rounded-full bg-[#e6bd6b]" /><span className="h-2 w-2 rounded-full bg-[#77c88c]" /></div>
        <span className="font-mono text-[10px] tracking-wide text-slate-600">powershell — mj-fte</span>
        <span className="w-8" />
      </div>
      <div className="min-h-[300px] px-5 py-6 font-mono text-[11px] leading-[2.05] sm:min-h-[346px] sm:px-7 sm:py-7 sm:text-xs">
        {lines.slice(0, visible).map((line, index) => <div key={`${line.text}-${index}`} className={line.accent ? 'text-cyan-200' : line.prompt ? 'text-slate-100' : 'text-slate-500'}><span className={line.prompt ? 'text-violet-300' : 'text-transparent'}>{line.prompt ? '› ' : '· '}</span>{line.text}{index === visible - 1 && <span className="caret ml-0.5 inline-block h-3 w-[6px] translate-y-[2px] bg-cyan-200/75" />}</div>)}
        {visible === lines.length && <div className="mt-2 text-slate-600">ready for your next instruction</div>}
      </div>
      <div className="flex items-center justify-between border-t border-white/[.08] px-5 py-3 font-mono text-[10px] text-slate-600"><span>read-only preview</span><span className="flex items-center gap-1.5 text-cyan-200/60"><CircleCheck size={12} /> no changes made</span></div>
    </div>
  );
}

function Home() {
  const [openFaq, setOpenFaq] = useState<number | null>(0);
  return (
    <div className="site-shell noise">
      <Navbar />
      <main>
        <section className="hero-glow relative isolate min-h-[760px] overflow-hidden px-5 pb-24 pt-36 sm:pt-44 lg:px-8">
          <div className="grid-paper absolute inset-0 -z-10" />
          <div className="pointer-events-none absolute left-1/2 top-20 -z-10 h-[420px] w-[680px] -translate-x-1/2 rounded-full bg-cyan-200/[.05] blur-3xl" />
          <div className="mx-auto grid max-w-7xl items-center gap-14 lg:grid-cols-[.9fr_1.1fr] lg:gap-20">
            <div className="reveal">
              <div className="mb-7 flex items-center gap-3"><span className="h-px w-9 bg-cyan-200/75" /><span className="font-mono text-[11px] uppercase tracking-[.16em] text-slate-500">open-source / windows / python</span></div>
              <h1 aria-label="Tera system, meri zimmedari" className="font-display text-[3.6rem] font-medium leading-[.95] tracking-[-.075em] text-slate-100 sm:text-7xl lg:text-[6.5rem]">Tera system,<br /><span className="bg-gradient-to-r from-cyan-200 via-sky-200 to-violet-300 bg-clip-text text-transparent">meri zimmedari</span></h1>
              <p className="mt-8 max-w-lg text-[17px] leading-8 text-slate-400">A transparent, safety-first disk cleaner and system analyzer for Windows. Know what is taking space. Decide what leaves. Nothing happens without your say.</p>
              <div className="mt-9 flex flex-col items-start gap-4 sm:flex-row sm:items-center">
                <a href="#install" data-testid="link-hero-install" className="group inline-flex items-center gap-2 rounded-md bg-cyan-200 px-5 py-3 text-sm font-semibold text-[#10141e] transition hover:bg-cyan-100">Install mj-fte <ArrowRight size={16} className="transition group-hover:translate-x-0.5" /></a>
                <ExternalAnchor href={GITHUB} label="link-hero-github" className="inline-flex items-center gap-2 px-1 py-3 text-sm text-slate-400 transition hover:text-slate-100"><Github size={16} /> Read the source</ExternalAnchor>
              </div>
              <div className="mt-10 flex flex-wrap items-center gap-x-5 gap-y-3 font-mono text-[11px] text-slate-500"><span className="flex items-center gap-2"><ShieldCheck size={14} className="text-cyan-200/70" /> safe by default</span><span className="h-3 w-px bg-white/10" /><span>MIT licensed</span><span className="h-3 w-px bg-white/10" /><span>Python 3.9+</span></div>
            </div>
            <div className="reveal reveal-delay-2 relative"><TerminalWindow /><div className="absolute -bottom-7 -left-4 hidden rounded-lg border border-white/[.1] bg-[#151b27]/90 px-3 py-2 font-mono text-[10px] text-slate-400 shadow-xl sm:block"><span className="mr-2 text-cyan-200">●</span> preview mode — nothing deleted</div></div>
          </div>
        </section>

        <section id="features" className="relative border-t border-white/[.08] px-5 py-28 lg:px-8">
          <div className="mx-auto max-w-7xl">
            <SectionHeading eyebrow="The premise" title={<>Cleaning should not feel like <span className="text-violet-200">guesswork.</span></>} body="Most disk cleaners ask for trust first and explain later. mj-fte does the reverse: inspect, explain, preview, then act." icon={Eye} />
            <div className="mt-16 grid gap-4 md:grid-cols-12">
              <FeatureCard className="md:col-span-7" number="01" icon={ScanLine} title="See the whole picture" body="Scan disk usage across familiar Windows locations and surface the files that actually matter — without hiding the details behind a percentage." tags={['disk analysis', 'human-readable output']} />
              <FeatureCard className="md:col-span-5" number="02" icon={ShieldCheck} title="Safety is the default" body="Protected paths are never candidates. Dry-run is the natural first step. Every destructive command asks you to confirm." tags={['protected paths', 'explicit confirmation']} accent />
              <FeatureCard className="md:col-span-5" number="03" icon={Wrench} title="Small tool, clear intent" body="No daemon. No telemetry. No dashboard to babysit. Just a focused CLI that does one job with a readable output you can keep." tags={['zero telemetry', 'composable CLI']} />
              <FeatureCard className="md:col-span-7" number="04" icon={FileCode2} title="Built for the terminal" body="Install it with pip, run it from PowerShell, and script it into your own workflow. The source is open because the work should be inspectable." tags={['Python', 'MIT license']} accent />
            </div>
          </div>
        </section>

        <section id="safety" className="section-glow relative border-y border-white/[.08] px-5 py-28 lg:px-8">
          <div className="mx-auto grid max-w-7xl gap-16 lg:grid-cols-[.8fr_1.2fr] lg:gap-28">
            <div><SectionHeading eyebrow="The safety contract" title={<>The tool should know<br /><span className="text-cyan-200">when to stop.</span></>} body="mj-fte treats file deletion as a permission, not a side effect. Its guardrails are part of the product, not a footnote." icon={LockKeyhole} /></div>
            <div className="space-y-0">
              <SafetyRow icon={Eye} title="Scan before you clean" body="Every cleanup starts with a report. See the candidate paths and estimated space before you choose an action." />
              <SafetyRow icon={ShieldCheck} title="Protected by design" body="Windows system locations and paths outside the safe allowlist are excluded from cleanup candidates." />
              <SafetyRow icon={KeyRound} title="Confirmation is explicit" body="A clean command never runs silently. You confirm what you saw — or you cancel with no consequence." />
              <SafetyRow icon={Database} title="Local-only operation" body="Your scan stays on your machine. There are no uploads, accounts, or analytics hidden in the command." />
            </div>
          </div>
        </section>

        <section id="commands" className="px-5 py-28 lg:px-8">
          <div className="mx-auto max-w-7xl">
            <div className="flex flex-col justify-between gap-6 lg:flex-row lg:items-end"><SectionHeading eyebrow="A small surface area" title="Four commands. No ceremony." body="Each command has one job. The output stays readable in a terminal, a log file, or your own automation." icon={Terminal} /><Link href="/docs#commands" data-testid="link-command-docs" className="group inline-flex items-center gap-2 pb-1 text-sm text-cyan-200">Read command reference <ArrowRight size={15} className="transition group-hover:translate-x-1" /></Link></div>
            <div className="mt-14 divide-y divide-white/[.09] border-y border-white/[.09]">
              <CommandRow command="mj-fte scan" description="Analyze disk usage and show safe cleanup candidates." note="read-only" />
              <CommandRow command="mj-fte clean --dry-run" description="Preview exactly what a cleanup would remove. Makes no changes." note="recommended" />
              <CommandRow command="mj-fte clean" description="Remove confirmed candidates after an explicit confirmation prompt." note="destructive" warning />
              <CommandRow command="mj-fte --help" description="Print available commands, options, and safety notes." note="reference" />
            </div>
          </div>
        </section>

        <section id="install" className="border-y border-white/[.08] bg-[#111722] px-5 py-24 lg:px-8">
          <div className="mx-auto grid max-w-7xl items-start gap-12 lg:grid-cols-[.78fr_1.22fr] lg:gap-24">
            <div><SectionHeading eyebrow="Start locally" title={<>One install.<br /><span className="text-cyan-200">Full visibility.</span></>} body="mj-fte works wherever Python works on Windows. No installer wizard, no account, no background service." icon={Download} /></div>
            <div className="space-y-4">
              <InstallStep index="01" title="Install from PyPI" code={INSTALL} />
              <InstallStep index="02" title="Scan in safe mode" code="mj-fte scan --safe" />
              <InstallStep index="03" title="Preview before acting" code="mj-fte clean --dry-run" />
              <p className="pt-3 font-mono text-[11px] leading-6 text-slate-500">Requires Python 3.9 or newer · Windows 10/11 · <ExternalAnchor href={PYPI} label="link-pypi-install" className="text-slate-400 underline decoration-white/20 underline-offset-4 hover:text-cyan-200">view package on PyPI</ExternalAnchor></p>
            </div>
          </div>
        </section>

        <section id="history" className="px-5 py-28 lg:px-8">
          <div className="mx-auto max-w-7xl">
            <div className="flex flex-col justify-between gap-5 border-b border-white/[.09] pb-8 sm:flex-row sm:items-end"><SectionHeading eyebrow="Project pulse" title="Quietly getting better." icon={History} /><ExternalAnchor href={CHANGELOG} label="link-changelog" className="inline-flex items-center gap-2 pb-1 text-sm text-slate-400 hover:text-slate-100">Full changelog <ExternalLink size={14} /></ExternalAnchor></div>
            <div className="grid gap-10 pt-10 sm:grid-cols-3">
              <Version version="0.4.0" date="Latest · 14 Feb 2025" title="Safer cleanup flow" body="Added --safe as the default scanning posture, clearer protected-path reporting, and a dry-run summary built for review." current />
              <Version version="0.3.1" date="06 Jan 2025" title="Sharper reports" body="More useful directory grouping and stable output for PowerShell redirection." />
              <Version version="0.3.0" date="18 Dec 2024" title="The first public cut" body="Disk analysis, cache detection, and a small command surface designed to be understood." />
            </div>
          </div>
        </section>

        <section id="faq" className="section-glow border-t border-white/[.08] px-5 py-28 lg:px-8">
          <div className="mx-auto grid max-w-7xl gap-14 lg:grid-cols-[.78fr_1.22fr] lg:gap-24">
            <SectionHeading eyebrow="Questions worth asking" title={<>Before you let a tool<br /><span className="text-violet-200">touch your disk.</span></>} body="A cleaner earns trust by being specific about its boundaries. Here are the answers we want you to have before installing." icon={AlertTriangle} />
            <div className="border-t border-white/[.1]">
              {FAQS.map((faq, index) => <div key={faq.question} className="border-b border-white/[.1]"><button type="button" data-testid={`button-faq-${index}`} onClick={() => setOpenFaq(openFaq === index ? null : index)} className="flex w-full items-center justify-between gap-5 py-5 text-left text-[15px] font-medium text-slate-200"><span>{faq.question}</span><ChevronDown size={17} className={`shrink-0 text-slate-500 transition ${openFaq === index ? 'rotate-180 text-cyan-200' : ''}`} /></button>{openFaq === index && <p data-testid={`text-faq-answer-${index}`} className="max-w-2xl pb-6 pr-8 text-sm leading-7 text-slate-400">{faq.answer}</p>}</div>)}
            </div>
          </div>
        </section>

        <section className="relative overflow-hidden px-5 py-28 text-center lg:px-8">
          <div className="pointer-events-none absolute inset-x-1/4 top-10 h-48 rounded-full bg-violet-300/[.09] blur-3xl" />
          <div className="relative mx-auto max-w-3xl"><p className="font-mono text-[11px] uppercase tracking-[.18em] text-cyan-200/70">The short version</p><h2 className="mt-5 font-display text-4xl font-medium leading-[1.03] tracking-[-.055em] text-slate-100 sm:text-6xl">Your disk is yours.<br /><span className="text-cyan-200">Keep it that way.</span></h2><p className="mx-auto mt-6 max-w-lg text-[15px] leading-7 text-slate-400">Install the open-source Windows cleaner that explains itself before it acts.</p><div className="mt-9 flex flex-col justify-center gap-4 sm:flex-row"><a href="#install" data-testid="link-bottom-install" className="inline-flex items-center justify-center gap-2 rounded-md bg-cyan-200 px-5 py-3 text-sm font-semibold text-[#10141e] transition hover:bg-cyan-100">Install mj-fte <ArrowRight size={16} /></a><ExternalAnchor href={ISSUES} label="link-bottom-issue" className="inline-flex items-center justify-center gap-2 rounded-md border border-white/[.14] px-5 py-3 text-sm text-slate-300 transition hover:border-white/30 hover:text-white">Ask a question <ExternalLink size={14} /></ExternalAnchor></div></div>
        </section>
      </main>
      <Footer />
    </div>
  );
}

function FeatureCard({ number, icon: Icon, title, body, tags, accent, className = '' }: { number: string; icon: typeof Eye; title: string; body: string; tags: string[]; accent?: boolean; className?: string }) {
  return <article className={`card-shadow group relative overflow-hidden rounded-xl border border-white/[.1] bg-white/[.025] p-7 transition duration-300 hover:-translate-y-1 hover:border-cyan-200/25 sm:p-9 ${className}`}><div className={`absolute inset-x-0 top-0 h-px ${accent ? 'bg-gradient-to-r from-violet-300/70 to-transparent' : 'bg-gradient-to-r from-cyan-200/70 to-transparent'}`} /><div className="flex items-start justify-between"><span className="font-mono text-[11px] text-slate-600">{number}</span><Icon size={20} className={accent ? 'text-violet-200/80' : 'text-cyan-200/80'} /></div><h3 className="mt-12 font-display text-2xl tracking-[-.035em] text-slate-100">{title}</h3><p className="mt-4 max-w-lg text-sm leading-7 text-slate-400">{body}</p><div className="mt-7 flex flex-wrap gap-2">{tags.map(tag => <span key={tag} className="rounded border border-white/[.1] px-2 py-1 font-mono text-[10px] text-slate-500">{tag}</span>)}</div></article>;
}

function SafetyRow({ icon: Icon, title, body }: { icon: typeof Eye; title: string; body: string }) {
  return <div className="flex gap-5 border-b border-white/[.1] py-6 first:border-t"><div className="mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-md border border-cyan-200/20 bg-cyan-200/[.06] text-cyan-200"><Icon size={15} /></div><div><h3 className="font-display text-lg text-slate-200">{title}</h3><p className="mt-2 max-w-xl text-sm leading-6 text-slate-500">{body}</p></div></div>;
}

function CommandRow({ command, description, note, warning }: { command: string; description: string; note: string; warning?: boolean }) {
  return <div className="grid gap-3 py-6 md:grid-cols-[.8fr_1.5fr_auto] md:items-center md:gap-8"><code className="font-mono text-sm text-cyan-100">{command}</code><p className="text-sm text-slate-400">{description}</p><span className={`w-fit rounded-full border px-2.5 py-1 font-mono text-[10px] uppercase tracking-wide ${warning ? 'border-amber-200/20 text-amber-200/70' : 'border-white/[.1] text-slate-500'}`}>{note}</span></div>;
}

function InstallStep({ index, title, code }: { index: string; title: string; code: string }) {
  return <div className="rounded-lg border border-white/[.1] bg-[#0d1119] p-4 transition hover:border-cyan-200/25"><div className="mb-3 flex items-center justify-between"><span className="font-mono text-[10px] text-slate-600">{index}</span><span className="text-sm text-slate-300">{title}</span><CopyButton value={code} compact /></div><code className="block rounded bg-black/20 px-3 py-2.5 font-mono text-[12px] text-cyan-100/80">{code}</code></div>;
}

function Version({ version, date, title, body, current }: { version: string; date: string; title: string; body: string; current?: boolean }) {
  return <article className={`relative border-l pl-5 ${current ? 'border-cyan-200/70' : 'border-white/[.14]'}`}><div className="absolute -left-[4px] top-0 h-1.5 w-1.5 rounded-full bg-cyan-200" /><div className="flex items-center gap-3"><span className="font-mono text-sm text-slate-200">v{version}</span>{current && <span className="rounded-full border border-cyan-200/25 bg-cyan-200/[.07] px-2 py-0.5 font-mono text-[9px] uppercase tracking-wide text-cyan-200">current</span>}</div><p className="mt-2 font-mono text-[10px] text-slate-600">{date}</p><h3 className="mt-6 font-display text-lg text-slate-200">{title}</h3><p className="mt-2 text-sm leading-6 text-slate-500">{body}</p></article>;
}

const FAQS = [
  { question: 'Can mj-fte delete something important?', answer: 'The safe scanner only surfaces known temporary, cache, and package-residue locations. Protected paths are excluded from cleanup candidates, and the clean command requires an explicit confirmation. Use --dry-run when you want to inspect the complete candidate list without touching anything.' },
  { question: 'Does the tool send my files anywhere?', answer: 'No. mj-fte is a local-only CLI. It does not upload scan results, require an account, run a background service, or include telemetry.' },
  { question: 'What happens when I use clean --dry-run?', answer: 'It runs the same candidate selection logic as a cleanup, prints what would be removed and the estimated space, then exits without making changes. It is the recommended way to understand a cleanup before confirming one.' },
  { question: 'Why is this a CLI instead of a desktop app?', answer: 'A terminal keeps the work close to the person asking for it. It is inspectable, scriptable, and naturally explicit. You can redirect output, read the source, and compose it with the tools already in your workflow.' },
  { question: 'How can I report a problem or request a feature?', answer: 'Open an issue on GitHub with your Windows version, Python version, command used, and the relevant output. Reproduction details help keep the tool safe for everyone.' },
];

function Docs() {
  return <div className="site-shell noise"><Navbar docs /><main className="px-5 pb-28 pt-32 lg:px-8"><div className="mx-auto grid max-w-7xl gap-12 lg:grid-cols-[220px_minmax(0,760px)_1fr] lg:gap-16"><DocsSidebar /><article className="min-w-0"><div id="introduction" className="border-b border-white/[.1] pb-14"><Eyebrow icon={BookOpen}>Reference documentation</Eyebrow><h1 className="font-display text-4xl font-medium tracking-[-.055em] text-slate-100 sm:text-6xl">mj-fte, explained<br /><span className="text-cyan-200">before it runs.</span></h1><p className="mt-7 max-w-2xl text-[16px] leading-8 text-slate-400">mj-fte is an open-source Windows disk cleaner and system analyzer CLI agent written in Python. It makes the risky work of cleaning a machine transparent and controlled.</p><div className="mt-7 flex flex-wrap gap-3"><span className="rounded-full border border-cyan-200/20 bg-cyan-200/[.06] px-3 py-1.5 font-mono text-[11px] text-cyan-100">v0.4.0</span><span className="rounded-full border border-white/[.12] px-3 py-1.5 font-mono text-[11px] text-slate-400">Python 3.9+</span><span className="rounded-full border border-white/[.12] px-3 py-1.5 font-mono text-[11px] text-slate-400">MIT license</span></div></div><DocsContent /></article><DocsAside /></div></main><Footer /></div>;
}

function DocsSidebar() {
  const items = [['introduction', 'Introduction'], ['installation', 'Installation'], ['commands', 'Commands'], ['safety', 'Safety model'], ['workflow', 'Typical workflow'], ['history', 'Version history'], ['faq', 'FAQ']];
  return <aside className="hidden lg:block"><div className="sticky top-28"><p className="mb-4 font-mono text-[10px] uppercase tracking-[.16em] text-slate-600">On this page</p><nav className="space-y-1 border-l border-white/[.1]">{items.map(([id, label]) => <a key={id} data-testid={`link-doc-sidebar-${id}`} href={`#${id}`} className="block border-l border-transparent py-2 pl-4 text-[13px] text-slate-500 transition hover:border-cyan-200/60 hover:text-slate-200">{label}</a>)}</nav><div className="mt-10 rounded-lg border border-white/[.1] bg-white/[.025] p-4"><p className="font-mono text-[10px] uppercase tracking-wide text-cyan-200/70">Need the source?</p><ExternalAnchor href={GITHUB} label="link-doc-sidebar-github" className="mt-3 flex items-center gap-2 text-xs text-slate-300 hover:text-cyan-200"><Github size={14} /> Browse on GitHub <ExternalLink size={12} /></ExternalAnchor></div></div></aside>;
}

function DocsAside() {
  return <aside className="hidden xl:block"><div className="sticky top-28 space-y-7"><div className="flex items-center gap-2 border-b border-white/[.1] pb-3 font-mono text-[10px] uppercase tracking-[.16em] text-slate-600"><Clock3 size={13} /> Maintained</div><p className="text-xs leading-6 text-slate-500">This documentation follows the current public release. If behavior differs on your machine, please open an issue with the command output.</p><ExternalAnchor href={ISSUES} label="link-doc-aside-issues" className="inline-flex items-center gap-2 text-xs text-cyan-200 hover:text-cyan-100">Open an issue <ArrowRight size={13} /></ExternalAnchor></div></aside>;
}

function DocsContent() {
  return <div className="prose prose-invert max-w-none prose-headings:font-display prose-headings:font-medium prose-headings:tracking-[-.035em] prose-p:text-slate-400 prose-p:leading-8 prose-li:text-slate-400 prose-strong:text-slate-200 prose-code:text-cyan-100 prose-code:before:content-none prose-code:after:content-none">
    <section id="installation" className="scroll-mt-28 border-b border-white/[.1] py-14"><h2>Installation</h2><p>mj-fte is distributed through PyPI and runs locally on Windows. Install it from PowerShell with the command below.</p><CodeBlock code={INSTALL} /><p>Verify the installation and inspect the available options:</p><CodeBlock code={'mj-fte --version\nmj-fte --help'} /><Callout title="Requirements" icon={CircleCheck}>Windows 10 or Windows 11 with Python 3.9 or newer. Run PowerShell with the permissions appropriate for the locations you intend to inspect.</Callout></section>
    <section id="commands" className="scroll-mt-28 border-b border-white/[.1] py-14"><h2>Commands</h2><p>The command surface is intentionally small. Start with a read-only scan, preview cleanup candidates, and only then choose to remove them.</p><div className="not-prose my-8 overflow-hidden rounded-lg border border-white/[.1]"><table className="w-full text-left text-sm"><thead className="bg-white/[.035] font-mono text-[10px] uppercase tracking-wide text-slate-500"><tr><th className="px-4 py-3 font-medium">Command</th><th className="px-4 py-3 font-medium">What it does</th><th className="hidden px-4 py-3 font-medium sm:table-cell">Changes disk?</th></tr></thead><tbody className="divide-y divide-white/[.08] text-slate-400"><tr><td className="px-4 py-4 font-mono text-cyan-100">scan</td><td className="px-4 py-4">Analyze disk usage and report candidates.</td><td className="hidden px-4 py-4 text-cyan-200 sm:table-cell">No</td></tr><tr><td className="px-4 py-4 font-mono text-cyan-100">clean --dry-run</td><td className="px-4 py-4">Show what a cleanup would remove.</td><td className="hidden px-4 py-4 text-cyan-200 sm:table-cell">No</td></tr><tr><td className="px-4 py-4 font-mono text-cyan-100">clean</td><td className="px-4 py-4">Remove confirmed safe candidates.</td><td className="hidden px-4 py-4 text-amber-200 sm:table-cell">Yes, after prompt</td></tr><tr><td className="px-4 py-4 font-mono text-cyan-100">--help</td><td className="px-4 py-4">Print command and option reference.</td><td className="hidden px-4 py-4 text-cyan-200 sm:table-cell">No</td></tr></tbody></table></div><h3>Scan your system</h3><CodeBlock code={'mj-fte scan\nmj-fte scan --safe'} /><h3>Preview a cleanup</h3><CodeBlock code="mj-fte clean --dry-run" /><h3>Run a cleanup</h3><CodeBlock code="mj-fte clean" /><Callout title="Keep the preview" icon={Eye}>The dry-run output is the clearest audit trail. Redirect it to a file when you want to review or share a proposed cleanup.</Callout></section>
    <section id="safety" className="scroll-mt-28 border-b border-white/[.1] py-14"><h2>Safety model</h2><p>mj-fte treats cleanup as an explicit decision. Its safety model is built from four simple boundaries:</p><ol><li><strong>Read first.</strong> Scanning and analysis do not modify files.</li><li><strong>Allowlist candidates.</strong> The cleaner looks only at known temporary, cache, and package-residue locations.</li><li><strong>Protect system paths.</strong> Windows system locations are not cleanup candidates.</li><li><strong>Ask before action.</strong> A destructive command requires confirmation. Dry-run is always available.</li></ol><Callout title="Local by default" icon={LockKeyhole}>Scan results remain on your machine. mj-fte has no account requirement, background process, or telemetry.</Callout></section>
    <section id="workflow" className="scroll-mt-28 border-b border-white/[.1] py-14"><h2>Typical workflow</h2><p>A good cleanup is a short conversation with your machine, not a single opaque button.</p><div className="not-prose my-8 space-y-3"><Workflow number="01" title="Inspect" code="mj-fte scan --safe" text="Understand where the space is going." /><Workflow number="02" title="Preview" code="mj-fte clean --dry-run" text="Review every candidate before anything changes." /><Workflow number="03" title="Decide" code="mj-fte clean" text="Confirm the cleanup only when the report makes sense." /></div></section>
    <section id="history" className="scroll-mt-28 border-b border-white/[.1] py-14"><h2>Version history</h2><p>The project stays intentionally focused as it grows.</p><div className="not-prose mt-7 space-y-5"><DocRelease version="0.4.0" date="14 Feb 2025" title="Safer cleanup flow" text="Added safe scanning posture, protected-path reporting, and a dry-run summary." current /><DocRelease version="0.3.1" date="06 Jan 2025" title="Sharper reports" text="Improved directory grouping and stable output for PowerShell redirection." /><DocRelease version="0.3.0" date="18 Dec 2024" title="The first public cut" text="Disk analysis, cache detection, and the initial command surface." /></div><p className="mt-8"><ExternalAnchor href={CHANGELOG} label="link-doc-changelog" className="text-cyan-200 no-underline hover:text-cyan-100">Read the complete changelog <ExternalLink size={13} className="inline" /></ExternalAnchor></p></section>
    <section id="faq" className="scroll-mt-28 py-14"><h2>FAQ</h2>{FAQS.map((faq) => <details key={faq.question} className="not-prose group border-b border-white/[.1] py-5"><summary className="flex cursor-pointer list-none items-center justify-between gap-4 text-sm font-medium text-slate-200"><span>{faq.question}</span><ChevronDown size={16} className="text-slate-500 transition group-open:rotate-180" /></summary><p className="mt-4 max-w-2xl text-sm leading-7 text-slate-400">{faq.answer}</p></details>)}</section>
  </div>;
}

function CodeBlock({ code }: { code: string }) {
  return <div className="not-prose group relative my-7 overflow-hidden rounded-lg border border-white/[.11] bg-[#090c12]"><div className="flex items-center justify-between border-b border-white/[.08] px-4 py-2.5"><span className="font-mono text-[10px] uppercase tracking-wide text-slate-600">powershell</span><CopyButton value={code} compact /></div><pre className="overflow-x-auto p-4 font-mono text-xs leading-7 text-cyan-100/85"><code>{code}</code></pre></div>;
}

function Callout({ title, icon: Icon, children }: { title: string; icon: typeof CircleCheck; children: ReactNode }) {
  return <div className="not-prose my-8 flex gap-3 rounded-lg border border-cyan-200/15 bg-cyan-200/[.045] p-4"><Icon size={17} className="mt-0.5 shrink-0 text-cyan-200" /><div><p className="font-display text-sm font-medium text-slate-200">{title}</p><p className="mt-1 text-sm leading-6 text-slate-400">{children}</p></div></div>;
}

function Workflow({ number, title, code, text }: { number: string; title: string; code: string; text: string }) {
  return <div className="grid gap-3 rounded-lg border border-white/[.1] bg-white/[.025] p-4 sm:grid-cols-[34px_100px_1fr] sm:items-center"><span className="font-mono text-[11px] text-slate-600">{number}</span><span className="font-display text-sm text-slate-200">{title}</span><div><code className="font-mono text-xs text-cyan-100">{code}</code><p className="mt-1 text-xs text-slate-500">{text}</p></div></div>;
}

function DocRelease({ version, date, title, text, current }: { version: string; date: string; title: string; text: string; current?: boolean }) {
  return <div className="flex gap-4 border-l border-white/[.14] pl-5"><div className="mt-1 h-2 w-2 shrink-0 rounded-full bg-cyan-200" /><div><div className="flex flex-wrap items-center gap-3"><code className="text-sm text-slate-200">v{version}</code>{current && <span className="font-mono text-[9px] uppercase tracking-wide text-cyan-200">current</span>}<span className="font-mono text-[10px] text-slate-600">{date}</span></div><p className="mt-2 text-sm text-slate-400">{title} — {text}</p></div></div>;
}

function Footer() {
  return <footer className="border-t border-white/[.08] px-5 py-10 lg:px-8"><div className="mx-auto flex max-w-7xl flex-col justify-between gap-8 sm:flex-row sm:items-end"><div><Logo /><p className="mt-3 max-w-xs text-xs leading-6 text-slate-600">A transparent disk cleaner for Windows power users. Open source, local-first, careful by default.</p></div><div className="flex flex-wrap gap-x-6 gap-y-3 font-mono text-[11px] text-slate-500"><ExternalAnchor href={GITHUB} label="link-footer-github" className="hover:text-slate-200">GitHub</ExternalAnchor><ExternalAnchor href={PYPI} label="link-footer-pypi" className="hover:text-slate-200">PyPI</ExternalAnchor><ExternalAnchor href={ISSUES} label="link-footer-issues" className="hover:text-slate-200">Issues</ExternalAnchor><Link href="/docs" data-testid="link-footer-docs" className="hover:text-slate-200">Docs</Link><Link href="/privacy" data-testid="link-footer-privacy" className="hover:text-slate-200">Privacy</Link></div></div><div className="mx-auto mt-9 flex max-w-7xl justify-between border-t border-white/[.07] pt-5 font-mono text-[10px] text-slate-700"><span>mj-fte / made for careful machines</span><span>MIT</span></div></footer>;
}

function Privacy() {
  return <div className="site-shell noise"><Navbar docs /><main className="px-5 pb-28 pt-32 lg:px-8"><div className="mx-auto max-w-3xl"><Eyebrow icon={BookOpen}>Legal</Eyebrow><h1 className="font-display text-4xl font-medium tracking-[-.055em] text-slate-100 sm:text-5xl">Privacy Policy</h1><p className="mt-4 font-mono text-xs text-slate-600">Last updated: August 21, 2026</p><div className="mt-12 space-y-10 text-[15px] leading-8 text-slate-400"><section><h2 className="font-display text-xl font-medium text-slate-100">1. The CLI never phones home</h2><p>mj-fte runs entirely on your machine. Scanning, classification and cleaning happen locally — your file names, folder structures and drive contents are never uploaded, transmitted or sold by us. Authentication tokens stay in <code className="rounded bg-white/[.06] px-1.5 py-0.5 font-mono text-[13px] text-cyan-100">%APPDATA%\MJ_FTE</code> on your own disk.</p></section><section><h2 className="font-display text-xl font-medium text-slate-100">2. Website analytics</h2><p>This website uses Google Analytics 4 to understand aggregate traffic (pages visited, country, device type). Google Analytics sets cookies and collects data per Google's privacy policy. You can opt out with the <ExternalAnchor href="https://tools.google.com/dlpage/gaoptout" label="link-ga-optout" className="text-cyan-200 hover:text-cyan-100">Google Analytics opt-out browser add-on</ExternalAnchor>.</p></section><section><h2 className="font-display text-xl font-medium text-slate-100">3. Advertising</h2><p>We may display ads served by Google AdSense in the future. Third-party vendors, including Google, use cookies to serve ads based on prior visits to this or other websites. You can disable personalized advertising in <ExternalAnchor href="https://adssettings.google.com" label="link-ads-settings" className="text-cyan-200 hover:text-cyan-100">Google Ads Settings</ExternalAnchor>.</p></section><section><h2 className="font-display text-xl font-medium text-slate-100">4. Google OAuth</h2><p>Sign-in uses Google OAuth. We receive only your name, email and profile picture, stored locally for display purposes. We never post, read mail or access other Google services.</p></section><section><h2 className="font-display text-xl font-medium text-slate-100">5. Contact</h2><p>Questions about this policy? Open an issue at <ExternalAnchor href={ISSUES} label="link-privacy-issues" className="text-cyan-200 hover:text-cyan-100">github.com/syed-mujtaba-stack/mj-fte/issues</ExternalAnchor>.</p></section></div></div></main><Footer /></div>;
}

function Router() {
  const [location] = useLocation();
  useEffect(() => { if (!location.includes('#')) window.scrollTo(0, 0); }, [location]);
  useEffect(() => { trackPageview(location); }, [location]);
  return <RoutedErrorBoundary><Switch><Route path="/" component={Home} /><Route path="/docs" component={Docs} /><Route path="/privacy" component={Privacy} /><Route component={NotFound} /></Switch></RoutedErrorBoundary>;
}

function RoutedErrorBoundary({ children }: { children: ReactNode }) {
  const [location] = useLocation();
  return <ErrorBoundary resetKey={location}>{children}</ErrorBoundary>;
}

function App() {
  return <QueryClientProvider client={queryClient}><TooltipProvider><WouterRouter base={import.meta.env.BASE_URL.replace(/\/$/, '')}><Router /></WouterRouter><Toaster /></TooltipProvider></QueryClientProvider>;
}

export default App;