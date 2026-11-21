#!/usr/bin/env python3
"""Browser QA of the deployed static site content, with four screenshots."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright

SITE = Path(__file__).resolve().parents[1] / "site"
OUT = Path(__file__).resolve().parents[1] / "screenshots"
OUT.mkdir(exist_ok=True)

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(SITE), **kwargs)
    def log_message(self, format, *args):
        pass

def main():
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    Thread(target=server.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:" + str(server.server_port) + "/"
    failures = []
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            for width in (320, 375, 768, 1280, 1920):
                context = browser.new_context(
                    viewport={"width": width, "height": 830},
                    device_scale_factor=1,
                    reduced_motion="reduce"
                )
                page = context.new_page()
                page.on("pageerror", lambda err: failures.append("Browser script error: " + str(err)))
                page.on("console", lambda msg: failures.append("Console: " + msg.text) if msg.type == "error" else None)
                page.on("response", lambda response: failures.append("HTTP " + str(response.status) + ": " + response.url) if response.status >= 400 else None)
                page.goto(base, wait_until="networkidle")
                page.evaluate("document.fonts.ready")
                assert page.locator("h1").is_visible(), "No hero at " + str(width)
                assert page.locator("#project-list article").count() >= 1, "No projects"
                assert page.locator(".empty-state").is_visible(), "Missing empty support state"
                assert page.locator("html").get_attribute("data-theme") == "dark", "Terminal not default"
                overflow = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
                assert overflow <= 1, "Horizontal overflow at " + str(width) + "px: " + str(overflow)
                assert page.locator("img.brand__logo--dark").evaluate("(img) => img.complete && img.naturalWidth > 0"), "Logo not loaded"
                if width in (375, 1280):
                    name = "mobile" if width == 375 else "desktop"
                    page.screenshot(path=str(OUT / ("terminal-" + name + ".png")), full_page=True)
                    page.locator('[data-theme-select="light"]').click()
                    assert page.locator("html").get_attribute("data-theme") == "light", "Paper switch broken"
                    page.locator('[data-lang="en"]').click()
                    assert "Independent development" in page.locator("h1").inner_text(), "EN switch broken"
                    page.reload(wait_until="networkidle")
                    assert page.locator("html").get_attribute("data-theme") == "light", "Theme preference not persisted"
                    assert page.locator("html").get_attribute("lang") == "en", "Language preference not persisted"
                    page.screenshot(path=str(OUT / ("paper-" + name + ".png")), full_page=True)
                context.close()
                print("PASS viewport:", width)
            browser.close()
        assert not failures, "\n".join(failures)
        print("PASS no 404/console errors. Screenshots:", *sorted(str(p.name) for p in OUT.glob("*.png")))
    finally:
        server.shutdown()

if __name__ == "__main__":
    main()
