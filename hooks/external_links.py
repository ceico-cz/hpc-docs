"""Open external links in a new browser tab.

Adds target="_blank" rel="noopener" to every link in the page content that points to another
site. Links to this site (site_url), relative links and links that already set a target are
left alone. The theme's own links (header, footer) are not part of the page content.
"""
import re

LINK = re.compile(r'<a\s[^>]*href="(https?://[^"]+)"[^>]*>')


def on_page_content(html, page, config, files):
    own = (config.get("site_url") or "").rstrip("/")

    def fix(m):
        tag, url = m.group(0), m.group(1)
        if " target=" in tag or (own and url.startswith(own)):
            return tag
        return tag[:-1] + ' target="_blank" rel="noopener">'

    return LINK.sub(fix, html)
