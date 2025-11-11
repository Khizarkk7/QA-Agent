QA Agent Console — Automated Frontend QA Tool

Open-Source QA Automation Agent for Angular/SPA Applications

Project Overview

This project is a console-based QA Agent designed to automate frontend testing for web applications, especially SPAs (Single Page Applications) built with frameworks like Angular or React.

The QA Agent uses:

Playwright: for browser automation and frontend testing

Python: as the scripting language

OpenAI / AI summarizer: optional layer to generate human-readable QA reports

Logging and Screenshots: for easy debugging of failures

Purpose:

Automatically test web pages for key checks (title, element presence, console errors, status codes)

Generate actionable QA reports for developers and testers

Serve as a foundation for building more advanced QA agents for open-source contribution

Screenshot Placeholder:

[Insert sample QA Agent test screenshot here]

Features

Test multiple pages using JSON-based scenarios

Supports SPA pages with network idle wait

Capture console logs, errors, and screenshots

Optional AI-based report generation using OpenAI API

Console-based output and optional file reports

Easy to extend with new checks and scenarios

Screenshot Placeholder:

[Insert screenshot showing feature execution here]

Getting Started
Prerequisites

Python 3.11+ installed

Git (optional, for cloning)

Installation
# Clone the repository
git clone https://github.com/<your-username>/qa-agent-console.git
cd qa-agent-console

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows CMD
.venv\Scripts\activate
# PowerShell
# .\.venv\Scripts\Activate.ps1
# macOS / Linux
# source .venv/bin/activate

# Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install

Configuration

Create a .env file in the project root:

OPENAI_API_KEY=your_openai_api_key_here
USE_HF=false
ARTIFACTS_DIR=artifacts


Define QA scenarios in scenarios.json (example):

[
  {
    "name": "Homepage",
    "url": "http://localhost:4200/",
    "checks": [
      {"type": "page_title_contains", "value": "K Store"},
      {"type": "element_exists", "selector": "nav"},
      {"type": "no_console_errors"}
    ]
  }
]

Running the QA Agent
python run_tests.py


Console will display results for each page

Screenshots and QA report will be saved in the artifacts/ folder

AI-based summarization will be generated if OPENAI_API_KEY is provided

Screenshot Placeholder:

[Insert screenshot of console test output here]

How It Works

Scenario Loader: Reads JSON test scenarios

Playwright Test Runner: Opens browser, navigates pages, performs checks, captures console logs and errors

Reporter: Summarizes results in console and/or AI-generated report

Artifacts: Screenshots and reports saved for debugging and tracking

Screenshot Placeholder:

[Insert diagram or screenshot showing workflow here]

Contributing

This project is open source. Contributions are welcome to improve QA checks, reporting, and support for additional frameworks.

How to contribute:

Fork the repository

Create a new branch: git checkout -b feature/new-check

Make your changes or improvements

Commit changes: git commit -m "Add new check for login page"

Push to branch: git push origin feature/new-check

Open a Pull Request

Future Enhancements

Add support for login/authentication flows

Visual regression testing with screenshot comparisons

Integration with CI/CD pipelines (GitHub Actions, Jenkins)

Extend checks for API responses and backend validation

AI-powered suggestions for failing tests

License

This project is licensed under MIT License — open source and free to use.

Contact

Maintainer: Khizar Saqib
Email: khzrsaqib@gmail.com

GitHub: https://github.com/khizarkk7
