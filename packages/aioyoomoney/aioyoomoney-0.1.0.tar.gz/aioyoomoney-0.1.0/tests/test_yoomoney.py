import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime

from pydantic import HttpUrl

from aioyoomoney import YooMoney
from aioyoomoney.schemas.account import Account
from aioyoomoney.schemas.operation_details import OperationDetails
from aioyoomoney.schemas.operation_history import OperationResponse, Operations
from aioyoomoney.schemas.quick_pay import QuickPay
from aioyoomoney.data_classes.payment_status import PaymentStatus



@pytest.fixture
def client():
    return YooMoney(token="fake_token", receiver="410011161616877")


@pytest.mark.asyncio
async def test_account_info(client):
    mock_data = {
        "account": "410011161616877",
        "balance": 1000.0,
        "currency": "643",
        "account_type": "personal",
        "identified": True,
        "account_status": "available",
        "balance_details": {
            "total": 1000.0,
            "available": 950.0,
            "deposition_pending": 0.0,
            "blocked": 50.0,
            "debt": 0.0,
            "hold": 0.0
        }
    }

    with patch.object(client, "_request", AsyncMock(return_value=mock_data)):
        result = await client.account_info()
        assert isinstance(result, Account)
        assert str(result.account) == mock_data["account"]


@pytest.mark.asyncio
async def test_operation_history_success(client):
    mock_response = {
        "operations": [],
        "next_record": None,
        "error": None
    }

    with patch.object(client, "_request", AsyncMock(return_value=mock_response)):
        result = await client.operation_history()
        assert isinstance(result, OperationResponse)
        assert result.error is None


@pytest.mark.asyncio
async def test_operation_history_error(client):
    mock_response = {
        "operations": [],
        "next_record": None,
        "error": "illegal_param_label"
    }

    with patch.object(client, "_request", AsyncMock(return_value=mock_response)):
        with pytest.raises(Exception):
            await client.operation_history()


@pytest.mark.asyncio
async def test_operation_details_success(client):
    mock_response = {
        "operation_id": "12345",
        "status": "success",
        "amount": 100,
        "label": "invoice_id_1",
        "error": None,
        "direction": "out",
        "datetime": datetime.now().isoformat(),
        "title": "Test shop",
        "sender": "410011111111111",
        "recipient": "410022222222222",
        "recipient_type": "account",
        "message": "Thanks for purchase",
        "comment": "Test comment",
        "label": "test-label",
        "details": "Details about the operation",
        "type": "payment-c2c",
        "digital_goods": {
            "merchantArticleId": "shop123",
            "serial": "ABC123456",
            "secret": "xyz-secret-token"
        }
    }

    with patch.object(client, "_request", AsyncMock(return_value=mock_response)):
        result = await client.operation_details("12345")
        assert isinstance(result, OperationDetails)
        assert result.operation_id == mock_response["operation_id"]


@pytest.mark.asyncio
async def test_operation_details_error(client):
    mock_response = {
        "operation_id": "1234567890",
        "status": "success",
        "error": "operation_error",
        # other fields remain the same
    }

    with patch.object(client, "_request", AsyncMock(return_value=mock_response)):
        with pytest.raises(Exception):
            await client.operation_details("1234567890")



@pytest.mark.asyncio
async def test_create_invoice(client):
    with patch.object(client, "_request", AsyncMock(return_value="https://yoomoney.ru/quickpay/confirm?id=abc123")):
        invoice = await client.create_invoice(
            amount=500.0,
            invoice_id="order-1",
            redirect_url="https://example.com"
        )
        assert isinstance(invoice, QuickPay)
        assert isinstance(invoice.url_pay, HttpUrl)


@pytest.mark.asyncio
async def test_check_invoice_success(client):
    operation = Operations(
        group_id="2342342",
        operation_id=123,
        datetime=datetime.now(),
        title="tit",
        pattern_id="ewrwe",
        direction="in",
        amount=100.0,
        type="deposition",
        status=PaymentStatus.SUCCESS,
        label="order-1"
    )
    mock_response = OperationResponse(operations=[operation], next_record=None, error=None)

    with patch.object(client, "operation_history", AsyncMock(return_value=mock_response)):
        result = await client.check_invoice("order-1")
        assert result is True


@pytest.mark.asyncio
async def test_check_invoice_fail(client):
    operation = Operations(
        group_id="2342342",
        operation_id=123,
        datetime=datetime.now(),
        title="tit",
        pattern_id="ewrwe",
        direction="in",
        amount=100.0,
        type="deposition",
        status=PaymentStatus.SUCCESS,
        label="order-2"
    )
    mock_response = OperationResponse(operations=[operation], next_record=None, error=None)

    with patch.object(client, "operation_history", AsyncMock(return_value=mock_response)):
        result = await client.check_invoice("order-1")
        assert result is False
