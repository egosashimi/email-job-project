"""
Rule-based analysis fallback for job match automation.
Provides analysis when AI is unavailable or fails.
"""

from typing import Dict, List
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from analysis.match_calculator import MatchCalculator


class RuleBasedAnalyzer:
    """Rule-based job match analyzer for fallback when AI is unavailable."""

    def __init__(self):
        """Initialize rule-based analyzer."""
        self.match_calculator = MatchCalculator()

    def analyze_match(self, resume: Dict, job: Dict) -> Dict:
        """Perform rule-based analysis of job match."""
        # Calculate match using our match calculator
        match_result = self.match_calculator.calculate_match(resume, job)
        
        # Extract red flags
        red_flags = self.match_calculator.extract_red_flags(resume, job)
        
        # Extract hidden opportunities
        hidden_opportunities = self.match_calculator.extract_hidden_opportunities(resume, job)
        
        # Extract skills information for strengths/weaknesses
        strengths, weaknesses = self._analyze_skills_match(resume, job)
        
        # Create reasoning based on scores
        reasoning = self._generate_reasoning(match_result, red_flags, strengths, weaknesses)
        
        return {
            "percentage": match_result["percentage"],
            "strengths": strengths,
            "weaknesses": weaknesses,
            "hidden_opportunities": hidden_opportunities,
            "red_flags": red_flags,
            "recommendation": match_result["recommendation"],
            "reasoning": reasoning
        }

    def _analyze_skills_match(self, resume: Dict, job: Dict) -> tuple:
        """Analyze skills match to identify strengths and weaknesses."""
        strengths = []
        weaknesses = []
        
        resume_skills = set([skill.lower() for skill in resume.get('skills', [])])
        job_requirements = job.get('requirements', '')
        
        # Extract job skills (simplified approach)
        job_skills = set()
        common_skills = [
            'Python', 'JavaScript', 'Java', 'C++', 'C#', 'Ruby', 'PHP', 'Swift', 'Kotlin',
            'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask', 'Spring', 'Rails',
            'SQL', 'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Docker', 'Kubernetes',
            'AWS', 'Azure', 'GCP', 'CI/CD', 'Git', 'Linux', 'Windows', 'MacOS'
        ]
        
        for skill in common_skills:
            if skill.lower() in job_requirements.lower():
                job_skills.add(skill.lower())
        
        # Identify strengths (matching skills)
        matching_skills = resume_skills.intersection(job_skills)
        for skill in matching_skills:
            strengths.append(f"Proficient in {skill}")
        
        # Identify weaknesses (missing skills)
        missing_skills = job_skills.difference(resume_skills)
        for skill in missing_skills:
            weaknesses.append(f"Missing {skill} experience")
        
        # If no skills identified, provide generic feedback
        if not strengths and not weaknesses and job_skills:
            weaknesses.append("No specific skills identified from resume")
        
        return strengths, weaknesses

    def _generate_reasoning(self, match_result: Dict, red_flags: List[str], strengths: List[str], weaknesses: List[str]) -> str:
        """Generate reasoning based on analysis."""
        score = match_result["percentage"]
        recommendation = match_result["recommendation"]
        
        reasoning_parts = []
        
        # Overall assessment
        if score >= 80:
            reasoning_parts.append("This is a strong match based on your experience, skills, and job requirements.")
        elif score >= 60:
            reasoning_parts.append("This is a possible match with some alignment in experience and skills.")
        elif score >= 40:
            reasoning_parts.append("This is a reach opportunity that may require additional skill development.")
        else:
            reasoning_parts.append("This job may not be a good fit based on current experience and requirements.")
        
        # Experience assessment
        experience_score = match_result["scores"]["experience"]
        if experience_score >= 80:
            reasoning_parts.append("Your experience level aligns well with the job requirements.")
        elif experience_score >= 60:
            reasoning_parts.append("Your experience is somewhat aligned with the job requirements.")
        else:
            reasoning_parts.append("The job requires more experience than currently demonstrated.")
        
        # Skills assessment
        if strengths:
            reasoning_parts.append(f"Strengths include: {', '.join(strengths[:3])}.")
        
        if weaknesses:
            reasoning_parts.append(f"Areas for improvement include: {', '.join(weaknesses[:3])}.")
        
        # Red flags
        if red_flags:
            reasoning_parts.append(f"Red flags: {', '.join(red_flags)}.")
        
        # Recommendation
        if recommendation == "STRONG_MATCH":
            reasoning_parts.append("Recommended as a strong match to apply.")
        elif recommendation == "POSSIBLE_MATCH":
            reasoning_parts.append("Recommended as a possible match to consider applying.")
        elif recommendation == "REACH":
            reasoning_parts.append("Consider as a reach opportunity with additional preparation.")
        else:
            reasoning_parts.append("Not recommended to apply at this time.")
        
        return " ".join(reasoning_parts)


# Example usage
def main():
    """Example usage of the RuleBasedAnalyzer."""
    analyzer = RuleBasedAnalyzer()
    
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
    result = analyzer.analyze_match(resume, job)
    
    print("Rule-Based Analysis Result:")
    print(f"  Percentage: {result['percentage']}%")
    print(f"  Recommendation: {result['recommendation']}")
    print(f"  Strengths: {result['strengths']}")
    print(f"  Weaknesses: {result['weaknesses']}")
    print(f"  Hidden Opportunities: {result['hidden_opportunities']}")
    print(f"  Red Flags: {result['red_flags']}")
    print(f"  Reasoning: {result['reasoning']}")


if __name__ == "__main__":
    main()