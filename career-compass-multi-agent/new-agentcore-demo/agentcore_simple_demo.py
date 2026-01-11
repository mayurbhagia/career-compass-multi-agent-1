# agentcore_simple_demo.py (WITH DYNAMODB)
import json
import boto3
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

# Global DynamoDB client (initialized once, reused across invocations)
_dynamodb = None
_table = None

def get_table():
    """Lazy load DynamoDB table"""
    global _dynamodb, _table
    if _table is None:
        _dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        _table = _dynamodb.Table('career-compass-jobs')
    return _table

class AgentCoreHandler(BaseHTTPRequestHandler):
    """HTTP handler for AgentCore Runtime requests"""

    def do_POST(self):
        """Handle POST requests from AgentCore Runtime"""
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            payload = json.loads(post_data.decode('utf-8'))

            # Call the invoke function
            result = invoke(payload)

            # Send response
            self.send_response(result['statusCode'])
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(result['body'].encode('utf-8'))

        except Exception as e:
            # Send error response
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_response = json.dumps({"error": str(e)})
            self.wfile.write(error_response.encode('utf-8'))

    def log_message(self, format, *args):
        """Override to log to stdout for CloudWatch"""
        print(f"[AgentCore] {format % args}")

def invoke(payload: dict) -> dict:
    """
    AgentCore Runtime entrypoint with DynamoDB integration
    Demonstrates MCP tool pattern with AWS service
    """
    prompt = payload.get("prompt", "")

    try:
        table = get_table()

        # MCP Tool 1: Count jobs in DynamoDB
        if "count" in prompt.lower() or "how many" in prompt.lower():
            response = table.scan(Select='COUNT')
            answer = f"✅ There are {response['Count']} jobs in the database."

        # MCP Tool 2: Get sample job from DynamoDB
        elif "show" in prompt.lower() or "example" in prompt.lower() or "sample" in prompt.lower():
            response = table.scan(Limit=1)
            if response['Items']:
                job = response['Items']
                answer = f"""✅ Sample Job from DynamoDB:

**Title:** {job['title']}
**Company:** {job['company']}
**Location:** {job.get('location', 'Not specified')}
**Category:** {job.get('category', 'Not specified')}
**Required Skills:** {', '.join(job.get('required_skills', []))}
**Salary Range:** {job.get('salary_range', 'Not specified')}
**Experience Level:** {job.get('experience_level', 'Not specified')}"""
            else:
                answer = "❌ No jobs found in database."

        # MCP Tool 3: List all jobs
        elif "list" in prompt.lower() or "all jobs" in prompt.lower():
            response = table.scan()
            jobs = response['Items']
            job_list = "".join([f"- {job['title']} at {job['company']}" for job in jobs])
            answer = f"✅ All Jobs in Database ({len(jobs)} total):{job_list}"

        # MCP Tool 4: Search by category
        elif "cloud" in prompt.lower() or "devops" in prompt.lower() or "data" in prompt.lower():
            category = None
            if "cloud" in prompt.lower():
                category = "Cloud"
            elif "devops" in prompt.lower():
                category = "DevOps"
            elif "data" in prompt.lower():
                category = "Data Science"

            if category:
                response = table.scan(
                    FilterExpression='category = :cat',
                    ExpressionAttributeValues={':cat': category}
                )
                jobs = response['Items']
                if jobs:
                    job_list = "".join([f"- {job['title']} at {job['company']}" for job in jobs])
                    answer = f"✅ {category} Jobs ({len(jobs)} found):{job_list}"
                else:
                    answer = f"❌ No {category} jobs found."
            else:
                answer = "Please specify a category: Cloud, DevOps, or Data Science"

        # Default response
        else:
            answer = """✅ Hello from AgentCore with DynamoDB!

I can help you with:
- **Count jobs**: "How many jobs are there?"
- **Show sample**: "Show me an example job"
- **List all**: "List all jobs"
- **Search by category**: "Show me Cloud jobs"

Try asking one of these questions!"""

        return {
            "statusCode": 200,
            "body": json.dumps({
                "answer": answer,
                "agent": "simple_demo_clean",
                "service": "DynamoDB",
                "table": "career-compass-jobs"
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e),
                "agent": "simple_demo_clean"
            })
        }

def run_server(port=8080):
    """Start HTTP server for AgentCore Runtime"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, AgentCoreHandler)
    print(f"🚀 AgentCore Runtime server starting on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    # Check if running in AgentCore Runtime environment
    if os.environ.get('AWS_EXECUTION_ENV'):
        # Running in AgentCore - start server
        run_server()
    else:
        # Running locally - test the invoke function
        print("Testing locally...")

        # Test 1: Count jobs
        result = invoke({"prompt": "How many jobs are there?"})
        print(f"Test 1: {json.loads(result['body'])['answer']}")

        # Test 2: Show sample job
        result = invoke({"prompt": "Show me an example job"})
        print(f"Test 2: {json.loads(result['body'])['answer']}")

        # Test 3: List all jobs
        result = invoke({"prompt": "List all jobs"})
        print(f"Test 3: {json.loads(result['body'])['answer']}")