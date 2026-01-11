# simple_agent.py
from strands import Agent
from strands.models import BedrockModel
from bedrock_agentcore.runtime import BedrockAgentCoreApp
import boto3
import json

# Initialize S3 client
s3_client = boto3.client('s3', region_name='us-west-2')

# Create Bedrock Model
model = BedrockModel(
    model_id="us.amazon.nova-pro-v1:0",
    temperature=0.7,
    max_tokens=1000
)

# Define S3 tool function
def read_s3_file(bucket_name: str, file_key: str) -> str:
    """
    Read a file from S3 bucket

    Args:
        bucket_name: Name of the S3 bucket
        file_key: Key/path of the file in S3

    Returns:
        Content of the file
    """
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        content = response['Body'].read().decode('utf-8')
        return f"File content from s3://{bucket_name}/{file_key}:
{content}"
    except Exception as e:
        return f"Error reading file: {str(e)}"

# Create Strands agent with S3 tool
agent = Agent(
    model=model,
    system_prompt="""You are a helpful assistant that can read files from S3.
    When asked to read a file, use the read_s3_file tool with the bucket name and file key.
    Be friendly and explain what you're doing.""",
    tools=[read_s3_file]
)

# AgentCore application wrapper
app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload: dict) -> dict:
    """
    AgentCore Runtime entrypoint
    Expects payload: {"prompt": "your question here"}
    """
    user_message = payload.get("prompt", "Hello! What can you help me with?")

    # Call the agent
    result = agent(user_message)

    return {
        "answer": str(result),
        "status": "success"
    }

if __name__ == "__main__":
    # Local dev server
    app.run()