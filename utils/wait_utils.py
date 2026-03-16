from playwright.sync_api import Page, TimeoutError
from utils.logger import Logger

logger = Logger.get_logger()

class WaitUtils:
    """Custom explicit wait utilities for Playwright."""

    @staticmethod
    def is_waf_blocked(page: Page) -> bool:
        """
        Detect common Akamai/WAF block pages (Access Denied / challenge shell).
        """
        try:
            title = (page.title() or "").strip().lower()
        except Exception:
            title = ""

        try:
            content = (page.content() or "").lower()
        except Exception:
            content = ""

        if "access denied" in title:
            return True
        if "<h1>access denied</h1>" in content or "you don't have permission to access" in content:
            return True
        # Akamai behavioral challenge container present in repo debug artifacts.
        if "sec-if-cpt-container" in content or "akamai" in content and "protected by" in content:
            return True
        return False

    @staticmethod
    def assert_not_waf_blocked(page: Page, context: str = ""):
        if WaitUtils.is_waf_blocked(page):
            extra = f" ({context})" if context else ""
            raise AssertionError(
                "Blocked by WAF/Akamai (Access Denied / challenge)."
                f"{extra} Current URL: {page.url}"
            )

    @staticmethod
    def wait_for_element_visible(page: Page, locator_string: str, timeout: int = 30000):
        """Wait explicitly for an element to be visible on the page."""
        try:
            logger.info(f"Waiting for element to be visible: {locator_string}")
            page.wait_for_selector(locator_string, state="visible", timeout=timeout)
            return True
        except TimeoutError:
            logger.error(f"Timeout waiting for element to be visible: {locator_string}")
            return False
        except Exception as e:
            logger.error(f"Error waiting for element: {locator_string}. Error: {e}")
            return False

    @staticmethod
    def wait_for_url_contains(page: Page, url_part: str, timeout: int = 30000):
        """Wait for the URL to contain a specific string."""
        try:
            logger.info(f"Waiting for URL to contain: '{url_part}'")
            # playwright expects glob or regex for url wait, or a function
            page.wait_for_url(f"**/*{url_part}*", timeout=timeout)
            return True
        except TimeoutError:
            logger.error(f"Timeout waiting for URL to contain '{url_part}'. current URL: {page.url}")
            return False
        except Exception as e:
            logger.error(f"Error waiting for URL: Error: {e}")
            return False

    @staticmethod
    def wait_and_click(page: Page, locator_string: str, timeout: int = 30000):
        """Wait for element to be visible and clickable, then click it."""
        try:
            logger.info(f"Waiting for element to be clickable: {locator_string}")
            page.wait_for_selector(locator_string, state="visible", timeout=timeout)
            page.click(locator_string, timeout=timeout)
            return True
        except Exception as e:
            logger.error(f"Failed to click element: {locator_string}. Error: {e}")
            return False
