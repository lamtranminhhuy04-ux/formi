"""Read actual rendered fonts using Chromium CDP; run before/after changes."""
import json
import sys
from pathlib import Path
from fontTools.ttLib import TTFont
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tests/artifacts'
PROBE = 'Ở nơi ấy, chúng mình đã cùng ngắm hoàng hôn và lưu giữ những điều dịu dàng nhất.'
GLYPHS = ('ă â ê ô ơ ư đ Ă Â Ê Ô Ơ Ư Đ\n'
          'á à ả ã ạ Á À Ả Ã Ạ\nắ ằ ẳ ẵ ặ Ắ Ằ Ẳ Ẵ Ặ\n'
          'ấ ầ ẩ ẫ ậ Ấ Ầ Ẩ Ẫ Ậ\nế ề ể ễ ệ Ế Ề Ể Ễ Ệ\n'
          'ố ồ ổ ỗ ộ Ố Ồ Ổ Ỗ Ộ\nớ ờ ở ỡ ợ Ớ Ờ Ở Ỡ Ợ\n'
          'ứ ừ ử ữ ự Ứ Ừ Ử Ữ Ự\ní ì ỉ ĩ ị Í Ì Ỉ Ĩ Ị\n'
          'ú ù ủ ũ ụ Ú Ù Ủ Ũ Ụ\ný ỳ ỷ ỹ ỵ Ý Ỳ Ỷ Ỹ Ỵ')

def rendered_fonts(page, selector):
    cdp = page.context.new_cdp_session(page)
    cdp.send('DOM.enable')
    cdp.send('CSS.enable')
    doc = cdp.send('DOM.getDocument')
    node = cdp.send('DOM.querySelector', {'nodeId': doc['root']['nodeId'], 'selector': selector})['nodeId']
    result = cdp.send('CSS.getPlatformFontsForNode', {'nodeId': node})['fonts']
    cdp.detach()
    return result

def main():
    phase = sys.argv[1] if len(sys.argv) > 1 else 'after'
    OUT.mkdir(exist_ok=True)
    report = {'encoding': {}, 'font_coverage': {}, 'rendered': {}}
    for f in [ROOT / 'index.html', *ROOT.glob('css/*.css'), *ROOT.glob('js/*.js')]:
        text = f.read_bytes().decode('utf-8', errors='strict')
        report['encoding'][str(f.relative_to(ROOT))] = {'utf8': True, 'replacement_character': '\ufffd' in text}
    paths = list((ROOT / 'assets/fonts').glob('*.woff2')) if phase == 'after' else [Path('C:/Windows/Fonts') / f for f in ['georgia.ttf', 'georgiai.ttf', 'times.ttf', 'segoeui.ttf', 'arial.ttf']]
    for path in paths:
        font = TTFont(path)
        cmap = font.getBestCmap()
        missing = ''.join(sorted({c for c in PROBE + GLYPHS if not c.isspace() and ord(c) not in cmap}))
        report['font_coverage'][path.name] = {'missing': missing, 'bytes': path.stat().st_size}
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        page = browser.new_page(viewport={'width': 1100, 'height': 1100})
        page.goto((ROOT / 'index.html').as_uri())
        page.evaluate('document.fonts.ready')
        for selector in ['#intro', '#couple', '#reason-title', '#hero-caption', '#signature', '.quiz-option']:
            report['rendered'][selector] = {
                'css': page.locator(selector).first.evaluate('(e)=>({family:getComputedStyle(e).fontFamily,weight:getComputedStyle(e).fontWeight,style:getComputedStyle(e).fontStyle})'),
                'fonts': rendered_fonts(page, selector)
            }
        page.evaluate('''({probe,glyphs,phase})=>{
          document.body.replaceChildren(); document.body.style.padding='28px';
          for(const [family,weight,style,size] of phase==='before'
              ? [['Georgia',400,'normal',28],['Georgia',400,'italic',28]]
              : [['var(--font-body)',400,'normal',16],['var(--font-body)',600,'normal',18],['var(--font-body)',650,'normal',18],['var(--font-body)',700,'normal',18],['var(--font-heading)',400,'normal',28],['var(--font-heading)',400,'italic',24]]){
            const section=document.createElement('section');section.style.cssText='margin-bottom:28px;';
            const label=document.createElement('p');label.textContent=`${family} / ${weight} / ${style} / ${size}px`;
            label.style.cssText='font:12px Arial,sans-serif;margin-bottom:8px;';
            const text=document.createElement('p');text.textContent=probe+'\\n'+glyphs;
            text.style.cssText=`font-family:${family};font-weight:${weight};font-style:${style};font-size:${size}px;line-height:1.7;white-space:pre-line;`;
            section.append(label,text);document.body.append(section);
          }
        }''', {'probe': PROBE, 'glyphs': GLYPHS, 'phase': phase})
        page.evaluate('document.fonts.ready')
        page.screenshot(path=str(OUT / f'font-{phase}.png'), full_page=True)
        browser.close()
    (OUT / f'audit-{phase}.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=True, indent=2))

if __name__ == '__main__':
    main()
