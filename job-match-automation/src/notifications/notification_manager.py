"""
Notification manager for job match automation.
Handles multiple notification methods with fallback mechanisms.
"""

import asyncio
import json
from typing import Dict, List
import sys
import os
from datetime import datetime

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from notifications.discord_notifier import DiscordNotifier
from core.config_manager import config


class NotificationManager:
    """Manages job match notifications with fallback mechanisms."""

    def __init__(self):
        """Initialize notification manager."""
        self.fallback_methods = [
            self._try_discord_notification,
            self._save_to_notification_queue,
            self._write_to_local_file,
            self._print_to_console
        ]
        self.notification_queue = []

    async def send_job_match_notification(self, job: Dict, analysis: Dict) -> bool:
        """Send a job match notification using available methods."""
        # Only send notifications for matches above 60%
        if analysis.get('percentage', 0) < 60:
            return True  # Not an error, just not sending notification
        
        # Try each notification method in order
        for method in self.fallback_methods:
            try:
                success = await method(job, analysis)
                if success:
                    return True
            except Exception as e:
                print(f"Notification method {method.__name__} failed: {e}")
                continue
        
        # If all methods fail, return False
        return False

    async def _try_discord_notification(self, job: Dict, analysis: Dict) -> bool:
        """Try to send notification via Discord."""
        if not config.discord_webhook_url:
            return False
        
        async with DiscordNotifier() as notifier:
            return await notifier.send_job_match_notification(job, analysis)

    async def _save_to_notification_queue(self, job: Dict, analysis: Dict) -> bool:
        """Save notification to queue for later sending."""
        notification = {
            'job': job,
            'analysis': analysis,
            'timestamp': datetime.now().isoformat(),
            'attempts': 0
        }
        self.notification_queue.append(notification)
        return True

    async def _write_to_local_file(self, job: Dict, analysis: Dict) -> bool:
        """Write notification to local file."""
        try:
            # Ensure notifications directory exists
            os.makedirs('data/notifications', exist_ok=True)
            
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/notifications/notification_{timestamp}.json"
            
            # Prepare notification data
            notification_data = {
                'timestamp': timestamp,
                'job': job,
                'analysis': analysis
            }
            
            # Write to file
            with open(filename, 'w') as f:
                json.dump(notification_data, f, indent=2)
            
            print(f"Notification saved to {filename}")
            return True
        except Exception as e:
            print(f"Error writing notification to file: {e}")
            return False

    async def _print_to_console(self, job: Dict, analysis: Dict) -> bool:
        """Print notification to console."""
        try:
            print("=" * 50)
            print("JOB MATCH NOTIFICATION")
            print("=" * 50)
            print(f"Company: {job.get('company', 'Unknown')}")
            print(f"Position: {job.get('title', 'Unknown')}")
            print(f"Match Score: {analysis.get('percentage', 0)}%")
            print(f"Recommendation: {analysis.get('recommendation', 'Unknown')}")
            print(f"URL: {job.get('url', 'Unknown')}")
            print("\nStrengths:")
            for strength in analysis.get('strengths', [])[:3]:
                print(f"  • {strength}")
            print("\nWeaknesses:")
            for weakness in analysis.get('weaknesses', [])[:3]:
                print(f"  • {weakness}")
            print("=" * 50)
            return True
        except Exception as e:
            print(f"Error printing notification to console: {e}")
            return False

    async def process_notification_queue(self) -> bool:
        """Process any queued notifications."""
        if not self.notification_queue:
            return True
        
        print(f"Processing {len(self.notification_queue)} queued notifications...")
        
        successful = 0
        for notification in self.notification_queue[:]:  # Copy to avoid modification during iteration
            job = notification['job']
            analysis = notification['analysis']
            
            # Try to send the notification
            success = await self.send_job_match_notification(job, analysis)
            if success:
                successful += 1
                self.notification_queue.remove(notification)
            else:
                # Increment attempts
                notification['attempts'] += 1
                # Remove if too many attempts
                if notification['attempts'] > 3:
                    self.notification_queue.remove(notification)
                    await self._write_to_local_file(job, analysis)  # Final fallback
        
        print(f"Successfully processed {successful} notifications")
        return successful == len(self.notification_queue)

    async def send_test_notification(self) -> bool:
        """Send a test notification to verify system is working."""
        test_job = {
            "title": "Test Position",
            "company": "Job Match Automation",
            "url": "https://example.com",
            "source": "test",
            "salary_min": 70000,
            "salary_max": 90000,
            "location": "New York, NY",
            "remote_option": True
        }
        
        test_analysis = {
            "percentage": 100,
            "strengths": ["System is working correctly"],
            "weaknesses": [],
            "hidden_opportunities": [],
            "recommendation": "STRONG_MATCH",
            "reasoning": "This is a test notification"
        }
        
        return await self.send_job_match_notification(test_job, test_analysis)


# Example usage
async def main():
    """Example usage of the NotificationManager."""
    manager = NotificationManager()
    
    # Sample job data
    job = {
        "title": "Python Developer",
        "company": "TechCorp",
        "url": "https://example.com/jobs/123",
        "source": "linkedin",
        "salary_min": 70000,
        "salary_max": 90000,
        "location": "New York, NY",
        "remote_option": True
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
        "recommendation": "POSSIBLE_MATCH",
        "reasoning": "Strong fundamental match with manageable skill gaps"
    }
    
    print("Sending test notification...")
    success = await manager.send_test_notification()
    print(f"Test notification {'succeeded' if success else 'failed'}")
    
    print("\nSending job match notification...")
    success = await manager.send_job_match_notification(job, analysis)
    print(f"Job match notification {'succeeded' if success else 'failed'}")


if __name__ == "__main__":
    asyncio.run(main())