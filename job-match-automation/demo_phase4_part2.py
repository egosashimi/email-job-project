"""
Demo script showing how the analytics and performance monitoring work.
"""

import sys
import os
import time

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from analysis.analytics import JobMatchAnalytics
from core.performance_monitor import PerformanceMonitor


def demo_analytics():
    """Demo analytics functionality."""
    print("=== Analytics Demo ===")
    
    analytics = JobMatchAnalytics()
    
    # Generate comprehensive report
    print("Generating comprehensive analytics report...")
    report = analytics.get_comprehensive_report(30)
    print(f"  Report generated: {report.get('report_generated')}")
    
    # Show match trends
    trends = report.get('match_trends', {})
    daily_trends = trends.get('daily_trends', [])
    print(f"  Daily trends data points: {len(daily_trends)}")
    
    # Show conversion rates
    conversion = report.get('conversion_rates', {})
    print(f"  Application conversion rate: {conversion.get('application_rate', 0):.2f}%")
    
    # Show salary analysis
    salary = report.get('salary_analysis', {})
    print(f"  Average salary: ${salary.get('average_salary', 0):,.0f}")
    
    # Show skill demand
    skills = report.get('skill_demand', [])
    print(f"  Top skills in demand: {len(skills)}")
    for skill in skills[:3]:
        print(f"    {skill['skill']}: {skill['count']} mentions ({skill['percentage']:.1f}%)")
    
    print()


def demo_performance_monitoring():
    """Demo performance monitoring functionality."""
    print("=== Performance Monitoring Demo ===")
    
    monitor = PerformanceMonitor()
    
    # Simulate some operations
    print("Simulating operations...")
    
    # Operation 1: Email monitoring
    timing = monitor.start_timing("email_monitor")
    time.sleep(0.05)  # Simulate work
    metrics = monitor.end_timing(timing)
    print(f"  Email monitoring took {metrics['duration']:.3f} seconds")
    
    # Operation 2: Job scraping
    timing = monitor.start_timing("job_scraping")
    time.sleep(0.1)  # Simulate work
    metrics = monitor.end_timing(timing)
    print(f"  Job scraping took {metrics['duration']:.3f} seconds")
    
    # Operation 3: AI analysis
    timing = monitor.start_timing("ai_analysis")
    time.sleep(0.2)  # Simulate work
    metrics = monitor.end_timing(timing)
    print(f"  AI analysis took {metrics['duration']:.3f} seconds")
    
    # Get operation performance
    print("\nGetting operation performance...")
    operations = monitor.get_operation_performance()
    print(f"  Performance data points: {len(operations)}")
    for op in operations[:2]:
        print(f"    {op.get('operation', 'unknown')}: {op.get('avg_duration', 0):.3f}s avg")
    
    # Get database performance
    print("\nGetting database performance...")
    db_perf = monitor.get_database_performance()
    print(f"  Database size: {db_perf.get('database_size_mb', 0):.2f} MB")
    table_counts = db_perf.get('table_counts', {})
    print(f"  Tables: {len(table_counts)}")
    for table, count in list(table_counts.items())[:3]:
        print(f"    {table}: {count} rows")
    
    print()


def main():
    """Run all demos."""
    print("Job Match Automation - Phase 4 Analytics & Performance Demo")
    print("=" * 55)
    print()
    
    # Run analytics demo
    demo_analytics()
    
    # Run performance monitoring demo
    demo_performance_monitoring()
    
    print("=== Demo Complete ===")
    print()
    print("Phase 4 components are working:")
    print("1. Advanced analytics and reporting")
    print("2. Performance monitoring and optimization")
    print("3. Database performance tracking")
    print("4. Operation performance analysis")


if __name__ == "__main__":
    main()