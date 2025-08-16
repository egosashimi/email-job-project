# Job Match Automation - Deployment Package

## Package Structure

```
job-match-automation/
├── src/
│   ├── core/
│   ├── analysis/
│   ├── notifications/
│   ├── storage/
│   ├── mcp/
│   └── main.py
├── data/
│   └── (empty - created on first run)
├── config/
│   └── .env.example
├── docs/
├── tests/
├── scripts/
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## Installation Instructions

### 1. System Requirements

- Python 3.13 or later
- pip package manager
- Git (for cloning repository)

### 2. Installation Steps

#### Option A: Install from GitHub

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

#### Option B: Install from PyPI (if published)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package
pip install job-match-automation
```

### 3. Configuration

1. Copy the example configuration:
   ```bash
   cp config/.env.example .env
   ```

2. Edit `.env` with your credentials:
   ```env
   EMAIL_ADDRESS=your-email@gmail.com
   EMAIL_PASSWORD=your-app-password
   OPENROUTER_API_KEY=your-openrouter-api-key
   DISCORD_WEBHOOK_URL=your-discord-webhook-url  # Optional
   ```

3. Place your resume in `data/resume.txt`

### 4. Database Initialization

The database will be automatically created on first run. No additional steps are required.

## Running the Application

### 1. One-Time Email Check

```bash
python src/main.py --check
```

### 2. Continuous Email Monitoring

```bash
python src/main.py --monitor
```

### 3. MCP Server Mode

```bash
python src/mcp/server.py
```

## Systemd Service (Linux)

Create a systemd service file for automatic startup:

```ini
# /etc/systemd/system/job-match-automation.service
[Unit]
Description=Job Match Automation
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/job-match-automation
ExecStart=/path/to/job-match-automation/venv/bin/python src/main.py --monitor
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable job-match-automation
sudo systemctl start job-match-automation
```

## Docker Deployment

Create a Dockerfile:

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "src/main.py", "--monitor"]
```

Build and run:

```bash
docker build -t job-match-automation .
docker run -d --name job-matcher job-match-automation
```

## Configuration Management

### Environment Variables

All configuration is managed through environment variables:

- `EMAIL_ADDRESS`: Your Gmail address
- `EMAIL_PASSWORD`: Your Gmail app password
- `OPENROUTER_API_KEY`: DeepSeek API key via OpenRouter
- `DISCORD_WEBHOOK_URL`: Discord webhook URL (optional)
- `DATABASE_PATH`: Path to SQLite database (default: data/jobs.db)

### Resume Management

Place your resume in `data/resume.txt`. The system supports text resumes and can extract:

- Experience years
- Skills
- Education
- Location
- Salary expectations

## Data Management

### Database

The application uses SQLite for data storage. The database file is located at `data/jobs.db` by default.

### Backup Strategy

Regular backups are recommended:

```bash
# Backup database
cp data/jobs.db data/backups/jobs_$(date +%Y%m%d).db

# Backup exports
cp -r data/exports data/backups/exports_$(date +%Y%m%d)/
```

### Data Retention

- Job data: Indefinite
- Analysis results: Indefinite
- Application tracking: Indefinite
- Email tracking: Indefinite

## Monitoring and Maintenance

### Log Files

Logs are output to stdout/stderr. For systemd deployments, logs can be viewed with:

```bash
journalctl -u job-match-automation -f
```

### Health Checks

Monitor the following for system health:

1. Database file accessibility
2. Email connection status
3. AI API quota usage
4. Discord webhook functionality
5. Disk space availability

### Updates

To update the application:

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt

# Restart service
sudo systemctl restart job-match-automation
```

## Troubleshooting

### Common Issues

1. **Email Connection Failed**
   - Verify email address and app password
   - Check Gmail IMAP settings
   - Ensure app password is used, not account password

2. **AI Analysis Not Working**
   - Verify OpenRouter API key
   - Check API quota limits
   - Ensure internet connectivity

3. **Discord Notifications Not Sending**
   - Verify webhook URL
   - Check Discord channel permissions
   - Ensure webhook hasn't been deleted

4. **Database Errors**
   - Check file permissions
   - Ensure sufficient disk space
   - Verify database isn't locked

### Log Analysis

Check logs for error patterns:

```bash
# View recent errors
grep -i error /var/log/job-match-automation.log

# Count errors by type
grep -i error /var/log/job-match-automation.log | cut -d' ' -f3 | sort | uniq -c
```

## Security Considerations

### Data Encryption

- Email credentials are encrypted at rest
- Resume data is encrypted at rest
- Database is stored locally with file system permissions

### API Security

- Use app passwords for Gmail, not account passwords
- Store API keys securely
- Rotate keys regularly

### Network Security

- All external communications use HTTPS
- No sensitive data is transmitted in plaintext
- Firewall rules should restrict unnecessary access

## Performance Optimization

### Resource Usage

- CPU: Minimal during normal operation
- Memory: ~50MB baseline
- Disk: ~10MB per 1000 jobs stored

### Scaling Considerations

For high-volume deployments:

1. Use a more robust database (PostgreSQL)
2. Implement connection pooling
3. Add load balancing
4. Use caching for frequent queries

### Memory Management

The application automatically manages memory:

- Database connections are properly closed
- HTTP sessions are cleaned up
- Temporary files are deleted

## Backup and Recovery

### Backup Procedures

Daily backups recommended:

```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d)
BACKUP_DIR="/path/to/backups"

# Backup database
cp data/jobs.db $BACKUP_DIR/jobs_$DATE.db

# Backup exports
cp -r data/exports $BACKUP_DIR/exports_$DATE/

# Keep only last 30 days of backups
find $BACKUP_DIR -name "jobs_*" -mtime +30 -delete
find $BACKUP_DIR -name "exports_*" -mtime +30 -delete
```

### Recovery Procedures

To restore from backup:

```bash
# Stop application
sudo systemctl stop job-match-automation

# Restore database
cp /path/to/backups/jobs_20240115.db data/jobs.db

# Start application
sudo systemctl start job-match-automation
```

## Maintenance Procedures

### Regular Maintenance Tasks

1. **Weekly**: Check disk space usage
2. **Monthly**: Review and clean old data
3. **Quarterly**: Update dependencies
4. **Annually**: Security audit

### Database Maintenance

```bash
# Vacuum database to reclaim space
sqlite3 data/jobs.db "VACUUM;"

# Check database integrity
sqlite3 data/jobs.db "PRAGMA integrity_check;"
```

### Dependency Updates

```bash
# Update pip
pip install --upgrade pip

# Update dependencies
pip install --upgrade -r requirements.txt

# Check for security vulnerabilities
pip audit
```