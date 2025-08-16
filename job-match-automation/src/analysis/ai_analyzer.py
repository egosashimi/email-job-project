"""
AI analysis module for job match automation.
Handles integration with DeepSeek via OpenRouter and job match analysis.
"""

import aiohttp
import json
import asyncio
from typing import Dict, Optional
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.config_manager import config


class AIJobAnalyzer:
    """Analyzes job matches using DeepSeek via OpenRouter."""

    def __init__(self):
        """Initialize AI job analyzer."""
        self.api_key = config.openrouter_api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "deepseek/deepseek-chat"
        self.session = None

    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()

    async def analyze_match(self, resume: Dict, job: Dict) -> Optional[Dict]:
        """Perform AI analysis of job match."""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            # Create the analysis prompt
            prompt = self._create_analysis_prompt(resume, job)
            
            # Prepare the API request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            # Make the API request
            async with self.session.post(self.base_url, headers=headers, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    # Extract the analysis from the response
                    content = result['choices'][0]['message']['content']
                    # Try to parse as JSON, fallback to text if parsing fails
                    try:
                        return json.loads(content)
                    except json.JSONDecodeError:
                        # If JSON parsing fails, return the content as reasoning
                        return {
                            "percentage": 50,  # Default percentage
                            "strengths": [],
                            "weaknesses": [],
                            "hidden_opportunities": [],
                            "red_flags": [],
                            "recommendation": "NEEDS_MANUAL_REVIEW",
                            "reasoning": content
                        }
                else:
                    print(f"API request failed with status {response.status}")
                    return None
        except Exception as e:
            print(f"Error during AI analysis: {e}")
            return None

    def _create_analysis_prompt(self, resume: Dict, job: Dict) -> str:
        """Create the analysis prompt for the AI model."""
        prompt = f"""You are a brutally honest career advisor analyzing job matches for a junior/mid-level developer.

Resume Summary:
{self._format_resume_summary(resume)}

Job Description:
{self._format_job_summary(job)}

Candidate Context:
- Junior/Mid level (2-3 years experience with AI-assisted development)
- Located in NYC, open to remote
- Salary expectation: $70-100k (minimum $45k)
- Strong with AI-assisted coding, Python/JavaScript experience
- No specific role preference, exploring opportunities

Analyze this match with brutal honesty. Consider:
1. Experience level match (reject if requires 5+ years)
2. Actual skill alignment (not keyword matching)
3. Hidden transferable skills that might apply
4. Red flags or concerns
5. Realistic chance of getting an interview

Provide a JSON response with this exact structure:
{{
    "percentage": <0-100>,
    "strengths": ["specific strength 1", "strength 2"],
    "weaknesses": ["specific gap 1", "gap 2"],
    "hidden_opportunities": ["transferable skill applications"],
    "red_flags": ["concern 1", "concern 2"],
    "recommendation": "STRONG_MATCH|POSSIBLE_MATCH|REACH|SKIP",
    "reasoning": "Brief explanation of the overall assessment"
}}

Be especially critical about experience requirements and technical depth."""

        return prompt

    def _format_resume_summary(self, resume: Dict) -> str:
        """Format resume data for the prompt."""
        summary = []
        
        if resume.get('experience_years'):
            summary.append(f"Experience: {resume['experience_years']} years")
        
        if resume.get('skills'):
            skills = resume['skills']
            if isinstance(skills, dict):
                skills_list = [f"{skill} ({level})" for skill, level in skills.items()]
                summary.append(f"Skills: {', '.join(skills_list)}")
            elif isinstance(skills, list):
                summary.append(f"Skills: {', '.join(skills)}")
        
        if resume.get('education'):
            summary.append(f"Education: {resume['education']}")
        
        if resume.get('location'):
            summary.append(f"Location: {resume['location']}")
        
        if resume.get('salary_expectation'):
            salary = resume['salary_expectation']
            if isinstance(salary, dict):
                min_salary = salary.get('min', 'N/A')
                ideal_salary = salary.get('ideal', 'N/A')
                summary.append(f"Salary Expectation: ${min_salary}-${ideal_salary}k")
        
        return "\n".join(summary) if summary else "No resume data provided"

    def _format_job_summary(self, job: Dict) -> str:
        """Format job data for the prompt."""
        summary = []
        
        if job.get('title'):
            summary.append(f"Title: {job['title']}")
        
        if job.get('company'):
            summary.append(f"Company: {job['company']}")
        
        if job.get('description'):
            # Truncate description to prevent token overflow
            desc = job['description'][:500] + "..." if len(job['description']) > 500 else job['description']
            summary.append(f"Description: {desc}")
        
        if job.get('requirements'):
            summary.append(f"Requirements: {job['requirements']}")
        
        if job.get('experience_years'):
            summary.append(f"Experience Required: {job['experience_years']} years")
        
        if job.get('salary_min') or job.get('salary_max'):
            min_sal = job.get('salary_min', 'N/A')
            max_sal = job.get('salary_max', 'N/A')
            summary.append(f"Salary Range: ${min_sal}-${max_sal}k")
        
        if job.get('location'):
            summary.append(f"Location: {job['location']}")
        
        if job.get('remote_option'):
            summary.append(f"Remote Option: {'Yes' if job['remote_option'] else 'No'}")
        
        return "\n".join(summary) if summary else "No job data provided"


# Example usage
async def main():
    """Example usage of the AIJobAnalyzer."""
    # Sample resume data
    resume = {
        "experience_years": 2,
        "skills": {
            "Python": "2 years",
            "JavaScript": "2 years",
            "AI-assisted development": "1 year"
        },
        "education": "Bachelor's in Computer Science",
        "location": "New York, NY",
        "salary_expectation": {
            "min": 70000,
            "ideal": 85000
        }
    }
    
    # Sample job data
    job = {
        "title": "Python Developer",
        "company": "TechCorp",
        "description": "We're looking for a Python developer with 2-3 years of experience...",
        "requirements": "Python, Django, PostgreSQL",
        "experience_years": 2,
        "salary_min": 70000,
        "salary_max": 90000,
        "location": "New York, NY",
        "remote_option": True
    }
    
    async with AIJobAnalyzer() as analyzer:
        print("Analyzing job match...")
        result = await analyzer.analyze_match(resume, job)
        if result:
            print(f"Match Percentage: {result.get('percentage', 'N/A')}%")
            print(f"Recommendation: {result.get('recommendation', 'N/A')}")
            print(f"Strengths: {result.get('strengths', [])}")
            print(f"Weaknesses: {result.get('weaknesses', [])}")
            print(f"Reasoning: {result.get('reasoning', 'N/A')}")
        else:
            print("Failed to analyze job match")


if __name__ == "__main__":
    asyncio.run(main())