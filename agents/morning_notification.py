# agents/morning_notification.py
# Agent for sending morning intentions/manifestations via email and SMS

import os
import yaml
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

try:
    from langchain_ollama import ChatOllama
    from langchain_core.prompts import PromptTemplate
    from langchain_core.output_parsers import StrOutputParser
except ImportError:
    print("ERROR: Required LangChain components not found.")
    exit()

try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except ImportError:
    print("WARNING: Twilio not installed. SMS functionality will be disabled.")
    TWILIO_AVAILABLE = False


def generate_morning_intention(config_path: str = "config.yaml") -> str:
    """
    Generate a morning intention/manifestation using LLM.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Generated intention text or error message
    """
    print("--- Generating Morning Intention ---")
    try:
        # Load configuration
        if not os.path.exists(config_path):
            return "ERROR: Config file not found"
            
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        agent_config = config.get('agents', {}).get('morning_notification', {})
        llm_model_id = agent_config.get('llm_model_id', 'llama3.1:8b')
        max_tokens = agent_config.get('llm_max_tokens', 512)
        
        # Define prompt template
        prompt_template_str = """
        You are a mindfulness and motivation coach. Generate a short, positive, and uplifting 
        morning intention or manifestation statement. The message should be:
        
        - Between 2-4 sentences
        - Inspiring and empowering
        - Focused on gratitude, positivity, or personal growth
        - Appropriate for starting the day with a positive mindset
        - NOT overly long or preachy
        
        Generate a unique morning intention:
        """
        
        prompt = PromptTemplate(
            input_variables=[],
            template=prompt_template_str,
        )
        
        # Initialize LLM
        print(f"Initializing LLM with model: {llm_model_id}")
        llm = ChatOllama(model=llm_model_id)
        
        # Create and run chain
        chain = prompt | llm | StrOutputParser()
        
        print("Generating intention with LLM...")
        intention = chain.invoke({})
        
        print("Intention generated successfully.")
        return intention.strip()
        
    except Exception as e:
        print(f"Error generating intention: {e}")
        return f"ERROR: {e}"


def send_email(intention: str, recipient_email: str = None) -> bool:
    """
    Send morning intention via email.
    
    Args:
        intention: The intention text to send
        recipient_email: Email address to send to (optional, reads from .env if not provided)
        
    Returns:
        True if successful, False otherwise
    """
    print("--- Sending Email ---")
    try:
        # Load environment variables
        load_dotenv()
        
        sender_email = os.getenv('EMAIL_ADDRESS')
        sender_password = os.getenv('EMAIL_PASSWORD')
        recipient = recipient_email or os.getenv('RECIPIENT_EMAIL')
        
        if not all([sender_email, sender_password, recipient]):
            print("ERROR: Email credentials not configured properly in .env file")
            return False
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient
        msg['Subject'] = "🌅 Your Morning Intention"
        
        # Email body
        body = f"""
Good Morning! 🌞

Here is your intention for today:

{intention}

Have a wonderful day filled with positivity and purpose!

---
This is an automated morning intention message.
"""
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email via Gmail SMTP
        print(f"Connecting to Gmail SMTP server...")
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        print(f"Email sent successfully to {recipient}")
        return True
        
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_sms(intention: str, recipient_phone: str = None) -> bool:
    """
    Send morning intention via SMS using Twilio.
    
    Args:
        intention: The intention text to send
        recipient_phone: Phone number to send to (optional, reads from .env if not provided)
        
    Returns:
        True if successful, False otherwise
    """
    print("--- Sending SMS ---")
    
    if not TWILIO_AVAILABLE:
        print("ERROR: Twilio library not available. Cannot send SMS.")
        return False
    
    try:
        # Load environment variables
        load_dotenv()
        
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        twilio_phone = os.getenv('TWILIO_PHONE_NUMBER')
        recipient = recipient_phone or os.getenv('RECIPIENT_PHONE')
        
        if not all([account_sid, auth_token, twilio_phone, recipient]):
            print("ERROR: Twilio credentials not configured properly in .env file")
            return False
        
        # Create Twilio client
        client = Client(account_sid, auth_token)
        
        # Create message body
        sms_body = f"🌅 Morning Intention:\n\n{intention}\n\nHave a great day!"
        
        # Send SMS
        message = client.messages.create(
            body=sms_body,
            from_=twilio_phone,
            to=recipient
        )
        
        print(f"SMS sent successfully to {recipient}. Message SID: {message.sid}")
        return True
        
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return False


def send_morning_notification(config_path: str = "config.yaml", 
                              recipient_email: str = None,
                              recipient_phone: str = None) -> dict:
    """
    Main function to generate and send morning intention via email and SMS.
    
    Args:
        config_path: Path to configuration file
        recipient_email: Optional email override
        recipient_phone: Optional phone number override
        
    Returns:
        Dictionary with status of email and SMS sending
    """
    print("="*50)
    print("Starting Morning Notification Agent")
    print("="*50)
    
    # Load configuration
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        agent_config = config.get('agents', {}).get('morning_notification', {})
        enable_email = agent_config.get('enable_email', True)
        enable_sms = agent_config.get('enable_sms', True)
    except Exception as e:
        print(f"Error loading config: {e}")
        return {'error': str(e)}
    
    # Generate intention
    intention = generate_morning_intention(config_path)
    
    if intention.startswith("ERROR:"):
        print(f"Failed to generate intention: {intention}")
        return {'error': intention}
    
    print("\n--- Generated Intention ---")
    print(intention)
    print("---" * 10)
    
    # Send notifications
    results = {
        'intention': intention,
        'email_sent': False,
        'sms_sent': False
    }
    
    if enable_email:
        results['email_sent'] = send_email(intention, recipient_email)
    else:
        print("Email notifications disabled in config")
    
    if enable_sms:
        results['sms_sent'] = send_sms(intention, recipient_phone)
    else:
        print("SMS notifications disabled in config")
    
    print("\n" + "="*50)
    print("Morning Notification Agent Complete")
    print(f"Email: {'✓ Sent' if results['email_sent'] else '✗ Failed/Disabled'}")
    print(f"SMS: {'✓ Sent' if results['sms_sent'] else '✗ Failed/Disabled'}")
    print("="*50)
    
    return results


# Test block for running this script directly
if __name__ == '__main__':
    result = send_morning_notification()
    print("\nFinal Result:", result)
