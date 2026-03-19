import pytest
import os
import time
from utils.env_manager import EnvironmentManager
from utils.logger import Logger

logger = Logger.get_logger()

def pytest_addoption(parser):
    """Register custom CLI flags for the framework."""
    parser.addoption("--fresh", action="store_true", help="Force regeneration of AI test data.")

@pytest.fixture(scope="session", autouse=True)
def load_env_config():
    """Reads configuration once for the session. Purging profiles is skipped for Real Chrome mode."""
    config_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml")
    if not os.path.exists(config_path):
        config_path = os.path.abspath(os.path.join(os.getcwd(), "config", "config.yaml"))
    EnvironmentManager.load_config(config_path)

@pytest.fixture(scope="session")
def setup_context(playwright):
    r"""
    Connect to a REAL Google Chrome instance running in Remote Debugging mode.
    This is the ultimate bypass for Akamai WAF as it uses your real human profile.
    
    PRE-REQUISITE:
    Run the following command in terminal before starting the test:
    /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir=chrome-debug
    """
    logger.info("Connecting to Real Google Chrome via CDP (Port 9222)...")
    
    try:
        # Use connect_over_cdp to attach to your real browser window
        browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
        
        # We use the default context of the real browser
        context = browser.contexts[0]
        
        # Ensure we have at least one page
        if not context.pages:
            context.new_page()
            
        yield context
        
        # Note: We do NOT close the real browser here. 
        # We just detach.
        logger.info("Detached from Real Google Chrome.")
        
    except Exception as e:
        logger.critical(f"Failed to connect to Debugging Chrome: {e}")
        logger.critical("DID YOU RUN THE CHROME COMMAND? -> /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222 --user-data-dir=chrome-debug")
        raise e

@pytest.fixture(scope="function")
def setup_driver_from_persistent(setup_context, request):
    """Function-scoped Page instance attached to the Real Chrome context with Stealth Injection."""
    # Close background tabs to keep session clean but preserved
    if len(setup_context.pages) > 1:
        for p in setup_context.pages[1:]:
            try: p.close()
            except: pass
    
    # Reuse the primary tab or create one if none exist
    page = setup_context.pages[0] if setup_context.pages else setup_context.new_page()
        
    # Stealth Injection: Mask automation flags at the core
    stealth_script = """
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    window.chrome = { runtime: {} };
    Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
    Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
    """
    page.add_init_script(stealth_script)
    
    page.set_default_timeout(60000)
    time.sleep(3) # Heavy stabilization for WAF
    
    if request.node:
        request.node.page = page
        
    yield page

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        test_instance = getattr(item, 'instance', None)
        page = getattr(test_instance, 'page', None)
        if page:
            os.makedirs("screenshots", exist_ok=True)
            try:
                page.screenshot(path=f"screenshots/fail_{item.name}.png")
                # Save DOM for extreme debugging
                with open(f"screenshots/fail_{item.name}.html", "w") as f:
                    f.write(page.content())
            except: pass
