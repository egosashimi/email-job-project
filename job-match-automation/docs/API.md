# Job Match Automation - API Documentation

## Overview

The Job Match Automation system exposes functionality through MCP (Model Context Protocol) tools. These tools can be accessed through the MCP server or integrated into other applications.

## MCP Server

The MCP server runs on stdin/stdout and exposes the following tools:

### Server Startup

```bash
python src/mcp/server.py
```

## Tools

### analyze_job_url

Analyze a specific job posting against your resume.

**Request:**
```json
{
  "method": "call_tool",
  "params": {
    "name": "analyze_job_url",
    "arguments": {
      "url": "https://example.com/job/123",
      "resume_path": "data/resume.txt"
    }
  }
}
```

**Response:**
```json
{
  "result": {
    "match_percentage": 75,
    "recommendation": "POSSIBLE_MATCH",
    "strengths": [
      "Python experience matches requirement",
      "Located in same city"
    ],
    "weaknesses": [
      "Missing AWS experience"
    ],
    "apply_url": "https://example.com/job/123"
  }
}
```

**Parameters:**
- `url` (string, required): Job posting URL
- `resume_path` (string, optional): Path to resume file (defaults to `data/resume.txt`)

**Response Fields:**
- `match_percentage` (integer): Match percentage (0-100)
- `recommendation` (string): Job recommendation (STRONG_MATCH, POSSIBLE_MATCH, REACH, SKIP)
- `strengths` (array): List of strengths for this position
- `weaknesses` (array): List of areas for improvement
- `apply_url` (string): Original job posting URL

### get_recent_matches

Retrieve recent job matches above a specified threshold.

**Request:**
```json
{
  "method": "call_tool",
  "params": {
    "name": "get_recent_matches",
    "arguments": {
      "hours": 24,
      "min_percentage": 60,
      "include_applied": false
    }
  }
}
```

**Response:**
```json
{
  "result": {
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
}
```

**Parameters:**
- `hours` (integer, optional): Hours to look back (default: 24)
- `min_percentage` (integer, optional): Minimum match percentage (default: 60)
- `include_applied` (boolean, optional): Include already applied jobs (default: false)

**Response Fields:**
- `matches` (array): List of recent job matches
- `total_count` (integer): Total number of matches
- `average_match` (number): Average match percentage

### update_application_status

Update the application status for a job.

**Request:**
```json
{
  "method": "call_tool",
  "params": {
    "name": "update_application_status",
    "arguments": {
      "job_id": "linkedin-123",
      "status": "APPLIED",
      "notes": "Applied via LinkedIn on 2024-01-15"
    }
  }
}
```

**Response:**
```json
{
  "result": {
    "success": true,
    "job_id": "linkedin-123",
    "new_status": "APPLIED"
  }
}
```

**Parameters:**
- `job_id` (string, required): Job identifier
- `status` (string, required): Status (APPLIED, REJECTED, INTERVIEW, OFFER)
- `notes` (string, optional): Additional notes

**Response Fields:**
- `success` (boolean): Whether the update was successful
- `job_id` (string): Job identifier
- `new_status` (string): New application status

### export_matches_csv

Export job matches to CSV for a date range.

**Request:**
```json
{
  "method": "call_tool",
  "params": {
    "name": "export_matches_csv",
    "arguments": {
      "start_date": "2024-01-01",
      "end_date": "2024-01-15",
      "min_percentage": 70
    }
  }
}
```

**Response:**
```json
{
  "result": {
    "filepath": "/data/exports/jobs_2024-01-01_to_2024-01-15.csv",
    "record_count": 47,
    "file_size_kb": 12.3
  }
}
```

**Parameters:**
- `start_date` (string, required): ISO format date (YYYY-MM-DD)
- `end_date` (string, required): ISO format date (YYYY-MM-DD)
- `min_percentage` (integer, optional): Minimum match percentage to include

**Response Fields:**
- `filepath` (string): Path to the exported CSV file
- `record_count` (integer): Number of records exported
- `file_size_kb` (number): File size in kilobytes

### check_email_now

Trigger immediate email check instead of waiting for schedule.

**Request:**
```json
{
  "method": "call_tool",
  "params": {
    "name": "check_email_now",
    "arguments": {
      "job_boards": ["linkedin.com", "indeed.com"]
    }
  }
}
```

**Response:**
```json
{
  "result": {
    "emails_processed": 8,
    "new_jobs_found": 12,
    "analysis_complete": 10,
    "errors": 2
  }
}
```

**Parameters:**
- `job_boards` (array, optional): Specific job boards to check

**Response Fields:**
- `emails_processed` (integer): Number of emails processed
- `new_jobs_found` (integer): Number of new jobs found
- `analysis_complete` (integer): Number of job analyses completed
- `errors` (integer): Number of errors encountered

### get_match_statistics

Get statistics about job matching performance.

**Request:**
```json
{
  "method": "call_tool",
  "params": {
    "name": "get_match_statistics",
    "arguments": {
      "days": 7
    }
  }
}
```

**Response:**
```json
{
  "result": {
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
}
```

**Parameters:**
- `days` (integer, optional): Days to analyze (default: 7)

**Response Fields:**
- `total_jobs_analyzed` (integer): Total number of jobs analyzed
- `average_match_percentage` (number): Average match percentage
- `matches_by_recommendation` (object): Count of matches by recommendation
- `application_conversion` (object): Application conversion statistics
- `top_companies` (array): Top companies by job count

## Data Structures

### Job Match

```json
{
  "job_id": "string",
  "company": "string",
  "title": "string",
  "match_percentage": "integer",
  "recommendation": "string",
  "analyzed_at": "string",
  "status": "string"
}
```

### Analysis Result

```json
{
  "match_percentage": "integer",
  "strengths": ["string"],
  "weaknesses": ["string"],
  "hidden_opportunities": ["string"],
  "red_flags": ["string"],
  "recommendation": "string",
  "reasoning": "string"
}
```

### Application Status

```json
{
  "job_id": "string",
  "status": "string",
  "applied_at": "string",
  "updated_at": "string",
  "notes": "string"
}
```

## Error Handling

All tools return errors in the following format:

```json
{
  "error": {
    "code": "integer",
    "message": "string"
  }
}
```

### Common Error Codes

- `-32601`: Method or tool not found
- `-32603`: Internal error
- `-32700`: Parse error

## Integration Examples

### Python Client

```python
import json
import subprocess

def call_mcp_tool(tool_name, arguments):
    # Start MCP server
    process = subprocess.Popen(
        ['python', 'src/mcp/server.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Call tool
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "call_tool",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    
    process.stdin.write(json.dumps(request) + '\n')
    process.stdin.flush()
    
    # Read response
    response = process.stdout.readline()
    return json.loads(response)

# Example usage
result = call_mcp_tool("get_recent_matches", {"hours": 24, "min_percentage": 60})
print(result)
```

### Command Line Usage

```bash
# Start MCP server
python src/mcp/server.py

# In another terminal, send requests via stdin
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools", "params": {}}' | python src/mcp/server.py
```