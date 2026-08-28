import re
from datetime import datetime
from typing import Dict, Any, Optional
from shared.contracts.contracts import Transaction, TransactionType, TransactionCategory


class SMSParser:
    """
    Parses raw SMS banking text messages to extract financial transaction data.
    """
    
    # Common Indian Bank SMS regex patterns
    PATTERNS = [
        # Pattern 1: "INR 12,000.00 debited from A/C XX4102 on 28-Aug-2026 at Care Diagnostics"
        re.compile(
            r"(?:INR|Rs\.?)\s*(?P<amount>[0-9,]+(?:\.[0-9]{2})?)\s*(?P<type>debited|credited|spent|withdrawn)"
            r".*?(?:from|to|in)\s*(?:A\/C|acct|card)?\s*(?P<account>[X\d]+)?"
            r".*?(?:at|to|for|vpa)\s*(?P<merchant>[A-Za-z0-9\s\.\-_]+?)(?:\.|\s+Avl|\s+on|\s*$)",
            re.IGNORECASE
        ),
        # Pattern 2: "Txn of INR 12000.00 done on HDFC Bank Card XX1234 at Care Diagnostics"
        re.compile(
            r"(?:Txn of|Paid)\s*(?:INR|Rs\.?)\s*(?P<amount>[0-9,]+(?:\.[0-9]{2})?)"
            r".*?(?:at|to)\s*(?P<merchant>[A-Za-z0-9\s\.\-_]+?)(?:\.|\s+Avl|\s+on|\s*$)",
            re.IGNORECASE
        )
    ]

    @staticmethod
    def parse_sms(raw_text: str, user_id: str, default_account_id: str = "acc_primary") -> Optional[Transaction]:
        clean_text = raw_text.replace("\n", " ").strip()
        
        amount = None
        txn_type = TransactionType.DEBIT
        merchant = "Unknown Merchant"
        account_id = default_account_id
        confidence = 0.5
        
        # Determine transaction type from keywords
        lower_text = clean_text.lower()
        if "credit" in lower_text or "received" in lower_text or "refund" in lower_text:
            txn_type = TransactionType.CREDIT
        elif "debit" in lower_text or "spent" in lower_text or "paid" in lower_text or "withdrawn" in lower_text:
            txn_type = TransactionType.DEBIT

        for pattern in SMSParser.PATTERNS:
            match = pattern.search(clean_text)
            if match:
                groups = match.groupdict()
                if "amount" in groups and groups["amount"]:
                    raw_amount = groups["amount"].replace(",", "")
                    try:
                        amount = float(raw_amount)
                        confidence += 0.3
                    except ValueError:
                        pass
                
                if "merchant" in groups and groups["merchant"]:
                    merchant = groups["merchant"].strip()
                    confidence += 0.15
                    
                if "account" in groups and groups["account"]:
                    account_id = f"acc_{groups['account'].strip()}"
                    confidence += 0.05
                break
                
        # Fallback simple amount extraction if regex failed full match
        if amount is None:
            amt_match = re.search(r"(?:INR|Rs\.?)\s*([0-9,]+(?:\.[0-9]{2})?)", clean_text, re.IGNORECASE)
            if amt_match:
                try:
                    amount = float(amt_match.group(1).replace(",", ""))
                    confidence = 0.6
                except ValueError:
                    return None
            else:
                return None

        # Determine category
        category = TransactionCategory.OTHER
        merchant_lower = merchant.lower()
        if any(w in merchant_lower for w in ["hospital", "medical", "clinic", "care", "diagnostics", "pharmacy"]):
            category = TransactionCategory.UNEXPECTED
        elif any(w in merchant_lower for w in ["salary", "payroll", "tech corp"]):
            category = TransactionCategory.INCOME
        elif any(w in merchant_lower for w in ["supermarket", "groceries", "mart", "store"]):
            category = TransactionCategory.GROCERIES
        elif any(w in merchant_lower for w in ["rent", "landlord", "housing"]):
            category = TransactionCategory.HOUSING
        elif any(w in merchant_lower for w in ["electric", "water", "bill", "broadband"]):
            category = TransactionCategory.UTILITIES

        confidence = min(1.0, confidence)
        
        return Transaction(
            transaction_id=f"tx_sms_{int(datetime.utcnow().timestamp())}",
            user_id=user_id,
            account_id=account_id,
            amount=amount,
            currency="INR",
            type=txn_type,
            category=category,
            description=merchant if merchant != "Unknown Merchant" else clean_text[:60],
            timestamp=datetime.utcnow(),
            source="sms",
            confidence=confidence,
            is_recurring=False
        )
