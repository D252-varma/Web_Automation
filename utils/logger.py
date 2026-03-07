import logging
import os
from datetime import datetime

class Logger:
    """Custom logging subsystem for structured execution tracing."""

    _logger = None

    @classmethod
    def get_logger(cls):
        if cls._logger is None:
            # Create logs directory if it doesn't exist
            if not os.path.exists("logs"):
                os.makedirs("logs")

            cls._logger = logging.getLogger("MeeshoAutomation")
            cls._logger.setLevel(logging.INFO)

            # Formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                datefmt='%Y-%m-%d %H:%M:%S'
            )

            # Console Handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            cls._logger.addHandler(console_handler)

            # File Handler
            log_file = f"logs/execution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            cls._logger.addHandler(file_handler)

        return cls._logger
