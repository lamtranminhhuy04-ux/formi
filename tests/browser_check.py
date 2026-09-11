"""Optional maintainer QA: pip install playwright; python tests/browser_check.py.
Uses installed Edge; no dependency is required to run the website itself.
"""
import functools
import http.server
import json
from pathlib import Path
import threading
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tests' / 'artifacts'
OUT.mkdir(exist_ok=True)

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT.parent)))
threading.Thread(target=server.serve_forever, daemon=True).start()
URL = f'http://127.0.0.1:{server.server_port}/{ROOT.name}/'
report = []

def check(value, name):
    assert value, name
    report.append(name)

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    context = browser.new_context(reduced_motion='reduce')
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('console', lambda message: errors.append(message.text) if message.type == 'error' else None)
    page.goto(URL)
    page.wait_for_selector('.timeline-item')
    check(page.locator('.timeline-item').count() == 6, 'Six timeline events from data')
    check(page.locator('#music').is_disabled(), 'Music clearly disabled without source')
    for width in [320, 375, 768, 1024, 1440]:
        page.set_viewport_size({'width': width, 'height': 960})
        check(page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'No horizontal overflow at {width}px')
        # Visit each lazy image before full-page visual inspection.
        for image in page.locator('img').all():
            image.scroll_into_view_if_needed()
        page.wait_for_function('Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)')
        page.evaluate('window.scrollTo(0,0)')
        page.screenshot(path=str(OUT / f'page-{width}.png'), full_page=True)
        if width in [375,1440]:
            page.screenshot(path=str(OUT / f'hero-{width}.png'))
    page.locator('#start').click()
    check(page.evaluate('document.activeElement.id') == 'together', 'Start journey moves keyboard focus')
    for index in range(4):
        pin = page.locator('.map-pin').nth(index)
        pin.click()
        expected = page.evaluate(f'UNIVERSE_DATA.places[{index}].name')
        check(page.locator('#dialog-title').inner_text() == expected, f'Map pin {index+1} shows correct memory')
        page.keyboard.press('Escape')
        check(page.evaluate('document.activeElement.classList.contains("map-pin")'), 'Dialog restores focus')
    page.locator('.polaroid').first.click()
    page.keyboard.press('ArrowRight')
    check(page.locator('#photo-position').inner_text() == '2 / 6', 'Lightbox keyboard next')
    page.keyboard.press('ArrowLeft')
    check(page.locator('#photo-position').inner_text() == '1 / 6', 'Lightbox keyboard previous')
    page.locator('#photo-prev').click()
    check(page.locator('#photo-position').inner_text() == '6 / 6', 'Lightbox wraps around')
    for _ in range(8):
        page.keyboard.press('Tab')
        check(page.evaluate('Boolean(document.activeElement.closest("dialog"))'), 'Dialog traps keyboard focus')
    page.mouse.click(2, 2)
    check(not page.locator('dialog').is_visible(), 'Backdrop closes dialog')
    for index in range(4):
        page.locator('#letters-grid button').nth(index).click()
        check(page.locator('#dialog-content .prose p').count() == 2, f'Open-when letter {index+1} opens')
        page.keyboard.press('Escape')
    page.reload()
    check(page.locator('#letters-grid .opened').count() == 4, 'Opened letters persist on reload')
    page.evaluate('UNIVERSE_DATA.targetDate = "2099-01-01T00:00:00+07:00"')
    for index in range(5):
        page.locator('.quiz-option').first.click()
        check(bool(page.locator('.quiz-feedback').inner_text()), f'Quiz feedback {index+1}')
        page.locator('.quiz-next').click()
    check(page.locator('#quiz-card').inner_text().find('CHÌA KHÓA') >= 0, 'Quiz awards key regardless of score')
    check(page.locator('#gift-open').is_disabled(), 'Completed quiz cannot bypass future countdown')
    page.reload()
    check('CHÌA KHÓA' in page.locator('#quiz-card').inner_text(), 'Quiz completion persists')
    page.evaluate('UNIVERSE_DATA.targetDate = new Date(Date.now()+1800).toISOString()')
    page.wait_for_function('!document.getElementById("gift-open").disabled')
    check(page.locator('#count-days').inner_text() == '00', 'Countdown reaches zero automatically')
    page.locator('#gift-open').click()
    check(page.locator('#gift-content').is_visible(), 'Gift opens with both conditions')
    page.locator('#final-envelope').click()
    check(page.locator('#final-letter').is_visible(), 'Final letter opens')
    check(page.locator('.confetti').count() == 0, 'Reduced motion suppresses confetti')
    page.get_by_role('button', name='Chơi lại').click()
    check(page.locator('.quiz-option').count() == 3, 'Quiz can be replayed')
    check(page.evaluate('UniverseClock.elapsed("2099-01-01T00:00:00+07:00").days === 0'), 'Future start never negative')
    check(page.evaluate('UniverseClock.remaining("2000-01-01T00:00:00+07:00").seconds === 0'), 'Past countdown never negative')
    check(page.evaluate('UniverseClock.timestamp("2024-02-14T00:00:00+07:00") === Date.parse("2024-02-13T17:00:00Z")'), 'Explicit timezone is correct')
    check(page.evaluate('!UniverseClock.remaining("bad date").valid'), 'Invalid countdown fails closed')
    check(page.evaluate('Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)'), 'All local images load under project subpath')
    check(page.evaluate('Array.from(document.styleSheets).every(s => Array.from(s.cssRules).length > 0)'), 'All stylesheets parse')
    check(not errors, f'No browser console or JavaScript errors: {errors}')
    page.evaluate('localStorage.clear()')
    page.reload()
    page.evaluate('UNIVERSE_DATA.bypassCountdown = true')
    page.wait_for_function('document.getElementById("countdown-status").textContent.includes("thử nghiệm")')
    check(page.locator('#gift-open').is_disabled(), 'Countdown bypass still requires quiz')
    page.evaluate('localStorage.setItem(UNIVERSE_DATA.storageKey, "broken json")')
    page.reload()
    check(page.locator('.quiz-option').count() == 3, 'Corrupt storage safely ignored')
    blocked = browser.new_context()
    blocked.add_init_script('Object.defineProperty(window, "localStorage", {get(){throw new DOMException("Blocked", "SecurityError")}})')
    blocked_page = blocked.new_page()
    blocked_page.goto(URL)
    blocked_page.locator('#letters-grid button').first.click()
    check(blocked_page.locator('dialog').is_visible(), 'Blocked localStorage does not break interaction')
    blocked.close()
    local = context.new_page()
    local.goto((ROOT / 'index.html').as_uri())
    check(local.locator('.timeline-item').count() == 6, 'Direct file:// launch works without server')
    local.close()
    motion = browser.new_context(reduced_motion='no-preference', viewport={'width':375,'height':812})
    m = motion.new_page()
    m.goto(URL)
    m.locator('#final-envelope').click()
    m.wait_for_selector('#final-letter', state='visible')
    check(m.locator('.confetti').count() == 18, 'Confetti appears only after final letter opens')
    m.wait_for_timeout(2300)
    check(m.locator('.confetti').count() == 0, 'Confetti nodes are cleaned up')
    motion.close()
    browser.close()
server.shutdown()
(OUT / 'results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'PASS: {len(report)} checks. Screenshots: {OUT}')
