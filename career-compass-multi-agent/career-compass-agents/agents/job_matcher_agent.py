import os
import boto3
import json
from typing import Dict, Any, List, Optional
from strands import Agent
from strands.models import BedrockModel
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    """Helper to encode Decimal types from DynamoDB"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

class JobMatcherAgent:
    """
    Job Matcher Agent using Strands framework + AWS MCP tool
    Matches student profiles with job listings from DynamoDB
    Demonstrates Lab 3 pattern: Strands Agent + AWS Service Integration
    """
    
    def __init__(self, region: str = "us-west-2", table_name: str = "career-compass-jobs"):
        self.region = region
        self.table_name = table_name
        
        # Initialize DynamoDB client (AWS MCP tool pattern)
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        self.table = self.dynamodb.Table(table_name)
        
        # Initialize Bedrock Model with Nova Pro
        self.model = BedrockModel(
            model_id="us.amazon.nova-pro-v1:0",
            temperature=0.7,
            max_tokens=3000,
            top_p=0.9
        )
        
        # System prompt for job matching
        self.system_prompt = """You are an expert Job Matcher AI specializing in matching students with suitable tech job opportunities.

Your responsibilities:
1. Analyze student skills, experience, and career preferences
2. Match them with relevant job listings from the database
3. Calculate match scores based on skill overlap and requirements
4. Identify skill gaps and provide learning recommendations
5. Rank jobs by relevance and match quality

When providing recommendations:
- Be specific about why a job is a good match
- Highlight matching skills and relevant experience
- Identify missing skills that could be learned
- Consider experience level and job type appropriateness
- Provide actionable next steps for the student
- Be encouraging about growth opportunities

Always maintain a supportive and constructive tone."""
        
        # Create Strands agent
        self.agent = Agent(
            model=self.model,
            system_prompt=self.system_prompt
        )
    
    def get_all_jobs(self) -> List[Dict[str, Any]]:
        """
        Retrieve all jobs from DynamoDB using AWS MCP tool pattern
        Handles pagination automatically
        """
        try:
            response = self.table.scan()
            jobs = response.get('Items', [])
            
            # Handle pagination if needed
            while 'LastEvaluatedKey' in response:
                response = self.table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                jobs.extend(response.get('Items', []))
            
            return jobs
        except Exception as e:
            print(f"Error retrieving jobs from DynamoDB: {str(e)}")
            return []
    
    def get_jobs_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Retrieve jobs by category using Global Secondary Index
        Demonstrates efficient DynamoDB querying
        """
        try:
            response = self.table.query(
                IndexName='category-index',
                KeyConditionExpression='category = :cat',
                ExpressionAttributeValues={':cat': category}
            )
            return response.get('Items', [])
        except Exception as e:
            print(f"Error querying jobs by category: {str(e)}")
            return []
    
    def calculate_skill_match(self, student_skills: List[str], job_skills: List[str]) -> float:
        """Calculate skill match percentage"""
        if not job_skills:
            return 0.0
        
        student_skills_lower = [s.lower().strip() for s in student_skills]
        job_skills_lower = [s.lower().strip() for s in job_skills]
        
        matching_skills = set(student_skills_lower) & set(job_skills_lower)
        match_percentage = (len(matching_skills) / len(job_skills_lower)) * 100
        
        return round(match_percentage, 2)
    
    def match_jobs(
        self,
        student_skills: List[str],
        experience_level: str = "Entry Level",
        preferred_categories: Optional[List[str]] = None,
        top_n: int = 5
    ) -> Dict[str, Any]:
        """
        Match student profile with jobs from DynamoDB
        
        Args:
            student_skills: List of student's technical skills
            experience_level: Student's experience level
            preferred_categories: Preferred job categories (optional)
            top_n: Number of top matches to return
            
        Returns:
            Dictionary with matched jobs and analysis
        """
        
        # Get all jobs from DynamoDB using AWS MCP tool
        all_jobs = self.get_all_jobs()
        
        if not all_jobs:
            return {
                "status": "error",
                "error": "No jobs found in database",
                "top_matches": []
            }
        
        # Calculate match scores for each job
        job_matches = []
        for job in all_jobs:
            required_skills = job.get('required_skills', [])
            preferred_skills = job.get('preferred_skills', [])
            
            # Calculate match scores
            required_match = self.calculate_skill_match(student_skills, required_skills)
            preferred_match = self.calculate_skill_match(student_skills, preferred_skills)
            
            # Overall match score (weighted: 70% required, 30% preferred)
            overall_match = (required_match * 0.7) + (preferred_match * 0.3)
            
            # Experience level match bonus
            exp_match = 1.0 if job.get('experience_level') == experience_level else 0.5
            
            # Category preference bonus
            cat_match = 1.0
            if preferred_categories:
                cat_match = 1.2 if job.get('category') in preferred_categories else 0.8
            
            # Final score with bonuses
            final_score = overall_match * exp_match * cat_match
            
            # Identify matching and missing skills
            student_skills_lower = set([s.lower().strip() for s in student_skills])
            required_skills_lower = set([s.lower().strip() for s in required_skills])
            preferred_skills_lower = set([s.lower().strip() for s in preferred_skills])
            
            matching_skills = list(student_skills_lower & (required_skills_lower | preferred_skills_lower))
            missing_skills = list(required_skills_lower - student_skills_lower)
            
            job_matches.append({
                "job": job,
                "match_score": round(final_score, 2),
                "required_match": required_match,
                "preferred_match": preferred_match,
                "matching_skills": matching_skills,
                "missing_skills": missing_skills
            })
        
        # Sort by match score (descending)
        job_matches.sort(key=lambda x: x['match_score'], reverse=True)
        
        # Get top N matches
        top_matches = job_matches[:top_n]
        
        return {
            "status": "success",
            "total_jobs_analyzed": len(all_jobs),
            "top_matches": top_matches,
            "student_skills": student_skills,
            "experience_level": experience_level
        }
    
    def get_recommendations(
        self,
        student_skills: List[str],
        experience_level: str = "Entry Level",
        preferred_categories: Optional[List[str]] = None,
        top_n: int = 5
    ) -> Dict[str, Any]:
        """
        Get AI-powered job recommendations with detailed analysis
        Combines DynamoDB data with Strands AI analysis
        
        Args:
            student_skills: List of student's technical skills
            experience_level: Student's experience level
            preferred_categories: Preferred job categories
            top_n: Number of recommendations
            
        Returns:
            Dictionary with recommendations and AI analysis
        """
        
        # Get matched jobs from DynamoDB
        match_result = self.match_jobs(
            student_skills=student_skills,
            experience_level=experience_level,
            preferred_categories=preferred_categories,
            top_n=top_n
        )
        
        if match_result['status'] == 'error':
            return match_result
        
        # Prepare data for AI analysis
        jobs_summary = []
        for match in match_result['top_matches']:
            job = match['job']
            jobs_summary.append({
                "title": job['title'],
                "company": job['company'],
                "location": job.get('location', 'Not specified'),
                "match_score": match['match_score'],
                "matching_skills": match['matching_skills'],
                "missing_skills": match['missing_skills'],
                "salary": job.get('salary_range', 'Not specified'),
                "category": job.get('category', 'Not specified')
            })
        
        # Create prompt for Strands AI analysis
        analysis_prompt = f"""Analyze these job matches for a student and provide detailed recommendations:

STUDENT PROFILE:
- Skills: {', '.join(student_skills)}
- Experience Level: {experience_level}
- Preferred Categories: {', '.join(preferred_categories) if preferred_categories else 'Any'}

TOP JOB MATCHES FROM DATABASE:
{json.dumps(jobs_summary, indent=2, cls=DecimalEncoder)}

Please provide:
1. **Overall Assessment**: Brief summary of the student's job market fit (2-3 sentences)
2. **Top 3 Recommended Jobs**: For each job, explain:
   - Why it's a good match
   - How their skills align
   - What makes them a strong candidate
3. **Skill Gap Analysis**: 
   - Critical skills to learn immediately
   - Nice-to-have skills for better opportunities
4. **Action Plan**: Specific steps to improve job prospects (prioritized)
5. **Interview Preparation**: Tips specific to the recommended roles

Be specific, encouraging, and actionable. Focus on growth opportunities."""
        
        try:
            # Get AI analysis using Strands agent
            ai_response = self.agent(analysis_prompt)
            
            return {
                "status": "success",
                "match_data": match_result,
                "ai_analysis": str(ai_response),
                "agent_name": "JobMatcherAgent"
            }
            
        except Exception as e:
            print(f"Error in AI analysis: {str(e)}")
            return {
                "status": "partial_success",
                "match_data": match_result,
                "ai_analysis": f"Match data available but AI analysis failed: {str(e)}",
                "agent_name": "JobMatcherAgent"
            }
    
    def find_jobs_by_skill(self, skill: str) -> List[Dict[str, Any]]:
        """
        Find all jobs that require a specific skill
        Useful for exploring opportunities for a particular technology
        """
        all_jobs = self.get_all_jobs()
        matching_jobs = []
        
        skill_lower = skill.lower().strip()
        for job in all_jobs:
            required_skills = [s.lower().strip() for s in job.get('required_skills', [])]
            preferred_skills = [s.lower().strip() for s in job.get('preferred_skills', [])]
            
            if skill_lower in required_skills or skill_lower in preferred_skills:
                matching_jobs.append(job)
        
        return matching_jobs
    
    def get_skill_demand_analysis(self, skill: str) -> Dict[str, Any]:
        """
        Analyze demand for a specific skill across all jobs
        Provides insights on salary ranges and job categories
        """
        matching_jobs = self.find_jobs_by_skill(skill)
        
        if not matching_jobs:
            return {
                "status": "error",
                "error": f"No jobs found requiring skill: {skill}"
            }
        
        # Aggregate data
        categories = {}
        for job in matching_jobs:
            cat = job.get('category', 'Other')
            categories[cat] = categories.get(cat, 0) + 1
        
        analysis_prompt = f"""Analyze the demand for the skill "{skill}" based on this job data:

JOBS REQUIRING {skill.upper()}:
Total Jobs: {len(matching_jobs)}
Categories: {json.dumps(categories, indent=2)}

Sample Jobs:
{json.dumps([{"title": j['title'], "company": j['company'], "salary": j.get('salary_range')} for j in matching_jobs[:5]], indent=2, cls=DecimalEncoder)}

Provide:
1. **Market Demand**: How in-demand is this skill?
2. **Career Paths**: What roles typically require this skill?
3. **Salary Insights**: Typical salary ranges for this skill
4. **Complementary Skills**: What other skills are commonly required alongside this?
5. **Learning Recommendation**: Should students prioritize learning this skill?

Be specific and data-driven."""
        
        try:
            ai_response = self.agent(analysis_prompt)
            
            return {
                "status": "success",
                "skill": skill,
                "total_jobs": len(matching_jobs),
                "categories": categories,
                "analysis": str(ai_response),
                "agent_name": "JobMatcherAgent"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }