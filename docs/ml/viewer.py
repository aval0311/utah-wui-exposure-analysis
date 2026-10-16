"""Offline ML v1 presentation viewer. Python standard library only; no models."""
import argparse
import csv
import hashlib
import html
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(root=ROOT, active_notebook=False):
    manifest = json.loads((root / 'release_manifest.json').read_text(encoding='utf-8'))
    for row in manifest['files']:
        if active_notebook and row['path'] == 'wui_ml_v1_snapshot.ipynb':
            nb = json.loads((root/row['path']).read_text(encoding='utf-8'))
            inputs = [(c['cell_type'], ''.join(c['source'])) for c in nb['cells']]
            digest = hashlib.sha256(json.dumps(inputs,ensure_ascii=False).encode('utf-8')).hexdigest()
            if digest != manifest['notebook_input_sha256']:
                raise ValueError('Snapshot notebook source differs.')
            continue
        path = (root / row['path']).resolve()
        if not path.is_relative_to(root.resolve()) or not path.is_file():
            raise ValueError('Missing or unsafe release file: ' + row['path'])
        if path.stat().st_size != row['bytes'] or sha256(path) != row['sha256']:
            raise ValueError('Release file differs: ' + row['path'])
    return {'verified_files': len(manifest['files']), 'version': manifest['version'],
            'notebook_check': 'source only during execution' if active_notebook else 'full file',
            'new_model_fits': 0, 'new_predictions': 0}


def inline(text):
    text = html.escape(text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    return re.sub(r'`([^`]+)`', r'<code>\1</code>', text)


def markdown(text):
    """Render this release's limited Markdown subset, not arbitrary Markdown."""
    lines = text.splitlines(); out = []; i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1; continue
        if line.startswith('#'):
            n = len(line) - len(line.lstrip('#'))
            level = min(n + 1, 6)
            out.append(f'<h{level}>{inline(line[n:].strip())}</h{level}>'); i += 1
        elif line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r'[-: ]+', c) for c in cells): rows.append(cells)
                i += 1
            out.append('<div class="table-scroll" tabindex="0" role="region" aria-label="Scrollable results table"><table>')
            for j, cells in enumerate(rows):
                tag = 'th scope="col"' if j == 0 else 'td'; end = 'th' if j == 0 else 'td'
                out.append('<tr>' + ''.join(f'<{tag}>{inline(c)}</{end}>' for c in cells) + '</tr>')
            out.append('</table></div>')
        elif line.startswith('- '):
            out.append('<ul>')
            while i < len(lines) and lines[i].strip().startswith('- '):
                out.append('<li>' + inline(lines[i].strip()[2:]) + '</li>'); i += 1
            out.append('</ul>')
        else:
            words = [line]; i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].lstrip().startswith(('#', '|', '- ')):
                words.append(lines[i].strip()); i += 1
            out.append('<p>' + inline(' '.join(words)) + '</p>')
    return '\n'.join(out)


def page(root=ROOT):
    maps = json.loads((root/'data/map_descriptions.json').read_text(encoding='utf-8'))
    release = json.loads((root/'release.json').read_text(encoding='utf-8'))
    links = ' '.join(f'<a href="#map-{row["year"]}">{row["year"]}</a>' for row in maps)
    sections = []
    for row in maps:
        year = row['year']
        caption = inline(row['caption'])
        spatial = inline(row['spatial_description'])
        cells = ''.join('<tr><th scope="row">'+html.escape(c['county'])+'</th><td>'+str(c['eligible'])+
            '</td><td>'+f'{c["mean_probability_pct"]:.2f}%'+'</td><td>'+str(c['raw_top10'])+'</td></tr>' for c in row['counties'])
        sections.append(f'''<section class="annual" id="map-{year}" aria-labelledby="year-{year}">
<h2 id="year-{year}">{year} development holdout</h2>
<figure><a href="{row['image']}" aria-label="Open full resolution {year} map"><img width="2880" height="1980"
src="{row['image']}" alt="{html.escape(row['alt'], quote=True)}" aria-describedby="caption-{year}" loading="lazy"></a>
<figcaption id="caption-{year}">{caption}</figcaption></figure><p>{spatial}</p>
<div class="table-scroll" tabindex="0" role="region" aria-label="{year} county summary"><table><caption>{year} eligible county summaries</caption><thead><tr>
<th scope="col">County</th><th scope="col">Eligible cells</th><th scope="col">Mean conservative probability</th><th scope="col">Raw top 10% cells</th>
</tr></thead><tbody>{cells}</tbody></table></div><a href="#maps">Back to year navigation</a></section>''')
    docs = []
    for name, slug in [('narrative.md','study'), ('AREA_AUDIT.md','area'), ('SOURCES.md','sources'),
                       ('REPRODUCIBILITY.md','reproduce'), ('DATA_LICENSE.md','credits')]:
        docs.append(f'<section id="{slug}">{markdown((root/name).read_text(encoding="utf-8"))}</section>')
    return '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Utah wildfire occurrence development study, 2001–2021. Frozen ML v1 probability and ranking maps with area and reporting limitations.">
<title>Utah wildfire occurrence | ML v1 portfolio</title>
<style>
:root{color-scheme:light;--ink:#172b3a;--muted:#425568;--accent:#12595d;--line:#cbd5df}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f3f5f6;color:var(--ink);font:17px/1.65 system-ui,sans-serif}
header,main,footer{max-width:1120px;margin:auto;padding:32px}header{padding-top:58px}h1{font-size:clamp(30px,5vw,48px);line-height:1.12;max-width:850px;margin:12px 0 20px}h2{font-size:27px;line-height:1.3}h3{font-size:21px}
a{color:#09565f;text-underline-offset:3px}a:focus-visible,[tabindex]:focus-visible{outline:3px solid #a24d00;outline-offset:4px}.skip{position:absolute;left:-9999px}.skip:focus{left:12px;top:12px;background:white;padding:12px}
.eyebrow{font-size:14px;letter-spacing:.11em;text-transform:uppercase;color:var(--accent);font-weight:700}.scope{border-left:4px solid var(--accent);padding:12px 22px;background:#e3edef}.scope p{margin:4px 0}
nav{display:flex;flex-wrap:wrap;gap:10px 22px;margin:24px 0}section{background:white;border:1px solid var(--line);border-radius:8px;padding:28px;margin:0 0 28px;scroll-margin-top:20px}section p{max-width:90ch}figure{margin:12px 0}img{max-width:100%;height:auto;display:block}figcaption{padding:16px 0;color:var(--muted);font-size:15px}
table{border-collapse:collapse;width:100%;font-size:15px;margin:12px 0 20px}th,td{padding:10px 12px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}th{background:#edf2f4}caption{text-align:left;font-weight:700}.table-scroll{overflow-x:auto}code{font-size:.9em;overflow-wrap:anywhere;background:#edf2f4;padding:2px 4px}.downloads{background:#e3edef}footer{color:var(--muted);font-size:14px}
@media(max-width:640px){header,main,footer{padding:20px}section{padding:18px}table{min-width:560px}h2{font-size:23px}nav{gap:10px 16px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}@media print{body{background:white}nav,.skip{display:none}section{break-inside:avoid;border:0}.annual{break-before:page}}
</style></head><body><a class="skip" href="#main">Skip to content</a><header>
<div class="eyebrow">Adam Valentino · ML v1 · 1.0.0 · 16 October 2026</div><h1>Utah wildfire occurrence modeling</h1>
<p>A development case study of probability calibration, geographic validation and the effect of observation area on wildfire rankings.</p>
<div class="scope"><p><strong>Development 2001–2021 · Annual maps 2013–2021</strong></p><p>Recorded occurrence within county-clipped cells across Salt Lake, Utah and Washington counties. These years informed model selection; the results are not an independent final evaluation or an operational forecast.</p></div>
<nav aria-label="Main navigation"><a href="#study">Study</a><a href="#maps">Annual maps</a><a href="#area">Area audit</a><a href="#sources">Sources</a><a href="#reproduce">Reproduce the presentation</a><a href="#downloads">Downloads</a></nav></header><main id="main">
''' + docs[0] + f'<section id="maps"><h2>Annual probability and ranking maps</h2><p>Top panels show conservative probability; bottom panels show raw ranking percentile. Outlines select the annual top 10% across the three counties. Hatched cells are excluded, not low risk. Every map is accompanied by text and county summaries.</p><nav aria-label="Map years">{links}</nav></section>' + '\n'.join(sections) + '\n'.join(docs[1:]) + '''
<section id="downloads" class="downloads"><h2>Downloads and evidence</h2><ul>
<li><a href="wui_ml_v1_atlas.pdf">Map atlas with searchable text captions</a></li>
<li><a href="wui_ml_v1_snapshot.ipynb">Executed snapshot notebook</a></li>
<li><a href="decision.md">Frozen model decision, publication copy</a> and <a href="data/frozen_specification.json">exact specification</a></li>
<li><a href="map_captions.md">All map descriptions and captions</a></li>
<li><a href="data/map_attributes.csv">Cell-year predictions and eligibility, 2013–2021 CSV</a></li>
<li><a href="data/model_comparison.csv">Model comparison CSV</a> and <a href="data/annual_comparison.csv">annual comparison CSV</a></li>
<li><a href="data/source_provenance.json">Source and transformation provenance</a></li>
<li><a href="RELEASE_VALIDATION.md">Release validation</a> and <a href="release_manifest.json">file checksums</a></li>
<li><a href="CITATION.cff">Citation</a>, <a href="LICENSE">code and documentation license</a>, <a href="PUBLISHING.md">publication handoff</a></li>
</ul></section></main><footer>Adam Valentino · ML v1 publication package 1.0.0 · Based on frozen development evidence. Baseline and frozen model unchanged. No new evaluation of 2024–2025. <a href="https://aval0311.github.io/utah-wui-exposure-analysis/">Descriptive WUI baseline portfolio</a>.</footer></body></html>'''


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true', help='Check every manifest-listed file')
    parser.add_argument('--build', action='store_true', help='Rebuild index.html from included snapshots')
    args = parser.parse_args()
    if args.build:
        (ROOT/'index.html').write_text(page(), encoding='utf-8', newline='\n')
    if args.verify or not args.build:
        print(json.dumps(verify(), indent=2))
