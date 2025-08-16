"""
Database management for job match automation.
Handles SQLite database operations and schema management.
"""

import sqlite3
import os
from typing import List, Dict, Optional
from datetime import datetime
from src.core.config_manager import config


class DatabaseManager:
    """Manages SQLite database operations for job match automation."""

    def __init__(self):
        """Initialize database manager."""
        self.db_path = config.database_path
        self._initialize_database()

    def _initialize_database(self):
        """Create database and tables if they don't exist."""
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Create tables
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Job postings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS jobs (
                    id TEXT PRIMARY KEY,
                    source TEXT NOT NULL,
                    company TEXT,
                    title TEXT,
                    url TEXT UNIQUE NOT NULL,
                    description TEXT,
                    requirements TEXT,
                    salary_min INTEGER,
                    salary_max INTEGER,
                    location TEXT,
                    remote_option BOOLEAN,
                    experience_years INTEGER,
                    discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    email_id TEXT
                )
            ''')
            
            # Analysis results table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analyses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_id TEXT NOT NULL,
                    match_percentage INTEGER NOT NULL,
                    strengths TEXT,
                    weaknesses TEXT,
                    hidden_opportunities TEXT,
                    red_flags TEXT,
                    recommendation TEXT,
                    reasoning TEXT,
                    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (job_id) REFERENCES jobs(id)
                )
            ''')
            
            # Application tracking table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_id TEXT NOT NULL,
                    status TEXT DEFAULT 'PENDING',
                    applied_at TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT,
                    FOREIGN KEY (job_id) REFERENCES jobs(id)
                )
            ''')
            
            # Email tracking to prevent duplicates
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS processed_emails (
                    email_id TEXT PRIMARY KEY,
                    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    job_count INTEGER
                )
            ''')
            
            # Create indexes for performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_jobs_discovered ON jobs(discovered_at)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_analyses_percentage ON analyses(match_percentage)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_applications_status ON applications(status)')
            
            conn.commit()

    def store_job(self, job_data: Dict) -> bool:
        """Store a job posting in the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT OR REPLACE INTO jobs (
                        id, source, company, title, url, description, requirements,
                        salary_min, salary_max, location, remote_option, experience_years, email_id
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    job_data.get('id'),
                    job_data.get('source'),
                    job_data.get('company'),
                    job_data.get('title'),
                    job_data.get('url'),
                    job_data.get('description'),
                    job_data.get('requirements'),
                    job_data.get('salary_min'),
                    job_data.get('salary_max'),
                    job_data.get('location'),
                    job_data.get('remote_option'),
                    job_data.get('experience_years'),
                    job_data.get('email_id')
                ))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"Error storing job: {e}")
            return False

    def is_email_processed(self, email_id: str) -> bool:
        """Check if an email has already been processed."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT 1 FROM processed_emails WHERE email_id = ?', (email_id,))
                return cursor.fetchone() is not None
        except Exception as e:
            print(f"Error checking processed email: {e}")
            return False

    def mark_email_processed(self, email_id: str, job_count: int = 0):
        """Mark an email as processed."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO processed_emails (email_id, job_count)
                    VALUES (?, ?)
                ''', (email_id, job_count))
                conn.commit()
        except Exception as e:
            print(f"Error marking email as processed: {e}")

    def get_recent_jobs(self, hours: int = 24) -> List[Dict]:
        """Get job postings from the last N hours."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM jobs 
                    WHERE discovered_at > datetime('now', '-{} hours')
                    ORDER BY discovered_at DESC
                '''.format(hours))
                
                columns = [description[0] for description in cursor.description]
                rows = cursor.fetchall()
                
                return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            print(f"Error retrieving recent jobs: {e}")
            return []