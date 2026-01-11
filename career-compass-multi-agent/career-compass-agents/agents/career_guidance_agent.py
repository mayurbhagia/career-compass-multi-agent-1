import boto3
import json
import os
import sys
from typing import Dict, List, Any, Optional

# Add parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from config import AgentConfig
from agents.mcp_tools.knowledge_base_tool import KnowledgeBaseTool

class CareerGuidanceAgent:
    """
    Career Guidance Agent using Bedrock Knowledge Base
    Follows Lab 2 workshop pattern with MCP tools
    """
    
    def __init__(self, knowledge_base_id: str, region: str = "us-west-2"):
        self.config = AgentConfig()
        self.region = region
        
        self.bedrock_runtime = boto3.client(
            'bedrock-runtime',
            region_name=region
        )
        
        self.kb_tool = KnowledgeBaseTool(
            knowledge_base_id=knowledge_base_id,
            region=region
        )
        
        self.system_prompt = """You are a Career Guidance AI Assistant specializing in helping students with:
        - Career path exploration and job descriptions
        - Interview preparation and tips
        - University recommendations for higher studies
        - Skill development guidance
        
        When answering questions:
        1. Use the query_knowledge_base tool to retrieve relevant information
        2. Provide specific, actionable advice
        3. Cite sources when available
        4. Be encouraging and supportive
        5. If information is not in the knowledge base, acknowledge it honestly
        
        Always maintain a professional yet friendly tone."""
    
    def _create_tool_config(self) -> List[Dict]:
        """Create tool configuration for Bedrock"""
        return [self.kb_tool.to_tool_definition()]
    
    def _handle_tool_use(self, tool_use_block: Dict) -> Dict:
        """Handle tool execution"""
        tool_name = tool_use_block['name']
        tool_input = tool_use_block['input']
        
        if tool_name == self.kb_tool.name:
            result = self.kb_tool.execute(
                query=tool_input['query'],
                max_results=tool_input.get('max_results', 5)
            )
            
            return {
                "toolUseId": tool_use_block['toolUseId'],
                "content": [
                    {
                        "json": {
                            "answer": result.answer,
                            "sources": result.sources,
                            "confidence": result.confidence
                        }
                    }
                ]
            }
        
        return {
            "toolUseId": tool_use_block['toolUseId'],
            "content": [{"text": "Tool not found"}],
            "status": "error"
        }
    
    def process_query(
        self,
        user_query: str,
        conversation_history: Optional[List[Dict]] = None,
        max_iterations: int = 5
    ) -> Dict[str, Any]:
        """Process user query with agentic loop"""
        
        messages = conversation_history or []
        iteration = 0
        
        # Add initial user message
        messages.append({
            "role": "user",
            "content": [{"text": user_query}]
        })
        
        while iteration < max_iterations:
            iteration += 1
            
            # Invoke model with current conversation
            response = self.bedrock_runtime.converse(
                modelId=self.config.BEDROCK_MODEL_ID,
                messages=messages,
                system=[{"text": self.system_prompt}],
                inferenceConfig={
                    "temperature": self.config.TEMPERATURE,
                    "maxTokens": self.config.MAX_TOKENS,
                    "topP": self.config.TOP_P
                },
                toolConfig={
                    "tools": self._create_tool_config()
                }
            )
            
            stop_reason = response['stopReason']
            output_message = response['output']['message']
            
            # Add assistant response to conversation
            messages.append(output_message)
            
            if stop_reason == 'tool_use':
                tool_results = []
                
                for content_block in output_message['content']:
                    if 'toolUse' in content_block:
                        tool_use = content_block['toolUse']
                        print(f"🔧 Agent using tool: {tool_use['name']}")
                        print(f"   Input: {tool_use['input']}")
                        
                        tool_result = self._handle_tool_use(tool_use)
                        tool_results.append({"toolResult": tool_result})
                
                # Add tool results as user message
                messages.append({
                    "role": "user",
                    "content": tool_results
                })
                
                continue
            
            elif stop_reason == 'end_turn':
                final_response = ""
                for content_block in output_message['content']:
                    if 'text' in content_block:
                        final_response += content_block['text']
                
                return {
                    "response": final_response,
                    "conversation_history": messages,
                    "iterations": iteration,
                    "status": "success"
                }
            
            else:
                return {
                    "response": f"Unexpected stop reason: {stop_reason}",
                    "conversation_history": messages,
                    "iterations": iteration,
                    "status": "error"
                }
        
        return {
            "response": "Maximum iterations reached without completion",
            "conversation_history": messages,
            "iterations": iteration,
            "status": "timeout"
        }
    
    def chat(self, user_query: str) -> str:
        """Simple chat interface"""
        result = self.process_query(user_query)
        return result['response']