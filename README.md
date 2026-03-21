# Meesho Web Automation Framework

A robust, enterprise-grade web automation framework built with Python and Playwright for automating End-to-End ecommerce flows on Meesho.com. This framework is designed with production-ready patterns, focusing on stability, anti-bot evasion, and data-driven scalability.

## 🚀 Key Features

- **Playwright & Pytest**: High-performance cross-browser automation with native wait-for-load capabilities.
- **Page Object Model (POM)**: Clean separation of UI elements (locators) and business logic (actions) for high maintainability.
- **Data-Driven Testing (DDT)**: Dynamically executes search and checkout scenarios using external `JSON` data sources.
- **Advanced Stealth Engine**: Custom implementation for masking automation markers and mimicking human browser behavior to bypass sophisticated WAF/Bot detection.
- **Environment Agnostic**: Flexible configuration for `dev`, `qa`, and `prod` environments via `config.yaml`.
- **AI-Driven Dynamic Test Generation**: Uses Google Gemini (2.5 Flash) to automatically generate high-fidelity, realistic test cases (product names and test types) which are then executed by the framework.
- **AI-Powered Failure Analysis**: Automated root-cause detection. On failure, Gemini analyzes the captured HTML source and explains the probable reason (Identifying WAF blocks vs. UI state issues).
- **Hybrid AI Data Strategy**: Implemented a sophisticated hybrid strategy where test data is reused for stability and speed, but can be dynamically regenerated using a runtime `--fresh` flag.
- **Rich Diagnostic Reporting**: Automatic generation of:
  - **HTML Execution Reports**: Comprehensive test summaries with timestamps.
  - **Trace Files**: Deep debugging with Playwright's trace viewer.
  - **Visual Evidence**: Screenshots captured automatically on test failures.

## 📁 Project Structure

```text
Meesho_Automation/
├── data/
│   ├── search_products.json  # Static fallback keywords
│   └── ai_test_data.json     # Dynamically generated products (Gemini)
├── pages/
│   ├── base_page.py          # Core Playwright wrapper
│   ├── home_page.py          # Search bar action logic
│   └── ...                   # Other Page Objects
├── tests/
│   ├── conftest.py           # Stealth engine & CLI flags (--fresh)
│   ├── test_ai_failure.py    # AI Failure Analysis Demo (intentional error)
│   └── test_search_add_to_cart.py # AI-driven E2E Test
├── utils/
│   ├── ai_test_generator.py  # Gemini LLM engine (Module 5)
│   ├── ai_failure_analyzer.py # AI Diagnostic engine (Module 6)
│   └── ...                   # Standard utilities
├── logs/
│   ├── meesho_automation.log  # Test execution logs
│   └── ai_failure_report.log  # AI-generated failure explanations
├── .env                      # API Keys (Gemini)
├── pytest.ini                # Execution configuration
└── requirements.txt          # AI & Playwright dependencies
```

## 🛠 Installation & Setup

1. **Clone the repository and enter the directory.**
2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # venv\Scripts\activate   # Windows
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

## 🕵️ Hybrid Stealth Execution (WAF Bypass)

To reliably bypass advanced bot-detection systems (like Akamai), this framework uses a **Hybrid Manual-Automation Flow**. This ensures the browser profile is "warmed up" by a real human before the automation takes over.

### Pre-requisite: Manual Browser Launch
You must launch a instance of Google Chrome with Remote Debugging enabled **before** running the tests:

1. **Close all existing Chrome windows.**
2. **Run the following command in your terminal:**
   ```bash
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir=chrome-debug
   ```
3. **Human Warm-up:** 
   - Once Chrome opens, navigate to `https://www.meesho.com` manually.
   - Perform a quick search or browse for 10-15 seconds like a normal user.
   - This "proves" to the website that a real human is using the session.

4. **Run Automation:** Leave this Chrome window open and run the test command (see below). The script will automatically connect to this "human-verified" session.

## 🏃 Running Tests

### Standard Execution (Reuse AI Data)
To run the automated search and "Add to Cart" flow using existing AI-generated products:
```bash
pytest tests/test_search_add_to_cart.py -v
```

### Fresh AI Data Generation
To force Gemini to generate a brand new set of test products before running the automation:
```bash
pytest tests/test_search_add_to_cart.py -v --fresh
```

### AI Failure Debugging (Example)
To see the **AI Analysis in action**, we've included a controlled failure test. This test deliberately looks for a non-existent element to trigger a crash, which then activates Gemini's root-cause explanation:
```bash
PYTHONPATH=. pytest tests/test_ai_failure.py -v -s
```
**Expected Outcome:** 
1. The test will FAIL.
2. In your terminal, look for the **`--- AI FAILURE ANALYSIS ---`** header.
3. Gemini will explain that you are on the "Meesho Homepage" but looking for a "Product-level button."

### Generating Reports
To generate a comprehensive HTML summary:
```bash
PYTHONPATH=. pytest tests/test_search_add_to_cart.py -v --html=report.html --self-contained-html
```

## 📊 Diagnostics and Observations

- **Authentication Logic**: The framework automatically detects if a user is logged in.
  - **Logged In**: Verifies product addition by checking cart increments.
  - **Guest**: Verifies that the login popup is triggered upon clicking "Add to Cart".
- **Anti-Bot Strategy**: Implements human-paced typing, randomized mouse movements, and heavy-duty stabilization waits to ensure reliable execution against WAF challenges.
- **Logs**: Detailed execution steps are printed to the console and can be directed to `logs/meesho_automation.log`.
