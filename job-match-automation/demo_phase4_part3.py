"""
Demo script showing how the email scheduler works.
"""

import sys
import os
import time

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.email_scheduler import EmailScheduler


def demo_email_scheduler():
    """Demo email scheduler functionality."""
    print("=== Email Scheduler Demo ===")
    
    scheduler = EmailScheduler()
    
    # Add jobs
    print("Adding scheduled jobs...")
    scheduler.add_job("linkedin_check", 30, scheduler.check_email_job, ["linkedin.com"])
    scheduler.add_job("indeed_check", 60, scheduler.check_email_job, ["indeed.com"])
    scheduler.add_job("general_check", 120, scheduler.check_email_job)
    
    # Show job status
    print("\nJob status:")
    jobs_status = scheduler.get_all_jobs_status()
    for job in jobs_status:
        print(f"  {job['name']}:")
        print(f"    Interval: {job['interval_minutes']} minutes")
        print(f"    Next run: {job['next_run']}")
        print(f"    Running: {job['running']}")
    
    # Start scheduler
    print("\nStarting scheduler...")
    scheduler.start()
    print("[SUCCESS] Scheduler started")
    
    # Wait a moment to see it running
    print("Scheduler is now running in the background...")
    time.sleep(3)
    
    # Show job status after starting
    print("\nJob status after starting:")
    jobs_status = scheduler.get_all_jobs_status()
    for job in jobs_status:
        print(f"  {job['name']}: Next run at {job['next_run']}")
    
    # Stop scheduler
    print("\nStopping scheduler...")
    scheduler.stop()
    print("[SUCCESS] Scheduler stopped")
    
    # Show final job status
    print("\nFinal job status:")
    jobs_status = scheduler.get_all_jobs_status()
    for job in jobs_status:
        print(f"  {job['name']}: Stopped")
    
    print()


def main():
    """Run all demos."""
    print("Job Match Automation - Phase 4 Email Scheduler Demo")
    print("=" * 50)
    print()
    
    # Run email scheduler demo
    demo_email_scheduler()
    
    print("=== Demo Complete ===")
    print()
    print("Phase 4 email scheduler components are working:")
    print("1. Job scheduling with configurable intervals")
    print("2. Multiple job board specific checks")
    print("3. Background scheduler with start/stop control")
    print("4. Job status monitoring")


if __name__ == "__main__":
    main()