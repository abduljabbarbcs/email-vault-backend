from flask import Blueprint, request, jsonify
from rococo.auth import  generate_confirmation_token
import sys, os
from dotenv import load_dotenv
sys.path.append("..")
from common.repositories import RepositoryFactory, EmailRepository
from common.schemas import ResendEmailParams
from common.utils import send_email

resend_bp = Blueprint('resend', __name__)

load_dotenv(dotenv_path='../.env.secrets')
env = os.environ


@resend_bp.route('', methods=['POST'])
def resend_email():
    try:
        events = {'password': 'RESET_PASSWORD', 'signup': 'USER_SIGNUP'}
        links = {'password': 'reset-password', 'signup': 'verify-email'}
        data = request.get_json()
        resend_params = ResendEmailParams(**data)
        email_repo = RepositoryFactory.get_repository(EmailRepository)
        # check if email exists
        emailM = email_repo.find_by_email(resend_params.email)
        if not emailM:
            return jsonify({'error': 'Email not found'}), 404
        if resend_params.event !='signup' and not emailM.is_verified:
            return jsonify({'message': 'Email is not verified'}), 400
        reset_token = generate_confirmation_token(resend_params.email, env['VERIFICATION_KEY'])
        verify_link = f"{env['DOMAIN']}/{links.get(resend_params.event)}?token={reset_token}"
        send_email(verify_link, events.get(resend_params.event) , resend_params.email)
        return jsonify({'message': 'Email re-sent successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500