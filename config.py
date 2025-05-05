import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # OpenAI settings
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    OPENAI_MAX_TOKENS = int(os.getenv('OPENAI_MAX_TOKENS', '1000'))
    OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))
    
    # Application settings
    SUPPORTED_LANGUAGES = ['python', 'java', 'c', 'cpp']
    MAX_QUESTION_LENGTH = 500
    MAX_RESPONSE_LENGTH = 2000
    
    # Logging settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Rate limiting settings
    RATE_LIMIT = os.getenv('RATE_LIMIT', '100 per day')
    
    @staticmethod
    def validate():
        """Validate configuration settings"""
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in environment variables")
        
        if Config.OPENAI_MAX_TOKENS < 100 or Config.OPENAI_MAX_TOKENS > 4000:
            raise ValueError("OPENAI_MAX_TOKENS must be between 100 and 4000")
        
        if Config.OPENAI_TEMPERATURE < 0 or Config.OPENAI_TEMPERATURE > 1:
            raise ValueError("OPENAI_TEMPERATURE must be between 0 and 1") 