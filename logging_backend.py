import logging
from datetime import datetime
import os
import json

# Create logs directory
os.makedirs('logs', exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/prompt_response_log_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()  # This will also print to console
    ]
)

logger = logging.getLogger(__name__)

def log_interaction(prompt, response):
    """
    Log the prompt and response to file and console
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "response": response
    }
    
    logger.info(f"PROMPT: {prompt}")
    logger.info(f"RESPONSE: {response}")
    logger.info("-" * 80)  # Separator
    
    # Also save as JSON for easier parsing later
    with open(f'logs/interactions_{datetime.now().strftime("%Y%m%d")}.jsonl', 'a') as f:
        f.write(json.dumps(log_entry) + '\n')