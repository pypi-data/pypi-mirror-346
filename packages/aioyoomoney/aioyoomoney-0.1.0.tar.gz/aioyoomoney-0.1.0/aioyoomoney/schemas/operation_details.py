from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, Field

class DigitalGoods(BaseModel):
    merchant_id: Optional[str] = Field(alias="merchantArticleId")
    serial: Optional[str] = None
    secret: Optional[str] = None


class OperationDetails(BaseModel):
    # Код ошибки, присутствует при ошибке выполнения запроса.
    error: Optional[str] = None

    # Идентификатор операции. Значение параметра соответствует либо значению параметра operation_id
    # ответа метода operation-history либо, в случае если запрашивается история счета плательщика,
    # значению поля payment_id ответа метода process-payment.
    operation_id: str

    # Статус платежа (перевода). Значение параметра соответствует значению поля status ответа метода operation-history.
    status: Optional[str] = None

    # Идентификатор шаблона платежа, по которому совершен платеж. Присутствует только для платежей.
    pattern_id: Optional[str] = None

    # Направление движения средств. Может принимать значения:
    # in (приход);
    # out (расход).
    direction: Literal["in", "out"]

    # Сумма операции (сумма списания со счета).
    amount: float

    # Сумма к получению. Присутствует для исходящих переводов другим пользователям.
    amount_due: Optional[float] = None

    # Сумма комиссии. Присутствует для исходящих переводов другим пользователям.
    fee: Optional[float] = None

    # Дата и время совершения операции.
    date: datetime = Field(alias="datetime")

    # Краткое описание операции (название магазина или источник пополнения).
    title: str

    # Номер счета отправителя перевода. Присутствует для входящих переводов от других пользователей.
    sender: Optional[str] = None

    # Идентификатор получателя перевода. Присутствует для исходящих переводов другим пользователям.
    recipient: Optional[str] = None

    # Тип идентификатора получателя перевода. Возможные значения:
    # account — номер счета получателя в сервисе ЮMoney;
    # phone — номер привязанного мобильного телефона получателя;
    # email — электронная почта получателя перевода.
    # Присутствует для исходящих переводов другим пользователям.
    recipient_type: Optional[Literal["account", "phone", "email"]] = None

    # Сообщение получателю перевода. Присутствует для переводов другим пользователям.
    message: Optional[str] = None

    # Комментарий к переводу или пополнению. Присутствует в истории отправителя перевода или получателя пополнения.
    comment: Optional[str] = None

    # Метка платежа. Присутствует для входящих и исходящих переводов другим пользователям ЮMoney,
    # у которых был указан параметр label вызова request-payment.
    label: Optional[str] = None

    # Детальное описание платежа. Строка произвольного формата, может содержать любые символы и переводы строк.
    # Необязательный параметр.
    details: Optional[str] = None

    # Тип операции. Описание возможных типов операций см. в описании метода operation-history
    type: str

    # Данные о цифровом товаре (пин-коды и бонусы игр, iTunes, Xbox, etc.)
    # Поле присутствует при успешном платеже в магазины цифровых товаров.
    digital_goods: Optional[DigitalGoods] = None
