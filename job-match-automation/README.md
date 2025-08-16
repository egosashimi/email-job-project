# Job Match Automation

An automated email monitoring system that analyzes job postings from multiple job boards against a user's resume, providing brutally honest match assessments via Discord notifications and data exports.

## Features

- Monitor Gmail for job emails from LinkedIn, Indeed, ZipRecruiter, Y Combinator, Startup Jobs
- Follow email links to fetch actual job descriptions
- Compare jobs against resume using AI (DeepSeek via OpenRouter)
- Provide honest match percentage focusing on experience alignment
- Send Discord notifications for viable matches (>60% recommended)
- Track application history and responses
- Export data to CSV and future web interface
- MCP server for tool integration

## Technical Requirements

- Python 3.13
- DeepSeek API access via OpenRouter
- Gmail account with app password
- Discord webhook URL

## Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
4. Install dependencies: `pip install -r requirements.txt`

## Configuration

1. Copy `.env.example` to `.env`
2. Fill in your credentials and configuration values
3. Encrypt your resume using the provided script

## Usage

1. Run the email monitor: `python src/main.py --monitor`
2. Run a one-time check: `python src/main.py --check`
3. Start the MCP server: `python src/main.py --mcp`

## License

MIT