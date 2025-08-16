"""
Match calculation module for job match automation.
Handles calculation of match percentages and recommendations.
"""

from typing import Dict, List, Optional
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.config_manager import config


class MatchCalculator:
    """Calculates job match percentages and provides recommendations."""

    def __init__(self):
        """Initialize match calculator."""
        pass

    def calculate_match(self, resume: Dict, job: Dict) -> Dict:
        """Calculate match percentage and provide recommendation."""
        # Extract key information
        resume_experience = resume.get('experience_years', 0)
        job_experience = job.get('experience_years', 0)
        
        # Check for senior role filter (5+ years requirement)
        if job_experience >= 5:
            return {
                "percentage": 0,
                "recommendation": "SKIP",
                "reason": "Job requires 5+ years experience which exceeds candidate level"
            }
        
        # Calculate experience match
        experience_score = self._calculate_experience_score(resume_experience, job_experience)
        
        # Calculate skills match
        skills_score = self._calculate_skills_score(resume.get('skills', []), job.get('requirements', ''))
        
        # Calculate location match
        location_score = self._calculate_location_score(resume.get('location', ''), job.get('location', ''), job.get('remote_option', False))
        
        # Calculate salary match
        salary_score = self._calculate_salary_score(resume.get('salary_expectation', {}), job.get('salary_min', 0), job.get('salary_max', 0))
        
        # Weighted average of all scores
        # Experience: 30%, Skills: 40%, Location: 15%, Salary: 15%
        total_score = (
            experience_score * 0.3 +
            skills_score * 0.4 +
            location_score * 0.15 +
            salary_score * 0.15
        )
        
        # Determine recommendation based on score
        recommendation = self._determine_recommendation(total_score)
        
        return {
            "percentage": round(total_score),
            "recommendation": recommendation,
            "scores": {
                "experience": experience_score,
                "skills": skills_score,
                "location": location_score,
                "salary": salary_score
            }
        }

    def _calculate_experience_score(self, resume_experience: int, job_experience: int) -> int:
        """Calculate experience match score."""
        if job_experience == 0:
            # No experience requirement specified
            return 70  # Neutral score
        
        if resume_experience >= job_experience:
            # Candidate meets or exceeds requirement
            return 90
        
        # Calculate partial match based on proximity
        if job_experience <= resume_experience + 1:
            return 75
        elif job_experience <= resume_experience + 2:
            return 60
        else:
            return 30

    def _calculate_skills_score(self, resume_skills: List[str], job_requirements: str) -> int:
        """Calculate skills match score."""
        if not job_requirements:
            return 70  # Neutral score if no requirements specified
        
        # Convert resume skills to lowercase for comparison
        resume_skills_lower = [skill.lower() for skill in resume_skills]
        
        # Extract skills from job requirements (simplified approach)
        job_skills = re.findall(r'\b(?:Python|JavaScript|Java|C\+\+|C#|Ruby|PHP|Swift|Kotlin|React|Angular|Vue|Node\.js|Django|Flask|Spring|Rails|SQL|PostgreSQL|MySQL|MongoDB|Redis|Docker|Kubernetes|AWS|Azure|GCP|CI/CD|Git|Linux|Windows|MacOS)\b', job_requirements, re.IGNORECASE)
        
        if not job_skills:
            return 70  # Neutral score if no recognizable skills in requirements
        
        # Count matching skills
        matching_skills = 0
        for skill in job_skills:
            if skill.lower() in resume_skills_lower:
                matching_skills += 1
        
        # Calculate percentage match
        match_percentage = (matching_skills / len(job_skills)) * 100
        
        # Adjust score to be between 0-100 with some baseline
        return max(10, min(100, int(match_percentage * 0.8 + 20)))

    def _calculate_location_score(self, resume_location: str, job_location: str, remote_option: bool) -> int:
        """Calculate location match score."""
        # If remote is an option, location is less important
        if remote_option:
            return 80
        
        # If either location is not specified, return neutral score
        if not resume_location or not job_location:
            return 70
        
        # Check for exact match
        if resume_location.lower() == job_location.lower():
            return 100
        
        # Check for partial match (same city)
        resume_parts = resume_location.split(',')
        job_parts = job_location.split(',')
        
        if len(resume_parts) > 0 and len(job_parts) > 0:
            if resume_parts[0].strip().lower() == job_parts[0].strip().lower():
                return 90
        
        # Different locations
        return 30

    def _calculate_salary_score(self, resume_salary: Dict, job_salary_min: int, job_salary_max: int) -> int:
        """Calculate salary match score."""
        # If no salary information, return neutral score
        if not resume_salary or (job_salary_min == 0 and job_salary_max == 0):
            return 70
        
        resume_min = resume_salary.get('min', 0)
        resume_ideal = resume_salary.get('ideal', 0)
        
        # If resume doesn't specify salary expectations, return neutral
        if resume_min == 0 and resume_ideal == 0:
            return 70
        
        # If job doesn't specify salary, assume it's competitive
        if job_salary_min == 0 and job_salary_max == 0:
            return 80
        
        # Check if job meets minimum salary requirement
        if job_salary_max >= resume_min and job_salary_min <= resume_ideal:
            return 90
        
        # Check if job is close to salary expectations
        if job_salary_max >= resume_min * 0.8:
            return 70
        
        # Salary is below expectations
        return 40

    def _determine_recommendation(self, score: int) -> str:
        """Determine recommendation based on match score."""
        if score >= 80:
            return "STRONG_MATCH"
        elif score >= 60:
            return "POSSIBLE_MATCH"
        elif score >= 40:
            return "REACH"
        else:
            return "SKIP"

    def extract_red_flags(self, resume: Dict, job: Dict) -> List[str]:
        """Extract red flags from job posting."""
        red_flags = []
        
        # Experience mismatch
        resume_experience = resume.get('experience_years', 0)
        job_experience = job.get('experience_years', 0)
        
        if job_experience >= 5:
            red_flags.append("Job requires 5+ years experience")
        elif job_experience > resume_experience + 2:
            red_flags.append(f"Job requires {job_experience} years experience, {resume_experience} years available")
        
        # Location mismatch (if not remote)
        if not job.get('remote_option', False):
            resume_location = resume.get('location', '').lower()
            job_location = job.get('location', '').lower()
            
            if resume_location and job_location and resume_location != job_location:
                # Check if cities match
                resume_city = resume_location.split(',')[0].strip()
                job_city = job_location.split(',')[0].strip()
                
                if resume_city != job_city:
                    red_flags.append(f"Location mismatch: candidate in {resume_location}, job in {job_location}")
        
        # Salary mismatch
        resume_salary = resume.get('salary_expectation', {})
        job_min = job.get('salary_min', 0)
        job_max = job.get('salary_max', 0)
        
        if resume_salary and (job_min > 0 or job_max > 0):
            resume_min = resume_salary.get('min', 0)
            if job_max < resume_min:
                red_flags.append(f"Salary below minimum expectation: ${job_max}k < ${resume_min}k")
        
        return red_flags

    def extract_hidden_opportunities(self, resume: Dict, job: Dict) -> List[str]:
        """Extract hidden opportunities from job posting."""
        opportunities = []
        
        # Check for transferable skills
        resume_skills = resume.get('skills', [])
        job_requirements = job.get('requirements', '')
        
        # Look for related skills that might be transferable
        transferable_skills = {
            'JavaScript': ['React', 'Vue', 'Angular', 'Node.js'],
            'Python': ['Django', 'Flask', 'FastAPI'],
            'SQL': ['PostgreSQL', 'MySQL', 'MongoDB'],
            'Git': ['CI/CD', 'DevOps']
        }
        
        for resume_skill in resume_skills:
            related_skills = transferable_skills.get(resume_skill, [])
            for related_skill in related_skills:
                if related_skill.lower() in job_requirements.lower():
                    opportunities.append(f"Transferable skill: {resume_skill} -> {related_skill}")
        
        # Check for adjacent technologies
        adjacent_tech = {
            'Docker': ['Kubernetes'],
            'AWS': ['Azure', 'GCP'],
            'React': ['Vue', 'Angular']
        }
        
        for skill in resume_skills:
            adjacents = adjacent_tech.get(skill, [])
            for adjacent in adjacents:
                if adjacent.lower() in job_requirements.lower():
                    opportunities.append(f"Adjacent technology: {skill} -> {adjacent}")
        
        return opportunities


# Import regex module
import re

# Example usage
def main():
    """Example usage of the MatchCalculator."""
    calculator = MatchCalculator()
    
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
    match_result = calculator.calculate_match(resume, job)
    print("Match Result:")
    print(f"  Percentage: {match_result['percentage']}%")
    print(f"  Recommendation: {match_result['recommendation']}")
    print("  Scores:")
    for category, score in match_result['scores'].items():
        print(f"    {category}: {score}")
    
    # Extract red flags
    red_flags = calculator.extract_red_flags(resume, job)
    print(f"\nRed Flags: {red_flags}")
    
    # Extract hidden opportunities
    opportunities = calculator.extract_hidden_opportunities(resume, job)
    print(f"Hidden Opportunities: {opportunities}")


if __name__ == "__main__":
    main()