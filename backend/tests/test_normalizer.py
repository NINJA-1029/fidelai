from datetime import datetime, timezone
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
    assert txn.timestamp.year == 2026
    assert txn.timestamp.month == 8
    assert txn.timestamp.day == 28


def test_sms_parser_salary_credit():
    raw_sms = "INR 65,000.00 credited to A/C XX4102 on 01-Aug-2026 for Tech Corp Salary."
    txn = SMSParser.parse_sms(raw_sms, user_id="user_demo_01")
    
    assert txn is not None
    assert txn.amount == 65000.0
    assert txn.type == TransactionType.CREDIT
    assert txn.category == TransactionCategory.INCOME
    assert txn.confidence >= 0.85


def test_sms_parser_icici_upi_dining():
    raw_sms = "Dear Customer, your A/C XX7890 has been debited with INR 2,499.00 on 12-Aug-26. Info: UPI/Swiggy/swiggy@icici. Available Balance is INR 45,210.00."
    txn = SMSParser.parse_sms(raw_sms, user_id="user_demo_01")
    
    assert txn is not None
    assert txn.amount == 2499.0
    assert txn.type == TransactionType.DEBIT
    assert txn.category == TransactionCategory.DINING
    assert "Swiggy" in txn.description
    assert txn.account_id == "acc_7890"


def test_sms_parser_sbi_utility_bill():
    raw_sms = "Dear SBI User, your A/C ending with 3456 has been debited by Rs.2450.00 on 20-Aug-26 transfer to BESCOM Electric Bill Ref No 627192. Bal: INR 28000.00"
    txn = SMSParser.parse_sms(raw_sms, user_id="user_demo_01")
    
    assert txn is not None
    assert txn.amount == 2450.0
    assert txn.type == TransactionType.DEBIT
    assert txn.category == TransactionCategory.UTILITIES
    assert "BESCOM Electric Bill" in txn.description


def test_sms_parser_axis_transportation():
    raw_sms = "INR 850.00 debited from Axis Bank A/C XX5678 on 15-Aug-26 towards UBER INDIA. Avl Bal: INR 28,000."
    txn = SMSParser.parse_sms(raw_sms, user_id="user_demo_01")
    
    assert txn is not None
    assert txn.amount == 850.0
    assert txn.type == TransactionType.DEBIT
    assert txn.category == TransactionCategory.TRANSPORTATION
    assert "UBER INDIA" in txn.description


def test_sms_parser_kotak_groceries():
    raw_sms = "Sent Rs. 1,850.00 from Kotak Bank A/c ...8901 to grocery@okaxis (Reliance Fresh)."
    txn = SMSParser.parse_sms(raw_sms, user_id="user_demo_01")
    
    assert txn is not None
    assert txn.amount == 1850.0
    assert txn.type == TransactionType.DEBIT
    assert txn.category == TransactionCategory.GROCERIES
    assert "Reliance Fresh" in txn.description


def test_sms_parser_hdfc_credit_card_shopping():
    raw_sms = "Alert: INR 4,999.00 spent on your HDFC Bank Card XX9876 at Amazon India on 18-Aug-2026. Avl Lmt: INR 95,000"
    txn = SMSParser.parse_sms(raw_sms, user_id="user_demo_01")
    
    assert txn is not None
    assert txn.amount == 4999.0
    assert txn.type == TransactionType.DEBIT
    assert txn.category == TransactionCategory.SHOPPING
    assert "Amazon India" in txn.description


def test_sms_parser_recurring_sip_investment():
    raw_sms = "INR 5,000.00 debited from A/C XX4102 on 05-Aug-2026 towards Zerodha Monthly SIP. Avl Bal: INR 50,000.00"
    txn = SMSParser.parse_sms(raw_sms, user_id="user_demo_01")
    
    assert txn is not None
    assert txn.amount == 5000.0
    assert txn.category == TransactionCategory.INVESTMENT
    assert txn.is_recurring is True


def test_sms_parser_date_formats():
    # DD-Mon-YYYY
    t1 = SMSParser.parse_date("28-Aug-2026")
    assert t1 is not None and t1.year == 2026 and t1.month == 8 and t1.day == 28

    # DDMonYY
    t2 = SMSParser.parse_date("15AUG26")
    assert t2 is not None and t2.year == 2026 and t2.month == 8 and t2.day == 15

    # DD/MM/YYYY
    t3 = SMSParser.parse_date("04/09/2026")
    assert t3 is not None and t3.year == 2026 and t3.month == 9 and t3.day == 4

    # YYYY-MM-DD
    t4 = SMSParser.parse_date("2026-11-30")
    assert t4 is not None and t4.year == 2026 and t4.month == 11 and t4.day == 30


def test_sms_parser_available_balance_extraction():
    b1 = SMSParser.extract_available_balance("INR 1,000 debited. Avl Bal: INR 30,000.00")
    assert b1 == 30000.0

    b2 = SMSParser.extract_available_balance("Charged Rs 500. Available Balance is Rs. 15,200.50")
    assert b2 == 15200.50

    b3 = SMSParser.extract_available_balance("Paid Rs 200. No balance mentioned.")
    assert b3 is None


def test_sms_parser_unrecognized_capping():
    # Generic unclassified merchant should cap confidence < 0.70
    raw_sms = "INR 350.00 debited from A/C XX4102 at XYZ Enterprises."
    txn = SMSParser.parse_sms(raw_sms, user_id="user_demo_01")
    
    assert txn is not None
    assert txn.category == TransactionCategory.OTHER
    assert txn.confidence < 0.70


def test_sms_parser_unparseable_text():
    raw_text = "Your OTP for login is 987654. Do not share it with anyone."
    txn = SMSParser.parse_sms(raw_text, user_id="user_demo_01")
    assert txn is None


def test_financial_event_normalizer_sms():
    raw_sms = "INR 2,000.00 debited from A/C XX4102 at Power Grid Electric Bill. Avl Bal: INR 35,000.00"
    event = FinancialEventNormalizer.normalize_sms(user_id="user_demo_01", raw_sms=raw_sms)
    
    assert event.event_type == "transaction_created"
    assert event.source == "sms"
    assert event.transaction is not None
    assert event.transaction.amount == 2000.0
    assert event.payload["available_balance"] == 35000.0
    assert event.payload["extracted_category"] == "utilities"


def test_financial_event_normalizer_unparseable_sms():
    raw_sms = "Dear user, welcome to our service."
    event = FinancialEventNormalizer.normalize_sms(user_id="user_demo_01", raw_sms=raw_sms)
    
    assert event.event_type == "transaction_created"
    assert event.source == "sms"
    assert event.transaction is None
    assert event.confidence <= 0.30
    assert event.payload["raw_sms"] == raw_sms


def test_financial_event_normalizer_transaction_dict():
    data = {
        "transaction_id": "tx_custom_001",
        "user_id": "user_demo_01",
        "account_id": "acc_01",
        "amount": 4500.0,
        "currency": "INR",
        "type": "debit",
        "category": "housing",
        "description": "Society Maintenance Fee",
        "timestamp": "2026-08-20T10:00:00Z",
        "source": "bank_api",
        "confidence": 1.0,
        "is_recurring": True,
    }
    event = FinancialEventNormalizer.normalize_transaction_dict(user_id="user_demo_01", data=data)
    
    assert event.transaction is not None
    assert event.transaction.amount == 4500.0
    assert event.transaction.category == TransactionCategory.HOUSING
    assert event.transaction.is_recurring is True


def test_financial_event_normalizer_receipt():
    receipt_data = {
        "receipt_id": "rcpt_987",
        "merchant_name": "Apollo Pharmacy",
        "total_amount": 1450.0,
        "currency": "INR",
        "timestamp": "2026-08-25T14:20:00Z",
        "items": [{"name": "Prescription Medicines", "price": 1450.0}],
        "confidence": 0.96,
    }
    event = FinancialEventNormalizer.normalize_receipt(user_id="user_demo_01", receipt_data=receipt_data)
    
    assert event.source == "receipt"
    assert event.transaction is not None
    assert event.transaction.amount == 1450.0
    assert event.transaction.category == TransactionCategory.HEALTHCARE
    assert "Apollo Pharmacy" in event.transaction.description


def test_financial_event_normalizer_csv_row():
    row = {
        "Date": "2026-08-15",
        "Description": "Netflix Monthly Subscription",
        "Amount": "649.00",
        "Type": "Debit",
        "Account": "XX9900",
    }
    mapping = {
        "date": "Date",
        "description": "Description",
        "amount": "Amount",
        "type": "Type",
        "account": "Account",
    }
    event = FinancialEventNormalizer.normalize_csv_row(
        user_id="user_demo_01",
        row=row,
        column_mapping=mapping,
    )
    
    assert event.source == "csv"
    assert event.transaction is not None
    assert event.transaction.amount == 649.0
    assert event.transaction.category == TransactionCategory.ENTERTAINMENT
    assert event.transaction.is_recurring is True


def test_financial_event_normalizer_manual():
    manual_data = {
        "amount": 300.0,
        "type": "debit",
        "category": "transportation",
        "description": "Auto Rickshaw Cash Fare",
    }
    event = FinancialEventNormalizer.normalize_manual(user_id="user_demo_01", transaction_data=manual_data)
    
    assert event.source == "manual"
    assert event.confidence == 1.0
    assert event.transaction is not None
    assert event.transaction.amount == 300.0
    assert event.transaction.category == TransactionCategory.TRANSPORTATION


def test_financial_event_normalizer_batch():
    batch = [
        {"source": "sms", "raw_text": "INR 500 debited at Starbucks on 10-Aug-2026."},
        {"source": "manual", "amount": 100.0, "type": "debit", "category": "dining", "description": "Coffee"},
    ]
    events = FinancialEventNormalizer.normalize_batch(user_id="user_demo_01", items=batch)
    
    assert len(events) == 2
    assert events[0].transaction is not None
    assert events[0].transaction.category == TransactionCategory.DINING
    assert events[1].source == "manual"

