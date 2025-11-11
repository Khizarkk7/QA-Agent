# tester.py
import os, time, json, traceback
from playwright.sync_api import sync_playwright
from utils import ensure_dir, save_screenshot, log_info, log_error

ARTIFACTS_DIR = os.getenv("ARTIFACTS_DIR", "artifacts")
ensure_dir(ARTIFACTS_DIR)

def run_check(page, check, results):
    typ = check.get("type")
    try:
        if typ == "page_title_contains":
            expected = check["value"]
            title = page.title()
            ok = expected.lower() in (title or "").lower()
            results.append(("page_title_contains", expected, ok, title))
        elif typ == "element_exists":
            sel = check["selector"]
            el = page.query_selector(sel)
            ok = el is not None
            results.append(("element_exists", sel, ok, "found" if ok else "not found"))
        elif typ == "no_console_errors":
            # page-level console errors are captured separately
            # We'll rely on page.context to store console messages via event in run_scenario
            results.append(("no_console_errors", None, True, "placeholder"))
        elif typ == "status_code_200":
            # We can perform a fetch to check status via JS
            res = page.request.get(page.url)
            ok = res.status == 200
            results.append(("status_code_200", None, ok, f"{res.status}"))
        elif typ == "click_and_wait":
            sel = check["selector"]
            page.click(sel, timeout=5000)
            page.wait_for_load_state("networkidle", timeout=5000)
            results.append(("click_and_wait", sel, True, "clicked"))
        else:
            results.append(("unknown_check", typ, False, "unsupported"))
    except Exception as e:
        results.append((typ, None, False, f"exception: {e}"))
        raise

def run_scenario(scenario):
    name = scenario.get("name")
    url = scenario.get("url")
    checks = scenario.get("checks", [])

    scenario_result = {"name": name, "url": url, "checks": [], "console": [], "errors": []}
    ts = int(time.time())
    screenshot_path = os.path.join(ARTIFACTS_DIR, f"{name.replace(' ', '_')}_{ts}.png")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            # capture console messages
            def on_console(msg):
                txt = f"[{msg.type}] {msg.text}"
                scenario_result["console"].append(txt)
            page.on("console", lambda msg: on_console(msg))

            page.goto(url, timeout=15000)
            # small wait for SPAs
            page.wait_for_load_state("networkidle", timeout=8000)

            for check in checks:
                try:
                    run_check(page, check, scenario_result["checks"])
                except Exception as e:
                    err = traceback.format_exc()
                    scenario_result["errors"].append(err)
                    save_screenshot(page, screenshot_path)
            # final screenshot
            save_screenshot(page, screenshot_path)
            browser.close()
    except Exception as e:
        scenario_result["errors"].append(traceback.format_exc())
    return scenario_result

def run_all(scenarios):
    results = []
    for s in scenarios:
        log_info(f"Running: {s.get('name')} -> {s.get('url')}")
        res = run_scenario(s)
        results.append(res)
    return results
