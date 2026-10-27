import os, pathlib
os.environ['PLAYWRIGHT_BROWSERS_PATH'] = 'C:/Users/insig/AppData/Local/ms-playwright'
from playwright.sync_api import sync_playwright
P = pathlib.Path('C:/Users/insig/figures/upskill-hermes/pages')
O = pathlib.Path('C:/Users/insig/figures/upskill-hermes/shots'); O.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={'width': 390, 'height': 860}, device_scale_factor=2)
    page.goto((P/'module-3-building-agents.html').as_uri()); page.wait_for_timeout(300)
    page.screenshot(path=str(O/'m3-top-phone.png'))
    page.evaluate("window.scrollTo(0, 1500)"); page.wait_for_timeout(200)
    page.screenshot(path=str(O/'m3-mid-phone.png'))
    page.evaluate("window.scrollTo(0, 3600)"); page.wait_for_timeout(200)
    page.screenshot(path=str(O/'m3-late-phone.png'))
    page.goto((P/'index.html').as_uri()); page.wait_for_timeout(300)
    page.screenshot(path=str(O/'index-top-phone.png'))
    b.close()
    print('ok')
