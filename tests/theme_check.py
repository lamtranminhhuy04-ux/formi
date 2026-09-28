"""Extended typography, theme, accessibility and regression audit.
Optional QA dependencies: playwright, fonttools[woff], html5lib, tinycss2.
No dependencies or build steps are added to the website.
"""
import functools
import hashlib
import http.server
import io
import json
from pathlib import Path
import re
import threading
import time
import unicodedata
import wave
import xml.etree.ElementTree as ET

import html5lib
import tinycss2
from fontTools.ttLib import TTFont
from playwright.sync_api import sync_playwright
from font_probe import PROBE, GLYPHS, rendered_fonts

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tests/artifacts'
OUT.mkdir(exist_ok=True)
report = {'checks': [], 'contrast': {}, 'responsive': [], 'fonts': {}, 'network': {}, 'performance': {}}

def check(value, label):
    assert value, label
    report['checks'].append(label)

def luminance(hex_value):
    rgb = [int(hex_value[i:i+2], 16) / 255 for i in (1, 3, 5)]
    rgb = [x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4 for x in rgb]
    return .2126 * rgb[0] + .7152 * rgb[1] + .0722 * rgb[2]

def contrast(a, b):
    lo, hi = sorted([luminance(a), luminance(b)])
    return (hi + .05) / (lo + .05)

html = (ROOT / 'index.html').read_bytes()
check(0 <= html.lower().find(b'<meta charset="utf-8">') < 1024, 'UTF-8 declared within first 1024 bytes')
for path in [ROOT / 'index.html', *ROOT.glob('css/*.css'), *ROOT.glob('js/*.js')]:
    source = path.read_bytes().decode('utf-8', errors='strict')
    check('\ufffd' not in source and not any(x in source for x in ['Ã¡', 'áº', 'â€']), f'UTF-8 without mojibake: {path.name}')
    check(unicodedata.normalize('NFC', source) == source, f'NFC text: {path.name}')
parser = html5lib.HTMLParser(strict=False)
parser.parse(html.decode('utf-8'))
check(not parser.errors, f'HTML5 parser errors: {parser.errors}')
for path in ROOT.glob('assets/**/*.svg'):
    ET.parse(path)
check(True, 'All SVG assets parse as XML')
for path in ROOT.glob('css/*.css'):
    rules = tinycss2.parse_stylesheet(path.read_text(encoding='utf-8'), skip_comments=True, skip_whitespace=True)
    check(not any(rule.type == 'error' for rule in rules), f'CSS parses: {path.name}')

css = (ROOT / 'css/styles.css').read_text(encoding='utf-8')
root_tokens = css[css.index(':root {'):css.index('}', css.index(':root {'))]
tokens = dict(re.findall(r'--([\w-]+):\s*(#[\da-fA-F]{6,8});', root_tokens))
for token in ['color-background', 'color-section', 'color-surface', 'color-primary', 'color-primary-dark', 'color-text', 'color-text-muted', 'color-border', 'color-focus']:
    check(token in tokens, f'Pastel token: {token}')
check(not re.search(r'#[\da-fA-F]{3,8}\b', css[css.index('}', css.index(':root {'))+1:]), 'All CSS colors centralized in root tokens')
check(not any(color in css.lower() for color in ['#f7f2e8', '#803d49', '#43392f', '#76685b', '#e9ebdf', '#ece5dc']), 'Old brown/olive UI theme removed')
check('Georgia' not in css and 'sans-serif' in css and '"Times New Roman"' in css, 'Full Vietnamese fallback stacks replace Georgia')
fonts_css = (ROOT / 'css/fonts.css').read_text(encoding='utf8')
check(fonts_css.count('font-display: swap') == 3, 'All three font faces use swap')
check('font-weight: 400 700' in fonts_css and 'font-style: italic' in fonts_css, 'Actual variable body weights and italic heading face declared')
check((ROOT / '.nojekyll').exists(), '.nojekyll remains at project root')

# Validate every local static/data asset path with case-sensitive directory lookup.
assets = set()
for path in [ROOT / 'index.html', *ROOT.glob('js/*.js')]:
    source = path.read_text(encoding='utf8')
    assets.update(re.findall(r'["\']((?:assets|css|js)/[^"\']+)["\']', source))
for path in ROOT.glob('css/*.css'):
    for raw in re.findall(r'url\(["\']?([^"\')]+)', path.read_text(encoding='utf8')):
        resolved = (path.parent / raw).resolve()
        assets.add(resolved.relative_to(ROOT).as_posix())
for relative in sorted(assets):
    current = ROOT
    for part in Path(relative).parts:
        check(part in [p.name for p in current.iterdir()], f'Exact-case path: {relative} / {part}')
        current = current / part
check(not re.search(r'(?:src|href)=["\']/[^/]', html.decode()), 'No domain-root asset URLs')

required = {ord(c) for c in PROBE + GLYPHS if not c.isspace()}
required.update(range(0x1EA0, 0x1EFA))
required.update(ord(c) for c in unicodedata.normalize('NFD', PROBE + GLYPHS) if not c.isspace())
for path in (ROOT / 'assets/fonts').glob('*.woff2'):
    font = TTFont(path)
    missing = required - set(font.getBestCmap())
    check(not missing, f'Full Vietnamese NFC/NFD coverage: {path.name}')
    report['fonts'][path.name] = {'bytes': path.stat().st_size, 'missing': sorted(missing)}
check(sum(v['bytes'] for v in report['fonts'].values()) < 160000, 'All local web fonts total under 160 KB')
for pair in [('color-text', 'color-background'), ('color-text-muted', 'color-background'), ('color-text-muted', 'color-section'), ('color-primary-dark', 'color-paper-pink'), ('color-on-primary', 'color-primary-dark'), ('color-text', 'color-envelope'), ('color-text-muted', 'color-envelope'), ('color-success-dark', 'color-surface'), ('color-disabled-text', 'color-disabled-background')]:
    ratio = contrast(tokens[pair[0]], tokens[pair[1]])
    report['contrast'][' / '.join(pair)] = round(ratio, 2)
    check(ratio >= 4.5, f'AA text contrast: {pair} = {ratio:.2f}:1')
check(contrast(tokens['color-focus'], tokens['color-background']) >= 3, 'Focus outline contrast >= 3:1')

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Handler, directory=str(ROOT.parent)))
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f'http://127.0.0.1:{server.server_port}/{ROOT.name}/'
source_data = (ROOT / 'js/data.js').read_text(encoding='utf8')
data_hash = hashlib.sha256((ROOT / 'js/data.js').read_bytes()).hexdigest()

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    context = browser.new_context(reduced_motion='reduce', viewport={'width': 1440, 'height': 960})
    page = context.new_page()
    errors, warnings, failed, responses = [], [], [], []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else warnings.append(m.text) if m.type == 'warning' else None)
    page.on('requestfailed', lambda r: failed.append(r.url))
    page.on('response', lambda r: responses.append({'url': r.url, 'status': r.status}))
    page.add_init_script('''window.auditCLS=0;new PerformanceObserver(list=>{for(const e of list.getEntries())if(!e.hadRecentInput)window.auditCLS+=e.value;}).observe({type:'layout-shift',buffered:true});''')
    page.goto(base)
    page.evaluate('document.fonts.ready')
    page.wait_for_timeout(300)
    report['performance']['initialCLS'] = page.evaluate('window.auditCLS')
    check(report['performance']['initialCLS'] <= .1, 'Initial layout shift <= 0.1')
    check(page.locator('h1').count() == 1, 'One main heading')
    check(page.locator('header').count() == 1 and page.locator('main').count() == 1 and page.locator('footer').count() == 1, 'Semantic landmarks present')
    check(page.locator('main > section').count() == 11, 'All 12 journey steps retained (countdown and gift share one section)')
    check(page.evaluate('new Set([...document.querySelectorAll("[id]")].map(e=>e.id)).size === document.querySelectorAll("[id]").length'), 'No duplicate rendered IDs')
    check(page.evaluate('Array.from(document.querySelectorAll("a[href^=\\"#\\"]")).every(a=>document.getElementById(a.hash.slice(1)))'), 'Every in-page link has a target')
    check(page.evaluate('Array.from(document.images).every(i=>i.hasAttribute("alt") && i.alt.length>0)'), 'All images have nonempty alt text')
    check(page.evaluate('Array.from(document.querySelectorAll("button")).every(b=>b.getAttribute("aria-label") || b.textContent.trim())'), 'Every button has an accessible name')
    check(page.locator('#countdown').get_attribute('aria-live') is None, 'Countdown does not announce each second')
    check(page.locator('.quiz-feedback').get_attribute('role') == 'status', 'Quiz feedback is a polite status region')
    for selector, expected in [('#intro', 'Noto Sans'), ('#reason-title', 'Universe Serif'), ('#hero-caption', 'Universe Serif'), ('#signature', 'Universe Serif')]:
        faces = rendered_fonts(page, selector)
        check(len(faces) == 1 and faces[0]['familyName'] == expected and faces[0]['isCustomFont'], f'No mixed Vietnamese font in {selector}')

    # Pure language probes avoid legitimate system-font fallback for decorative symbols.
    page.evaluate('''({text})=>{const area=document.createElement('div');area.id='font-audit';
      for(const [family,weight,style] of [['Noto Sans',400,'normal'],['Noto Sans',600,'normal'],['Noto Sans',650,'normal'],['Noto Sans',700,'normal'],['Universe Serif',400,'normal'],['Universe Serif',400,'italic']]){
        const e=document.createElement('p');e.textContent=text;e.style.cssText=`font-family:"${family}";font-weight:${weight};font-style:${style};font-size:20px;line-height:1.8`;area.append(e);
      }document.body.append(area);}''', {'text': PROBE + ' ' + GLYPHS + ' ' + unicodedata.normalize('NFD', PROBE)})
    page.evaluate('document.fonts.ready')
    for i in range(6):
        faces = rendered_fonts(page, f'#font-audit p:nth-child({i+1})')
        check(len(faces) == 1 and faces[0]['isCustomFont'], f'Vietnamese regular/bold/italic render probe {i+1} uses one web font')
    page.locator('#font-audit').evaluate('(e)=>e.remove()')

    for width, height in [(320, 812), (375, 812), (768, 1024), (1024, 768), (1440, 960), (812, 375)]:
        page.set_viewport_size({'width': width, 'height': height})
        check(page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'No overflow at {width}x{height}')
        for img in page.locator('main img').all():
            img.scroll_into_view_if_needed()
        page.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
        # Plain paragraph/heading boxes should never vertically clip Vietnamese marks.
        clipped = page.locator('h1,h2,h3,p,.envelope-label,.caption').evaluate_all('''es=>es.filter(e=>e.getClientRects().length&&getComputedStyle(e).overflowY==='hidden'&&e.scrollHeight>e.clientHeight+1).map(e=>e.id||e.className)''')
        check(not clipped, f'No clipped text boxes at {width}x{height}: {clipped}')
        sizes = page.locator('#start,.map-pin,.quiz-option,#letters-grid button,#music').evaluate_all('es=>es.filter(e=>e.getClientRects().length).map(e=>({w:e.getBoundingClientRect().width,h:e.getBoundingClientRect().height}))')
        check(all(s['w'] >= 44 and s['h'] >= 44 for s in sizes), f'Primary touch targets >=44px at {width}x{height}')
        page.locator('.map-pin').nth(2).click()
        rect = page.locator('dialog').bounding_box()
        check(rect['x'] >= 0 and rect['y'] >= 0 and rect['x']+rect['width'] <= width+1 and rect['y']+rect['height'] <= height+1, f'Modal fits {width}x{height}')
        page.keyboard.press('Escape')
        page.locator('.polaroid').first.click()
        page.locator('#photo-next').click()
        check(page.locator('#photo-position').inner_text() == '2 / 6', f'Lightbox touch navigation at {width}x{height}')
        page.keyboard.press('Escape')
        page.locator('#final-envelope').click()
        check(page.locator('#final-letter').is_visible(), f'Final letter readable at {width}x{height}')
        check(page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'Open final letter does not overflow at {width}x{height}')
        report['responsive'].append({'width': width, 'height': height, 'overflow': False, 'modal': 'pass', 'touch': 'pass'})
    page.set_viewport_size({'width': 1440, 'height': 960})
    page.locator('#start').focus()
    page.keyboard.press('Tab')
    outline = page.evaluate('({style:getComputedStyle(document.activeElement).outlineStyle,width:getComputedStyle(document.activeElement).outlineWidth})')
    check(outline['style'] != 'none' and int(outline['width'].replace('px','')) >= 3, 'Keyboard focus has visible 3px outline')
    # Quiz updates progress immediately; both feedback paths remain textual.
    page.locator('.quiz-option').first.click()
    check(page.locator('progress').get_attribute('value') == '1', 'Quiz progress updates on answer, before next question')
    check(page.locator('.quiz-option.selected').inner_text().startswith('✓'), 'Correct answer marked with check and text')
    page.locator('.quiz-next').click()
    page.locator('.quiz-option').first.click()
    check(page.locator('.quiz-option.selected').inner_text().startswith('♡') and bool(page.locator('.quiz-feedback').inner_text()), 'Incorrect answer has kind textual feedback, not only color')

    # Separate browser contexts only: never touch the user's real localStorage.
    multi = browser.new_context(reduced_motion='reduce')
    a, b = multi.new_page(), multi.new_page()
    a.goto(base); b.goto(base)
    a.locator('#letters-grid button').nth(0).click()
    b.locator('#letters-grid button').nth(1).click()
    a.wait_for_function('document.querySelectorAll("#letters-grid .opened").length === 2')
    saved = json.loads(a.evaluate('localStorage.getItem(UNIVERSE_DATA.storageKey)'))
    check(set(saved['openedLetters']) == {'sad', 'miss'}, 'Two tabs preserve both opened letters')
    b.keyboard.press('Escape')
    for _ in range(5):
        b.locator('.quiz-option').first.click(); b.locator('.quiz-next').click()
    a.wait_for_function('document.getElementById("quiz-card").textContent.includes("CHÌA KHÓA")')
    check(True, 'Quiz completion synchronizes across tabs')
    b.evaluate('localStorage.removeItem(UNIVERSE_DATA.storageKey)')
    a.wait_for_function('document.querySelectorAll("#letters-grid .opened").length === 0')
    check(a.locator('.quiz-option').count() == 3, 'Explicit storage reset updates other tab and relocks gift')
    multi.close()

    # Missing-font fallback is an intentional simulated network failure, logged separately.
    fallback = browser.new_context(reduced_motion='reduce', viewport={'width': 375, 'height': 812})
    fallback.route('**/*.woff2', lambda route: route.abort('failed'))
    f = fallback.new_page(); f.goto(base); f.evaluate('document.fonts.ready')
    check(f.locator('#intro').inner_text().startswith('Giữa'), 'Text remains readable when web fonts fail')
    for sel, expected in [('#intro',{'Segoe UI','Noto Sans','Arial'}), ('#reason-title',{'Times New Roman'}), ('#hero-caption',{'Times New Roman'})]:
        faces = rendered_fonts(f, sel)
        check(len(faces) == 1 and faces[0]['familyName'] in expected and not faces[0]['isCustomFont'], f'Complete fallback font for {sel}: {faces}')
    check(f.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'Font fallback does not overflow mobile')
    f.locator('#letters-grid button').first.click()
    check(f.locator('dialog').is_visible(), 'Interaction works with fonts blocked')
    f.keyboard.press('Escape'); f.evaluate('scrollTo(0,0)'); f.screenshot(path=str(OUT / 'fallback-mobile.png'))
    fallback.close()

    # A valid generated WAV is served from memory only; data.js on disk is unchanged.
    wav_io = io.BytesIO()
    with wave.open(wav_io, 'wb') as wav:
        wav.setnchannels(1); wav.setsampwidth(2); wav.setframerate(8000); wav.writeframes(b'\x00\x00' * 8000)
    audio_context = browser.new_context(reduced_motion='reduce')
    audio_context.route('**/js/data.js', lambda route: route.fulfill(body=source_data.replace('audioSrc: ""', 'audioSrc: "assets/audio/test.wav"'), content_type='text/javascript; charset=utf-8'))
    audio_context.route('**/assets/audio/test.wav', lambda route: route.fulfill(body=wav_io.getvalue(), content_type='audio/wav'))
    au = audio_context.new_page(); au.goto(base)
    check(au.locator('#music').get_attribute('aria-pressed') == 'false', 'Configured audio does not autoplay')
    au.locator('#music').click()
    au.wait_for_function('document.getElementById("music").getAttribute("aria-pressed")==="true"')
    au.locator('#music').click()
    au.wait_for_function('document.getElementById("music").getAttribute("aria-pressed")==="false"')
    check(au.locator('#music').get_attribute('aria-pressed') == 'false', 'Audio play/pause works with a valid file')
    audio_context.close()
    missing_audio = browser.new_context(reduced_motion='reduce')
    missing_audio.route('**/js/data.js', lambda route: route.fulfill(body=source_data.replace('audioSrc: ""', 'audioSrc: "assets/audio/missing.mp3"'), content_type='text/javascript; charset=utf-8'))
    missing_audio.route('**/assets/audio/missing.mp3', lambda route: route.fulfill(status=404, body=''))
    ma = missing_audio.new_page(); ma.goto(base); ma.locator('#music').click()
    ma.wait_for_function('document.getElementById("music").disabled')
    check('khả dụng' in ma.locator('#music').inner_text(), 'Missing audio disables control with readable status')
    ma.locator('#letters-grid button').first.click()
    check(ma.locator('dialog').is_visible(), 'Missing audio does not break letters')
    missing_audio.close()

    missing_map = browser.new_context(reduced_motion='reduce')
    missing_map.route('**/js/data.js', lambda route: route.fulfill(body=source_data.replace('mapImage: "assets/images/map-placeholder.svg"', 'mapImage: "assets/images/missing-map.svg"'), content_type='text/javascript; charset=utf-8'))
    missing_map.route('**/assets/images/missing-map.svg', lambda route: route.fulfill(status=404, body=''))
    mm = missing_map.new_page(); mm.goto(base)
    mm.wait_for_function('document.getElementById("map-image").naturalWidth>0')
    check(mm.locator('#map-image').get_attribute('src') == 'assets/images/map-placeholder.svg', 'Missing custom map falls back to local illustrated map')
    missing_map.close()

    # file:// and normal static-server root, not just a fixed repository subpath.
    local = context.new_page(); local.goto((ROOT / 'index.html').as_uri()); local.evaluate('document.fonts.ready')
    check(rendered_fonts(local, '#reason-title')[0]['isCustomFont'], 'Local font loads through file://')
    local.close()
    root_server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Handler, directory=str(ROOT)))
    threading.Thread(target=root_server.serve_forever, daemon=True).start()
    local_http = context.new_page(); local_http.goto(f'http://127.0.0.1:{root_server.server_port}/'); local_http.evaluate('document.fonts.ready')
    check(local_http.locator('.timeline-item').count() == 6 and rendered_fonts(local_http, '#intro')[0]['isCustomFont'], 'Website and fonts work at a static-server root')
    local_http.close(); root_server.shutdown()

    check(not errors, f'Normal session console/JS errors: {errors}')
    check(not warnings, f'Normal session important console warnings: {warnings}')
    check(not failed and all(r['status'] < 400 for r in responses), 'No failed requests or 404s in normal session')
    check(all(r['url'].startswith(base) for r in responses), 'All runtime resources local to project subpath')
    report['network'] = {'errors': errors, 'warnings': warnings, 'failed': failed, 'responses': responses, 'intentional_failure_cases': ['blocked fonts', 'missing audio', 'missing custom map']}
    report['performance']['resourceBytes'] = page.evaluate('performance.getEntriesByType("resource").reduce((s,r)=>s+r.encodedBodySize,0)')
    browser.close()
server.shutdown()
check(hashlib.sha256((ROOT / 'js/data.js').read_bytes()).hexdigest() == data_hash, 'Tests never modify personal data.js')
(OUT / 'theme-results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"PASS: {len(report['checks'])} additional checks; report: {OUT / 'theme-results.json'}")
