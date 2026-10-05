#!/usr/bin/env python3
"""Build crawlable PT/EN static pages from one shared HTML template."""
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = 'https://wildneyfonseca.com.br'
TEMPLATE = ROOT / 'templates' / 'home.html'
LANGUAGES = {
    'pt': {
        'html_lang': 'pt-BR', 'og_locale': 'pt_BR', 'url': f'{BASE_URL}/pt/',
        'language_label': 'Idioma',
        'ids': {'HOME':'inicio','PROBLEM':'problema','SOLUTIONS':'solucoes','HOW':'como-funciona','RESULTS':'resultados','ABOUT':'sobre','CONTACT':'contato'},
    },
    'en': {
        'html_lang': 'en', 'og_locale': 'en_US', 'url': f'{BASE_URL}/en/',
        'language_label': 'Language',
        'ids': {'HOME':'home','PROBLEM':'problem','SOLUTIONS':'solutions','HOW':'how-it-works','RESULTS':'results','ABOUT':'about','CONTACT':'contact'},
    },
}


def replace_localized_nodes(markup: str, content: dict[str, str], locale: str) -> str:
    keys = set(re.findall(r'\bdata-i="([\w-]+)"', markup))
    missing = sorted(keys - content.keys())
    if missing:
        raise ValueError(f'{locale}: missing translations for {", ".join(missing)}')

    # Each data-i node owns its inner HTML; nested emphasis and line breaks in a
    # translated value remain part of the shared semantic structure.
    for key in sorted(keys):
        pattern = re.compile(
            r'(<(?P<tag>[a-z][\w:-]*)(?=[^>]*\bdata-i="' + re.escape(key) + r'")[^>]*>)'
            r'[\s\S]*?(</(?P=tag)\s*>)', re.IGNORECASE
        )
        markup, count = pattern.subn(lambda m: m.group(1) + content[key] + m.group(3), markup)
        if count == 0:
            raise ValueError(f'{locale}: could not render data-i="{key}"')

    def replace_alt(match: re.Match) -> str:
        key = match.group(1)
        if key not in content:
            raise ValueError(f'{locale}: missing alt translation for {key}')
        return 'alt="' + html.escape(content[key], quote=True) + '"'

    markup = re.sub(r'data-i-alt="([\w-]+)"\s+alt="[^"]*"', replace_alt, markup)

    def replace_placeholder(match: re.Match) -> str:
        key = match.group(2)
        if key not in content:
            raise ValueError(f'{locale}: missing placeholder translation for {key}')
        return match.group(1) + html.escape(content[key], quote=True)

    markup = re.sub(r'(placeholder=")[^"]*("\s+data-i-placeholder="([\w-]+)")',
                    lambda m: 'placeholder="' + html.escape(content[m.group(3)], quote=True) + '"', markup)
    markup = re.sub(r'\sdata-i="[\w-]+"', '', markup)
    markup = re.sub(r'\sdata-i-placeholder="[\w-]+"', '', markup)
    return markup


def render(locale: str) -> str:
    language = LANGUAGES[locale]
    content = json.loads((ROOT / 'js' / 'content' / f'{locale}.json').read_text(encoding='utf-8'))
    markup = replace_localized_nodes(TEMPLATE.read_text(encoding='utf-8'), content, locale)
    values = {
        'LANG': language['html_lang'],
        'META_TITLE': content['metaTitle'],
        'META_DESCRIPTION': content['metaDescription'],
        'OG_LOCALE': language['og_locale'],
        'PAGE_URL': language['url'],
        'LANGUAGE_LABEL': language['language_label'],
        'MENU_OPEN': content['menuOpen'],
        'SCROLL_LABEL': content['scrollLabel'],
        'SOCIAL_LABEL': 'Redes sociais' if locale == 'pt' else 'Social media',
        'EMAIL_LABEL': 'E-mail' if locale == 'pt' else 'Email',
        'PT_CURRENT': ' aria-current="page"' if locale == 'pt' else '',
        'EN_CURRENT': ' aria-current="page"' if locale == 'en' else '',
        **{f'ID_{key}': value for key, value in language['ids'].items()},
    }
    for key, value in values.items():
        # These two values are controlled attribute fragments, not attribute
        # contents; keep their quotes literal so aria-current remains valid.
        replacement = str(value) if key in {'PT_CURRENT', 'EN_CURRENT'} else html.escape(str(value), quote=True)
        markup = markup.replace('{{' + key + '}}', replacement)
    unresolved = re.findall(r'\{\{[A-Z_]+\}\}', markup)
    if unresolved:
        raise ValueError(f'{locale}: unresolved template values: {unresolved}')
    return markup


def root_redirect() -> str:
    return '''<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="robots" content="noindex,follow">
  <link rel="canonical" href="https://wildneyfonseca.com.br/pt/">
  <meta http-equiv="refresh" content="0;url=/pt/">
  <title>Forgedriven</title>
</head>
<body><p><a href="/pt/">Acessar o site em português</a></p></body>
</html>
'''


def copy_public_files(destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for directory in ('CSS', 'images', 'assets', 'js'):
        source = ROOT / directory
        if source.exists():
            shutil.copytree(source, destination / directory, dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns('content', '*:Zone.Identifier'))
    for locale in LANGUAGES:
        target = destination / locale
        target.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / locale / 'index.html', target / 'index.html')
    (destination / 'index.html').write_text(root_redirect(), encoding='utf-8')
    (destination / '.nojekyll').touch()
    cname = ROOT / 'CNAME'
    if cname.exists():
        shutil.copy2(cname, destination / 'CNAME')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, help='Optional static deploy directory (for example dist)')
    args = parser.parse_args()

    for locale in LANGUAGES:
        target = ROOT / locale
        target.mkdir(parents=True, exist_ok=True)
        (target / 'index.html').write_text(render(locale), encoding='utf-8')
    (ROOT / 'index.html').write_text(root_redirect(), encoding='utf-8')
    if args.output:
        output = args.output if args.output.is_absolute() else ROOT / args.output
        copy_public_files(output)


if __name__ == '__main__':
    main()
