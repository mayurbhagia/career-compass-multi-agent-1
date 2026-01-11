import json
import uuid
import boto3

agent_arn = "arn:aws:bedrock-agentcore:us-west-2:596174723673:runtime/agentcore_simple_demo-rggOl14ojg"

prompt = "How many jobs are in the database?"

# Initialize the Amazon Bedrock AgentCore client
agent_core_client = boto3.client('bedrock-agentcore')

# Prepare the payload
payload = json.dumps({"prompt": prompt}).encode()

# Invoke the agent
response = agent_core_client.invoke_agent_runtime(
    agentRuntimeArn=agent_arn,
    runtimeSessionId=str(uuid.uuid4()),
    payload=payload,
    qualifier="DEFAULT"
)

content = []
for chunk in response.get("response", []):
    content.append(chunk.decode('utf-8'))
print(json.loads(''.join(content)))