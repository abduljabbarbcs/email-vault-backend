from flask import Blueprint, request, jsonify
from rococo.models import OtpMethod
import sys, os
from dotenv import load_dotenv
sys.path.append("..")
from common.repositories import RepositoryFactory, OTPMethodRepository, EmailRepository
from common.utils import generate_otp, send_email

signup_bp = Blueprint('signup', __name__)
load_dotenv(dotenv_path='../.env.secrets')
env = os.environ
### TODO
### OTP GENERATION AND VERIFICATION ###
@signup_bp.route('/otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    email = data.get('email')

    email_repo = RepositoryFactory.get_repository(EmailRepository)
    emailM = email_repo.find_by_email(email)
    if not emailM:
        return jsonify({'error': 'Email not found'}), 404

    # Generate OTP
    otp_code = generate_otp()
    otp_method_repo = RepositoryFactory.get_repository(OTPMethodRepository)
    otp = OtpMethod(person=emailM.person, secret=otp_code, name='Login OTP', enabled=True)
    otp_method_repo.save(otp)

    # Send OTP via RabbitMQ -> Email Transmitter
    send_email(otp_code, 'USER_SIGNUP' , email)
    return jsonify({'message': 'OTP sent successfully.'}), 200

@signup_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data['email']
    otp_code = data['otp']

    otp_method_repo = RepositoryFactory.get_repository(OTPMethodRepository)
    otp = otp_method_repo.find_by_secret(otp_code)

    if otp and otp.enabled:
        return jsonify({'message': 'OTP verified successfully'}), 200
    return jsonify({'error': 'Invalid OTP or expired'}), 400

  
