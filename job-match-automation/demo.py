"""
Demo script showing how the email monitoring and job scraping components work together.
"""

import sys
import os
import asyncio

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.email_monitor import EmailMonitor
from core.job_scraper import JobScraper
from storage.database import DatabaseManager


def demo_email_monitoring():
    """Demo email monitoring functionality."""
    print("=== Email Monitoring Demo ===")
    print("This demo shows how the email monitoring system works.")
    print("Note: This will not actually connect to an email server without credentials.")
    print()
    
    # Create email monitor (won't connect without credentials)
    monitor = EmailMonitor()
    print(f"Email Monitor created:")
    print(f"  - Email: {monitor.email_address}")
    print(f"  - IMAP Server: {monitor.imap_server}:{monitor.imap_port}")
    print()
    
    # Show job board patterns
    print("Configured Job Boards:")
    for domain, criteria in monitor.JOB_BOARDS.items():
        print(f"  - {domain}: {criteria['from']}")
    print()


async def demo_job_scraping():
    """Demo job scraping functionality."""
    print("=== Job Scraping Demo ===")
    print("This demo shows how the job scraping system works.")
    print()
    
    # Create job scraper
    scraper = JobScraper()
    print("Job Scraper created with domain-specific rules:")
    for domain in scraper.SCRAPING_RULES.keys():
        print(f"  - {domain}")
    print()
    
    # Show experience extraction
    test_descriptions = [
        "We are looking for a software engineer with 3+ years of experience.",
        "Minimum 2 years of professional experience required.",
        "Entry level position, no experience required."
    ]
    
    print("Experience Extraction Examples:")
    for desc in test_descriptions:
        years = scraper._extract_experience_years(desc)
        print(f"  - '{desc}' -> {years} years")
    print()


def demo_database():
    """Demo database functionality."""
    print("=== Database Demo ===")
    print("This demo shows how the database system works.")
    print()
    
    # Create database manager
    db = DatabaseManager()
    print(f"Database Manager created:")
    print(f"  - Database Path: {db.db_path}")
    print()
    
    # Show table structure
    print("Database Tables:")
    print("  - jobs: Job postings with source, company, title, URL, etc.")
    print("  - analyses: AI analysis results with match percentage, strengths, etc.")
    print("  - applications: Application tracking with status")
    print("  - processed_emails: Email tracking to prevent duplicates")
    print()


async def main():
    """Run all demos."""
    print("Job Match Automation - Demo")
    print("=" * 40)
    print()
    
    # Run email monitoring demo
    demo_email_monitoring()
    
    # Run job scraping demo
    await demo_job_scraping()
    
    # Run database demo
    demo_database()
    
    print("=== Demo Complete ===")
    print()
    print("Next steps:")
    print("1. Configure your .env file with email credentials")
    print("2. Run the email monitor with: python src/main.py --monitor")
    print("3. Check the database for stored jobs")


if __name__ == "__main__":
    asyncio.run(main())