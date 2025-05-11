from datetime import datetime
from typing import Optional, List, Literal

from pydantic import BaseModel, Field


class OperationRequest(BaseModel):
    type: Optional[str] = Field(
        examples=["deposition", "payments", "deposition payments"],
        description="Перечень типов операций, которые требуется отобразить",
        default=None
    )
    label: Optional[str] = Field(
        default=None,
        description="Отбор платежей по значению метки. Выбираются платежи, "
                    "у которых указано заданное значение параметра label вызова request-payment."
    )
    from_: Optional[datetime] = Field(
        alias="from",
        description="Вывести операции от момента времени (операции, равные from, или более поздние)."
                    " Если параметр отсутствует, выводятся все операции.",
        default=None
    )
    till: Optional[datetime] = Field(
        description="Вывести операции до момента времени (операции более ранние, чем till)."
                    " Если параметр отсутствует, выводятся все операции.",
        default=None
    )
    start_record: Optional[str] = Field(
        description="Если параметр присутствует, то будут отображены операции, начиная с номера start_record. "
                    "Операции нумеруются с 0."
                    "Подробнее: https://yoomoney.ru/docs/wallet/user-account/operation-history#filtering-logic",
        default=None
    )
    records: int = Field(
        description="Количество запрашиваемых записей истории операций. "
                    "Допустимые значения: от 1 до 100, по умолчанию — 30.",
        ge=1,
        lt=100,
        default=30
    )
    details: bool = Field(
        description="Показывать подробные детали операции. По умолчанию false. "
                    "Для отображения деталей операции требуется наличие права operation-details.",
        default=False
    )

class SpendingCategory(BaseModel):
    name: str
    sum: float

class Operations(BaseModel):
    # Группа платежей
    group_id: Optional[str] = None

    # Идентификатор операции.
    operation_id: int

    # Статус платежа (перевода). Может принимать следующие значения:
    # success — платеж завершен успешно;
    # refused — платеж отвергнут получателем или отменен отправителем;
    # in_progress — платеж не завершен или перевод не принят получателем.
    status: Literal["success", "refused", "in_progress"]

    # Дата и время совершения операции.
    date: datetime = Field(alias="datetime")

    # Краткое описание операции (название магазина или источник пополнения).
    title: Optional[str] = None

    #Идентификатор шаблона, по которому совершен платеж. Присутствует только для платежей.
    pattern_id: Optional[str] = None

    #Направление движения средств. Может принимать значения:
    #in (приход);
    #out (расход).
    direction: Literal["in", "out"]

    # Сумма операции.
    amount: float

    # Метка платежа. Присутствует для входящих и исходящих переводов другим пользователям ЮMoney,
    # у которых был указан параметр label вызова request-payment.
    label: Optional[str] = None

    # Тип операции. Возможные значения:
    # payment-shop — исходящий платеж в магазин;
    # outgoing-transfer — исходящий P2P-перевод любого типа;
    # deposition — зачисление;
    # incoming-transfer — входящий перевод.
    type: Literal["payment-shop", "outgoing-transfer", "deposition", "incoming-transfer"]

    # Категории расходов
    spending_categories: List[SpendingCategory] = Field(alias="spendingCategories", default=[])

    # Валюта
    amount_currency: Optional[str] = None

    # Поле провода платежа через СБП
    is_sbp_operation: Optional[bool] = None

    # Получатель
    recipient: Optional[str] = None

    # Тип получателя
    recipient_type: Optional[str] = None

    # Прикрепленное сообщение
    message: Optional[str] = None

    # Комментарий
    comment: Optional[str] = None

    # Пока не знаю что такое
    codepro: Optional[bool] = None

    # Детали платежа
    details: Optional[str] = None


class OperationResponse(BaseModel):
    error: Optional[str] = None
    next_record: Optional[str] = None
    operations: List[Operations]