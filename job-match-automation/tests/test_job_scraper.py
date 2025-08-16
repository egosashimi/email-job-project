"""
Unit tests for the job scraper module.
"""

import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.job_scraper import JobScraper


class TestJobScraper:
    """Tests for the JobScraper class."""

    def test_init(self):
        """Test JobScraper initialization."""
        scraper = JobScraper()
        assert scraper.session is None

    def test_extract_experience_years(self):
        """Test experience years extraction."""
        scraper = JobScraper()
        
        # Test various formats
        assert scraper._extract_experience_years("3+ years of experience") == 3
        assert scraper._extract_experience_years("minimum 2 years experience") == 2
        assert scraper._extract_experience_years("at least 5 years of professional experience") == 5
        assert scraper._extract_experience_years("2 yr experience") == 2
        
        # Test no match
        assert scraper._extract_experience_years("experience preferred") is None
        assert scraper._extract_experience_years("entry level position") is None

    def test_parse_generic(self):
        """Test generic parsing."""
        scraper = JobScraper()
        
        html = """
        <html>
        <head><title>Software Engineer - Test Company</title></head>
        <body>
        <h1>Software Engineer</h1>
        <p>We are looking for a software engineer with 3+ years of experience.</p>
        <p>Responsibilities include coding and testing.</p>
        </body>
        </html>
        """
        
        result = scraper._parse_generic(html)
        assert "Software Engineer" in result['title']
        assert "3+" in result['description']
        assert result['experience_years'] == 3