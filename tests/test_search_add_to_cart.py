import pytest
import time
from tests.base_test import BaseTest
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_details_page import ProductDetailsPage
from utils.data_loader import DataLoader
from utils.env_manager import EnvironmentManager

class TestSearchAddToCart(BaseTest):
    """
    Search and Add to Cart Test Suite.
    Optimized for 'Real Chrome' Debugging Mode.
    """

    @pytest.mark.parametrize("product_name", DataLoader.get_test_data("search_products.json")["products"])
    def test_search_and_add_to_cart(self, product_name):
        """Sequential Stealth Flow with Zero Hardcoding."""
        import random
        home_page = HomePage(self.page)
        search_results_page = SearchResultsPage(self.page)
        pdp = ProductDetailsPage(self.page) # Shared instance for scanners
    
        self.logger.info(f"--- Starting Stealth Sequence: {product_name} ---")
    
        # 1. Anti-Bot Cooldown & Tab Hygiene
        time.sleep(random.randint(20, 35))

        # Clear background tabs
        for p in self.page.context.pages:
            if p != self.page:
                try: p.close()
                except: pass

        # 2. Open Home via Config
        base_url = EnvironmentManager.get_base_url()
        current_url = self.page.url
        if not current_url or base_url not in current_url:
            self.logger.info(f"Navigating to Home: {base_url}")
            self.page.goto(base_url, wait_until="load", timeout=60000)
            time.sleep(3)
    
        # 3. Natural Search
        home_page.search_for_product(product_name)
    
        # 4. Humanized Product Selection
        search_results_page.click_product_by_index(0)
        
        # Professional Step: Adaptive Tab Discovery (Identifying PDP via POM pattern)
        target_page = self.page
        pdp_found = False
        
        self.logger.info("Scanning for valid Product Details Page...")
        for i in range(15):
            for p in self.page.context.pages:
                if "/p/" in p.url and "meesho.com" in p.url: # Standard structural checks
                    target_page = p
                    pdp_found = True
                    break
            if pdp_found: break
            time.sleep(1)

        # Re-attach PDP to the target page if it switched
        pdp = ProductDetailsPage(target_page)
        assert pdp.verify_product_displayed(), f"Failed to load PDP for {product_name}."
        
        initial_count = pdp.get_cart_count()
        pdp.select_size_if_available()
        time.sleep(2)
        pdp.add_to_cart()
        
        # 5. Dual-Outcome Verification
        if pdp.verify_login_modal_present():
             self.logger.info(f"SUCCESS (Guest): Login popup confirmed for {product_name}.")
        else:
            self.logger.info("Logged-in session detected. Verifying Cart Update.")
            is_ui_success = pdp.verify_added_to_cart_success()
            new_count = pdp.get_cart_count()
            assert is_ui_success or new_count > initial_count, f"Cart update failed for {product_name}."
            self.logger.info(f"SUCCESS (Auth): Product {product_name} added to cart.")

        if len(self.page.context.pages) > 1:
            target_page.close()

        self.logger.info(f"--- Finished Test: {product_name} ---")
