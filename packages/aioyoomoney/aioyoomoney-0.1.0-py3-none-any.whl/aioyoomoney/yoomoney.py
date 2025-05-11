import uuid
from datetime import datetime
from typing import Union, Literal, Optional

from pydantic import HttpUrl
from yarl import URL

from .base.session import ContextSession
from .data_classes.payment_status import PaymentStatus
from .globals import API_URL, ERROR_CODES
from .schemas.account import Account
from .schemas.operation_details import OperationDetails
from .schemas.operation_history import OperationRequest, OperationResponse
from .schemas.quick_pay import QuickPay


class YooMoney:
    def __init__(
            self,
            token: str,
            receiver: Optional[str] = None
    ):
        self.__token = token
        self.__headers = {
            'Authorization': 'Bearer ' + self.__token,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        self.__receiver = receiver


    async def _request(
            self,
            url: str = API_URL,
            endpoint: str = "",
            method: str = "POST",
            is_json: bool = True,
            **kwargs) -> Union[dict, URL]:
        async with (ContextSession(url=f"{url}{endpoint}", method=method, headers=self.__headers, **kwargs)
                    as session):
            if is_json:
                return await session.json()
            return session.url

    async def account_info(self) -> Account:
        """
        Получение информации о состоянии счета пользователя.
        :return: Account
        """
        return Account(**await self._request(
            endpoint="account-info",
            method="POST"
        )
                       )

    async def operation_history(
            self,
            type_: Union[Literal["deposition", "payment"], str] = None,
            label: Optional[str] = None,
            from_: Optional[datetime] = None,
            till: Optional[datetime] = None,
            start_record: Optional[str] = None,
            records: Optional[int] = 30,
            details: Optional[bool] = False
    ) -> OperationResponse:
        """
        Метод позволяет просматривать историю операций (полностью или частично) в постраничном режиме.
        Записи истории выдаются в обратном хронологическом порядке: от последних к более ранним.

        :param type_: str - Перечень типов операций, которые требуется отобразить
        :param label: str - Отбор платежей по значению метки. Выбираются платежи,
                      у которых указано заданное значение параметра label вызова request-payment.
        :param from_: datetime - Вывести операции от момента времени (операции, равные from, или более поздние).
                      Если параметр отсутствует, выводятся все операции.
        :param till: datetime - Вывести операции до момента времени (операции более ранние, чем till).
                     Если параметр отсутствует, выводятся все операции.
        :param start_record: str - Если параметр присутствует, то будут отображены операции, начиная с номера start_record.
                             Операции нумеруются с 0.
                            Подробнее: https://yoomoney.ru/docs/wallet/user-account/operation-history#filtering-logic
        :param records: int - Количество запрашиваемых записей истории операций.
                        Допустимые значения: от 1 до 100, по умолчанию — 30.
        :param details: bool - Показывать подробные детали операции. По умолчанию false.
                        Для отображения деталей операции требуется наличие права operation-details.
        :return: OperationResponse
        """
        operation = OperationRequest(**{
            "type": type_,
            "label": label,
            "from": from_,
            "till": till,
            "start_record": start_record,
            "records": records,
            "details": details
        }
        )
        response = await self._request(
            endpoint="operation-history",
            method="POST",
            params=operation.model_dump_json())

        response = OperationResponse(**response)

        if response.error is not None:
            error = ERROR_CODES.get(response.error, None)
            if error:
                raise error()
            else:
                raise Exception("Непредвиденная ошибка. Попробуйте осуществить запрос позже!")

        return response

    async def operation_details(self, operation_id: str) -> OperationDetails:
        """
        Позволяет получить детальную информацию об операции из истории.
        :param operation_id: str - Идентификатор операции. Значение параметра следует указывать как
                                   значение параметра operation_id ответа метода operation-history или
                                   значение поля payment_id ответа метода process-payment,
                                   если запрашивается история счета плательщика.
        :return: OperationDetails
        """
        response  = await self._request(
            endpoint="operation-details",
            method="POST",
            data={
                "operation_id": operation_id
            }
        )
        response = OperationDetails(**response)

        if response.error is not None:
            error = ERROR_CODES.get(response.error, None)
            if error:
                raise error()
            else:
                raise Exception("Непредвиденная ошибка. Попробуйте осуществить запрос позже!")

        return response

    async def create_invoice(
            self,
            amount: float,
            invoice_id: Union[int, str, uuid.UUID] = None,
            redirect_url: Union[str, HttpUrl] = None
    ) -> QuickPay:
        """
        Форма — это набор полей с информацией о переводе. Форму можно разместить в своем интерфейсе
        (например, на сайте или в блоге).
        Когда отправитель нажимает на кнопку, данные формы отправляются в ЮMoney и инициируют
        распоряжение на перевод в ваш кошелек.
        :param amount: float - Сумма перевода (спишется с отправителя).
        :param invoice_id: int, str - Идентификатор платежа, чтобы было проще потом найти. Желательно сохранять в бд.
        :param redirect_url: str, HttpUrl - URL для редиректа после оплаты.
        :return: QuickPay
        """
        if not self.__receiver:
            raise AttributeError("Укажите номер кошелька ЮMoney, на который нужно зачислять деньги отправителей в"
                                 "классе Yoomoney(receiver=?)")
        url = "https://yoomoney.ru/quickpay/confirm"

        invoice_id = invoice_id if invoice_id else uuid.uuid4()

        if redirect_url:
            redirect_url = HttpUrl(str(redirect_url))

        data = {
            "receiver": self.__receiver,
            "quickpay-form": "button",
            "paymentType": "AC",
            "sum": amount,
            "label": invoice_id ,
            "successURL": redirect_url
        }
        response: URL = await self._request(
            url=url,
            data=data,
            is_json=False
        )

        return QuickPay(
            url_pay=HttpUrl(str(response)),
            invoice_id=invoice_id,
            redirect_url=redirect_url
        )

    async def check_invoice(self, invoice_id: Union[int, str, uuid.UUID]) -> bool:
        operations = (await self.operation_history()).operations
        invoice_id = str(invoice_id)
        for operation in operations:
            if operation.status == PaymentStatus.SUCCESS and operation.label == invoice_id:
                return True
        return False

