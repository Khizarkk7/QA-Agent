# QA Agent Console — Automated Frontend QA Tool
Open-Source QA Automation Agent for Angular/SPA Applications

---

## Project Overview
This project is a console-based QA Agent designed to automate frontend testing for web applications, especially SPAs (Single Page Applications) built with frameworks like Angular or React.

The QA Agent uses:

- **Playwright**: for browser automation and frontend testing
- **Python**: as the scripting language
- **OpenAI / AI summarizer**: optional layer to generate human-readable QA reports
- **Logging and Screenshots**: for easy debugging of failures

**Purpose:**

- Automatically test web pages for key checks (title, element presence, console errors, status codes)
- Generate actionable QA reports for developers and testers
- Serve as a foundation for building more advanced QA agents for open-source contribution


## Features

- Test multiple pages using JSON-based scenarios
- Supports SPA pages with network idle wait
- Capture console logs, errors, and screenshots
- Optional AI-based report generation using OpenAI API
- Console-based output and optional file reports
- Easy to extend with new checks and scenarios

## Configuration

1. Create a .env file in the project root (an example .env is included in the repo):

OPENAI_API_KEY=your_openai_api_key_here
USE_HF=false
ARTIFACTS_DIR=artifacts

2. Define QA scenarios in scenarios.json (an example file is included):

[
  {
    "name": "Homepage",
    "url": "http://localhost:4200/",
    "checks": [
      {"type": "page_title_contains", "value": "K Store"},
      {"type": "element_exists", "selector": "nav"},
      {"type": "no_console_errors"}
    ]
  },
  {
    "name": "Product List",
    "url": "http://localhost:4200/shop/levis",
    "checks": [
      {"type": "status_code_200"},
      {"type": "element_exists", "selector": ".product-card"},
      {"type": "click_and_wait", "selector": ".product-card:first-child a"}
    ]
  }
]

## Running the QA Agent
python run_tests.py

## How It Works

Scenario Loader: Reads JSON test scenarios

Playwright Test Runner: Opens browser, navigates pages, performs checks, captures console logs and errors

Reporter: Summarizes results in console and/or AI-generated report

Artifacts: Screenshots and reports saved for debugging and tracking


## Contributing

This project is open source. Contributions are welcome to improve QA checks, reporting, and support for additional frameworks.

How to contribute:

Fork the repository

Create a new branch: git checkout -b feature/new-check

Make your changes or improvements

Commit changes: git commit -m "Add new check for login page"

Push to branch: git push origin feature/new-check

Open a Pull Request

## License

This project is licensed under MIT License — open source and free to use.

## Contact

Maintainer: Khizar Saqib

Email: khzrsaqib@gmail.com
GitHub: https://github.com/khizarkk7

