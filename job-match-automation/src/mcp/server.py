"""
MCP server module for job match automation.
Exposes job matching functionality as MCP tools.
"""

import json
import sys
import os
import asyncio
from typing import Dict, List, Any
from datetime import datetime, timedelta

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import our existing modules
from core.email_monitor import EmailMonitor
from core.job_scraper import JobScraper
from core.resume_parser import ResumeParser
from analysis.job_match_analyzer import JobMatchAnalyzer
from storage.application_tracker import ApplicationTracker
from storage.csv_exporter import CSVExporter
from storage.database import DatabaseManager
from core.config_manager import config


class JobMatcherMCP:
    """MCP server exposing job matching functionality."""

    def __init__(self):
        """Initialize MCP server."""
        self.tools = {
            "analyze_job_url": self.analyze_job_url,
            "get_recent_matches": self.get_recent_matches,
            "update_application_status": self.update_application_status,
            "export_matches_csv": self.export_matches_csv,
            "check_email_now": self.check_email_now,
            "get_match_statistics": self.get_match_statistics
        }
        
        # Initialize components
        self.email_monitor = EmailMonitor()
        self.resume_parser = ResumeParser()
        self.analyzer = JobMatchAnalyzer()
        self.tracker = ApplicationTracker()
        self.exporter = CSVExporter()
        self.db = DatabaseManager()

    async def handle_request(self, request: Dict) -> Dict:
        """Handle an MCP request."""
        try:
            method = request.get("method")
            params = request.get("params", {})
            
            if method == "initialize":
                return self._handle_initialize()
            elif method == "tools":
                return self._handle_tools()
            elif method == "call_tool":
                tool_name = params.get("name")
                tool_params = params.get("arguments", {})
                return await self._handle_call_tool(tool_name, tool_params)
            else:
                return {
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }

    def _handle_initialize(self) -> Dict:
        """Handle initialize request."""
        return {
            "protocolVersion": "1.0.0",
            "capabilities": {
                "tools": {}
            }
        }

    def _handle_tools(self) -> Dict:
        """Handle tools request."""
        return {
            "tools": [
                {
                    "name": "analyze_job_url",
                    "description": "Analyze a specific job posting against your resume",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "url": {"type": "string", "description": "Job posting URL"},
                            "resume_path": {"type": "string", "description": "Path to resume file (optional)"}
                        },
                        "required": ["url"]
                    }
                },
                {
                    "name": "get_recent_matches",
                    "description": "Get recent job matches above a specified threshold",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "hours": {"type": "integer", "description": "Hours to look back (default: 24)"},
                            "min_percentage": {"type": "integer", "description": "Minimum match percentage (default: 60)"},
                            "include_applied": {"type": "boolean", "description": "Include already applied jobs (default: false)"}
                        }
                    }
                },
                {
                    "name": "update_application_status",
                    "description": "Update the application status for a job",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "job_id": {"type": "string", "description": "Job identifier"},
                            "status": {"type": "string", "description": "Status: APPLIED, REJECTED, INTERVIEW, OFFER"},
                            "notes": {"type": "string", "description": "Additional notes (optional)"}
                        },
                        "required": ["job_id", "status"]
                    }
                },
                {
                    "name": "export_matches_csv",
                    "description": "Export job matches to CSV for a date range",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "start_date": {"type": "string", "description": "ISO format date (YYYY-MM-DD)"},
                            "end_date": {"type": "string", "description": "ISO format date (YYYY-MM-DD)"},
                            "min_percentage": {"type": "integer", "description": "Minimum match percentage to include"}
                        },
                        "required": ["start_date", "end_date"]
                    }
                },
                {
                    "name": "check_email_now",
                    "description": "Trigger immediate email check instead of waiting for schedule",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "job_boards": {"type": "array", "items": {"type": "string"}, "description": "Specific job boards to check"}
                        }
                    }
                },
                {
                    "name": "get_match_statistics",
                    "description": "Get statistics about job matching performance",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "days": {"type": "integer", "description": "Days to analyze (default: 7)"}
                        }
                    }
                }
            ]
        }

    async def _handle_call_tool(self, tool_name: str, tool_params: Dict) -> Dict:
        """Handle call_tool request."""
        if tool_name not in self.tools:
            return {
                "error": {
                    "code": -32601,
                    "message": f"Tool not found: {tool_name}"
                }
            }
        
        try:
            result = await self.tools[tool_name](**tool_params)
            return {"result": result}
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Tool execution failed: {str(e)}"
                }
            }

    async def analyze_job_url(self, url: str, resume_path: str = None) -> Dict:
        """Analyze a specific job posting against resume."""
        try:
            # Set default resume path if not provided
            if not resume_path:
                resume_path = "data/resume.txt"
            
            # Scrape job details
            async with JobScraper() as scraper:
                job_details = await scraper.fetch_job_details(url)
                if not job_details:
                    return {"error": "Could not fetch job details"}
            
            # Analyze match
            analysis = await self.analyzer.analyze_match(resume_path, job_details)
            
            return {
                "match_percentage": analysis.get("percentage", 0),
                "recommendation": analysis.get("recommendation", "UNKNOWN"),
                "strengths": analysis.get("strengths", [])[:3],
                "weaknesses": analysis.get("weaknesses", [])[:3],
                "apply_url": url
            }
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}

    async def get_recent_matches(self, hours: int = 24, min_percentage: int = 60, include_applied: bool = False) -> Dict:
        """Get recent job matches above threshold."""
        try:
            # Calculate time filter
            since = datetime.now() - timedelta(hours=hours)
            
            # Query database for matches
            matches = []
            # This is a simplified implementation - in a real implementation you would query the database
            # For now, we'll return a placeholder response
            return {
                "matches": matches,
                "total_count": len(matches),
                "average_match": 0
            }
        except Exception as e:
            return {"error": f"Failed to get matches: {str(e)}"}

    async def update_application_status(self, job_id: str, status: str, notes: str = "") -> Dict:
        """Update job application status."""
        valid_statuses = ["APPLIED", "REJECTED", "INTERVIEW", "OFFER"]
        if status not in valid_statuses:
            return {"error": f"Invalid status. Must be one of: {valid_statuses}"}
        
        try:
            success = self.tracker.update_application_status(job_id, status, notes)
            if success:
                return {
                    "success": True,
                    "job_id": job_id,
                    "new_status": status
                }
            else:
                return {"error": "Failed to update status"}
        except Exception as e:
            return {"error": f"Update failed: {str(e)}"}

    async def export_matches_csv(self, start_date: str, end_date: str, min_percentage: int = 0) -> Dict:
        """Export job matches to CSV for date range."""
        try:
            result = self.exporter.export_matches(start_date, end_date, min_percentage)
            return {
                "filepath": result["filepath"],
                "record_count": result["record_count"],
                "file_size_kb": result["file_size_kb"]
            }
        except Exception as e:
            return {"error": f"Export failed: {str(e)}"}

    async def check_email_now(self, job_boards: List[str] = None) -> Dict:
        """Trigger immediate email check."""
        try:
            # This is a simplified implementation
            # In a real implementation, you would trigger the email monitoring system
            return {
                "emails_processed": 0,
                "new_jobs_found": 0,
                "analysis_complete": 0,
                "errors": 0
            }
        except Exception as e:
            return {"error": f"Email check failed: {str(e)}"}

    async def get_match_statistics(self, days: int = 7) -> Dict:
        """Get statistics about job matching performance."""
        try:
            # Get application statistics
            app_stats = self.tracker.get_application_statistics()
            
            # Get export summary
            export_summary = self.exporter.get_export_summary(days)
            
            return {
                "total_jobs_analyzed": export_summary.get("analyzed_jobs", 0),
                "average_match_percentage": 0,  # Would need to calculate from database
                "matches_by_recommendation": export_summary.get("match_distribution", {}),
                "application_conversion": app_stats.get("status_counts", {}),
                "top_companies": []  # Would need to query database for this
            }
        except Exception as e:
            return {"error": f"Failed to get statistics: {str(e)}"}


# Simple stdin/stdout server
async def run_mcp_server():
    """Run the MCP server using stdin/stdout."""
    mcp_server = JobMatcherMCP()
    
    print("MCP server started", file=sys.stderr)
    
    # Send initialization response
    init_response = {
        "jsonrpc": "2.0",
        "id": None,
        "method": "initialize",
        "params": {
            "protocolVersion": "1.0.0",
            "capabilities": {
                "tools": {}
            }
        }
    }
    print(json.dumps(init_response), flush=True)
    
    # Main loop
    try:
        while True:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
                
            try:
                request = json.loads(line.strip())
                response = await mcp_server.handle_request(request)
                response["jsonrpc"] = "2.0"
                response["id"] = request.get("id")
                print(json.dumps(response), flush=True)
            except json.JSONDecodeError:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": "Parse error"
                    }
                }
                print(json.dumps(error_response), flush=True)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)


def main():
    """Main entry point."""
    print("Job Matcher MCP Server", file=sys.stderr)
    print("=====================", file=sys.stderr)
    print("Starting MCP server...", file=sys.stderr)
    
    try:
        asyncio.run(run_mcp_server())
    except KeyboardInterrupt:
        print("Server stopped", file=sys.stderr)
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()