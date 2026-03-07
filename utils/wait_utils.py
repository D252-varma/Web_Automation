from playwright.sync_api import Page, expect
from utils.logger import Logger

logger = Logger.get_logger()

class WaitUtils:
    """Custom explicit wait utilities to supplement Playwright's auto-waits."""

    @staticmethod
    def wait_for_element_visible(page: Page, locator_string: str, timeout: int = 30000):
        """Wait explicitly for an element to be visible on the page."""
        try:
            logger.info(f"Waiting for element to be visible: {locator_string}")
            page.wait_for_selector(locator_string, state="visible", timeout=timeout)
            return True
        except Exception as e:
            logger.error(f"Timeout waiting for element to be visible: {locator_string}. Error: {e}")
            return False

    @staticmethod
    def wait_for_url_contains(page: Page, url_part: str, timeout: int = 30000):
        """Wait for the URL to contain a specific string."""
        try:
            logger.info(f"Waiting for URL to contain: '{url_part}'")
            page.wait_for_url(f"**/*{url_part}*", timeout=timeout)
            return True
        except Exception as e:
            logger.error(f"Timeout waiting for URL to contain '{url_part}'. current URL: {page.url}. Error: {e}")
            return False

    @staticmethod
    def wait_and_click(page: Page, locator_string: str, timeout: int = 30000):
        """Wait for element to be visible and click it."""
        if WaitUtils.wait_for_element_visible(page, locator_string, timeout):
            page.click(locator_string)
            return True
        return False
