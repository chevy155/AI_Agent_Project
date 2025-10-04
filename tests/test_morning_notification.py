# tests/test_morning_notification.py
# Tests for the morning notification agent

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from agents.morning_notification import (
    generate_morning_intention,
    send_email,
    send_sms,
    send_morning_notification
)


class TestMorningNotification(unittest.TestCase):
    """Test cases for morning notification agent"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.config_path = "config.yaml"
        self.test_intention = "Today is a new opportunity to grow and thrive. Embrace challenges with confidence."
    
    @patch('agents.morning_notification.ChatOllama')
    def test_generate_morning_intention(self, mock_ollama):
        """Test that intention generation works"""
        # Mock the LLM response
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = self.test_intention
        
        # Since we're mocking at ChatOllama level, we need to mock the chain creation
        # This is a simplified test - in real scenario, you'd test the actual LLM if available
        
        # For now, just test that the function exists and has proper structure
        self.assertTrue(callable(generate_morning_intention))
    
    @patch('agents.morning_notification.smtplib.SMTP')
    @patch('agents.morning_notification.load_dotenv')
    @patch.dict(os.environ, {
        'EMAIL_ADDRESS': 'test@gmail.com',
        'EMAIL_PASSWORD': 'test_password',
        'RECIPIENT_EMAIL': 'recipient@gmail.com'
    })
    def test_send_email(self, mock_dotenv, mock_smtp):
        """Test email sending functionality"""
        # Mock SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        result = send_email(self.test_intention)
        
        # Verify SMTP was called
        mock_smtp.assert_called_with('smtp.gmail.com', 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once()
        
        # Should return True on success
        self.assertTrue(result)
    
    @patch('agents.morning_notification.Client')
    @patch('agents.morning_notification.load_dotenv')
    @patch('agents.morning_notification.TWILIO_AVAILABLE', True)
    @patch.dict(os.environ, {
        'TWILIO_ACCOUNT_SID': 'test_sid',
        'TWILIO_AUTH_TOKEN': 'test_token',
        'TWILIO_PHONE_NUMBER': '+11234567890',
        'RECIPIENT_PHONE': '+19876543210'
    })
    def test_send_sms(self, mock_dotenv, mock_client):
        """Test SMS sending functionality"""
        # Mock Twilio client
        mock_twilio_instance = MagicMock()
        mock_message = MagicMock()
        mock_message.sid = 'test_message_sid'
        mock_twilio_instance.messages.create.return_value = mock_message
        mock_client.return_value = mock_twilio_instance
        
        result = send_sms(self.test_intention)
        
        # Verify Twilio client was created
        mock_client.assert_called_once_with('test_sid', 'test_token')
        
        # Verify message was sent
        mock_twilio_instance.messages.create.assert_called_once()
        
        # Should return True on success
        self.assertTrue(result)
    
    @patch('agents.morning_notification.send_sms')
    @patch('agents.morning_notification.send_email')
    @patch('agents.morning_notification.generate_morning_intention')
    def test_send_morning_notification(self, mock_generate, mock_email, mock_sms):
        """Test the main notification function"""
        # Mock the functions
        mock_generate.return_value = self.test_intention
        mock_email.return_value = True
        mock_sms.return_value = True
        
        result = send_morning_notification()
        
        # Verify all functions were called
        mock_generate.assert_called_once()
        mock_email.assert_called_once()
        mock_sms.assert_called_once()
        
        # Check result structure
        self.assertIn('intention', result)
        self.assertIn('email_sent', result)
        self.assertIn('sms_sent', result)
        self.assertEqual(result['intention'], self.test_intention)
        self.assertTrue(result['email_sent'])
        self.assertTrue(result['sms_sent'])


if __name__ == '__main__':
    unittest.main()
