# logger.py - Logging system for the AI tutor

import logging
from datetime import datetime
import os

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging
log_filename = f"logs/tutor_{datetime.now().strftime('%Y%m%d')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()  # Also print to console
    ]
)

# Create logger
logger = logging.getLogger('AITutor')

# Convenience functions
def log_info(message):
    """Log an info message"""
    logger.info(message)

def log_error(message, error=None):
    """Log an error message"""
    if error:
        logger.error(f"{message}: {error}")
    else:
        logger.error(message)

def log_warning(message):
    """Log a warning message"""
    logger.warning(message)

def log_debug(message):
    """Log a debug message"""
    logger.debug(message)

def log_api_call(function_name, tokens_used, cost):
    """Log an API call"""
    logger.info(f"API Call - {function_name} | Tokens: {tokens_used} | Cost: ${cost:.6f}")

def log_student_action(action, details=""):
    """Log student actions"""
    logger.info(f"Student Action - {action} | {details}")

# Test logging
if __name__ == "__main__":
    log_info("Logger initialized")
    log_error("Test error", Exception("This is a test"))
    log_warning("Test warning")
    log_api_call("test_function", 100, 0.0002)
    log_student_action("Solved Problem", "Topic: loops, Correct: True")
    
    print(f"\n✓ Check the logs folder for: {log_filename}")