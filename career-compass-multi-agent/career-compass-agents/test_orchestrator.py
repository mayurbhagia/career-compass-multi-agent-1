import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from orchestrator_agent import OrchestratorAgent

# Sample data for testing
SAMPLE_RESUME = """
PRIYA SHARMA
Email: priya.sharma@email.com

TECHNICAL SKILLS
Programming: Python, Java, JavaScript
Web: React, Node.js, HTML/CSS, REST APIs
Databases: MySQL, MongoDB
Cloud: AWS (EC2, S3, Lambda), Git, Docker

PROJECTS
E-Commerce Website | React, Node.js, MongoDB
- Built full-stack platform with authentication
- Deployed on AWS EC2

INTERNSHIP
Software Development Intern | TechCorp | Jun-Aug 2024
- Developed REST APIs using Node.js
- Reduced API response time by 30%
"""

SAMPLE_SKILLS = ["Python", "React", "Node.js", "JavaScript", "MongoDB", "AWS", "Docker", "Git"]

def test_orchestrator():
    """Test the Orchestrator Agent"""
    
    print("🚀 Initializing Orchestrator Agent...")
    orchestrator = OrchestratorAgent(region="us-west-2")
    
    print("" + "="*60)
    print("TESTING ORCHESTRATOR AGENT (MULTI-AGENT COORDINATION)")
    print("="*60 + "")
    
    # Test 1: Career Guidance Query
    print("📝 Test 1: Career Guidance Query")
    print("-" * 60)
    query1 = "What skills do I need to become a Cloud Engineer?"
    
    try:
        result = orchestrator.process_query(query1)
        print(f"Intent: {result['intent']}")
        print(f"Agent Used: {result['agent_used']}")
        print(f"✅ Response:{result['response']}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("" + "="*60)
    
    # Test 2: Resume Analysis Query
    print("📝 Test 2: Resume Analysis Query")
    print("-" * 60)
    query2 = "Can you review my resume and provide feedback?"
    
    try:
        result = orchestrator.process_query(query2, resume_text=SAMPLE_RESUME)
        print(f"Intent: {result['intent']}")
        print(f"Agent Used: {result['agent_used']}")
        print(f"✅ Response:{result['response'][:500]}...")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("" + "="*60)
    
    # Test 3: Job Matching Query
    print("📝 Test 3: Job Matching Query")
    print("-" * 60)
    query3 = "What jobs match my skills?"
    
    try:
        result = orchestrator.process_query(query3, student_skills=SAMPLE_SKILLS)
        print(f"Intent: {result['intent']}")
        print(f"Agent Used: {result['agent_used']}")
        print(f"✅ Response:{result['response'][:500]}...")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("" + "="*60)
    
    # Test 4: Multi-Agent Query
    print("📝 Test 4: Multi-Agent Query")
    print("-" * 60)
    query4 = "Analyze my resume and recommend suitable jobs"
    
    try:
        result = orchestrator.process_query(
            query4,
            resume_text=SAMPLE_RESUME,
            student_skills=SAMPLE_SKILLS
        )
        print(f"Intent: {result['intent']}")
        print(f"Agent Used: {result['agent_used']}")
        print(f"✅ Response:{result['response'][:500]}...")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("" + "="*60)
    print("✅ Testing Complete!")
    print("="*60)

if __name__ == "__main__":
    test_orchestrator()