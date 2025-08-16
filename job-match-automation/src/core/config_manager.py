"""
Configuration management for the job match automation system.
Handles environment variables, encrypted credentials, and configuration validation.
"""

import os
from pathlib import Path
from typing import Optional
from cryptography.fernet import Fernet


class ConfigManager:
    """Manages application configuration from environment variables and encrypted files."""

    def __init__(self, env_file: Optional[str] = None):
        """Initialize configuration manager."""
        # Load environment variables from file if provided
        if env_file and os.path.exists(env_file):
            from dotenv import load_dotenv
            load_dotenv(env_file)
        
        # Load from system environment
        self._load_from_environment()
    
    def _load_from_environment(self):
        """Load configuration from environment variables."""
        self.email_address = os.getenv("EMAIL_ADDRESS")
        self.email_password = os.getenv("EMAIL_PASSWORD")
        self.email_imap_server = os.getenv("EMAIL_IMAP_SERVER", "imap.gmail.com")
        self.email_imap_port = int(os.getenv("EMAIL_IMAP_PORT", "993"))
        self.database_path = os.getenv("DATABASE_PATH", "data/jobs.db")
        self.discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        
        # Handle encryption key
        encryption_key = os.getenv("ENCRYPTION_KEY")
        if encryption_key:
            self.encryption_key = encryption_key.encode()
        else:
            # Generate a new key if none provided
            self.encryption_key = Fernet.generate_key()
        
        self.cipher_suite = Fernet(self.encryption_key)
    
    def validate(self) -> bool:
        """Validate that required configuration values are present."""
        required_vars = [
            self.email_address,
            self.email_password,
            self.openrouter_api_key
        ]
        return all(required_vars)
    
    def get_encryption_key(self) -> bytes:
        """Get the encryption key."""
        return self.encryption_key
    
    def encrypt_value(self, value: str) -> bytes:
        """Encrypt a value using the configured cipher."""
        return self.cipher_suite.encrypt(value.encode())
    
    def decrypt_value(self, encrypted_value: bytes) -> str:
        """Decrypt a value using the configured cipher."""
        return self.cipher_suite.decrypt(encrypted_value).decode()


# Global configuration instance
config = ConfigManager()