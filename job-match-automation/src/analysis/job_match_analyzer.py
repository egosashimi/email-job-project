"""
Unified analysis module for job match automation.
Combines AI analysis with rule-based fallback.
"""

from typing import Dict, Optional
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from analysis.ai_analyzer import AIJobAnalyzer
from analysis.rule_based_analyzer import RuleBasedAnalyzer
from core.resume_parser import ResumeParser


class JobMatchAnalyzer:
    """Unified job match analyzer combining AI and rule-based approaches."""

    def __init__(self):
        """Initialize job match analyzer."""
        self.ai_analyzer = AIJobAnalyzer()
        self.rule_based_analyzer = RuleBasedAnalyzer()
        self.resume_parser = ResumeParser()

    async def analyze_match(self, resume_path: str, job: Dict) -> Dict:
        """Perform job match analysis with AI fallback."""
        # Parse resume
        resume = self.resume_parser.parse(resume_path)
        
        # Try AI analysis first
        ai_result = await self._try_ai_analysis(resume, job)
        
        if ai_result:
            return ai_result
        
        # Fallback to rule-based analysis
        print("AI analysis failed, falling back to rule-based analysis")
        return self.rule_based_analyzer.analyze_match(resume, job)

    async def _try_ai_analysis(self, resume: Dict, job: Dict) -> Optional[Dict]:
        """Try AI analysis with error handling."""
        try:
            async with AIJobAnalyzer() as ai_analyzer:
                result = await ai_analyzer.analyze_match(resume, job)
                if result:
                    # Ensure result has all required fields
                    required_fields = ['percentage', 'strengths', 'weaknesses', 'recommendation', 'reasoning']
                    for field in required_fields:
                        if field not in result:
                            result[field] = self._get_default_value(field)
                    
                    # Add hidden opportunities and red flags if not present
                    if 'hidden_opportunities' not in result:
                        result['hidden_opportunities'] = []
                    
                    if 'red_flags' not in result:
                        result['red_flags'] = self.rule_based_analyzer.match_calculator.extract_red_flags(resume, job)
                    
                    return result
        except Exception as e:
            print(f"AI analysis failed: {e}")
        
        return None

    def _get_default_value(self, field: str):
        """Get default value for missing fields."""
        defaults = {
            'percentage': 50,
            'strengths': [],
            'weaknesses': [],
            'recommendation': 'NEEDS_MANUAL_REVIEW',
            'reasoning': 'Analysis failed, using default values'
        }
        return defaults.get(field, '')

    def analyze_match_sync(self, resume_path: str, job: Dict) -> Dict:
        """Synchronous version of match analysis using rule-based only."""
        # Parse resume
        resume = self.resume_parser.parse(resume_path)
        
        # Use rule-based analysis
        return self.rule_based_analyzer.analyze_match(resume, job)


# Example usage
async def main():
    """Example usage of the JobMatchAnalyzer."""
    analyzer = JobMatchAnalyzer()
    
    # Create a sample resume file for testing
    sample_resume = """John Doe
New York, NY
john.doe@email.com

SUMMARY
Experienced Python and JavaScript developer with 2 years of professional experience.
Skilled in AI-assisted development and full-stack applications.

SKILLS
Python, JavaScript, React, Node.js, Django, Flask, SQL, PostgreSQL, Git, Docker

EXPERIENCE
Software Developer, TechCorp
2022 - Present
- Developed Python applications using Django and Flask
- Created responsive web interfaces with React
- Implemented RESTful APIs with Node.js

Junior Developer, StartupXYZ
2021 - 2022
- Worked on JavaScript projects using React and Node.js
- Collaborated with senior developers on Python backend services

EDUCATION
Bachelor of Science in Computer Science
University of New York, 2021

SALARY EXPECTATIONS
$70,000 - $85,000
"""
    
    # Write sample resume to file
    with open('sample_resume.txt', 'w') as f:
        f.write(sample_resume)
    
    # Sample job data
    job = {
        "title": "Python Developer",
        "company": "TechCorp",
        "description": "We're looking for a Python developer with 2-3 years of experience...",
        "requirements": "Python, Django, React, PostgreSQL",
        "experience_years": 2,
        "salary_min": 70000,
        "salary_max": 90000,
        "location": "New York, NY",
        "remote_option": True
    }
    
    # Perform analysis
    print("Performing job match analysis...")
    result = await analyzer.analyze_match('sample_resume.txt', job)
    
    print("\nAnalysis Result:")
    print(f"  Percentage: {result['percentage']}%")
    print(f"  Recommendation: {result['recommendation']}")
    print(f"  Strengths: {result['strengths']}")
    print(f"  Weaknesses: {result['weaknesses']}")
    if result.get('hidden_opportunities'):
        print(f"  Hidden Opportunities: {result['hidden_opportunities']}")
    if result.get('red_flags'):
        print(f"  Red Flags: {result['red_flags']}")
    print(f"  Reasoning: {result['reasoning']}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())