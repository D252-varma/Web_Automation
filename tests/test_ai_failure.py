import pytest
from tests.base_test import BaseTest

class TestAIFailure(BaseTest):
    """Temporary test suite to verify Module 6 AI-Powered Failure Analysis."""

    def test_deliberate_failure(self):
        """
        This test is intentionally designed to FAIL by looking for a button that doesn't exist.
        The failure will trigger the conftest.py hook to call Gemini for a root cause analysis.
        """
        self.page.goto("https://www.meesho.com")
        
        # This element does not exist, so it will trigger the 'assert' failure
        error_msg = "Checking for a fake button to verify the AI Failure Analyzer integration."
        assert self.page.is_visible("text='NON_EXISTENT_AI_DEBUG_BUTTON'"), error_msg
