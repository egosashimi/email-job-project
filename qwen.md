# Job Match Automation - Qwen's Source of Truth

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

## Project Structure
```
job-match-automation/
├── src/
│   ├── core/                 # Email monitoring, job scraping, resume parsing
│   ├── analysis/             # AI analysis and match calculation
│   ├── notifications/        # Discord notifications
│   ├── storage/              # Database and export functionality
│   ├── mcp/                  # MCP server implementation
│   └── main.py               # Entry point
├── data/                     # Resume, database, exports
├── config/                   # Configuration files
├── tests/                    # Unit and integration tests
├── docs/                     # Documentation
├── scripts/                  # Utility scripts
├── requirements.txt
├── README.md
└── .gitignore
```

## Database Schema
- **jobs**: Job postings with source, company, title, URL, description, requirements, salary, location
- **analyses**: AI analysis results with match percentage, strengths, weaknesses, recommendation
- **applications**: Application tracking with status (PENDING, APPLIED, REJECTED, INTERVIEW, OFFER)
- **processed_emails**: Email tracking to prevent duplicates

## MCP Server Tools
1. **analyze_job_url**: Analyze specific job posting against resume
2. **get_recent_matches**: Retrieve recent job matches above threshold
3. **update_application_status**: Update job application status
4. **export_matches_csv**: Export job matches to CSV
5. **check_email_now**: Trigger immediate email check
6. **get_match_statistics**: Get statistics about job matching performance

## Error Handling Principles
1. **Graceful Degradation**: Always have fallback methods
2. **Retry Logic**: Exponential backoff for transient failures
3. **Caching**: Store successful results for resilience
4. **Logging**: Comprehensive error logging for debugging
5. **Manual Queue**: Flag items that need human review

## Testing Strategy
- **Unit Tests**: For each component (email parsing, AI analysis, etc.)
- **Integration Tests**: End-to-end workflow testing
- **Performance Tests**: Bulk processing and concurrent operations
- **Test Coverage**: Minimum 80% overall, 95% for critical paths