"""Claude API client for interacting with Claude 3.7 Sonnet."""

import time
from typing import Dict, Any, List, Optional
from anthropic import Anthropic
from .logger import WorkBackLogger
from .analysis_context import AnalysisContext
# Configure logging
logger = WorkBackLogger().get_logger("claude_client")

class ClaudeClient:
    """Client for interacting with Claude API."""
    
    # Define available tools and their schemas
    TOOLS = [
        {
            "name": "grep_files",
            "description": "Find filenames containing specific patterns",
            "input_schema": {
                "type": "object",
                "properties": {
                    "search_patterns": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of strings or patterns to search for in files"
                    },
                    "savedState": {
                        "type": "string",
                        "description": "Save a temporary state which you can use to continue the analysis later. In this store, 'So far we've seen:' and 'We need to look for:' sections. Make those sections numbered bullet points"
                    },
                    "InvestigationGoal": {
                        "type": "string",
                        "description": "Current investigation goal"
                    }
                },
                "required": ["search_patterns", "savedState", "InvestigationGoal"]
            }
        },
        {
            "name": "fetch_logs",
            "description": "Fetch a specific page of logs for analysis. Pages are numbered from 1 to total_pages. Request the next page number to fetch.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "page_number": {
                        "type": "integer",
                        "description": "Next page number of logs to fetch (1-based indexing)"
                    },
                    "savedState": {
                        "type": "string",
                        "description": "Save a temporary state which you can use to continue the analysis later. In this store, 'So far we've seen:' and 'We need to look for:' sections. Make those sections numbered bullet points"
                    },
                    "InvestigationGoal": {
                        "type": "string",
                        "description": "Current investigation goal"
                    }
                },
                "required": ["page_number", "savedState", "InvestigationGoal"]
            }
        },
        {
            "name": "fetch_code",
            "description": "Fetch code from a specific file and line number",
            "input_schema": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Path to the file to analyze"
                    },
                    "line_number": {
                        "type": "integer",
                        "description": "Line number to focus analysis on"
                    },
                    "savedState": {
                        "type": "string",
                        "description": "Save a temporary state which you can use to continue the analysis later. In this store, 'So far we've seen:' and 'We need to look for:' sections. Make those sections numbered bullet points"
                    },
                    "InvestigationGoal": {
                        "type": "string",
                        "description": "Current investigation goal"
                    }
                },
                "required": ["filename", "line_number", "savedState", "InvestigationGoal"]
            }
        },
        {
            "name": "show_root_cause",
            "description": "Display final root cause analysis when sufficient information is available",
            "input_schema": {
                "type": "object",
                "properties": {
                    "root_cause": {
                        "type": "string",
                        "description": "Detailed explanation of the root cause and recommendations"
                    },
                    "savedState": {
                        "type": "string",
                        "description": "Save a temporary state which you can use to continue the analysis later. In this store, 'So far we've seen:' and 'We need to look for:' sections. Make those sections numbered bullet points"
                    },
                    "InvestigationGoal": {
                        "type": "string",
                        "description": "Current investigation goal"
                    }
                },
                "required": ["root_cause", "savedState", "InvestigationGoal"]
            }
        },
        {
            "name": "ask_user",
            "description": "Ask the user a question when clarification or additional information is needed",
            "input_schema": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The question to ask the user"
                    },
                    "context": {
                        "type": "string",
                        "description": "Optional context about why this information is needed"
                    },
                    "savedState": {
                        "type": "string",
                        "description": "Save a temporary state which you can use to continue the analysis later. In this store, 'So far we've seen:' and 'We need to look for:' sections. Make those sections numbered bullet points"
                    },
                    "InvestigationGoal": {
                        "type": "string",
                        "description": "Current investigation goal"
                    }
                },
                "required": ["question", "savedState", "InvestigationGoal"]
            }
        }
    ]
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-7-sonnet-latest"):
        """
        Initialize Claude API client.
        
        Args:
            api_key: Anthropic API key.
            model: Claude model to use.
        """
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("API key must be provided either as argument or in ANTHROPIC_API_KEY environment variable")
            
        self.model = model
        self.client = Anthropic(api_key=self.api_key)
        self.max_tokens = 4096
        self.analyzed_pages = set()  # Track which pages have been analyzed

    def analyze_error(self, analysis_context: AnalysisContext):
        """
        Ask Claude to analyze an error and suggest next steps.
        
        Args:
            error_input: The error or log content to analyze
            findings: List of all findings so far (contains only metadata, not content)
            
        Returns:
            Dictionary with:
            - tool: The name of the tool to use
            - params: Parameters for the tool
            - analysis: Any additional analysis text
            - error: Optional error message if something went wrong
        """
        try:
            # Format findings for the prompt
            user_prompt = f"""
Here is the requested information:
{analysis_context.current_page_content}
"""
            history_prompt = f"""
Here is the state you have saved:
{analysis_context.current_findings['savedState']}

We are investigating: {analysis_context.current_findings['InvestigationGoal']}

Information you researched so far:
{analysis_context.history}

If you need to request same information again, make a note in savedState so you don't repeat the same analysis.
"""
            if  "Requested Code:" in user_prompt and "Code Context:" in user_prompt:
                system_prompt = f"Sending Requested Code. Please check if you can establish the root cause of the error. If you can, use show_root_cause tool. If you can't, continue the current analysis"
            elif "files matching patterns" in user_prompt:
                system_prompt = f"Sending Grepped File names. Please continue the current analysis. If needed request code from relevant found files. If you can establish the root cause of the error, use show_root_cause tool."
            elif analysis_context.current_findings['resending_logs']:
                system_prompt = f"Sending the requested Logs page. Please continue the current analysis. If you can establish the root cause of the error, use show_root_cause tool."
            elif "Question:" in user_prompt and "Answer:" in user_prompt:
                system_prompt = f"User has provided an answer to your question. Please analyze the response and continue the investigation. If you can establish the root cause of the error, use show_root_cause tool."
            else:
                system_prompt = f"""
You are an expert system debugging assistant. Analyze this error and determine the next step.

Some tips about tool:
1. grep_files: 
    If you know the file name, just call fetch_code tool with the filename. Use grep, only to find files with patterns.
    If you don't know the exact path of a file, no need to grep. You can still use fetch_code tool with the filename.
2. fetch_code:
    Use this tool to get the code context of the file.
    If you have the file name and line number, use this tool.
    If you don't know the exact path, still use this tool.
    If you don't have the line number, then start with 1
3. show_root_cause:
    Use this tool to show the root cause of the error.
    If you have enough information to determine the root cause, use this tool.

IMPORTANT INSTRUCTIONS:
1. Use the current analysis state to avoid repeating searches or analysis.
2. If user pushes back saying you have already analyzed the code, make sure to don't ask again.
4. For fetch_logs:
   - NEVER request a page that has already been analyzed
   - ALWAYS use the exact page number specified in "NEXT PAGE TO REQUEST" in the header
   - If you see "ALL PAGES HAVE BEEN ANALYZED", use show_root_cause instead
5. Use ask_user when you need clarification, but try to be specific with your questions and provide context about why you need the information.

Respond with:
1. Your updated analysis of the situation
2. The most appropriate next tool and its parameters
3. If you can establish the root cause of the error, use show_root_cause tool.
Your response should clearly separate the analysis state from the tool choice.
"""
            # Log what we're sending to LLM
            logger.info("Sending to LLM:")
            logger.info(f"========================= User prompt ==========================")
            logger.info(user_prompt)
            logger.info(f"========================= System prompt ==========================")
            logger.info(system_prompt.split("\n")[:5])
            logger.info(f"========================= End of prompt ==========================")
            logger.info(f"Already analyzed information. Don't request the same information again.")
            logger.info(f"Files already fetched: {sorted(analysis_context.current_findings.get('fetched_files', set()))}")
            logger.info(f"Log pages already fetched: {sorted(analysis_context.current_findings.get('fetched_logs_pages', set()))}")
            logger.info(f"Code already fetched: {sorted(analysis_context.current_findings.get('fetched_code', set()))}")    
            # Call Claude using the SDK
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system_prompt,
                messages=[{"role": "user", 
                           "content": [
                               {"type": "text", "text": user_prompt,  "cache_control": {"type": "ephemeral"}},
                               {"type": "text", "text": history_prompt, "cache_control": {"type": "ephemeral"}}
                           ]}
                        ],
                tools=self.TOOLS,
                tool_choice={"type": "any"}
            )
            
            # Log response summary
            logger.info("Received from LLM")
            
            # Extract tool choice and analysis from content array
            content = response.content
            tool_response = None
            updated_analysis = None
            
            # Look for tool_use and text in content array
            for item in content:
                if item.type == 'tool_use':
                    tool_response = {
                        'tool': item.name,
                        'params': item.input,
                        'analysis': '',  # Tool calls don't include analysis text
                        'error': None
                    }
                elif item.type == 'text':
                    # The text response contains both analysis and state
                    text_parts = item.text.split("\nTool Choice:", 1)
                    if len(text_parts) > 1:
                        updated_analysis = text_parts[0].strip()
                        # Tool choice is handled by tool_use
                    else:
                        updated_analysis = item.text.strip()
            
            # If no valid content found, use empty response
            if not tool_response:
                tool_response = {
                    'tool': None,
                    'params': {},
                    'analysis': 'No valid response from LLM',
                    'error': None
                }
                
            # Log tool choice
            logger.info(f"- Tool requested: {tool_response['tool']}")
            if tool_response['tool'] == 'grep_files':
                logger.info(f"- Grepped files: {tool_response['params']['search_patterns']}")
            elif tool_response['tool'] == 'fetch_logs':
                logger.info(f"- Fetched logs page: {tool_response['params']['page_number']}")
            elif tool_response['tool'] == 'fetch_code':
                logger.info(f"- Fetched code: {tool_response['params']['filename']} at line {tool_response['params']['line_number']}")
            
            return tool_response
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error during LLM analysis: {error_msg}")
            
            # Handle rate limit errors specially
            if "rate_limit_error" in error_msg:
                time.sleep(5)  # Wait 5 seconds before next attempt
                return {
                    'tool': None,
                    'params': {},
                    'analysis': 'Rate limit reached. Please try again with a smaller context.',
                    'error': 'Rate limit error'
                }
            
            return {
                'tool': None,
                'params': {},
                'analysis': '',
                'error': error_msg
            }