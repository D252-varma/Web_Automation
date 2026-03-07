
from pages.base_page import BasePage

class HomePage(BasePage):
    """Page Object for Meesho Home Page."""

    # Locators
    # Note: Meesho's actual locators might vary, using robust strategies like CSS/XPath or Playwright test IDs.
    SEARCH_INPUT = "input[placeholder*='Search']"
    
    # We will assume clicking 'Enter' to search or clicking a search icon, but Playwright fill + press enter works fine.
    
    def __init__(self, page):
        super().__init__(page)

    def search_for_product(self, product_name: str):
        """Action to search for a product using the global search bar."""
        self.logger.info(f"HomePage: Searching for product: {product_name}")
        self.fill(self.SEARCH_INPUT, product_name)
        # Pressing Enter to initiate search
        self.page.locator(self.SEARCH_INPUT).press("Enter")
        # Explicit wait to ensure search results load
        self.page.wait_for_load_state("networkidle")

    def verify_home_page_loaded(self) -> bool:
        """Verify the user is on the homepage by checking the search bar visibility."""
        self.logger.info("HomePage: Verifying page is loaded.")
        return self.is_visible(self.SEARCH_INPUT)
