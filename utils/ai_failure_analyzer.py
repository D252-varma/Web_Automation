import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AIFailureAnalyzer")

class AIFailureAnalyzer:
    """
    AI-Powered Failure Analysis Utility.
    Analyzes HTML content from failed tests using Google Gemini to explain the root cause.
    """

    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            logger.error("GEMINI_API_KEY not found in .env.")
            return

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def analyze_failure(self, html_content: str, test_name: str, expected_behavior: str = "Successful product search and addition to cart"):
        """
        Sends failure data to Gemini for analysis.
        Saves resulting report to logs/ai_failure_report.txt.
        """
        if not html_content:
            logger.error("No HTML content provided for analysis.")
            return "No HTML content available."

        # Truncate HTML content if too large (token limits)
        # We focus on the body for relevance
        if len(html_content) > 30000:
            html_content = html_content[:30000] + "... [Truncated]"

        prompt = (
            "You are a Senior QA Automation Engineer and Playwright expert.\n"
            f"A test named '{test_name}' has failed on Meesho.com.\n\n"
            f"EXPECTED BEHAVIOR:\n{expected_behavior}\n\n"
            "HTML CONTENT SNAPSHOT OF FAILURE:\n"
            "-----------------------------------\n"
            f"{html_content}\n"
            "-----------------------------------\n\n"
            "TASK:\n"
            "1. Analyze the HTML content above.\n"
            "2. Identify if the page shows 'Access Denied', 'Something went wrong', a login popup, or a missing 'Add to Cart' button.\n"
            "3. Explain in plain English why the test most likely failed.\n"
            "4. Provide a structured reason and type if possible (e.g., UI_STATE_ISSUE, WAF_BLOCK, BOT_DETECTED).\n"
            "Return the analysis in a professional, concise format."
        )

        try:
            logger.info(f"AI: Analyzing failure for test: {test_name}...")
            response = self.model.generate_content(prompt)
            analysis_text = response.text.strip()

            # Ensure logs directory exists
            os.makedirs("logs", exist_ok=True)
            report_path = os.path.join("logs", "ai_failure_report.log") # Using .log for better highlighting
            
            with open(report_path, "a") as f:
                f.write(f"\n{'='*50}\n")
                f.write(f"FAILURE REPORT FOR: {test_name}\n")
                f.write(f"TIMESTAMP: {os.popen('date').read().strip()}\n")
                f.write(f"{'-'*50}\n")
                f.write(analysis_text)
                f.write(f"\n{'='*50}\n")
                
            logger.info("AI Analysis Complete. Report saved to logs/ai_failure_report.log")
            print(f"\n--- AI FAILURE ANALYSIS ---\n{analysis_text}\n---------------------------")
            
            return analysis_text

        except Exception as e:
            logger.error(f"AI Analysis Failed: {e}")
            return f"AI Analysis failed due to: {e}"

if __name__ == "__main__":
    # Quick debug test
    analyzer = AIFailureAnalyzer()
    analyzer.analyze_failure("<html><body>Access Denied</body></html>", "Debug_Test")
