import pytest
import time
import os
import random
from tests.base_test import BaseTest
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_details_page import ProductDetailsPage
from utils.data_loader import DataLoader
from utils.env_manager import EnvironmentManager
from utils.ai_test_generator import AITestGenerator

def get_parametrized_data():
    """
    Logic to load either AI-generated or fall-back static test data.
    Hybrid Mode: Regenerates data if --fresh flag is present or file is missing.
    """
    import sys
    ai_data_path = "ai_test_data.json"
    force_refresh = "--fresh" in sys.argv
    
    # Proactively check/generate AI data logic
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    full_path = os.path.join(data_dir, ai_data_path)
    
    should_generate = force_refresh or not os.path.exists(full_path)
    
    if should_generate:
        try:
            generator = AITestGenerator()
            generator.generate_test_data(count=3)
            # Re-verify existence after generation attempt
            if not os.path.exists(full_path):
                 raise FileNotFoundError("AI generation was attempted but file is still missing.")
        except Exception as e:
            # Fallback to search_products.json if AI engine fails
            return DataLoader.get_test_data("search_products.json")["products"]
            
    # Load the prioritized AI data
    try:
        data = DataLoader.get_test_data("ai_test_data.json")
        return [t["product"] for t in data["tests"]]
    except:
        return DataLoader.get_test_data("search_products.json")["products"]

class TestSearchAddToCart(BaseTest):
    """
    Search and Add to Cart Test Suite with AI-Driven Data.
    """

    # Load test logic dynamically
    @pytest.mark.parametrize("product_name", get_parametrized_data())
    def test_search_and_add_to_cart(self, product_name):
        """
        AI-Driven Flow:
        Executes the Add-To-Cart sequence using dynamic product data from Gemini.
        """
        # ModuleRequirement: Functional Flow separation
        # Since 'page' context is managed by BaseTest, we pass self.page
        self.run_add_to_cart_flow(self.page, product_name)

    def run_add_to_cart_flow(self, page, product):
        """
        Modular execution logic as requested by AI Architecture Plan.
        Handles: Navigate -> Search -> Open -> Select Size -> Add to Cart -> Validate.
        """
        home_page = HomePage(page)
        search_results_page = SearchResultsPage(page)
        pdp = ProductDetailsPage(page)
        
        self.logger.info(f"--- Processing Product: {product} ---")

        # 1. Humanized Start
        time.sleep(random.randint(15, 25)) # Reduced slightly for better runtime
        
        # 2. Open Home (Check navigation)
        base_url = EnvironmentManager.get_base_url()
        if base_url not in page.url:
            self.logger.info(f"Navigating to Home: {base_url}")
            page.goto(base_url, wait_until="load", timeout=60000)
            time.sleep(3)

        # 3. Search product
        home_page.search_for_product(product)

        # 4. Open first product
        search_results_page.click_product_by_index(0)
        
        # Discovery: Locate Active PDP tab/tab transition
        target_page = self.page
        pdp_found = False
        for i in range(15):
            for p in self.page.context.pages:
                if "/p/" in p.url and "meesho.com" in p.url:
                    target_page = p
                    pdp_found = True
                    break
            if pdp_found: break
            time.sleep(1)

        # 5. Core PDP Interaction Flow
        pdp = ProductDetailsPage(target_page)
        assert pdp.verify_product_displayed(), f"Failure: Product Details not found for {product}."
        
        initial_count = pdp.get_cart_count()
        pdp.select_size_if_available()
        time.sleep(2)
        pdp.add_to_cart()

        # 6. Dynamic Validation logic as per Module 5 requirements
        if pdp.verify_login_modal_present():
            self.logger.info(f"VERIFIED (Guest): Login popup successfully triggered for: {product}")
        else:
            self.logger.info("Auth session active. Verifying UI success markers.")
            is_success = pdp.verify_added_to_cart_success()
            curr_count = pdp.get_cart_count()
            self.logger.info(f"Cart Count transitioned from {initial_count} -> {curr_count}")
            assert is_success or curr_count > initial_count, f"Add to Cart failed for product: {product}"
            self.logger.info(f"VERIFIED (Auth): Cart count update verified for: {product}")

        # Cleanup
        if target_page != self.page:
            target_page.close()
            self.logger.info("Closed secondary product tab.")
        
        self.logger.info(f"--- Flow Complete: {product} ---")
