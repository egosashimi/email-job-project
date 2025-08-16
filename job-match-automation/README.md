# Job Match Automation

An automated email monitoring system that analyzes job postings from multiple job boards against a user's resume, providing brutally honest match assessments via Discord notifications and data exports.

## Project Status
**✅ COMPLETE** - All phases implemented and tested
- Phase 1: Foundation and Core Infrastructure ✅
- Phase 2: AI Analysis and Matching ✅
- Phase 3: Notifications and Application Tracking ✅
- Phase 4: MCP Server and Advanced Features ✅
- Phase 5: Testing and Deployment ✅

## Features

- **Email Monitoring**: Automatically checks Gmail for job emails from LinkedIn, Indeed, ZipRecruiter, Y Combinator, Startup Jobs
- **Job Analysis**: Uses AI to analyze job postings against your resume
- **Match Scoring**: Provides detailed match percentages with strengths and weaknesses
- **Discord Notifications**: Sends rich notifications with job details for matches 60%+
- **Application Tracking**: Tracks your job application status (PENDING, APPLIED, REJECTED, INTERVIEW, OFFER)
- **Data Export**: Exports job matches and application history to CSV
- **MCP Integration**: Exposes functionality as MCP tools for integration with other applications
- **Advanced Analytics**: Comprehensive analytics with trends, conversion rates, and skill demand analysis
- **Performance Monitoring**: System and operation performance tracking
- **Email Scheduling**: Configurable email scheduler with job board specificity

## Technical Requirements

- Python 3.13 or later
- Gmail account with app password
- DeepSeek API access via OpenRouter (free tier available)
- Discord webhook URL (for notifications, optional)

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/job-match-automation.git
   cd job-match-automation
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the system:
   ```bash
   cp config/.env.example .env
   # Edit .env with your credentials
   ```

5. Place your resume in `data/resume.txt`

6. Run a one-time check:
   ```bash
   python src/main.py --check
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

## MCP Tools

The system exposes the following MCP tools:

- `analyze_job_url`: Analyze a specific job posting against your resume
- `get_recent_matches`: Retrieve recent job matches above a specified threshold
- `update_application_status`: Update the application status for a job
- `export_matches_csv`: Export job matches to CSV for a date range
- `check_email_now`: Trigger immediate email check instead of waiting for schedule
- `get_match_statistics`: Get statistics about job matching performance

## Documentation

- [User Guide](docs/USER_GUIDE.md) - Complete user documentation
- [Quick Start Guide](docs/QUICK_START.md) - Rapid deployment guide
- [API Documentation](docs/API.md) - MCP tool API documentation
- [Deployment Guide](docs/DEPLOYMENT.md) - Deployment instructions
- [Release Notes](RELEASE_NOTES.md) - Detailed release information

## System Architecture

```
job-match-automation/
├── src/
│   ├── core/                 # Email monitoring, job scraping, resume parsing, configuration
│   ├── analysis/             # AI analysis, match calculation, rule-based fallback, analytics
│   ├── notifications/        # Discord notifications, notification management
│   ├── storage/              # Database, application tracking, CSV export
│   ├── mcp/                  # MCP server implementation
│   └── main.py               # Entry point
├── data/                     # Database and exports
├── config/                   # Configuration files
├── docs/                     # Documentation
├── tests/                    # Unit and integration tests
├── scripts/                  # Utility scripts
├── requirements.txt          # Main dependencies
├── requirements-dev.txt      # Development dependencies
├── README.md                 # This file
└── .gitignore                # Version control exclusions
```

## Testing

The system includes a comprehensive test suite:

```bash
# Run all tests
python test_runner.py

# Run specific test modules
python -m pytest tests/test_module.py -v
```

## CI/CD

The project includes GitHub Actions workflow for automated testing:

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
      - name: Install dependencies
      - name: Run tests
```

## Security

- All sensitive data (email credentials, resume) is encrypted at rest
- Communication with external services uses HTTPS
- API keys are stored securely and never exposed in logs
- Regular security audits recommended

## Privacy

- Job data is stored locally and never shared with third parties
- Resume data is only used for job matching and is not transmitted externally
- Email content is processed locally and not stored permanently

## Contributing

We welcome contributions from the community:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues, feature requests, or questions, please open an issue on the GitHub repository.