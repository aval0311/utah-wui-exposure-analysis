"""Build the presentation PDF from saved figures and text; never load a model."""
from pathlib import Path
import json
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfdoc import PDFString
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader

ROOT = Path(__file__).resolve().parents[1]
maps = json.loads((ROOT/'data/map_descriptions.json').read_text(encoding='utf-8'))
claims = json.loads((ROOT/'data/claims.json').read_text(encoding='utf-8'))
W, H = 1152, 1008
c = canvas.Canvas(str(ROOT/'wui_ml_v1_atlas.pdf'), pagesize=(W,H), invariant=1)
c.setTitle('Utah wildfire occurrence modeling - ML v1 publication atlas')
c.setAuthor('Adam Valentino')
c.setSubject('Development 2001-2021; held-out maps 2013-2021; recorded occurrence and area limitations')
c.setKeywords('wildfire, Utah, XGBoost, development backtest, recorded occurrence, ML v1')
c.setViewerPreference('DisplayDocTitle', 'true')
c._doc.Catalog.Lang = PDFString('en-US')
navy = HexColor('#172b3a'); muted = HexColor('#425568')
body = ParagraphStyle('body',fontName='Helvetica',fontSize=14,leading=21,textColor=navy)
small = ParagraphStyle('small',parent=body,fontSize=11,leading=16)
heading = ParagraphStyle('head',parent=body,fontName='Helvetica-Bold',fontSize=20,leading=26)


def block(text,x,y,width,style=body):
    p=Paragraph(text,style);_,height=p.wrap(width,H)
    assert y-height>35, ('page overflow', text[:40], y-height)
    p.drawOn(c,x,y-height)
    return y-height-18


def top(title, subtitle, page):
    c.setFillColor(navy);c.setFont('Helvetica-Bold',30);c.drawString(46,H-65,title)
    c.setFont('Helvetica',13);c.drawString(46,H-92,subtitle)
    c.setFont('Helvetica',10);c.drawRightString(W-46,H-36,f'{page} / 11')
    c.setStrokeColor(HexColor('#cbd5df'));c.line(46,H-114,W-46,H-114)


top('Utah wildfire occurrence modeling','Adam Valentino | ML v1 publication 1.0.0 | 16 October 2026',1)
y=H-145
y=block('<b>Development 2001-2021. Held-out annual maps 2013-2021.</b> The target is at least one recorded wildfire discovery within a county-clipped cell during a UTC year. The 997 nominal 4 km cells cover Salt Lake, Utah and Washington counties, including non-WUI land.',46,y,W-92)
y=block('<b>Development evidence, not independent final evaluation.</b> These years informed model and calibration choices. Individual observations were held out from their fitted models, but the reported comparison is retrospective model development. No claim of statistical significance, statewide transfer or operational readiness is made.',46,y,W-92)
left,right,width=46,605,501
yl=block('Frozen model decision',left,y,width,heading)
yl=block('Conservative XGBoost is the probability recommendation. Raw XGBoost is the development ranking reference; sigmoid Random Forest is the benchmark. The maps combine five geographic fits per year under one frozen specification.',left,yl,width)
yl=block('Mean annual Brier score: <b>0.070814</b> conservative XGBoost, <b>0.071353</b> raw XGBoost and <b>0.071341</b> sigmoid Random Forest. The relative reduction in mean Brier score versus past-rate references is about 1%.',left,yl,width)
yl=block('Raw top-decile recall averages <b>18.09%</b> per year, versus <b>17.42%</b> for conservative probabilities. Probability calibration and location ranking have different trade-offs.',left,yl,width)
yl=block('Spatial and temporal safeguards',left,yl,width,heading)
yl=block('For target year T, base training uses 2001 through T-3; calibration uses T-2 and T-1. Five spatial folds use 20 km blocks with 4 km exclusion buffers. Imputation is fitted on training rows only. There are 8,588 eligible held-out cell-years and 656 recorded positives.',left,yl,width)
yr=block('Observation area matters',right,y,width,heading)
yr=block('Full 16 km2 cells account for <b>75.0%</b> of eligible cell-years and <b>98.0%</b> of top-decile slots. The clipped-cell conservative mean is <b>3.22%</b>, versus <b>3.03%</b> recorded occurrence. The larger clipped group underpredicts: <b>6.40% versus 8.09%</b>.',right,yr,width)
yr=block('Changing only the area input to 16 km2 raises the clipped-cell mean to <b>7.61%</b> and replaces <b>96/863</b> conservative selections. This is a sensitivity diagnostic, not a corrected forecast. <b>All maps retain original values and rankings.</b>',right,yr,width)
yr=block('Remaining limitations',right,yr,width,heading)
yr=block('Full cells account for <b>89.2%</b> of the 2020 count shortfall. Reporting changes and real occurrence changes cannot be separated. No-record labels do not establish absence of fire.',right,yr,width)
yr=block('Contemporary terrain is a static historical proxy. Climate uses pre-cutoff windows and an assumed 60-day lag. Historical as-issued terrain and climate availability is unverified. Probabilities are not property-loss estimates, daily fire danger or per-km2 hazard.',right,yr,width)
assert min(yl,yr)>95
block('Frozen baseline and model unchanged. No new training or 2024-2025 evaluation. Text, tables and map descriptions are also available in the accompanying offline index.html.',46,75,W-92,small)
c.showPage()
top('Sources and map reading','Source metadata checked 16 October 2026 | Analysis uses retained snapshots',2)
y=H-145
entries=[
('Recorded wildfire labels','NIFC InFORM public fire-occurrence layer; reviewed development labels for 2001-2021. CreatedBySystem and reporting-status changes around 2020 are descriptive evidence, not proof of a change in true occurrence or completeness. Raw incident records are not redistributed.','https://www.nifc.gov/programs/information-technology'),
('Terrain','USGS 3DEP / National Elevation Dataset 1 arc-second catalog retained 15 October 2026; aligned 30 m terrain. Catalog publication dates span 2013-2026 and are not terrain observation dates. Historical as-issued availability is not established.','https://www.usgs.gov/3d-elevation-program'),
('County footprint','State of Utah, SGID; UGRC and Lieutenant Governor\'s Office. Retained county response acquired 15 October 2026. Administrative boundaries define the fixed study footprint, not cadastral accuracy.','https://gis.utah.gov/products/sgid/boundaries/county/'),
('Antecedent climate','John T. Abatzoglou, gridMET (2013), International Journal of Climatology 33, 121-131, doi:10.1002/joc.3413. Subset archive completed 16 October 2026. Source days 1 October 1999 through 30 September 2020 support the 2001-2021 targets.','https://www.climatologylab.org/gridmet.html')]
for title,text,url in entries:
    y=block(title,46,y,W-92,heading)
    y=block(escape(text)+f'<br/><link href="{url}" color="#09565f">{escape(url)}</link>',46,y,W-92,small)
y=block('Read the maps',46,y,W-92,heading)
y=block('Top panels: conservative recorded-occurrence probability with common legends. Bottom panels: raw ranking percentile, 100 highest. Outlines select ceil(10% of eligible cells) across all three counties each year. Hatching identifies unknown labels or excluded flagged zeros, not low risk. County panels have separate extents; coordinates use EPSG:26912.',46,y,W-92,small)
y=block('Every following page includes the unchanged map image and a searchable text description. County averages describe eligible cells only. Native text companions improve access; this PDF is not represented as a fully tagged PDF/UA document. The offline HTML provides semantic headings, descriptions and tables.',46,y,W-92,small)
c.showPage()
for number,row in enumerate(maps,3):
    # Preserve every map pixel and scale the original image uniformly.
    c.drawImage(ImageReader(str(ROOT/row['image'])),0,216,width=1152,height=792)
    # The source image retains its old atlas number. Overlay only that margin.
    c.setFillColor(HexColor('#ffffff'));c.rect(W-70,H-50,70,50,fill=1,stroke=0)
    c.setFillColor(muted);c.setFont('Helvetica',9);c.drawRightString(W-22,H-14,f'{number} / 11')
    c.setFillColor(navy);c.setFont('Helvetica-Bold',14)
    c.drawString(46,191,f'{row["year"]} accessible map description')
    c.setFont('Helvetica',10);c.drawRightString(W-46,191,f'{number} / 11')
    y=block(escape(row['caption']),46,173,W-92,small)
    y=block(escape(row['spatial_description']),46,y,W-92,small)
    assert y>36
    c.showPage()
c.save()
print('Created 11-page publication atlas with native text on every page.')
