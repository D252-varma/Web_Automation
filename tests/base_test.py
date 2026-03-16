import pytest
from utils.logger import Logger

class BaseTest:
    """
    BaseTest class. Manually manages a PERSISTENT branded Google Chrome instance.
    Focuses on launching a stable environment without premature navigation triggers.
    """

    @pytest.fixture(autouse=True)
    def class_setup(self, setup_driver_from_persistent):
        """
        Setup method explicitly leveraging Pytest Playwright plugin for isolated context.
        The 'setup_driver' fixture perfectly implements the 'browser -> context -> page' tear-up/down.
        """
        self.page = setup_driver_from_persistent
        self.logger = Logger.get_logger()
        self.logger.info("Initializing Pristine Pytest-Playwright Engine.")
