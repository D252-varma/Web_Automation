
from utils.env_manager import EnvironmentManager
from utils.logger import Logger

# Initialize the custom logger
logger = Logger.get_logger()

def test_module_2():
    logger.info("--- Starting Module 2 Utilities Test ---")
    
    # 1. Test Environment Manager
    logger.info("1. Testing Environment Manager loading config.yaml...")
    try:
        EnvironmentManager.load_config()
        base_url = EnvironmentManager.get_base_url()
        headless = EnvironmentManager.is_headless()
        timeout = EnvironmentManager.get_timeout()
        
        logger.info(f"Loaded Environment: {EnvironmentManager._env}")
        logger.info(f"Base URL: {base_url}")
        logger.info(f"Headless Mode: {headless}")
        logger.info(f"Timeout: {timeout}")
        logger.info("Environment Manager working successfully!\n")
    except Exception as e:
        logger.error(f"Environment Manager Failed: {e}")

if __name__ == "__main__":
    test_module_2()
