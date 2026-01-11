from bedrock_agentcore import BedrockAgentCoreApp 
from strands import Agent, tool 
from strands_tools import calculator  
from strands.models import BedrockModel 
import logging 

app = BedrockAgentCoreApp(debug=True) 

# Logging setup 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 

# Create a custom tool  
@tool 
def weather(): 
     """ Get weather """  
     return "sunny" 

model_id = "us.anthropic.claude-sonnet-4-20250514-v1:0" 
model = BedrockModel( 
     model_id=model_id, 
) 

agent = Agent( 
     model=model, 
     tools=[calculator, weather], 
     system_prompt="You're a helpful assistant. You can do simple math calculation, and tell the weather." 
) 

@app.entrypoint 
def invoke(payload): 
     """Your AI agent function""" 
     user_input = payload.get("prompt", "Hello! How can I help you today?") 
     logger.info("\n User input: %s", user_input) 
     response = agent(user_input) 
     logger.info("\n Agent result: %s ", response.message) 
     return response.message['content'][0]['text'] 

if __name__ == "__main__": 
     app.run()