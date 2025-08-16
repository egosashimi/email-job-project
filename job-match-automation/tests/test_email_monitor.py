"""
Unit tests for the email monitor module.
"""

import pytest
from unittest.mock import Mock, patch
from src.core.email_monitor import EmailMonitor


class TestEmailMonitor:
    """Tests for the EmailMonitor class."""

    def test_init(self):
        """Test EmailMonitor initialization."""
        with patch('src.core.config_manager.config') as mock_config:
            mock_config.email_address = 'test@example.com'
            mock_config.email_password = 'password'
            mock_config.email_imap_server = 'imap.example.com'
            mock_config.email_imap_port = 993
            
            monitor = EmailMonitor()
            
            assert monitor.email_address == 'test@example.com'
            assert monitor.email_password == 'password'
            assert monitor.imap_server == 'imap.example.com'
            assert monitor.imap_port == 993

    def test_is_job_link(self):
        """Test job link detection."""
        monitor = EmailMonitor()
        
        # Test positive cases
        assert monitor._is_job_link('https://linkedin.com/jobs/view/12345', 'jobs-noreply@linkedin.com')
        assert monitor._is_job_link('https://indeed.com/viewjob?jk=abc123', 'noreply@indeed.com')
        
        # Test negative cases
        assert not monitor._is_job_link('https://example.com/about', 'noreply@example.com')
        assert not monitor._is_job_link('https://linkedin.com/profile/view', 'jobs-noreply@linkedin.com')