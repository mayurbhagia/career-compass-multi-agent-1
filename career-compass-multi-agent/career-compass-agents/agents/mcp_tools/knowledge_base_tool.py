
import boto3
import json
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

class KnowledgeBaseToolInput(BaseModel):
    """Input schema for Knowledge Base tool"""
    query: str = Field(
        description="The question or query to search in the knowledge base"
    )
    max_results: Optional[int] = Field(
        default=5,
        description="Maximum number of results to return"
    )

class KnowledgeBaseToolOutput(BaseModel):
    """Output schema for Knowledge Base tool"""
    answer: str
    sources: List[Dict[str, Any]]
    confidence: str

class KnowledgeBaseTool:
    """MCP Tool for querying Bedrock Knowledge Base"""
    
    def __init__(self, knowledge_base_id: str, region: str = "us-west-2"):
        self.knowledge_base_id = knowledge_base_id
        self.region = region
        self.bedrock_agent_runtime = boto3.client(
            'bedrock-agent-runtime',
            region_name=region
        )
        
    @property
    def name(self) -> str:
        return "query_knowledge_base"
    
    @property
    def description(self) -> str:
        return """Query the career guidance knowledge base to get information about:
        - Job descriptions and career paths
        - Interview preparation tips
        - University recommendations for higher studies
        - Required skills for different roles
        - Salary information and career growth opportunities
        
        Use this tool when users ask about careers, jobs, interviews, or education."""
    
    @property
    def input_schema(self) -> Dict:
        return KnowledgeBaseToolInput.model_json_schema()
    
    def execute(self, query: str, max_results: int = 5) -> KnowledgeBaseToolOutput:
        """Execute knowledge base query"""
        try:
            response = self.bedrock_agent_runtime.retrieve_and_generate(
                input={'text': query},
                retrieveAndGenerateConfiguration={
                    'type': 'KNOWLEDGE_BASE',
                    'knowledgeBaseConfiguration': {
                        'knowledgeBaseId': self.knowledge_base_id,
                        'modelArn': 'arn:aws:bedrock:us-west-2:596174723673:inference-profile/us.amazon.nova-pro-v1:0',
                        
                        'retrievalConfiguration': {
                            'vectorSearchConfiguration': {
                                'numberOfResults': max_results
                            }
                        }
                    }
                }
            )
            
            answer = response['output']['text']
            sources = []
            
            if 'citations' in response:
                for citation in response['citations']:
                    for reference in citation.get('retrievedReferences', []):
                        sources.append({
                            'content': reference.get('content', {}).get('text', ''),
                            'location': reference.get('location', {}).get('s3Location', {}),
                            'score': reference.get('metadata', {}).get('score', 0)
                        })
            
            confidence = "high" if len(sources) >= 3 else "medium" if len(sources) >= 1 else "low"
            
            return KnowledgeBaseToolOutput(
                answer=answer,
                sources=sources,
                confidence=confidence
            )
            
        except Exception as e:
            print(f"Error querying knowledge base: {str(e)}")
            return KnowledgeBaseToolOutput(
                answer=f"I encountered an error while searching the knowledge base: {str(e)}",
                sources=[],
                confidence="low"
            )
    
    def to_tool_definition(self) -> Dict:
        """Convert to Bedrock tool definition format"""
        return {
            "toolSpec": {
                "name": self.name,
                "description": self.description,
                "inputSchema": {
                    "json": self.input_schema
                }
            }
        }