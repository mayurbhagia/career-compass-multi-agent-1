
import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.resume_analyzer_agent import ResumeAnalyzerAgent

# Sample resume for testing
SAMPLE_RESUME = """
PRIYA SHARMA
Email: priya.sharma@email.com | Phone: +91-9876543210
LinkedIn: linkedin.com/in/priyasharma | GitHub: github.com/priyasharma

EDUCATION
Bachelor of Engineering in Computer Science
Mumbai University, Mumbai, India
CGPA: 8.5/10 | Expected Graduation: May 2026

TECHNICAL SKILLS
Programming Languages: Python, Java, C++, JavaScript
Web Technologies: React, Node.js, HTML/CSS, REST APIs
Databases: MySQL, MongoDB, PostgreSQL
Cloud & Tools: AWS (EC2, S3, Lambda), Git, Docker, Linux
Frameworks: Django, Flask, Express.js

PROJECTS

E-Commerce Website | React, Node.js, MongoDB | Jan 2025 - Mar 2025
- Built full-stack e-commerce platform with user authentication and payment integration
- Implemented shopping cart, product search, and order management features
- Deployed on AWS EC2 with 99.9% uptime
- Technologies: React, Node.js, Express, MongoDB, Stripe API

Machine Learning Price Predictor | Python, Scikit-learn | Sep 2024 - Nov 2024
- Developed ML model to predict house prices with 85% accuracy
- Performed data cleaning, feature engineering, and model optimization
- Created Flask API for model deployment
- Technologies: Python, Pandas, Scikit-learn, Flask

INTERNSHIP EXPERIENCE

Software Development Intern | TechCorp Solutions, Mumbai | Jun 2024 - Aug 2024
- Developed REST APIs for customer management system using Node.js
- Collaborated with team of 5 developers using Agile methodology
- Reduced API response time by 30% through optimization
- Participated in code reviews and daily standups

CERTIFICATIONS
- AWS Certified Cloud Practitioner (Dec 2024)
- Python for Data Science - Coursera (Aug 2024)
- Full Stack Web Development - Udemy (May 2024)

ACHIEVEMENTS
- Winner, College Hackathon 2024 - Built AI chatbot for student queries
- Published research paper on "ML in Healthcare" in college journal
- Core member, Computer Science Society - Organized 3 technical workshops
"""

def test_resume_analyzer():
    """Test the Resume Analyzer Agent"""
    
    print("🚀 Initializing Resume Analyzer Agent (Strands)...")
    agent = ResumeAnalyzerAgent(region="us-west-2")
    
    print("" + "="*60)
    print("TESTING RESUME ANALYZER AGENT (STRANDS)")
    print("="*60 + "")
    
    # Test 1: Full Analysis
    print("📝 Test 1: Full Resume Analysis")
    print("-" * 60)
    try:
        result = agent.analyze_resume(SAMPLE_RESUME)
        if result['status'] == 'success':
            print(f"✅ Analysis Complete!")
            print(result['analysis'])
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("" + "="*60)
    
    # Test 2: Quick Score
    print("📝 Test 2: Quick Score")
    print("-" * 60)
    try:
        result = agent.quick_score(SAMPLE_RESUME)
        if result['status'] == 'success':
            print(f"✅ Score Complete!")
            print(result['score_analysis'])
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("" + "="*60)
    print("✅ Testing Complete!")
    print("="*60)

if __name__ == "__main__":
    test_resume_analyzer()