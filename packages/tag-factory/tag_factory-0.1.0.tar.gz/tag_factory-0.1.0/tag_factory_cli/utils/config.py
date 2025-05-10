"""
Configuration utilities for Tag Factory CLI.
"""
import os


class Config:
    """Configuration handler for Tag Factory CLI using environment variables."""

    def __init__(self):
        """Initialize configuration handler using environment variables."""
        pass

    def get(self, key, default=None):
        """Get configuration value from environment variable.
        
        Args:
            key: Configuration key (will be converted to uppercase and prefixed with TAG_FACTORY_)
            default: Default value if environment variable not found
            
        Returns:
            Configuration value
        """
        env_key = f"TAG_FACTORY_{key.upper()}"
        return os.environ.get(env_key, default)

    def get_api_key(self):
        """Get API key from environment variable."""
        return os.environ.get("TAG_FACTORY_API_KEY")

    def get_api_url(self):
        """Get API URL from environment variable."""
        return os.environ.get("TAG_FACTORY_API_URL", "http://localhost:3000/api")
