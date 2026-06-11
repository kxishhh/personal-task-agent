#!/usr/bin/env python3

import sys
import os
from agent import PersonalAgent
from config import validate_config, DEBUG

def print_welcome():
    """Print welcome message"""
    print("\n" + "="*60)
    print("🤖 Personal Task Automation Agent")
    print("="*60)
    print("\nHello! I'm your personal assistant. I can help you with:")
    print("  📱 Opening applications")
    print("  📝 Generating documents and code")
    print("  📧 Sending emails")
    print("  🌐 Summarizing videos and web content")
    print("  ⚙️  Automating complex tasks")
    print("\nTry commands like:")
    print("  - 'Open Chrome'")
    print("  - 'Generate a Python script that does X'")
    print("  - 'Send an email to john@example.com with subject Hello'")
    print("  - 'Summarize the YouTube video at [URL]'")
    print("\nType 'exit' or 'quit' to close the agent.")
    print("Type 'clear' to clear conversation history.")
    print("="*60 + "\n")

def main():
    """Main entry point"""
    try:
        # Validate configuration
        validate_config()
        
        # Initialize agent
        agent = PersonalAgent()
        
        if DEBUG:
            print("[DEBUG MODE ENABLED]")
        
        print_welcome()
        
        # Main conversation loop
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() in ["exit", "quit"]:
                    print("\n👋 Goodbye! Thanks for using Personal Task Agent.")
                    break
                
                if user_input.lower() == "clear":
                    agent.clear_history()
                    print("✓ Conversation history cleared.")
                    continue
                
                # Process command
                response = agent.process_command(user_input)
                print(f"\nAssistant: {response}\n")
            
            except KeyboardInterrupt:
                print("\n\n👋 Agent interrupted. Goodbye!")
                break
            
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                if DEBUG:
                    import traceback
                    traceback.print_exc()
                print()

if __name__ == "__main__":
    main()
