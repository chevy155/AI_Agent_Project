# Morning Notification Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                  MORNING NOTIFICATION SYSTEM                    │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│   Trigger        │  Manual: python send_morning_notification.py
│   (User/Cron)    │  Scheduled: Daily at 7:00 AM via cron/scheduler
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────────┐
│  STEP 1: Generate Morning Intention                              │
│  ────────────────────────────────────────────────────────────   │
│  • Load config.yaml settings                                     │
│  • Connect to Ollama LLM (llama3.1:8b)                          │
│  • Send prompt: "Generate uplifting morning intention..."       │
│  • Receive unique, positive message (2-4 sentences)             │
└────────┬─────────────────────────────────────────────────────────┘
         │
         ▼
    ┌────────────────────────┐
    │  Generated Intention:  │
    │  "Today is filled with │
    │   new opportunities..." │
    └────────┬───────────────┘
             │
        ┌────┴────┐
        │         │
        ▼         ▼
┌──────────────────┐  ┌──────────────────┐
│  STEP 2A: Email  │  │  STEP 2B: SMS    │
│  ────────────── │  │  ──────────────  │
│  Service: Gmail  │  │  Service: Twilio │
│  SMTP            │  │  SMS API         │
│                  │  │                  │
│  • Load .env     │  │  • Load .env     │
│  • Connect SMTP  │  │  • Init Twilio   │
│  • Format email  │  │  • Format SMS    │
│  • Send message  │  │  • Send message  │
└────────┬─────────┘  └────────┬─────────┘
         │                     │
         ▼                     ▼
┌──────────────────┐  ┌──────────────────┐
│   📧 Email       │  │   📱 SMS         │
│   marcocarrillo  │  │   (415) 613-2143│
│   15532@gmail.com│  │                  │
└──────────────────┘  └──────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  RESULT: Success confirmation with status for each channel       │
│  ✓ Email sent | ✓ SMS sent | ✗ Failed/Disabled                │
└─────────────────────────────────────────────────────────────────┘


KEY COMPONENTS:
═══════════════

📁 agents/morning_notification.py
   ├─ generate_morning_intention()  - LLM-powered intention generator
   ├─ send_email()                  - Gmail SMTP email sender
   ├─ send_sms()                    - Twilio SMS sender
   └─ send_morning_notification()   - Main orchestrator function

📁 send_morning_notification.py
   └─ Simple CLI script to trigger notifications

📁 config.yaml
   └─ agents.morning_notification settings

📁 .env (user creates from .env.example)
   ├─ EMAIL_ADDRESS, EMAIL_PASSWORD
   ├─ RECIPIENT_EMAIL
   ├─ TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
   ├─ TWILIO_PHONE_NUMBER
   └─ RECIPIENT_PHONE

📁 tests/test_morning_notification.py
   └─ Unit tests with mocked external services
```
