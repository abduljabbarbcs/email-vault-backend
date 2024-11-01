from typing import Optional
from rococo.models import VersionedModel
from rococo.models import Person
from dataclasses import field
from dataclasses import dataclass

from dataclasses import dataclass

@dataclass
class ReferralCode(VersionedModel):
    code: str = None
    referrer_person_id: str = field(default=None, metadata={
        'relationship': {'model': 'Person'},
        'field_type': 'entity_id'
    })
    referred_person_id: str = field(default=None, metadata={
        'relationship': {'model': 'Person'},
        'field_type': 'entity_id'
    })
    class Meta:
        table_name = 'referral_codes'


@dataclass
class PaymentInfo(VersionedModel):
    """A model to store masked and secure payment information."""
    person: str = field(default=None, metadata={
        'relationship': {'model': 'Person'},
        'field_type': 'entity_id'
    })
    card_holder_name:str = None
    card_number_masked: str = None
    card_hash: str = None

    class Meta:
        table_name = 'payment_info'
