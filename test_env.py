from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Test environment variables
def test_env_vars():
    try:
        # Check OpenAI API key
        openai_key = os.getenv('OPENAI_API_KEY')
        if not openai_key:
            logger.error("❌ OPENAI_API_KEY not found in environment variables")
        else:
            logger.info("✅ OPENAI_API_KEY is set (first 8 chars: %s...)", openai_key[:8])

        # Check Secret Key
        secret_key = os.getenv('SECRET_KEY')
        if not secret_key:
            logger.error("❌ SECRET_KEY not found in environment variables")
        else:
            logger.info("✅ SECRET_KEY is set (first 8 chars: %s...)", secret_key[:8])

        # Check Rate Limit
        rate_limit = os.getenv('RATE_LIMIT')
        if not rate_limit:
            logger.error("❌ RATE_LIMIT not found in environment variables")
        else:
            logger.info("✅ RATE_LIMIT is set to: %s", rate_limit)

    except Exception as e:
        logger.error("❌ Error testing environment variables: %s", str(e))

if __name__ == "__main__":
    logger.info("Testing environment variables...")
    test_env_vars()