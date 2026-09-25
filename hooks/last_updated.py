"""Show a "last updated" date on every page.

The date is the page's last git commit, ignoring bulk commits that touched every page
without changing its content (the Wiki.js import, reformatting). Pages with no other commit
use the Wiki.js edit date stored in front matter (wikijs_updated).

Add the hash of any future bulk commit (e.g. a final re-sync from Wiki.js) to BULK_COMMITS.
"""
import datetime
import subprocess

BULK_COMMITS = {
    "f02778ea9dc8df77689966ec7199cfbf4390c891",  # initial import from Wiki.js
    "27bd6cf",                                   # redesign: callout titles, wikijs_updated field
    "3c093a8",                                   # copy-edit of titles and headings
}


def _is_bulk(sha):
    return any(sha.startswith(b) or b.startswith(sha) for b in BULK_COMMITS)


def _git_date(path):
    try:
        out = subprocess.run(
            ["git", "log", "--format=%H %cs", "--", path],
            capture_output=True, text=True, check=True,
        ).stdout.split("\n")
    except (OSError, subprocess.CalledProcessError):
        return None
    for line in out:
        if line.strip():
            sha, date = line.split()
            if not _is_bulk(sha):
                return date
    return None


def on_page_markdown(markdown, page, config, files):
    date = _git_date(page.file.abs_src_path) or page.meta.get("wikijs_updated")
    if date:
        if isinstance(date, str):
            date = datetime.date.fromisoformat(date)
        page.meta["revision_date"] = f"Last updated {date:%-d %B %Y}"
    return markdown
