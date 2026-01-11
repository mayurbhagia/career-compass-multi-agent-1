
# agentcore_simple_demo.py (ULTRA-MINIMAL - NO DEPENDENCIES)
import json

def invoke(payload: dict) -> dict:
    """
    AgentCore Runtime entrypoint
    Simplest possible version - no AWS services, no dependencies
    """
    prompt = payload.get("prompt", "")
    
    try:
        # Simple hardcoded response
        answer = f"✅ Hello from AgentCore! You said: '{prompt}'"
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "answer": answer,
                "agent": "agentcore_simple_demo",
                "test": "success"
            })
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e),
                "agent": "agentcore_simple_demo"
            })
        }

# For local testing
if __name__ == "__main__":
    print("Testing locally...")
    result = invoke({"prompt": "Hello!"})
    print(f"Result: {json.loads(result['body'])}")