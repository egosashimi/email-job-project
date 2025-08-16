"""
Simple test script to verify core functionality.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that we can import our modules."""
    try:
        from core.config_manager import ConfigManager
        print("[PASS] ConfigManager imported successfully")
    except Exception as e:
        print(f"[FAIL] Failed to import ConfigManager: {e}")
    
    try:
        from core.email_monitor import EmailMonitor
        print("[PASS] EmailMonitor imported successfully")
    except Exception as e:
        print(f"[FAIL] Failed to import EmailMonitor: {e}")
    
    try:
        from storage.database import DatabaseManager
        print("[PASS] DatabaseManager imported successfully")
    except Exception as e:
        print(f"[FAIL] Failed to import DatabaseManager: {e}")

def test_config_manager():
    """Test ConfigManager functionality."""
    try:
        from core.config_manager import ConfigManager
        config = ConfigManager()
        print("[PASS] ConfigManager instantiated successfully")
        
        # Test encryption/decryption
        test_value = "test_value"
        encrypted = config.encrypt_value(test_value)
        decrypted = config.decrypt_value(encrypted)
        
        if decrypted == test_value:
            print("[PASS] Encryption/decryption working correctly")
        else:
            print("[FAIL] Encryption/decryption failed")
    except Exception as e:
        print(f"[FAIL] ConfigManager test failed: {e}")

def test_database():
    """Test DatabaseManager functionality."""
    try:
        from storage.database import DatabaseManager
        db = DatabaseManager()
        print("[PASS] DatabaseManager instantiated successfully")
        
        # Test storing a job
        job_data = {
            'id': 'test-123',
            'source': 'linkedin',
            'url': 'https://example.com/job/123',
            'title': 'Test Job'
        }
        
        result = db.store_job(job_data)
        if result:
            print("[PASS] Job storage successful")
        else:
            print("[FAIL] Job storage failed")
            
    except Exception as e:
        print(f"[FAIL] DatabaseManager test failed: {e}")

if __name__ == "__main__":
    print("Running basic functionality tests...\n")
    test_imports()
    print()
    test_config_manager()
    print()
    test_database()
    print("\nTests completed.")