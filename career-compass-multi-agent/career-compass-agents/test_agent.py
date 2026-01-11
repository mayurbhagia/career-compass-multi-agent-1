import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.career_guidance_agent import CareerGuidanceAgent

def test_career_guidance_agent():
    """Test the Career Guidance Agent"""
    
    # Set your Knowledge Base ID
    KB_ID = os.getenv("KB_ID", "YOUR_KB_ID_HERE")
    
    if KB_ID == "YOUR_KB_ID_HERE":
        print("❌ Error: Please set KB_ID environment variable")
        print("   Example: export KB_ID=your-knowledge-base-id")
        return
    
    # Initialize agent
    print("🚀 Initializing Career Guidance Agent...")
    agent = CareerGuidanceAgent(
        knowledge_base_id=KB_ID,
        region="us-west-2"
    )
    
    # Test queries
    test_queries = [
        "What skills are needed to become a Cloud Engineer?",
        "How should I prepare for technical interviews?",
        "Which universities are best for MS in Computer Science in the US?"
    ]
    
    print("" + "="*60)
    print("TESTING CAREER GUIDANCE AGENT")
    print("="*60 + "")
    
    for i, query in enumerate(test_queries, 1):
        print(f"📝 Query {i}: {query}")
        print("-" * 60)
        
        try:
            response = agent.chat(query)
            print(f"🤖 Response:{response}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print("" + "="*60)
    print("✅ Testing Complete!")
    print("="*60)

if __name__ == "__main__":
    test_career_guidance_agent()