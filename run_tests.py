# run_tests.py
import json, os, time
from utils import log_info
from tester import run_all
from reporter import generate_report

SCENARIO_FILE = "scenarios.json"

def load_scenarios():
    with open(SCENARIO_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    log_info("Loading scenarios...")
    scenarios = load_scenarios()
    log_info(f"{len(scenarios)} scenarios loaded.")
    results = run_all(scenarios)
    report = generate_report(results)
    print("\n\n===== QA AGENT REPORT =====\n")
    print(report)
    print("\n===== END REPORT =====\n")
    # Optionally: save report to file
    with open("artifacts/qa_report.txt", "w", encoding="utf-8") as f:
        f.write(report)

if __name__ == "__main__":
    main()
