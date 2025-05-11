from pydantic import BaseModel, Field, HttpUrl
from typing import Union, Optional
from uuid import UUID


class QuickPay(BaseModel):
    """
    Форма для выставления счетов пользователям.
    """

    url_pay: HttpUrl = Field(
        ...,
        description="URL для оплаты счета"
    )
    invoice_id: Union[str, int, UUID] = Field(
        ...,
        description="Идентификатор платежа (строка, число или UUID)"
    )
    redirect_url: Optional[HttpUrl] = Field(
        None,
        description="URL для редиректа после оплаты"
    )
