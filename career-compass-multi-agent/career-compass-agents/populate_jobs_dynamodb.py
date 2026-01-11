
import boto3
import json

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table('career-compass-jobs')

# Sample job listings for tech roles
jobs = [
    {
        "job_id": "JOB001",
        "title": "Cloud Engineer",
        "company": "TechCorp Solutions",
        "location": "Bangalore, India",
        "category": "Cloud",
        "experience_level": "Entry Level",
        "required_skills": ["AWS", "Python", "Docker", "Kubernetes", "Terraform"],
        "preferred_skills": ["CI/CD", "Linux", "Networking"],
        "description": "Build and maintain cloud infrastructure on AWS. Work with containerization and infrastructure as code.",
        "salary_range": "8-12 LPA",
        "job_type": "Full-time",
        "posted_date": "2026-01-05"
    },
    {
        "job_id": "JOB002",
        "title": "Full Stack Developer",
        "company": "StartupXYZ",
        "location": "Mumbai, India",
        "category": "Software Development",
        "experience_level": "Entry Level",
        "required_skills": ["React", "Node.js", "JavaScript", "MongoDB", "REST APIs"],
        "preferred_skills": ["TypeScript", "GraphQL", "AWS"],
        "description": "Develop modern web applications using MERN stack. Work on both frontend and backend components.",
        "salary_range": "6-10 LPA",
        "job_type": "Full-time",
        "posted_date": "2026-01-08"
    },
    {
        "job_id": "JOB003",
        "title": "Data Scientist",
        "company": "Analytics Pro",
        "location": "Hyderabad, India",
        "category": "Data Science",
        "experience_level": "Entry Level",
        "required_skills": ["Python", "Machine Learning", "Pandas", "Scikit-learn", "SQL"],
        "preferred_skills": ["TensorFlow", "PyTorch", "Statistics"],
        "description": "Work on machine learning projects and data analysis. Build predictive models and visualizations.",
        "salary_range": "10-15 LPA",
        "job_type": "Full-time",
        "posted_date": "2026-01-07"
    },
    {
        "job_id": "JOB004",
        "title": "DevOps Engineer",
        "company": "CloudNative Inc",
        "location": "Pune, India",
        "category": "DevOps",
        "experience_level": "Entry Level",
        "required_skills": ["Docker", "Kubernetes", "Jenkins", "Git", "Linux"],
        "preferred_skills": ["AWS", "Terraform", "Ansible", "Python"],
        "description": "Implement CI/CD pipelines and manage containerized applications. Automate infrastructure deployment.",
        "salary_range": "7-11 LPA",
        "job_type": "Full-time",
        "posted_date": "2026-01-06"
    },
    {
        "job_id": "JOB005",
        "title": "Machine Learning Engineer",
        "company": "AI Innovations",
        "location": "Bangalore, India",
        "category": "AI/ML",
        "experience_level": "Entry Level",
        "required_skills": ["Python", "TensorFlow", "PyTorch", "Machine Learning", "Deep Learning"],
        "preferred_skills": ["MLOps", "AWS SageMaker", "Docker"],
        "description": "Build and deploy machine learning models. Work on computer vision and NLP projects.",
        "salary_range": "12-18 LPA",
        "job_type": "Full-time",
        "posted_date": "2026-01-04"
    },
    {
        "job_id": "JOB006",
        "title": "Backend Developer",
        "company": "Enterprise Systems",
        "location": "Delhi NCR, India",
        "category": "Software Development",
        "experience_level": "Entry Level",
        "required_skills": ["Java", "Spring Boot", "MySQL", "REST APIs", "Git"],
        "preferred_skills": ["Microservices", "Redis", "Kafka"],
        "description": "Develop scalable backend services using Java and Spring Boot. Work with microservices architecture.",
        "salary_range": "8-13 LPA",
        "job_type": "Full-time",
        "posted_date": "2026-01-09"
    },
    {
        "job_id": "JOB007",
        "title": "Frontend Developer",
        "company": "WebTech Solutions",
        "location": "Chennai, India",
        "category": "Software Development",
        "experience_level": "Entry Level",
        "required_skills": ["React", "JavaScript", "HTML", "CSS", "Git"],
        "preferred_skills": ["TypeScript", "Redux", "Webpack"],
        "description": "Create responsive and interactive user interfaces. Work with modern frontend frameworks.",
        "salary_range": "5-9 LPA",
        "job_type": "Full-time",
        "posted_date": "2026-01-10"
    },
    {
        "job_id": "JOB008",
        "title": "Cybersecurity Analyst",
        "company": "SecureNet Systems",
        "location": "Mumbai, India",
        "category": "Security",
        "experience_level": "Entry Level",
        "required_skills": ["Network Security", "Linux", "Python", "Security Tools"],
        "preferred_skills": ["Ethical Hacking", "SIEM", "Incident Response"],
        "description": "Monitor security systems and respond to incidents. Learn about threat detection and prevention.",
        "salary_range": "8-12 LPA",
        "job_type": "Full-time",
        "posted_date": "2026-01-08"
    }
]

# Insert jobs into DynamoDB
print("🚀 Populating DynamoDB with sample job listings...")
for job in jobs:
    try:
        table.put_item(Item=job)
        print(f"✅ Added: {job['job_id']} - {job['title']} at {job['company']}")
    except Exception as e:
        print(f"❌ Error adding {job['job_id']}: {str(e)}")

print(f"✅ Successfully added {len(jobs)} jobs to DynamoDB table 'career-compass-jobs'")

# Verify by scanning table
response = table.scan()
print(f"📊 Total jobs in table: {response['Count']}")