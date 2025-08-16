"""
Unit tests for the resume parser module.
"""

import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.resume_parser import ResumeParser


class TestResumeParser:
    """Tests for the ResumeParser class."""

    def test_init(self):
        """Test ResumeParser initialization."""
        parser = ResumeParser()
        assert parser is not None

    def test_extract_experience_years(self):
        """Test experience years extraction."""
        parser = ResumeParser()
        
        # Test various formats
        content = "I have 3+ years of experience"
        assert parser._extract_experience_years(content) == 3
        
        content = "Minimum 2 years of professional experience required"
        assert parser._extract_experience_years(content) == 2
        
        content = "At least 5 years of experience"
        assert parser._extract_experience_years(content) == 5
        
        # Test no match
        content = "Experience preferred"
        result = parser._extract_experience_years(content)
        # Could be None or calculated from history
        assert result is None or isinstance(result, int)

    def test_extract_skills(self):
        """Test skills extraction."""
        parser = ResumeParser()
        
        # Test skills section extraction
        content = """
        SKILLS
        Python, JavaScript, React, Node.js
        """
        skills = parser._extract_skills(content)
        assert "Python" in skills
        assert "JavaScript" in skills
        assert "React" in skills
        assert "Node.js" in skills
        
        # Test keyword extraction
        content = "Experienced in Python and JavaScript development"
        skills = parser._extract_skills(content)
        assert "Python" in skills
        assert "JavaScript" in skills

    def test_extract_education(self):
        """Test education extraction."""
        parser = ResumeParser()
        
        # Test section extraction
        content = """
        EDUCATION
        Bachelor of Science in Computer Science
        University of New York, 2021
        """
        education = parser._extract_education(content)
        assert "Bachelor of Science in Computer Science" in education
        
        # Test degree pattern matching
        content = "I have a Bachelor's degree in Computer Science"
        education = parser._extract_education(content)
        assert "Bachelor" in education

    def test_extract_location(self):
        """Test location extraction."""
        parser = ResumeParser()
        
        # Test section extraction
        content = """
        CONTACT
        New York, NY
        john.doe@email.com
        """
        location = parser._extract_location(content)
        assert "New York, NY" == location
        
        # Test NYC matching
        content = "Based in NYC, looking for remote opportunities"
        location = parser._extract_location(content)
        assert "New York, NY" == location

    def test_extract_salary_expectations(self):
        """Test salary expectations extraction."""
        parser = ResumeParser()
        
        # Test range format
        content = "Salary expectations: $70,000 - $85,000"
        salary = parser._extract_salary_expectations(content)
        assert salary["min"] == 70000
        assert salary["ideal"] == 85000
        
        # Test single value
        content = "Looking for $75,000"
        salary = parser._extract_salary_expectations(content)
        assert salary["min"] == 75000
        assert salary["ideal"] == 90000  # With buffer

    def test_extract_section(self):
        """Test section extraction."""
        parser = ResumeParser()
        
        content = """
        SKILLS
        Python, JavaScript, React
        
        EXPERIENCE
        Software Developer, TechCorp
        """
        
        section = parser._extract_section(content, ['skills'])
        assert "Python, JavaScript, React" in section