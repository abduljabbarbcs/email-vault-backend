from typing import Type
from rococo.data.mysql import MySqlAdapter
from rococo.models.versioned_model import VersionedModel
from rococo.repositories.mysql import MySqlRepository
from rococo.models import Email, LoginMethod, Organization, OtpMethod, Person, RecoveryCode
from common.models import ReferralCode, PaymentInfo
from dotenv import load_dotenv
import os

load_dotenv()
env = os.environ

class RepositoryFactory:
    _repositories = {}

    @classmethod
    def _get_db_connection(cls):
        return MySqlAdapter(host=env['MYSQL_HOST'], user=env['MYSQL_USER'], database=env['MYSQL_DATABASE'], 
                            port=int(env['MYSQL_PORT']), password=env['MYSQL_PASSWORD'])

    @classmethod
    def get_repository(cls, repo_class: Type[MySqlRepository]):
        if repo_class not in cls._repositories:
            adapter = cls._get_db_connection()
            message_adapter = None 
            message_queue_name = "my_queue"
            cls._repositories[repo_class] = repo_class(adapter, message_adapter, message_queue_name)
        return cls._repositories[repo_class]

class EmailRepository(MySqlRepository):

    def __init__(self, adapter, message_adapter, message_queue_name):
        super().__init__(adapter, Email, message_adapter, message_queue_name)
        self.adapter = adapter

    def find_by_email(self, email: str):
        conditions = {"email": email}
        return self.get_one(conditions)

class LoginMethodRepository(MySqlRepository):

    def __init__(self, adapter, message_adapter, message_queue_name):
        super().__init__(adapter, LoginMethod, message_adapter, message_queue_name)

    def find_by_email(self, condition: dict):
        obj = self.get_one(condition, ['email','person'])    
        return obj

class PersonRepository(MySqlRepository):
    def __init__(self, adapter, message_adapter, message_queue_name):
        super().__init__(adapter, Person, message_adapter, message_queue_name)
    
    def find_by_id(self, person_id: str):
        conditions = {"entity_id": person_id}
        return self.get_one(conditions)

class OrganizationRepository(MySqlRepository):
    def __init__(self, adapter, message_adapter, message_queue_name):
        super().__init__(adapter, Organization, message_adapter, message_queue_name)

    def find_by_name(self, name: str):
        conditions = {"name": name}
        return self.get_one(conditions)

class ReferralCodeRepository(MySqlRepository):
    def __init__(self, adapter, message_adapter, message_queue_name):
        super().__init__(adapter, ReferralCode, message_adapter, message_queue_name)

    def find_by_code(self, code: str):
        conditions = {"code": code}
        return self.get_one(conditions)

class PaymentInfoRepository(MySqlRepository):
    def __init__(self, adapter, message_adapter, message_queue_name):
        super().__init__(adapter, PaymentInfo, message_adapter, message_queue_name)

class OTPMethodRepository(MySqlRepository):
    def __init__(self, adapter, message_adapter, message_queue_name):
        super().__init__(adapter, OtpMethod, message_adapter, message_queue_name)

    def find_by_secret(self, secret: str):
        conditions = {"secret": secret}
        return self.get_one(conditions)

class RecoveryCodeRepository(MySqlRepository):
    def __init__(self, adapter, message_adapter, message_queue_name):
        super().__init__(adapter, RecoveryCode, message_adapter, message_queue_name)

    def find_by_token(self, token: str):
        conditions = {"token": token}
        return self.get_one(conditions)
