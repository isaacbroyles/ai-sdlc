#!/usr/bin/env python3
"""Supply-chain lint for this skills marketplace.

Skills are instructions an agent runs with the installer's permissions, so
changes that hide content or add executable surface must be deliberate.
Standard library only; run from the repo root: python3 .github/scripts/lint.py
"""
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
errors = []


def err(path, msg):
    errors.append(f"{path}: {msg}")


files = subprocess.run(
    ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, text=True, check=True
).stdout.split("\0")
files = [f for f in files if f]

# --- File-type allowlist: no executable surface without a deliberate change ---
PLUGIN_EXT = {".md", ".json", ".png"}
FORBIDDEN_NAMES = {".mcp.json", "hooks.json"}
FORBIDDEN_DIRS = {"hooks", "bin", "scripts", "node_modules"}
for f in files:
    p = Path(f)
    if p.parts[0] != "plugins":
        continue
    if p.name in FORBIDDEN_NAMES or FORBIDDEN_DIRS & set(p.parts):
        err(f, "hooks, MCP servers and scripts are not allowed in plugins without maintainer sign-off")
    elif p.suffix.lower() not in PLUGIN_EXT:
        err(f, f"file type {p.suffix or p.name!r} is not on the plugin allowlist {sorted(PLUGIN_EXT)}")
    if (ROOT / f).stat().st_mode & 0o111:
        err(f, "executable bit set")

# --- Hidden content: invisible/bidi characters and HTML comments ---
TEXT_EXT = {".md", ".json", ".yml", ".yaml", ".py", ".txt"}
ALLOWED_URL_HOSTS = {
    "github.com", "docs.github.com", "docs.claude.com", "claude.ai",
    "claude.com", "img.shields.io", "code.claude.com", "anthropic.com", "docs.anthropic.com",
}
URL_RE = re.compile(r"https?://[^\s)>\]\"'`]+")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
DANGEROUS_IN_CODE = [
    (re.compile(r"\b(curl|wget)\b[^\n|]*\|\s*(sudo\s+)?(ba|z|da)?sh\b"), "pipes a download into a shell"),
    (re.compile(r"base64\s+(-d|--decode)"), "decodes base64"),
    (re.compile(r"--dangerously-\S+"), "uses a --dangerously-* flag"),
    (re.compile(r"--admin\b"), "bypasses protections with --admin"),
    (re.compile(r"--no-verify\b"), "skips hooks with --no-verify"),
    (re.compile(r"\beval\s"), "uses eval"),
    (re.compile(r"\bchmod\s+\+?[0-7]*x"), "makes a file executable"),
]

for f in files:
    p = ROOT / f
    if p.suffix.lower() not in TEXT_EXT:
        continue
    text = p.read_text(encoding="utf-8")
    for ch in sorted(set(text)):
        cat = unicodedata.category(ch)
        if cat in ("Cf", "Co", "Cn") or (cat == "Cc" and ch not in "\n\r\t"):
            err(f, f"hidden/control character U+{ord(ch):04X} ({unicodedata.name(ch, 'unnamed')})")
    if p.suffix.lower() == ".md":
        if "<!--" in text:
            err(f, "HTML comment (can hide instructions from reviewers)")
        in_fence = False
        for n, line in enumerate(text.splitlines(), 1):
            if FENCE_RE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                for rx, why in DANGEROUS_IN_CODE:
                    if rx.search(line):
                        err(f"{f}:{n}", f"code block {why}")
    for m in URL_RE.finditer(text):
        host = (urlparse(m.group(0)).hostname or "").lower()
        if not any(host == h or host.endswith("." + h) for h in ALLOWED_URL_HOSTS):
            err(f, f"URL host {host!r} is not on the allowlist (edit lint.py in a reviewed change)")

# --- Manifests and skills ---
for f in files:
    if f.endswith(".json"):
        try:
            json.loads((ROOT / f).read_text(encoding="utf-8"))
        except ValueError as e:
            err(f, f"invalid JSON: {e}")

mp = ROOT / ".claude-plugin/marketplace.json"
if mp.exists():
    for plugin in json.loads(mp.read_text()).get("plugins", []):
        src = plugin.get("source")
        if not (isinstance(src, str) and src.startswith("./plugins/") and ".." not in src):
            err(".claude-plugin/marketplace.json",
                f"plugin {plugin.get('name')!r} source must be a local ./plugins/ path, got {src!r}")
        elif not (ROOT / src / ".claude-plugin/plugin.json").exists():
            err(".claude-plugin/marketplace.json", f"{src} has no .claude-plugin/plugin.json")

for f in files:
    p = Path(f)
    if p.name == "SKILL.md":
        m = re.match(r"---\n(.*?)\n---\n", (ROOT / f).read_text(encoding="utf-8"), re.S)
        if not m:
            err(f, "missing YAML frontmatter")
            continue
        name = re.search(r"^name:\s*(\S+)\s*$", m.group(1), re.M)
        if not name or name.group(1) != p.parent.name:
            err(f, "frontmatter `name` must match the skill directory name")
        if not re.search(r"^description:\s*\S", m.group(1), re.M):
            err(f, "frontmatter `description` is required")

if errors:
    print("\n".join(errors))
    print(f"\n{len(errors)} problem(s) found")
    sys.exit(1)
print(f"OK: {len(files)} tracked files checked")
