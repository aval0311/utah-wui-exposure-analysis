"""Generate release summaries directly from an accepted run's exported tables."""
import csv, json
from pathlib import Path

def add_phase_navigation(html):
    """Keep both historical and ML studies discoverable on dashboard exports."""
    css_anchor = '  #wui-app .wui-body { flex:1;'
    if '<nav class="wui-phase-nav"' in html:
        if 'class="wui-timeline-link"' not in html:
            anchor = '  </nav>\n  <div class="wui-body">'
            if html.count(anchor) != 1:
                raise ValueError('Review project-phase navigation before export.')
            html = html.replace(anchor, '    <a class="wui-timeline-link" href="https://aval0311.github.io/utah-wui-exposure-analysis/history/">Historical timeline <span aria-hidden="true">&rarr;</span></a>\n' + anchor)
        if '#wui-app .wui-phase-nav .wui-timeline-link' not in html:
            html = html.replace(css_anchor, '  #wui-app .wui-phase-nav .wui-timeline-link { background:var(--wui-teal); color:white;\n    padding:0 12px; border-radius:4px; text-decoration:none; }\n  #wui-app .wui-phase-nav .wui-timeline-link:hover { background:#12575C; }\n' + css_anchor)
        return html
    html_anchor = '  </header>\n  <div class="wui-body">'
    if html.count(css_anchor) != 1 or html.count(html_anchor) != 1:
        raise ValueError('Dashboard header changed; review project-phase navigation before export.')
    css = '''  #wui-app .wui-phase-nav { flex:none; display:flex; align-items:center; flex-wrap:wrap;
    gap:4px 20px; padding:4px 20px; background:var(--wui-selected);
    border-bottom:1px solid #BFD4D3; font-size:12px; }
  #wui-app .wui-phase-nav [aria-current="page"] { color:var(--wui-muted); }
  #wui-app .wui-phase-nav a { display:inline-flex; align-items:center; gap:6px;
    min-height:36px; color:#12575C; font-weight:700; text-decoration:underline; text-underline-offset:3px; }
  #wui-app .wui-phase-nav a:hover { color:#0B363A; }
'''
    navigation = '''  </header>
  <nav class="wui-phase-nav" aria-label="Project phases">
    <span aria-current="page">WUI dashboard</span>
    <a href="https://aval0311.github.io/utah-wui-exposure-analysis/ml/">ML case study <span aria-hidden="true">&rarr;</span></a>
  </nav>
  <div class="wui-body">'''
    return add_phase_navigation(html.replace(css_anchor, css + css_anchor).replace(html_anchor, navigation))

def release_summary(run):
    run=Path(run)
    manifest=json.loads((run/'run_manifest.json').read_text(encoding='utf-8'))
    def rows(name):
        with (run/name).open(encoding='utf-8-sig',newline='') as stream:
            return list(csv.DictReader(stream))
    counties=rows('county_exposure.csv')
    coverage=rows('hazard_coverage.csv')
    sensitivity=rows('weight_sensitivity.csv') if (run/'weight_sensitivity.csv').is_file() else []
    lines=[f"Accepted snapshot run: **{manifest['run_id']}**, completed **{manifest['completed_utc'][:10]} UTC**.",
           'This summary is synchronized from exported tables; new execution results appear later in the notebook.',
           '', '| County | Estimated residents in mapped WUI | Estimated housing units | Share of county population |',
           '|---|---:|---:|---:|']
    for row in counties:
        lines.append(f"| {row['COUNTY_NAME'].replace(' County','')} | {float(row['EST_ACS_POP_EXPOSED']):,.0f} | {float(row['EST_ACS_HOUSING_EXPOSED']):,.0f} | {float(row['PERCENT_ACS_POP_EXPOSED']):.2f}% |")
    largest=max(counties,key=lambda r:float(r['EST_ACS_POP_EXPOSED']))
    share=max(counties,key=lambda r:float(r['PERCENT_ACS_POP_EXPOSED']))
    lead = (f"{largest['COUNTY_NAME']} has the largest estimated exposed population and the highest share of county residents within mapped WUI." if largest['COUNTY_NAME']==share['COUNTY_NAME'] else f"{largest['COUNTY_NAME']} has the largest estimated exposed population; {share['COUNTY_NAME']} has the highest county population share.")
    lines.extend(['',lead+" These area-weighted estimates describe mapped WUI overlap, not population within a modeled hazard class.",
                  '',f"The study footprint totals **{sum(float(r['AREA_KM2']) for r in coverage):,.2f} km²**.",
                  '', '| Coverage category | Study area (%) |', '|---|---:|'])
    for row in coverage:
        lines.append(f"| {row['CATEGORY']} | {float(row['STUDY_AREA_PERCENT']):.2f} |")
    lines.extend(['','County panels are polygon-masked. Nonburnable land and missing observations have separate exclusion categories.'])
    if sensitivity:
        lines.extend(['',f"Sensitivity uses **{int(sensitivity[0]['SAMPLE_PIXELS']):,}** modeled sample pixels.",''])
        for row in sensitivity:
            if row['SCENARIO']!='Baseline':
                lines.append(f"- {row['SCENARIO']}: **{float(row['CLASS_AGREEMENT_PERCENT']):.2f}%** class agreement; top-quintile Jaccard **{float(row['TOP_QUINTILE_JACCARD']):.3f}**.")
        lines.extend(['','These comparisons assess stability under assumed weights.'])
    history=manifest['historical_selection']
    lines.extend(['',f"Historical selection retained **{history['selected_rectangle_records']:,} recorded wildfires** in the density rectangle, including **{history['selected_inside_counties']:,} inside the county polygons**. Prescribed fires are excluded.",
                  '',f"This complete snapshot run took **{manifest['elapsed_seconds']/60:.1f} minutes**, measured from configuration through input verification, processing, and snapshot-inventory finalization. This single functional-validation timing is separate from the retained composite benchmark."])
    return '\n'.join(lines)+'\n'
