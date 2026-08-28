from backend.ingestion.sms_parser import SMSParser
from backend.ingestion.normalizer import FinancialEventNormalizer
from shared.contracts.contracts import TransactionCategory, TransactionType


def test_sms_parser_emergency_medical():
    raw_sms = "INR 12,000.00 debited from A/C XX4102 on 28-Aug-2026 at Care Diagnostics. Avl Bal: INR 30,000.00"
    txn = SMSParser.parse_sms(raw_sms, user_id="user_demo_01")
    
    assert txn is not None
    assert txn.amount == 12000.0
    assert txn.currency == "INR"
    assert txn.type == TransactionType.DEBIT
    assert txn.category == TransactionCategory.UNEXPECTED
    assert "Care Diagnostics" in txn.description
    assert txn.confidence >= 0.8


def test_sms_parser_salary_credit():
    raw_sms = "INR 65,000.00 credited to A/C XX4102 on 01-Aug-2026 for Tech Corp Salary."
    txn = SMSParser.parse_sms(raw_sms, user_id="user_demo_01")
    
    assert txn is not None
    assert txn.amount == 65000.0
    assert txn.type == TransactionType.CREDIT
    assert txn.category == TransactionCategory.INCOME


def test_financial_event_normalizer():
    raw_sms = "INR 2,000.00 debited from A/C XX4102 at Power Grid Electric Bill."
    event = FinancialEventNormalizer.normalize_sms(user_id="user_demo_01", raw_sms=raw_sms)
    
    assert event.event_type == "transaction_created"
    assert event.source == "sms"
    assert event.transaction is not None
    assert event.transaction.amount == 2000.0
