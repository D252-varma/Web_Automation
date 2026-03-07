import pytest
from playwright.sync_api import sync_playwright
import os
from datetime import datetime
from utils.env_manager import EnvironmentManager
from utils.logger import Logger

logger = Logger.get_logger()

# Load environment configuration once before any tests run
@pytest.fixture(scope="session", autouse=True)
def load_env_config():
    """Reads configuration based on environment before test session starts."""
    config_path = os.path.join(os.path.dirname(__file__), "config", "config.yaml")
    # If conftest is at the root, config/config.yaml is straightforward.
    if not os.path.exists(config_path):
        # Fallback if tests are run from a different CWD
        config_path = os.path.abspath(os.path.join(os.getcwd(), "config", "config.yaml"))
    
    EnvironmentManager.load_config(config_path)
    logger.info(f"Loaded configuration for environment: {EnvironmentManager._env}")

@pytest.fixture(scope="function")
def setup_playwright():
    """Provide a Playwright page instance and handle trace/screenshot on failure."""
    headless = EnvironmentManager.is_headless()
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=headless)
        
        # Create a new browser context with tracing enabled
        context = browser.new_context()
        
        # Start tracing before creating the page (captures screenshots, snapshots, sources)
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        
        page = context.new_page()
        page.set_default_timeout(EnvironmentManager.get_timeout())
        
        yield page
        
        # Yield returns control to the test function. Once the test finishes, code below resumes.
        
        # Playwright's trace handling should usually be done via pytest hooks for pass/fail,
        # but here we can save a trace for every test run just in case, or only on failure if we use pytest hooks.
        # For simplicity in this fixture, we save the trace.
        
        os.makedirs("traces", exist_ok=True)
        trace_path = f"traces/trace_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        
        context.tracing.stop(path=trace_path)
        logger.info(f"Saved trace to {trace_path}")
        
        context.close()
        browser.close()

# Pytest Hook to take a screenshot specifically on test failure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture a screenshot when a test fails.
    Requires the 'page' fixture to be present in the test.
    """
    # Execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # We only care about actual test failures (not setup/teardown failures here)
    if rep.when == "call" and rep.failed:
        logger.error(f"Test failed: {item.name}")
        
        # Try to find the page fixture from the test item
        page = item.funcargs.get("setup_playwright", None)
        if page:
            os.makedirs("screenshots", exist_ok=True)
            screenshot_path = f"screenshots/fail_{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            try:
                page.screenshot(path=screenshot_path, full_page=True)
                logger.info(f"Saved screenshot on failure to {screenshot_path}")
            except Exception as e:
                logger.error(f"Failed to capture screenshot: {e}")
