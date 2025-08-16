"""
Unit tests for the email monitor module.
"""

import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.email_monitor import EmailMonitor


class TestEmailMonitor:
    """Tests for the EmailMonitor class."""

    def test_init(self):
        """Test EmailMonitor initialization."""
        # Mock the config directly
        from core import config_manager
        original_config = config_manager.config
        
        # Create a mock config
        mock_config = Mock()
        mock_config.email_address = 'test@example.com'
        mock_config.email_password = 'password'
        mock_config.email_imap_server = 'imap.example.com'
        mock_config.email_imap_port = 993
        
        # Replace the config in the module
        config_manager.config = mock_config
        
        # Now create the EmailMonitor
        monitor = EmailMonitor()
        
        # Restore the original config
        config_manager.config = original_config
        
        assert monitor.email_address == 'test@example.com'
        assert monitor.email_password == 'password'
        assert monitor.imap_server == 'imap.example.com'
        assert monitor.imap_port == 993

    def test_is_job_link(self):
        """Test job link detection."""
        # Mock the config for initialization
        from core import config_manager
        original_config = config_manager.config
        config_manager.config = Mock()
        
        monitor = EmailMonitor()
        
        # Restore the original config
        config_manager.config = original_config
        
        # Test positive cases
        assert monitor._is_job_link('https://linkedin.com/jobs/view/12345', 'jobs-noreply@linkedin.com')
        assert monitor._is_job_link('https://indeed.com/viewjob?jk=abc123', 'noreply@indeed.com')
        
        # Test negative cases
        assert not monitor._is_job_link('https://example.com/about', 'noreply@example.com')
        assert not monitor._is_job_link('https://linkedin.com/profile/view', 'jobs-noreply@linkedin.com')