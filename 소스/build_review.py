"""python 소스/build_review.py — Pillow만 필요. 네트워크를 사용하지 않습니다."""
from pathlib import Path
import json,base64,io
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())
def pic(path,width=720):
 im=Image.open(ROOT/path).convert('RGB');im.thumbnail((width,round(width*16/9)))
 out=io.BytesIO();im.save(out,'JPEG',quality=88,optimize=True)
 return 'data:image/jpeg;base64,'+base64.b64encode(out.getvalue()).decode()
def audio(path):return 'data:audio/mpeg;base64,'+base64.b64encode((ROOT/path).read_bytes()).decode()
refs=load('기록/레퍼런스/이미지목록.json');sounds=load('기록/레퍼런스/사운드목록.json');screens=load('기록/목업/화면목록.json')
for r in refs:
 r['image']=pic(r['file'],960) if r.get('file') and r['embed'] else None
for r in sounds:r['audio']=audio(r['preview']) if r.get('preview') else None
for r in screens:r['image']=pic(r['file']) if r.get('file') and (ROOT/r['file']).exists() else None
docs={p.name:p.read_text() for p in sorted((ROOT/'기록').glob('*.md'))}
docs['글꼴_OFL.txt']=(ROOT/'소스/글꼴/OFL.txt').read_text()
data=dict(refs=refs,sounds=sounds,screens=screens,docs=docs,date='2026-10-15')
payload=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
template=(ROOT/'소스/review.template.html').read_text()
out=template.replace('__WAXPOP_DATA__',payload)
font=base64.b64encode((ROOT/'소스/글꼴/Pretendard-Regular.woff2').read_bytes()).decode()
out=out.replace('/*EMBED_FONT*/',"@font-face{font-family:WaxPopFont;src:url(data:font/woff2;base64,"+font+") format('woff2');font-weight:400;font-style:normal;font-display:swap;}")
(ROOT/'waxpop-review.html').write_text(out)
print('HTML:',len(out.encode()),'bytes; refs',len(refs),'embedded',sum(bool(r['image']) for r in refs),'sounds',sum(bool(r['audio']) for r in sounds),'mockups',sum(bool(r['image']) for r in screens))
