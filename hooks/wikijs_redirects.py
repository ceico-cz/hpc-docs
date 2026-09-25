"""Keep old Wiki.js URLs working: /en/<path> and /home redirect to the new pages."""
import os


def on_config(config):
    maps = config.plugins["redirects"].config["redirect_maps"]
    docs = config["docs_dir"]
    for root, _, files in os.walk(docs):
        for f in files:
            if not f.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(root, f), docs).replace(os.sep, "/")
            if rel == "index.md":
                maps.setdefault("home.md", rel)
                maps.setdefault("en/home.md", rel)
                maps.setdefault("en/index.md", rel)
            else:
                maps.setdefault(f"en/{rel}", rel)
    return config
