"""
Resume parsing module for job match automation.
Handles parsing resumes from various formats and extracting relevant information.
"""

import re
from typing import Dict, List, Optional
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.config_manager import config


class ResumeParser:
    """Parses resumes and extracts relevant information for job matching."""

    def __init__(self):
        """Initialize resume parser."""
        pass

    def parse(self, resume_path: str) -> Dict:
        """Parse a resume file and extract relevant information."""
        # Determine file type and parse accordingly
        if resume_path.endswith('.txt'):
            return self._parse_text_resume(resume_path)
        elif resume_path.endswith('.pdf'):
            return self._parse_pdf_resume(resume_path)
        elif resume_path.endswith('.docx'):
            return self._parse_docx_resume(resume_path)
        else:
            # Try to parse as text if unknown format
            return self._parse_text_resume(resume_path)

    def _parse_text_resume(self, resume_path: str) -> Dict:
        """Parse a text-based resume."""
        try:
            with open(resume_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return self._extract_resume_info(content)
        except Exception as e:
            print(f"Error parsing text resume: {e}")
            return {}

    def _parse_pdf_resume(self, resume_path: str) -> Dict:
        """Parse a PDF resume."""
        try:
            # For now, we'll just try to extract text from PDF
            # In a real implementation, you'd use a library like PyPDF2 or pdfminer
            print("PDF parsing not implemented yet, treating as text")
            return self._parse_text_resume(resume_path)
        except Exception as e:
            print(f"Error parsing PDF resume: {e}")
            return {}

    def _parse_docx_resume(self, resume_path: str) -> Dict:
        """Parse a Word document resume."""
        try:
            # For now, we'll just try to extract text from DOCX
            # In a real implementation, you'd use a library like python-docx
            print("DOCX parsing not implemented yet, treating as text")
            return self._parse_text_resume(resume_path)
        except Exception as e:
            print(f"Error parsing DOCX resume: {e}")
            return {}

    def _extract_resume_info(self, content: str) -> Dict:
        """Extract information from resume content."""
        resume_info = {}
        
        # Extract experience years
        resume_info['experience_years'] = self._extract_experience_years(content)
        
        # Extract skills
        resume_info['skills'] = self._extract_skills(content)
        
        # Extract education
        resume_info['education'] = self._extract_education(content)
        
        # Extract location
        resume_info['location'] = self._extract_location(content)
        
        # Extract salary expectations
        resume_info['salary_expectation'] = self._extract_salary_expectations(content)
        
        return resume_info

    def _extract_experience_years(self, content: str) -> Optional[int]:
        """Extract total years of experience from resume."""
        # Look for patterns like "X years of experience"
        patterns = [
            r'(\\d+)\\+?\\s*years?\\s*(?:of\\s*)?experience',
            r'(\\d+)\\+?\\s*years?\\s*(?:of\\s*)?professional',
            r'(\\d+)\\+?\\s*yr',
            r'minimum\\s*(\\d+)\\s*years?',
            r'at least\\s*(\\d+)\\s*years?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        # If no explicit experience mentioned, try to calculate from work history
        return self._calculate_experience_from_history(content)

    def _calculate_experience_from_history(self, content: str) -> Optional[int]:
        """Calculate experience from work history entries."""
        # This is a simplified implementation
        # A real implementation would parse dates more carefully
        date_pattern = r'(?:\\d{4}|\\d{2})\\s*(?:-|to|through)\\s*(?:\\d{4}|present|current)'
        matches = re.findall(date_pattern, content, re.IGNORECASE)
        
        if matches:
            # For now, we'll just return a default value
            # A real implementation would calculate the actual years
            return 2
        
        return None

    def _extract_skills(self, content: str) -> List[str]:
        """Extract skills from resume."""
        # Look for a skills section
        skills_section = self._extract_section(content, ['skills', 'technologies', 'tools'])
        
        if skills_section:
            # Extract individual skills (simplified approach)
            # In a real implementation, you'd want more sophisticated parsing
            skills = re.split(r'[,;\\n]', skills_section)
            skills = [skill.strip() for skill in skills if skill.strip()]
            return skills[:20]  # Limit to 20 skills
        
        # Fallback: look for common skill keywords throughout the resume
        common_skills = [
            'Python', 'JavaScript', 'Java', 'C++', 'C#', 'Ruby', 'PHP', 'Swift', 'Kotlin',
            'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask', 'Spring', 'Rails',
            'SQL', 'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Docker', 'Kubernetes',
            'AWS', 'Azure', 'GCP', 'CI/CD', 'Git', 'Linux', 'Windows', 'MacOS'
        ]
        
        found_skills = []
        content_lower = content.lower()
        
        for skill in common_skills:
            if skill.lower() in content_lower:
                found_skills.append(skill)
        
        return found_skills[:20]  # Limit to 20 skills

    def _extract_education(self, content: str) -> str:
        """Extract education information."""
        education_section = self._extract_section(content, ['education', 'academic'])
        
        if education_section:
            # Return the first line of the education section as a summary
            lines = education_section.strip().split('\\n')
            return lines[0] if lines else ""
        
        # Fallback: look for degree patterns
        degree_patterns = [
            r'Bachelor.*(?:in\\s+)?(\\w+(?:\\s+\\w+)*)',
            r'Master.*(?:in\\s+)?(\\w+(?:\\s+\\w+)*)',
            r'PhD.*(?:in\\s+)?(\\w+(?:\\s+\\w+)*)',
            r'Associate.*(?:in\\s+)?(\\w+(?:\\s+\\w+)*)'
        ]
        
        for pattern in degree_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return ""

    def _extract_location(self, content: str) -> str:
        """Extract location information."""
        # Look for a location section or contact info
        location_section = self._extract_section(content, ['location', 'address', 'contact'])
        
        if location_section:
            # Look for city, state patterns
            location_pattern = r'([A-Za-z\\s]+),?\\s+([A-Z]{2})'
            match = re.search(location_pattern, location_section)
            if match:
                return f"{match.group(1)}, {match.group(2)}"
        
        # Fallback: look for NYC specifically (as mentioned in requirements)
        if 'new york' in content.lower() or 'nyc' in content.lower():
            return "New York, NY"
        
        return ""

    def _extract_salary_expectations(self, content: str) -> Dict:
        """Extract salary expectations."""
        # Look for salary patterns
        salary_patterns = [
            r'\\$(\\d+)(?:,(\\d+))?\\s*(?:-|to)\\s*\\$(\\d+)(?:,(\\d+))?'
            r'\\$(\\d+)(?:,(\\d+))?'
        ]
        
        for pattern in salary_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                groups = match.groups()
                if len(groups) >= 4 and groups[2]:  # Range format
                    min_salary = int(groups[0] + (groups[1] or '000'))
                    max_salary = int(groups[2] + (groups[3] or '000'))
                    return {"min": min_salary, "ideal": max_salary}
                else:  # Single value
                    salary = int(groups[0] + (groups[1] or '000'))
                    return {"min": salary, "ideal": salary + 15000}  # Add buffer for ideal
        
        # Return default values based on project requirements
        return {"min": 70000, "ideal": 85000}

    def _extract_section(self, content: str, section_names: List[str]) -> str:
        """Extract a specific section from the resume."""
        content_lower = content.lower()
        
        for section_name in section_names:
            # Look for section header
            section_pattern = rf'{section_name}[\\s:]*\\n(?:-|\\*|\\d+\\.|\\n)*([^\\n].*?)(?=\\n(?:\\w|\\Z))'
            match = re.search(section_pattern, content_lower, re.DOTALL | re.IGNORECASE)
            
            if match:
                # Find the actual section in the original content
                start_pos = content_lower.find(match.group(0))
                if start_pos != -1:
                    # Extract the section content
                    section_content = content[start_pos:start_pos + len(match.group(0))]
                    return section_content
        
        return ""


# Example usage
def main():
    """Example usage of the ResumeParser."""
    parser = ResumeParser()
    
    # Create a sample resume file for testing
    sample_resume = """John Doe
New York, NY
john.doe@email.com
(555) 123-4567

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
    resume_info = parser.parse('sample_resume.txt')
    
    print("Parsed Resume Information:")
    for key, value in resume_info.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()