
import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.job_matcher_agent import JobMatcherAgent

def test_job_matcher():
    """Test the Job Matcher Agent with Strands + DynamoDB"""
    
    print("🚀 Initializing Job Matcher Agent (Strands + DynamoDB + AWS MCP)...")
    agent = JobMatcherAgent(region="us-west-2", table_name="career-compass-jobs")
    
    print("" + "="*60)
    print("TESTING JOB MATCHER AGENT (STRANDS + AWS MCP)")
    print("="*60 + "")
    
    # Test 1: Match jobs for a Full Stack Developer profile
    print("📝 Test 1: Full Stack Developer Profile")
    print("-" * 60)
    
    student_skills_1 = [
        "Python", "React", "Node.js", "JavaScript", "MongoDB",
        "HTML", "CSS", "Git", "REST APIs", "AWS"
    ]
    
    try:
        result = agent.get_recommendations(
            student_skills=student_skills_1,
            experience_level="Entry Level",
            preferred_categories=["Software Development"],
            top_n=3
        )
        
        if result['status'] in ['success', 'partial_success']:
            print(f"✅ Found {result['match_data']['total_jobs_analyzed']} jobs in DynamoDB")
            print(f"🎯 Top Matches:")
            for i, match in enumerate(result['match_data']['top_matches'], 1):
                job = match['job']
                print(f"{i}. {job['title']} at {job['company']}")
                print(f"   Match Score: {match['match_score']}%")
                print(f"   Location: {job.get('location', 'Not specified')}")
                print(f"   Matching Skills: {', '.join(match['matching_skills'][:5])}")
                print(f"   Missing Skills: {', '.join(match['missing_skills'][:3])}")
                print(f"   Salary: {job.get('salary_range', 'Not specified')}")
            
            print(f"🤖 AI Analysis:{result['ai_analysis']}")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("" + "="*60)
    
    # Test 2: Match jobs for a Cloud Engineer profile
    print("📝 Test 2: Cloud Engineer Profile")
    print("-" * 60)
    
    student_skills_2 = [
        "AWS", "Python", "Docker", "Kubernetes", "Linux",
        "Terraform", "Git", "CI/CD"
    ]
    
    try:
        result = agent.get_recommendations(
            student_skills=student_skills_2,
            experience_level="Entry Level",
            preferred_categories=["Cloud", "DevOps"],
            top_n=3
        )
        
        if result['status'] in ['success', 'partial_success']:
            print(f"✅ Analysis complete!")
            print(f"🎯 Top {len(result['match_data']['top_matches'])} Matches:")
            for i, match in enumerate(result['match_data']['top_matches'], 1):
                job = match['job']
                print(f"{i}. {job['title']} at {job['company']}")
                print(f"   Match Score: {match['match_score']}%")
                print(f"   Category: {job.get('category', 'Not specified')}")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("" + "="*60)
    
    # Test 3: Find jobs by specific skill
    print("📝 Test 3: Find Jobs Requiring Python")
    print("-" * 60)
    
    try:
        python_jobs = agent.find_jobs_by_skill("Python")
        print(f"✅ Found {len(python_jobs)} jobs requiring Python:")
        for job in python_jobs[:5]:
            print(f"   • {job['title']} at {job['company']} ({job.get('category', 'N/A')})")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("" + "="*60)
    
    # Test 4: Skill demand analysis
    print("📝 Test 4: Skill Demand Analysis for AWS")
    print("-" * 60)
    
    try:
        result = agent.get_skill_demand_analysis("AWS")
        if result['status'] == 'success':
            print(f"✅ Analysis complete!")
            print(f"Total jobs requiring AWS: {result['total_jobs']}")
            print(f"Categories: {result['categories']}")
            print(f"{result['analysis']}")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("" + "="*60)
    print("✅ Testing Complete!")
    print("="*60)

if __name__ == "__main__":
    test_job_matcher()