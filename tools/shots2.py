import os, pathlib
os.environ['PLAYWRIGHT_BROWSERS_PATH'] = 'C:/Users/insig/AppData/Local/ms-playwright'
from playwright.sync_api import sync_playwright
PAGES = pathlib.Path('C:/Users/insig/figures/upskill-hermes/pages')
OUT = pathlib.Path('C:/Users/insig/figures/upskill-hermes/shots'); OUT.mkdir(exist_ok=True)
TARGETS = [('index','index.html'), ('lesson-01','lesson-01.html'), ('lesson-09','lesson-09.html'),
           ('module-3','module-3-building-agents.html')]
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
    for name, f in TARGETS:
        page.goto((PAGES/f).as_uri(), wait_until='load'); page.wait_for_timeout(250)
        page.screenshot(path=str(OUT/(name+'-phone.png')), full_page=True); print('shot', name)
    page.close()
    d = b.new_page(viewport={'width': 1180, 'height': 900}, device_scale_factor=2)
    for name, f in (('index','index.html'), ('module-3','module-3-building-agents.html')):
        d.goto((PAGES/f).as_uri(), wait_until='load'); d.wait_for_timeout(250)
        d.screenshot(path=str(OUT/(name+'-desktop.png')), full_page=True); print('shot', name, 'desktop')
    b.close()
