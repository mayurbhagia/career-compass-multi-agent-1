# invoke_demo.py
import boto3
import json

# Initialize AgentCore client
client = boto3.client('bedrock-agentcore-runtime', region_name='us-west-2')

# Your runtime ARN from deployment
RUNTIME_ARN = "arn:aws:bedrock-agentcore:us-west-2:596174723673:runtime/simple-demo-agent"

# Invoke the agent
response = client.invoke_agent_runtime(
    agentRuntimeArn=RUNTIME_ARN,
    sessionId='demo-session-1',
    inputText=json.dumps({
        "prompt": "Can you read the demo.txt file from my S3 bucket?"
    })
)

# Print response
print("Agent Response:")
for event in response['output']:
    if 'chunk' in event:
        print(event['chunk']['bytes'].decode('utf-8'))