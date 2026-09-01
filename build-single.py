#!/usr/bin/env python3
"""Build the single-file, offline copy of the app.

    python3 build-single.py            -> dist/flow-metrics.html

WHY THIS EXISTS
The hosted app is four files (index.html, chart.min.js, theme.css, sw.js) plus a
manifest and icons, served from GitHub Pages. That is the right shape for a site.
It is the wrong shape for "send me the app" — a person who downloads index.html
on its own gets an unstyled page with no charts.

This script folds the palette and Chart.js into index.html and takes out the
parts that only mean something on a served origin, so what comes out is ONE file
that runs by double-clicking it, with no server, no network and no install.

WHAT IT IS NOT
It is not a build step for the hosted app, and nothing here is committed as a
source file. index.html stays the thing that is written and tested; dist/ is
generated, gitignored, and rebuilt whenever the app changes. If you find
yourself editing the output, you are editing the wrong file.

WHAT CHANGES, AND WHY EACH ONE
  1. theme.css and chart.min.js are inlined.       — nothing left to fetch
  2. manifest + icon links are dropped.            — no install off a file://
  3. The service-worker registration is dropped.   — a downloaded file IS the cache
  4. Share is dropped.                             — see the note above the cut
  5. The sibling-app link is dropped.              — it needs the network
  6. Privacy, How it works, NOTICE and LICENCE
     become in-page dialogs.                       — the files aren't there to link to
  7. The CSP is tightened to inline-only.          — see the note above it

EVERY EDIT IS COUNTED. Each replace() below asserts how many times it must match,
so if index.html moves under this script the build fails loudly instead of
quietly shipping an app with a live Share button or an un-inlined stylesheet.

DEPENDENCY: the README is rendered with the `markdown` package (pip3 install
markdown). It is a BUILD-time dependency only — nothing is added to the page that
the app does not already carry, and the output stays free of third-party script.
"""

import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, 'dist')
OUT_NAME = 'flow-metrics.html'
REPO = 'team-dashboard'
APP_TITLE = 'Flow Metrics'

# Sections of the README that describe behaviour THIS build does not have.
# A "How it works" window that explains a Share button the reader cannot see is
# a wrong answer, not a harmless extra — so they come out, and the note at the
# top of the window says the copy has been trimmed and where the full one lives.
DROP_README_SECTIONS = [
    'Sharing a Read-Only Link',
    'Installing It',
    'Working Offline',
]


def fail(msg):
    print('build-single: ' + msg, file=sys.stderr)
    raise SystemExit(1)


class Doc:
    """The page under construction, with a replace() that counts."""

    def __init__(self, text):
        self.text = text
        self.edits = []

    def sub(self, pattern, repl, count, label, regex=False):
        if regex:
            new, n = re.subn(pattern, lambda m: repl, self.text)
        else:
            n = self.text.count(pattern)
            new = self.text.replace(pattern, repl)
        if n != count:
            fail('%s: expected %d match(es), found %d. index.html has moved '
                 'under this script — read the change before touching this line.'
                 % (label, count, n))
        self.text = new
        self.edits.append('%-34s %d' % (label, n))

    def cut_span(self, a, b, label):
        """Cut an already-located span, by index."""
        if a < 0 or b <= a:
            fail('%s: no span to cut' % label)
        self.text = self.text[:a] + self.text[b:]
        self.edits.append('%-34s %d chars' % (label, b - a))

    def cut_between(self, start, end, label, include_end=False):
        """Cut from the first `start` to the following `end`, both required."""
        a = self.text.find(start)
        if a < 0:
            fail('%s: start anchor not found' % label)
        b = self.text.find(end, a)
        if b < 0:
            fail('%s: end anchor not found' % label)
        if include_end:
            b += len(end)
        removed = b - a
        self.text = self.text[:a] + self.text[b:]
        self.edits.append('%-34s %d chars' % (label, removed))


def read(name):
    with open(os.path.join(HERE, name), encoding='utf-8') as fh:
        return fh.read()


# ── The four documents ──────────────────────────────────────────────────────
# They go into <template> elements rather than JS strings. A template's contents
# are parsed as HTML but never rendered, so nothing here needs escaping for a
# script context — which matters, because a stray `</script>` or an unbalanced
# `<!--` inside 120KB of README would take the whole app's script down with it.
# The only sequence a template cannot contain is its own closing tag, and that
# is asserted before anything is written.

def gh_slug(text, seen):
    """GitHub's heading-anchor slug, so the README's own table of contents
    still lands. Lowercase, punctuation dropped, spaces to hyphens, and a
    numeric suffix for a repeat — the same tie-break GitHub uses."""
    s = re.sub(r'[^\w\- ]', '', text.lower(), flags=re.UNICODE)
    s = s.replace(' ', '-')
    n = seen.get(s, 0)
    seen[s] = n + 1
    return s if n == 0 else '%s-%d' % (s, n)


def render_readme():
    try:
        import markdown
    except ImportError:
        fail('the `markdown` package is needed to render the README.\n'
             '  pip3 install markdown')

    md = read('README.md')

    # Drop the sections this build does not have. A section runs from its own
    # `## ` heading to the next one at the same level.
    parts = re.split(r'(?m)^(?=## )', md)
    kept, dropped = [], []
    for part in parts:
        head = part.split('\n', 1)[0].lstrip('# ').strip()
        if head in DROP_README_SECTIONS:
            dropped.append(head)
            continue
        kept.append(part)
    missing = [s for s in DROP_README_SECTIONS if s not in dropped]
    if missing:
        fail('README sections to drop not found: %s' % ', '.join(missing))
    md = ''.join(kept)

    body = markdown.markdown(md, extensions=['tables', 'fenced_code', 'sane_lists'])

    # Heading ids, prefixed so they cannot collide with an element in the app.
    seen = {}
    slugs = {}

    def add_id(m):
        level, attrs, text = m.group(1), m.group(2), m.group(3)
        plain = re.sub(r'<[^>]+>', '', text)
        slug = gh_slug(html.unescape(plain), seen)
        slugs[slug] = 'doc-' + slug
        return '<h%s id="doc-%s"%s>%s</h%s>' % (level, slug, attrs, text, level)

    body = re.sub(r'<h([1-6])([^>]*)>(.*?)</h\1>', add_id, body, flags=re.S)

    # In-document links: point them at the prefixed ids. A link whose target
    # was in a dropped section loses its href rather than sitting there looking
    # clickable and doing nothing.
    def fix_anchor(m):
        target = m.group(1)
        if target in slugs:
            return 'href="#%s"' % slugs[target]
        return 'data-dead-link="1"'

    body = re.sub(r'href="#([^"]+)"', fix_anchor, body)

    # Repo-relative links become absolute: they are external either way, and an
    # unresolvable relative href from a file:// page is just a broken link.
    body = re.sub(
        r'href="(?!https?:|#|data:)([^":]+)"',
        lambda m: 'href="https://github.com/eagleadams86/%s/blob/main/%s" '
                  'target="_blank" rel="noopener noreferrer"' % (REPO, m.group(1)),
        body)

    # No images: img-src in this build is data: only, so a remote badge would be
    # a blocked request and an empty box.
    body = re.sub(r'<img\b[^>]*>', '', body)

    note = (
        '<p class="doc-note">This is the single-file copy of %s — one HTML file '
        'that runs from your own disk, with no server and no network. Sharing '
        'read-only links, installing it as an app and the offline cache belong '
        'to the hosted version, so those sections are not in this copy of the '
        'guide. Everything else below describes what is in front of you.</p>'
        % APP_TITLE)
    return note + body, dropped


def render_plain(name):
    return '<pre class="doc-pre">%s</pre>' % html.escape(read(name))


def strip_html_comments(text):
    """Take the comments out, in a LOOP rather than one pass.

    One pass over a multi-character delimiter can leave a NEW opener behind that
    the pass has already gone by — the family's suites carry the same helper,
    written the same way, for the same reason.

    It runs before <main> is located, and that is not tidiness: privacy.html's
    own notes DISCUSS the markup ("the back link stays outside <main> — it is
    navigation, not the document"), so a plain search for the tag finds the
    sentence about it and lifts half a comment into the reader's window. It did.
    """
    prev = None
    while prev != text:
        prev = text
        text = re.sub(r'<!--.*?-->', '', text, flags=re.S)
    return text


def render_privacy():
    src = strip_html_comments(read('privacy.html'))
    a, b = src.find('<main'), src.find('</main>')
    if a < 0 or b < 0:
        fail('privacy.html: no <main> to lift')
    inner = src[src.find('>', a) + 1:b]
    # The page's own "back to the app" nav means nothing inside a dialog.
    inner = re.sub(r'<nav\b.*?</nav>', '', inner, flags=re.S)
    # Its own <h1> is the window's title, and the window already carries it —
    # two identical headings, one above the other, is what a reader reads as a
    # mistake. The effective-date line under it stays; that is the document
    # saying which version of itself this is.
    inner, n = re.subn(r'<h1\b.*?</h1>', '', inner, count=1, flags=re.S)
    if n != 1:
        fail('privacy.html: no <h1> to fold into the window title')
    if '<main' in inner or '</footer>' in inner:
        fail('privacy.html: lifted more than the policy')
    return inner.strip()


# ── The dialog that shows them ──────────────────────────────────────────────
DOCS_CSS = """
<style id="single-file-docs">
/* The four documents that used to be links out of the footer. Prose measure,
   not the app's dialog width: this is a document to read, and 1100px of body
   text is a wall. Matches the 720px privacy.html itself uses. */
#docsDialog { max-width: 760px; }
#docsDialog h2 { font-size: var(--fs-lg); margin: 0 0 14px; }
#docsDialog .docs-body { max-height: min(68vh, 640px); overflow-y: auto;
  overscroll-behavior: contain; font-size: var(--fs-sm);
  color: var(--text-secondary); line-height: var(--lh-base); padding-right: 6px; }
.docs-body h1 { font-size: var(--fs-lg); color: var(--text-primary); margin: 0 0 6px; }
.docs-body h2 { font-size: var(--fs-md); color: var(--text-primary); margin: 26px 0 6px; }
.docs-body h3 { font-size: var(--fs-base); color: var(--text-primary); margin: 18px 0 4px; }
.docs-body h4, .docs-body h5, .docs-body h6 {
  font-size: var(--fs-sm); color: var(--text-primary); margin: 14px 0 4px; }
.docs-body p, .docs-body li { color: var(--text-secondary); }
.docs-body ul, .docs-body ol { padding-left: 20px; }
.docs-body a { color: var(--accent); }
.docs-body strong { color: var(--text-primary); }
.docs-body code, .docs-body .doc-pre {
  font-family: var(--font-mono, ui-monospace, SFMono-Regular, Menlo, monospace);
  font-size: var(--fs-xs); }
.docs-body pre, .docs-body .doc-pre {
  background: var(--surface-alt); border: 1px solid var(--border);
  border-radius: 8px; padding: 10px 12px; overflow-x: auto; white-space: pre-wrap; }
.docs-body table { border-collapse: collapse; width: 100%; margin: 10px 0;
  font-size: var(--fs-xs); display: block; overflow-x: auto; }
.docs-body th, .docs-body td {
  border: 1px solid var(--border); padding: 5px 8px; text-align: left;
  vertical-align: top; }
.docs-body th { color: var(--text-primary); }
.docs-body blockquote { margin: 10px 0; padding-left: 12px;
  border-left: 2px solid var(--border-strong); }
.docs-body .card { background: var(--surface-alt); border: 1px solid var(--border);
  border-radius: 10px; padding: 12px 16px; margin: 12px 0; }
.docs-body .doc-note { background: var(--surface-alt); border: 1px solid var(--border);
  border-radius: 10px; padding: 12px 16px; margin: 0 0 18px; }
/* A dead in-document link (its section is not in this copy) keeps its words and
   loses its affordance — no underline, no pointer, no colour that says "click". */
.docs-body [data-dead-link] { color: inherit; text-decoration: none; }
/* The footer links became buttons. Same words, same muted colour, same hover as
   the anchors they replace — the rules are copied from .privacy-links a. */
.privacy-links .linkbtn { background: none; border: 0; padding: 0; margin: 0;
  font: inherit; color: var(--text-muted); text-decoration: underline;
  cursor: pointer; }
.privacy-links .linkbtn:hover { color: var(--text-secondary); }
@media print {
  .privacy-links .linkbtn { text-decoration: none; color: #000 !important; }
  #docsDialog { display: none !important; }
}
</style>
"""

DOCS_HTML = """
<!-- ── The four documents ─────────────────────────────────────────────────────
     On the hosted site these are four links out of the footer: privacy.html
     beside the app, and three files on GitHub. A downloaded file can reach none
     of them, and a footer that promises a privacy policy it cannot show is
     worse than no footer — so the documents travel inside the page and open
     here. The <template>s below carry them; nothing is rendered until asked. -->
<dialog id="docsDialog" aria-labelledby="docsTitle">
  <h2 id="docsTitle"></h2>
  <div id="docsBody" class="docs-body"></div>
  <div class="row" style="justify-content:flex-end;margin-top:18px">
    <button class="btn primary" id="docsCloseBtn" type="button">Close</button>
  </div>
</dialog>
__TEMPLATES__
<script>
(function () {
  var TITLES = {
    privacy: 'Privacy Policy',
    readme:  'How It Works',
    notice:  'Ownership and Provenance',
    license: 'Licence'
  };
  var dlg   = document.getElementById('docsDialog');
  var body  = document.getElementById('docsBody');
  var title = document.getElementById('docsTitle');
  var shown = null;

  function open(which) {
    var tpl = document.getElementById('doc-tpl-' + which);
    if (!tpl) return;
    /* Cloned, not innerHTML: the markup is built into this file at build time,
       so there is nothing to sanitise, and a clone keeps it that way — no
       string ever becomes markup at runtime. Re-cloned per open so a scrolled
       document opens at the top the second time, like every other window. */
    if (shown !== which) {
      body.textContent = '';
      body.appendChild(tpl.content.cloneNode(true));
      shown = which;
    }
    title.textContent = TITLES[which] || '';
    body.scrollTop = 0;
    dlg.showModal();
  }

  document.addEventListener('click', function (e) {
    var btn = e.target.closest ? e.target.closest('[data-doc]') : null;
    if (btn) { e.preventDefault(); open(btn.getAttribute('data-doc')); }
  });
  document.getElementById('docsCloseBtn').addEventListener('click', function () {
    dlg.close();
  });

  /* Backdrop click closes, like every other window in the app. Press and
     release must BOTH be outside, so a drag that starts on the text and ends
     off the edge does not count as a click on the backdrop. */
  var startedOutside = false;
  function outside(e) {
    var r = dlg.getBoundingClientRect();
    return e.clientX < r.left || e.clientX > r.right ||
           e.clientY < r.top  || e.clientY > r.bottom;
  }
  dlg.addEventListener('mousedown', function (e) { startedOutside = outside(e); });
  dlg.addEventListener('click', function (e) {
    if (startedOutside && outside(e)) dlg.close();
    startedOutside = false;
  });

  /* The README's own table of contents. Scroll inside the window instead of
     navigating: a real jump would write to location.hash, and the app watches
     the hash. */
  body.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a[href^="#"]') : null;
    if (!a) return;
    e.preventDefault();
    var el = document.getElementById(a.getAttribute('href').slice(1));
    if (el) el.scrollIntoView({ block: 'start' });
  });
})();
</script>
"""


def build():
    doc = Doc(read('index.html'))

    # ── 1. Everything the page loads, folded in ─────────────────────────────
    css = read('theme.css')
    js = read('chart.min.js')
    if '</script' in js.lower():
        fail('chart.min.js contains a closing script tag and cannot be inlined')
    doc.sub('<link rel="stylesheet" href="theme.css">',
            '<style>\n/* theme.css, inlined by build-single.py — edit the file, '
            'not this copy. */\n' + css + '\n</style>', 1, 'inline theme.css')
    doc.sub('<script src="chart.min.js"></script>',
            '<script>\n/* chart.min.js, inlined by build-single.py. */\n' + js
            + '\n</script>', 1, 'inline chart.min.js')

    # The brand mark in the header is an <img> pointing at favicon.ico. The head
    # already carries the same picture as an inline SVG data URI for the tab
    # icon, so the header wears that instead of a file that is not there — one
    # picture, already in the page, and no second copy to keep in step.
    icon = re.search(r'<link rel="icon" type="image/svg\+xml" href="(data:[^"]+)">',
                     doc.text)
    if not icon:
        fail('no inline SVG icon in <head> for the header mark to reuse')
    doc.sub('<img src="favicon.ico?v=1" width="22" height="22" alt=""',
            '<img src="%s" width="22" height="22" alt=""' % icon.group(1), 1,
            'brand mark to inline icon')

    # ── 2. Things that only exist on a served origin ────────────────────────
    doc.sub('\n<link rel="manifest" href="manifest.webmanifest">', '', 1,
            'drop manifest link')
    doc.sub('\n<link rel="alternate icon" href="favicon.ico?v=1">', '', 1,
            'drop favicon link')
    doc.sub('\n<link rel="apple-touch-icon" href="apple-touch-icon.png">', '', 1,
            'drop apple-touch-icon')

    # The whole registration <script>. A downloaded file cannot register a
    # worker and does not need one — it IS the cache. Left in, it would sit
    # there logging "Offline unavailable" on every open.
    i = doc.text.find('serviceWorker.register')
    if i < 0:
        fail('service-worker registration not found')
    sw_a = doc.text.rfind('<script>', 0, i)
    sw_b = doc.text.find('</script>', i)
    doc.cut_span(sw_a, sw_b + len('</script>'), 'drop service worker')

    # ── 3. Share ────────────────────────────────────────────────────────────
    # A share link is location.origin + location.pathname + the payload. From a
    # file:// page that is a path on the sender's own disk: a link that looks
    # real and works for nobody. The feature comes out rather than shipping a
    # button that produces one.
    #
    # WHAT IS REMOVED: the button, the window, and every line that wires them
    # up at load time. WHAT IS LEFT: the encoder and the read-only view code,
    # which are unreachable once the prefix below can never match a fragment.
    # They are not excised because they share helpers (plural, andList) with the
    # rest of the app, and cutting them would mean rewriting code the test suite
    # covers to produce a file the test suite does not.
    doc.sub('    <button class="btn small" id="shareBtn" type="button" '
            'title="Create a read-only link to show someone your figures">'
            '<span aria-hidden="true">↗</span> Share</button>\n', '', 1,
            'drop Share button')
    doc.cut_between('<!-- ── Share a read-only link', '</dialog>',
                    'drop Share window', include_end=True)
    doc.cut_between("$('shareSelectAll').addEventListener('click', () => {",
                    'function shareTeamsPicked() {', 'drop Select All wiring')
    # This one takes the backdrop handler and the window's own controls with it,
    # which is why nothing is left holding a node that is no longer there.
    doc.cut_between("$('shareKeep').addEventListener('change', e => {",
                    '/* ══════════════════════════════════════════════════════'
                    '═════════════════════\n   9b. CLEAN UP OLD DATA',
                    'drop Share wiring')
    doc.sub("['manageBtn', 'dataBtn', 'shareBtn', 'settingsBtn']",
            "['manageBtn', 'dataBtn', 'settingsBtn']", 1, 'drop Share from viewOnly')
    # The inbound half. A prefix that cannot begin a fragment makes shareToken
    # null and viewOnly false for good — one edit, rather than unpicking every
    # branch that reads them — and keeps the hashchange watcher quiet, which a
    # bare `shareToken = null` would not: it compares against this prefix and
    # would reload the page in a loop on a pasted link.
    doc.sub("const SHARE_PREFIX = '#share=';",
            "/* Share links are not in the single-file build. A fragment always\n"
            "   starts with '#', so this can never match: shareToken stays null,\n"
            "   viewOnly stays false, and the hashchange watcher stays quiet. */\n"
            "const SHARE_PREFIX = 'no-share-links-in-this-build';", 1,
            'disable inbound share links')

    # ── 4. The sibling-app link ─────────────────────────────────────────────
    # It points at GitHub Pages. Offline it is a dead end, and this build has no
    # way to know whether the reader has the other file.
    doc.cut_between('<!-- A real <a>, not a button that navigates', '</a>',
                    'drop sibling-app link', include_end=True)

    # ── 5. The footer links become dialogs ──────────────────────────────────
    doc.sub('<p class="privacy privacy-links"><a href="privacy.html">Privacy policy</a> '
            '&middot;\n    <a href="https://github.com/eagleadams86/%s" '
            'target="_blank" rel="noopener noreferrer">How it works</a></p>' % REPO,
            '<p class="privacy privacy-links">'
            '<button type="button" class="linkbtn" data-doc="privacy">Privacy policy</button> '
            '&middot;\n    <button type="button" class="linkbtn" data-doc="readme">'
            'How it works</button></p>', 1, 'privacy + how-it-works buttons')
    doc.sub('<a href="https://github.com/eagleadams86/%s/blob/main/NOTICE"\n'
            '       target="_blank" rel="noopener noreferrer">independent personal '
            'project</a>' % REPO,
            '<button type="button" class="linkbtn" data-doc="notice">'
            'independent personal project</button>', 1, 'NOTICE button')
    doc.sub('<a href="https://github.com/eagleadams86/%s/blob/main/LICENSE"\n'
            '       target="_blank" rel="noopener noreferrer">MIT licensed</a>' % REPO,
            '<button type="button" class="linkbtn" data-doc="license">'
            'MIT licensed</button>', 1, 'LICENSE button')

    # ── 6. A CSP with no origin in it at all ────────────────────────────────
    # Nothing is fetched any more, so nothing needs to be allowed. 'self' comes
    # out on purpose: every file:// page shares one origin with every other file
    # on the disk, so 'self' is a far wider promise here than it is on the site.
    old_csp = re.search(r'<meta http-equiv="Content-Security-Policy"[^>]*>', doc.text)
    if not old_csp:
        fail('no CSP meta tag found')
    doc.sub(old_csp.group(0),
            '<meta http-equiv="Content-Security-Policy" content="default-src '
            "'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; "
            "img-src data:; connect-src 'none'; frame-src 'none'; base-uri "
            "'none'; form-action 'none'\">", 1, 'tighten CSP')

    # ── 7. The documents ────────────────────────────────────────────────────
    readme_html, dropped = render_readme()
    docs = {
        'privacy': render_privacy(),
        'readme': readme_html,
        'notice': render_plain('NOTICE'),
        'license': render_plain('LICENSE'),
    }
    templates = []
    for key, content in docs.items():
        if '</template' in content.lower():
            fail('%s contains a closing template tag' % key)
        templates.append('<template id="doc-tpl-%s">%s</template>' % (key, content))
    block = DOCS_HTML.replace('__TEMPLATES__', '\n'.join(templates))

    doc.sub('</head>', DOCS_CSS + '</head>', 1, 'add document styles')
    doc.sub('</body>', block + '\n</body>', 1, 'add document windows')

    # ── Out ─────────────────────────────────────────────────────────────────
    for stray in ['chart.min.js', 'theme.css', 'manifest.webmanifest',
                  'apple-touch-icon.png', 'privacy.html', 'favicon.ico']:
        # Relative references only. An absolute URL to the hosted site is an
        # ordinary external link — the README is full of them — and is not a
        # thing this file is failing to carry.
        if re.search(r'(?:src|href)="(?!https?:|data:|#)[^"]*%s' % re.escape(stray),
                     doc.text):
            fail('a reference to %s survived — the output is not self-contained'
                 % stray)
    if 'id="shareBtn"' in doc.text:
        fail('the Share button survived')

    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, OUT_NAME)
    with open(out, 'w', encoding='utf-8') as fh:
        fh.write(doc.text)

    print('built %s  (%.2f MB)' % (out, os.path.getsize(out) / 1048576.0))
    for line in doc.edits:
        print('   ' + line)
    print('   README sections dropped: %s' % ', '.join(dropped))


if __name__ == '__main__':
    build()
