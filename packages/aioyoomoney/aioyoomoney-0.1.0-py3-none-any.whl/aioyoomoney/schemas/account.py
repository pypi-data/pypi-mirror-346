from typing import Optional, List

from pydantic import BaseModel

class BalanceDetails(BaseModel):
    total: float
    available: float
    deposition_pending: Optional[float] =None
    blocked: Optional[float] = None
    debt: Optional[float] = None
    hold: Optional[float] = None

class CardsLinked(BaseModel):
    pan_fragment: str
    type: str

class Account(BaseModel):
    account: int
    balance: float
    currency: int
    account_type: str
    identified: bool
    account_status: str
    balance_details: BalanceDetails
    cards_linked: Optional[List[CardsLinked]] = None