from pydantic import BaseModel
from typing import Optional

class SignupParams(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    company_name: str
    referral_code: Optional[str] = None
    card_number: str
    cvv: str
    expiry_date: str
    card_holder_name: str

class SigninParams(BaseModel):
    email: str
    password: str

class ResendEmailParams(BaseModel):
    email: str
    event: str
