from pathlib import Path
import base64,zlib,hashlib,re,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
ST=ROOT/'staging'; DOCS=ROOT/'docs'; IMG=DOCS/'images'
OUT=DOCS/'Fortinet_Daily_Study_Quiz_2026-09-05-15-19.html'
EXPECTED='c946a8cf19d25d20c42cfdb379b2a30247a0a14693872ad5d30cc4d58c4d84f4'
b64=''.join((ST/f'report15_19.b64z.{i}').read_text().strip() for i in range(1,6))
data=zlib.decompress(base64.b64decode(b64))
assert hashlib.sha256(data).hexdigest()==EXPECTED
s=data.decode('utf-8')
assert s.count('class="lesson"')==12
assert s.count('class="question"')==50
assert s.count('class="check"')==50
assert s.count('class="feedback"')==50
assert 'data:image' not in s
assert '<svg' not in s.lower()
prefix='05-09-26-15-19-'
draw=list(IMG.glob(prefix+'*.drawio')); svg=list(IMG.glob(prefix+'*.svg'))
assert len(draw)==12 and len(svg)==12
for p in draw+svg:
    assert p.stat().st_size>1000
    ET.parse(p)
for p in svg:
    assert f'images/{p.name}' in s
for p in draw:
    assert f'images/{p.name}' in s
OUT.write_bytes(data)
idx=DOCS/'index.html'; x=idx.read_text()
new='''<section class="card latest"><span class="badge">LATEST TEST RUN — DRAW.IO/SVG</span><h2>2026-09-05 15:19 America/Los_Angeles</h2><p>Documentation-driven test run covering all 12 mandatory Fortinet products with 12 editable draw.io sources, 12 matching standalone SVG diagrams, and 50 static graded MCQs with detailed answer teaching feedback.</p><div class="grid"><div><b>12/12</b><br>engineering lessons</div><div><b>12/12</b><br>draw.io sources</div><div><b>12/12</b><br>standalone SVGs</div><div><b>50/50</b><br>static MCQs</div><div><b>50/50</b><br>detailed feedback blocks</div><div><b>0</b><br>embedded SVG/data URIs</div></div><p><a class="btn" href="Fortinet_Daily_Study_Quiz_2026-09-05-15-19.html">Open latest report</a></p><p><b>Pages URL:</b> <a href="https://ccaiccie4.github.io/Fortinet/Fortinet_Daily_Study_Quiz_2026-09-05-15-19.html">https://ccaiccie4.github.io/Fortinet/Fortinet_Daily_Study_Quiz_2026-09-05-15-19.html</a></p></section>'''
x=x.replace('<section class="card latest">','<section class="card">',1)
pos=x.find('<section class="card">')
assert pos!=-1
x=x[:pos]+new+x[pos:]
idx.write_text(x)
assert 'Fortinet_Daily_Study_Quiz_2026-09-05-15-19.html' in idx.read_text()
print({'report_bytes':len(data),'lessons':12,'questions':50,'drawio':12,'svg':12,'sha256':EXPECTED})
# trigger workflow after all staging chunks are committed
