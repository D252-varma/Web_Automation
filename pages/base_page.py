import time
from utils.logger import Logger
from utils.wait_utils import WaitUtils
from playwright.sync_api import Page

class BasePage:
    """BasePage to hold common Playwright wrapper methods for all Page Objects."""

    def __init__(self, page: Page):
        self.page = page
        self.logger = Logger.get_logger()
        self.wait_utils = WaitUtils()

    def click(self, locator: str, timeout: int = 30000):
        """Wrapper for clicking an element with explicit wait."""
        self.logger.info(f"Clicking on locator: {locator}")
        self.wait_utils.wait_and_click(self.page, locator, timeout)

    def fill(self, locator: str, text: str, timeout: int = 30000):
        """Wrapper for filling an input field using human-like typing."""
        self.logger.info(f"Typing '{text}' into locator: {locator}")
        if self.wait_utils.wait_for_element_visible(self.page, locator, timeout):
            # Using type with a delay to mimic human speed
            import random
            self.page.locator(locator).click()
            self.page.locator(locator).type(text, delay=random.randint(50, 150))

    def get_text(self, locator: str, timeout: int = 30000) -> str:
        """Wrapper for getting text content from an element."""
        self.logger.info(f"Getting text from locator: {locator}")
        if self.wait_utils.wait_for_element_visible(self.page, locator, timeout):
            text = self.page.text_content(locator, timeout=timeout)
            self.logger.info(f"Found text: {text}")
            return str(text).strip() if text else ""
        return ""

    def is_visible(self, locator: str, timeout: int = 5000) -> bool:
        """Wrapper to quickly check if an element is visible."""
        return self.wait_utils.wait_for_element_visible(self.page, locator, timeout)

    def get_title(self) -> str:
        """Wrapper to get the page title."""
        title = self.page.title()
        self.logger.info(f"Page Title is: {title}")
        return title
