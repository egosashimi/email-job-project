"""
Performance monitoring module for job match automation.
Monitors and optimizes system performance.
"""

import time
import sqlite3
from typing import Dict, List
from datetime import datetime, timedelta
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from storage.database import DatabaseManager


class PerformanceMonitor:
    """Monitors and optimizes system performance."""

    def __init__(self):
        """Initialize performance monitor."""
        self.db = DatabaseManager()
        self.metrics = []

    def start_timing(self, operation: str) -> Dict:
        """Start timing an operation."""
        return {
            'operation': operation,
            'start_time': time.time()
        }

    def end_timing(self, timing_data: Dict) -> Dict:
        """End timing an operation and record metrics."""
        end_time = time.time()
        
        metrics = {
            'operation': timing_data['operation'],
            'duration': end_time - timing_data['start_time'],
            'timestamp': datetime.now().isoformat()
        }
        
        self.metrics.append(metrics)
        
        # Keep only last 1000 metrics
        if len(self.metrics) > 1000:
            self.metrics = self.metrics[-1000:]
        
        return metrics

    def get_operation_performance(self, operation: str = None, hours: int = 24) -> List[Dict]:
        """Get performance metrics for operations."""
        if operation:
            # Filter metrics for specific operation
            filtered_metrics = [
                m for m in self.metrics 
                if m['operation'] == operation
            ]
        else:
            # Use all metrics
            filtered_metrics = self.metrics
        
        if not filtered_metrics:
            return []
        
        # Calculate statistics
        durations = [m['duration'] for m in filtered_metrics]
        
        return [
            {
                'operation': operation or 'all',
                'count': len(filtered_metrics),
                'avg_duration': sum(durations) / len(durations),
                'min_duration': min(durations),
                'max_duration': max(durations)
            }
        ]

    def get_database_performance(self) -> Dict:
        """Get database performance metrics."""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                # Get table sizes
                cursor.execute('''
                    SELECT name, COUNT(*) as row_count
                    FROM sqlite_master 
                    WHERE type='table'
                    GROUP BY name
                ''')
                table_counts = dict(cursor.fetchall())
                
                # Get database size
                try:
                    db_size = os.path.getsize(self.db.db_path)
                    db_size_mb = db_size / (1024 * 1024)
                except:
                    db_size_mb = 0
                
                return {
                    'table_counts': table_counts,
                    'database_size_mb': db_size_mb,
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            print(f"Error getting database performance: {e}")
            return {}

    def get_slow_operations(self, threshold_seconds: float = 5.0) -> List[Dict]:
        """Get operations that took longer than threshold."""
        slow_ops = [
            m for m in self.metrics 
            if m['duration'] > threshold_seconds
        ]
        return sorted(slow_ops, key=lambda x: x['duration'], reverse=True)

    def get_performance_report(self, hours: int = 24) -> Dict:
        """Get a comprehensive performance report."""
        return {
            'report_generated': datetime.now().isoformat(),
            'period_hours': hours,
            'database_performance': self.get_database_performance(),
            'operation_performance': self.get_operation_performance(),
            'slow_operations': self.get_slow_operations(5.0)
        }


# Example usage
def main():
    """Example usage of the PerformanceMonitor."""
    monitor = PerformanceMonitor()
    
    # Simulate some operations
    print("Simulating operations...")
    
    # Operation 1: Email monitoring
    timing = monitor.start_timing("email_monitor")
    time.sleep(0.1)  # Simulate work
    metrics = monitor.end_timing(timing)
    print(f"Email monitoring took {metrics['duration']:.3f} seconds")
    
    # Operation 2: Job scraping
    timing = monitor.start_timing("job_scraping")
    time.sleep(0.2)  # Simulate work
    metrics = monitor.end_timing(timing)
    print(f"Job scraping took {metrics['duration']:.3f} seconds")
    
    # Operation 3: AI analysis
    timing = monitor.start_timing("ai_analysis")
    time.sleep(0.5)  # Simulate work
    metrics = monitor.end_timing(timing)
    print(f"AI analysis took {metrics['duration']:.3f} seconds")
    
    # Get performance report
    print("\nGenerating performance report...")
    report = monitor.get_performance_report()
    print(f"Report generated: {report.get('report_generated')}")
    
    # Show operation performance
    operations = report.get('operation_performance', [])
    print(f"\nOperation performance data points: {len(operations)}")


if __name__ == "__main__":
    main()