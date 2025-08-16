"""
Comprehensive test suite for job match automation.
"""

import pytest
import asyncio
import os
import sys
import tempfile
import shutil
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import our modules
from core.config_manager import ConfigManager
from core.email_monitor import EmailMonitor
from core.job_scraper import JobScraper
from core.resume_parser import ResumeParser
from analysis.ai_analyzer import AIJobAnalyzer
from analysis.match_calculator import MatchCalculator
from analysis.rule_based_analyzer import RuleBasedAnalyzer
from analysis.job_match_analyzer import JobMatchAnalyzer
from notifications.discord_notifier import DiscordNotifier
from notifications.notification_manager import NotificationManager
from storage.application_tracker import ApplicationTracker
from storage.csv_exporter import CSVExporter
from storage.database import DatabaseManager


class TestConfigManager:
    """Tests for ConfigManager."""

    def test_init(self):
        """Test ConfigManager initialization."""
        # Create a temporary .env file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
            f.write("EMAIL_ADDRESS=test@example.com\n")
            f.write("EMAIL_PASSWORD=password123\n")
            f.write("OPENROUTER_API_KEY=testkey\n")
            env_file = f.name
        
        try:
            config = ConfigManager(env_file)
            assert config.email_address == "test@example.com"
            assert config.email_password == "password123"
            assert config.openrouter_api_key == "testkey"
        finally:
            os.unlink(env_file)

    def test_encryption(self):
        """Test encryption/decryption functionality."""
        config = ConfigManager()
        test_value = "secret_value"
        encrypted = config.encrypt_value(test_value)
        decrypted = config.decrypt_value(encrypted)
        assert decrypted == test_value


class TestEmailMonitor:
    """Tests for EmailMonitor."""

    def test_init(self):
        """Test EmailMonitor initialization."""
        with patch('core.config_manager.config') as mock_config:
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
        assert monitor._is_job_link('https://linkedin.com/jobs/view/12345', 'jobs-noreply@linkedin.com')
        assert monitor._is_job_link('https://indeed.com/viewjob?jk=abc123', 'noreply@indeed.com')
        assert not monitor._is_job_link('https://example.com/about', 'noreply@example.com')


class TestJobScraper:
    """Tests for JobScraper."""

    def test_init(self):
        """Test JobScraper initialization."""
        scraper = JobScraper()
        assert scraper is not None
        assert scraper.session is None

    def test_extract_experience_years(self):
        """Test experience years extraction."""
        scraper = JobScraper()
        assert scraper._extract_experience_years("3+ years of experience") == 3
        assert scraper._extract_experience_years("minimum 2 years experience") == 2
        assert scraper._extract_experience_years("at least 5 years of professional experience") == 5


class TestResumeParser:
    """Tests for ResumeParser."""

    def test_init(self):
        """Test ResumeParser initialization."""
        parser = ResumeParser()
        assert parser is not None

    def test_extract_skills(self):
        """Test skills extraction."""
        parser = ResumeParser()
        content = "Skills: Python, JavaScript, React, Node.js"
        skills = parser._extract_skills(content)
        assert "Python" in skills
        assert "JavaScript" in skills
        assert "React" in skills


class TestMatchCalculator:
    """Tests for MatchCalculator."""

    def test_init(self):
        """Test MatchCalculator initialization."""
        calculator = MatchCalculator()
        assert calculator is not None

    def test_calculate_experience_score(self):
        """Test experience score calculation."""
        calculator = MatchCalculator()
        assert calculator._calculate_experience_score(3, 3) == 90
        assert calculator._calculate_experience_score(2, 3) == 75
        assert calculator._calculate_experience_score(0, 3) == 30

    def test_determine_recommendation(self):
        """Test recommendation determination."""
        calculator = MatchCalculator()
        assert calculator._determine_recommendation(85) == "STRONG_MATCH"
        assert calculator._determine_recommendation(70) == "POSSIBLE_MATCH"
        assert calculator._determine_recommendation(50) == "REACH"
        assert calculator._determine_recommendation(20) == "SKIP"


class TestRuleBasedAnalyzer:
    """Tests for RuleBasedAnalyzer."""

    def test_init(self):
        """Test RuleBasedAnalyzer initialization."""
        analyzer = RuleBasedAnalyzer()
        assert analyzer is not None
        assert analyzer.match_calculator is not None


class TestApplicationTracker:
    """Tests for ApplicationTracker."""

    def test_init(self):
        """Test ApplicationTracker initialization."""
        tracker = ApplicationTracker()
        assert tracker is not None
        assert tracker.db is not None


class TestCSVExporter:
    """Tests for CSVExporter."""

    def test_init(self):
        """Test CSVExporter initialization."""
        exporter = CSVExporter()
        assert exporter is not None
        assert exporter.db is not None


class TestDatabaseManager:
    """Tests for DatabaseManager."""

    def test_init(self):
        """Test DatabaseManager initialization."""
        # Create a temporary database file
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test.db")
        
        try:
            with patch('core.config_manager.config') as mock_config:
                mock_config.database_path = db_path
                db = DatabaseManager()
                assert db is not None
                assert os.path.exists(temp_dir)
        finally:
            shutil.rmtree(temp_dir)


class TestIntegration:
    """Integration tests."""

    def test_config_to_email_monitor(self):
        """Test integration from config to email monitor."""
        with patch('core.config_manager.config') as mock_config:
            mock_config.email_address = 'test@example.com'
            mock_config.email_password = 'password'
            mock_config.email_imap_server = 'imap.example.com'
            mock_config.email_imap_port = 993
            
            monitor = EmailMonitor()
            assert monitor.email_address == 'test@example.com'

    def test_resume_to_match_calculation(self):
        """Test integration from resume parsing to match calculation."""
        # Create a sample resume
        sample_resume = """John Doe
        New York, NY
        Skills: Python, JavaScript, React
        
        Experience:
        Software Developer, TechCorp (2022-Present)
        """
        
        # Write to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(sample_resume)
            resume_path = f.name
        
        try:
            # Parse resume
            parser = ResumeParser()
            resume_data = parser.parse(resume_path)
            
            # Calculate match
            calculator = MatchCalculator()
            job_data = {
                "experience_years": 2,
                "requirements": "Python, React",
                "location": "New York, NY",
                "remote_option": True
            }
            
            result = calculator.calculate_match(resume_data, job_data)
            assert "percentage" in result
            assert "recommendation" in result
        finally:
            os.unlink(resume_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])