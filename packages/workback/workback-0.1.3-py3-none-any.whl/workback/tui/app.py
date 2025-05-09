"""Main application for the WorkBack TUI."""

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Header, Footer, Input, RichLog, Static, Button, Label
from textual.worker import Worker, get_current_worker
from textual import work
from workback.tools.analysis_tools import AnalysisContext, Analyzer
from workback.tools.logger import WorkBackLogger
import os
import re
import asyncio
import time
import requests
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
from github import Github
from github.GithubException import GithubException

from workback.tools.claude_client import ClaudeClient

# Configure logging
logger = WorkBackLogger().get_logger("app")

class CommandBar(Static):
    """A bar displaying available commands."""
    
    def __init__(self):
        super().__init__()
        self.update_commands({
            "ctrl+q": "Quit",
            "/help": "Show help",
            "/clear": "Clear chat",
            "/analyze": "Analyze root cause",
            "/resume": "Resume analysis with provided file",
            "/answer": "Answer AI's question",
            "/github": "Analyze GitHub issue"
        })
    
    def update_commands(self, commands: dict) -> None:
        """Update the displayed commands."""
        command_text = " | ".join(f"{key}: {value}" for key, value in commands.items())
        self.update(f"[bold]{command_text}[/]")

class WorkBack(App):
    """A terminal-based AI chat interface with root cause analysis capabilities."""

    def __init__(self, *args, **kwargs):
        # Load CSS from external file
        css_path = Path(__file__).parent / "styles.css"
        with open(css_path, "r") as f:
            self.CSS = f.read()
            
        super().__init__(*args, **kwargs)
        self.analysis_context = None  # For storing analysis context
        self.analyzer = None  # Will be initialized when needed
        self.current_context = {}
        self.waiting_for = None  # Track what input we're waiting for
        self.current_logs = None  # Store the current log content
        self.current_log_path = None  # Store the current log file path
        self.llm_model = "claude-3-7-sonnet-20250219"  # LLM model to use
        self.api_key_file = os.path.expanduser("~/.workback/api_key")
        self.github_key_file = os.path.expanduser("~/.workback/github_key")
        self.current_report_file = None  # Store the current report file handle
        
        # Try to load API keys from files
        self.api_key = self._load_api_key()
        self.github_token = self._load_github_token()
        
        # Initialize Claude client - will use ANTHROPIC_API_KEY env var or stored key
        try:
            if self.api_key:
                self.claude = ClaudeClient(api_key=self.api_key, model=self.llm_model)
            else:
                self.claude = ClaudeClient(model=self.llm_model)  # Try env var
            self.claude_available = True
        except ValueError:
            self.claude_available = False

        # Initialize state
        self.pending_operation = None  # For storing operations that need API key
        self.dark_mode = False

    def compose(self) -> ComposeResult:
        """Compose the application layout."""
        # No header or footer to remove default commands
        with Container():
            with Vertical(id="chat-area"):
                yield RichLog(highlight=True, markup=True, id="chat-log")
            with Vertical(id="input-area"):
                yield Input(placeholder="Type your message here (Ctrl+I to interrupt)", id="user-input")
        with Vertical(id="command-bar"):
            yield CommandBar()

    def on_mount(self) -> None:
        """Handle the mount event."""
        self.query_one(Input).focus()

    def _create_report_file(self) -> None:
        """Create a new report file with timestamp."""
        # Create reports directory if it doesn't exist
        reports_dir = Path.home() / ".workback" / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = reports_dir / f"report-{timestamp}.md"
        
        # Close existing report file if open
        if self.current_report_file:
            self.current_report_file.close()
        
        # Open new report file
        self.current_report_file = open(report_path, "w")
        
        # Write header
        self.current_report_file.write(f"# WorkBack Analysis Report\n")
        self.current_report_file.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Log the report file creation
        logger.info(f"Created new report file: {report_path}")
        self.display_analysis(f"Created new report file: {report_path}")

    def display_analysis(self, message: str) -> None:
        """Display an analysis message in the chat log and write to report file."""
        # Create report file if it doesn't exist
        if not self.current_report_file:
            self._create_report_file()
        
        # Format message for display
        if message.startswith("Root Cause Analysis:"):
            display_msg = "[bold green]AI Root Cause:[/]" + message
            report_msg = f"## Root Cause Analysis\n{message}\n"
        else:
            display_msg = "[bold green][Workback Agent]: [/]" + message
            report_msg = f"{message}\n"
        
        # Write to chat log
        chat_log = self.query_one("#chat-log", RichLog)
        chat_log.write(display_msg)
        
        # Write to report file
        if self.current_report_file:
            self.current_report_file.write(report_msg)
            self.current_report_file.flush()  # Ensure immediate write
        
        # Force a refresh of the display
        self.refresh()

    def on_unmount(self) -> None:
        """Handle unmount event - close report file."""
        if self.current_report_file:
            self.current_report_file.close()
            self.current_report_file = None

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle submitted input."""
        user_input = event.value.strip()
        if not user_input:
            return

        input_widget = self.query_one("#user-input", Input)
        
        # Check if we're waiting for specific input
        if self.waiting_for:
            if self.waiting_for == "api_key":
                # Handle API key input
                self._handle_api_key_input(user_input)
                input_widget.value = ""
                input_widget.placeholder = "Type your message here (Ctrl+I to interrupt)"
                self.waiting_for = None
                return
            elif self.waiting_for == "github_token":
                # Handle GitHub token input
                self._handle_github_token_input(user_input)
                input_widget.value = ""
                input_widget.placeholder = "Type your message here (Ctrl+I to interrupt)"
                self.waiting_for = None
                return
            elif self.waiting_for == "analyze_file_path":
                self._process_log_file(user_input)
                input_widget.value = ""
                input_widget.placeholder = "Type your message here (Ctrl+I to interrupt)"
                self.waiting_for = None
                return
        
        # Handle command inputs
        if user_input.startswith("/"):
            self._handle_command(user_input)
            input_widget.value = ""
            return

        # Clear input field
        input_widget.value = ""

        
    def _handle_command(self, command_text: str) -> None:
        """Handle command inputs."""
        input_widget = self.query_one("#user-input", Input)
        
        # Split the command and args
        parts = command_text.split(None, 1)
        command = parts[0].lower()
        args_text = parts[1] if len(parts) > 1 else ""
        
        if command == "/help":
            help_text = """
[bold]Available Commands:[/]
- [bold]/help[/] - Show this help message
- [bold]/clear[/] - Clear the chat history
- [bold]/analyze[/] - Analyze logs for root cause
- [bold]/resume [file_path][/] - Resume analysis with specified file
- [bold]/apikey [key][/] - Set API key for Claude
- [bold]/apikey-status[/] - Check API key status
- [bold]/github [url][/] - Analyze a GitHub issue

[bold]Keyboard Shortcuts:[/]
- [bold]Ctrl+Q[/] - Quit the application
            """
            self.display_analysis(help_text)
        elif command == "/clear":
            chat_log = self.query_one("#chat-log", RichLog)
            chat_log.clear()
            self.display_analysis("Chat history cleared.")
        elif command == "/resume":
            if not args_text:
                self.display_analysis("Please provide a file path.")
                self.display_analysis("Usage: /resume <file_path>")
                return
            self._handle_resume(args_text)
        elif command == "/answer":
            if not args_text:
                self.display_analysis("Please provide your answer.")
                self.display_analysis("Usage: /answer <your response>")
                return
            self._handle_answer(args_text)
        elif command == "/apikey":
            # Handle API key command
            if not args_text:
                # Prompt for API key
                self._prompt_for_api_key()
            else:
                # Set API key directly
                self._handle_api_key_input(args_text)
        elif command == "/apikey-status":
            # Check API key status
            if self.claude_available:
                self.display_analysis("Claude API is configured and available.")
                
                # Show a masked version of the key
                if self.api_key:
                    masked_key = self.api_key[:7] + "..." + self.api_key[-4:] if len(self.api_key) > 11 else "***"
                    self.display_analysis(f"API Key: {masked_key}")
                else:
                    self.display_analysis("Using environment variable ANTHROPIC_API_KEY")
            else:
                self.display_analysis("Claude API is not available.")
                self.display_analysis("Note: Use /apikey to set your API key.")
        elif command == "/analyze":
            # Handle analyze workflow with file path input
            if not args_text:
                self.display_analysis("Please provide a log file path.")
                # Set the input widget to a special mode to capture the file path
                self.waiting_for = "analyze_file_path"
                input_widget.placeholder = "Enter path to log file"
                return
            else:
                # Process the file path directly
                self._process_log_file(args_text)
        elif command == "/github":
            if not args_text:
                self.display_analysis("Please provide a GitHub issue URL.")
                self.display_analysis("Usage: /github <github_issue_url>")
                return
            self._handle_github_issue(args_text)
    

    @work(thread=True)
    def _analyze_logs_with_llm(self, log_content: str) -> None:
        """Analyze logs with LLM to identify potential issues."""
        
        if not self.claude_available:
            # Store the operation for later resumption
            self.pending_operation = ("analyze_logs", log_content)
            
            # Prompt user for API key
            self._prompt_for_api_key()
            return
            
        # Create new analysis context and analyzer
        self.analysis_context = AnalysisContext(log_content)
        self.analyzer = Analyzer(analysis_context=self.analysis_context, display_callback=self.display_analysis)
            
        # Start recursive analysis
        try:
            # Start analysis
            self.analyzer.analyze()
            
        except Exception as e:
            self.display_analysis(f"Error: Failed to analyze logs: {str(e)}")

    @work(thread=True)        
    def _process_log_file(self, file_path: str) -> None:
        """Process a log file and send to LLM for analysis."""
        
        # Check if this is actually a command that was misinterpreted as a path
        if file_path.startswith("/") and len(file_path.split()) == 1 and not os.path.exists(file_path):
            known_commands = ["/help", "/clear", "/analyze", "/code", "/log", "/stack", "/callers", "/select"]
            if file_path in known_commands:
                self.display_analysis(f"'{file_path}' appears to be a command, not a file path.")
                self.display_analysis("Please provide an absolute path to a log file.")
                return
        
        # Try to read the file
        try:
            # Normal log file processing
            with open(file_path, 'r') as f:
                log_content = f.read()
                
            # Store the log content and path for later reference
            self.current_logs = log_content
            self.current_log_path = file_path
            
            # Display a sample of the log content
            self.display_analysis(f"Loaded logs from: {file_path}")
            
            # Get a sample to show (first 5 lines)
            sample_lines = log_content.split("\n")[:5]
            self.display_analysis("Analyzing logs...")
            for line in sample_lines:
                self.display_analysis(f"  {line}")
            
            if len(log_content.split("\n")) > 5:
                self.display_analysis("  ...")
            
            # Start analysis
            self._analyze_logs_with_llm(log_content)
            
        except Exception as e:
            self.display_analysis(f"Error: Could not read file: {str(e)}")
    
    def _load_api_key(self) -> Optional[str]:
        """Load API key from file."""
        try:
            if os.path.exists(self.api_key_file):
                with open(self.api_key_file, 'r') as f:
                    return f.read().strip()
        except Exception:
            # If we can't read the file, just return None
            pass
        return None
    
    def _save_api_key(self, api_key: str) -> bool:
        """Save API key to file."""
        try:
            # Make directory if it doesn't exist
            os.makedirs(os.path.dirname(self.api_key_file), exist_ok=True)
            
            # Save API key to file
            with open(self.api_key_file, 'w') as f:
                f.write(api_key)
            
            # Set file permissions to be readable only by the user
            os.chmod(self.api_key_file, 0o600)
            
            return True
        except Exception as e:
            self.display_analysis(f"Error saving API key: {str(e)}")
            return False
    
    def _prompt_for_api_key(self) -> None:
        """Prompt user for API key."""
        input_widget = self.query_one("#user-input", Input)
        
        self.display_analysis("Claude API key not found. Please enter your Anthropic API key.")
        self.display_analysis("Your key will be stored in ~/.workback/api_key")
        
        # Set the input widget to a special mode to capture the API key
        self.waiting_for = "api_key"
        input_widget.placeholder = "Enter your Anthropic API key (starts with 'sk-')"
    
    def _handle_api_key_input(self, api_key: str) -> None:
        """Handle API key input from user."""
        
        # Validate the API key format
        if not api_key.startswith("sk-"):
            self.display_analysis("Error: Invalid API key format. API keys start with 'sk-'.")
            self.display_analysis("Please enter a valid Anthropic API key.")
            return
        
        # Save the API key
        if self._save_api_key(api_key):
            self.api_key = api_key
            
            # Initialize Claude with the new key
            try:
                self.claude = ClaudeClient(api_key=self.api_key, model=self.llm_model)
                self.claude_available = True
                self.display_analysis("Success: API key saved and Claude initialized.")
                
                # If we were in the middle of an operation, continue
                if hasattr(self, 'pending_operation') and self.pending_operation:
                    operation, args = self.pending_operation
                    self.display_analysis("Resuming previous operation...")
                    
                    if operation == "analyze_logs":
                        self._analyze_logs_with_llm(args)
                    
                    self.pending_operation = None
            except ValueError as e:
                self.display_analysis(f"Error: Failed to initialize Claude with the provided key: {str(e)}")
        else:
            self.display_analysis("Error: Failed to save API key.")
    
    @work(thread=True)
    def _handle_resume(self, file_path: str) -> None:
        """Handle resuming analysis with the specified file."""
        
        # Call the resume command handler
        return self.analyzer.read_file(file_path)

    @work(thread=True)
    def _handle_answer(self, answer: str) -> None:
        """
        Handle user's answer to a previously asked question.
        
        Args:
            answer: The user's answer to the question
        """
        if not self.analyzer:
            self.display_analysis("Error: No active analysis session.")
            return
            
        try:
            # Get the current question from context
            question = self.analyzer.analysis_context.current_findings.get('user_question', {})
            if not question:
                self.display_analysis("Error: No pending question to answer.")
                return
                
            # Format content to include both question and answer
            content = (
                f"Question: {question.get('question', 'Unknown question')}\n"
                f"Answer: {answer}"
            )
            
            # Update context with the answer and continue analysis
            self.analyzer.analysis_context.update_state(
                current_page_content=content,
                increment_iterations=True,
                user_question=question,
                user_answer=answer
            )
            
            # Display the Q&A exchange
            self.display_analysis("Processing your answer...")
            self.display_analysis(content)
            
            # Continue analysis using the analyzer
            self.analyzer.analyze()

            logger.info("Successfully processed user's answer and continued analysis")
            
        except Exception as e:
            self.display_analysis(f"Error handling answer: {str(e)}")
        
    @work(thread=True)
    def _handle_github_issue(self, url: str) -> None:
        """Handle GitHub issue analysis."""
        try:
            # Parse the GitHub URL
            parsed_url = urlparse(url)
            if not parsed_url.netloc.endswith('github.com'):
                self.display_analysis("Error: Not a valid GitHub URL")
                return
                
            # Extract owner, repo, and issue number
            path_parts = parsed_url.path.strip('/').split('/')
            if len(path_parts) < 4 or path_parts[2] != 'issues':
                self.display_analysis("Error: Not a valid GitHub issue URL")
                return
                
            owner = path_parts[0]
            repo = path_parts[1]
            issue_number = int(path_parts[3])
            
            # Get GitHub token from file or environment
            github_token = self.github_token or os.environ.get('GITHUB_TOKEN')
            if not github_token:
                # Store the operation for later resumption
                self.pending_operation = ("github_issue", url)
                
                # Prompt user for GitHub token
                self._prompt_for_github_token()
                return
            
            # Initialize GitHub client
            g = Github(github_token)
            
            try:
                # Get repository and issue
                repository = g.get_repo(f"{owner}/{repo}")
                issue = repository.get_issue(issue_number)
                
                # Format issue content for analysis
                issue_content = f"""GitHub Issue: {issue.title}
URL: {url}
State: {issue.state}
Created: {issue.created_at}
Updated: {issue.updated_at}
Labels: {', '.join(label.name for label in issue.labels)}
Assignee: {issue.assignee.login if issue.assignee else 'None'}

Description:
{issue.body}

Comments:
"""
                # Add comments
                for comment in issue.get_comments():
                    issue_content += f"\n--- Comment by {comment.user.login} on {comment.created_at} ---\n"
                    issue_content += f"{comment.body}\n"
                
                # Start analysis with the issue content
                self._analyze_logs_with_llm(issue_content)
                
            except GithubException as e:
                self.display_analysis(f"Error accessing GitHub: {str(e)}")
            finally:
                g.close()
            
        except Exception as e:
            self.display_analysis(f"Error processing GitHub issue: {str(e)}")

    def _load_github_token(self) -> Optional[str]:
        """Load GitHub token from file."""
        try:
            if os.path.exists(self.github_key_file):
                with open(self.github_key_file, 'r') as f:
                    return f.read().strip()
        except Exception:
            # If we can't read the file, just return None
            pass
        return None
    
    def _save_github_token(self, token: str) -> bool:
        """Save GitHub token to file."""
        try:
            # Make directory if it doesn't exist
            os.makedirs(os.path.dirname(self.github_key_file), exist_ok=True)
            
            # Save token to file
            with open(self.github_key_file, 'w') as f:
                f.write(token)
            
            # Set file permissions to be readable only by the user
            os.chmod(self.github_key_file, 0o600)
            
            return True
        except Exception as e:
            self.display_analysis(f"Error saving GitHub token: {str(e)}")
            return False
    
    def _prompt_for_github_token(self) -> None:
        """Prompt user for GitHub token."""
        input_widget = self.query_one("#user-input", Input)
        
        self.display_analysis("GitHub token not found. Please enter your GitHub token.")
        self.display_analysis("Your token will be stored in ~/.workback/github_key")
        
        # Set the input widget to a special mode to capture the token
        self.waiting_for = "github_token"
        input_widget.placeholder = "Enter your GitHub token"
    
    def _handle_github_token_input(self, token: str) -> None:
        """Handle GitHub token input from user."""
        
        # Save the token
        if self._save_github_token(token):
            self.github_token = token
            self.display_analysis("Success: GitHub token saved.")
            
            # If we were in the middle of an operation, continue
            if hasattr(self, 'pending_operation') and self.pending_operation:
                operation, args = self.pending_operation
                self.display_analysis("Resuming previous operation...")
                
                if operation == "github_issue":
                    self._handle_github_issue(args)
                
                self.pending_operation = None
        else:
            self.display_analysis("Error: Failed to save GitHub token.")
        