"""Tools for analyzing logs, stack traces, and code locations."""

import os
import time
import subprocess
from dataclasses import dataclass
from typing import List, Optional, Callable, Any, Dict, Set
from .claude_client import ClaudeClient
from .analysis_context import AnalysisContext
from .logger import WorkBackLogger
from collections import defaultdict

# Configure logging
logger = WorkBackLogger().get_logger("analysis_tools")

@dataclass
class CodeLocation:
    file_path: str
    line_number: int
    function_name: Optional[str] = None
    
    def __str__(self) -> str:
        return f"{self.file_path}:{self.line_number}"

@dataclass
class StackTraceEntry:
    code_location: CodeLocation
    context: Optional[str] = None

class Analyzer:
    """Analyzer for debugging issues using Claude."""

    def __init__(self, workspace_root: Optional[str] = None, analysis_context: Optional[AnalysisContext] = None, display_callback: Optional[Callable[[str], None]] = None):
        """Initialize the analyzer."""
        self.workspace_root = workspace_root or os.getcwd()
        logger.info(f"Initialized analyzer with workspace root: {self.workspace_root}")
        
        # Load API key from ~/.workback/api_key
        api_key = None
        api_key_file = os.path.expanduser("~/.workback/api_key")
        try:
            if os.path.exists(api_key_file):
                with open(api_key_file, 'r') as f:
                    api_key = f.read().strip()
        except Exception:
            pass
            
        self.claude = ClaudeClient(api_key=api_key)
        
        # Store display callback - ensure it's callable
        if display_callback is not None and not callable(display_callback):
            logger.warning(f"display_callback provided but not callable: {type(display_callback)}")
            display_callback = None
        self.display_callback = display_callback
        self.analysis_context = analysis_context
        
    def analyze(self) -> None:
        """
        Analyze input using Claude and execute suggested tools.
        """
        
        # Initialize context if not provided
        if not self.analysis_context:
            raise ValueError("Analysis context not provided")
        
        # Prevent infinite recursion
        if self.analysis_context.iterations >= self.analysis_context.MAX_ITERATIONS:
            logger.warning(f"Analysis stopped: Maximum iterations ({self.analysis_context.MAX_ITERATIONS}) reached")
            if callable(self.display_callback):
                self.display_callback(f"Analysis stopped: Maximum iterations ({self.analysis_context.MAX_ITERATIONS}) reached")
            return
            
        # Log iteration start
        logger.info(f"=== Iteration {self.analysis_context.iterations} ===")
        
        response = self.claude.analyze_error(self.analysis_context)
        
        if not response or 'tool' not in response:
            logger.error("Invalid response from Claude")
            return
            
        tool_name = response.get('tool')
        tool_params = response.get('params', {})
        analysis = response.get('analysis', '')
            
        if callable(self.display_callback) and analysis:
            self.display_callback(analysis)
        # Update both current analysis and investigation goal in a single call if available
        current_analysis = tool_params.get('savedState')
        investigation_goal = tool_params.get('InvestigationGoal')
        
        if (current_analysis or investigation_goal) and callable(self.display_callback):
            if investigation_goal:
                self.display_callback(f"[bold yellow]Current Goal:[/] {investigation_goal}")
            if current_analysis:
                self.display_callback(f"[bold yellow]Analysis so far:[/] {current_analysis}")
            
            self.analysis_context.update_state(
                current_analysis=current_analysis,
                investigation_goal=investigation_goal
            )

        try:
            # Execute the suggested tool
            if tool_name == 'grep_files':
                search_patterns = tool_params.get('search_patterns', [])
                if search_patterns:
                    self._grep_files(self.analysis_context, search_patterns)
                    # Use centralized method to increment iterations
                    self.analysis_context.update_state(increment_iterations=True)
                    if callable(self.display_callback):
                        self.display_callback(f"Iteration {self.analysis_context.iterations}: Sending matched files to LLM")
                    self.analyze()
                    return
            elif tool_name == 'fetch_logs':
                page_number = tool_params.get('page_number')
                
                if page_number is not None and page_number in self.analysis_context.current_findings['fetched_logs_pages']:
                    logger.warning(f"Page {page_number} has already been analyzed, resending")
                    # Use centralized update methods
                    self.analysis_context.update_state(resending_logs=True)
                    self.analysis_context.update_page_content_for_logs(page_number)
                    
                    self.analyze()
                    return             
                
                if self.analysis_context.advance_page():
                    # Update content for logs first (needs to happen before the state update)
                    self.analysis_context.update_page_content_for_logs()
                    
                    # Use consolidated update method
                    self.analysis_context.update_state(
                        resending_logs=False,
                        fetched_log_page=page_number
                    )
                    
                    if callable(self.display_callback):
                        self.display_callback(f"Sending next page to LLM")
                    self.analyze()
                else:
                    # No more pages - update state accordingly
                    self.analysis_context.update_state(
                        current_page_content="No more pages to analyze",
                        resending_logs=True  # Note: this matches the behavior in the original code
                    )
                    
                    if callable(self.display_callback):
                        self.display_callback(f"No more pages to analyze. Letting LLM know")
                    self.analyze()
                return
                    
            elif tool_name == 'fetch_code':
                filename = tool_params.get('filename')
                line_number = tool_params.get('line_number')
                self.analysis_context.set_code_request(filename, line_number, tool_params)

                if filename and line_number:
                    # Check if we've already analyzed this file and line
                    if (filename, line_number) in self.analysis_context.current_findings["fetched_code"]:
                        if callable(self.display_callback):
                            self.display_callback(f"Already analyzed file {filename} at line {line_number}. Not sharing again to avoid loops.")
                        self.analysis_context.update_state(
                            current_page_content=f"Already analyzed file {filename} at line {line_number}. Not sharing again to avoid loops.",
                            increment_iterations=True)
                        self.analyze()
                        return

                    # Try to find the file first
                    found_path = self._find_file(filename)
                    if found_path:
                        # File found, read it directly
                        self.read_file(found_path)
                        return
                    else:
                        # Ask user to provide directory for file search
                        if callable(self.display_callback):
                            self.display_callback(f"Could not find file: [bold yellow]{filename}[/]")
                            self.display_callback("Please provide the file path using: [bold yellow]/resume <file with path>[/]")
                        return
                    
            elif tool_name == 'ask_user':
                question = tool_params.get('question')
                context = tool_params.get('context')
                if question:
                    # Store the question in analysis context
                    self.analysis_context.set_user_question(question, tool_params)
                    
                    # Display the question and optional context to user
                    if callable(self.display_callback):
                        if context:
                            self.display_callback(f"Context: {context}")
                        self.display_callback(f"Question: {question}")
                        self.display_callback("Use /answer <your response> to continue analysis")
                    return

            elif tool_name == 'show_root_cause':
                root_cause = tool_params.get('root_cause', '')
                if root_cause and callable(self.display_callback):
                    self.display_callback(f"\nRoot Cause Analysis:\n{root_cause}")
                return
                
            else:
                logger.warning(f"Unknown tool: {tool_name}")
                return
            
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {str(e)}")
            if callable(self.display_callback):
                self.display_callback(f"Error executing tool {tool_name}: {str(e)}")

    def _get_gitignore_dirs(self) -> List[str]:
        """Get directory patterns from .gitignore file."""
        gitignore_path = os.path.join(self.workspace_root, '.gitignore')
        dirs_to_exclude = set()
        
        try:
            if os.path.exists(gitignore_path):
                with open(gitignore_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        # Skip comments and empty lines
                        if not line or line.startswith('#'):
                            continue
                        # Look for directory patterns (ending with /)
                        if line.endswith('/'):
                            dirs_to_exclude.add(line.rstrip('/'))
                        # Also add common build/binary directories if not already specified
                dirs_to_exclude.update(['target', 'node_modules', '.git', 'dist', 'build'])
                logger.info(f"Found directories to exclude: {sorted(dirs_to_exclude)}")
            else:
                logger.info("No .gitignore file found, using default exclusions")
                dirs_to_exclude = {'target', 'node_modules', '.git', 'dist', 'build'}
        except Exception as e:
            logger.error(f"Error reading .gitignore: {str(e)}")
            dirs_to_exclude = {'target', 'node_modules', '.git', 'dist', 'build'}
            
        return sorted(list(dirs_to_exclude))
        
    def _grep_files(self, context: AnalysisContext, search_patterns: List[str]) -> None:
        """
        Search for files based on patterns, both in file contents and file names.
        
        Args:
            context: Analysis context
            search_patterns: List of patterns to search for
        """
        logger.info("=== File Search Request ===")
        logger.info(f"- Patterns: {', '.join(search_patterns)}")
        
        # Track timing and results
        start_time = time.time()
        found_files = set()
        patterns_matched = defaultdict(lambda: {"content": 0, "name": 0})

        self.display_callback(f"Searching for files matching patterns: {', '.join(search_patterns)}")
        
        try:
            # Get directories to exclude from .gitignore
            exclude_dirs = self._get_gitignore_dirs()
            exclude_args = []
            for dir_name in exclude_dirs:
                exclude_args.extend(['--exclude-dir', dir_name])
            
            # Search for each pattern
            for pattern in search_patterns:
                try:
                    # Search file contents using grep
                    grep_cmd = ['grep', '-r', '-n', *exclude_args, pattern]
                    if self.workspace_root:
                        grep_cmd.append(self.workspace_root)
                    else:
                        grep_cmd.append('.')
                    
                    grep_result = subprocess.run(grep_cmd, capture_output=True, text=True)
                    
                    # grep returns 0 if matches found, 1 if no matches (not an error)
                    if grep_result.returncode not in [0, 1]:
                        logger.error(f"Grep command failed: {grep_result.stderr}")
                    else:
                        # Process grep output to get file paths and line numbers
                        content_matches = {}
                        for line in grep_result.stdout.splitlines():
                            # grep -n output format: file:line:content
                            parts = line.split(':', 2)
                            if len(parts) >= 2:
                                file_path = parts[0]
                                line_num = int(parts[1])
                                if file_path not in content_matches:
                                    content_matches[file_path] = []
                                content_matches[file_path].append(line_num)
                        
                        found_files.update(content_matches.keys())
                        patterns_matched[pattern]["content"] = len(content_matches)
                        patterns_matched[pattern]["line_numbers"] = content_matches
                    
                    # Search filenames using find
                    # Escape special characters in pattern for find
                    escaped_pattern = pattern.replace('(', '\\(').replace(')', '\\)').replace('[', '\\[').replace(']', '\\]')
                    find_cmd = ['find']
                    if self.workspace_root:
                        find_cmd.append(self.workspace_root)
                    else:
                        find_cmd.append('.')
                    
                    # Add exclusions for directories
                    for dir_name in exclude_dirs:
                        find_cmd.extend(['-not', '-path', f'*/{dir_name}/*'])
                    
                    # Add the name pattern
                    find_cmd.extend(['-type', 'f', '-iname', f'*{escaped_pattern}*'])
                    
                    find_result = subprocess.run(find_cmd, capture_output=True, text=True)
                    
                    if find_result.returncode == 0:
                        name_matches = set(find_result.stdout.splitlines())
                        found_files.update(name_matches)
                        patterns_matched[pattern]["name"] = len(name_matches)
                    else:
                        logger.error(f"Find command failed: {find_result.stderr}")
                    
                except Exception as e:
                    logger.error(f"Error searching for pattern '{pattern}': {str(e)}")
                    continue
                
        except Exception as e:
            logger.error(f"Error during file search: {str(e)}")
            return
            
        # Calculate total duration
        total_duration = time.time() - start_time
        
        # Log search results
        logger.info("Search Results:")
        logger.info(f"- Total files found: {len(found_files)}")
        logger.info("- Pattern matches:")
        for pattern, counts in patterns_matched.items():
            logger.info(f"  • '{pattern}': {counts['content']} files (content), {counts['name']} files (name)")
        
        # Handle the results
        if found_files:
            if len(found_files) > 10:
                results_msg = []
                results_msg.append(f"Found {len(found_files)} total files matching patterns: {', '.join(search_patterns)}")
                results_msg.append(f"These are too many files and doesn't help with debugging")
                results_msg.append(f"Please request more specific patterns so you will have manageable number of files")
                
                # Use consolidated update method
                context.update_state(
                    current_page_content="\n".join(results_msg),
                    searched_patterns=search_patterns
                )
                
                if callable(self.display_callback):
                    self.display_callback("Telling LLM to request more specific patterns")
                return
            
            # Format results message
            results_msg = [f"Found {len(found_files)} total files matching patterns: {', '.join(search_patterns)}"]
            results_msg.append("\nMatches by pattern:")
            for pattern, counts in patterns_matched.items():
                results_msg.append(f"• '{pattern}': {counts['content']} files (content matches), {counts['name']} files (name matches)")
                if "line_numbers" in counts:
                    results_msg.append("  Line numbers by file:")
                    for file_path, lines in counts["line_numbers"].items():
                        results_msg.append(f"    - {file_path}: lines {', '.join(map(str, sorted(lines)))}")
            
            results_msg.append("\nList of files:")
            results_msg.extend(sorted(found_files))
            
            # Update context with the results message and add search patterns and files in one call
            context.update_state(
                current_page_content="\n".join(results_msg),
                searched_patterns=search_patterns,
                fetched_files=found_files
            )
            
            if callable(self.display_callback):
                summary = f"Found {len(found_files)} files matching patterns"
                details = []
                for pattern, counts in patterns_matched.items():
                    if counts['content'] > 0 or counts['name'] > 0:
                        details.append(f"'{pattern}': {counts['content']} content matches, {counts['name']} filename matches")
                if details:
                    summary += "\n" + "\n".join(details)
                self.display_callback(summary)
        else:
            # Update context with no files found message and add searched patterns in one call
            context.update_state(
                current_page_content=f"No files found matching patterns: {', '.join(search_patterns)}",
                searched_patterns=search_patterns
            )
            
            if callable(self.display_callback):
                self.display_callback("No files found matching patterns")

    def _translate_path(self, filename: str) -> List[str]:
        """
        Translate a filename to possible local paths.
        
        Args:
            filename: The filename to translate
            
        Returns:
            List of possible local paths
        """
        possible_paths = []
        
        # Try direct path
        if os.path.isabs(filename):
            possible_paths.append(filename)
        
        # Try relative to workspace root
        workspace_path = os.path.join(self.workspace_root, filename)
        possible_paths.append(workspace_path)
        
        # Try without leading path components
        base_name = os.path.basename(filename)
        possible_paths.append(os.path.join(self.workspace_root, base_name))
        
        # Try progressively removing path components
        path_parts = filename.split('/')
        for i in range(len(path_parts)):
            partial_path = '/'.join(path_parts[i:])
            possible_paths.append(os.path.join(self.workspace_root, partial_path))
        
        return possible_paths

    def _find_file(self, filename: str) -> Optional[str]:
        """
        Try to find a file in the workspace using various path combinations.
        
        Args:
            filename: The filename to find
            
        Returns:
            The full path to the file if found, None otherwise
        """
        possible_paths = self._translate_path(filename)
        
        for path in possible_paths:
            if os.path.isfile(path):
                logger.info(f"Found file at: {path}")
                self.display_callback(f"Found file at: {path}")
                return path
                
        logger.info(f"Could not find file {filename} in any of the possible locations")
        self.display_callback(f"Could not find file {filename} in any of the possible locations")
        return None

    def read_file(self, file_path: str):
        """
        Read a file and update context with its contents.
        This is used when resuming analysis after a fetch_code request.
        
        Args:
            file_path: Path to the file to read
        """
        if not self.analysis_context:
            logger.error("No context available for reading file")
            return
            
        try:
            line_number = self.analysis_context.current_findings['requested_code']['line_number']
            # Read the file
            with open(file_path, 'r') as f:
                code = f.read()
                
            # Get code context (50 lines before and after)
            lines = code.split('\n')
            start = max(0, line_number - 50)
            end = min(len(lines), line_number + 50)
            code_context = '\n'.join(lines[start:end])
            
            # Format content for display
            content = (
                f"You Requested Code:\nFile: {file_path}\nLine: {line_number}\n\n"
                f"Sharing the code from lines {start} to {end} of the file {file_path}\n\n"
                f"Code Context:\n{code_context}"
            )
            
            # Use consolidated update method with all changes in one call
            self.analysis_context.update_state(
                current_page_content=content,
                increment_iterations=True,
                fetched_code=(file_path, line_number, start, end, len(lines), lines[max(0, line_number-5):min(len(lines), line_number+5)])

            )
            
            # Only call display_callback if it's a callable
            if callable(self.display_callback):
                self.display_callback(f"Sending file: {file_path} at line: {line_number}")
                for line in lines[max(0, line_number-5):min(len(lines), line_number+5)]:
                    self.display_callback(f"       {line}")
                self.display_callback(f"       ...\n")
            
            # Continue analysis
            self.analyze()

            logger.info(f"Successfully read file {file_path} around line {line_number} and continued analysis")
            
        except Exception as e:
            logger.error(f"Error reading file: {str(e)}")
            if callable(self.display_callback):
                self.display_callback(f"Error reading file: {str(e)}")

    def _search_files(self, pattern: str) -> Set[str]:
        """
        Search for files containing a pattern.
        
        Args:
            pattern: Pattern to search for
            
        Returns:
            Set of file paths that contain the pattern
        """
        # Get directories to exclude from .gitignore
        exclude_dirs = self._get_gitignore_dirs()
        exclude_args = []
        for dir_name in exclude_dirs:
            exclude_args.extend(['--exclude-dir', dir_name])
        
        try:
            # Use grep with recursive search and exclusions
            grep_cmd = ['grep', '-r', '-l', *exclude_args, pattern]
            if self.workspace_root:
                grep_cmd.append(self.workspace_root)
            else:
                grep_cmd.append('.')
            
            grep_result = subprocess.run(grep_cmd, capture_output=True, text=True)
            
            # grep returns 0 if matches found, 1 if no matches (not an error)
            if grep_result.returncode not in [0, 1]:
                logger.error(f"Grep command failed: {grep_result.stderr}")
                return set()
            
            # Return set of matching files
            return set(grep_result.stdout.splitlines())
            
        except Exception as e:
            logger.error(f"Error searching for pattern '{pattern}': {str(e)}")
            return set() 