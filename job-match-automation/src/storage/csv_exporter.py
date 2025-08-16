"""
CSV export module for job match automation.
Handles exporting job matches to CSV format.
"""

import csv
import sqlite3
from typing import List, Dict
from datetime import datetime, timedelta
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from storage.database import DatabaseManager


class CSVExporter:
    """Exports job matches to CSV format."""

    def __init__(self):
        """Initialize CSV exporter."""
        self.db = DatabaseManager()

    def export_matches(self, start_date: str = None, end_date: str = None, 
                      min_percentage: int = 0, filepath: str = None) -> str:
        """Export job matches to CSV file."""
        try:
            # Set default dates if not provided
            if not end_date:
                end_date = datetime.now().strftime("%Y-%m-%d")
            
            if not start_date:
                # Default to 30 days ago
                start_date_obj = datetime.now() - timedelta(days=30)
                start_date = start_date_obj.strftime("%Y-%m-%d")
            
            # Set default filepath if not provided
            if not filepath:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filepath = f"data/exports/jobs_{timestamp}.csv"
            
            # Ensure exports directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Query database for matches
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                query = '''
                    SELECT 
                        j.id,
                        j.company,
                        j.title,
                        j.url,
                        a.match_percentage,
                        a.recommendation,
                        j.salary_min,
                        j.salary_max,
                        j.location,
                        j.remote_option,
                        j.discovered_at,
                        ap.status
                    FROM jobs j
                    LEFT JOIN analyses a ON j.id = a.job_id
                    LEFT JOIN applications ap ON j.id = ap.job_id
                    WHERE j.discovered_at BETWEEN ? AND ?
                '''
                params = [start_date, f"{end_date} 23:59:59"]
                
                if min_percentage > 0:
                    query += ' AND a.match_percentage >= ?'
                    params.append(min_percentage)
                
                query += ' ORDER BY j.discovered_at DESC'
                
                cursor.execute(query, params)
                columns = [description[0] for description in cursor.description]
                rows = cursor.fetchall()
                
                # Write to CSV
                with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Write header
                    writer.writerow(columns)
                    
                    # Write rows
                    writer.writerows(rows)
                
                # Return file information
                file_size = os.path.getsize(filepath)
                record_count = len(rows)
                
                return {
                    "filepath": filepath,
                    "record_count": record_count,
                    "file_size_kb": round(file_size / 1024, 2)
                }
        except Exception as e:
            print(f"Error exporting matches to CSV: {e}")
            raise

    def export_application_history(self, filepath: str = None) -> str:
        """Export application history to CSV file."""
        try:
            # Set default filepath if not provided
            if not filepath:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filepath = f"data/exports/applications_{timestamp}.csv"
            
            # Ensure exports directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Query database for application history
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                query = '''
                    SELECT 
                        a.job_id,
                        j.company,
                        j.title,
                        j.url,
                        a.status,
                        a.applied_at,
                        a.updated_at,
                        a.notes
                    FROM applications a
                    JOIN jobs j ON a.job_id = j.id
                    ORDER BY a.updated_at DESC
                '''
                
                cursor.execute(query)
                columns = [description[0] for description in cursor.description]
                rows = cursor.fetchall()
                
                # Write to CSV
                with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Write header
                    writer.writerow(columns)
                    
                    # Write rows
                    writer.writerows(rows)
                
                # Return file information
                file_size = os.path.getsize(filepath)
                record_count = len(rows)
                
                return {
                    "filepath": filepath,
                    "record_count": record_count,
                    "file_size_kb": round(file_size / 1024, 2)
                }
        except Exception as e:
            print(f"Error exporting application history to CSV: {e}")
            raise

    def get_export_summary(self, days: int = 30) -> Dict:
        """Get summary of export data."""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                # Calculate date filter
                since_date = datetime.now() - timedelta(days=days)
                
                # Get total jobs in period
                cursor.execute('''
                    SELECT COUNT(*) 
                    FROM jobs 
                    WHERE discovered_at > ?
                ''', (since_date.isoformat(),))
                total_jobs = cursor.fetchone()[0]
                
                # Get jobs with analysis
                cursor.execute('''
                    SELECT COUNT(*) 
                    FROM jobs j
                    JOIN analyses a ON j.id = a.job_id
                    WHERE j.discovered_at > ?
                ''', (since_date.isoformat(),))
                analyzed_jobs = cursor.fetchone()[0]
                
                # Get jobs with applications
                cursor.execute('''
                    SELECT COUNT(*) 
                    FROM jobs j
                    JOIN applications a ON j.id = a.job_id
                    WHERE j.discovered_at > ?
                ''', (since_date.isoformat(),))
                applied_jobs = cursor.fetchone()[0]
                
                # Get match distribution
                cursor.execute('''
                    SELECT a.recommendation, COUNT(*) 
                    FROM analyses a
                    JOIN jobs j ON a.job_id = j.id
                    WHERE j.discovered_at > ?
                    GROUP BY a.recommendation
                ''', (since_date.isoformat(),))
                match_distribution = dict(cursor.fetchall())
                
                return {
                    'total_jobs': total_jobs,
                    'analyzed_jobs': analyzed_jobs,
                    'applied_jobs': applied_jobs,
                    'match_distribution': match_distribution,
                    'period_days': days
                }
        except Exception as e:
            print(f"Error getting export summary: {e}")
            return {}


# Example usage
def main():
    """Example usage of the CSVExporter."""
    exporter = CSVExporter()
    
    # Get export summary
    print("Getting export summary...")
    summary = exporter.get_export_summary(30)
    print(f"Summary: {summary}")
    
    # Export matches
    print("\nExporting job matches...")
    try:
        result = exporter.export_matches(min_percentage=60)
        print(f"Export completed: {result}")
    except Exception as e:
        print(f"Export failed: {e}")
    
    # Export application history
    print("\nExporting application history...")
    try:
        result = exporter.export_application_history()
        print(f"Export completed: {result}")
    except Exception as e:
        print(f"Export failed: {e}")


if __name__ == "__main__":
    main()