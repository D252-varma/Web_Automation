import time
from pages.base_page import BasePage

class SearchResultsPage(BasePage):
    """Page Object for the Search Results grid."""

    # Locators
    PRODUCT_CARDS = "a[href*='/p/']" 
    SEARCH_TITLE = "h1"

    def __init__(self, page):
        super().__init__(page)

    def click_first_product(self):
        """Action to visually click the first product on the search results grid."""
        self.click_product_by_index(0)

    def click_product_by_index(self, index: int):
        """Clicks a product card with high-fidelity validation and retry."""
        import random
        self.logger.info(f"SearchResultsPage: Attempting stable click on product index: {index}.")
        
        # 1. Wait for stable grid hydration
        # Target the product item specifically to ensure we aren't clicking on skeletons
        grid_selector = "div[class*='ProductList'], [data-testid*='product-card'], a[href*='/p/']"
        try:
            self.page.wait_for_selector(grid_selector, timeout=12000)
            time.sleep(random.uniform(2, 4)) # Allow final hydration
        except:
            if self.page.locator(grid_selector).count() == 0:
                self.logger.error("No valid products detected after hydration wait.")
                return

        products = self.page.locator(grid_selector)
        count = products.count()
        self.logger.info(f"Available products for selection: {count}")
        
        target_index = min(index, count - 1)
        product = products.nth(target_index)
        
        # 2. Humanized Approach
        product.scroll_into_view_if_needed()
        time.sleep(random.uniform(0.8, 1.5))
        
        box = product.bounding_box()
        if box:
            self.page.mouse.move(box['x'] + box['width']/2, box['y'] + box['height']/2, steps=15)
            time.sleep(random.uniform(0.3, 0.6))

        # 3. High-Signal Click (attempts standard then JS)
        current_url = self.page.url
        try:
            # Try to find the <a> tag within or as the product
            link_locator = product.locator("xpath=.//ancestor-or-self::a[contains(@href, '/p/')]").first
            link_locator.click(timeout=3000, force=True)
            self.logger.info("Humanized link click dispatched.")
        except:
            self.logger.warning("Direct link click failed. Using generic product container click.")
            product.click(force=True, delay=random.randint(50, 200))

        # Small grace period for transition
        time.sleep(random.uniform(2, 4))
        if self.page.url == current_url:
            self.logger.warning("URL didn't change. Dispatching JS forced navigation as fallback.")
            try:
                href = product.get_attribute("href") or product.locator("a").first.get_attribute("href")
                if href:
                    if not href.startswith("http"):
                        href = "https://www.meesho.com" + href
                    self.page.evaluate(f"window.location.href = '{href}'")
            except: 
                # Last resort: click center again via JS
                product.evaluate("el => el.click()")
        
    def get_search_results_title(self) -> str:
        """Fetch the search title header usually stating 'Showing results for...'"""
        self.logger.info("SearchResultsPage: Fetching search results title text.")
        return self.get_text(self.SEARCH_TITLE)

    def are_products_displayed(self) -> bool:
        """Check if at least one product card is rendered."""
        # Wait a moment for rendering
        try:
            self.page.wait_for_selector(self.PRODUCT_CARDS, timeout=5000)
        except:
            pass
        count = self.page.locator(self.PRODUCT_CARDS).count()
        self.logger.info(f"SearchResultsPage: Found {count} products on screen.")
        return count > 0
