"""
Job scraping functionality for job match automation.
Handles fetching job details from job board URLs.
"""

import aiohttp
import asyncio
import re
from typing import Dict, Optional
from urllib.parse import urlparse
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.config_manager import config


class JobScraper:
    """Fetches full job descriptions from job board URLs."""

    SCRAPING_RULES = {
        'linkedin.com': {
            'job_title': ['h1.topcard__title'],
            'company': ['a.topcard__org-name-link'],
            'location': ['span.topcard__flavor:nth-child(2)'],
            'description': ['div.description__text', 'div.show-more-less-html__markup'],
            'requirements': ['ul.description__job-criteria-list'],
            'salary': ['div.salary-main-content', 'span.salary-range']
        },
        'indeed.com': {
            'job_title': ['h1.jobsearch-JobInfoHeader-title'],
            'company': ['div.jobsearch-InlineCompanyRating a'],
            'location': ['div.jobsearch-InlineCompanyRating div:nth-child(3)'],
            'description': ['div.jobsearch-JobComponent-description', 'div#jobDescriptionText'],
            'requirements': ['div.jobsearch-JobComponent-description'],
            'salary': ['span.salary-snippet', 'div.salary-container']
        },
        'ziprecruiter.com': {
            'job_title': ['h1.job_title'],
            'company': ['div.job_company'],
            'location': ['div.location_content'],
            'description': ['div.job_description'],
            'requirements': ['div.job_description'],
            'salary': ['span.salary']
        }
    }

    def __init__(self):
        """Initialize job scraper."""
        self.session = None

    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()

    async def fetch_job_details(self, url: str) -> Optional[Dict]:
        """Fetch and parse job details from URL."""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
                
            async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                if response.status == 200:
                    html = await response.text()
                    return self._parse_job_page(html, urlparse(url).netloc)
                else:
                    print(f"HTTP {response.status} error fetching {url}")
                    return None
        except asyncio.TimeoutError:
            print(f"Timeout error fetching {url}")
            return None
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def _parse_job_page(self, html: str, domain: str) -> Optional[Dict]:
        """Parse job page HTML based on domain-specific rules."""
        # Extract domain-specific rules
        rules = self.SCRAPING_RULES.get(domain, {})
        if not rules:
            # Try generic parsing
            return self._parse_generic(html)
        
        # Parse using domain-specific rules
        job_data = {}
        
        # Extract job title
        job_data['title'] = self._extract_by_selectors(html, rules.get('job_title', []))
        
        # Extract company
        job_data['company'] = self._extract_by_selectors(html, rules.get('company', []))
        
        # Extract location
        job_data['location'] = self._extract_by_selectors(html, rules.get('location', []))
        
        # Extract description
        job_data['description'] = self._extract_by_selectors(html, rules.get('description', []))
        
        # Extract requirements
        job_data['requirements'] = self._extract_by_selectors(html, rules.get('requirements', []))
        
        # Extract salary
        job_data['salary'] = self._extract_by_selectors(html, rules.get('salary', []))
        
        # Extract experience requirement
        job_data['experience_years'] = self._extract_experience_years(job_data.get('description', '') + 
                                                                      job_data.get('requirements', ''))
        
        return job_data

    def _extract_by_selectors(self, html: str, selectors: list) -> str:
        """Extract content using CSS selectors (simplified implementation)."""
        # This is a simplified implementation - in practice, you'd use BeautifulSoup
        # For now, we'll use regex to extract content
        for selector in selectors:
            # This is a very basic implementation - a real implementation would use BeautifulSoup
            # For now, we'll just try to extract some text
            pattern = r'>([^<]+)<'
            matches = re.findall(pattern, html)
            if matches:
                # Return the first non-empty match
                for match in matches:
                    text = match.strip()
                    if text:
                        return text
        return ""

    def _extract_experience_years(self, text: str) -> Optional[int]:
        """Extract years of experience requirement."""
        patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'(\d+)\+?\s*years?\s*(?:of\s*)?professional',
            r'(\d+)\+?\s*yr',
            r'minimum\s*(\d+)\s*years?',
            r'at least\s*(\d+)\s*years?'
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        return None

    def _parse_generic(self, html: str) -> Dict:
        """Generic parsing for unknown job boards."""
        # Extract title (look for <title> tag or <h1> tags)
        title_match = re.search(r'<title>([^<]+)', html, re.IGNORECASE)
        if not title_match:
            title_match = re.search(r'<h1[^>]*>([^<]+)', html, re.IGNORECASE)
        
        title = title_match.group(1).strip() if title_match else "Unknown Job"
        
        # Extract description (look for large blocks of text)
        desc_matches = re.findall(r'<p[^>]*>([^<]+)', html, re.IGNORECASE)
        description = " ".join(desc_matches[:10]) if desc_matches else ""
        
        # Extract experience requirement
        experience_years = self._extract_experience_years(html)
        
        return {
            'title': title,
            'description': description,
            'experience_years': experience_years
        }


# Example usage
async def main():
    """Example usage of the JobScraper."""
    urls = [
        "https://www.linkedin.com/jobs/view/test-job-123/",
        "https://www.indeed.com/viewjob?jk=test123",
        "https://www.ziprecruiter.com/job/test-job-456"
    ]
    
    async with JobScraper() as scraper:
        for url in urls:
            print(f"Fetching job details for {url}")
            job_details = await scraper.fetch_job_details(url)
            if job_details:
                print(f"Title: {job_details.get('title', 'N/A')}")
                print(f"Company: {job_details.get('company', 'N/A')}")
                print(f"Experience Required: {job_details.get('experience_years', 'N/A')} years")
                print("-" * 50)
            else:
                print(f"Failed to fetch details for {url}")


if __name__ == "__main__":
    asyncio.run(main())