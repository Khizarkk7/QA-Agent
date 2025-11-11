import os, time, traceback
from playwright.sync_api import sync_playwright
from utils import ensure_dir, save_screenshot, log_info
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

USERNAME = os.getenv("QA_USERNAME")
PASSWORD = os.getenv("QA_PASSWORD")
LOGIN_URL = os.getenv("LOGIN_URL", "http://192.168.70.94:4200/login")

ARTIFACTS_DIR = os.getenv("ARTIFACTS_DIR", "artifacts")
ensure_dir(ARTIFACTS_DIR)


def perform_login(page):
    """Perform login if login page is required."""
    log_info("Performing login...")

    page.goto(LOGIN_URL, timeout=30000)
    page.wait_for_load_state("networkidle", timeout=10000)

    # Fill credentials
    page.fill('input[name="email"]', USERNAME)
    page.fill('input[name="password"]', PASSWORD)
    page.click('button[type="submit"]')

    page.wait_for_load_state("networkidle", timeout=15000)
    log_info("Login successful (if credentials are valid)")


def test_page(url, login=False):
    """Main testing logic for a given URL."""
    result = {
        "url": url,
        "title": None,
        "buttons": [],
        "links": [],
        "forms": [],
        "console_errors": [],
        "network": [],
        "screenshot": None,
        "status": "PASS"
    }

    ts = int(time.time())
    screenshot_path = os.path.join(ARTIFACTS_DIR, f"{ts}.png")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
            context = browser.new_context(ignore_https_errors=True)
            page = context.new_page()

            # Capture console errors
            page.on("console", lambda msg: result["console_errors"].append(f"[{msg.type}] {msg.text}"))

            # Capture network requests safely
            def network_listener(req):
                try:
                    status = req.response.status if req.response else None
                except:
                    status = None
                result["network"].append({
                    "url": req.url,
                    "method": req.method,
                    "status": status
                })

            page.on("requestfinished", network_listener)

            # If login required, perform login before accessing URL
            if login:
                perform_login(page)

            # Go to target page
            page.goto(url, timeout=30000)
            page.wait_for_load_state("networkidle", timeout=15000)

            # Page title
            try:
                result["title"] = page.title()
            except:
                result["title"] = "N/A"

            # Wait for buttons/forms to load
            try:
                page.wait_for_selector("button, input[type='submit'], input[type='button'], form", timeout=10000)
            except:
                pass

            # Buttons
            buttons = page.query_selector_all("button, input[type='button'], input[type='submit']")
            for b in buttons:
                try:
                    b.click(timeout=3000)
                    outer_html = b.get_attribute("outerHTML") or "<unknown>"
                    result["buttons"].append({"selector": outer_html, "status": "PASS"})
                except:
                    outer_html = b.get_attribute("outerHTML") or "<unknown>"
                    result["buttons"].append({"selector": outer_html, "status": "FAIL"})
                    result["status"] = "FAIL"

            # Links (first 5)
            links = page.query_selector_all("a")
            for l in links[:5]:
                href = l.get_attribute("href") or "<unknown>"
                result["links"].append({"href": href})

            # Forms
            forms = page.query_selector_all("form")
            for f in forms:
                form_name = f.get_attribute("name") or f.get_attribute("id") or "unknown"
                result["forms"].append({"name": form_name})

            # Screenshot
            try:
                save_screenshot(page, screenshot_path)
                result["screenshot"] = screenshot_path
            except Exception as e:
                result["console_errors"].append(f"Screenshot error: {str(e)}")
                result["screenshot"] = None

            browser.close()

    except Exception as e:
        result["status"] = "FAIL"
        result["console_errors"].append(str(e))
        print(traceback.format_exc())

    return result


def run_all(urls):
    """Run all URLs in sequence."""
    results = []
    for item in urls:
        if isinstance(item, dict):
            url = item.get("url")
            login_flag = item.get("login", False)
        else:
            url = item
            login_flag = False

        log_info(f"Testing URL: {url} | login={login_flag}")
        res = test_page(url, login=login_flag)
        results.append(res)

    return results
