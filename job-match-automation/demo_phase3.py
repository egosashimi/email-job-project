"""
Demo script showing how the notification system works.
"""

import sys
import os
import asyncio
import json
from datetime import datetime

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from notifications.discord_notifier import DiscordNotifier
from notifications.notification_manager import NotificationManager


async def demo_discord_notification():
    """Demo Discord notification functionality."""
    print("=== Discord Notification Demo ===")
    
    # Sample job data
    job = {
        "id": "linkedin-12345",
        "title": "Python Developer",
        "company": "TechCorp",
        "url": "https://linkedin.com/jobs/view/12345",
        "source": "linkedin",
        "salary_min": 70000,
        "salary_max": 90000,
        "location": "New York, NY",
        "remote_option": True,
        "experience_years": 2,
        "discovered_at": datetime.now().isoformat()
    }
    
    # Sample analysis data
    analysis = {
        "percentage": 75,
        "strengths": [
            "Python experience matches requirement",
            "Located in same city",
            "Salary range aligns with expectations"
        ],
        "weaknesses": [
            "Missing AWS experience",
            "No mention of Docker knowledge"
        ],
        "hidden_opportunities": [
            "AI-assisted development experience could accelerate cloud learning"
        ],
        "red_flags": [
            "Job lists 'nice to have' 5 years experience"
        ],
        "recommendation": "POSSIBLE_MATCH",
        "reasoning": "Strong fundamental match with manageable skill gaps"
    }
    
    # Test Discord notification (if webhook URL is configured)
    print("Testing Discord notification...")
    try:
        async with DiscordNotifier() as notifier:
            # Send test notification
            success = await notifier.send_test_notification()
            print(f"Test notification {'succeeded' if success else 'failed'}")
            
            # Send job match notification
            success = await notifier.send_job_match_notification(job, analysis)
            print(f"Job match notification {'succeeded' if success else 'failed'}")
    except Exception as e:
        print(f"Discord notification test failed: {e}")
        print("This is expected if Discord webhook URL is not configured")
    
    print()


async def demo_notification_manager():
    """Demo notification manager functionality."""
    print("=== Notification Manager Demo ===")
    
    # Sample job data
    job = {
        "id": "indeed-67890",
        "title": "Full Stack Developer",
        "company": "StartupXYZ",
        "url": "https://indeed.com/viewjob?jk=67890",
        "source": "indeed",
        "salary_min": 80000,
        "salary_max": 100000,
        "location": "New York, NY",
        "remote_option": False,
        "experience_years": 3,
        "discovered_at": datetime.now().isoformat()
    }
    
    # Sample analysis data
    analysis = {
        "percentage": 82,
        "strengths": [
            "Full stack experience with JavaScript and Python",
            "Located in same city",
            "Salary range aligns with expectations"
        ],
        "weaknesses": [
            "No mention of React experience",
            "Missing Kubernetes knowledge"
        ],
        "hidden_opportunities": [
            "JavaScript experience suggests you could quickly pick up React"
        ],
        "red_flags": [],
        "recommendation": "STRONG_MATCH",
        "reasoning": "Excellent match with strong alignment in skills and location"
    }
    
    # Test notification manager
    print("Testing notification manager...")
    manager = NotificationManager()
    
    # Send test notification
    success = await manager.send_test_notification()
    print(f"Test notification {'succeeded' if success else 'failed'}")
    
    # Send job match notification
    success = await manager.send_job_match_notification(job, analysis)
    print(f"Job match notification {'succeeded' if success else 'failed'}")
    
    # Show notification queue
    print(f"Notification queue size: {len(manager.notification_queue)}")
    
    print()


async def demo_fallback_notifications():
    """Demo fallback notification methods."""
    print("=== Fallback Notification Demo ===")
    
    # Sample job data (low match percentage to trigger different behavior)
    job = {
        "id": "ziprecruiter-55555",
        "title": "Senior Architect",
        "company": "BigCorp",
        "url": "https://ziprecruiter.com/job/55555",
        "source": "ziprecruiter",
        "salary_min": 150000,
        "salary_max": 200000,
        "location": "San Francisco, CA",
        "remote_option": False,
        "experience_years": 10,
        "discovered_at": datetime.now().isoformat()
    }
    
    # Sample analysis data (low match)
    analysis = {
        "percentage": 35,
        "strengths": [
            "Python experience",
            "Docker knowledge"
        ],
        "weaknesses": [
            "Requires 10 years experience",
            "Missing cloud architecture experience",
            "Location mismatch"
        ],
        "hidden_opportunities": [],
        "red_flags": [
            "Requires 10 years experience (candidate has 2)"
        ],
        "recommendation": "SKIP",
        "reasoning": "Significant experience gap and location mismatch"
    }
    
    # Test notification manager with low match (should not send notification)
    print("Testing notification for low match job (should not send)...")
    manager = NotificationManager()
    
    # Send job match notification (should not send due to low match)
    success = await manager.send_job_match_notification(job, analysis)
    print(f"Low match notification {'succeeded' if success else 'skipped (as expected)'}")
    
    # Show that no notification was queued
    print(f"Notification queue size: {len(manager.notification_queue)}")
    
    print()


async def main():
    """Run all demos."""
    print("Job Match Automation - Phase 3 Notification Demo")
    print("=" * 50)
    print()
    
    # Run Discord notification demo
    await demo_discord_notification()
    
    # Run notification manager demo
    await demo_notification_manager()
    
    # Run fallback notifications demo
    await demo_fallback_notifications()
    
    print("=== Demo Complete ===")
    print()
    print("Phase 3 notification components are working:")
    print("1. Discord notifications (when configured)")
    print("2. Notification manager with fallback mechanisms")
    print("3. Automatic filtering based on match percentage")
    print("4. Multiple fallback methods (file, console)")


if __name__ == "__main__":
    asyncio.run(main())