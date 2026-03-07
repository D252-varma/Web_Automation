
from pages.base_page import BasePage

class SearchResultsPage(BasePage):
    """Page Object for the Search Results grid."""

    # Locators
    # Assuming products are wrapped in some grid item container (e.g., div containing 'Product')
    # Or typically a generic div class that denotes a product card.
    PRODUCT_CARDS = "div[cursor='pointer']" 
    SEARCH_TITLE = "h1" # Typically where "Showing results for 'kurti'" is displayed.

    def __init__(self, page):
        super().__init__(page)

    def select_first_product(self):
        """Action to select the first product in the search results."""
        self.logger.info("SearchResultsPage: Selecting the first product from the grid.")
        # Grab the first match of the product cards
        first_product = self.page.locator(self.PRODUCT_CARDS).first
        first_product.click()
        self.page.wait_for_load_state("networkidle")
        
    def get_search_results_title(self) -> str:
        """Fetch the search title header usually stating 'Showing results for...'"""
        self.logger.info("SearchResultsPage: Fetching search results title text.")
        return self.get_text(self.SEARCH_TITLE)

    def are_products_displayed(self) -> bool:
        """Check if at least one product card is rendered."""
        count = self.page.locator(self.PRODUCT_CARDS).count()
        self.logger.info(f"SearchResultsPage: Found {count} products on screen.")
        return count > 0
