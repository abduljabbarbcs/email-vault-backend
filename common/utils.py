import random
import string
import hashlib
import re
import os
from dotenv import load_dotenv
from rococo.messaging import RabbitMqConnection

load_dotenv(dotenv_path='../.env.secrets')
env = os.environ

def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def mask_credit_card(card_number: str):
    return "**** **** **** " + card_number[-4:]

def hash_sensitive_info(info: str, salt: str):
    return hashlib.sha256((info + salt).encode('utf-8')).hexdigest()

def generate_referral_code(length=8):
    characters = string.ascii_uppercase + string.digits
    referral_code = ''.join(random.choices(characters, k=length))
    return referral_code

def validate_password(password: str):
    pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$')
    if pattern.match(password):
        return True
    return False

# Send verification email via RabbitMQ -> Email Transmitter
def send_email(verify_link: str, event: str, email: str):
    email_transmitter_queue_name = os.getenv('QUEUE_NAME_PREFIX') + os.getenv('EmailServiceProcessor_QUEUE_NAME')
    with RabbitMqConnection(env['RABBITMQ_HOST'], env['RABBITMQ_PORT'], env['RABBITMQ_USER'], env['RABBITMQ_PASSWORD'], env['RABBITMQ_VIRTUAL_HOST']) as conn:
        return conn.send_message(email_transmitter_queue_name, {
                    'event': event,
                    'data': {
                        'verify_link': verify_link
                    },
                    'to_emails': [email]
                })