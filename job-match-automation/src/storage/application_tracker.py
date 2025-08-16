"""
Application tracking module for job match automation.
Handles tracking application status and history.
"""

import sqlite3
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from storage.database import DatabaseManager


class ApplicationTracker:
    """Tracks job application status and history."""

    def __init__(self):
        """Initialize application tracker."""
        self.db = DatabaseManager()

    def update_application_status(self, job_id: str, status: str, notes: str = "") -> bool:
        """Update the application status for a job."""
        valid_statuses = ["PENDING", "APPLIED", "REJECTED", "INTERVIEW", "OFFER"]
        
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")
        
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if application record exists
                cursor.execute('SELECT id FROM applications WHERE job_id = ?', (job_id,))
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing record
                    cursor.execute('''
                        UPDATE applications 
                        SET status = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE job_id = ?
                    ''', (status, notes, job_id))
                else:
                    # Create new record
                    cursor.execute('''
                        INSERT INTO applications (job_id, status, notes, applied_at)
                        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                    ''', (job_id, status, notes))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"Error updating application status: {e}")
            return False

    def get_application_status(self, job_id: str) -> Optional[str]:
        """Get the current application status for a job."""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT status FROM applications WHERE job_id = ?', (job_id,))
                row = cursor.fetchone()
                return row[0] if row else None
        except Exception as e:
            print(f"Error getting application status: {e}")
            return None

    def get_recent_applications(self, days: int = 30) -> List[Dict]:
        """Get recently updated applications."""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                # Calculate date filter
                since_date = datetime.now().replace(microsecond=0) - timedelta(days=days)
                
                cursor.execute('''
                    SELECT a.*, j.company, j.title, j.url
                    FROM applications a
                    JOIN jobs j ON a.job_id = j.id
                    WHERE a.updated_at > ?
                    ORDER BY a.updated_at DESC
                ''', (since_date.isoformat(),))
                
                columns = [description[0] for description in cursor.description]
                rows = cursor.fetchall()
                
                return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            print(f"Error getting recent applications: {e}")
            return []

    def get_application_statistics(self) -> Dict:
        """Get statistics about applications."""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                # Get total applications by status
                cursor.execute('''
                    SELECT status, COUNT(*) 
                    FROM applications 
                    GROUP BY status
                ''')
                status_counts = dict(cursor.fetchall())
                
                # Get recent applications (last 7 days)
                since_date = datetime.now().replace(microsecond=0) - timedelta(days=7)
                cursor.execute('''
                    SELECT COUNT(*) 
                    FROM applications 
                    WHERE updated_at > ?
                ''', (since_date.isoformat(),))
                recent_applications = cursor.fetchone()[0]
                
                # Get application conversion rates
                cursor.execute('SELECT COUNT(*) FROM jobs')
                total_jobs = cursor.fetchone()[0]
                
                cursor.execute('SELECT COUNT(*) FROM applications WHERE status = "APPLIED"')
                applied_jobs = cursor.fetchone()[0]
                
                conversion_rate = (applied_jobs / total_jobs * 100) if total_jobs > 0 else 0
                
                return {
                    'status_counts': status_counts,
                    'recent_applications': recent_applications,
                    'total_jobs': total_jobs,
                    'applied_jobs': applied_jobs,
                    'conversion_rate': conversion_rate
                }
        except Exception as e:
            print(f"Error getting application statistics: {e}")
            return {}

    def add_application_note(self, job_id: str, note: str) -> bool:
        """Add a note to an application."""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                # Get existing notes
                cursor.execute('SELECT notes FROM applications WHERE job_id = ?', (job_id,))
                row = cursor.fetchone()
                
                if row:
                    existing_notes = row[0] if row[0] else ""
                    updated_notes = f"{existing_notes}\n{datetime.now().strftime('%Y-%m-%d %H:%M')}: {note}"
                    
                    # Update notes
                    cursor.execute('''
                        UPDATE applications 
                        SET notes = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE job_id = ?
                    ''', (updated_notes, job_id))
                    
                    conn.commit()
                    return True
                else:
                    print(f"No application found for job_id: {job_id}")
                    return False
        except Exception as e:
            print(f"Error adding application note: {e}")
            return False


# Example usage
def main():
    """Example usage of the ApplicationTracker."""
    tracker = ApplicationTracker()
    
    # Sample job ID
    job_id = "linkedin-12345"
    
    # Update application status
    print("Updating application status...")
    success = tracker.update_application_status(job_id, "APPLIED", "Submitted resume and cover letter")
    print(f"Status update {'succeeded' if success else 'failed'}")
    
    # Get current status
    status = tracker.get_application_status(job_id)
    print(f"Current status: {status}")
    
    # Add a note
    print("\nAdding application note...")
    success = tracker.add_application_note(job_id, "Followed up via email")
    print(f"Note addition {'succeeded' if success else 'failed'}")
    
    # Get statistics
    print("\nGetting application statistics...")
    stats = tracker.get_application_statistics()
    print(f"Statistics: {stats}")
    
    # Get recent applications
    print("\nGetting recent applications...")
    recent = tracker.get_recent_applications(30)
    print(f"Found {len(recent)} recent applications")


if __name__ == "__main__":
    main()