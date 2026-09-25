"""Show a "last updated" date on every page.

Pages edited in git after the Wiki.js import use their last commit date. Pages untouched
since the import use the Wiki.js edit date stored in front matter (wikijs_updated), so the
import commit itself does not make every page look freshly updated.
"""
import datetime
import subprocess

IMPORT_COMMIT = "f02778ea9dc8df77689966ec7199cfbf4390c891"


def _git_date(path):
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", f"{IMPORT_COMMIT}..HEAD", "--", path],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    return out or None


def on_page_markdown(markdown, page, config, files):
    date = _git_date(page.file.abs_src_path) or page.meta.get("wikijs_updated")
    if date:
        if isinstance(date, str):
            date = datetime.date.fromisoformat(date)
        page.meta["revision_date"] = f"Last updated {date:%-d %B %Y}"
    return markdown
