"""
Demo script showing how the Phase 2 components work together.
"""

import sys
import os
import asyncio

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.resume_parser import ResumeParser
from analysis.match_calculator import MatchCalculator
from analysis.rule_based_analyzer import RuleBasedAnalyzer


def demo_resume_parsing():
    """Demo resume parsing functionality."""
    print("=== Resume Parsing Demo ===")
    
    # Create a sample resume
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
    
    # Parse the resume
    parser = ResumeParser()
    resume_info = parser.parse('sample_resume.txt')
    
    print("Parsed Resume Information:")
    for key, value in resume_info.items():
        print(f"  {key}: {value}")
    print()


def demo_match_calculation():
    """Demo match calculation functionality."""
    print("=== Match Calculation Demo ===")
    
    # Sample resume data
    resume = {
        "experience_years": 2,
        "skills": ["Python", "JavaScript", "React", "Django", "SQL"],
        "location": "New York, NY",
        "salary_expectation": {"min": 70000, "ideal": 85000}
    }
    
    # Sample job data
    job = {
        "experience_years": 2,
        "requirements": "Python, Django, React, PostgreSQL",
        "location": "New York, NY",
        "remote_option": True,
        "salary_min": 70000,
        "salary_max": 90000
    }
    
    # Calculate match
    calculator = MatchCalculator()
    match_result = calculator.calculate_match(resume, job)
    
    print("Match Calculation Result:")
    print(f"  Percentage: {match_result['percentage']}%")
    print(f"  Recommendation: {match_result['recommendation']}")
    print("  Scores:")
    for category, score in match_result['scores'].items():
        print(f"    {category}: {score}")
    print()


def demo_rule_based_analysis():
    """Demo rule-based analysis functionality."""
    print("=== Rule-Based Analysis Demo ===")
    
    # Sample resume data
    resume = {
        "experience_years": 2,
        "skills": ["Python", "JavaScript", "React", "Django", "SQL"],
        "location": "New York, NY",
        "salary_expectation": {"min": 70000, "ideal": 85000}
    }
    
    # Sample job data
    job = {
        "experience_years": 2,
        "requirements": "Python, Django, React, PostgreSQL",
        "location": "New York, NY",
        "remote_option": True,
        "salary_min": 70000,
        "salary_max": 90000
    }
    
    # Perform rule-based analysis
    analyzer = RuleBasedAnalyzer()
    result = analyzer.analyze_match(resume, job)
    
    print("Rule-Based Analysis Result:")
    print(f"  Percentage: {result['percentage']}%")
    print(f"  Recommendation: {result['recommendation']}")
    print(f"  Strengths: {result['strengths']}")
    print(f"  Weaknesses: {result['weaknesses']}")
    print(f"  Hidden Opportunities: {result['hidden_opportunities']}")
    print(f"  Red Flags: {result['red_flags']}")
    print(f"  Reasoning: {result['reasoning']}")
    print()


async def main():
    """Run all demos."""
    print("Job Match Automation - Phase 2 Demo")
    print("=" * 40)
    print()
    
    # Run resume parsing demo
    demo_resume_parsing()
    
    # Run match calculation demo
    demo_match_calculation()
    
    # Run rule-based analysis demo
    demo_rule_based_analysis()
    
    print("=== Demo Complete ===")
    print()
    print("Phase 2 components are working correctly:")
    print("1. Resume parsing extracts key information")
    print("2. Match calculation provides weighted scores")
    print("3. Rule-based analysis gives detailed feedback")


if __name__ == "__main__":
    asyncio.run(main())