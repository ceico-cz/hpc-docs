"""Add a content hash to the URLs of our own stylesheets (extra_css).

GitHub Pages lets browsers cache files for 10 minutes, and extra.css keeps the same URL on
every deploy. A page whose new markup needs new CSS can then be drawn with the old stylesheet.
Appending ?v=<hash of the file> gives every changed file a new URL, so browsers fetch it
again; an unchanged file keeps its URL and stays cached. Entries that are not files under
docs/ (such as external URLs) are left alone.
"""
import hashlib
from pathlib import Path


def _versioned(path, docs_dir):
    if "://" in path or "?" in path:
        return path
    source = Path(docs_dir) / path
    if not source.is_file():
        return path
    digest = hashlib.sha256(source.read_bytes()).hexdigest()[:10]
    return f"{path}?v={digest}"


def on_config(config):
    docs_dir = config["docs_dir"]
    config["extra_css"] = [_versioned(p, docs_dir) for p in config["extra_css"]]
    return config
