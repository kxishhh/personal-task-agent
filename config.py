import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")

# Email Configuration
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Agent Configuration
AGENT_NAME = os.getenv("AGENT_NAME", "PersonalAssistant")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# System paths
HOME_DIR = os.path.expanduser("~")
DOCUMENTS_DIR = os.path.join(HOME_DIR, "Documents")

# Validate required keys
def validate_config():
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set in .env file")
    if not SMTP_EMAIL or not SMTP_PASSWORD:
        raise ValueError("SMTP_EMAIL and SMTP_PASSWORD not set in .env file")
    return True
