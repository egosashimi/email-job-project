# Job Match Automation - Quick Start Guide

## Getting Started in 5 Minutes

### 1. Prerequisites

- Python 3.13 or later
- Gmail account
- OpenRouter API key (free tier available)

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/your-username/job-match-automation.git
cd job-match-automation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

1. Copy the example configuration:
   ```bash
   cp config/.env.example .env
   ```

2. Edit `.env` with your credentials:
   ```env
   EMAIL_ADDRESS=your-email@gmail.com
   EMAIL_PASSWORD=your-gmail-app-password
   OPENROUTER_API_KEY=your-openrouter-api-key
   ```

3. Place your resume in `data/resume.txt`

### 4. Run a Quick Check

```bash
python src/main.py --check
```

This will check your email for job postings and analyze any found jobs.

### 5. Set Up Notifications (Optional)

Add your Discord webhook URL to `.env` for job notifications:
```env
DISCORD_WEBHOOK_URL=your-discord-webhook-url
```

## First Run

After configuration, run a one-time check to see the system in action:

```bash
python src/main.py --check
```

You should see output similar to:
```
Starting email monitoring...
Found 2 job emails.
Processing email from jobs-noreply@linkedin.com
Found 1 job links in email.
Stored job: Python Developer at TechCorp
Processing email from noreply@indeed.com
Found 3 job links in email.
Stored job: Full Stack Developer at StartupXYZ
Stored job: Senior Engineer at BigCorp
Stored job: Data Scientist at DataCorp
Email monitoring completed.
```

## Understanding the Results

The system will:

1. **Find job emails** from LinkedIn, Indeed, ZipRecruiter, and other job boards
2. **Extract job links** from those emails
3. **Store job information** in the local database
4. **Analyze job matches** using AI against your resume
5. **Send notifications** for matches above 60% (if configured)

## Next Steps

### Continuous Monitoring

To continuously monitor your email:

```bash
python src/main.py --monitor
```

This will check your email every hour for new job postings.

### MCP Server Mode

To use the system as an MCP tool server:

```bash
python src/mcp/server.py
```

This exposes all functionality as MCP tools for integration with other applications.

### Track Applications

Update application status using MCP tools:

```bash
# This would be called through an MCP client
update_application_status(job_id="linkedin-123", status="APPLIED")
```

## Common Tasks

### View Recent Matches

```bash
# Through MCP tools
get_recent_matches(hours=24, min_percentage=60)
```

### Export Data

```bash
# Through MCP tools
export_matches_csv(start_date="2024-01-01", end_date="2024-01-31")
```

### Check System Statistics

```bash
# Through MCP tools
get_match_statistics(days=7)
```

## Troubleshooting

### No Jobs Found

1. Check that you're receiving job emails from supported job boards
2. Verify your email credentials are correct
3. Ensure IMAP is enabled in Gmail settings

### AI Analysis Failing

1. Verify your OpenRouter API key is correct
2. Check that you haven't exceeded free tier limits
3. Ensure you have internet connectivity

### Notifications Not Working

1. Verify your Discord webhook URL is correct
2. Check that the webhook hasn't been deleted
3. Ensure the Discord channel is accessible

## Need Help?

- Check the full documentation in `docs/`
- Open an issue on GitHub
- Contact support at support@jobmatchautomation.com

## Ready to Go!

You're now ready to use Job Match Automation to find your perfect job matches. The system will help you focus on opportunities that align with your experience and skills, saving you time and increasing your chances of landing interviews.