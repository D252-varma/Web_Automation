from pages.base_page import BasePage
from utils.wait_utils import WaitUtils
import time
import os

class HomePage(BasePage):
    """Page Object for Meesho Home Page."""

    # Locators
    # Target the main search container input specifically
    SEARCH_INPUT = "header input[placeholder*='Search' i], .search-input-elm, input[placeholder*='products' i]"
    SEARCH_ICON_MOBILE = "img[alt='Search'], .NavComposedstyled__IconSection-sc-qv8j9o-4 img"
    CLOSE_POPUP_BTN = ".close-btn-selector"
    
    def __init__(self, page):
        super().__init__(page)

    def close_signup_popup_if_present(self):
        """Action to close the 'Sign up now' popup if it randomly appears on the home screen."""
        self.logger.info("Checking for 'Sign up now' popup...")
        try:
            # Look for common markers of the signup modal
            popup_indicators = [
                "text='Sign up now'",
                "text='Sign Up to view your profile'",
                ".signup-modal"
            ]
            
            is_present = False
            for selector in popup_indicators:
                if self.page.locator(selector).first.is_visible(timeout=2000):
                    is_present = True
                    break
            
            if is_present:
                self.logger.info("Signup popup detected. Attempting to click close (X).")
                close_selectors = [
                    "button:has-text('✕')",
                    "span:has-text('✕')",
                    ".close-btn",
                    "svg[cursor='pointer']",
                    "img[alt='close']",
                    "div[class*='close']",
                    "button[class*='close']"
                ]
                for selector in close_selectors:
                    try:
                        close_btn = self.page.locator(selector).first
                        if close_btn.is_visible(timeout=500):
                            close_btn.click()
                            self.logger.info(f"Clicked close button with selector: {selector}")
                            time.sleep(1)
                            return
                    except: continue

            # Final dismiss: Click outside and press Escape
            self.page.mouse.click(10, 10) # Click top-left corner
            self.page.keyboard.press("Escape")
            time.sleep(0.5)


        except Exception as e:
            self.logger.warning(f"Error handling signup popup: {e}")

    def search_for_product(self, product_name: str):
        """Ultra-stealth search flow with anti-timeout resilience."""
        import random
        self.logger.info(f"HomePage: Initiating search for: {product_name}")
        
        # 1. Page Readiness & Human Discovery
        self.close_signup_popup_if_present()
        
        # Humanize: Scroll down and up to look like a 'browsing' user
        self.page.mouse.wheel(0, random.randint(200, 500))
        time.sleep(random.uniform(1.0, 1.5))
        self.page.mouse.move(random.randint(100, 800), random.randint(100, 800), steps=10)
        self.page.mouse.wheel(0, -random.randint(200, 500))
        time.sleep(random.uniform(0.5, 1.0))

        # 2. Main UI Interaction (No Direct URL jumps - Akamai blocks them)
        try:
            search_input_selector = "input[placeholder*='Search' i], .search-input-elm"
            search_box = self.page.locator(search_input_selector).first
            
            # Protocol: Human Jitter Focus
            box = search_box.bounding_box()
            if box:
                self.page.mouse.move(box['x'] + random.randint(10, 30), box['y'] + box['height']/2, steps=15)
                time.sleep(0.5)
            
            # Click specifically (Force to bypass overlay checks)
            search_box.click(force=True, delay=random.randint(100, 200)) 
            time.sleep(1.0)
            
            # CLEAR - Mac specific Meta+A
            self.page.keyboard.press("Meta+A")
            time.sleep(0.4)
            self.page.keyboard.press("Backspace")
            time.sleep(0.8)
            
            # Human-like typing (Slower and more varied)
            for char in product_name:
                self.page.keyboard.type(char, delay=random.randint(50, 150))
                if random.random() > 0.8: time.sleep(random.uniform(0.1, 0.3))
                
            time.sleep(random.uniform(1.0, 2.0))
            self.page.keyboard.press("Enter")
            self.logger.info(f"Search query '{product_name}' submitted via Keyboard interaction.")
            
        except Exception as e:
            self.logger.warning(f"UI Search interaction failed: {e}. Attempting one-page-reset and retry.")
            self.page.reload(wait_until="load")
            time.sleep(5)
            return self.search_for_product(product_name) # Recursive retry once

        # 3. Validation
        try:
            # Wait for results or 404
            self.page.wait_for_url("**/search?q=**", timeout=15000)
            
            # Check if we hit a 'Not Found' screen immediately
            body_text = self.page.locator("body").inner_text().lower()
            block_markers = ["couldn't find", "not found", "let's start over", "access denied"]
            if any(marker in body_text for marker in block_markers):
                self.logger.error("Search results returned 'Block/Not Found' markers. Attempting stealth refresh.")
                time.sleep(random.uniform(2, 4))
                self.page.reload(wait_until="load")
                time.sleep(random.uniform(5, 8))
            
            self.logger.info("Search results hydration in progress.")
        except:
            self.logger.warning("Search transition delayed.")
            
        # Mandatory stabilization for grid loading
        time.sleep(random.randint(7, 10)) 

    def verify_home_page_loaded(self) -> bool:
        """Verify the user is on the homepage with WAF-Block recovery."""
        self.logger.info("HomePage: Verifying page is loaded.")
        
        # 1. Proactive Block Check
        try:
            body_text = self.page.locator("body").inner_text().lower()
            if "access denied" in body_text:
                self.logger.warning("Home page blocked by Akamai. Attempting stealth refresh...")
                time.sleep(5)
                self.page.reload(wait_until="load")
                time.sleep(5)
        except: pass

        self.close_signup_popup_if_present()
        
        # 2. Humanization: Stabilization Scroll
        try:
            self.page.mouse.wheel(0, 300)
            time.sleep(1)
            self.page.mouse.wheel(0, -300)
            time.sleep(1)
        except: pass
        
        # 3. Target Verification
        try:
            search_input_selector = "input[placeholder*='Search' i], .search-input-elm"
            self.page.wait_for_selector(search_input_selector, state="visible", timeout=25000)
            return True
        except Exception as e:
            self.logger.error(f"Home page failed to stabilize: {e}")
            return False
