"""Scroll-capture each course page and encode a short walkthrough video per module."""
import os
import pathlib
import shutil
import subprocess

os.environ['PLAYWRIGHT_BROWSERS_PATH'] = 'C:/Users/insig/AppData/Local/ms-playwright'
from playwright.sync_api import sync_playwright

BASE = pathlib.Path('C:/Users/insig/figures/upskill-hermes')
PAGES = BASE / 'pages'
OUT = BASE / 'video'
OUT.mkdir(exist_ok=True)
FRAMES = BASE / '_frames'
FFMPEG = 'C:/Users/insig/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.1-full_build/bin/ffmpeg.exe'

TARGETS = [
    ('00-course-map', 'index.html'),
    ('01-agentic-revolution', 'module-1-agentic-revolution.html'),
    ('02-ai-literacy', 'module-2-ai-literacy.html'),
    ('03-building-agents', 'module-3-building-agents.html'),
    ('04-strategy-ethics', 'module-4-strategy-ethics.html'),
    ('05-advanced-topics', 'module-5-advanced-topics.html'),
]


def capture(page, html, out_dir, viewport_h=900, step=150):
    page.goto((PAGES / html).as_uri(), wait_until='load')
    page.wait_for_timeout(300)
    height = page.evaluate("Math.max(document.body.scrollHeight, document.documentElement.scrollHeight, document.body.offsetHeight)")
    y, n = 0, 0
    while y < height:
        page.evaluate("window.scrollTo(0, %d)" % y)
        page.wait_for_timeout(90)
        page.screenshot(path=str(out_dir / ('f_%03d.png' % n)))
        n += 1
        y += step
        if n > 140:
            break
    return n


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page(viewport={'width': 900, 'height': 900}, device_scale_factor=1)
        for name, html in TARGETS:
            if not (PAGES / html).exists():
                print('skip', html)
                continue
            d = FRAMES / name
            if d.exists():
                shutil.rmtree(d)
            d.mkdir(parents=True)
            n = capture(page, html, d)
            out = OUT / (name + '.mp4')
            subprocess.run([FFMPEG, '-y', '-framerate', '6', '-i', str(d / 'f_%03d.png'),
                            '-vf', 'scale=900:-2', '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
                            '-crf', '23', '-movflags', '+faststart', str(out)],
                           check=True, capture_output=True)
            print('%-26s %2d frames  %6.1f KB  %s' % (name, n, out.stat().st_size / 1024, out.name))
        b.close()


if __name__ == '__main__':
    main()
