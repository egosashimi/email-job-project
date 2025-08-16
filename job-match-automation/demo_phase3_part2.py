"""
Demo script showing how the application tracking and CSV export work.
"""

import sys
import os
from datetime import datetime

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from storage.application_tracker import ApplicationTracker
from storage.csv_exporter import CSVExporter


def demo_application_tracking():
    """Demo application tracking functionality."""
    print("=== Application Tracking Demo ===")
    
    tracker = ApplicationTracker()
    
    # Sample job IDs
    job_ids = [
        "linkedin-12345",
        "indeed-67890",
        "ziprecruiter-55555"
    ]
    
    # Update application statuses
    print("Updating application statuses...")
    statuses = ["APPLIED", "INTERVIEW", "REJECTED"]
    notes = [
        "Submitted resume and cover letter",
        "Technical interview scheduled for next week",
        "Not enough experience with required technologies"
    ]
    
    for i, job_id in enumerate(job_ids):
        success = tracker.update_application_status(job_id, statuses[i], notes[i])
        print(f"  {job_id}: {'Success' if success else 'Failed'}")
    
    # Add notes to applications
    print("\nAdding additional notes...")
    for job_id in job_ids:
        success = tracker.add_application_note(job_id, f"Followed up on {datetime.now().strftime('%Y-%m-%d')}")
        print(f"  {job_id}: {'Success' if success else 'Failed'}")
    
    # Get current statuses
    print("\nCurrent application statuses:")
    for job_id in job_ids:
        status = tracker.get_application_status(job_id)
        print(f"  {job_id}: {status}")
    
    # Get statistics
    print("\nApplication statistics:")
    stats = tracker.get_application_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print()


def demo_csv_export():
    """Demo CSV export functionality."""
    print("=== CSV Export Demo ===")
    
    exporter = CSVExporter()
    
    # Get export summary
    print("Getting export summary...")
    summary = exporter.get_export_summary(30)
    print(f"  Period: {summary.get('period_days', 0)} days")
    print(f"  Total jobs: {summary.get('total_jobs', 0)}")
    print(f"  Analyzed jobs: {summary.get('analyzed_jobs', 0)}")
    print(f"  Applied jobs: {summary.get('applied_jobs', 0)}")
    
    # Show match distribution
    match_dist = summary.get('match_distribution', {})
    if match_dist:
        print("  Match distribution:")
        for recommendation, count in match_dist.items():
            print(f"    {recommendation}: {count}")
    
    # Export job matches
    print("\nExporting job matches...")
    try:
        result = exporter.export_matches(min_percentage=60)
        print(f"  Export completed:")
        print(f"    File: {result['filepath']}")
        print(f"    Records: {result['record_count']}")
        print(f"    Size: {result['file_size_kb']} KB")
    except Exception as e:
        print(f"  Export failed: {e}")
    
    # Export application history
    print("\nExporting application history...")
    try:
        result = exporter.export_application_history()
        print(f"  Export completed:")
        print(f"    File: {result['filepath']}")
        print(f"    Records: {result['record_count']}")
        print(f"    Size: {result['file_size_kb']} KB")
    except Exception as e:
        print(f"  Export failed: {e}")
    
    print()


def main():
    """Run all demos."""
    print("Job Match Automation - Phase 3 Application Tracking & Export Demo")
    print("=" * 65)
    print()
    
    # Run application tracking demo
    demo_application_tracking()
    
    # Run CSV export demo
    demo_csv_export()
    
    print("=== Demo Complete ===")
    print()
    print("Phase 3 components are working:")
    print("1. Application status tracking")
    print("2. Application notes and history")
    print("3. Application statistics")
    print("4. CSV export of job matches")
    print("5. CSV export of application history")


if __name__ == "__main__":
    main()