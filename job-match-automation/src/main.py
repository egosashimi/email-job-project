"""
Main entry point for the job match automation system.
"""

import argparse
import logging
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from core.email_monitor import EmailMonitor
from storage.database import DatabaseManager


def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def monitor_emails():
    """Monitor emails for job postings."""
    logging.info("Starting email monitoring...")
    
    with EmailMonitor() as monitor:
        # Search for job emails from the last 24 hours
        job_emails = monitor.search_job_emails(hours_back=24)
        
        if not job_emails:
            logging.info("No job emails found.")
            return
        
        logging.info(f"Found {len(job_emails)} job emails.")
        
        # Initialize database
        db = DatabaseManager()
        
        # Process each email
        for email_data in job_emails:
            email_id = email_data['email_id']
            
            # Check if email has already been processed
            if db.is_email_processed(email_id):
                logging.info(f"Email {email_id} already processed, skipping.")
                continue
            
            logging.info(f"Processing email from {email_data['from']}")
            
            # Extract job links
            job_links = email_data['job_links']
            logging.info(f"Found {len(job_links)} job links in email.")
            
            # Store job information in database
            for job_link in job_links:
                job_data = {
                    'id': f"{email_data['source']}-{hash(job_link['url'])}",
                    'source': email_data['source'],
                    'url': job_link['url'],
                    'title': job_link['title_hint'],
                    'email_id': email_id
                }
                
                if db.store_job(job_data):
                    logging.info(f"Stored job: {job_link['title_hint']}")
                else:
                    logging.error(f"Failed to store job: {job_link['title_hint']}")
            
            # Mark email as processed
            db.mark_email_processed(email_id, len(job_links))
        
        logging.info("Email monitoring completed.")


def main():
    """Main entry point."""
    setup_logging()
    
    parser = argparse.ArgumentParser(description="Job Match Automation")
    parser.add_argument(
        "--monitor",
        action="store_true",
        help="Monitor emails for job postings"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Run a one-time email check"
    )
    
    args = parser.parse_args()
    
    if args.monitor or args.check:
        monitor_emails()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()