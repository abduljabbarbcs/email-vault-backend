from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from rococo.auth import  generate_confirmation_token, validate_confirmation_token
import sys, os
from dotenv import load_dotenv
sys.path.append("..")
from common.repositories import RepositoryFactory, LoginMethodRepository, EmailRepository
from common.schemas import SigninParams
from common.utils import send_email

reset_bp = Blueprint('reset', __name__)

load_dotenv(dotenv_path='../.env.secrets')
env = os.environ
TOKEN_EXPIRY = 60*15

### CHECK MAIL ROUTE ###
@reset_bp.route('/check-email', methods=['POST'])
def check_email():
    try:
        data = request.get_json()
        email = data.get('email')
        email_repo = RepositoryFactory.get_repository(EmailRepository)
        # check if email exists
        emailM = email_repo.find_by_email(email)
        if not emailM:
            return jsonify({'error': 'Email not found'}), 404
        if not emailM.is_verified:
            return jsonify({'message': 'Email is not verified'}), 400
        
        reset_token = generate_confirmation_token(email, env['VERIFICATION_KEY'])
        # Send password reset email via RabbitMQ -> Email Transmitter
        reset_link = f"{env['DOMAIN']}/reset-password?token={reset_token}"
        send_email(reset_link, 'PASSWORD_RESET' , email)
        return jsonify({'message': 'Password reset email sent successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

### VERIFY EMAIL FOR PASSWORD_RESET ROUTE
@reset_bp.route('/verify-password-email/<token>', methods=['GET'])
def verify_email_password(token):
    email = validate_confirmation_token(token, env['VERIFICATION_KEY'], TOKEN_EXPIRY)
    if not email:
        return jsonify({'error': 'Invalid Token'}), 400
    
    return jsonify({'message': 'Email verified successfully'}), 200

### RESET PASSWORD ROUTE ###
@reset_bp.route('/change-password', methods=['POST'])
def verify_email_pass():
    data = request.get_json()
    reset_params = SigninParams(**data)
    login_method_repo = RepositoryFactory.get_repository(LoginMethodRepository)
    # get login method and email from db
    login_method = login_method_repo.find_by_email({'email.email': reset_params.email})
    if not login_method.email.is_verified:
        return jsonify({'error': 'Email not verified'}), 400
    password_hash = generate_password_hash(reset_params.password)
    # save new password
    login_method.password = password_hash
    login_method_repo.save(login_method)
    return jsonify({'message': 'Password changed successfully'}), 200
