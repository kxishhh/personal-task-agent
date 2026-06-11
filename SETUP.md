# Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- API keys for services

## Step 1: Clone the Repository

```bash
git clone https://github.com/kxishhh/personal-task-agent.git
cd personal-task-agent
```

## Step 2: Create Virtual Environment (Recommended)

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Get API Keys

### Claude API Key
1. Go to https://console.anthropic.com
2. Sign up or log in
3. Create an API key
4. Copy the key

### Email Configuration
For Gmail:
1. Go to https://myaccount.google.com/apppasswords
2. Generate an app password
3. Use your Gmail address and the generated app password

For other email providers:
- Use your email address and password (or app password if 2FA is enabled)

### YouTube API Key (Optional)
1. Go to https://console.cloud.google.com
2. Create a new project
3. Enable YouTube Data API v3
4. Create credentials (API key)
5. Copy the key

## Step 5: Configure Environment

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your keys:
   ```
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
   SMTP_EMAIL=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   YOUTUBE_API_KEY=AIzaSyD-xxxxxxxxxxxxx
   DEBUG=false
   ```

## Step 6: Run the Agent

```bash
python main.py
```

You should see the welcome message and be ready to issue commands!

## Troubleshooting

### API Key Issues
- **"ANTHROPIC_API_KEY not set"**: Make sure `.env` file exists and has the correct key
- **"Authentication failed"**: Check that your API key is valid and has access

### Email Issues
- **"Failed to send email"**: 
  - Verify SMTP credentials
  - For Gmail, use an app password, not your regular password
  - Enable "Less secure app access" if needed

### Application Launching Issues
- **"Failed to launch app"**: 
  - Make sure the app is installed
  - Use the correct app name
  - Check that it's in the system PATH

## Testing

Try these commands to test each feature:

```
# Test app launcher
Open Chrome

# Test file generation
Generate a Python script that prints Hello World

# Test email
Send an email to test@example.com with subject Test and body This is a test

# Test web scraping
Show me information about Python programming

# Complex task
Open Chrome and search for latest news about AI
```

## Next Steps

- Customize the system prompt in `agent.py` to match your needs
- Add more tools in the `tools/` directory
- Create custom workflows for repetitive tasks
- Integrate with additional APIs and services

## Security Notes

- Never commit `.env` file to version control
- Keep your API keys private
- Use app-specific passwords for email when possible
- Regularly rotate your API keys
