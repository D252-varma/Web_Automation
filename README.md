# Meesho Web Automation Framework

A robust, enterprise-grade web automation framework built with Python and Playwright for automating End-to-End ecommerce flows on Meesho.com. This framework is designed with production-ready patterns, focusing on stability, anti-bot evasion, and data-driven scalability.

## 🚀 Key Features

- **Playwright & Pytest**: High-performance cross-browser automation with native wait-for-load capabilities.
- **Page Object Model (POM)**: Clean separation of UI elements (locators) and business logic (actions) for high maintainability.
- **Data-Driven Testing (DDT)**: Dynamically executes search and checkout scenarios using external `JSON` data sources.
- **Advanced Stealth Engine**: Custom implementation for masking automation markers and mimicking human browser behavior to bypass sophisticated WAF/Bot detection.
- **Environment Agnostic**: Flexible configuration for `dev`, `qa`, and `prod` environments via `config.yaml`.
- **Rich Diagnostic Reporting**: Automatic generation of:
  - **HTML Execution Reports**: Comprehensive test summaries with timestamps.
  - **Trace Files**: Deep debugging with Playwright's trace viewer.
  - **Visual Evidence**: Screenshots captured automatically on test failures.

## 📁 Project Structure

```text
Meesho_Automation/
├── config/
│   └── config.yaml           # Environment variables (URLs, Timeouts)
├── data/
│   └── search_products.json  # Search keywords for Data-Driven tests
├── pages/
│   ├── base_page.py          # Core wrapper for basic Playwright actions
│   ├── home_page.py          # Home view interactions
│   ├── search_results_page.py # Result grid handling
│   └── product_details_page.py # PDP validation and cart actions
├── tests/
│   ├── base_test.py          # Project-level pytest fixtures
│   ├── conftest.py           # Stealth injection and hook implementations
│   └── test_search_add_to_cart.py # Core E2E Test Scenarios
├── utils/
│   ├── env_manager.py        # Config loader logic
│   ├── logger.py             # Standardized execution logging
│   ├── data_loader.py        # JSON/YAML data parser
│   └── wait_utils.py         # Performance-optimized wait strategies
├── pytest.ini                # Test runner configuration
└── requirements.txt          # Project dependencies
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

## 🏃 Running Tests

### Standard Execution
To run the automated search and "Add to Cart" flow:
```bash
pytest tests/test_search_add_to_cart.py -v
```

### Generating Reports
To generate a detailed HTML report:
```bash
pytest tests/test_search_add_to_cart.py --html=report.html --self-contained-html
```

## 📊 Diagnostics and Observations

- **Authentication Logic**: The framework automatically detects if a user is logged in.
  - **Logged In**: Verifies product addition by checking cart increments.
  - **Guest**: Verifies that the login popup is triggered upon clicking "Add to Cart".
- **Anti-Bot Strategy**: Implements human-paced typing, randomized mouse movements, and heavy-duty stabilization waits to ensure reliable execution against WAF challenges.
- **Logs**: Detailed execution steps are printed to the console and can be directed to `logs/meesho_automation.log`.
