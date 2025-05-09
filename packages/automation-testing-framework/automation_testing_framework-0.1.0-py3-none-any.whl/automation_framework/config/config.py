import os
import logging
import tempfile
from pathlib import Path
try:
    from dotenv import load_dotenv
    # Load environment variables from .env file if available
    load_dotenv()
except ImportError:
    # dotenv is optional
    pass

# Setup logger
logger = logging.getLogger(__name__)

class Config:
    """Configuration class for the automation framework."""
    
    # Browser configurations
    BROWSER = os.getenv('BROWSER', 'chromium')
    HEADLESS = os.getenv('HEADLESS', 'true').lower() == 'true'
    SLOW_MO = int(os.getenv('SLOW_MO', '0'))  # Slow down execution for debugging
    
    # Application configurations
    BASE_URL = os.getenv('BASE_URL', 'https://example.com')
    
    # Timeouts
    DEFAULT_TIMEOUT = int(os.getenv('DEFAULT_TIMEOUT', '30000'))  # milliseconds
    
    # Test data
    TEST_DATA_PATH = os.getenv('TEST_DATA_PATH', os.path.join(tempfile.gettempdir(), 'automation_framework', 'data'))
    
    # Reporting
    REPORTS_BASE_PATH = os.getenv('REPORTS_PATH', os.path.join(tempfile.gettempdir(), 'automation_framework', 'reports'))
    SCREENSHOTS_PATH = os.path.join(REPORTS_BASE_PATH, 'screenshots')
    ALLURE_RESULTS_PATH = os.path.join(REPORTS_BASE_PATH, 'allure-results')
    
    # Database configurations
    # PostgreSQL
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', '5432'))
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'postgres')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
    
    # ClickHouse
    CLICKHOUSE_HOST = os.getenv('CLICKHOUSE_HOST', 'localhost')
    CLICKHOUSE_PORT = int(os.getenv('CLICKHOUSE_PORT', '8123'))
    CLICKHOUSE_DB = os.getenv('CLICKHOUSE_DB', 'default')
    CLICKHOUSE_USER = os.getenv('CLICKHOUSE_USER', 'default')
    CLICKHOUSE_PASSWORD = os.getenv('CLICKHOUSE_PASSWORD', '')
    
    # AWS Configuration
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
    AWS_SESSION_TOKEN = os.getenv('AWS_SESSION_TOKEN', '')
    AWS_ENDPOINT_URL = os.getenv('AWS_ENDPOINT_URL', '')
    
    @classmethod
    def setup(cls, base_url=None, timeout=None, postgres_config=None, clickhouse_config=None, aws_config=None):
        """
        Configure the framework programmatically.
        
        Args:
            base_url: Base URL for API requests
            timeout: Default timeout in milliseconds
            postgres_config: Dictionary with PostgreSQL configuration
            clickhouse_config: Dictionary with ClickHouse configuration
            aws_config: Dictionary with AWS configuration
        """
        if base_url:
            cls.BASE_URL = base_url
            
        if timeout:
            cls.DEFAULT_TIMEOUT = timeout
        
        if postgres_config:
            cls.POSTGRES_HOST = postgres_config.get('host', cls.POSTGRES_HOST)
            cls.POSTGRES_PORT = postgres_config.get('port', cls.POSTGRES_PORT)
            cls.POSTGRES_DB = postgres_config.get('db', cls.POSTGRES_DB)
            cls.POSTGRES_USER = postgres_config.get('user', cls.POSTGRES_USER)
            cls.POSTGRES_PASSWORD = postgres_config.get('password', cls.POSTGRES_PASSWORD)
        
        if clickhouse_config:
            cls.CLICKHOUSE_HOST = clickhouse_config.get('host', cls.CLICKHOUSE_HOST)
            cls.CLICKHOUSE_PORT = clickhouse_config.get('port', cls.CLICKHOUSE_PORT)
            cls.CLICKHOUSE_DB = clickhouse_config.get('db', cls.CLICKHOUSE_DB)
            cls.CLICKHOUSE_USER = clickhouse_config.get('user', cls.CLICKHOUSE_USER)
            cls.CLICKHOUSE_PASSWORD = clickhouse_config.get('password', cls.CLICKHOUSE_PASSWORD)
        
        if aws_config:
            cls.AWS_REGION = aws_config.get('region', cls.AWS_REGION)
            cls.AWS_ACCESS_KEY_ID = aws_config.get('access_key_id', cls.AWS_ACCESS_KEY_ID)
            cls.AWS_SECRET_ACCESS_KEY = aws_config.get('secret_access_key', cls.AWS_SECRET_ACCESS_KEY)
            cls.AWS_SESSION_TOKEN = aws_config.get('session_token', cls.AWS_SESSION_TOKEN)
            cls.AWS_ENDPOINT_URL = aws_config.get('endpoint_url', cls.AWS_ENDPOINT_URL)
        
        cls.create_directories()
        logger.info("Framework configuration updated")
    
    # Ensure directories exist
    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist."""
        try:
            os.makedirs(cls.SCREENSHOTS_PATH, exist_ok=True)
            os.makedirs(cls.ALLURE_RESULTS_PATH, exist_ok=True)
            os.makedirs(cls.TEST_DATA_PATH, exist_ok=True)
            logger.debug(f"Created directories: {cls.SCREENSHOTS_PATH}, {cls.ALLURE_RESULTS_PATH}, {cls.TEST_DATA_PATH}")
        except Exception as e:
            logger.warning(f"Failed to create directories: {str(e)}")

# Create directories at import time
Config.create_directories()
