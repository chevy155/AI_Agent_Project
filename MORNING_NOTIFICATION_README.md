# Morning Notification Feature

This feature sends daily morning intentions/manifestations via email and SMS.

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Edit the `.env` file with your actual credentials:

#### Email Configuration (Gmail)
- `EMAIL_ADDRESS`: Your Gmail address
- `EMAIL_PASSWORD`: Your Gmail App Password (not your regular password)
  - To create an App Password: https://support.google.com/accounts/answer/185833
- `RECIPIENT_EMAIL`: Email address to receive notifications (default: marcocarrillo15532@gmail.com)

#### SMS Configuration (Twilio)
- `TWILIO_ACCOUNT_SID`: Your Twilio Account SID
- `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token
- `TWILIO_PHONE_NUMBER`: Your Twilio phone number (format: +1234567890)
- `RECIPIENT_PHONE`: Phone number to receive SMS (default: +14156132143)

To get Twilio credentials:
1. Sign up at https://www.twilio.com/try-twilio
2. Get your Account SID and Auth Token from the console
3. Get a Twilio phone number

### 3. Configure Settings (Optional)

Edit `config.yaml` to customize the agent settings:

```yaml
agents:
  morning_notification:
    llm_model_id: "llama3.1:8b"  # LLM model to use for generating intentions
    llm_max_tokens: 512           # Max tokens for generation
    enable_email: True            # Enable/disable email notifications
    enable_sms: True              # Enable/disable SMS notifications
```

### 4. Ensure Ollama is Running

The intention generation uses a local LLM via Ollama. Make sure Ollama is running:

```bash
ollama serve
```

And ensure the model is available:

```bash
ollama pull llama3.1:8b
```

## Usage

### Send Morning Notification Manually

Run the script to send a morning intention right now:

```bash
python send_morning_notification.py
```

Or:

```bash
python -m agents.morning_notification
```

### Schedule Daily Notifications

#### On Linux/Mac (using cron)

1. Edit your crontab:
```bash
crontab -e
```

2. Add this line to run at 7:00 AM daily:
```
0 7 * * * cd /path/to/AI_Agent_Project && /path/to/python send_morning_notification.py >> /tmp/morning_notification.log 2>&1
```

#### On Windows (using Task Scheduler)

1. Open Task Scheduler
2. Create a new task
3. Set trigger to daily at 7:00 AM
4. Set action to run: `python C:\path\to\AI_Agent_Project\send_morning_notification.py`

## How It Works

1. **Generate Intention**: Uses LangChain with Ollama to generate a unique, positive morning intention
2. **Send Email**: Sends the intention via Gmail SMTP
3. **Send SMS**: Sends the intention via Twilio SMS API

## Troubleshooting

### Email Not Sending
- Ensure you're using a Gmail App Password, not your regular password
- Enable "Less secure app access" if using older Gmail accounts
- Check that your Gmail account allows SMTP access

### SMS Not Sending
- Verify your Twilio credentials are correct
- Ensure your Twilio account is active and has credits
- Check that the phone number format is correct (+1234567890)
- For trial accounts, verify the recipient number in Twilio console

### LLM Not Working
- Ensure Ollama is running: `ollama serve`
- Check that the model is installed: `ollama list`
- Pull the model if needed: `ollama pull llama3.1:8b`

## Customization

You can customize the intention prompt by editing the `generate_morning_intention()` function in `agents/morning_notification.py`.

## Security Notes

- Never commit your `.env` file to version control
- The `.env` file is already in `.gitignore`
- Keep your API credentials secure
- Use environment variables for all sensitive data
