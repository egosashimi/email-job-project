"""
Unit tests for the match calculator module.
"""

import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from analysis.match_calculator import MatchCalculator


class TestMatchCalculator:
    """Tests for the MatchCalculator class."""

    def test_init(self):
        """Test MatchCalculator initialization."""
        calculator = MatchCalculator()
        assert calculator is not None

    def test_calculate_experience_score(self):
        """Test experience score calculation."""
        calculator = MatchCalculator()
        
        # Test exact match
        assert calculator._calculate_experience_score(3, 3) == 90
        
        # Test candidate exceeds requirement
        assert calculator._calculate_experience_score(5, 3) == 90
        
        # Test close match
        assert calculator._calculate_experience_score(2, 3) == 75
        assert calculator._calculate_experience_score(1, 3) == 60
        
        # Test distant match
        assert calculator._calculate_experience_score(0, 3) == 30
        
        # Test no requirement
        assert calculator._calculate_experience_score(2, 0) == 70

    def test_calculate_skills_score(self):
        """Test skills score calculation."""
        calculator = MatchCalculator()
        
        # Test perfect match
        resume_skills = ["Python", "Django", "React"]
        job_requirements = "Python, Django, React"
        score = calculator._calculate_skills_score(resume_skills, job_requirements)
        assert score >= 80  # High score for perfect match
        
        # Test partial match
        resume_skills = ["Python"]
        job_requirements = "Python, Django, React"
        score = calculator._calculate_skills_score(resume_skills, job_requirements)
        assert 40 <= score <= 80  # Medium score for partial match
        
        # Test no match
        resume_skills = ["Java", "Spring"]
        job_requirements = "Python, Django, React"
        score = calculator._calculate_skills_score(resume_skills, job_requirements)
        assert score <= 40  # Low score for no match
        
        # Test no requirements
        score = calculator._calculate_skills_score(resume_skills, "")
        assert score == 70  # Neutral score

    def test_calculate_location_score(self):
        """Test location score calculation."""
        calculator = MatchCalculator()
        
        # Test exact match
        assert calculator._calculate_location_score("New York, NY", "New York, NY", False) == 100
        
        # Test remote option
        assert calculator._calculate_location_score("New York, NY", "San Francisco, CA", True) == 80
        
        # Test city match
        assert calculator._calculate_location_score("New York, NY", "New York, CA", False) == 90
        
        # Test different locations
        assert calculator._calculate_location_score("New York, NY", "San Francisco, CA", False) == 30
        
        # Test missing information
        assert calculator._calculate_location_score("", "San Francisco, CA", False) == 70
        assert calculator._calculate_location_score("New York, NY", "", False) == 70

    def test_calculate_salary_score(self):
        """Test salary score calculation."""
        calculator = MatchCalculator()
        
        # Test good match
        resume_salary = {"min": 70000, "ideal": 85000}
        assert calculator._calculate_salary_score(resume_salary, 70000, 90000) == 90
        
        # Test close match
        assert calculator._calculate_salary_score(resume_salary, 60000, 80000) == 70
        
        # Test below expectations
        assert calculator._calculate_salary_score(resume_salary, 50000, 60000) == 40
        
        # Test missing information
        assert calculator._calculate_salary_score({}, 70000, 90000) == 70
        assert calculator._calculate_salary_score(resume_salary, 0, 0) == 70

    def test_determine_recommendation(self):
        """Test recommendation determination."""
        calculator = MatchCalculator()
        
        # Test strong match
        assert calculator._determine_recommendation(85) == "STRONG_MATCH"
        
        # Test possible match
        assert calculator._determine_recommendation(70) == "POSSIBLE_MATCH"
        
        # Test reach
        assert calculator._determine_recommendation(50) == "REACH"
        
        # Test skip
        assert calculator._determine_recommendation(20) == "SKIP"

    def test_extract_red_flags(self):
        """Test red flag extraction."""
        calculator = MatchCalculator()
        
        # Test senior role flag
        resume = {"experience_years": 2}
        job = {"experience_years": 5}
        red_flags = calculator.extract_red_flags(resume, job)
        assert any("5+ years" in flag for flag in red_flags)
        
        # Test experience mismatch
        job = {"experience_years": 6}
        red_flags = calculator.extract_red_flags(resume, job)
        assert any("6 years experience" in flag for flag in red_flags)
        
        # Test location mismatch
        resume = {"location": "New York, NY"}
        job = {"location": "San Francisco, CA", "remote_option": False}
        red_flags = calculator.extract_red_flags(resume, job)
        assert any("Location mismatch" in flag for flag in red_flags)
        
        # Test salary mismatch
        resume = {"salary_expectation": {"min": 80000}}
        job = {"salary_max": 70000}
        red_flags = calculator.extract_red_flags(resume, job)
        assert any("Salary below" in flag for flag in red_flags)

    def test_extract_hidden_opportunities(self):
        """Test hidden opportunity extraction."""
        calculator = MatchCalculator()
        
        # Test transferable skills
        resume = {"skills": ["JavaScript"]}
        job = {"requirements": "React, Node.js"}
        opportunities = calculator.extract_hidden_opportunities(resume, job)
        assert any("Transferable skill" in opp for opp in opportunities)
        
        # Test adjacent technologies
        resume = {"skills": ["Docker"]}
        job = {"requirements": "Kubernetes"}
        opportunities = calculator.extract_hidden_opportunities(resume, job)
        assert any("Adjacent technology" in opp for opp in opportunities)

    def test_calculate_match(self):
        """Test complete match calculation."""
        calculator = MatchCalculator()
        
        # Test good match
        resume = {
            "experience_years": 2,
            "skills": ["Python", "Django", "React"],
            "location": "New York, NY",
            "salary_expectation": {"min": 70000, "ideal": 85000}
        }
        
        job = {
            "experience_years": 2,
            "requirements": "Python, Django, React",
            "location": "New York, NY",
            "remote_option": False,
            "salary_min": 70000,
            "salary_max": 90000
        }
        
        result = calculator.calculate_match(resume, job)
        assert result["percentage"] >= 70
        assert result["recommendation"] in ["STRONG_MATCH", "POSSIBLE_MATCH"]
        assert "scores" in result