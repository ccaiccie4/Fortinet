from pathlib import Path
import base64, hashlib, zipfile, shutil, re, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
ST=ROOT/'staging'; DOCS=ROOT/'docs'; IMG=DOCS/'images'
parts=[
 'fortinet-2026-09-07-10-38.correct.01',
 'fortinet-2026-09-07-10-38.correct.02a','fortinet-2026-09-07-10-38.correct.02b','fortinet-2026-09-07-10-38.correct.02c','fortinet-2026-09-07-10-38.correct.02d2',
 'fortinet-2026-09-07-10-38.b64.03','fortinet-2026-09-07-10-38.b64.04','fortinet-2026-09-07-10-38.b64.05','fortinet-2026-09-07-10-38.b64.06',
 'fortinet-2026-09-07-10-38.correct.07','fortinet-2026-09-07-10-38.b64.08','fortinet-2026-09-07-10-38.b64.09']
s=''.join((ST/p).read_text().strip() for p in parts)
assert len(s)==97032, len(s)
data=base64.b64decode(s, validate=True)
assert hashlib.sha256(data).hexdigest()=='8eb4c4c4c3b24f35af8e5879c11d13e1d3f42687c00cf81418953b5504838ba7'
zip_path=ST/'run1038.zip'; zip_path.write_bytes(data)
tmp=ST/'run1038-extract'; shutil.rmtree(tmp,ignore_errors=True); tmp.mkdir()
with zipfile.ZipFile(zip_path) as z: z.extractall(tmp)
src=tmp/'Fortinet_Daily_Study_Quiz_2026-09-07-10-38'
report=src/'Fortinet_Daily_Study_Quiz_2026-09-07-10-38.html'
html=report.read_text(encoding='utf-8')
assert html.count('class="lesson"')==12
assert html.count('class="question"')==50
assert html.count('Check Answer</button>')==50
assert html.count('class="feedback" id=')==50
assert 'data:image/svg' not in html.lower() and '<svg' not in html.lower()
svgs=sorted((src/'images').glob('*.svg')); dios=sorted((src/'images').glob('*.drawio'))
assert len(svgs)==12 and len(dios)==12
for p in svgs+dios: ET.parse(p)
refs=re.findall(r'(?:src|href)="(images/[^"]+\.(?:svg|drawio))"',html)
assert refs and not [r for r in refs if not (src/r).exists()]
DOCS.mkdir(exist_ok=True); IMG.mkdir(exist_ok=True)
shutil.copy2(report,DOCS/report.name)
for p in svgs+dios: shutil.copy2(p,IMG/p.name)
idx=DOCS/'index.html'; old=idx.read_text(encoding='utf-8')
run='Fortinet_Daily_Study_Quiz_2026-09-07-10-38.html'
if run not in old:
    card='''<section class="card latest"><span class="badge">LATEST VALIDATED RUN</span><h2>2026-09-07 10:38 America/Los_Angeles</h2><p>Feature-first Fortinet engineering study covering all 12 mandatory products, 12 editable draw.io sources, 12 matching SVGs, and 50 static graded MCQs.</p><div class="grid"><div><b>12/12</b><br>lessons</div><div><b>12/12</b><br>draw.io</div><div><b>12/12</b><br>SVG</div><div><b>50/50</b><br>MCQs</div><div><b>50/50</b><br>feedback</div><div><b>0</b><br>embedded SVG</div></div><p><a class="btn" href="Fortinet_Daily_Study_Quiz_2026-09-07-10-38.html">Open latest report</a></p><p><b>Pages URL:</b> <a href="https://ccaiccie4.github.io/Fortinet/Fortinet_Daily_Study_Quiz_2026-09-07-10-38.html">https://ccaiccie4.github.io/Fortinet/Fortinet_Daily_Study_Quiz_2026-09-07-10-38.html</a></p></section>'''
    old=old.replace('<p>Daily feature-first Fortinet engineering study sessions.</p>','<p>Daily feature-first Fortinet engineering study sessions.</p>'+card,1)
    idx.write_text(old,encoding='utf-8')
print('PASS',report.name,len(svgs),len(dios),hashlib.sha256(data).hexdigest())
# Triggered after all exact staging parts were present.
