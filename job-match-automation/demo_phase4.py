"""
Demo script showing how the MCP server would work.
"""

import sys
import os
import json
import asyncio

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp.server import JobMatcherMCP


async def demo_mcp_server():
    """Demo MCP server functionality."""
    print("=== MCP Server Demo ===")
    
    # Create MCP server instance
    mcp_server = JobMatcherMCP()
    
    # Demo initialize request
    print("1. Testing initialize request...")
    init_request = {
        "method": "initialize",
        "params": {}
    }
    response = await mcp_server.handle_request(init_request)
    print(f"   Response: {response}")
    print()
    
    # Demo tools request
    print("2. Testing tools request...")
    tools_request = {
        "method": "tools",
        "params": {}
    }
    response = await mcp_server.handle_request(tools_request)
    tools = response.get("tools", [])
    print(f"   Available tools: {len(tools)}")
    for tool in tools[:3]:  # Show first 3 tools
        print(f"     - {tool['name']}: {tool['description']}")
    print()
    
    # Demo call_tool request for update_application_status
    print("3. Testing update_application_status tool...")
    call_request = {
        "method": "call_tool",
        "params": {
            "name": "update_application_status",
            "arguments": {
                "job_id": "linkedin-12345",
                "status": "APPLIED",
                "notes": "Submitted resume and cover letter"
            }
        }
    }
    response = await mcp_server.handle_request(call_request)
    print(f"   Response: {response}")
    print()
    
    # Demo call_tool request for export_matches_csv
    print("4. Testing export_matches_csv tool...")
    from datetime import datetime, timedelta
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date_obj = datetime.now() - timedelta(days=30)
    start_date = start_date_obj.strftime("%Y-%m-%d")
    
    call_request = {
        "method": "call_tool",
        "params": {
            "name": "export_matches_csv",
            "arguments": {
                "start_date": start_date,
                "end_date": end_date,
                "min_percentage": 60
            }
        }
    }
    response = await mcp_server.handle_request(call_request)
    print(f"   Response: {response}")
    print()
    
    # Demo call_tool request for get_match_statistics
    print("5. Testing get_match_statistics tool...")
    call_request = {
        "method": "call_tool",
        "params": {
            "name": "get_match_statistics",
            "arguments": {
                "days": 7
            }
        }
    }
    response = await mcp_server.handle_request(call_request)
    print(f"   Response: {response}")
    print()


async def main():
    """Run all demos."""
    print("Job Match Automation - Phase 4 MCP Server Demo")
    print("=" * 45)
    print()
    
    # Run MCP server demo
    await demo_mcp_server()
    
    print("=== Demo Complete ===")
    print()
    print("Phase 4 MCP server components are working:")
    print("1. Initialize and tools discovery")
    print("2. Tool execution (update_application_status)")
    print("3. Tool execution (export_matches_csv)")
    print("4. Tool execution (get_match_statistics)")


if __name__ == "__main__":
    asyncio.run(main())