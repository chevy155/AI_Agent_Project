#!/usr/bin/env python3
# send_morning_notification.py - Script to send morning intention/manifestation

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from agents.morning_notification import send_morning_notification

if __name__ == '__main__':
    print("Morning Notification Script")
    print("This will send a morning intention to the configured email and phone number.")
    print()
    
    # You can optionally override recipients here
    # result = send_morning_notification(
    #     recipient_email="custom@email.com",
    #     recipient_phone="+1234567890"
    # )
    
    result = send_morning_notification()
    
    if 'error' in result:
        print(f"\nERROR: {result['error']}")
        sys.exit(1)
    else:
        print("\nNotification sent successfully!")
        sys.exit(0)
