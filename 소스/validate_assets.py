from pathlib import Path
import json,subprocess,io,base64,re,hashlib
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1]
refs=json.loads((R/'기록/레퍼런스/이미지목록.json').read_text());sounds=json.loads((R/'기록/레퍼런스/사운드목록.json').read_text());screens=json.loads((R/'기록/목업/화면목록.json').read_text())
result={'photos':0,'sounds':0,'screens':0,'preview_peaks':{},'photo_sha256':{}}
for x in refs:
 p=R/x['file'];im=Image.open(p);im.verify();result['photos']+=1;result['photo_sha256'][x['id']]=hashlib.sha256(p.read_bytes()).hexdigest();assert x['url'] and x['image_url'] and x['license'] and len(x['observations'])>=2
for x in screens:
 im=Image.open(R/x['file']);im.verify();result['screens']+=1
for x in sounds:
 for k in ['file','preview']:
  subprocess.check_output(['ffprobe','-v','error','-show_format','-of','json',str(R/x[k])])
 a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(R/x['preview']),'-f','f32le','-']),dtype='<f4');peak=float(np.max(np.abs(a)));result['preview_peaks'][x['id']]=peak;assert peak<1.0
 assert x['commercial'] and x['edit'] and x['license_url'];result['sounds']+=1
s=(R/'waxpop-review.html').read_text();d=json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>',s,re.S).group(1));assert len(d['refs'])==27 and sum(bool(x['image']) for x in d['refs'])==3 and sum(bool(x['audio']) for x in d['sounds'])==32 and sum(bool(x['image']) for x in d['screens'])==15
for x in d['refs']+d['screens']:
 if x.get('image'):Image.open(io.BytesIO(base64.b64decode(x['image'].split(',')[1]))).verify()
result.update(html_bytes=(R/'waxpop-review.html').stat().st_size,embedded_photos=3,embedded_sounds=32,embedded_screens=15,unique_photos=len(set(result['photo_sha256'].values())))
(R/'기록/검증').mkdir(exist_ok=True);(R/'기록/검증/파일검사.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in result.items() if not isinstance(v,dict)},ensure_ascii=False))
