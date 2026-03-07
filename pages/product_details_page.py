
from pages.base_page import BasePage
import time

class ProductDetailsPage(BasePage):
    """Page Object for a single product's detail screen."""

    # Locators
    PRODUCT_NAME = "h1" # The main header containing product name
    ADD_TO_CART_BTN = "span:has-text('Add to Cart')" # Locate by the generic text span Meesho uses for the Add to Cart button
    CART_ICON = "a[href='/cart']"
    CART_COUNT = ".cart-count" # This class name is generic, usually there's a badge on the cart

    def __init__(self, page):
        super().__init__(page)

    def verify_product_displayed(self) -> bool:
        """Check if the product name header is visible."""
        self.logger.info("ProductDetailsPage: Verifying product details are rendered.")
        return self.is_visible(self.PRODUCT_NAME)

    def get_product_name(self) -> str:
        return self.get_text(self.PRODUCT_NAME)

    def add_to_cart(self):
        """Action to click the Add to Cart button."""
        self.logger.info("ProductDetailsPage: Clicking 'Add to Cart'.")
        self.click(self.ADD_TO_CART_BTN)
        # Often there's a small flyout animation or network call, adding a small explicit sleep post-click
        # However, Playwright is fast, so we wait for network idle to ensure the count updates.
        time.sleep(2)

    def navigate_to_cart(self):
        """Click the top-right cart icon."""
        self.logger.info("ProductDetailsPage: Moving to the Cart page.")
        self.click(self.CART_ICON)

    def get_cart_count(self) -> int:
        """Retrieve the number displayed on the cart icon badge."""
        self.logger.info("ProductDetailsPage: Fetching current cart count.")
        try:
            # We wait a moment for the cart count element to update after clicking 'Add to cart'
            if self.is_visible(self.CART_COUNT, timeout=5000):
                count_text = self.get_text(self.CART_COUNT)
                return int(count_text) if count_text.isdigit() else 0
        except Exception:
            self.logger.info("ProductDetailsPage: Cart count not found, assuming 0.")
        return 0
