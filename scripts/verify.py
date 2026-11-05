#! /usr/bin/env python3
"""Verification helper: lints all repo checks in one pass.

Checks (offline, no external dependencies):
  1. Every docs/*.md file exists and internal cross-references resolve.
  2. site/index.html has balanced tags and references style.css + app.js.
  3. app.js passes node --check (skipped if node is absent).
  4. site/style.css has matching braces.
  5. LICENSE contains the exact required copyright line; README credits
     Asdale Dynamics, LLC.
  6. No secrets-looking strings (api keys, private keys) snuck into files.
  7. site/app.js + site/style.css + site/index.html are shipped together
     (assets exist on disk before any 'build'; there is no build step to fail).
"""

import re
import shutil
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
failures = []


def check(name, condition, detail=""):
    if condition:
        print(f"  ok   {name}")
    else:
        print(f"  FAIL {name} {detail}")
        failures.append(name)


VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input",
             "link", "meta", "param", "source", "track", "wbr"}


class TagBalance(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID_TAGS:
            # <script> content is treated as CDATA by HTMLParser, so it
            # self-closes via handle_endonly if content has no '<'.
            self._open(tag)

    def _open(self, tag):
        self.stack.append(tag) if hasattr(self, "stack") else None

    # simpler: reimplement stack here
    stack = []

    def handle_starttag_real(self, tag):
        pass

    def handle_endtag(self, tag):
        if tag in VOID_TAGS:
            return
        if not self.stack:
            self.errors.append(f"closing </{tag}> with empty stack")
            return
        if self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.errors.append(f"mismatch: expected </{self.stack[-1]}>, got </{tag}>")


def html_balance(path):
    text = path.read_text(encoding="utf-8")
    stack = []
    errors = []
    # Remove <script>...</script> and <style>...</style> inner content
    stripped = re.sub(r"<script\b.*?</script>", "<script></script>", text, flags=re.S | re.I)
    stripped = re.sub(r"<style\b.*?</style>", "<style></style>", stripped, flags=re.S | re.I)
    for m in re.finditer(r"<(/?)([a-zA-Z][a-zA-Z0-9-]*)\b[^>]*?(/?)>", stripped):
        closing, tag, selfclose = m.group(1), m.group(2).lower(), m.group(3)
        if tag in VOID_TAGS or selfclose:
            continue
        if closing:
            if not stack:
                errors.append(f"stray </{tag}>")
            elif stack[-1] != tag:
                errors.append(f"expected </{stack[-1]}>, found </{tag}>")
                stack.pop() if stack and stack[-1] == tag else None
            else:
                stack.pop()
        else:
            stack.append(tag)
    if stack:
        errors.append(f"unclosed tags: {stack}")
    return errors


def main():
    docs = ROOT / "docs"
    site = ROOT / "site"

    print("[1] docs present and cross-links resolve")
    expected = ["00-index.md", "01-what-are-data-brokers.md", "02-state-removal-rights.md",
                "03-walkthrough.md", "04-request-templates.md", "05-opt-out-pages.md",
                "06-renewals-calendar.md", "07-stay-off-going-forward.md"]
    for name in expected:
        check(f"docs/{name} exists", (docs / name).is_file())
    all_doc_text = "\n".join(
        p.read_text(encoding="utf-8") for p in sorted(docs.glob("*.md"))
    )
    refs = set(re.findall(r"`?(\d{2}-[a-z0-9-]+\.md)`?", all_doc_text))
    for ref in sorted(refs):
        check(f"docs cross-ref {ref} -> file exists", (docs / ref).is_file())

    print("[2] site/index.html")
    html_errors = html_balance(site / "index.html")
    check("index.html tags balanced", not html_errors, "; ".join(html_errors))
    html_text = (site / "index.html").read_text(encoding="utf-8")
    check("index.html references style.css", "style.css" in html_text)
    check("index.html references app.js", "app.js" in html_text)
    check("index.html has no external network resources",
          not re.search(r"(?:https?:)?//[^\"'\s>]*\.(?:js|css|png|jpg|woff|ico)",
                        html_text),
          "found external asset reference — the site must be fully offline")

    print("[3] site/app.js")
    app_js = site / "app.js"
    check("app.js exists", app_js.is_file())
    if shutil.which("node") and app_js.is_file():
        r = subprocess.run(["node", "--check", str(app_js)],
                           capture_output=True, text=True)
        check("node --check site/app.js", r.returncode == 0, r.stderr.strip())
    else:
        print("  skip node --check (node not available)")

    print("[4] site/style.css")
    css = (site / "style.css").read_text(encoding="utf-8")
    check("style.css braces balanced", css.count("{") == css.count("}"))
    check("style.css checkable anchors present",
          ".checklist" in css and ".progress-fill" in css)

    print("[5] LICENSE / README")
    lic = (ROOT / "LICENSE").read_text(encoding="utf-8")
    check("LICENSE exact copyright line",
          "Copyright (c) 2026 Asdale Dynamics, LLC" in lic)
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    check("README credits Asdale Dynamics, LLC",
          "Asdale Dynamics, LLC" in readme)
    check("README is not legal advice (disclaimer present)",
          "Education only" in readme or "not legal advice" in readme)

    print("[6] no secrets / keys pattern scan")
    secret_patterns = [
        r"(?i)(api[_-]?key|secret|password|passwd|token)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}",
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
        r"AKIA[0-9A-Z]{16}",
        r"ghp_[A-Za-z0-9]{30,}",
    ]
    blob = "\n".join(
        p.read_text(encoding="utf-8", errors="ignore")
        for p in list(ROOT.rglob("*")) if p.is_file() and ".git" not in p.parts
    )
    leaks = [pat for pat in secret_patterns if re.search(pat, blob)]
    check("no secrets-pattern matches", not leaks, str(leaks))

    print("[7] personal-data hygiene in templates")
    # Templates must contain only bracket placeholders, not fake-but-real names
    fake_names = ["John Doe", "Jane Doe"]  # do not even ship these
    check("templates avoid placeholder personal names",
          all(n not in all_doc_text for n in fake_names))
    check("site affirms no-scraping policy (manual visits only)",
          "no scraping" in html_text.lower())
    check("site affirms manual, no automated submissions",
          "no automated submissions" in html_text.lower())

    print()
    if failures:
        print(f"FAILED: {len(failures)} check(s): {failures}")
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
