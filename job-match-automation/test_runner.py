"""
Test runner for job match automation.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_all_components():
    """Test all components of the job match automation system."""
    print("Job Match Automation - Test Runner")
    print("=" * 35)
    print()
    
    # Test results tracking
    passed = 0
    failed = 0
    total = 0
    
    # Test ConfigManager
    print("1. Testing ConfigManager...")
    total += 1
    try:
        from core.config_manager import ConfigManager
        config = ConfigManager()
        test_value = "test_value"
        encrypted = config.encrypt_value(test_value)
        decrypted = config.decrypt_value(encrypted)
        assert decrypted == test_value
        print("   [PASS] ConfigManager encryption/decryption")
        passed += 1
    except Exception as e:
        print(f"   [FAIL] ConfigManager: {e}")
        failed += 1
    
    # Test EmailMonitor
    print("2. Testing EmailMonitor...")
    total += 1
    try:
        from core.email_monitor import EmailMonitor
        monitor = EmailMonitor()
        assert monitor is not None
        print("   [PASS] EmailMonitor initialization")
        passed += 1
    except Exception as e:
        print(f"   [FAIL] EmailMonitor: {e}")
        failed += 1
    
    # Test JobScraper
    print("3. Testing JobScraper...")
    total += 1
    try:
        from core.job_scraper import JobScraper
        scraper = JobScraper()
        assert scraper is not None
        print("   [PASS] JobScraper initialization")
        passed += 1
    except Exception as e:
        print(f"   [FAIL] JobScraper: {e}")
        failed += 1
    
    # Test ResumeParser
    print("4. Testing ResumeParser...")
    total += 1
    try:
        from core.resume_parser import ResumeParser
        parser = ResumeParser()
        assert parser is not None
        print("   [PASS] ResumeParser initialization")
        passed += 1
    except Exception as e:
        print(f"   [FAIL] ResumeParser: {e}")
        failed += 1
    
    # Test MatchCalculator
    print("5. Testing MatchCalculator...")
    total += 3
    try:
        from analysis.match_calculator import MatchCalculator
        calculator = MatchCalculator()
        assert calculator is not None
        print("   [PASS] MatchCalculator initialization")
        passed += 1
        
        # Test experience score calculation
        score = calculator._calculate_experience_score(3, 3)
        assert score == 90
        print("   [PASS] Experience score calculation")
        passed += 1
        
        # Test recommendation determination
        rec = calculator._determine_recommendation(85)
        assert rec == "STRONG_MATCH"
        print("   [PASS] Recommendation determination")
        passed += 1
    except Exception as e:
        print(f"   [FAIL] MatchCalculator: {e}")
        failed += 3
    
    # Test RuleBasedAnalyzer
    print("6. Testing RuleBasedAnalyzer...")
    total += 1
    try:
        from analysis.rule_based_analyzer import RuleBasedAnalyzer
        analyzer = RuleBasedAnalyzer()
        assert analyzer is not None
        print("   [PASS] RuleBasedAnalyzer initialization")
        passed += 1
    except Exception as e:
        print(f"   [FAIL] RuleBasedAnalyzer: {e}")
        failed += 1
    
    # Test ApplicationTracker
    print("7. Testing ApplicationTracker...")
    total += 1
    try:
        from storage.application_tracker import ApplicationTracker
        tracker = ApplicationTracker()
        assert tracker is not None
        print("   [PASS] ApplicationTracker initialization")
        passed += 1
    except Exception as e:
        print(f"   [FAIL] ApplicationTracker: {e}")
        failed += 1
    
    # Test CSVExporter
    print("8. Testing CSVExporter...")
    total += 1
    try:
        from storage.csv_exporter import CSVExporter
        exporter = CSVExporter()
        assert exporter is not None
        print("   [PASS] CSVExporter initialization")
        passed += 1
    except Exception as e:
        print(f"   [FAIL] CSVExporter: {e}")
        failed += 1
    
    # Test DatabaseManager
    print("9. Testing DatabaseManager...")
    total += 1
    try:
        from storage.database import DatabaseManager
        db = DatabaseManager()
        assert db is not None
        print("   [PASS] DatabaseManager initialization")
        passed += 1
    except Exception as e:
        print(f"   [FAIL] DatabaseManager: {e}")
        failed += 1
    
    # Summary
    print()
    print("Test Summary")
    print("=" * 12)
    print(f"Total:  {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print()
        print("[SUCCESS] All tests passed!")
        return True
    else:
        print()
        print(f"[FAILURE] {failed} tests failed out of {total} total tests")
        return False


if __name__ == "__main__":
    success = test_all_components()
    sys.exit(0 if success else 1)