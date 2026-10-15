"""생성 PNG를 수정하지 않고 내장한 스타일·팔레트 비교 HTML."""
from pathlib import Path
import base64, html, json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'waxpop-style-review.html'
styles = json.loads((ROOT / '기록/목업/스타일/시안목록.json').read_text())
palettes = json.loads((ROOT / '소스/스타일팔레트.json').read_text())

def esc(value):
    return html.escape(str(value), quote=True)

def data_uri(name):
    return 'data:image/png;base64,' + base64.b64encode((ROOT / name).read_bytes()).decode()

def swatches(p):
    return ''.join(f'<div class="swatch"><i style="background:{color}"></i><span>{esc(name)}</span><code>{color}</code></div>'
                   for color, name in zip(p['balls'], p['ball_names']))

cards = ''.join(f'''<article class="style-card"><div class="art"><img src="{data_uri(s['file'])}" alt="{esc(s['name'])} 민트색 기본 볼 시안"></div>
<div class="card-copy"><span class="label">{s['id']}</span><h3>{esc(s['name'])}</h3><p>{esc(s['description'])}</p><p class="small">{esc(s['note'])}</p><div class="tiny-sample" style="display:flex;gap:12px;align-items:center;font-size:11px;color:#786b7b">48px 축소</div></div></article>'''
                for s in styles)
themes = ''.join(f'''<article class="theme-card" style="--theme-bg:{p['background']};--theme-board:{p['board']};--theme-ink:{p['ink']};--theme-button:{p['button']};--theme-panel:{p['panel']}">
<div class="theme-top"><span>{p['id']} · {esc(p['tag'])}</span><h3>{esc(p['name'])}</h3><p>{esc(p['description'])}</p></div>
<div class="ui-demo"><div class="goal">목표 <strong>민트 볼 모으기</strong></div><div class="color-row">{''.join(f'<i style="background:{x}"></i>' for x in p['balls'])}</div><span class="sample-button">시작하기</span></div>
<div class="theme-colors">{swatches(p)}</div><div class="roles"><span>배경 <code>{p['background']}</code></span><span>보드 <code>{p['board']}</code></span><span>글자 <code>{p['ink']}</code></span><span>버튼 <code>{p['button']}</code></span></div>
</article>''' for p in palettes)
data = [{'id':p['id'],'name':p['name'],'bg':p['background'],'board':p['board']} for p in palettes]
page = '''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>왁스팝 · 볼과 팔레트 비교</title>
<style>
*{box-sizing:border-box}html{color:#35253e;background:#fffaf5;font-family:system-ui,-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Malgun Gothic",sans-serif}body{margin:0}main{max-width:1280px;margin:auto;padding:48px 28px 64px}h1{font-size:clamp(30px,5vw,54px);letter-spacing:-.055em;margin:12px 0 16px;line-height:1.13}h2{font-size:27px;letter-spacing:-.04em;margin:0 0 10px}h3{font-size:24px;letter-spacing:-.04em;margin:8px 0}p{line-height:1.65;margin:8px 0}.eyebrow{font-size:13px;letter-spacing:.16em;font-weight:800;color:#8b5773}.intro{max-width:800px;color:#66556b}.notice{border:1px solid #e7cbd8;background:#fff0f5;border-radius:16px;padding:14px 18px;margin:24px 0 34px;font-size:14px}.style-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}.style-card{background:white;border:1px solid #ebdfea;border-radius:24px;overflow:hidden;min-width:0}.art{padding:12px;aspect-ratio:1;background:#e3f2eb;display:grid;place-items:center;transition:background .15s}.art img{width:100%;height:100%;object-fit:contain}.card-copy{padding:18px}.label{color:#9b536d;font-size:13px;font-weight:800}.small{font-size:12px;color:#786b7b}.card-copy p{font-size:14px}.toolbar{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:20px 0}button{font:inherit;color:#3c2943;background:white;border:1px solid #d9c7d9;border-radius:999px;padding:10px 17px;cursor:pointer;min-height:44px}button[aria-pressed="true"]{background:#3c2943;color:white}button:focus-visible,a:focus-visible{outline:3px solid #b04485;outline-offset:4px}.section{margin-top:46px}.theme-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin-top:20px}.theme-card{border:1px solid #e7dfe6;border-radius:24px;background:var(--theme-bg);color:var(--theme-ink);overflow:hidden}.theme-top{padding:24px 22px 12px}.theme-top>span{font-weight:800;font-size:12px}.theme-top p{font-size:14px;min-height:68px}.ui-demo{margin:8px 20px 20px;padding:18px;background:var(--theme-board);border-radius:18px}.goal{background:var(--theme-panel);padding:10px 12px;border-radius:12px;font-size:12px;display:flex;justify-content:space-between;gap:10px}.color-row{display:flex;justify-content:center;gap:13px;margin:18px 0}.color-row i{display:block;width:37px;height:37px;border:2px solid #00000010;border-radius:50%}.sample-button{display:block;background:var(--theme-button);color:var(--theme-ink);border-radius:14px;text-align:center;font-weight:800;padding:12px}.theme-colors{padding:0 20px 18px;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:7px}.swatch{min-width:0}.swatch i{display:block;height:34px;border-radius:8px;border:1px solid #00000012}.swatch span{display:block;font-size:10px;margin:6px 0 3px;white-space:nowrap}.swatch code{display:block;font-size:10px;letter-spacing:-.04em}.roles{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:15px 20px;background:#ffffff80;font-size:11px}.roles code{display:block;margin-top:3px}.recommend{background:#fff;border:1px solid #e7dfea;border-radius:18px;padding:20px;margin-top:24px}footer{font-size:12px;color:#786b7b;margin-top:28px}code{font-family:ui-monospace,monospace}a{color:#814062;overflow-wrap:anywhere}@media(max-width:950px){.style-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.theme-grid{grid-template-columns:1fr}.theme-top p{min-height:0}.theme-card{max-width:600px}.theme-colors .swatch span,.theme-colors .swatch code{font-size:12px}}@media(max-width:440px){main{padding:28px 14px 40px}.style-grid{gap:10px}.card-copy{padding:12px}.card-copy h3{font-size:19px}.card-copy p{font-size:12px}.art{padding:3px}.toolbar{gap:7px}button{padding:9px 12px;font-size:13px}}@media print{main{padding:0}.toolbar{display:none}.style-grid{grid-template-columns:repeat(4,1fr)}.theme-grid{grid-template-columns:repeat(3,1fr)}.style-card,.theme-card{break-inside:avoid}*{print-color-adjust:exact;-webkit-print-color-adjust:exact}}
</style><main><header><div class="eyebrow">WAX POP / ART DIRECTION</div><h1>바삭한 껍질,<br>말랑하고 달콤한 한 알.</h1><p class="intro">기본 볼 4종과 UI 팔레트 3종을 따로 비교합니다. 먼저 볼의 그림체를 고르고, 그다음 화면의 색을 고르면 됩니다. 같은 민트색·정면·왼쪽 위 조명으로 요청한 생성 시안입니다.</p></header>
<p class="notice">아직 그림체·팔레트가 확정되지 않았습니다. 생성 이미지의 실제 모양·빛은 조금씩 다릅니다. 파열·드래그·애니메이션을 검증한 게임용 완성 에셋은 아닙니다.</p>
<section aria-labelledby="balls-heading"><h2 id="balls-heading">어떤 볼이 왁스팝에 어울릴까요?</h2><p>배경을 바꿔 가장자리와 재질을 비교하세요. 이미지 자체의 색은 바꾸지 않습니다.</p><div class="toolbar" role="group" aria-label="볼 비교 배경"><button data-theme="P1" aria-pressed="true">소다 피치</button><button data-theme="P2" aria-pressed="false">베리 레몬</button><button data-theme="P3" aria-pressed="false">트로피컬 구미</button><button data-theme="white" aria-pressed="false">흰색</button><button data-theme="dark" aria-pressed="false">짙은색</button></div><div class="style-grid">@@STYLES@@</div></section>
<section class="section" id="palette-section" aria-labelledby="palette-heading"><h2 id="palette-heading">화면 전체의 색, 세 가지 제안</h2><p>아래는 정확한 색상과 버튼·패널 배치의 비교 예시입니다. 완성 화면 목업은 아닙니다. 작은 글자에는 짙은 글자색을 사용합니다.</p><div class="theme-grid">@@THEMES@@</div></section>
<aside class="recommend"><strong>현재 추천: B01 밀키왁스 + P1 소다 피치</strong><p>뽀얀 껍질과 말랑한 볼의 인상을 살리고, 민트·복숭아·연보라·크림의 기존 방향을 상큼하게 다듬는 조합입니다. 실제 추천은 생성 결과의 관찰 메모와 함께 확인하세요.</p><p>선택한 뒤에는 원본 이미지, 윤곽, 빛, 반사, 색, 표면 무늬를 기준으로 저장하고 이후 이미지 생성에 함께 참조합니다.</p></aside>
<footer>2026-10-15 · 실제 실물 사진이 아닌 AI 생성 시안 · 이미지와 코드는 이 파일에 내장 · 외부 요청 없이 열람 · 이 파일은 게임이 아닙니다.</footer></main><script>
const themes=@@DATA@@;document.querySelectorAll('.style-card').forEach(card=>{const small=card.querySelector('.art img').cloneNode();small.style.cssText='width:48px;height:48px;object-fit:contain';small.alt='';card.querySelector('.tiny-sample').append(small)});document.querySelectorAll('[data-theme]').forEach(button=>button.addEventListener('click',()=>{const id=button.dataset.theme;const found=themes.find(x=>x.id===id);const color=found?found.board:id==='dark'?'#354052':'#FFFFFF';document.querySelectorAll('.art').forEach(x=>x.style.background=color);document.querySelectorAll('[data-theme]').forEach(x=>x.setAttribute('aria-pressed',String(x===button)))}));
</script></html>'''
page = page.replace('@@STYLES@@', cards).replace('@@THEMES@@', themes).replace('@@DATA@@', json.dumps(data, ensure_ascii=False))
font = base64.b64encode((ROOT / '소스/글꼴/Pretendard-Regular.woff2').read_bytes()).decode()
page = page.replace('<style>', '<style>@font-face{font-family:WaxPopPretendard;src:url(data:font/woff2;base64,' + font + ') format("woff2");font-weight:100 900;font-display:swap}')
page = page.replace('font-family:system-ui', 'font-family:WaxPopPretendard,system-ui')
license_text = esc((ROOT / '소스/글꼴/OFL.txt').read_text())
page = page.replace('</footer>', '<details><summary>Pretendard 글꼴 · SIL Open Font License 1.1</summary><pre style="white-space:pre-wrap;overflow-wrap:anywhere">' + license_text + '</pre></details></footer>')
assert '@@' not in page
assert page.count('data:image/png;base64,') == 4
OUT.write_text(page, encoding='utf-8')
print(json.dumps({'file':str(OUT),'bytes':OUT.stat().st_size,'embedded_png':4},ensure_ascii=False))
