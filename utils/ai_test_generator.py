import os
import json
import logging
import google.generativeai as genai
from dotenv import load_dotenv

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AITestGenerator")

class AITestGenerator:
    """
    AI Test Case Generator Utility.
    Uses Google Gemini to dynamically generate structured test data for Meesho.
    """

    def __init__(self):
        # Load .env variables
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            logger.error("GEMINI_API_KEY not found in .env file.")
            raise ValueError("GEMINI_API_KEY is required.")
            
        # Configure Gemini
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def generate_test_data(self, count: int = 3):
        """
        Prompts Gemini to generate specific test cases for Meesho products.
        Saves the result to data/ai_test_data.json.
        """
        prompt = (
            f"Generate {count} realistic product search test cases for an e-commerce fashion website like Meesho. "
            "Return only valid JSON with the following structure: "
            "{ \"tests\": [ { \"product\": \"<product_name>\", \"test_type\": \"add_to_cart\" } ] }. "
            "Ensure the products are relevant to Meesho (e.g., Kurti, Saree, Watch, Shoes, T-shirt). "
            "Return ONLY the raw JSON string without any markdown formatting."
        )

        try:
            logger.info(f"AI: Requesting {count} test cases from Gemini...")
            response = self.model.generate_content(prompt)
            
            # Clean response text in case LLM adds markdown blocks
            raw_text = response.text.strip()
            if raw_text.startswith("```json"):
                raw_text = raw_text.replace("```json", "", 1).replace("```", "", 1).strip()
            elif raw_text.startswith("```"):
                raw_text = raw_text.replace("```", "", 1).replace("```", "", 1).strip()

            # Validate JSON
            test_data = json.loads(raw_text)
            
            # Ensure data directory exists
            data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
            os.makedirs(data_dir, exist_ok=True)
            
            output_path = os.path.join(data_dir, "ai_test_data.json")
            with open(output_path, "w") as f:
                json.dump(test_data, f, indent=2)
                
            logger.info(f"AI Success: Successfully saved generated test cases to {output_path}")
            return test_data

        except Exception as e:
            logger.error(f"AI Failure: Prompt execution failed. {e}")
            # Fallback data if AI fails
            fallback = {
                "tests": [
                    {"product": "kurti", "test_type": "add_to_cart"},
                    {"product": "shoes", "test_type": "add_to_cart"}
                ]
            }
            logger.info("Using fallback test data.")
            return fallback

if __name__ == "__main__":
    generator = AITestGenerator()
    generator.generate_test_data()
