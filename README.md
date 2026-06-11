# Personal Task Automation Agent

A comprehensive AI-powered desktop agent that handles everyday tasks through natural language commands.

## Features

- 🗣️ **Voice & Text Commands** - Control via voice or text input
- 📱 **App Launcher** - Open any application on your system
- 📝 **Content Generation** - Generate documents, code, emails, etc.
- 📧 **Email Management** - Send emails automatically
- 🌐 **Web Browsing** - Summarize videos and extract information
- ⚙️ **Task Automation** - Execute complex multi-step workflows
- 🤖 **AI-Powered** - Uses Claude AI for intelligent task understanding

## Installation

```bash
git clone https://github.com/kxishhh/personal-task-agent.git
cd personal-task-agent
pip install -r requirements.txt
```

## Configuration

1. Copy `.env.example` to `.env`
2. Add your API keys:
   - `ANTHROPIC_API_KEY` - Claude API key from https://console.anthropic.com
   - `SMTP_EMAIL` - Your email address
   - `SMTP_PASSWORD` - Your email password or app password
   - `YOUTUBE_API_KEY` - YouTube API key (optional, for video summaries)

## Usage

```bash
python main.py
```

Then speak or type your commands:
- "Open Chrome"
- "Generate a Python script for web scraping"
- "Send an email to john@example.com with subject 'Meeting Notes' and body 'Here are the notes from today'"
- "Open YouTube and summarize this video: https://youtube.com/watch?v=xxx"
- "Create a report document with sales data"

## Architecture

- **main.py** - Main agent orchestrator and command loop
- **tools/app_launcher.py** - Opens applications on your system
- **tools/file_generator.py** - Generates documents, code, and content
- **tools/email_sender.py** - Sends emails with attachments
- **tools/web_scraper.py** - Summarizes videos and web content
- **agent.py** - Core AI agent logic using Claude
- **config.py** - Configuration management

## Supported Commands

### App Launcher
- "Open Chrome"
- "Launch Spotify"
- "Start Discord"

### File Generation
- "Generate a Python script that does X"
- "Write me a professional email template"
- "Create a report document"

### Email
- "Send an email to user@example.com with subject 'Hello' and message 'Hi there'"
- "Mail the report to the team"

### Web/Video
- "Summarize this YouTube video: [URL]"
- "Get me information about [topic] from the web"

## License

MIT
