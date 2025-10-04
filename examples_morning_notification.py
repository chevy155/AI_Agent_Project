#!/usr/bin/env python3
"""
Example demonstrating how to use the morning notification agent.

This script shows different ways to use the morning notification feature:
1. Basic usage with default settings
2. Custom recipients
3. Email-only or SMS-only modes
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from agents.morning_notification import (
    generate_morning_intention,
    send_email,
    send_sms,
    send_morning_notification
)


def example_1_basic_usage():
    """Example 1: Basic usage with default settings from .env"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Usage (Default Recipients from .env)")
    print("="*60)
    
    result = send_morning_notification()
    print(f"\nResult: {result}")


def example_2_custom_recipients():
    """Example 2: Override recipients programmatically"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Custom Recipients")
    print("="*60)
    
    result = send_morning_notification(
        recipient_email="custom@example.com",
        recipient_phone="+11234567890"
    )
    print(f"\nResult: {result}")


def example_3_generate_only():
    """Example 3: Just generate intention without sending"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Generate Intention Only")
    print("="*60)
    
    intention = generate_morning_intention()
    print(f"\nGenerated Intention:\n{intention}")


def example_4_email_only():
    """Example 4: Send email only (disable SMS in config.yaml)"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Email Only")
    print("="*60)
    print("Set enable_sms: False in config.yaml, then run:")
    print("result = send_morning_notification()")
    print("\nThis will skip SMS and only send email.")


def example_5_programmatic_send():
    """Example 5: Generate once, send to multiple recipients"""
    print("\n" + "="*60)
    print("EXAMPLE 5: One Intention, Multiple Recipients")
    print("="*60)
    
    # Generate intention once
    intention = generate_morning_intention()
    print(f"\nGenerated Intention:\n{intention}\n")
    
    # Send to multiple email addresses
    print("Sending to multiple recipients...")
    send_email(intention, "recipient1@example.com")
    send_email(intention, "recipient2@example.com")
    
    # Send to multiple phone numbers
    send_sms(intention, "+11234567890")
    send_sms(intention, "+10987654321")


if __name__ == '__main__':
    print("\n" + "="*60)
    print("MORNING NOTIFICATION - USAGE EXAMPLES")
    print("="*60)
    print("\nThese examples show how to use the morning notification feature.")
    print("NOTE: You need to configure .env file for these to work!")
    print("\nAvailable examples:")
    print("  1. Basic usage with default settings")
    print("  2. Custom recipients")
    print("  3. Generate intention only")
    print("  4. Email only mode")
    print("  5. One intention to multiple recipients")
    
    # Uncomment the example you want to run:
    # example_1_basic_usage()
    # example_2_custom_recipients()
    # example_3_generate_only()
    # example_4_email_only()
    # example_5_programmatic_send()
    
    print("\n" + "="*60)
    print("Uncomment an example function call to run it!")
    print("="*60)
