
import pytest
from utils.logger import Logger
from utils.env_manager import EnvironmentManager

@pytest.mark.usefixtures("setup_playwright")
class BaseTest:
    """
    BaseTest class that all test classes inherit from.
    Provides shared setup, logging, and environment specifics.
    """

    @pytest.fixture(autouse=True)
    def class_setup(self, setup_playwright):
        """
        Setup method run before every test method.
        Receives the 'setup_playwright' fixture from conftest.py.
        """
        self.page = setup_playwright
        self.logger = Logger.get_logger()
        self.base_url = EnvironmentManager.get_base_url()

        self.logger.info(f"Starting test. Navigating to base URL: {self.base_url}")
        self.page.goto(self.base_url)
        
        # We can also yield to handle teardown specific to tests, but the fixture
        # in conftest handles the browser contexts/pages.
