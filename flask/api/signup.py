from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from rococo.auth import  generate_confirmation_token, validate_confirmation_token
from rococo.models import Person,Organization, LoginMethod, Email
import sys, os, re
from dotenv import load_dotenv
sys.path.append("..")
from common.models import PaymentInfo
from common.schemas import SignupParams
from common.repositories import (
    RepositoryFactory, LoginMethodRepository, PersonRepository, OrganizationRepository,
    ReferralCodeRepository, PaymentInfoRepository, EmailRepository
)
from common.utils import mask_credit_card, hash_sensitive_info, send_email

signup_bp = Blueprint('signup', __name__)
load_dotenv(dotenv_path='../.env.secrets')
env = os.environ
TOKEN_EXPIRY = 60*15

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str):
    pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$')
    if pattern.match(password):
        return True
    return False

def check_referral_code(referral_code, person):
    referral_code_repo = RepositoryFactory.get_repository(ReferralCodeRepository)
    code = referral_code_repo.find_by_code(referral_code)
    if code and not code.referred_person_id:
        code.referred_person_id = person
        return code
    else:
        return False

@signup_bp.route('', methods=['POST'])
def sign_up():
    data = request.get_json()
    signup_params = SignupParams(**data)
    valid_email = is_valid_email(signup_params.email)
    if not valid_email:
        return jsonify({'error': 'Invalid email'}), 400
    valid_password = validate_password(signup_params.password)
    if not valid_password:
        return jsonify({'error': 'Invalid password'}), 400
    if not signup_params.first_name or not signup_params.last_name or not signup_params.email or not signup_params.password or not signup_params.company_name or \
    not signup_params.card_number or not signup_params.expiry_date or not signup_params.card_holder_name or not signup_params.cvv:
        return jsonify({'error': 'All fields including payment info are required'}), 400

    try:
        # Use the RepositoryFactory to initialize repositories
        login_method_repo = RepositoryFactory.get_repository(LoginMethodRepository)
        person_repo = RepositoryFactory.get_repository(PersonRepository)
        referral_code_repo = RepositoryFactory.get_repository(ReferralCodeRepository)
        organization_repo = RepositoryFactory.get_repository(OrganizationRepository)
        payment_info_repo = RepositoryFactory.get_repository(PaymentInfoRepository)
        email_repo = RepositoryFactory.get_repository(EmailRepository)

        # Hash password
        password_hash = generate_password_hash(signup_params.password)
        # Check if email already exists
        existing_email = email_repo.find_by_email(signup_params.email)
        if existing_email:
            return jsonify({'error': 'Email already exists'}), 400

        person = Person(first_name=signup_params.first_name, last_name=signup_params.last_name)
        # Process referral code
        if signup_params.referral_code:
            referral_code = check_referral_code(signup_params.referral_code, person)
            if not referral_code:
                return jsonify({'error': 'Invalid or used referral code'}), 400
            person_repo.save(person)
            referral_code_repo.save(referral_code)
        else: person_repo.save(person)
        emailM = Email(email=signup_params.email, person=person)
        email_repo.save(emailM)
        login_method = LoginMethod(email = emailM, password=password_hash, person=person.entity_id, method_type='email-password')
        login_method_repo.save(login_method)
        # check if organization exists otherwise create a new organization
        organization = organization_repo.find_by_name(signup_params.company_name)
        if not organization:
            organization = Organization(name=signup_params.company_name)
            organization_repo.save(organization)
        # mask card number and then hash it to store in db
        card_number_masked = mask_credit_card(signup_params.card_number)
        card_hash = hash_sensitive_info(signup_params.card_number+signup_params.cvv+signup_params.expiry_date, signup_params.email)
        payment_info = PaymentInfo(person=person, card_number_masked=card_number_masked, card_hash=card_hash, card_holder_name=signup_params.card_holder_name)
        payment_info_repo.save(payment_info)
        # Generate verification token and send mail
        verification_token = generate_confirmation_token(signup_params.email, env['VERIFICATION_KEY'])
        verification_link = f"{env['DOMAIN']}/verify-email?token={verification_token}"
        send_email(verification_link, 'USER_SIGNUP' , signup_params.email)
        return jsonify({'message': 'Sign-up successful, please verify your email.',
                        'person':f'{signup_params.first_name}   {signup_params.last_name}', 'email': signup_params.email}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

### VERIFY EMAIL ROUTE
@signup_bp.route('/verify-email/<token>', methods=['GET'])
def verify_email(token):
    try:
        email_repo = RepositoryFactory.get_repository(EmailRepository)
        login_method_repo = RepositoryFactory.get_repository(LoginMethodRepository)
        # validate verification token
        email = validate_confirmation_token(token, env['VERIFICATION_KEY'], TOKEN_EXPIRY)
        if not email:
            return jsonify({'error': 'Invalid Token'}), 400
        
        emailM = email_repo.find_by_email(email)
        if emailM.is_verified:
            return jsonify({'message': 'Email already verified'}), 200
        login_method = login_method_repo.find_by_email({'email.email': email})
        emailM.is_verified = 1
        login_method.email = emailM
        email_repo.save(emailM)
        login_method_repo.save(login_method)
        return jsonify({'message': 'Email verified successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
