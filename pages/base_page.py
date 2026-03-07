
from playwright.sync_api import Page
from utils.logger import Logger
from utils.wait_utils import WaitUtils

class BasePage:
    """BasePage to hold common Playwright wrapper methods for all Page Objects."""

    def __init__(self, page: Page):
        self.page = page
        self.logger = Logger.get_logger()
        self.wait = WaitUtils()

    def click(self, locator: str, timeout: int = 30000):
        """Wrapper for clicking an element with explicit wait."""
        self.logger.info(f"Clicking on locator: {locator}")
        self.wait.wait_for_element_visible(self.page, locator, timeout)
        self.page.locator(locator).click()

    def fill(self, locator: str, text: str, timeout: int = 30000):
        """Wrapper for filling an input field."""
        self.logger.info(f"Filling '{text}' into locator: {locator}")
        self.wait.wait_for_element_visible(self.page, locator, timeout)
        self.page.locator(locator).fill(text)

    def get_text(self, locator: str, timeout: int = 30000) -> str:
        """Wrapper for getting text content from an element."""
        self.logger.info(f"Getting text from locator: {locator}")
        self.wait.wait_for_element_visible(self.page, locator, timeout)
        text = self.page.locator(locator).text_content()
        self.logger.info(f"Found text: {text}")
        return str(text).strip() if text else ""

    def is_visible(self, locator: str, timeout: int = 5000) -> bool:
        """Wrapper to quickly check if an element is visible."""
        try:
            self.page.wait_for_selector(locator, state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def get_title(self) -> str:
        """Wrapper to get the page title."""
        title = self.page.title()
        self.logger.info(f"Page Title is: {title}")
        return title
