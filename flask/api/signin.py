from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import check_password_hash
from rococo.auth import  generate_access_token
import sys, os
from dotenv import load_dotenv
sys.path.append("..")
from common.models import ReferralCode
from middlewares.auth import auth_middleware
from common.repositories import (
    RepositoryFactory, LoginMethodRepository, PersonRepository, ReferralCodeRepository
)
from common.utils import generate_referral_code
from common.schemas import SigninParams

signin_bp = Blueprint('signin', __name__)
load_dotenv(dotenv_path='../.env.secrets')
env = os.environ

### SIGN-IN ROUTE
@signin_bp.route('', methods=['POST'])
def sign_in():
    try:
        data = request.get_json()
        signin_params = SigninParams(**data)
        login_method_repo = RepositoryFactory.get_repository(LoginMethodRepository)
        login_method = login_method_repo.find_by_email({'email.email': signin_params.email})
        if not login_method:
            return jsonify({'error': 'Email not found'}), 404
        if not login_method.email.is_verified:
            return jsonify({'error': 'Email not verified'}), 400
        person = login_method.person.entity_id
        access_token = generate_access_token(person, env['VERIFICATION_KEY'], 3600)
        password_verify = check_password_hash(login_method.password, signin_params.password)
        if not password_verify:
            return jsonify({'error': 'Invalid password'}), 401
        else:
            response = make_response(jsonify({'message': 'Login successful'}), 200)
            # Set the access_token in a cookie
            response.set_cookie(
                'access_token',
                value=access_token[0],
                httponly=True,
                secure=True,
                samesite='Strict',
                max_age=60 * 60
            )
            return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

### GENERATE REFERRAL CODE ROUTE
@signin_bp.route('/referral-code', methods=['POST'])
@auth_middleware
def generate_referal_code(entity_id):
    try:
        referral_repo = RepositoryFactory.get_repository(ReferralCodeRepository)
        person_repo = RepositoryFactory.get_repository(PersonRepository)
        person = person_repo.find_by_id(entity_id)
        if not person:
            return jsonify({'error': 'Invalid person_id'}), 404
        code = generate_referral_code()
        referral_code = ReferralCode(code=code, referrer_person_id=entity_id)
        referral_repo.save(referral_code)
        return jsonify({'Code': f'{code}'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
  