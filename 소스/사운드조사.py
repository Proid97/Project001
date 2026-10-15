import urllib.request,urllib.parse,json,pathlib,re,concurrent.futures,subprocess,numpy as np,math,shutil
ROOT=pathlib.Path('/workspace/scratch/3747d75f8758/Project001');OUT=ROOT/'기록/레퍼런스';rows=[]
def get(u):return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'WaxPopResearch/1.0'}),timeout=25).read()
fs=[('qubodup',127449,'Slime','슬라임·젤리','플라스틱 그릇 속 슬라임'),('greenlinker',794270,'Slime stretching and squeezing','슬라임·젤리','슬라임 늘리기·누르기'),('breiti',587848,'Guck, Slime, slippery Jelly slowly kneading squeezing with Hands, some Bubbles.wav','슬라임·젤리','젤리·슬라임 주무르기'),('rubberduck9999',680446,'slime - bubble blowing recordings','슬라임·젤리','직접 만든 슬라임에 입으로 기포 넣기'),('rubberduck9999',680447,'slime - squishing sounds','슬라임·젤리','직접 만든 슬라임 누르기'),('lolamadeus',181914,'Jelly Wobbling on Plate 1.wav','말랑한 속','접시 위 실제 젤리'),('Fugeni',559768,'Jello Squish','말랑한 속','그릇 속 젤리'),('jtap97',448884,'slime noise 3_1.wav','슬라임·젤리','putty·slime 녹음 / 세부 재질 설명 부족')]
for creator,n,title,cat,material in fs:
 rows.append(dict(id=f'A{len(rows)+1:03}',title=title,creator=creator,category=cat,material=material,real_material=True,url=f'https://freesound.org/people/{creator}/sounds/{n}/',fsid=n))
packs={'ui':('Calinou/kenney-ui-audio','master','addons/kenney_ui_audio/','LICENSE.txt'), 'impact':('Boyquotes/kenney-impact-sounds-for-godot','main','addons/kenney impact sounds/','LICENSE'), 'rpg':('Boyquotes/kenney-rpg-audio-for-godot','main','addons/kenney rpg audio/','LICENSE')}
specs={'ui':[('click1.wav','버튼'),('click2.wav','버튼'),('rollover1.wav','연결'),('rollover2.wav','연결'),('switch1.wav','누르기'),('switch2.wav','누르기')], 'impact':[('impact_soft_light_000.ogg','착지'),('impact_soft_light_001.ogg','착지'),('impact_soft_medium_000.ogg','착지'),('impact_soft_heavy_000.ogg','특수 볼'),('impact_glass_light_000.ogg','껍질·보조'),('impact_glass_light_001.ogg','껍질·보조'),('impact_glass_medium_000.ogg','특수 볼'),('impact_plastic_light_000.ogg','껍질·보조'),('impact_plastic_light_001.ogg','껍질·보조'),('impact_wood_light_000.ogg','껍질·보조')], 'rpg':[('cloth_1.ogg','연결'),('cloth_2.ogg','연결'),('book_flip_1.ogg','껍질·보조'),('book_flip_2.ogg','껍질·보조'),('handle_coins.ogg','목표·결과'),('drop_leather.ogg','착지'),('metal_click.ogg','버튼'),('chop.ogg','특수 볼')]}
for k,ss in specs.items():
 repo,branch,prefix,lic=packs[k];tree=json.load(open('work/'+k+'.json'))['tree'];paths={x['path'] for x in tree}
 for name,cat in ss:
  path=prefix+name
  if path not in paths:print('missing',k,name);continue
  rows.append(dict(id=f'A{len(rows)+1:03}',title=name,creator='Kenney',category=cat,material='보조 효과음 / 실제 왁스·슬라임 녹음으로 세지 않음',real_material=False,url=f'https://github.com/{repo}/blob/{branch}/'+urllib.parse.quote(path),download_url=f'https://raw.githubusercontent.com/{repo}/{branch}/'+urllib.parse.quote(path),original_filename=name,license_url=f'https://github.com/{repo}/blob/{branch}/'+('addons/kenney_ui_audio/LICENSE.txt' if k=='ui' else lic),pack=k))
def fetch(r):
 try:
  r.update(date='2026-10-15',license='CC0 1.0',commercial=True,edit=True,attribution='표시 의무 없음. 제작자·원문 링크는 자발적으로 보존.',audition='직접 청음하지 않음. 해독·파형 검사만 수행.',caution='말소리·음악·소음·울림과 실제 게임 적합성은 이어폰·휴대폰에서 청음 필요.')
  if 'fsid'in r:
   page=get(r['url']).decode();
   if not ('creativecommons.org/publicdomain/zero/1.0' in page or 'Creative Commons 0' in page):raise ValueError('개별 CC0 표기 미확인')
   urls=re.findall(r'https://cdn\.freesound\.org/previews/[^\s"<>]+-hq\.mp3',page)
   if not urls:raise ValueError('공개 미리듣기 URL 없음')
   r['download_url']=urls[0];r['license_url']=r['url'];r['original_filename']=urls[0].split('/')[-1];r['source_kind']='사이트 공개 미리듣기 MP3. 원본 WAV/FLAC는 로그인 필요하여 미확보.'
  else:r['source_kind']='배포 저장소 원본 파일'
  b=get(r['download_url']);ext=r['original_filename'].split('.')[-1];path=OUT/'사운드'/f"{r['id']}_{'실물' if r['real_material'] else '보조'}_{r['category'].replace('·','_')}.{ext}";path.write_bytes(b)
  info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(path)]));s=info['streams'][0]
  pcm=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-f','f32le','-acodec','pcm_f32le','-']);a=np.frombuffer(pcm,dtype='<f4');peak=float(np.max(np.abs(a)));rms=float(np.sqrt(np.mean(a.astype(float)**2)));clipped=int(np.sum(np.abs(a)>1.0))
  r.update(file=str(path.relative_to(ROOT)),duration=float(info['format']['duration']),sample_rate=int(s['sample_rate']),channels=s['channels'],format=s['codec_name'],peak=peak,peak_dbfs=round(20*math.log10(max(peak,1e-9)),2),rms_dbfs=round(20*math.log10(max(rms,1e-9)),2),samples_over_1=clipped,bytes=len(b))
  # Long source recordings: deterministic first-active window. This is NOT a listening-based best take.
  frames=a.reshape(-1,s['channels']).mean(1);sr=int(s['sample_rate']);win=max(1,int(sr*.02));energy=np.array([np.sqrt(np.mean(frames[i:i+win].astype(float)**2)) for i in range(0,len(frames),win)])
  active=np.where(energy>max(.004,float(np.max(energy))*.12))[0];start=max(0,float(active[0]*.02-.06)) if len(active) else 0;duration=min(7 if r['real_material'] else 3,r['duration']-start);gain=min(12,max(-30,-3-r['peak_dbfs']))
  preview=OUT/'사운드/미리듣기'/f"{r['id']}.mp3";preview.parent.mkdir(exist_ok=True)
  subprocess.run(['ffmpeg','-v','error','-y','-ss',str(start),'-i',str(path),'-t',str(duration),'-af',f'volume={gain}dB,afade=t=in:d=0.008,afade=t=out:st={max(0,duration-.04)}:d=0.04','-ar','44100','-ac','1','-codec:a','libmp3lame','-b:a','96k',str(preview)],check=True)
  r.update(preview=str(preview.relative_to(ROOT)),preview_transform=f'{start:.3f}초부터 {duration:.3f}초 / {gain:+.2f}dB / 앞 8ms·뒤 40ms 페이드 / 모노 44.1kHz MP3 96kbps. 자동 구간 선택, 청음 선별 아님.',status='파일 확보·해독 완료',recommendation='임시 비교 후보 / 청음 전')
  if clipped:r['caution']='원본 디코딩 피크가 1.0 초과. 미리듣기는 감쇠했으나 원본 잘림·왜곡은 청음 확인 필요. '+r['caution']
 except Exception as e:r.update(file=None,preview=None,status='확보 실패',error=str(e))
 return r
rows=list(concurrent.futures.ThreadPoolExecutor(6).map(fetch,rows));(OUT/'사운드목록.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
for k in packs:
 shutil.copy('work/'+k+'_license.txt',OUT/'출처'/f'{k}_LICENSE.txt')
print([(r['id'],r['title'],r['status'],r.get('peak'),r.get('duration')) for r in rows])
