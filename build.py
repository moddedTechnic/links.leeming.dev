import shutil
from pathlib import Path
from typing import Any

import yaml

BASE_DIR = Path(__file__).parent
LINKS_FILE = BASE_DIR / 'links.yml'
PUBLIC_DIR = BASE_DIR / 'public'

DIST_DIR = BASE_DIR / 'dist'
INDEX_FILE = DIST_DIR / 'index.html'

PAGE = '''
<!DOCTYPE html>
<html lang="en-gb">
    <head>
        <meta charset="UTF-8"/>
        <meta name="description" content="Useful links relating to Jonathan Leeming"/>
        <meta name="viewport" content="width=device-width"/>
        <title>Jonathan Leeming | Links</title>

        <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
        <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
        <link rel="manifest" href="/site.webmanifest">
        <link href="style.css" rel="stylesheet">
    </head>
    <body>
        <main>
            <h1>Links</h1>
            <nav>
                <ul>
{links}
                </ul>
            </nav>
        </main>

        <footer>
            <p>Icons from <a href="https://phosphoricons.com/">Phosphor Icons</a>.</p>
            <p><a href="https://leeming.dev">Jonathan Leeming</a> © 2025</p>
        </footer>
    </body>
</html>
'''


SECTION = '''
<h{level}>{title}</h{level}>
<ul>
{content}
</ul>
'''

CARD = '''
<li>
    <a href="https://{url}">
        {image}
        <span>{title}</span>
    </a>
</li>
'''


def format_link(link: dict[str, Any], level=2):
    if 'section' in link:
        title = link['section']
        links = link.get('links', [])
        return SECTION.format(
            title=title,
            level=level,
            content='\n'.join(format_link(l, level+1) for l in links),
        ).strip()
    url = link['url']
    title = link.get('title', url)
    if icon := link.get('icon'):
        image = f'<img src="icons/{icon}.svg" alt="">'
    else:
        image = '<span></span>'
    return CARD.format(
        url=url,
        title=title,
        image=image,
    ).strip()


def main():
    with LINKS_FILE.open('r') as f:
        links = yaml.safe_load(f)
    page = PAGE.format(
        links='\n'.join(format_link(l) for l in links)
    ).strip()

    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    shutil.copytree(PUBLIC_DIR, DIST_DIR)
    INDEX_FILE.write_text(page)


if __name__ == '__main__':
    exit(main())

