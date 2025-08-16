# Job Match Automation - User Guide

## Overview

Job Match Automation is an intelligent system that monitors your email for job postings, analyzes them against your resume, and provides detailed match assessments. The system helps you focus on realistic job opportunities by filtering out positions that don't align with your experience level or skills.

## Key Features

- **Email Monitoring**: Automatically checks Gmail for job emails from major job boards
- **Job Analysis**: Uses AI to analyze job postings against your resume
- **Match Scoring**: Provides detailed match percentages with strengths and weaknesses
- **Discord Notifications**: Sends rich notifications with job details
- **Application Tracking**: Tracks your job application status
- **Data Export**: Exports job matches and application history to CSV
- **MCP Integration**: Exposes functionality as MCP tools for integration

## System Requirements

- Python 3.13 or later
- Gmail account with app password
- DeepSeek API key via OpenRouter (free tier available)
- Discord account for notifications (optional)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/job-match-automation.git
cd job-match-automation
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### 1. Environment Variables

Copy the example configuration file:

```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:

```env
# Email Configuration
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_IMAP_SERVER=imap.gmail.com
EMAIL_IMAP_PORT=993

# Database Configuration
DATABASE_PATH=data/jobs.db

# Encryption Configuration
ENCRYPTION_KEY=  # Leave blank to auto-generate

# Discord Configuration
DISCORD_WEBHOOK_URL=your-discord-webhook-url

# AI Configuration
OPENROUTER_API_KEY=your-openrouter-api-key
```

### 2. Resume Setup

Place your resume in `data/resume.txt`. The system supports text resumes and can extract:

- Experience years
- Skills
- Education
- Location
- Salary expectations

Example resume format:

```
John Doe
New York, NY
john.doe@email.com
(555) 123-4567

SUMMARY
Experienced Python and JavaScript developer with 2 years of professional experience.
Skilled in AI-assisted development and full-stack applications.

SKILLS
Python, JavaScript, React, Node.js, Django, Flask, SQL, PostgreSQL, Git, Docker

EXPERIENCE
Software Developer, TechCorp
2022 - Present
- Developed Python applications using Django and Flask
- Created responsive web interfaces with React
- Implemented RESTful APIs with Node.js

EDUCATION
Bachelor of Science in Computer Science
University of New York, 2021

SALARY EXPECTATIONS
$70,000 - $85,000
```

## Usage

### Running the Email Monitor

To continuously monitor your email for job postings:

```bash
python src/main.py --monitor
```

### One-Time Email Check

To check your email once for new job postings:

```bash
python src/main.py --check
```

### MCP Server Mode

To run the system as an MCP server for tool integration:

```bash
python src/mcp/server.py
```

## Notification System

The system sends Discord notifications for job matches with a match percentage of 60% or higher. Notifications include:

- Match percentage and recommendation
- Job details (company, position, salary, location)
- Your strengths for this position
- Areas for improvement
- Hidden opportunities

### Notification Filtering

By default, notifications are only sent for matches with 60% or higher. You can adjust this threshold in the configuration.

## Application Tracking

Track your job applications using the built-in application tracker:

- **PENDING**: Job identified but not yet applied
- **APPLIED**: Application submitted
- **REJECTED**: Application rejected
- **INTERVIEW**: Interview scheduled or completed
- **OFFER**: Job offer received

Update application status through the MCP tools or directly in the database.

## Data Export

Export your job matches and application history to CSV:

```bash
# Export job matches
python src/storage/csv_exporter.py --export-matches

# Export application history
python src/storage/csv_exporter.py --export-applications
```

## MCP Tools

The system exposes the following MCP tools:

### analyze_job_url

Analyze a specific job posting against your resume.

**Parameters:**
- `url` (string, required): Job posting URL
- `resume_path` (string, optional): Path to resume file

### get_recent_matches

Retrieve recent job matches above a specified threshold.

**Parameters:**
- `hours` (integer, optional): Hours to look back (default: 24)
- `min_percentage` (integer, optional): Minimum match percentage (default: 60)
- `include_applied` (boolean, optional): Include already applied jobs (default: false)

### update_application_status

Update the application status for a job.

**Parameters:**
- `job_id` (string, required): Job identifier
- `status` (string, required): Status (APPLIED, REJECTED, INTERVIEW, OFFER)
- `notes` (string, optional): Additional notes

### export_matches_csv

Export job matches to CSV for a date range.

**Parameters:**
- `start_date` (string, required): ISO format date (YYYY-MM-DD)
- `end_date` (string, required): ISO format date (YYYY-MM-DD)
- `min_percentage` (integer, optional): Minimum match percentage

### check_email_now

Trigger immediate email check instead of waiting for schedule.

**Parameters:**
- `job_boards` (array, optional): Specific job boards to check

### get_match_statistics

Get statistics about job matching performance.

**Parameters:**
- `days` (integer, optional): Days to analyze (default: 7)

## Troubleshooting

### Email Connection Issues

1. Verify your email address and app password are correct
2. Ensure "Less secure app access" is disabled (use app passwords instead)
3. Check that IMAP is enabled in your Gmail settings

### Discord Notifications Not Working

1. Verify your Discord webhook URL is correct
2. Check that the webhook hasn't been deleted or revoked
3. Ensure the Discord channel exists and is accessible

### AI Analysis Failures

1. Verify your OpenRouter API key is correct
2. Check that you haven't exceeded the free tier limits
3. Ensure you have internet connectivity

### Database Issues

1. Check that the database file is writable
2. Ensure sufficient disk space is available
3. Verify database file permissions

## Security

- All sensitive data (email credentials, resume) is encrypted at rest
- Communication with external services uses HTTPS
- API keys are stored securely and never exposed in logs
- Regular security audits are recommended

## Privacy

- Job data is stored locally and never shared with third parties
- Resume data is only used for job matching and is not transmitted externally
- Email content is processed locally and not stored permanently

## Support

For issues, feature requests, or questions, please open an issue on the GitHub repository.