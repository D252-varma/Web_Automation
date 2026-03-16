import time
from pages.base_page import BasePage

class ProductDetailsPage(BasePage):
    """Page Object for a single product's detail screen."""

    # Locators
    PRODUCT_NAME = "h1" 
    ADD_TO_CART_BTN = "button:has-text('Add to Cart')"
    CART_ICON = "img[alt='Cart']"
    CART_COUNT = "span[class*='CartBadge']"
    APP_PROMO_CLOSE = "img[alt='close']"
    
    # Generic size locators for mobile/desktop
    SIZE_CHIPS = "span[class*='SingleChip'], span[class*='SizeSelectionstyled__SizeChip']"
    SIZE_HEADER = "h6:has-text('Select Size')"

    def __init__(self, page):
        super().__init__(page)

    def verify_product_displayed(self) -> bool:
        """Strict verification with anti-WAF and Soft-Block detection."""
        import random
        self.logger.info("ProductDetailsPage: Waiting for product hydration...")
        
        # Humanize: Random browsing behavior to trigger hydration
        self.page.mouse.wheel(0, random.randint(200, 400))
        time.sleep(random.uniform(2.0, 4.0)) # Stable reflection
        
        try:
            # Detect 'Soft Blocks' or 404s
            body_text = self.page.locator("body").inner_text().lower()
            block_markers = ["access denied", "forbidden", "akamai", "couldn't find", "not found", "let's start over"]
            
            if any(marker in body_text for marker in block_markers):
                self.logger.warning(f"Stealth block marker detected in body. Attempting one-time recovery refresh.")
                time.sleep(random.uniform(4, 7))
                self.page.reload(wait_until="load")
                time.sleep(random.uniform(5, 8))

            # Wait for the main product signal with heavy patience
            self.page.wait_for_selector("h1", timeout=30000)
            h1_locator = self.page.locator("h1").first
            h1_text = h1_locator.inner_text().lower()
            
            # Guard against block persistence
            if any(marker in h1_text for marker in ["access denied", "forbidden"]):
                self.logger.error(f"Persistent Akamai block: {h1_text}")
                return False
                
            # Random Human Reflection Pause
            time.sleep(random.uniform(3, 5))
            
            # Final proof: 'Add to Cart' button presence
            if self.page.locator(self.ADD_TO_CART_BTN).count() > 0:
                self.logger.info(f"Legitimate PDP confirmed: {h1_text}")
                return True
            else:
                self.logger.warning("Content loaded but 'Add to Cart' button is missing. Possible out-of-stock.")
        except Exception as e:
            self.logger.warning(f"PDP hydration failed or timed out: {e}")
            
        return False

    def get_product_name(self) -> str:
        return self.get_text(self.PRODUCT_NAME)

    def select_size_if_available(self):
        """Action to select a size (e.g. shoes, kurtis) if the option presents itself."""
        self.logger.info("Checking if size selection is required.")
        try:
            # Short wait to see if size chips hydrate
            try:
                self.page.wait_for_selector(self.SIZE_CHIPS, state="visible", timeout=3000)
            except:
                pass 

            chips = self.page.locator(self.SIZE_CHIPS)
            count = chips.count()
            if count > 0:
                self.logger.info(f"Found {count} Size chips. Searching for an available variant.")
                for i in range(count):
                    chip = chips.nth(i)
                    outer_html = chip.evaluate("el => el.outerHTML") or ""
                    
                    # 'greyT3Divider' and 'eRPXHK' etc are classes for disabled/out-of-stock chips
                    is_disabled = "greyT3Divider" in outer_html or "eRPXHK" in outer_html or "disabled" in outer_html
                    if is_disabled:
                        continue 
                        
                    self.logger.info(f"Clicking available size chip: {chip.text_content()}")
                    chip.scroll_into_view_if_needed()
                    time.sleep(1)
                    chip.click()
                    time.sleep(1)
                    return # Mission accomplished
                    
                self.logger.info("Checked all sizes but none are available. Proceeding anyway.")
            else:
                self.logger.info("No size selection detected.")
        except Exception as e:
            self.logger.warning(f"Error in size selection: {e}")

    def add_to_cart(self):
        """Action to click 'Add to Cart', including a natural 'Human Jiggle' scroll."""
        self.logger.info("ProductDetailsPage: Attempting 'Add to Cart'.")
        
        # 1. Close any overlay if it appears
        try:
            promo_close = self.page.locator(self.APP_PROMO_CLOSE).last
            if promo_close.is_visible(timeout=1000):
                promo_close.click()
        except: pass

        # 2. Human Jiggle Scroll to prove humanity to Akamai
        self.logger.info("Executing 'Human Jiggle' scroll.")
        self.page.mouse.wheel(0, 300)
        time.sleep(1)
        self.page.mouse.wheel(0, -100)
        time.sleep(1)

        try:
            btn = self.page.locator(self.ADD_TO_CART_BTN).first
            btn.scroll_into_view_if_needed()
            time.sleep(1)
            btn.click(delay=150) # Slow click
            self.logger.info("Click submitted. Waiting for login modal.")
            time.sleep(3)
        except Exception as e:
            self.logger.warning(f"Standard click failed: {e}. Trying force click.")
            self.page.click(self.ADD_TO_CART_BTN, force=True, delay=200)

    def verify_login_modal_present(self) -> bool:
        """Professional check to see if the post-AddToCart login modal appeared."""
        self.logger.info("Verifying Login Modal presence.")
        
        login_markers = [
            "text='Log In to view your profile'",
            "text='Enter Phone Number'",
            "button:has-text('Continue')",
            ".login-modal",
            "img[alt='meesho_logo']"
        ]
        
        for marker in login_markers:
            try:
                if self.page.locator(marker).first.is_visible(timeout=5000):
                    self.logger.info(f"Verified Login Modal via marker: {marker}")
                    return True
            except:
                continue
                
        self.logger.error("Login Modal NOT detected after Add to Cart.")
        return False

    def navigate_to_cart(self):
        """Click the top-right cart icon."""
        self.logger.info("ProductDetailsPage: Moving to the Cart page.")
        self.click(self.CART_ICON)

    def verify_added_to_cart_success(self) -> bool:
        """Professional check for successful AddToCart when ALREADY logged in."""
        self.logger.info("Verifying product added to cart (Authenticated Flow).")
        
        success_markers = [
            "button:has-text('Go to Cart')",
            "text='Product added to the cart'",
            "span:has-text('View Cart')"
        ]
        
        for marker in success_markers:
            try:
                if self.page.locator(marker).first.is_visible(timeout=5000):
                    self.logger.info(f"Verified AddToCart success via marker: {marker}")
                    return True
            except:
                continue
        return False

    def get_cart_count(self) -> int:
        """Retrieve the number displayed on the cart icon badge."""
        self.logger.info("ProductDetailsPage: Fetching current cart count.")
        try:
            # Locator for the badge itself
            badge = self.page.locator(self.CART_COUNT).first
            if badge.is_visible(timeout=2000):
                text = badge.inner_text() or "0"
                digits = ''.join(filter(str.isdigit, text))
                return int(digits) if digits else 0
        except Exception as e:
            self.logger.warning(f"Failed to fetch cart count: {e}")
            
        return 0
