"""
Email monitoring system for job match automation.
Handles IMAP connection, email searching, and job link extraction.
"""

import imaplib
import email
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import re
import logging
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.config_manager import config


class EmailMonitor:
    """Monitors Gmail for job emails from specified job boards."""

    JOB_BOARDS = {
        'linkedin.com': {
            'from': 'jobs-noreply@linkedin.com',
            'subject_patterns': ['job alert', 'new jobs']
        },
        'indeed.com': {
            'from': 'noreply@indeed.com',
            'subject_patterns': ['job alert', 'new positions']
        },
        'ziprecruiter.com': {
            'from': 'no-reply@ziprecruiter.com',
            'subject_patterns': ['new jobs', 'job matches']
        },
        'ycombinator.com': {
            'from': 'jobs@ycombinator.com',
            'subject_patterns': ['work at a startup']
        },
        'startup.jobs': {
            'from': 'notifications@startup.jobs',
            'subject_patterns': ['new opportunities']
        }
    }

    def __init__(self):
        """Initialize email monitor with configuration."""
        self.email_address = config.email_address
        self.email_password = config.email_password
        self.imap_server = config.email_imap_server
        self.imap_port = config.email_imap_port
        self.imap = None
        self.logger = logging.getLogger(__name__)

    def connect(self) -> bool:
        """Connect to the IMAP server."""
        try:
            self.imap = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            self.imap.login(self.email_address, self.email_password)
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect to IMAP server: {e}")
            return False

    def disconnect(self):
        """Disconnect from the IMAP server."""
        if self.imap:
            try:
                self.imap.close()
                self.imap.logout()
            except Exception as e:
                self.logger.error(f"Error disconnecting from IMAP server: {e}")

    def search_job_emails(self, hours_back: int = 24) -> List[Dict]:
        """Search for job emails from the last N hours."""
        if not self.imap:
            if not self.connect():
                return []

        try:
            # Select the inbox
            self.imap.select('INBOX')
            
            # Calculate date for searching
            date_since = (datetime.now() - timedelta(hours=hours_back)).strftime("%d-%b-%Y")
            
            # Search for emails from job boards
            job_emails = []
            for domain, criteria in self.JOB_BOARDS.items():
                # Search for emails from specific sender
                search_criteria = f'(FROM "{criteria["from"]}" SINCE {date_since})'
                status, messages = self.imap.search(None, search_criteria)
                
                if status == 'OK':
                    email_ids = messages[0].split()
                    for email_id in email_ids:
                        email_data = self._fetch_email(email_id)
                        if email_data:
                            email_data['source'] = domain
                            job_emails.append(email_data)
            
            return job_emails
        except Exception as e:
            self.logger.error(f"Error searching for job emails: {e}")
            return []

    def _fetch_email(self, email_id: bytes) -> Optional[Dict]:
        """Fetch and parse a specific email."""
        try:
            # Fetch the email
            status, msg_data = self.imap.fetch(email_id, '(RFC822)')
            
            if status != 'OK':
                return None
            
            # Parse the email
            email_body = msg_data[0][1]
            email_message = email.message_from_bytes(email_body)
            
            # Extract relevant information
            subject = email_message.get('Subject', '')
            sender = email_message.get('From', '')
            date = email_message.get('Date', '')
            
            # Get email body
            body = self._get_email_body(email_message)
            
            # Extract job links
            job_links = self._extract_job_links(body, sender)
            
            return {
                'email_id': email_id.decode(),
                'subject': subject,
                'from': sender,
                'date': date,
                'body': body,
                'job_links': job_links
            }
        except Exception as e:
            self.logger.error(f"Error fetching email {email_id}: {e}")
            return None

    def _get_email_body(self, email_message) -> str:
        """Extract the body text from an email message."""
        body = ""
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/html":
                    body = part.get_payload(decode=True).decode('utf-8')
                    break
                elif part.get_content_type() == "text/plain" and not body:
                    body = part.get_payload(decode=True).decode('utf-8')
        else:
            body = email_message.get_payload(decode=True).decode('utf-8')
        
        return body

    def _extract_job_links(self, html_body: str, sender: str) -> List[Dict]:
        """Extract job links from email body."""
        links = []
        
        # Extract all href links
        href_pattern = r'href=[\'"]([^\'"]*)[\'"]'
        href_matches = re.findall(href_pattern, html_body, re.IGNORECASE)
        
        # Filter for job-related links
        for match in href_matches:
            # Check if it's a job link based on sender and URL
            if self._is_job_link(match, sender):
                # Try to extract job title from surrounding text
                title = self._extract_title_near_link(html_body, match)
                links.append({
                    'url': match,
                    'title_hint': title
                })
        
        return links

    def _is_job_link(self, url: str, sender: str) -> bool:
        """Determine if a URL is likely a job link based on sender and URL patterns."""
        # Check if URL contains job-related paths
        job_indicators = ['/jobs/', '/job/', '/viewjob', '/jobview']
        return any(indicator in url.lower() for indicator in job_indicators)

    def _extract_title_near_link(self, html_body: str, url: str) -> str:
        """Attempt to extract job title from text near the link."""
        # This is a simplified approach - in practice, you might want more sophisticated parsing
        # Find text near the URL in the HTML
        url_index = html_body.find(url)
        if url_index != -1:
            # Look for text before the URL (within 200 characters)
            start = max(0, url_index - 200)
            text_before = html_body[start:url_index]
            
            # Try to find text that looks like a job title
            # This is a very basic approach - you'd want more sophisticated parsing
            lines = text_before.split('\n')
            for line in reversed(lines):
                # Look for lines that aren't HTML tags and aren't too short
                clean_line = re.sub(r'<[^>]+>', '', line).strip()
                if len(clean_line) > 10 and len(clean_line) < 100:
                    return clean_line[:50] + "..." if len(clean_line) > 50 else clean_line
        
        return "Job Posting"

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()