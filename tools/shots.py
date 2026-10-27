"""Screenshot the course pages at phone and desktop widths, and build a printable PDF."""
import os
import pathlib

os.environ['PLAYWRIGHT_BROWSERS_PATH'] = 'C:/Users/insig/AppData/Local/ms-playwright'
from playwright.sync_api import sync_playwright

PAGES = pathlib.Path('C:/Users/insig/figures/upskill-hermes/pages')
OUT = pathlib.Path('C:/Users/insig/figures/upskill-hermes/shots')
OUT.mkdir(exist_ok=True)

TARGETS = [('index', 'index.html'), ('lesson-01', 'lesson-01.html'), ('lesson-09', 'lesson-09.html')]

with sync_playwright() as p:
    b = p.chromium.launch()
    for label, w, h, suffix in (('phone', 390, 844, '-phone'), ('desktop', 1180, 900, '-desktop')):
        page = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=2)
        for name, f in TARGETS:
            page.goto((PAGES / f).as_uri(), wait_until='load')
            page.wait_for_timeout(250)
            page.screenshot(path=str(OUT / (name + suffix + '.png')), full_page=True)
            print('shot', name + suffix)
        page.close()

    # printable PDF of all lessons, one page per lesson start
    page = b.new_page()
    page.goto((PAGES / 'index.html').as_uri(), wait_until='load')
    page.pdf(path=str(OUT / 'course-index.pdf'), format='A4', print_background=True,
             margin={'top': '14mm', 'bottom': '14mm', 'left': '12mm', 'right': '12mm'})
    print('pdf', OUT / 'course-index.pdf')
    b.close()
