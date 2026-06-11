import json
import re
from anthropic import Anthropic
from tools.app_launcher import AppLauncher
from tools.file_generator import FileGenerator
from tools.email_sender import EmailSender
from tools.web_scraper import WebScraper
from config import DEBUG

class PersonalAgent:
    """Main AI agent that orchestrates tasks using Claude"""
    
    def __init__(self):
        self.client = Anthropic()
        self.model = "claude-3-5-sonnet-20241022"
        self.conversation_history = []
        
        # Initialize tools
        self.app_launcher = AppLauncher()
        self.file_generator = FileGenerator()
        self.email_sender = EmailSender()
        self.web_scraper = WebScraper()
        
        self.system_prompt = """You are a helpful personal task automation assistant. Your goal is to help the user by:
1. Opening applications when asked
2. Generating documents, code, and content
3. Sending emails
4. Browsing the web and summarizing content
5. Performing complex multi-step tasks

When the user asks you to do something, analyze what tools you need and provide clear, step-by-step instructions.

Available tools:
- app_launcher: Open applications and URLs
- file_generator: Create documents, code, reports
- email_sender: Send emails with attachments
- web_scraper: Get page content, summarize videos

Always be helpful, clear, and confirm before taking major actions."""
    
    def process_command(self, user_input: str) -> str:
        """
        Process a user command and execute the appropriate action
        
        Args:
            user_input: The user's natural language command
            
        Returns:
            Response from the agent
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Get response from Claude
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=self.system_prompt,
            messages=self.conversation_history
        )
        
        assistant_message = response.content[0].text
        
        # Add assistant response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        if DEBUG:
            print(f"[DEBUG] User: {user_input}")
            print(f"[DEBUG] Assistant: {assistant_message}")
        
        # Try to extract and execute actions from the response
        actions = self._extract_actions(user_input, assistant_message)
        
        if actions:
            execution_results = self._execute_actions(actions)
            
            # If actions were executed, get a follow-up response from Claude
            if execution_results:
                action_summary = self._summarize_actions(execution_results)
                
                self.conversation_history.append({
                    "role": "user",
                    "content": f"I've completed these actions: {action_summary}"
                })
                
                follow_up = self.client.messages.create(
                    model=self.model,
                    max_tokens=1024,
                    system=self.system_prompt,
                    messages=self.conversation_history
                )
                
                final_response = follow_up.content[0].text
                self.conversation_history.append({
                    "role": "assistant",
                    "content": final_response
                })
                
                return final_response
        
        return assistant_message
    
    def _extract_actions(self, user_input: str, response: str) -> list:
        """Extract actionable items from the conversation"""
        actions = []
        
        # Check for app launching
        if any(phrase in user_input.lower() for phrase in ["open", "launch", "start", "run"]):
            apps = self._extract_apps(user_input)
            for app in apps:
                actions.append({"type": "launch_app", "app": app})
        
        # Check for file generation
        if any(phrase in user_input.lower() for phrase in ["generate", "create", "write", "make"]):
            actions.append({"type": "generate_file", "input": user_input})
        
        # Check for email
        if any(phrase in user_input.lower() for phrase in ["email", "mail", "send"]):
            actions.append({"type": "send_email", "input": user_input})
        
        # Check for web/video
        if any(phrase in user_input.lower() for phrase in ["youtube", "video", "summarize", "summarise", "watch"]):
            actions.append({"type": "web_action", "input": user_input})
        
        return actions
    
    def _extract_apps(self, text: str) -> list:
        """Extract application names from text"""
        common_apps = ["chrome", "firefox", "spotify", "discord", "slack", "vscode", 
                      "youtube", "gmail", "twitter", "reddit", "calculator", "notepad"]
        
        apps = []
        text_lower = text.lower()
        
        for app in common_apps:
            if app in text_lower:
                apps.append(app)
        
        return apps
    
    def _execute_actions(self, actions: list) -> list:
        """Execute the extracted actions"""
        results = []
        
        for action in actions:
            try:
                if action["type"] == "launch_app":
                    result = self.app_launcher.launch_app(action["app"])
                    results.append(result)
                
                elif action["type"] == "generate_file":
                    # Ask Claude for file details
                    file_prompt = f"The user wants to: {action['input']}. Provide JSON with: filename, content, type"
                    # This would be handled in a more sophisticated flow
                    
                elif action["type"] == "send_email":
                    # Parse email details from input
                    pass
                
                elif action["type"] == "web_action":
                    if "youtube" in action["input"].lower() or "video" in action["input"].lower():
                        # Extract URL and summarize
                        url_match = re.search(r'https?://[^\s]+', action["input"])
                        if url_match:
                            url = url_match.group()
                            result = self.web_scraper.get_video_info(url)
                            results.append(result)
            
            except Exception as e:
                results.append({"status": "error", "message": str(e)})
        
        return results
    
    def _summarize_actions(self, results: list) -> str:
        """Summarize the execution results"""
        summary = []
        
        for result in results:
            if isinstance(result, dict):
                if result.get("status") == "success":
                    summary.append(f"✓ {result.get('message', 'Action completed')}")
                else:
                    summary.append(f"✗ {result.get('message', 'Action failed')}")
        
        return "; ".join(summary)
    
    def handle_app_launch(self, command: str) -> str:
        """Handle app launching requests"""
        apps = self._extract_apps(command)
        
        if not apps:
            return "I couldn't identify which app to open. Could you be more specific?"
        
        results = []
        for app in apps:
            result = self.app_launcher.launch_app(app)
            results.append(result)
        
        return "\n".join([r["message"] for r in results])
    
    def handle_file_generation(self, filename: str, content: str, file_type: str = "txt") -> str:
        """Handle file generation requests"""
        result = self.file_generator.generate_document(filename, content, file_type)
        return result["message"]
    
    def handle_email_sending(self, recipient: str, subject: str, body: str) -> str:
        """Handle email sending requests"""
        result = self.email_sender.send_email(recipient, subject, body)
        return result["message"]
    
    def handle_web_action(self, url: str) -> str:
        """Handle web scraping and video summarization"""
        if "youtube" in url.lower() or "youtu.be" in url.lower():
            result = self.web_scraper.get_video_info(url)
            if result["status"] == "success":
                return f"Video: {result['title']}\nDuration: {result['duration']}s\nUploader: {result['uploader']}"
            else:
                return result["message"]
        else:
            result = self.web_scraper.get_page_content(url)
            if result["status"] == "success":
                return f"Title: {result['title']}\n\nContent:\n{result['content']}"
            else:
                return result["message"]
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
