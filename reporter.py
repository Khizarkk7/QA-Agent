# reporter.py
import os, json
from dotenv import load_dotenv
load_dotenv()

USE_HF = os.getenv("USE_HF", "false").lower() == "true"
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# Try OpenAI first, else basic summarizer
def generate_report(results):
    # results is list of scenario_result dicts
    if OPENAI_KEY:
        try:
            return generate_openai_report(results)
        except Exception as e:
            print("OpenAI reporting failed, falling back. Err:", e)
    # fallback
    return generate_basic_report(results)

def generate_basic_report(results):
    lines = []
    for r in results:
        name = r.get("name")
        url = r.get("url")
        lines.append(f"--- {name} ({url}) ---")
        console = r.get("console") or []
        errors = r.get("errors") or []
        checks = r.get("checks") or []
        for c in checks:
            typ, detail, ok, info = c
            status = "PASS" if ok else "FAIL"
            lines.append(f"{typ}: {detail} -> {status} ({info})")
        if console:
            # show up to 5 console lines
            lines.append("Console logs:")
            for ln in console[:5]:
                lines.append("  " + ln)
        if errors:
            lines.append("Errors:")
            for err in errors:
                lines.append("  " + (err.splitlines()[0] if err else "error"))
    return "\n".join(lines)

def generate_openai_report(results):
    try:
        import importlib
        openai = importlib.import_module("openai")
    except Exception:
        # OpenAI SDK not available; fall back to basic report
        return generate_basic_report(results)

    openai.api_key = OPENAI_KEY
    # Prepare prompt
    summary = json.dumps(results, default=str)[:15000]  # truncate large
    prompt = f"You're an expert QA engineer. Analyze these automated test results and produce a short, actionable QA report with PASS/FAIL statements and suggested fixes:\n\n{summary}\n\nReport:"
    # Try Completion API, fall back to ChatCompletion if necessary
    try:
        resp = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=400,
            temperature=0.2
        )
        return resp.choices[0].text.strip()
    except Exception:
        # Attempt ChatCompletion for newer OpenAI SDKs
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.2
        )
        # compatible access to message content
        try:
            return resp.choices[0].message['content'].strip()
        except Exception:
            return resp.choices[0].message.content.strip()
