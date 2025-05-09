"""
Analysis context for a debugging session.

This module defines the AnalysisContext class, which centralizes state management for 
the debugging analysis process. All state updates should go through the methods provided 
by this class to ensure consistency, proper logging, and maintainability.

The design follows a centralized state management pattern where:
1. All state updates go through well-defined methods
2. Each method has a single responsibility
3. Updates are logged consistently
4. The class is the single source of truth for the analysis state
"""

from typing import Dict, Any, Optional, List, Set, Union
from .logger import WorkBackLogger
import enum

# Configure logging
logger = WorkBackLogger().get_logger("analysis_context")

class AnalysisContext:
    """
    Analysis context for a debugging session.
    
    This class centralizes all state management for the analysis process. It provides methods
    to update various aspects of the analysis state, ensuring consistent updates and proper logging.
    
    Key features:
    - Centralized state updates through the update_state method
    - Specialized methods for common update patterns (e.g., adding searched patterns, fetched files)
    - Consistent logging for all state changes
    - Methods for page navigation and content retrieval
    
    All state modifications should go through this class's methods rather than directly
    modifying attributes, to ensure consistency and proper tracking.
    """
    current_findings: Dict[str, Any]  # Findings so far
    current_page: int = 0  # Current page number (0-based internally)
    total_pages: int = 0  # Total number of pages
    page_size: int = 50000  # Characters per page
    overlap_size: int = 5000  # Characters of overlap between pages
    all_logs: str = ""  # Complete log content
    current_page_content: Optional[str] = None  # Content of the current page being analyzed 
    iterations: int = 0
    MAX_ITERATIONS = 50
    history = ''
    
    def __init__(self, initial_input: str):
        self.current_findings = {
            "searched_patterns": set(),
            "fetched_logs_pages": set([1]),
            "fetched_code": set(),
            "savedState": "",
            "InvestigationGoal": "",
            "resending_logs": False,
            "fetched_files": set(),
            "user_question": None,  # Store the current question
        }
        
        self.all_logs = initial_input
        self.analyzed_pages: Set[int] = set()  # Initialize analyzed_pages set
        # Calculate total pages based on content length and overlap
        self.total_pages = max(1, (len(initial_input) + self.page_size - 1) // (self.page_size - self.overlap_size))
        self.current_page = 0  # Start at first page (0-based internally)
        self.current_page_content = "Logs: \n Page 1 of " + str(self.total_pages) + ":\n" + self.get_current_page() 
        logger.info(f"Total pages of Logs: {self.total_pages}")
        self.history = f"Shared page 1 of {self.total_pages} of logs"
    
    def update_state(self, 
                     current_page_content: Optional[str] = None,
                     resending_logs: Optional[bool] = None,
                     current_analysis: Optional[str] = None,
                     investigation_goal: Optional[str] = None,
                     increment_iterations: bool = False,
                     searched_patterns: Optional[Union[List[str], Set[str]]] = None,
                     fetched_files: Optional[Union[List[str], Set[str]]] = None,
                     fetched_code: Optional[tuple] = None,
                     fetched_log_page: Optional[int] = None,
                     code_request: Optional[Dict[str, Any]] = None,
                     user_question: Optional[Dict[str, Any]] = None,
                     user_answer: Optional[str] = None) -> None:
        """
        Comprehensive central method to update the analysis context state.
        
        Args:
            current_page_content: Updated content for the current page
            resending_logs: Whether logs are being resent
            current_analysis: Updated current analysis string
            investigation_goal: Updated investigation goal
            increment_iterations: Whether to increment the iterations counter
            searched_patterns: Patterns to add to searched_patterns set
            fetched_files: Files to add to fetched_files set
            fetched_code: Tuple of (file_path, line_number) to add to fetched_code set
            fetched_log_page: Page number to add to fetched_logs_pages set
            code_request: Dictionary with code request details (filename, line_number, tool_params)
            user_question: Dictionary with user question details (question, context, tool_params)
        """
        if current_page_content is not None:
            self.current_page_content = current_page_content
            logger.info("Updated current page content")
            
        if resending_logs is not None:
            self.current_findings["resending_logs"] = resending_logs
            logger.info(f"Updated resending_logs to {resending_logs}")
            
        if current_analysis is not None:
            self.current_findings["savedState"] = current_analysis
            logger.info(f"Updated current analysis")
            
        if investigation_goal is not None:
            self.current_findings["InvestigationGoal"] = investigation_goal
            logger.info(f"Updated investigation goal")
            
        if searched_patterns is not None:
            self.current_findings["searched_patterns"].update(searched_patterns)
            logger.info(f"Added searched patterns: {searched_patterns}")
            self.history += f"\nSearched for patterns: {searched_patterns}"
            
        if fetched_files is not None:
            self.current_findings["fetched_files"].update(fetched_files)
            logger.info(f"Added fetched files: {len(fetched_files)} files")
            if (len(fetched_files) > 10):
                self.history += f"\nGrepping files resulted in {len(fetched_files)} files and I asked you to request more specific search patterns"
            else:
                self.history += f"\nFetched files: {', '.join(fetched_files)}"
        if fetched_code is not None:
            file_path, line_number, start, end, total_lines, code_context = fetched_code
            self.current_findings["fetched_code"].add((file_path, line_number))
            self.history += f"\nYou requested code from {file_path} at line {line_number}. I shared from {start} to {end}. Total code size: {total_lines} lines."
            self.history += f"Code sample from {max(start, line_number-5)} to {min(end, line_number+5)}.\n"
            self.history += f"{'\n'.join(code_context)}\n"
            logger.info(f"Added fetched code: {file_path}:{line_number}")
            
        if fetched_log_page is not None:
            self.current_findings["fetched_logs_pages"].add(fetched_log_page)
            logger.info(f"Added fetched log page: {fetched_log_page}")
            self.history += f"\nFetched log page: {fetched_log_page}"
        if code_request is not None:
            self.current_findings['requested_code'] = code_request
            logger.info(f"Set code request for {code_request.get('filename')}:{code_request.get('line_number')}")
        if user_question is not None:
            self.current_findings['user_question'] = user_question
            logger.info(f"Set user question: {user_question.get('question')}")
            self.history += f"\nAsked user question: {user_question.get('question')}"
        if user_answer is not None:
            self.history += f"\nUser answered: {user_answer}"
        if increment_iterations:
            self.iterations += 1
            logger.info(f"Incremented iterations to {self.iterations}")
    
    def set_code_request(self, filename: str, line_number: int, tool_params: Dict[str, Any]) -> None:
        """
        Store a code request for later resumption.
        
        Args:
            filename: Path to the file
            line_number: Line number in the file
            tool_params: Tool parameters from the LLM
        """
        code_request = {
            'filename': filename,
            'line_number': line_number,
            'tool_params': tool_params
        }
        self.update_state(code_request=code_request)
    
    def update_page_content_for_logs(self, page_number: Optional[int] = None) -> None:
        """
        Update current_page_content with the content of the current page.
        
        Args:
            page_number: Optional specific page number to display (1-based)
        """
        if page_number is not None:
            self.current_page_content = f"""
Sending Logs: Page : {page_number} of {self.get_total_pages()}
Page Content: {self.get_page_content(page_number-1)}
"""
        else:
            self.current_page_content = "Logs: \n Page " + str(self.get_current_page_number()) + " of " + str(self.get_total_pages()) + ":\n" + self.get_current_page()
        
        logger.info(f"Updated page content for logs, page {page_number if page_number is not None else self.get_current_page_number()}")
        
    def get_current_page(self) -> str:
        """Get the current page of logs with overlap."""
        # Calculate start and end positions based on 0-based page number
        start = max(0, self.current_page * (self.page_size - self.overlap_size))
        end = min(len(self.all_logs), start + self.page_size)
        
        # If this is not the first page, include overlap from previous page
        if self.current_page > 0:
            start = max(0, start - self.overlap_size)
            
        return self.all_logs[start:end]

    def advance_page(self) -> bool:
        """
        Advance to next page. Returns False if no more pages.
        Note: Uses 0-based page numbers internally.
        """
        if self.current_page + 1 >= self.total_pages:
            return False
        self.current_page += 1
        return True

    def get_current_page_number(self) -> int:
        """Get the current page number in 1-based format for external use."""
        return self.current_page + 1

    def get_total_pages(self) -> int:
        """Get the total number of pages."""
        return self.total_pages

    def mark_page_analyzed(self, page_number: int) -> None:
        """Mark a page as analyzed (using 1-based page numbers)."""
        self.analyzed_pages.add(page_number)

    def is_page_analyzed(self, page_number: int) -> bool:
        """Check if a page has been analyzed (using 1-based page numbers)."""
        return page_number in self.analyzed_pages

    def get_analyzed_pages(self) -> List[int]:
        """Get list of analyzed pages in sorted order (1-based)."""
        return sorted(list(self.analyzed_pages)) 
        
    def get_page_content(self, page_number: int) -> str:
        """Get the content of a specific page."""
        start = max(0, page_number * (self.page_size - self.overlap_size))
        end = min(len(self.all_logs), start + self.page_size)
        return self.all_logs[start:end]

    def set_user_question(self, question: str, tool_params: Dict[str, Any]) -> None:
        """
        Store a user question for later resumption.
        
        Args:
            question: The question to ask the user
            tool_params: Tool parameters from the LLM including optional context
        """
        user_question = {
            'question': question,
            'context': tool_params.get('context'),
            'tool_params': tool_params
        }
        self.update_state(user_question=user_question)
