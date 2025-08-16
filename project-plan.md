Perfect! I have everything I need. Let me create comprehensive documentation for your AI coding agent. Given your background and goals, I'll design this to showcase your understanding of modern development practices while keeping it achievable.

## Complete Architecture Documents for AI Agent

### 1. **PROJECT_SPECIFICATION.md**

```markdown
# Job Match Automation - Complete Project Specification

## Project Overview
An automated email monitoring system that analyzes job postings from multiple job boards against a user's resume, providing brutally honest match assessments via Discord notifications and data exports.

## User Context
- **Developer Level**: Junior/Mid-level developer with AI-assisted coding experience
- **Location**: NYC preferred, remote acceptable
- **Salary Range**: $45k minimum, $70-100k ideal
- **Goal**: Apply to realistic matches only, maximize interview probability
- **Tech Background**: Python and JavaScript experience, comfortable with AI-assisted development

## Core Features
1. Monitor Gmail for job emails from LinkedIn, Indeed, ZipRecruiter, Y Combinator, Startup Jobs
2. Follow email links to fetch actual job descriptions
3. Compare jobs against resume using AI (DeepSeek via OpenRouter)
4. Provide honest match percentage focusing on experience alignment
5. Send Discord notifications for viable matches (>60% recommended)
6. Track application history and responses
7. Export data to CSV and future web interface
8. MCP server for tool integration

## Technical Requirements
- **OS**: Windows 10
- **Python**: 3.13 (flexible)
- **Security**: Encrypted storage for email credentials and resume
- **AI Model**: DeepSeek (free tier via OpenRouter)
- **Notifications**: Discord webhooks
- **Data Storage**: SQLite for job history, encrypted JSON for credentials

## Key Constraints
- Avoid jobs requiring 5+ years experience
- Focus on realistic matches over aspirational
- Handle rate limits from job boards
- Secure sensitive data (resume, credentials)
- Async processing for efficiency
```

### 2. **IMPLEMENTATION_GUIDE.md**

```markdown
# Implementation Guide for AI Coding Agent

## Project Structure
```
job-match-automation/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── email_monitor.py      # IMAP email fetching
│   │   ├── job_scraper.py        # Fetch job details from links
│   │   ├── resume_parser.py      # Parse and structure resume
│   │   └── config_manager.py     # Secure config handling
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── ai_analyzer.py        # DeepSeek integration
│   │   ├── match_calculator.py   # Match scoring logic
│   │   └── experience_filter.py  # Filter out senior positions
│   ├── notifications/
│   │   ├── __init__.py
│   │   ├── discord_notifier.py   # Discord webhook integration
│   │   └── notification_templates.py
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── database.py           # SQLite operations
│   │   ├── encryption.py         # Credential encryption
│   │   └── csv_exporter.py       # Export functionality
│   ├── mcp/
│   │   ├── __init__.py
│   │   ├── server.py             # MCP server implementation
│   │   └── tools.py              # Exposed MCP tools
│   └── main.py                   # Entry point
├── data/
│   ├── resume.txt                # User's resume (encrypted)
│   ├── jobs.db                   # SQLite database
│   └── exports/                  # CSV exports
├── config/
│   ├── .env.example
│   ├── job_boards.yaml           # Email patterns for each board
│   └── keywords.yaml             # Experience level indicators
├── tests/
│   ├── test_email_monitor.py
│   ├── test_ai_analyzer.py
│   ├── test_mcp_server.py
│   └── fixtures/                 # Sample emails and job descriptions
├── docs/
│   ├── API.md
│   ├── MCP_USAGE.md
│   └── TROUBLESHOOTING.md
├── scripts/
│   ├── setup.py                  # Initial setup script
│   └── encrypt_resume.py         # Resume encryption utility
├── requirements.txt
├── README.md
├── .gitignore
└── .github/
    └── workflows/
        └── test.yml              # GitHub Actions CI
```

## Core Components Implementation

### 1. Email Monitor (src/core/email_monitor.py)
```python
import imaplib
import email
from typing import List, Dict
from datetime import datetime, timedelta
import asyncio
from cryptography.fernet import Fernet

class EmailMonitor:
    """Monitors Gmail for job emails from specified job boards."""
    
    JOB_BOARDS = {
        'linkedin.com': {
            'from': 'jobs-noreply@linkedin.com',
            'subject_patterns': ['job alert', 'new jobs']
        },
        'indeed.com': {
            'from': 'noreply@indeed.com',
            'subject_patterns': ['job alert', 'new positions']
        },
        'ziprecruiter.com': {
            'from': 'no-reply@ziprecruiter.com',
            'subject_patterns': ['new jobs', 'job matches']
        },
        'ycombinator.com': {
            'from': 'jobs@ycombinator.com',
            'subject_patterns': ['work at a startup']
        },
        'startup.jobs': {
            'from': 'notifications@startup.jobs',
            'subject_patterns': ['new opportunities']
        }
    }
    
    def __init__(self, encrypted_credentials: str):
        self.credentials = self._decrypt_credentials(encrypted_credentials)
        self.imap = None
        
    async def get_job_emails(self, hours_back: int = 24) -> List[Dict]:
        """Fetch job emails from the last N hours."""
        # Implementation details in full code
        pass

### 2. Job Scraper (src/core/job_scraper.py)
```python
import aiohttp
from bs4 import BeautifulSoup
import re
from typing import Dict, Optional
from urllib.parse import urlparse

class JobScraper:
    """Fetches full job descriptions from email links."""
    
    SCRAPING_RULES = {
        'linkedin.com': {
            'job_description': ['div.description__text', 'div.show-more-less-html__markup'],
            'requirements': ['ul.description__job-criteria-list'],
            'salary': ['div.salary-main-content', 'span.salary-range']
        },
        'indeed.com': {
            'job_description': ['div.jobsearch-JobComponent-description', 'div#jobDescriptionText'],
            'requirements': ['div.jobsearch-JobComponent-description'],
            'salary': ['span.salary-snippet', 'div.salary-container']
        },
        # Add patterns for other job boards
    }
    
    async def fetch_job_details(self, url: str) -> Optional[Dict]:
        """Fetch and parse job details from URL."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=30) as response:
                    html = await response.text()
                    return self._parse_job_page(html, urlparse(url).netloc)
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def _extract_experience_years(self, text: str) -> Optional[int]:
        """Extract years of experience requirement."""
        patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'(\d+)\+?\s*years?\s*(?:of\s*)?professional',
            r'(\d+)\+?\s*yr'
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        return None
```

### 3. AI Analyzer (src/analysis/ai_analyzer.py)
```python
import os
import json
import aiohttp
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class MatchAnalysis:
    percentage: int
    strengths: List[str]
    weaknesses: List[str]
    hidden_opportunities: List[str]
    red_flags: List[str]
    recommendation: str  # 'STRONG_MATCH', 'POSSIBLE_MATCH', 'REACH', 'SKIP'
    reasoning: str

class AIJobAnalyzer:
    """Analyzes job matches using DeepSeek via OpenRouter."""
    
    ANALYSIS_PROMPT = """You are a brutally honest career advisor analyzing job matches for a junior/mid-level developer.

Resume Summary:
{resume_summary}

Job Description:
{job_description}

Candidate Context:
- Junior/Mid level (2-3 years experience with AI-assisted development)
- Located in NYC, open to remote
- Salary expectation: $70-100k (minimum $45k)
- Strong with AI-assisted coding, Python/JavaScript experience
- No specific role preference, exploring opportunities

Analyze this match with brutal honesty. Consider:
1. Experience level match (reject if requires 5+ years)
2. Actual skill alignment (not keyword matching)
3. Hidden transferable skills that might apply
4. Red flags or concerns
5. Realistic chance of getting an interview

Provide a JSON response:
{
    "percentage": <0-100>,
    "strengths": ["specific strength 1", "strength 2"],
    "weaknesses": ["specific gap 1", "gap 2"],
    "hidden_opportunities": ["transferable skill applications"],
    "red_flags": ["concern 1", "concern 2"],
    "recommendation": "STRONG_MATCH|POSSIBLE_MATCH|REACH|SKIP",
    "reasoning": "Brief explanation of the overall assessment"
}

Be especially critical about experience requirements and technical depth."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "deepseek/deepseek-chat"
    
    async def analyze_match(self, resume: Dict, job: Dict) -> MatchAnalysis:
        """Perform AI analysis of job match."""
        # Implementation with proper error handling
        pass
```

### 4. MCP Server (src/mcp/server.py)
```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio
from typing import Dict, List

class JobMatcherMCP:
    """MCP server exposing job matching functionality."""
    
    def __init__(self, analyzer, database):
        self.analyzer = analyzer
        self.database = database
        self.server = Server("job-matcher")
        self._setup_tools()
    
    def _setup_tools(self):
        @self.server.tool()
        async def analyze_job_url(url: str, resume_path: str) -> str:
            """Analyze a specific job posting against resume."""
            job_details = await self.scraper.fetch_job_details(url)
            resume = self.resume_parser.parse(resume_path)
            analysis = await self.analyzer.analyze_match(resume, job_details)
            return json.dumps(analysis.__dict__)
        
        @self.server.tool()
        async def get_recent_matches(hours: int = 24, min_percentage: int = 60) -> str:
            """Get recent job matches above threshold."""
            matches = await self.database.get_recent_matches(hours, min_percentage)
            return json.dumps(matches)
        
        @self.server.tool()
        async def update_application_status(job_id: str, status: str) -> str:
            """Update application status for a job."""
            # Status: APPLIED, REJECTED, INTERVIEW, OFFER
            result = await self.database.update_job_status(job_id, status)
            return json.dumps({"success": result})
        
        @self.server.tool()
        async def export_matches_csv(start_date: str, end_date: str) -> str:
            """Export job matches to CSV for date range."""
            filepath = await self.exporter.export_date_range(start_date, end_date)
            return json.dumps({"filepath": filepath})
```

### 3. **DATABASE_SCHEMA.md**

```markdown
# Database Schema and Storage Design

## SQLite Schema (jobs.db)

```sql
-- Job postings table
CREATE TABLE jobs (
    id TEXT PRIMARY KEY,
    source TEXT NOT NULL,  -- 'linkedin', 'indeed', etc.
    company TEXT NOT NULL,
    title TEXT NOT NULL,
    url TEXT UNIQUE NOT NULL,
    description TEXT,
    requirements

```sql
-- Job postings table (continued)
CREATE TABLE jobs (
    id TEXT PRIMARY KEY,
    source TEXT NOT NULL,  -- 'linkedin', 'indeed', etc.
    company TEXT NOT NULL,
    title TEXT NOT NULL,
    url TEXT UNIQUE NOT NULL,
    description TEXT,
    requirements TEXT,
    salary_min INTEGER,
    salary_max INTEGER,
    location TEXT,
    remote_option BOOLEAN,
    experience_years INTEGER,
    discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    email_id TEXT  -- Track source email
);

-- Analysis results table
CREATE TABLE analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id TEXT NOT NULL,
    match_percentage INTEGER NOT NULL,
    strengths TEXT,  -- JSON array
    weaknesses TEXT,  -- JSON array
    hidden_opportunities TEXT,  -- JSON array
    red_flags TEXT,  -- JSON array
    recommendation TEXT,
    reasoning TEXT,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(id)
);

-- Application tracking table
CREATE TABLE applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id TEXT NOT NULL,
    status TEXT DEFAULT 'PENDING',  -- PENDING, APPLIED, REJECTED, INTERVIEW, OFFER
    applied_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (job_id) REFERENCES jobs(id)
);

-- Email tracking to prevent duplicates
CREATE TABLE processed_emails (
    email_id TEXT PRIMARY KEY,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    job_count INTEGER
);

-- Create indexes for performance
CREATE INDEX idx_jobs_discovered ON jobs(discovered_at);
CREATE INDEX idx_jobs_company ON jobs(company);
CREATE INDEX idx_analyses_percentage ON analyses(match_percentage);
CREATE INDEX idx_applications_status ON applications(status);
```

## Encrypted Storage
- Resume stored as encrypted file: `data/resume.enc`
- Credentials in encrypted JSON: `data/credentials.enc`
- Encryption key derived from environment variable
```

### 4. **API_CONTRACTS.md**

```markdown
# API Contracts and Data Structures

## Email Parser Output
```json
{
    "email_id": "unique-email-id",
    "source": "linkedin",
    "received_at": "2024-01-15T10:30:00Z",
    "job_links": [
        {
            "url": "https://linkedin.com/jobs/view/123456",
            "title_hint": "Python Developer at TechCorp"
        }
    ]
}
```

## Job Scraper Output
```json
{
    "id": "linkedin-123456",
    "source": "linkedin",
    "company": "TechCorp",
    "title": "Python Developer",
    "url": "https://linkedin.com/jobs/view/123456",
    "description": "Full job description text...",
    "requirements": {
        "experience_years": 3,
        "skills": ["Python", "AWS", "Docker"],
        "education": "Bachelor's degree or equivalent"
    },
    "salary": {
        "min": 70000,
        "max": 100000,
        "currency": "USD"
    },
    "location": {
        "city": "New York",
        "state": "NY",
        "remote_option": true
    },
    "posted_date": "2024-01-14",
    "application_deadline": null
}
```

## AI Analysis Request
```json
{
    "resume": {
        "experience_years": 2,
        "skills": {
            "Python": "2 years",
            "JavaScript": "2 years",
            "AI-assisted development": "1 year"
        },
        "education": "Bachelor's in Computer Science",
        "location": "New York, NY",
        "salary_expectation": {
            "min": 70000,
            "ideal": 85000
        }
    },
    "job": {
        // Job scraper output format
    }
}
```

## AI Analysis Response
```json
{
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
        "AI-assisted development experience could accelerate cloud learning",
        "JavaScript knowledge suggests full-stack potential"
    ],
    "red_flags": [
        "Job lists 'nice to have' 5 years experience"
    ],
    "recommendation": "POSSIBLE_MATCH",
    "reasoning": "Strong fundamental match with manageable skill gaps"
}
```

## Discord Notification Format
```json
{
    "embeds": [{
        "title": "🎯 TechCorp - Python Developer",
        "url": "https://linkedin.com/jobs/view/123456",
        "color":

```json
{
    "embeds": [{
        "title": "🎯 TechCorp - Python Developer",
        "url": "https://linkedin.com/jobs/view/123456",
        "color": 5025616,  // Green for good match
        "fields": [
            {
                "name": "📊 Match Score",
                "value": "75%",
                "inline": true
            },
            {
                "name": "💰 Salary",
                "value": "$70k-$100k",
                "inline": true
            },
            {
                "name": "📍 Location",
                "value": "NYC (Remote OK)",
                "inline": true
            },
            {
                "name": "✅ Your Strengths",
                "value": "• Python experience matches\n• Located in same city\n• Salary range aligns",
                "inline": false
            },
            {
                "name": "⚠️ Gaps to Address",
                "value": "• Missing AWS experience\n• No Docker mentioned",
                "inline": false
            },
            {
                "name": "💡 Hidden Opportunity",
                "value": "Your AI-assisted dev experience could accelerate cloud learning",
                "inline": false
            },
            {
                "name": "🎯 Recommendation",
                "value": "**POSSIBLE MATCH** - Worth applying with tailored resume",
                "inline": false
            }
        ],
        "footer": {
            "text": "Source: LinkedIn • Click title to view full posting"
        },
        "timestamp": "2024-01-15T10:30:00.000Z"
    }]
}
```

## CSV Export Format
```csv
job_id,company,title,url,match_percentage,recommendation,salary_min,salary_max,location,remote,analyzed_date,applied,status
linkedin-123456,TechCorp,Python Developer,https://...,75,POSSIBLE_MATCH,70000,100000,"New York, NY",Yes,2024-01-15,Yes,PENDING
```
```

### 5. **ERROR_HANDLING.md**

```markdown
# Error Handling and Recovery Strategies

## Email Connection Errors

### IMAP Authentication Failure
```python
class EmailAuthError(Exception):
    """Raised when email authentication fails."""
    
    RECOVERY_ACTIONS = [
        "1. Verify email and app password are correct",
        "2. Check if 2FA is enabled (need app-specific password)",
        "3. Ensure 'Less secure app access' or proper OAuth",
        "4. Try regenerating app password"
    ]

# Implementation
async def connect_with_retry(self, max_retries=3):
    for attempt in range(max_retries):
        try:
            await self._connect()
            return
        except imaplib.IMAP4.error as e:
            if "AUTHENTICATIONFAILED" in str(e):
                raise EmailAuthError(
                    f"Authentication failed. {EmailAuthError.RECOVERY_ACTIONS}"
                )
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

### Rate Limiting
```python
class RateLimiter:
    def __init__(self):
        self.limits = {
            'linkedin.com': {'requests': 10, 'period': 300},  # 10 per 5 min
            'indeed.com': {'requests': 20, 'period': 300},
            'default': {'requests': 30, 'period': 300}
        }
        self.requests = defaultdict(list)
    
    async def check_rate_limit(self, domain: str):
        # Implementation with sliding window
        pass
```

## Job Scraping Errors

### Page Structure Changes
```python
FALLBACK_STRATEGIES = {
    'use_cached_version': 'Check if we have recent cache',
    'try_alternative_selectors': 'Use backup CSS selectors',
    'extract_from_meta_tags': 'Try OpenGraph/meta tags',
    'flag_for_manual_review': 'Mark as needs attention'
}

async def scrape_with_fallback(self, url: str):
    strategies = [
        self._scrape_with_primary_rules,
        self._scrape_with_backup_rules,
        self._scrape_from_meta_tags,
        self._basic_text_extraction
    ]
    
    for strategy in strategies:
        result = await strategy(url)
        if result and result.get('title') and result.get('description'):
            return result
    
    # Log failure for monitoring
    await self.log_scraping_failure(url, "All strategies failed")
    return None
```

### Anti-Scraping Measures
```python
class ScrapingDefense:
    @staticmethod
    async def handle_cloudflare(session, url):
        # Use cloudscraper library
        pass
    
    @staticmethod
    async def handle_rate_limit(response):
        if response.status == 429:
            retry_after = response.headers.get('Retry-After', 60)
            await asyncio.sleep(int(retry_after))
            return True
        return False
```

## AI Processing Errors

### API Failures
```python
async def analyze_with_fallback(self, resume: Dict, job: Dict):
    try:
        # Primary: DeepSeek via OpenRouter
        return await self._analyze_deepseek(resume, job)
    except Exception as e:
        # Fallback 1: Try different model
        try:
            return await self._analyze_alternative_model(resume, job)
        except:
            # Fallback 2: Rule-based analysis
            return self._basic_rule_analysis(resume, job)

def _basic_rule_analysis(self, resume: Dict, job: Dict):
    """Fallback rule-based matching when AI fails."""
    score = 0
    strengths = []
    weaknesses = []
    
    # Experience match
    job_years = job.get('experience_years', 0)
    if job_years <= 3:
        score += 30
        strengths.append("Experience level matches")
    elif job_years >= 5:
        weaknesses.append(f"Requires {job_years} years experience")
        score -= 20
    
    # Location match
    if job.get('remote_option') or job.get('location', {}).get('city') == 'New York':
        score += 20
        strengths.append("Location works")
    
    # Continue with other rules...
    return MatchAnalysis(
        percentage=max(0, min(100, score)),
        strengths=strengths,
        weaknesses=weaknesses,
        recommendation="NEEDS_MANUAL_REVIEW"
    )
```

## Discord Notification Failures

### Webhook Errors
```python
class NotificationManager:
    def __init__(self):
        self.fallback_methods = [
            self._try_discord_webhook,
            self._save_to_notification_queue,
            self._write_to_local_file,
            self._print_to_console
        ]
    
    async def send_notification(self, job_match: Dict):
        for method in self.fallback_methods:
            try:
                await method(job_match)
                break
            except Exception as e:
                logger.error(f"Notification method {method.__name__} failed: {e}")
                continue
```

## Database Errors

### Connection Issues
```python
class DatabaseManager:
    async def execute_with_retry(self, query: str, params: tuple):
        for attempt in range(3):
            try:
                return await self._execute(query, params)
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e):
                    await asyncio.sleep(0.1 * (attempt + 1))
                else:
                    raise
```

## Recovery Strategies Summary

1. **Graceful Degradation**: Always have fallback methods
2. **Retry Logic**: Expon

```markdown
## Recovery Strategies Summary

1. **Graceful Degradation**: Always have fallback methods
2. **Retry Logic**: Exponential backoff for transient failures
3. **Caching**: Store successful results for resilience
4. **Logging**: Comprehensive error logging for debugging
5. **Monitoring**: Track error rates and patterns
6. **Manual Queue**: Flag items that need human review

## Error Monitoring Dashboard
```python
class ErrorMonitor:
    def __init__(self):
        self.error_counts = defaultdict(int)
        self.error_patterns = defaultdict(list)
    
    async def log_error(self, component: str, error_type: str, details: dict):
        self.error_counts[f"{component}:{error_type}"] += 1
        self.error_patterns[component].append({
            'type': error_type,
            'timestamp': datetime.now(),
            'details': details
        })
        
        # Alert if error rate exceeds threshold
        if self.error_counts[f"{component}:{error_type}"] > 10:
            await self.send_alert(component, error_type)
```
```

### 6. **TESTING_STRATEGY.md**

```markdown
# Testing Strategy and Test Data

## Test Structure

### Unit Tests

#### Email Monitor Tests (tests/test_email_monitor.py)
```python
import pytest
from unittest.mock import Mock, patch
from src.core.email_monitor import EmailMonitor

class TestEmailMonitor:
    @pytest.fixture
    def mock_email_data(self):
        return {
            'linkedin': {
                'from': 'jobs-noreply@linkedin.com',
                'subject': 'New Python Developer positions in NYC',
                'body': 'View jobs: https://linkedin.com/jobs/view/123...',
                'date': '2024-01-15'
            },
            'indeed': {
                'from': 'noreply@indeed.com',
                'subject': 'Job Alert: 5 new Software Engineer jobs',
                'body': 'https://indeed.com/viewjob?jk=abc123...',
                'date': '2024-01-15'
            }
        }
    
    @pytest.mark.asyncio
    async def test_fetch_job_emails(self, mock_email_data):
        with patch('imaplib.IMAP4_SSL') as mock_imap:
            monitor = EmailMonitor(encrypted_creds)
            emails = await monitor.get_job_emails(hours_back=24)
            assert len(emails) == 2
            assert any('linkedin' in e['source'] for e in emails)
    
    def test_parse_email_links(self):
        html_body = '''
        <a href="https://linkedin.com/jobs/view/123456">Python Developer</a>
        <a href="https://linkedin.com/jobs/view/789012">Senior Engineer</a>
        '''
        links = EmailMonitor._extract_job_links(html_body, 'linkedin.com')
        assert len(links) == 2
```

#### AI Analyzer Tests (tests/test_ai_analyzer.py)
```python
class TestAIAnalyzer:
    @pytest.fixture
    def sample_resume(self):
        return {
            'experience_years': 2,
            'skills': ['Python', 'JavaScript', 'Git'],
            'education': 'BS Computer Science',
            'location': 'New York, NY'
        }
    
    @pytest.fixture
    def sample_jobs(self):
        return {
            'good_match': {
                'title': 'Junior Python Developer',
                'experience_years': 2,
                'required_skills': ['Python', 'Git'],
                'salary_range': [70000, 90000]
            },
            'bad_match': {
                'title': 'Senior Architect',
                'experience_years':

```markdown
            'bad_match': {
                'title': 'Senior Architect',
                'experience_years': 10,
                'required_skills': ['Python', 'Kubernetes', 'System Design'],
                'salary_range': [150000, 200000]
            },
            'edge_case': {
                'title': 'Full Stack Developer',
                'experience_years': 3,
                'required_skills': ['JavaScript', 'React', 'Node.js'],
                'salary_range': [80000, 100000]
            }
        }
    
    @pytest.mark.asyncio
    async def test_analyze_good_match(self, sample_resume, sample_jobs):
        analyzer = AIJobAnalyzer(api_key='test')
        with patch('aiohttp.ClientSession.post') as mock_post:
            mock_post.return_value.__aenter__.return_value.json = Mock(
                return_value={'choices': [{'message': {'content': json.dumps({
                    'percentage': 85,
                    'recommendation': 'STRONG_MATCH'
                })}}]}
            )
            result = await analyzer.analyze_match(sample_resume, sample_jobs['good_match'])
            assert result.percentage >= 70
            assert result.recommendation == 'STRONG_MATCH'
```

### Integration Tests

#### End-to-End Workflow Test (tests/test_integration.py)
```python
@pytest.mark.integration
class TestFullWorkflow:
    async def test_email_to_notification_flow(self):
        # 1. Mock email server with test email
        # 2. Process email and extract job
        # 3. Analyze with AI
        # 4. Send Discord notification
        # 5. Verify database entry
        pass
```

## Test Data

### Sample Email Bodies (tests/fixtures/emails/)

#### linkedin_job_alert.html
```html
<!DOCTYPE html>
<html>
<body>
    <h2>5 new Python Developer jobs in New York, NY</h2>
    <div class="job-card">
        <h3><a href="https://www.linkedin.com/jobs/view/3827391">Junior Python Developer</a></h3>
        <p>TechStartup Inc. • New York, NY • $70,000 - $90,000</p>
        <p>2+ years experience with Python, Django, PostgreSQL...</p>
    </div>
    <div class="job-card">
        <h3><a href="https://www.linkedin.com/jobs/view/3827392">Senior Python Engineer</a></h3>
        <p>BigCorp • New York, NY • $120,000 - $150,000</p>
        <p>7+ years experience, must have led teams...</p>
    </div>
</body>
</html>
```

#### indeed_job_alert.html
```html
<table>
    <tr>
        <td>
            <a href="https://www.indeed.com/viewjob?jk=abc123def456">Software Developer</a>
            <br>StartupXYZ - New York, NY 10001
            <br>$65,000 - $85,000 a year
        </td>
    </tr>
</table>
```

### Sample Job Descriptions (tests/fixtures/jobs/)

#### junior_developer.json
```json
{
    "title": "Junior Python Developer",
    "company": "TechStartup Inc",
    "description": "We're looking for a passionate junior developer to join our growing team. You'll work on exciting projects using Python, Django, and modern web technologies.\n\nResponsibilities:\n- Write clean, maintainable Python code\n- Collaborate with senior developers\n- Participate in code reviews\n- Help with debugging and testing\n\nRequirements:\n- 1-3 years of Python experience\n- Familiarity with Django or Flask\n- Basic understanding of databases\n- Eagerness to learn\n\nNice to have:\n- Experience with React\n- AWS knowledge\n- Open source contributions",
    "experience_years": 2,
    "salary": {
        "min": 70000,
        "max": 90000
    },
    "location": "New York, NY",
    "remote_option": true
}
```

### Mock AI Responses (tests/fixtures/ai_responses/)

#### realistic_analysis.json
```json
{
    "percentage": 72,
    "strengths": [
        "Python experience aligns well with the 2-year requirement",
        "Location match - both in NYC with remote option",
        "Salary range fits your expectations ($70-90k vs your $70-100k target)"
    ],
    "weaknesses": [
        "No mentioned Django/Flask experience",
        "Missing AWS knowledge (listed as nice-to-have)",
        "No database experience explicitly mentioned"
    ],
    "hidden_opportunities": [
        "Your AI-assisted coding experience shows strong learning ability",
        "JavaScript knowledge suggests you could quickly pick up React"
    ],
    "red_flags": [
        "Job mentions 'fast-paced startup' - could mean long hours"
    ],
    "recommendation": "POSSIBLE_MATCH",
    "reasoning": "Solid foundational match with manageable skill gaps. The junior-level positioning and salary alignment make this worth pursuing despite missing some specific frameworks."
}
```

## Performance Tests

### Load Testing (tests/test_performance.py)
```python
@pytest.mark.performance
class TestPerformance:
    async def test_bulk_email_processing(self):
        """Ensure we can handle 100+ emails efficiently."""
        emails = generate_test_emails(count=100)
        start_time = time.time()
        
        monitor = EmailMonitor(test_creds)
        results = await monitor.process_bulk(emails)
        
        elapsed = time.time() - start_time
        assert elapsed < 60  # Should process 100 emails in under 1 minute
        assert len(results) == 100
    
    async def test_concurrent_job_scraping(self):
        """Test parallel job scraping performance."""
        urls = [f"https://test.com/job/{i}" for i in range(20)]
        
        scraper = JobScraper()
        start_time = time.time()
        
        results = await scraper.fetch_multiple(urls, max_concurrent=5)
        
        elapsed = time.time() - start_time
        assert elapsed < 30  # 20 jobs in under 30 seconds
```

## Test Coverage Requirements

- **Minimum Coverage**: 80% overall
- **Critical Paths**: 95% coverage for:
  - Email parsing
  - AI analysis
  - Database operations
  - Error handling

## Continuous Integration Tests

### GitHub Actions Workflow (.github/workflows/test.yml)
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python 3.13
      uses: actions/setup-python@v2
      with:
        python-version: 3.13
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run linting
      run: |
        flake8 src/ --max-line-length=100
        black --check src/
    
    - name: Run unit tests
      env:
        OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY_TEST }}
      run: |
        pytest tests/unit/ -v --cov=src --cov-report=xml
    
    - name: Run integration tests
      if: github.event_name == 'push'
      run: |
        pytest tests/integration/ -v -m integration
    
    - name: Upload coverage
      uses: codecov/codecov-action@v1
      with:
        file: ./coverage.xml
```

## Test Environment Setup

### Local Testing Setup (scripts/setup_test_env.py)
```python
#!/usr/bin/env python3
"""Set up test environment with sample data."""

import os
import sqlite3
from pathlib import Path

def setup_test_database():
    """Create test database with sample data."""
    db_path = Path("tests/test_data/test_jobs.db")
    db_path.parent.mkdir(exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    
    # Create schema
    with open("src/storage/schema.sql") as f:
        conn.executescript(f.read())
    
    # Insert test data
    test_jobs = [
        ("test-1", "linkedin", "TestCorp", "Python Developer", 
         "http://test.com/1", "Test description", 70000, 90000, 
         "New York, NY", True, 2),
        # More test data...
    ]
    
    conn.executemany(
        "INSERT INTO jobs VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        test_jobs
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_test_environment()
```
```

### 7. **MCP_SERVER_SPECIFICATION.md**

```markdown
# MCP Server Specification

## Overview
The Job Matcher MCP Server exposes job matching functionality to other tools and AI assistants, enabling integration with various workflows and automation systems.

## Installation and Setup

### Server Configuration (mcp_config.json)
```json
{
  "name": "job-matcher",
  "version": "1.0.0",
  "description": "Automated job matching and analysis tools",
  "main": "src/mcp/server.py",
  "commands": {
    "start": "python -m src.mcp.server"
  },
  "tools": [
    "analyze_job_url",
    "get_recent_matches", 
    "update_application_status",
    "export_matches_csv",
    "check_email_now",
    "get_match_statistics"
  ]
}
```

## Exposed Tools

### 1. analyze_job_url
Analyzes a specific job posting against your resume.

**Parameters:**
- `url` (string, required): Job posting URL
- `resume_path` (string, optional): Path to resume file (uses default if not provided)

**Returns:**
```json
{
  "match_percentage": 75,
  "recommendation": "POSSIBLE_MATCH",
  "strengths": ["Python experience matches"],
  "weaknesses": ["Missing AWS experience"],
  "apply_url": "https://linkedin.com/jobs/view/123"
}
```

**Example Usage:**
```python
result = await mcp.call_tool(
    "analyze_job_url",
    {"url": "https://linkedin.com/jobs/view/123456"}
)
```

### 2. get_recent_matches
Retrieves recent job matches above a specified threshold.

**Parameters:**
- `hours` (integer, optional): Hours to look back (default: 24)
- `min_percentage` (integer, optional): Minimum match percentage (default: 60)
- `include_applied` (boolean, optional): Include already applied jobs (default: false)

**Returns:**
```json
{
  "matches": [
    {
      "job_id": "linkedin-123",
      "company": "TechCorp",
      "title": "Python Developer",
      "match_percentage": 82,
      "analyzed_at": "2024-01-15T10:30:00Z",
      "status": "PENDING"
    }
  ],
  "total_count": 5,
  "average_match": 73.4
}
```

### 3. update_application_status
Updates the application status for a job.

**Parameters:**
- `job_id` (string, required): Job identifier
- `status` (string, required): One of: APPLIED, REJECTED, INTERVIEW, OFFER
- `notes` (string, optional): Additional notes

**Returns:**
```json
{
  "success": true,
  "job_id": "linkedin-123",
  "old_status": "PENDING",
  "new_status": "APPLIED",
  "updated_at": "2024-01-15T12:00:00Z"
}
```

### 4. export_matches_csv
Exports job matches to CSV for a date range.

**Parameters:**
- `start_date` (string, required): ISO format date (YYYY-MM-DD)
- `end_date` (string, required): ISO format date (YYYY-MM-DD)
- `min_percentage` (integer, optional): Minimum match percentage to include

**Returns:**
```json
{
  "filepath": "/data/exports/jobs_2024-01-01_to_2024-01-15.csv",
  "record_count": 47,
  "file_size_kb": 12.3
}
```

### 5. check_email_now
Triggers immediate email check instead of waiting for schedule.

**Parameters:**
- `job_boards` (array, optional): Specific job boards to check

**Returns:**
```json
{
  "emails_processed": 8,
  "new_jobs_found": 12,
  "analysis_complete": 10,
  "errors": 2
}
```

### 6. get_match_statistics
Returns statistics about job matching performance.

**Parameters:**
- `days` (integer, optional): Days to analyze (default: 7)

**Returns:**
```json
{
  "total_jobs_analyzed": 156,
  "average_match_percentage": 68.3,
  "matches_by_recommendation": {
    "STRONG_MATCH": 12,
    "POSSIBLE_MATCH": 34,
    "REACH": 67,
    "SKIP": 43
  },
  "application_conversion": {
    "applied": 15,
    "interviewed": 3,
    "offers": 0
  },
  "top_companies": [
    {"name": "TechCorp", "count": 8},
    {"name": "StartupXYZ", "count": 5}
  ]
}
```

## Integration Examples

### With Claude Desktop
```json
// claude_desktop_config.json
{
  "mcpServers": {
    "job-matcher": {
      "comman

```json
// claude_desktop_config.json
{
  "mcpServers": {
    "job-matcher": {
      "command": "python",
      "args": ["-m", "src.mcp.server"],
      "cwd": "/path/to/job-match-automation"
    }
  }
}
```

### With CLI Tools
```bash
# Using the MCP CLI
mcp-cli call job-matcher analyze_job_url --url "https://linkedin.com/jobs/view/123"

# Pipe results to other tools
mcp-cli call job-matcher get_recent_matches --min_percentage 80 | jq '.matches[] | .title'
```

### With Python Scripts
```python
from mcp.client import MCPClient

async def check_job_matches():
    async with MCPClient("job-matcher") as client:
        # Get recent high-quality matches
        matches = await client.call_tool(
            "get_recent_matches",
            {"hours": 48, "min_percentage": 75}
        )
        
        # Update status for applied jobs
        for match in matches["matches"]:
            if user_applied(match):
                await client.call_tool(
                    "update_application_status",
                    {
                        "job_id": match["job_id"],
                        "status": "APPLIED",
                        "notes": f"Applied via {match['source']}"
                    }
                )
```

## Server Implementation (src/mcp/server.py)

```python
import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

class JobMatcherMCPServer:
    def __init__(self):
        self.server = Server("job-matcher")
        self.email_monitor = None
        self.analyzer = None
        self.database = None
        self._setup_tools()
    
    def _setup_tools(self):
        @self.server.tool()
        async def analyze_job_url(
            url: str,
            resume_path: Optional[str] = None
        ) -> Dict:
            """Analyze a specific job posting against resume."""
            try:
                # Fetch job details
                job_details = await self.scraper.fetch_job_details(url)
                if not job_details:
                    return {"error": "Could not fetch job details"}
                
                # Load resume
                resume = await self.load_resume(resume_path)
                
                # Analyze match
                analysis = await self.analyzer.analyze_match(resume, job_details)
                
                # Store in database
                await self.database.store_analysis(job_details, analysis)
                
                return {
                    "match_percentage": analysis.percentage,
                    "recommendation": analysis.recommendation,
                    "strengths": analysis.strengths[:3],
                    "weaknesses": analysis.weaknesses[:3],
                    "apply_url": url
                }
            except Exception as e:
                return {"error": f"Analysis failed: {str(e)}"}
        
        @self.server.tool()
        async def get_recent_matches(
            hours: int = 24,
            min_percentage: int = 60,
            include_applied: bool = False
        ) -> Dict:
            """Get recent job matches above threshold."""
            try:
                since = datetime.now() - timedelta(hours=hours)
                matches = await self.database.get_matches_since(
                    since, 
                    min_percentage,
                    include_applied
                )
                
                return {
                    "matches": [
                        {
                            "job_id": m["id"],
                            "company": m["company"],
                            "title": m["title"],
                            "match_percentage": m["match_percentage"],
                            "analyzed_at": m["analyzed_at"],
                            "status": m["status"],
                            "url": m["url"]
                        }
                        for m in matches
                    ],
                    "total_count": len(matches),
                    "average_match": sum(m["match_percentage"] for m in matches) / len(matches) if matches else 0
                }
            except Exception as e:
                return {"error": f"Failed to get matches: {str(e)}"}
        
        @self.server.tool()
        async def update_application_status(
            job_id: str,
            status: str,
            notes: Optional[str] = None
        ) -> Dict:
            """Update job application status."""
            valid_statuses = ["APPLIED", "REJECTED", "INTERVIEW", "OFFER"]
            if status not in valid_statuses:
                return {"error": f"Invalid status. Must be one of: {valid_statuses}"}
            
            try:
                old_status = await self.database.get_job_status(job_id)
                success = await self.database.update_status(job_id, status, notes)
                
                if success:
                    return {
                        "success": True,
                        "job_id": job_id,
                        "old_status": old_status,
                        "new_status": status,
                        "updated_at": datetime.now().isoformat()
                    }
                else:
                    return {"error": "Failed to update status"}
            except Exception as e:
                return {"error": f"Update failed: {str(e)}"}
        
        @self.server.tool()
        async def check_email_now(
            job_boards: Optional[List[str]] = None
        ) -> Dict:
            """Trigger immediate email check."""
            try:
                results = await self.email_monitor.check_now(job_boards)
                return {
                    "emails_processed": results["emails_processed"],
                    "new_jobs_found": results["new_jobs"],
                    "analysis_complete": results["analyzed"],
                    "errors": results["errors"]
                }
            except Exception as e:
                return {"error": f"Email check failed: {str(e)}"}

    async def start(self):
        """Initialize components and start server."""
        # Initialize components
        self.email_monitor = EmailMonitor(config)
        self.analyzer = AIJobAnalyzer(config)
        self.database = DatabaseManager(config)
        
        # Start the server
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream=read_stream,
                write_stream=write_stream,
                init_options={}
            )

if __name__ == "__main__":
    server = JobMatcherMCPServer()
    asyncio.run(server.start())
```

## Security Considerations

1. **Credential Protection**: Never expose email passwords through MCP
2. **Rate Limiting**: Implement per-client rate limits
3. **Input Validation**: Sanitize all URLs and user inputs
4. **Access Control**: Consider adding API key authentication

## Monitoring and Logging

```python
# MCP request logging
@self.server.middleware
async def log_requests(request, call_next):
    start_time = time.time()
    tool_name = request.tool_name
    
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        
        logger.info(f"MCP Tool: {tool_name} - Duration: {duration:.2f}s - Status: Success")
        return response
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"MCP Tool: {tool_name} - Duration: {duration:.2f}s - Error: {str(e)}")
        raise
```

## Client Libraries

### Python Client Example
```python
# mcp_client_example.py
from job_matcher_client import JobMatcherClient

async def main():
    client = JobMatcherClient()
    
    # Analyze a specific job
    result = await client.analyze_job("https://example.com/job/123")
    
    if result.match_percentage > 70:
        print(f"Good match! {result.match_percentage}%")
        print("Strengths:", result.strengths)
        
        # Update status
        await client.mark_as_applied(result.job_id)
```

This completes the comprehensive documentation for your job matching automation project. The AI coding agent should now have all the context needed to implement the system from scratch!