# AI Agent Project

A multi-agent system for finance analysis and personal productivity features.

## Features

### 📊 Finance Analysis Pipeline
- **Agent 1 (Data Loader)**: Loads and prepares NVIDIA stock data
- **Agent 2 (Indicator Calculator)**: Calculates technical indicators (SMA, RSI)
- **Agent 3 (Pattern Identifier)**: Analyzes patterns using LLM and generates reports

### 🌅 Morning Notification System (NEW!)
Send daily morning intentions/manifestations via email and SMS.

- **LLM-powered intention generation** using Ollama
- **Email notifications** via Gmail
- **SMS notifications** via Twilio
- **Scheduled or manual execution**

**Quick Start**: See [MORNING_NOTIFICATION_README.md](MORNING_NOTIFICATION_README.md) for setup instructions.

## Project Structure

```
AI_Agent_Project/
├── agents/
│   ├── data_loader.py              # Finance data loading
│   ├── indicator_calculator.py     # Technical indicators
│   ├── pattern_identifier.py       # LLM pattern analysis
│   └── morning_notification.py     # NEW: Morning notifications
├── tests/
│   └── test_*.py                   # Unit tests
├── main.py                         # Finance pipeline entry point
├── send_morning_notification.py   # NEW: Notification script
├── config.yaml                     # Configuration settings
└── requirements.txt                # Python dependencies
```

## Installation

```bash
# Clone the repository
git clone https://github.com/chevy155/AI_Agent_Project.git
cd AI_Agent_Project

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Finance Analysis Pipeline

```bash
python main.py
```

### Morning Notifications

1. Set up credentials (see [MORNING_NOTIFICATION_README.md](MORNING_NOTIFICATION_README.md))
2. Run manually:
   ```bash
   python send_morning_notification.py
   ```
3. Or schedule daily execution via cron/Task Scheduler

## Configuration

Edit `config.yaml` to customize:
- Data paths
- LLM model settings
- Agent-specific parameters
- Morning notification preferences

## Documentation

- **[MORNING_NOTIFICATION_README.md](MORNING_NOTIFICATION_README.md)** - Complete setup guide for notifications
- **[WORKFLOW_DIAGRAM.md](WORKFLOW_DIAGRAM.md)** - Visual architecture diagram
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Technical implementation details

## Requirements

- Python 3.8+
- Ollama (for LLM features)
- Gmail account (for email notifications)
- Twilio account (for SMS notifications)

## Testing

```bash
# Run all tests
python -m unittest discover tests

# Run specific test
python -m unittest tests.test_morning_notification
```

## Security

- Never commit `.env` files
- Use environment variables for credentials
- Use Gmail App Passwords (not regular passwords)
- Keep API credentials secure

## License

See LICENSE file for details.

## Contributing

Contributions welcome! Please ensure:
- Code follows existing patterns
- Tests pass
- Documentation is updated
- Security best practices are followed
