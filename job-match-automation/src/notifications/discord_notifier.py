"""
Discord notification module for job match automation.
Handles sending job match notifications via Discord webhooks.
"""

import aiohttp
import asyncio
import json
from typing import Dict, List, Optional
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.config_manager import config


class DiscordNotifier:
    """Sends job match notifications via Discord webhooks."""

    def __init__(self):
        """Initialize Discord notifier."""
        self.webhook_url = config.discord_webhook_url
        self.session = None

    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()

    async def send_job_match_notification(self, job: Dict, analysis: Dict) -> bool:
        """Send a job match notification to Discord."""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            # Only send notifications for matches above 60%
            if analysis.get('percentage', 0) < 60:
                return True  # Not an error, just not sending notification
            
            # Create the embed
            embed = self._create_job_match_embed(job, analysis)
            
            # Prepare the payload
            payload = {
                "embeds": [embed]
            }
            
            # Send the notification
            async with self.session.post(self.webhook_url, json=payload) as response:
                if response.status in [200, 204]:
                    return True
                else:
                    print(f"Failed to send Discord notification: {response.status}")
                    return False
        except Exception as e:
            print(f"Error sending Discord notification: {e}")
            return False

    def _create_job_match_embed(self, job: Dict, analysis: Dict) -> Dict:
        """Create a Discord embed for the job match notification."""
        # Determine color based on recommendation
        recommendation = analysis.get('recommendation', 'NEEDS_MANUAL_REVIEW')
        color_map = {
            'STRONG_MATCH': 0x00ff00,  # Green
            'POSSIBLE_MATCH': 0xffff00,  # Yellow
            'REACH': 0xff8c00,  # Orange
            'SKIP': 0xff0000,  # Red
            'NEEDS_MANUAL_REVIEW': 0x808080  # Gray
        }
        color = color_map.get(recommendation, 0x808080)
        
        # Create the embed
        embed = {
            "title": f"🎯 {job.get('company', 'Unknown Company')} - {job.get('title', 'Unknown Position')}",
            "url": job.get('url', ''),
            "color": color,
            "fields": [],
            "footer": {
                "text": f"Source: {job.get('source', 'Unknown')} • Click title to view full posting"
            }
        }
        
        # Add match score
        embed["fields"].append({
            "name": "📊 Match Score",
            "value": f"{analysis.get('percentage', 0)}%",
            "inline": True
        })
        
        # Add salary if available
        salary_min = job.get('salary_min')
        salary_max = job.get('salary_max')
        if salary_min or salary_max:
            if salary_min and salary_max:
                salary_text = f"${salary_min:,}-${salary_max:,}"
            elif salary_min:
                salary_text = f"From ${salary_min:,}"
            else:
                salary_text = f"Up to ${salary_max:,}"
            embed["fields"].append({
                "name": "💰 Salary",
                "value": salary_text,
                "inline": True
            })
        
        # Add location if available
        location = job.get('location')
        remote_option = job.get('remote_option', False)
        if location or remote_option:
            if remote_option and location:
                location_text = f"{location} (Remote OK)"
            elif remote_option:
                location_text = "Remote"
            else:
                location_text = location
            embed["fields"].append({
                "name": "📍 Location",
                "value": location_text,
                "inline": True
            })
        
        # Add strengths
        strengths = analysis.get('strengths', [])
        if strengths:
            strengths_text = "\n".join([f"• {strength}" for strength in strengths[:3]])
            embed["fields"].append({
                "name": "✅ Your Strengths",
                "value": strengths_text,
                "inline": False
            })
        
        # Add weaknesses
        weaknesses = analysis.get('weaknesses', [])
        if weaknesses:
            weaknesses_text = "\n".join([f"• {weakness}" for weakness in weaknesses[:3]])
            embed["fields"].append({
                "name": "⚠️ Gaps to Address",
                "value": weaknesses_text,
                "inline": False
            })
        
        # Add hidden opportunities
        opportunities = analysis.get('hidden_opportunities', [])
        if opportunities:
            opportunities_text = "\n".join([f"• {opportunity}" for opportunity in opportunities[:2]])
            embed["fields"].append({
                "name": "💡 Hidden Opportunity",
                "value": opportunities_text,
                "inline": False
            })
        
        # Add recommendation
        recommendation_text = {
            'STRONG_MATCH': "**STRONG MATCH** - Highly recommended to apply",
            'POSSIBLE_MATCH': "**POSSIBLE MATCH** - Worth applying with tailored resume",
            'REACH': "**REACH** - May require additional skill development",
            'SKIP': "**SKIP** - Not recommended to apply at this time",
            'NEEDS_MANUAL_REVIEW': "**NEEDS REVIEW** - Manual evaluation recommended"
        }.get(recommendation, f"**{recommendation}**")
        
        embed["fields"].append({
            "name": "🎯 Recommendation",
            "value": recommendation_text,
            "inline": False
        })
        
        return embed

    async def send_test_notification(self) -> bool:
        """Send a test notification to verify webhook is working."""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            payload = {
                "content": "Job Match Automation - Test Notification",
                "embeds": [{
                    "title": "✅ Test Notification",
                    "description": "Discord webhook is working correctly!",
                    "color": 0x00ff00
                }]
            }
            
            async with self.session.post(self.webhook_url, json=payload) as response:
                return response.status in [200, 204]
        except Exception as e:
            print(f"Error sending test notification: {e}")
            return False


# Example usage
async def main():
    """Example usage of the DiscordNotifier."""
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
    
    async with DiscordNotifier() as notifier:
        print("Sending test notification...")
        success = await notifier.send_test_notification()
        print(f"Test notification {'succeeded' if success else 'failed'}")
        
        print("\nSending job match notification...")
        success = await notifier.send_job_match_notification(job, analysis)
        print(f"Job match notification {'succeeded' if success else 'failed'}")


if __name__ == "__main__":
    asyncio.run(main())