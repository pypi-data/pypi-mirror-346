from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# load the environment variables
load_dotenv()

app = FastMCP("mcp-alteryx-server",
    prompt="""
# MCP Wrapper for Alteryx server

This MCP server provides tools for querying the remote Alteryx server using the Alteryx V3 API. It allows you to CRUD operations on Alteryx workflows, collections, users, jobs, connections and credendentials stored in the Alteryx server.

## Available Tools

### 1. get_workflows
Use this tool to get a list of workflows from the Alteryx server.

Example: "List all the workflows in the Alteryx server"

### 2. get_collections
Use this tool to get a list of collections from the Alteryx server.

Example: "List all the collections used by the user 'John Doe' in the Alteryx server"

### 3. get_users
Use this tool to get a list of users from the Alteryx server.

Example: "List all the users in the Alteryx server"

### 4. get_job_results
Use this tool to get the results of a workflow run from the Alteryx server.

Example: "List all the results of the workflow 'Workflow 1' in the Alteryx server"

### etc...

## Guidelines for Use

- Always check if a query would is about a workflow, a collection, a user, a job, a connection or a credential
- Keep queries concise and specific for best results
- Rate limits apply to all queries (typically 1 request/second)

## Output Format

All queries will be formatted as JSON for all results objects extracted from the Alteryx server.

- Workflow: Name, Description, and Created Date
- Collection: Name, Description, and Created Date
- User: Name, Email, and Created Date
- Job: Name, Description, and Created Date
- Connection: Name, Description, and Created Date
- Credential: Name, Description, and Created Date

If the API key is missing or invalid, appropriate error messages will be returned.
""")