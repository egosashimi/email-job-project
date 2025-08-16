"""
Unit tests for the AI analyzer module.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
import sys
import os
import json

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from analysis.ai_analyzer import AIJobAnalyzer


class TestAIJobAnalyzer:
    """Tests for the AIJobAnalyzer class."""

    def test_init(self):
        """Test AIJobAnalyzer initialization."""
        # Mock the config
        from core import config_manager
        original_config = config_manager.config
        mock_config = Mock()
        mock_config.openrouter_api_key = 'test-key'
        config_manager.config = mock_config
        
        analyzer = AIJobAnalyzer()
        
        # Restore the original config
        config_manager.config = original_config
        
        assert analyzer.api_key == 'test-key'
        assert analyzer.base_url == "https://openrouter.ai/api/v1/chat/completions"
        assert analyzer.model == "deepseek/deepseek-chat"

    def test_format_resume_summary(self):
        """Test resume summary formatting."""
        analyzer = AIJobAnalyzer()
        
        # Test with complete resume data
        resume = {
            "experience_years": 2,
            "skills": {
                "Python": "2 years",
                "JavaScript": "2 years"
            },
            "education": "Bachelor's in Computer Science",
            "location": "New York, NY",
            "salary_expectation": {
                "min": 70000,
                "ideal": 85000
            }
        }
        
        summary = analyzer._format_resume_summary(resume)
        assert "Experience: 2 years" in summary
        assert "Skills: Python (2 years), JavaScript (2 years)" in summary
        assert "Education: Bachelor's in Computer Science" in summary
        assert "Location: New York, NY" in summary
        assert "Salary Expectation: $70000-$85000k" in summary

    def test_format_job_summary(self):
        """Test job summary formatting."""
        analyzer = AIJobAnalyzer()
        
        # Test with complete job data
        job = {
            "title": "Python Developer",
            "company": "TechCorp",
            "description": "We're looking for a Python developer...",
            "requirements": "Python, Django, React",
            "experience_years": 2,
            "salary_min": 70000,
            "salary_max": 90000,
            "location": "New York, NY",
            "remote_option": True
        }
        
        summary = analyzer._format_job_summary(job)
        assert "Title: Python Developer" in summary
        assert "Company: TechCorp" in summary
        assert "Description: We're looking for a Python developer..." in summary
        assert "Requirements: Python, Django, React" in summary
        assert "Experience Required: 2 years" in summary
        assert "Salary Range: $70000-$90000k" in summary
        assert "Location: New York, NY" in summary
        assert "Remote Option: Yes" in summary

    @pytest.mark.asyncio
    async def test_analyze_match_success(self):
        """Test successful AI analysis."""
        # Mock the config
        from core import config_manager
        original_config = config_manager.config
        mock_config = Mock()
        mock_config.openrouter_api_key = 'test-key'
        config_manager.config = mock_config
        
        # Create analyzer
        analyzer = AIJobAnalyzer()
        
        # Restore the original config
        config_manager.config = original_config
        
        # Mock the HTTP session
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            'choices': [{
                'message': {
                    'content': json.dumps({
                        "percentage": 75,
                        "strengths": ["Python experience"],
                        "weaknesses": ["Missing React experience"],
                        "recommendation": "POSSIBLE_MATCH",
                        "reasoning": "Good match with some gaps"
                    })
                }
            }]
        })
        mock_session.post.return_value.__aenter__.return_value = mock_response
        analyzer.session = mock_session
        
        # Test data
        resume = {"experience_years": 2}
        job = {"title": "Python Developer"}
        
        # Perform analysis
        result = await analyzer.analyze_match(resume, job)
        
        # Verify result
        assert result is not None
        assert result["percentage"] == 75
        assert result["recommendation"] == "POSSIBLE_MATCH"
        assert "Python experience" in result["strengths"]
        assert "Missing React experience" in result["weaknesses"]

    @pytest.mark.asyncio
    async def test_analyze_match_failure(self):
        """Test failed AI analysis."""
        # Mock the config
        from core import config_manager
        original_config = config_manager.config
        mock_config = Mock()
        mock_config.openrouter_api_key = 'test-key'
        config_manager.config = mock_config
        
        # Create analyzer
        analyzer = AIJobAnalyzer()
        
        # Restore the original config
        config_manager.config = original_config
        
        # Mock the HTTP session to raise an exception
        mock_session = AsyncMock()
        mock_session.post.side_effect = Exception("API Error")
        analyzer.session = mock_session
        
        # Test data
        resume = {"experience_years": 2}
        job = {"title": "Python Developer"}
        
        # Perform analysis
        result = await analyzer.analyze_match(resume, job)
        
        # Verify result
        assert result is None