# CEICO HPC Services documentation

Sources of <https://hpc.ceico.cz>, built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
and published by GitHub Pages.

## Editing

Pages are Markdown files under `docs/`; the URL follows the file path
(`docs/getting-started/ssh.md` → `/getting-started/ssh/`). Images live next to the pages
(e.g. `docs/systems/phoebe/pictures/`) and are linked relatively.

The navigation is defined in `nav.yml`: top-level entries are the tabs in the header, nested
entries the sidebar. Add every new page there.

Each page shows a "Last updated" date: its last git commit, or for pages not touched since
the import, the Wiki.js edit date from the `wikijs_updated` front-matter field
(`hooks/last_updated.py`).

### Adding a system

Systems are listed on `docs/systems/index.md` and have their own section under the
"Systems" tab in `nav.yml`. For a new system, create its pages under `docs/systems/<name>/`
(an overview first), add a row to the right table in `docs/systems/index.md` (CEICO clusters
or third-party systems), and add a section to `nav.yml`. Add a card to "Our systems" on the
home page only for systems most users need.

### Releasing the MetaCentrum helper script

The Kerberos guide (`docs/systems/metacentrum/kerberos.md`) tells users to download
`docs/systems/metacentrum/metacentrum-kinit` from a git tag, not from `main`, so an
unreviewed change on `main` never reaches anyone's machine. After changing the script:

```bash
git tag -a metacentrum-kinit-vX.Y.Z -m "metacentrum-kinit X.Y.Z"
git push origin metacentrum-kinit-vX.Y.Z
```

then replace the old tag in both URLs in the guide (the `curl` command and the link above it).

The home page (`docs/index.md`) is hand-designed; its styles are in `docs/assets/extra.css`.

Useful syntax:

```markdown
!!! info "Note"
    Callout box (also: warning, success, danger).

=== "Tab one"

    Content of the first tab.

=== "Tab two"

    Content of the second tab.

![Alt text](pictures/photo.jpg){ style="width:35%" }
```

On GitHub every page has an edit button; changes go through a pull request, which is
built (but not deployed) by CI.

## Local preview

```bash
uv venv --python 3.14 .venv
uv pip install --python .venv -r requirements.txt
DISABLE_MKDOCS_2_WARNING=true .venv/bin/mkdocs serve     # http://127.0.0.1:8000
```

`mkdocs build --strict` fails on broken internal links; CI runs the same check.

## Deployment

`.github/workflows/deploy.yml` builds on every push to `main` and deploys to GitHub Pages.
`docs/CNAME` sets the custom domain `hpc.ceico.cz`.

Old Wiki.js URLs (`/en/<path>`, `/home`) redirect to the new pages (`hooks/wikijs_redirects.py`).

## Migration from Wiki.js

`tools/convert_wikijs.py` produced the initial content from a JSON dump of the Wiki.js
SQLite database plus its disk-storage asset export. It converts Wiki.js-specific markup
(callouts, tabsets, link lists, image sizes, absolute links) and the two CKEditor HTML pages.
It is kept for reference and for a final re-sync before the switch-over; after that, edit
`docs/` directly. A re-sync keeps the hand-designed home page and `nav.yml`
(`--write-nav` regenerates the Wiki.js navigation).
