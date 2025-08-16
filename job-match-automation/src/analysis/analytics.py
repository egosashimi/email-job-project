"""
Analytics module for job match automation.
Provides advanced analytics and statistics.
"""

import sqlite3
from typing import Dict, List
from datetime import datetime, timedelta
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from storage.database import DatabaseManager


class JobMatchAnalytics:
    """Advanced analytics for job match automation."""

    def __init__(self):
        """Initialize analytics module."""
        self.db = DatabaseManager()

    def get_match_trends(self, days: int = 30) -> Dict:
        """Get match trends over time."""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                # Calculate date ranges
                end_date = datetime.now()
                start_date = end_date - timedelta(days=days)
                
                # Get daily match counts
                cursor.execute('''
                    SELECT 
                        DATE(j.discovered_at) as date,
                        COUNT(*) as total_jobs,
                        AVG(a.match_percentage) as avg_match_percentage
                    FROM jobs j
                    LEFT JOIN analyses a ON j.id = a.job_id
                    WHERE j.discovered_at BETWEEN ? AND ?
                    GROUP BY DATE(j.discovered_at)
                    ORDER BY date
                ''', (start_date.isoformat(), end_date.isoformat()))
                
                daily_data = cursor.fetchall()
                
                # Get recommendation distribution over time
                cursor.execute('''
                    SELECT 
                        DATE(j.discovered_at) as date,
                        a.recommendation,
                        COUNT(*) as count
                    FROM jobs j
                    JOIN analyses a ON j.id = a.job_id
                    WHERE j.discovered_at BETWEEN ? AND ?
                    GROUP BY DATE(j.discovered_at), a.recommendation
                    ORDER BY date, a.recommendation
                ''', (start_date.isoformat(), end_date.isoformat()))
                
                recommendation_data = cursor.fetchall()
                
                return {
                    'daily_trends': [
                        {
                            'date': row[0],
                            'total_jobs': row[1],
                            'avg_match_percentage': row[2] or 0
                        }
                        for row in daily_data
                    ],
                    'recommendation_trends': [
                        {
                            'date': row[0],
                            'recommendation': row[1],
                            'count': row[2]
                        }
                        for row in recommendation_data
                    ]
                }
        except Exception as e:
            print(f"Error getting match trends: {e}")
            return {}

    def get_application_conversion_rates(self) -> Dict:
        """Get application conversion rates."""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                # Get total jobs analyzed
                cursor.execute('SELECT COUNT(*) FROM analyses')
                total_analyzed = cursor.fetchone()[0]
                
                # Get jobs with applications
                cursor.execute('''
                    SELECT COUNT(*) 
                    FROM analyses a
                    JOIN applications ap ON a.job_id = ap.job_id
                ''')
                with_applications = cursor.fetchone()[0]
                
                # Get application outcomes
                cursor.execute('''
                    SELECT ap.status, COUNT(*) 
                    FROM applications ap
                    GROUP BY ap.status
                ''')
                status_counts = dict(cursor.fetchall())
                
                # Calculate conversion rates
                application_rate = (with_applications / total_analyzed * 100) if total_analyzed > 0 else 0
                
                return {
                    'total_analyzed': total_analyzed,
                    'with_applications': with_applications,
                    'application_rate': application_rate,
                    'status_distribution': status_counts
                }
        except Exception as e:
            print(f"Error getting application conversion rates: {e}")
            return {}

    def get_salary_analysis(self, days: int = 90) -> Dict:
        """Get salary analysis for job matches."""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                # Calculate date filter
                since_date = datetime.now() - timedelta(days=days)
                
                # Get salary statistics for matches
                cursor.execute('''
                    SELECT 
                        AVG(j.salary_min) as avg_min_salary,
                        AVG(j.salary_max) as avg_max_salary,
                        MIN(j.salary_min) as min_salary,
                        MAX(j.salary_max) as max_salary,
                        COUNT(*) as job_count
                    FROM jobs j
                    JOIN analyses a ON j.id = a.job_id
                    WHERE j.salary_min IS NOT NULL 
                    AND j.salary_max IS NOT NULL
                    AND j.discovered_at > ?
                ''', (since_date.isoformat(),))
                
                row = cursor.fetchone()
                
                if row:
                    avg_min, avg_max, min_sal, max_sal, count = row
                    avg_salary = (avg_min + avg_max) / 2 if avg_min and avg_max else 0
                    
                    return {
                        'average_salary': avg_salary,
                        'salary_range': {
                            'min': min_sal,
                            'max': max_sal
                        },
                        'job_count': count,
                        'average_min_salary': avg_min or 0,
                        'average_max_salary': avg_max or 0
                    }
                else:
                    return {
                        'average_salary': 0,
                        'salary_range': {'min': 0, 'max': 0},
                        'job_count': 0,
                        'average_min_salary': 0,
                        'average_max_salary': 0
                    }
        except Exception as e:
            print(f"Error getting salary analysis: {e}")
            return {}

    def get_skill_demand_analysis(self, days: int = 90) -> List[Dict]:
        """Get analysis of skill demand in job postings."""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                # Calculate date filter
                since_date = datetime.now() - timedelta(days=days)
                
                # Get jobs with requirements
                cursor.execute('''
                    SELECT j.requirements
                    FROM jobs j
                    WHERE j.requirements IS NOT NULL
                    AND j.discovered_at > ?
                ''', (since_date.isoformat(),))
                
                rows = cursor.fetchall()
                
                # Count skill mentions
                skill_counts = {}
                for row in rows:
                    requirements = row[0].lower()
                    # Simple skill extraction (in a real implementation, you'd use NLP)
                    common_skills = [
                        'python', 'javascript', 'java', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin',
                        'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring', 'rails',
                        'sql', 'postgresql', 'mysql', 'mongodb', 'redis', 'docker', 'kubernetes',
                        'aws', 'azure', 'gcp', 'ci/cd', 'git', 'linux', 'windows', 'macos'
                    ]
                    
                    for skill in common_skills:
                        if skill in requirements:
                            skill_counts[skill] = skill_counts.get(skill, 0) + 1
                
                # Sort by count and return top skills
                sorted_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)
                
                return [
                    {
                        'skill': skill,
                        'count': count,
                        'percentage': (count / len(rows) * 100) if rows else 0
                    }
                    for skill, count in sorted_skills[:20]
                ]
        except Exception as e:
            print(f"Error getting skill demand analysis: {e}")
            return []

    def get_comprehensive_report(self, days: int = 30) -> Dict:
        """Get a comprehensive analytics report."""
        return {
            'report_generated': datetime.now().isoformat(),
            'period_days': days,
            'match_trends': self.get_match_trends(days),
            'conversion_rates': self.get_application_conversion_rates(),
            'salary_analysis': self.get_salary_analysis(days),
            'skill_demand': self.get_skill_demand_analysis(days)
        }


# Example usage
def main():
    """Example usage of the JobMatchAnalytics."""
    analytics = JobMatchAnalytics()
    
    # Get comprehensive report
    print("Generating comprehensive analytics report...")
    report = analytics.get_comprehensive_report(30)
    print(f"Report generated: {report.get('report_generated')}")
    print(f"Period: {report.get('period_days')} days")
    
    # Show match trends
    trends = report.get('match_trends', {})
    daily_trends = trends.get('daily_trends', [])
    print(f"\nDaily trends data points: {len(daily_trends)}")
    
    # Show conversion rates
    conversion = report.get('conversion_rates', {})
    print(f"\nApplication conversion rate: {conversion.get('application_rate', 0):.2f}%")
    
    # Show salary analysis
    salary = report.get('salary_analysis', {})
    print(f"\nAverage salary: ${salary.get('average_salary', 0):,.0f}")
    
    # Show skill demand
    skills = report.get('skill_demand', [])
    print(f"\nTop skills in demand: {len(skills)}")
    for skill in skills[:5]:
        print(f"  {skill['skill']}: {skill['count']} mentions ({skill['percentage']:.1f}%)")

if __name__ == "__main__":
    main()