"""
Email scheduler module for job match automation.
Schedules and manages periodic email checks.
"""

import asyncio
import threading
from typing import Dict, List, Callable
from datetime import datetime, timedelta
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.email_monitor import EmailMonitor
from storage.database import DatabaseManager


class EmailScheduler:
    """Schedules and manages periodic email checks."""

    def __init__(self):
        """Initialize email scheduler."""
        self.db = DatabaseManager()
        self.jobs = {}
        self.running = False
        self.scheduler_thread = None

    def add_job(self, name: str, interval_minutes: int, job_function: Callable, 
                job_boards: List[str] = None) -> bool:
        """Add a scheduled job."""
        self.jobs[name] = {
            'interval_minutes': interval_minutes,
            'job_function': job_function,
            'job_boards': job_boards or [],
            'last_run': None,
            'next_run': datetime.now() + timedelta(minutes=interval_minutes)
        }
        return True

    def remove_job(self, name: str) -> bool:
        """Remove a scheduled job."""
        if name in self.jobs:
            del self.jobs[name]
            return True
        return False

    def get_job_status(self, name: str) -> Dict:
        """Get status of a scheduled job."""
        if name in self.jobs:
            job = self.jobs[name]
            return {
                'name': name,
                'interval_minutes': job['interval_minutes'],
                'last_run': job['last_run'].isoformat() if job['last_run'] else None,
                'next_run': job['next_run'].isoformat(),
                'running': self.running
            }
        return None

    def get_all_jobs_status(self) -> List[Dict]:
        """Get status of all scheduled jobs."""
        return [self.get_job_status(name) for name in self.jobs]

    def start(self):
        """Start the scheduler."""
        if self.running:
            return False
        
        self.running = True
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        return True

    def stop(self):
        """Stop the scheduler."""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5.0)
        return True

    def _run_scheduler(self):
        """Run the scheduler loop."""
        while self.running:
            try:
                current_time = datetime.now()
                
                # Check each job
                for name, job in self.jobs.items():
                    if current_time >= job['next_run']:
                        # Run the job
                        try:
                            job['last_run'] = current_time
                            job['next_run'] = current_time + timedelta(minutes=job['interval_minutes'])
                            
                            # Run the job function
                            if asyncio.iscoroutinefunction(job['job_function']):
                                # Handle async functions
                                asyncio.run(job['job_function'](job['job_boards']))
                            else:
                                # Handle sync functions
                                job['job_function'](job['job_boards'])
                        except Exception as e:
                            print(f"Error running job {name}: {e}")
                
                # Sleep for a short time to avoid busy waiting
                time.sleep(60)  # Check every minute
            except Exception as e:
                print(f"Error in scheduler loop: {e}")
                time.sleep(60)

    async def check_email_job(self, job_boards: List[str] = None):
        """Job function to check emails."""
        print(f"Checking emails for job boards: {job_boards or 'all'}")
        
        try:
            with EmailMonitor() as monitor:
                # Search for job emails from the last 24 hours
                job_emails = monitor.search_job_emails(hours_back=24)
                
                if not job_emails:
                    print("No job emails found.")
                    return {
                        "emails_processed": 0,
                        "new_jobs_found": 0,
                        "errors": 0
                    }
                
                print(f"Found {len(job_emails)} job emails.")
                
                # Process each email
                processed_count = 0
                job_count = 0
                error_count = 0
                
                # For now, we'll just log the processing
                # In a real implementation, you would process the emails and extract jobs
                
                return {
                    "emails_processed": len(job_emails),
                    "new_jobs_found": job_count,
                    "errors": error_count
                }
        except Exception as e:
            print(f"Error checking emails: {e}")
            return {
                "emails_processed": 0,
                "new_jobs_found": 0,
                "errors": 1
            }

    def set_job_interval(self, name: str, interval_minutes: int) -> bool:
        """Set the interval for a scheduled job."""
        if name in self.jobs:
            self.jobs[name]['interval_minutes'] = interval_minutes
            # Update next run time based on new interval
            if self.jobs[name]['last_run']:
                self.jobs[name]['next_run'] = self.jobs[name]['last_run'] + timedelta(minutes=interval_minutes)
            else:
                self.jobs[name]['next_run'] = datetime.now() + timedelta(minutes=interval_minutes)
            return True
        return False


# Import time module
import time


# Example usage
def main():
    """Example usage of the EmailScheduler."""
    scheduler = EmailScheduler()
    
    # Add a job to check emails every 60 minutes
    scheduler.add_job("email_check", 60, scheduler.check_email_job)
    
    # Get job status
    print("Job status:")
    status = scheduler.get_job_status("email_check")
    print(f"  Name: {status['name']}")
    print(f"  Interval: {status['interval_minutes']} minutes")
    print(f"  Next run: {status['next_run']}")
    
    # Start scheduler
    print("\nStarting scheduler...")
    scheduler.start()
    print("Scheduler started")
    
    # Wait a moment to see it running
    time.sleep(2)
    
    # Stop scheduler
    print("\nStopping scheduler...")
    scheduler.stop()
    print("Scheduler stopped")


if __name__ == "__main__":
    main()