import os
from typing import Dict, Any, Optional
from strands import Agent
from strands.models import BedrockModel

class ResumeAnalyzerAgent:
    """
    Resume Analyzer Agent using Strands framework
    Analyzes student resumes and provides improvement suggestions
    """
    
    def __init__(self, region: str = "us-west-2"):
        self.region = region
        
        # Initialize Bedrock Model with Nova Pro - pass parameters directly
        self.model = BedrockModel(
            model_id="us.amazon.nova-pro-v1:0",
            temperature=0.7,
            max_tokens=3000,
            top_p=0.9
        )
        
        # System prompt for resume analysis
        self.system_prompt = """You are an expert Resume Analyzer AI specializing in helping students improve their resumes for tech jobs and internships.

When analyzing a resume, provide:
1. **Overall Assessment**: Brief summary of strengths and areas for improvement
2. **Technical Skills Analysis**: Evaluate technical skills section
3. **Project Analysis**: Review projects for impact and clarity
4. **Experience Analysis**: Assess internships and work experience
5. **Education & Certifications**: Review academic background
6. **Formatting & Structure**: Comment on layout and readability
7. **ATS Optimization**: Suggest keywords for Applicant Tracking Systems
8. **Actionable Recommendations**: Specific improvements with examples

Be constructive, encouraging, and specific. Provide concrete examples of improvements."""
        
        # Create Strands agent
        self.agent = Agent(
            model=self.model,
            system_prompt=self.system_prompt
        )
    
    def analyze_resume(self, resume_text: str) -> Dict[str, Any]:
        """
        Analyze a resume and provide detailed feedback
        
        Args:
            resume_text: The full text content of the resume
            
        Returns:
            Dictionary with analysis results
        """
        
        analysis_prompt = f"""Please analyze the following resume and provide comprehensive feedback:

RESUME:
{resume_text}

Provide your analysis in the following structure:
1. Overall Assessment (2-3 sentences)
2. Technical Skills Analysis
3. Project Analysis
4. Experience Analysis
5. Education & Certifications
6. Formatting & Structure
7. ATS Optimization Suggestions
8. Top 5 Actionable Recommendations

Be specific and provide examples where possible."""
        
        try:
            # Invoke the Strands agent - returns a string directly
            response = self.agent(analysis_prompt)
            
            return {
                "status": "success",
                "analysis": str(response),
                "resume_length": len(resume_text),
                "agent_name": "ResumeAnalyzerAgent"
            }
            
        except Exception as e:
            print(f"Error in analyze_resume: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "analysis": f"Error analyzing resume: {str(e)}"
            }
    
    def quick_score(self, resume_text: str) -> Dict[str, Any]:
        """
        Provide a quick score and summary of the resume
        
        Args:
            resume_text: The full text content of the resume
            
        Returns:
            Dictionary with score and brief feedback
        """
        
        scoring_prompt = f"""Analyze this resume and provide:
1. Overall Score (out of 10)
2. Brief 2-3 sentence summary
3. Top 3 strengths
4. Top 3 areas for improvement

RESUME:
{resume_text}

Format your response clearly with these sections."""
        
        try:
            response = self.agent(scoring_prompt)
            
            return {
                "status": "success",
                "score_analysis": str(response),
                "agent_name": "ResumeAnalyzerAgent"
            }
            
        except Exception as e:
            print(f"Error in quick_score: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def compare_with_job(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """
        Compare resume against a specific job description
        
        Args:
            resume_text: The full text content of the resume
            job_description: The job description to compare against
            
        Returns:
            Dictionary with comparison results
        """
        
        comparison_prompt = f"""Compare this resume against the job description and provide:
1. Match Score (out of 10)
2. Matching Skills
3. Missing Skills
4. Relevant Experience Alignment
5. Recommendations to improve match

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Provide specific, actionable feedback."""
        
        try:
            response = self.agent(comparison_prompt)
            
            return {
                "status": "success",
                "comparison": str(response),
                "agent_name": "ResumeAnalyzerAgent"
            }
            
        except Exception as e:
            print(f"Error in compare_with_job: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }