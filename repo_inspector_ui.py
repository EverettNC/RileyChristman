"""
Riley Christman — Repo Inspector UI
====================================
A popup window with:
  • URL input field (paste any GitHub repo URL)
  • Instructions field (tell Riley what to look for)
  • GrinderOCR unredaction on all Python files found
  • Results spoken aloud via ShortyVoiceEngineV2 (pyttsx3)
  • Results displayed in a scrollable text panel
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import re
import os
import sys
import logging

# ── Path setup ────────────────────────────────────────────────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

# ── Riley imports ─────────────────────────────────────────────────────────────
try:
    from riley_grinder import GrinderOCR, FinancialGrinder
    _GRINDER_OK = True
except Exception as e:
    _GRINDER_OK = False
    logging.warning(f"Grinder unavailable: {e}")

try:
    from shorty_voice_engine_v2 import ShortyVoiceEngineV2
    _VOICE = ShortyVoiceEngineV2()
    _VOICE_OK = True
except Exception as e:
    _VOICE_OK = False
    logging.warning(f"Voice unavailable: {e}")

try:
    import requests
    _REQUESTS_OK = True
except ImportError:
    _REQUESTS_OK = False

# ── Colours & fonts (Riley palette) ──────────────────────────────────────────
BG       = "#0d0d0d"
PANEL    = "#141414"
ACCENT   = "#00ffe1"       # Riley cyan
ACCENT2  = "#ff6b6b"       # warning red
TEXT     = "#e8e8e8"
MUTED    = "#666666"
FONT_UI  = ("Helvetica Neue", 12)
FONT_MONO= ("Menlo", 11)
FONT_H1  = ("Helvetica Neue", 16, "bold")
FONT_BTN = ("Helvetica Neue", 13, "bold")

# ─────────────────────────────────────────────────────────────────────────────
# GitHub helpers
# ─────────────────────────────────────────────────────────────────────────────

def parse_github_url(url: str):
    """Extract owner/repo from any GitHub URL variant."""
    url = url.strip().rstrip("/")
    m = re.search(r'github\.com[:/]([^/]+)/([^/\s]+?)(?:\.git)?$', url)
    if m:
        return m.group(1), m.group(2)
    return None, None


def fetch_repo_tree(owner: str, repo: str):
    """Fetch flat file tree via GitHub API (no auth needed for public repos)."""
    api = f"https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
    headers = {"Accept": "application/vnd.github+json",
               "X-GitHub-Api-Version": "2022-11-28"}
    r = requests.get(api, headers=headers, timeout=15)
    r.raise_for_status()
    return r.json().get("tree", [])


def fetch_file_content(owner: str, repo: str, path: str) -> str:
    """Fetch raw file content from GitHub."""
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/{path}"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.text


def fetch_repo_meta(owner: str, repo: str) -> dict:
    """Fetch basic repo metadata."""
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Accept": "application/vnd.github+json"}
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    return r.json()


# ─────────────────────────────────────────────────────────────────────────────
# Core inspection logic (runs in background thread)
# ─────────────────────────────────────────────────────────────────────────────

def inspect_repo(owner: str, repo: str, instructions: str,
                 on_progress, on_done, on_error):
    """
    Full inspection pipeline:
      1. Fetch repo metadata
      2. Fetch file tree
      3. Run GrinderOCR on every .py file
      4. Apply user instructions as keyword filter
      5. Return structured report
    """
    try:
        lines = []

        # ── 1. Repo metadata ──────────────────────────────────────────────
        on_progress("📡 Fetching repo metadata...")
        meta = fetch_repo_meta(owner, repo)
        lines.append(f"REPO:        {meta.get('full_name', f'{owner}/{repo}')}")
        lines.append(f"DESCRIPTION: {meta.get('description') or '(none)'}")
        lines.append(f"LANGUAGE:    {meta.get('language') or 'unknown'}")
        lines.append(f"STARS:       {meta.get('stargazers_count', 0):,}")
        lines.append(f"FORKS:       {meta.get('forks_count', 0):,}")
        lines.append(f"SIZE:        {meta.get('size', 0):,} KB")
        lines.append(f"PRIVATE:     {meta.get('private', False)}")
        lines.append(f"DEFAULT BRANCH: {meta.get('default_branch', 'main')}")
        lines.append("")

        # ── 2. File tree ──────────────────────────────────────────────────
        on_progress("🌲 Fetching file tree...")
        tree = fetch_repo_tree(owner, repo)
        py_files  = [f for f in tree if f["type"] == "blob"
                     and f["path"].endswith(".py")]
        all_files = [f for f in tree if f["type"] == "blob"]

        lines.append(f"TOTAL FILES: {len(all_files)}")
        lines.append(f"PYTHON FILES: {len(py_files)}")
        lines.append("")

        # Show top-level structure
        top_dirs = sorted(set(
            p["path"].split("/")[0] for p in all_files
        ))
        lines.append("TOP-LEVEL STRUCTURE:")
        for d in top_dirs[:20]:
            lines.append(f"  {d}")
        lines.append("")

        # ── 3. Instruction-based keyword filter ───────────────────────────
        instr_lower = instructions.lower().strip()
        instr_keywords = [w for w in re.findall(r'\b\w{3,}\b', instr_lower)
                          if w not in {"the", "and", "for", "all", "any",
                                       "look", "find", "check", "get", "show"}]

        if instr_keywords:
            lines.append(f"INSTRUCTION KEYWORDS: {', '.join(instr_keywords)}")
            lines.append("")

        # ── 4. GrinderOCR sweep ───────────────────────────────────────────
        grinder_hits  = []
        keyword_hits  = []
        crypto_files  = []
        grinder       = GrinderOCR() if _GRINDER_OK else None
        fin_grinder   = FinancialGrinder() if _GRINDER_OK else None

        cap = min(len(py_files), 40)   # cap at 40 files to stay fast
        on_progress(f"🔍 Running Grinder on {cap} Python files...")

        for i, fnode in enumerate(py_files[:cap]):
            path = fnode["path"]
            on_progress(f"  [{i+1}/{cap}] {path}")
            try:
                content = fetch_file_content(owner, repo, path)
            except Exception:
                continue

            # Keyword search from instructions
            if instr_keywords:
                for kw in instr_keywords:
                    if kw in content.lower():
                        snippet_idx = content.lower().find(kw)
                        snippet = content[max(0, snippet_idx-60):snippet_idx+80].strip()
                        keyword_hits.append({
                            "file": path,
                            "keyword": kw,
                            "snippet": snippet
                        })

            # Crypto / security markers
            crypto_markers = ["encrypt", "decrypt", "cipher", "aes", "rsa",
                               "kyber", "pq_layer", "chacha", "vigenere",
                               "stegan", "signature", "hmac", "hashlib"]
            if any(m in content.lower() for m in crypto_markers):
                crypto_files.append(path)

            # GrinderOCR unredaction
            if grinder:
                result = grinder.surgical_sweep(content)
                if result.unmasked:
                    for frag in result.fragments[:5]:  # top 5 per file
                        grinder_hits.append({
                            "file": path,
                            "original": frag["original"],
                            "unredacted": frag["unredacted"]
                        })

        # ── 5. Build report ───────────────────────────────────────────────
        if crypto_files:
            lines.append(f"CRYPTO / SECURITY FILES ({len(crypto_files)}):")
            for cf in crypto_files:
                lines.append(f"  ✦ {cf}")
            lines.append("")

        if keyword_hits:
            lines.append(f"INSTRUCTION MATCHES ({len(keyword_hits)} hits):")
            seen = set()
            for h in keyword_hits[:15]:
                key = f"{h['file']}:{h['keyword']}"
                if key not in seen:
                    seen.add(key)
                    lines.append(f"\n  FILE: {h['file']}")
                    lines.append(f"  KEYWORD: '{h['keyword']}'")
                    snip = h['snippet'].replace('\n', ' ')
                    lines.append(f"  ...{snip[:120]}...")
            lines.append("")

        if grinder_hits:
            lines.append(f"GRINDER UNREDACTION ({len(grinder_hits)} fragments):")
            for h in grinder_hits[:10]:
                lines.append(f"  FILE: {h['file']}")
                lines.append(f"    {h['original']}  →  {h['unredacted']}")
            lines.append("")

        if not keyword_hits and not grinder_hits:
            lines.append("GRINDER: No redactions or instruction matches found.")
            lines.append("Repo appears clean on surface scan.")
            lines.append("")

        # ── Voice summary ─────────────────────────────────────────────────
        voice_summary = (
            f"Repo {owner} slash {repo} inspected. "
            f"{len(all_files)} total files, {len(py_files)} Python. "
        )
        if crypto_files:
            voice_summary += f"{len(crypto_files)} files with cryptographic markers. "
        if keyword_hits:
            voice_summary += f"{len(keyword_hits)} matches on your instructions. "
        if grinder_hits:
            voice_summary += f"Grinder found {len(grinder_hits)} redaction fragments. "
        if not keyword_hits and not grinder_hits:
            voice_summary += "No redactions or keyword hits detected. Repo looks clean. "

        report = "\n".join(lines)
        on_done(report, voice_summary)

    except requests.exceptions.HTTPError as e:
        on_error(f"HTTP Error: {e}\n\nIs the repo public and the URL correct?")
    except Exception as e:
        on_error(f"Inspection failed: {type(e).__name__}: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# UI
# ─────────────────────────────────────────────────────────────────────────────

class RepoInspectorUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Riley — Repo Inspector")
        self.root.configure(bg=BG)
        self.root.geometry("860x720")
        self.root.resizable(True, True)
        self._build()

    def _build(self):
        root = self.root

        # ── Header ────────────────────────────────────────────────────────
        hdr = tk.Frame(root, bg=BG)
        hdr.pack(fill="x", padx=24, pady=(20, 0))

        plus_lbl = tk.Label(hdr, text="⊕", font=("Helvetica Neue", 28, "bold"),
                            fg=ACCENT, bg=BG)
        plus_lbl.pack(side="left", padx=(0, 10))

        title = tk.Label(hdr, text="REPO INSPECTOR",
                         font=FONT_H1, fg=ACCENT, bg=BG)
        title.pack(side="left")

        sub = tk.Label(hdr, text="powered by Riley Christman + GrinderOCR",
                       font=("Helvetica Neue", 10), fg=MUTED, bg=BG)
        sub.pack(side="left", padx=14, pady=(4, 0))

        ttk.Separator(root, orient="horizontal").pack(
            fill="x", padx=24, pady=10)

        # ── URL field ─────────────────────────────────────────────────────
        url_frame = tk.Frame(root, bg=BG)
        url_frame.pack(fill="x", padx=24, pady=(0, 6))

        tk.Label(url_frame, text="GitHub Repo URL",
                 font=FONT_UI, fg=TEXT, bg=BG).pack(anchor="w")

        self.url_var = tk.StringVar()
        url_entry = tk.Entry(url_frame, textvariable=self.url_var,
                             font=FONT_MONO, bg=PANEL, fg=ACCENT,
                             insertbackground=ACCENT,
                             relief="flat", bd=6)
        url_entry.pack(fill="x", ipady=8)
        url_entry.focus_set()

        # ── Instructions field ────────────────────────────────────────────
        instr_frame = tk.Frame(root, bg=BG)
        instr_frame.pack(fill="x", padx=24, pady=(0, 12))

        tk.Label(instr_frame, text="Instructions for Riley  (what to look for)",
                 font=FONT_UI, fg=TEXT, bg=BG).pack(anchor="w")

        self.instr_text = tk.Text(instr_frame, height=3,
                                  font=FONT_UI, bg=PANEL, fg=TEXT,
                                  insertbackground=ACCENT,
                                  relief="flat", bd=6, wrap="word")
        self.instr_text.pack(fill="x")
        self.instr_text.insert("1.0",
            "Look for redacted names, crypto implementations, security issues")

        # ── Buttons ───────────────────────────────────────────────────────
        btn_frame = tk.Frame(root, bg=BG)
        btn_frame.pack(fill="x", padx=24, pady=(0, 10))

        self.inspect_btn = tk.Button(
            btn_frame,
            text="⊕  INSPECT",
            font=FONT_BTN,
            bg=ACCENT, fg=BG,
            activebackground="#00ccb8",
            relief="flat", bd=0,
            padx=20, pady=8,
            cursor="hand2",
            command=self._start_inspection
        )
        self.inspect_btn.pack(side="left", padx=(0, 10))

        self.speak_btn = tk.Button(
            btn_frame,
            text="🔊  SPEAK RESULTS",
            font=FONT_BTN,
            bg=PANEL, fg=ACCENT,
            activebackground="#1a1a1a",
            relief="flat", bd=0,
            padx=20, pady=8,
            cursor="hand2",
            state="disabled",
            command=self._speak_results
        )
        self.speak_btn.pack(side="left", padx=(0, 10))

        self.clear_btn = tk.Button(
            btn_frame,
            text="✕  CLEAR",
            font=FONT_BTN,
            bg=PANEL, fg=MUTED,
            activebackground="#1a1a1a",
            relief="flat", bd=0,
            padx=20, pady=8,
            cursor="hand2",
            command=self._clear
        )
        self.clear_btn.pack(side="left")

        # ── Status bar ────────────────────────────────────────────────────
        self.status_var = tk.StringVar(value="Paste a GitHub URL and hit Inspect.")
        status_bar = tk.Label(root, textvariable=self.status_var,
                              font=("Helvetica Neue", 10), fg=MUTED, bg=BG,
                              anchor="w")
        status_bar.pack(fill="x", padx=26, pady=(0, 4))

        # ── Results panel ─────────────────────────────────────────────────
        result_frame = tk.Frame(root, bg=BG)
        result_frame.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        self.result_box = scrolledtext.ScrolledText(
            result_frame,
            font=FONT_MONO,
            bg=PANEL, fg=TEXT,
            insertbackground=ACCENT,
            relief="flat", bd=6,
            wrap="word",
            state="disabled"
        )
        self.result_box.pack(fill="both", expand=True)

        # colour tags
        self.result_box.tag_configure("header",  foreground=ACCENT,
                                      font=("Menlo", 11, "bold"))
        self.result_box.tag_configure("hit",     foreground="#ffdd57")
        self.result_box.tag_configure("error",   foreground=ACCENT2)
        self.result_box.tag_configure("muted",   foreground=MUTED)
        self.result_box.tag_configure("grinder", foreground="#c084fc")

        # internal state
        self._last_voice_summary = ""
        self._inspecting = False

    # ── Inspection flow ───────────────────────────────────────────────────────

    def _start_inspection(self):
        if self._inspecting:
            return

        url = self.url_var.get().strip()
        if not url:
            self._set_status("⚠  Paste a GitHub URL first.", error=True)
            return

        owner, repo = parse_github_url(url)
        if not owner:
            self._set_status("⚠  Couldn't parse that URL. Try: https://github.com/user/repo", error=True)
            return

        if not _REQUESTS_OK:
            self._set_status("⚠  requests library not installed.", error=True)
            return

        instructions = self.instr_text.get("1.0", "end").strip()

        self._clear_results()
        self._set_status(f"🔍 Inspecting {owner}/{repo}...")
        self._set_inspect_state(True)

        self._append(f"RILEY CHRISTMAN — REPO INSPECTION\n", tag="header")
        self._append(f"{'═'*60}\n", tag="muted")
        self._append(f"TARGET: {owner}/{repo}\n")
        self._append(f"INSTRUCTIONS: {instructions or '(none)'}\n\n")

        threading.Thread(
            target=inspect_repo,
            args=(owner, repo, instructions,
                  self._on_progress,
                  self._on_done,
                  self._on_error),
            daemon=True
        ).start()

    def _on_progress(self, msg: str):
        self.root.after(0, lambda: self._set_status(msg))
        self.root.after(0, lambda: self._append(f"{msg}\n", tag="muted"))

    def _on_done(self, report: str, voice_summary: str):
        self._last_voice_summary = voice_summary

        def _update():
            self._append(f"\n{'═'*60}\n", tag="muted")
            self._append("INSPECTION COMPLETE\n\n", tag="header")

            # colour-code the report lines
            for line in report.splitlines():
                if line.startswith("GRINDER"):
                    self._append(line + "\n", tag="grinder")
                elif "KEYWORD" in line or "MATCH" in line or "→" in line:
                    self._append(line + "\n", tag="hit")
                elif line.startswith("REPO") or line.startswith("LANGUAGE") or \
                     line.startswith("STARS") or line.startswith("TOTAL") or \
                     line.startswith("CRYPTO"):
                    self._append(line + "\n", tag="header")
                else:
                    self._append(line + "\n")

            self._set_status("✓ Done. Click 'Speak Results' to hear the summary.")
            self._set_inspect_state(False)
            self.speak_btn.config(state="normal")

            # Auto-speak
            self._speak_voice(voice_summary)

        self.root.after(0, _update)

    def _on_error(self, msg: str):
        def _update():
            self._append(f"\n⚠  ERROR: {msg}\n", tag="error")
            self._set_status("⚠  Inspection failed.", error=True)
            self._set_inspect_state(False)
        self.root.after(0, _update)

    # ── Voice ─────────────────────────────────────────────────────────────────

    def _speak_voice(self, text: str):
        if _VOICE_OK and text:
            threading.Thread(
                target=lambda: _VOICE.synthesize(text, mode="forensic"),
                daemon=True
            ).start()

    def _speak_results(self):
        if self._last_voice_summary:
            self._speak_voice(self._last_voice_summary)
        else:
            self._set_status("Nothing to speak yet.", error=False)

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _append(self, text: str, tag: str = None):
        self.result_box.config(state="normal")
        if tag:
            self.result_box.insert("end", text, tag)
        else:
            self.result_box.insert("end", text)
        self.result_box.see("end")
        self.result_box.config(state="disabled")

    def _clear_results(self):
        self.result_box.config(state="normal")
        self.result_box.delete("1.0", "end")
        self.result_box.config(state="disabled")

    def _clear(self):
        self._clear_results()
        self._last_voice_summary = ""
        self.speak_btn.config(state="disabled")
        self._set_status("Paste a GitHub URL and hit Inspect.")
        self._inspecting = False
        self.inspect_btn.config(state="normal", text="⊕  INSPECT")

    def _set_status(self, msg: str, error: bool = False):
        self.status_var.set(msg)
        # flash colour
        colour = ACCENT2 if error else MUTED

    def _set_inspect_state(self, running: bool):
        self._inspecting = running
        if running:
            self.inspect_btn.config(state="disabled", text="⟳  INSPECTING...")
        else:
            self.inspect_btn.config(state="normal", text="⊕  INSPECT")

    def run(self):
        self.root.mainloop()


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="[%(levelname)s] %(name)s: %(message)s")
    app = RepoInspectorUI()
    app.run()
