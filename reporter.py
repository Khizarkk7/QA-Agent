# reporter.py
import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
USE_HF = os.getenv("USE_HF", "false").lower() == "true"

def generate_report(results):
    try:
        if OPENAI_KEY:
            return generate_openai_report(results)
    except:
        pass
    return generate_basic_report(results)

def generate_basic_report(results):
    lines = []
    for r in results:
        lines.append(f"--- URL: {r['url']} ---")
        lines.append(f"Title: {r['title']}")
        lines.append(f"Status: {r['status']}")
        lines.append(f"Buttons: {len(r['buttons'])} checked")
        for b in r['buttons']:
            lines.append(f"  {b['status']} -> {b['selector'][:50]}")
        lines.append(f"Forms: {len(r['forms'])}")
        lines.append(f"Links (first 5): {[l['href'] for l in r['links']]}")
        if r['console_errors']:
            lines.append("Console Errors:")
            for e in r['console_errors']:
                lines.append(f"  {e}")
        lines.append(f"Screenshot saved: {r['screenshot']}")
    return "\n".join(lines)

def generate_openai_report(results):
    import json
    # import openai at runtime to avoid static import errors when the package isn't installed
    try:
        import importlib
        openai = importlib.import_module("openai")
    except Exception:
        # openai not available; fall back to the basic report
        return generate_basic_report(results)

    openai.api_key = OPENAI_KEY
    prompt = f"Analyze these QA test results and generate a short QA report:\n{json.dumps(results, default=str)}"

    # Try the older Completion API first, then fall back to ChatCompletion if necessary.
    try:
        resp = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            temperature=0.2
        )
        return resp.choices[0].text.strip()
    except Exception:
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.2
            )
            return resp.choices[0].message["content"].strip()
        except Exception:
            return generate_basic_report(results)
