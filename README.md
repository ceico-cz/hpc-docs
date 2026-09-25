# PHOEBE compute system wiki

Sources of <https://hpc.ceico.cz>, built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
and published by GitHub Pages.

## Editing

Pages are Markdown files under `docs/`; the URL follows the file path
(`docs/getting-there/ssh.md` → `/getting-there/ssh/`). Images live next to the pages
(e.g. `docs/phoebe_pictures/`) and are linked relatively.

The sidebar is defined in `nav.yml`. Pages not listed there are still built and reachable
through links, like in the old Wiki.js.

Useful syntax:

```markdown
!!! info ""
    Callout box (also: warning, success, danger).

=== "Tab one"

    Content of the first tab.

=== "Tab two"

    Content of the second tab.

![Alt text](../phoebe_pictures/photo.jpg){ style="width:35%" }
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
`docs/` directly.
