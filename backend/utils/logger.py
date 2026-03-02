import logging
import sys
from datetime import datetime

def setup_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

def log_request(endpoint: str, user_input: str = ""):
    """Log API requests"""
    logger.info(f"Request to {endpoint} - Input: {user_input[:50]}...")

def log_error(error: Exception, context: str = ""):
    """Log errors with context"""
    logger.error(f"Error in {context}: {str(error)}")

def log_api_call(service: str, status: str):
    """Log external API calls"""
    logger.info(f"{service} API call - Status: {status}")