from utils import log_info, ensure_dir
from tester import run_all
from reporter import generate_report
import os

#  Define pages to test
# "login": True → this page will trigger login using .env credentials
urls = [
    {"url": "http://192.168.70.94:4200/login", "login": False},  # Public login page
    {"url": "http://192.168.70.94:4200/app-admin/dashboard", "login": True} ,
    {"url": "http://192.168.70.94:4200/app-admin/shops/1026/products/all", "login": True},  # Protected
    # Protected
]

def main():
    log_info("🚀 Starting QA Agent...")
    results = run_all(urls)
    report = generate_report(results)

    # Print report in console
    print("\n\n===== QA AGENT REPORT =====\n")
    print(report)
    print("\n===== END REPORT =====\n")

    # Save report to file
    ensure_dir("artifacts")
    with open(os.path.join("artifacts", "qa_report.txt"), "w", encoding="utf-8") as f:
        f.write(report)

if __name__ == "__main__":
    main()
