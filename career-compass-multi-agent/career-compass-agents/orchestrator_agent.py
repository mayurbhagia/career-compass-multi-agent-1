import os
import sys
from typing import Dict, Any, List, Optional
from strands import Agent
from strands.models import BedrockModel

# Import specialized agents
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agents.career_guidance_agent import CareerGuidanceAgent
from agents.resume_analyzer_agent import ResumeAnalyzerAgent
from agents.job_matcher_agent import JobMatcherAgent

class OrchestratorAgent:
    """
    Orchestrator Agent using Strands framework
    Routes requests to specialized agents and coordinates multi-agent workflows
    """
    
    def __init__(self, region: str = "us-west-2"):
        self.region = region
        
        # Initialize specialized agents
        self.career_agent = CareerGuidanceAgent(
            knowledge_base_id=os.getenv("KB_ID", "5UO4KAMLS3"),
            region=region
        )
        
        self.resume_agent = ResumeAnalyzerAgent(region=region)
        
        self.job_matcher_agent = JobMatcherAgent(
            region=region,
            table_name="career-compass-jobs"
        )
        
        # Initialize Bedrock Model for orchestration
        self.model = BedrockModel(
            model_id="us.amazon.nova-pro-v1:0",
            temperature=0.7,
            max_tokens=2000,
            top_p=0.9
        )
        
        # System prompt for intent classification
        self.system_prompt = """You are an Orchestrator AI that routes student queries to specialized agents.

Available Agents:
1. **Career Guidance Agent**: Answers questions about career paths, job descriptions, interview preparation, university recommendations, skill development
2. **Resume Analyzer Agent**: Analyzes resumes and provides improvement suggestions
3. **Job Matcher Agent**: Matches student profiles with job opportunities and provides recommendations

Your task: Analyze the user's query and determine which agent(s) should handle it.

Respond with ONLY ONE of these options:
- "CAREER_GUIDANCE" - for career advice, interview prep, university guidance
- "RESUME_ANALYSIS" - for resume review and feedback
- "JOB_MATCHING" - for job recommendations and matching
- "MULTI_AGENT" - if the query requires multiple agents (e.g., "analyze my resume and recommend jobs")

Be precise and choose the most appropriate routing."""
        
        # Create Strands agent for intent classification
        self.intent_agent = Agent(
            model=self.model,
            system_prompt=self.system_prompt
        )
    
    def classify_intent(self, user_query: str) -> str:
        """
        Classify user intent to route to appropriate agent
        
        Args:
            user_query: The user's question or request
            
        Returns:
            Intent classification string
        """
        classification_prompt = f"""Classify this user query:

USER QUERY: "{user_query}"

Respond with ONLY ONE word: CAREER_GUIDANCE, RESUME_ANALYSIS, JOB_MATCHING, or MULTI_AGENT"""
        
        try:
            response = self.intent_agent(classification_prompt)
            intent = str(response).strip().upper()
            
            # Validate intent
            valid_intents = ["CAREER_GUIDANCE", "RESUME_ANALYSIS", "JOB_MATCHING", "MULTI_AGENT"]
            if any(valid in intent for valid in valid_intents):
                for valid in valid_intents:
                    if valid in intent:
                        return valid
            
            # Default to career guidance if unclear
            return "CAREER_GUIDANCE"
            
        except Exception as e:
            print(f"Error in intent classification: {str(e)}")
            return "CAREER_GUIDANCE"
    
    def process_query(
        self,
        user_query: str,
        resume_text: Optional[str] = None,
        student_skills: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Process user query by routing to appropriate agent(s)
        
        Args:
            user_query: The user's question
            resume_text: Optional resume text for analysis
            student_skills: Optional list of skills for job matching
            
        Returns:
            Dictionary with response and metadata
        """
        
        # Classify intent
        intent = self.classify_intent(user_query)
        print(f"�� Intent classified as: {intent}")
        
        try:
            if intent == "CAREER_GUIDANCE":
                response = self.career_agent.chat(user_query)
                return {
                    "status": "success",
                    "intent": intent,
                    "response": response,
                    "agent_used": "Career Guidance Agent"
                }
            
            elif intent == "RESUME_ANALYSIS":
                if not resume_text:
                    return {
                        "status": "error",
                        "intent": intent,
                        "response": "Please provide your resume text for analysis.",
                        "agent_used": None
                    }
                
                result = self.resume_agent.analyze_resume(resume_text)
                return {
                    "status": result['status'],
                    "intent": intent,
                    "response": result['analysis'],
                    "agent_used": "Resume Analyzer Agent"
                }
            
            elif intent == "JOB_MATCHING":
                if not student_skills:
                    return {
                        "status": "error",
                        "intent": intent,
                        "response": "Please provide your skills list for job matching.",
                        "agent_used": None
                    }
                
                result = self.job_matcher_agent.get_recommendations(
                    student_skills=student_skills,
                    experience_level="Entry Level",
                    top_n=3
                )
                
                if result['status'] == 'success':
                    return {
                        "status": "success",
                        "intent": intent,
                        "response": result['ai_analysis'],
                        "match_data": result['match_data'],
                        "agent_used": "Job Matcher Agent"
                    }
                else:
                    return {
                        "status": "error",
                        "intent": intent,
                        "response": result.get('error', 'Job matching failed'),
                        "agent_used": "Job Matcher Agent"
                    }
            
            elif intent == "MULTI_AGENT":
                # Handle multi-agent workflow
                responses = {}
                
                # Analyze resume if provided
                if resume_text:
                    resume_result = self.resume_agent.analyze_resume(resume_text)
                    responses['resume_analysis'] = resume_result['analysis']
                
                # Match jobs if skills provided
                if student_skills:
                    job_result = self.job_matcher_agent.get_recommendations(
                        student_skills=student_skills,
                        experience_level="Entry Level",
                        top_n=3
                    )
                    if job_result['status'] == 'success':
                        responses['job_recommendations'] = job_result['ai_analysis']
                        responses['match_data'] = job_result['match_data']
                
                # Combine responses
                combined_response = "## Multi-Agent Analysis"
                if 'resume_analysis' in responses:
                    combined_response += "### Resume Analysis" + responses['resume_analysis'] + ""
                if 'job_recommendations' in responses:
                    combined_response += "### Job Recommendations" + responses['job_recommendations']
                
                return {
                    "status": "success",
                    "intent": intent,
                    "response": combined_response,
                    "agent_used": "Multiple Agents",
                    "detailed_responses": responses
                }
            
            else:
                return {
                    "status": "error",
                    "intent": "UNKNOWN",
                    "response": "Unable to classify your request. Please try rephrasing.",
                    "agent_used": None
                }
                
        except Exception as e:
            return {
                "status": "error",
                "intent": intent,
                "response": f"Error processing request: {str(e)}",
                "agent_used": None
            }
    
    def get_career_advice(self, query: str) -> str:
        """Direct access to Career Guidance Agent"""
        return self.career_agent.chat(query)
    
    def analyze_resume(self, resume_text: str) -> Dict[str, Any]:
        """Direct access to Resume Analyzer Agent"""
        return self.resume_agent.analyze_resume(resume_text)
    
    def match_jobs(self, student_skills: List[str]) -> Dict[str, Any]:
        """Direct access to Job Matcher Agent"""
        return self.job_matcher_agent.get_recommendations(
            student_skills=student_skills,
            experience_level="Entry Level",
            top_n=5
        )