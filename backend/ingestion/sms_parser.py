from datetime import datetime, timezone
import re
from typing import Any, Dict, Optional, Tuple
from shared.contracts.contracts import Transaction, TransactionCategory, TransactionType


class SMSParser:
    """
    Parses raw SMS banking text messages from Indian financial institutions to extract
    structured transaction data with deterministic categorization and confidence scoring.
    """

    MONTH_MAP = {
        "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
        "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12
    }

    # Bank-specific and general SMS pattern extractors
    BANK_PATTERNS = [
        # Pattern 1: "INR 12,000.00 debited from A/C XX4102 on 28-Aug-2026 at Care Diagnostics. Avl Bal: INR 30,000.00"
        re.compile(
            r"(?:INR|Rs\.?|₹)\s*(?P<amount>[0-9,]+(?:\.[0-9]{1,2})?)\s+"
            r"(?P<type>debited|credited|spent|withdrawn|transferred|deposited)\s+"
            r"(?:from|to|in)\s+(?:A\/C|acct|account|card)?\s*(?P<account>[X\*\d\.]+)?\s*"
            r"(?:on\s+(?P<date>[0-9A-Za-z\/\-]+)\s*)?"
            r"(?:at|towards|transfer to|transferred to|paid to|to|for|vpa|by)\s+(?P<merchant>[A-Za-z0-9\s\.\-_&'/]+?)"
            r"(?:\.|\s+Avl|\s+Available|\s+Bal|\s+Ref|\s+UPI|\s*$)",
            re.IGNORECASE,
        ),
        # Pattern 2: "Dear SBI User, your A/C ending with 3456 has been debited by Rs.12000.00 on 28Aug26 transfer to Care Diagnostics Ref No 627192. Bal: INR 30000.00"
        re.compile(
            r"(?:A\/C|account|Card)\s*(?:ending with|ending|\*|no\.?)?\s*(?P<account>[X\*\d\.]+)?\s+"
            r"(?:has been|is)?\s*(?P<type>debited|credited)\s+(?:by|with|for)?\s*"
            r"(?:INR|Rs\.?|₹)\s*(?P<amount>[0-9,]+(?:\.[0-9]{1,2})?)\s*"
            r"(?:on\s+(?P<date>[0-9A-Za-z\/\-]+)\s*)?"
            r"(?:transfer to|transferred to|towards|paid to|at|to|for|by)\s+(?P<merchant>[A-Za-z0-9\s\.\-_&'/]+?)"
            r"(?:\.|\s+Ref|\s+Bal|\s+Avl|\s+UPI|\s*$)",
            re.IGNORECASE,
        ),
        # Pattern 3: "Txn of INR 12000.00 done on HDFC Bank Card XX1234 at Care Diagnostics on 28-Aug-2026. Avl Lmt: INR 50,000"
        re.compile(
            r"(?:Txn of|Paid|Alert:)\s*(?:INR|Rs\.?|₹)\s*(?P<amount>[0-9,]+(?:\.[0-9]{1,2})?)\s+"
            r"(?:done on|spent on|charged on|using)?\s*(?:[A-Za-z\s]+)?(?:Card|A\/C|acct)?\s*(?P<account>[X\*\d\.]+)?\s*"
            r"(?:at|to|towards|paid to)\s+(?P<merchant>[A-Za-z0-9\s\.\-_&'/]+?)\s*"
            r"(?:on\s+(?P<date>[0-9A-Za-z\/\-]+)\s*)?"
            r"(?:\.|\s+Avl|\s+Available|\s+Bal|\s+Ref|\s+UPI|\s*$)",
            re.IGNORECASE,
        ),
        # Pattern 4: "Dear Customer, your A/C XX7890 has been debited with INR 2,499.00 on 12-Aug-26. Info: UPI/Swiggy/swiggy@icici. Available Balance is INR 45,210.00"
        re.compile(
            r"(?:A\/C|acct|account)\s*(?:ending with|no\.?|is)?\s*(?P<account>[X\*\d\.]+)?\s+"
            r"(?:has been|is)?\s*(?P<type>debited|credited)\s+(?:with|by|for)\s+"
            r"(?:INR|Rs\.?|₹)\s*(?P<amount>[0-9,]+(?:\.[0-9]{1,2})?)\s*"
            r"(?:on\s+(?P<date>[0-9A-Za-z\/\-]+)\s*)?"
            r"(?:\.\s*Info:\s*(?:UPI\/)?(?P<merchant_info>[A-Za-z0-9\s\.\-_&'/@]+))",
            re.IGNORECASE,
        ),
        # Pattern 5: "Sent Rs. 850.00 from Kotak Bank A/c ...8901 to grocery@okaxis (Reliance Fresh)."
        re.compile(
            r"(?P<type>Sent|Paid|Received)\s*(?:INR|Rs\.?|₹)\s*(?P<amount>[0-9,]+(?:\.[0-9]{1,2})?)\s+"
            r"(?:from|in|to)\s+(?:[A-Za-z\s]+)?(?:A\/c|account|Card)?\s*(?P<account>[X\*\d\.]+)?\s*"
            r"(?:to|from)\s+(?P<merchant>[A-Za-z0-9\s\.\-_&'/@\(\)]+?)"
            r"(?:\.|\s+Avl|\s+Available|\s+Bal|\s+Ref|\s+UPI|\s*$)",
            re.IGNORECASE,
        ),
        # Pattern 6: "Rs 65,000.00 credited to A/C XX4102 on 01-Aug-26 for Tech Corp Salary."
        re.compile(
            r"(?:INR|Rs\.?|₹)\s*(?P<amount>[0-9,]+(?:\.[0-9]{1,2})?)\s+"
            r"(?P<type>credited|received|refunded)\s+(?:to|in)\s+(?:A\/C|acct|account)?\s*(?P<account>[X\*\d\.]+)?\s*"
            r"(?:on\s+(?P<date>[0-9A-Za-z\/\-]+)\s*)?"
            r"(?:for|from|by|towards)\s+(?P<merchant>[A-Za-z0-9\s\.\-_&'/]+?)"
            r"(?:\.|\s+Avl|\s+Available|\s+Bal|\s+Ref|\s+UPI|\s*$)",
            re.IGNORECASE,
        ),
    ]

    @classmethod
    def parse_amount(cls, text: str) -> Optional[float]:
        """Extracts monetary float amount from formatted numeric strings."""
        if not text:
            return None
        cleaned = text.replace(",", "").strip()
        try:
            val = float(cleaned)
            return val if val > 0 else None
        except ValueError:
            return None

    @classmethod
    def parse_transaction_type(cls, text: str) -> TransactionType:
        """Determines if the transaction is a DEBIT or CREDIT."""
        lower = text.lower()
        if any(w in lower for w in ["credit", "credited", "received", "refund", "refunded", "deposited", "cashback", "added"]):
            return TransactionType.CREDIT
        if any(w in lower for w in ["debit", "debited", "spent", "paid", "sent", "withdrawn", "charged", "purchased"]):
            return TransactionType.DEBIT
        return TransactionType.DEBIT

    @classmethod
    def parse_date(cls, date_str: Optional[str]) -> Optional[datetime]:
        """Parses various date representations commonly found in Indian banking SMS."""
        if not date_str:
            return None
        date_str = date_str.strip()

        # Format 1: 28-Aug-2026 or 28-Aug-26 or 28-August-2026
        m = re.match(r"^(\d{1,2})[-/\s]([A-Za-z]{3,9})[-/\s](\d{2,4})$", date_str, re.IGNORECASE)
        if m:
            day, month_str, year_str = m.groups()
            month_key = month_str[:3].lower()
            if month_key in cls.MONTH_MAP:
                month = cls.MONTH_MAP[month_key]
                day = int(day)
                year = int(year_str)
                if year < 100:
                    year += 2000
                try:
                    return datetime(year, month, day, tzinfo=timezone.utc)
                except ValueError:
                    pass

        # Format 2: 28Aug26 or 28AUG2026
        m = re.match(r"^(\d{1,2})([A-Za-z]{3,9})(\d{2,4})$", date_str, re.IGNORECASE)
        if m:
            day, month_str, year_str = m.groups()
            month_key = month_str[:3].lower()
            if month_key in cls.MONTH_MAP:
                month = cls.MONTH_MAP[month_key]
                day = int(day)
                year = int(year_str)
                if year < 100:
                    year += 2000
                try:
                    return datetime(year, month, day, tzinfo=timezone.utc)
                except ValueError:
                    pass

        # Format 3: DD/MM/YYYY or DD-MM-YYYY or DD/MM/YY
        m = re.match(r"^(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})$", date_str)
        if m:
            d1, d2, yr = m.groups()
            day, month = int(d1), int(d2)
            year = int(yr)
            if year < 100:
                year += 2000
            try:
                return datetime(year, month, day, tzinfo=timezone.utc)
            except ValueError:
                pass

        # Format 4: YYYY-MM-DD
        m = re.match(r"^(\d{4})[/-](\d{1,2})[/-](\d{1,2})$", date_str)
        if m:
            year, month, day = int(m.group(1)), int(m.group(2)), int(m.group(3))
            try:
                return datetime(year, month, day, tzinfo=timezone.utc)
            except ValueError:
                pass

        return None

    @classmethod
    def extract_available_balance(cls, text: str) -> Optional[float]:
        """Extracts available bank balance if included in the SMS body."""
        bal_match = re.search(
            r"(?:Avl\s*Bal|Available\s*Balance|Avl\s*Lmt|Bal|Balance)[\s:\-is]+(?:INR|Rs\.?|₹)?\s*([0-9,]+(?:\.[0-9]{1,2})?)",
            text,
            re.IGNORECASE,
        )
        if bal_match:
            return cls.parse_amount(bal_match.group(1))
        return None

    @classmethod
    def clean_merchant_name(cls, raw_merchant: str) -> str:
        """Cleans and extracts standardized entity/merchant name."""
        if not raw_merchant:
            return "Unknown Merchant"
        
        cleaned = raw_merchant.strip()
        # Remove trailing punctuation
        cleaned = re.sub(r"[\.,;:!\-]+$", "", cleaned).strip()
        
        # Check for UPI info like UPI/Swiggy/swiggy@icici or grocery@okaxis (Reliance Fresh)
        paren_match = re.search(r"\((.*?)\)", cleaned)
        if paren_match:
            return paren_match.group(1).strip()

        if "UPI/" in cleaned:
            parts = cleaned.split("UPI/")[-1].split("/")
            if parts and parts[0]:
                return parts[0].strip()

        if "@" in cleaned:
            # e.g., swiggy@icici -> Swiggy
            handle = cleaned.split("@")[0].strip()
            if handle:
                return handle.capitalize()

        # Remove prefix keywords if present
        cleaned = re.sub(r"^(?:transfer to|transferred to|towards|at|to|for|vpa|by)\s+", "", cleaned, flags=re.IGNORECASE).strip()
        
        # Remove trailing reference markers
        cleaned = re.sub(r"\s+(?:Ref|UPI|Avl|Bal|No|dated|on).*$", "", cleaned, flags=re.IGNORECASE).strip()

        return cleaned if cleaned else "Unknown Merchant"

    @classmethod
    def categorize_transaction(cls, merchant: str, full_text: str) -> TransactionCategory:
        """Categorizes transaction based on merchant and narrative keywords."""
        target = f"{merchant} {full_text}".lower()

        # 1. Unexpected & Emergency Expenses
        if any(w in target for w in [
            "hospital", "medical", "clinic", "care diagnostics", "emergency", "trauma",
            "diagnostics", "pathlab", "ambulance", "surgery", "icu"
        ]):
            return TransactionCategory.UNEXPECTED

        # 2. Income
        if any(w in target for w in [
            "salary", "payroll", "tech corp", "stipend", "dividend", "bonus", "freelance",
            "interest credited", "client payment", "consulting fee"
        ]):
            return TransactionCategory.INCOME

        # 3. Housing
        if any(w in target for w in [
            "rent", "landlord", "housing", "maintenance society", "society maintenance",
            "lease", "apartment rent"
        ]):
            return TransactionCategory.HOUSING

        # 4. Utilities
        if any(w in target for w in [
            "electric", "electricity", "bescom", "tneb", "msedcl", "water bill", "gas bill",
            "indane", "hp gas", "broadband", "wifi", "airtel", "jio", "vi bill", "act fibernet",
            "power grid", "billdesk"
        ]):
            return TransactionCategory.UTILITIES

        # 5. Groceries
        if any(w in target for w in [
            "supermarket", "groceries", "grocery", "mart", "reliance fresh", "bigbasket",
            "blinkit", "zepto", "instamart", "dmart", "nature's basket", "spencer", "provisions"
        ]):
            return TransactionCategory.GROCERIES

        # 6. Dining
        if any(w in target for w in [
            "swiggy", "zomato", "restaurant", "cafe", "starbucks", "mcdonalds", "dominos",
            "pizza", "burger", "kfc", "eats", "dining", "barbeque", "bistro", "food"
        ]):
            return TransactionCategory.DINING

        # 7. Transportation
        if any(w in target for w in [
            "uber", "ola", "rapido", "petrol", "fuel", "shell", "hpcl", "bpcl", "iocl",
            "irctc", "indian railways", "metro", "fastag", "toll", "parking", "flight", "indigo"
        ]):
            return TransactionCategory.TRANSPORTATION

        # 8. Healthcare (General non-emergency)
        if any(w in target for w in [
            "pharmacy", "apollo", "netmeds", "1mg", "pharmeasy", "medplus", "dental",
            "dr.", "doctor", "opticals", "lenskart"
        ]):
            return TransactionCategory.HEALTHCARE

        # 9. Shopping
        if any(w in target for w in [
            "amazon", "flipkart", "myntra", "ajio", "meesho", "zara", "h&m", "decathlon",
            "retail", "croma", "reliance digital", "apparel", "clothing", "shopping"
        ]):
            return TransactionCategory.SHOPPING

        # 10. Entertainment
        if any(w in target for w in [
            "netflix", "spotify", "bookmyshow", "pvr", "inox", "prime video", "hotstar",
            "youtube", "disney", "gaming", "steam", "playstation"
        ]):
            return TransactionCategory.ENTERTAINMENT

        # 11. Investments
        if any(w in target for w in [
            "zerodha", "groww", "mutual fund", "sip", "kuvera", "angelone", "upstox",
            "coin", "smallcase", "cams", "kfintech", "securities"
        ]):
            return TransactionCategory.INVESTMENT

        # 12. Savings
        if any(w in target for w in [
            "fixed deposit", "recurring deposit", "auto-sweep", "fd creation", "rd deposit"
        ]):
            return TransactionCategory.SAVINGS

        # 13. Debt Service / EMI
        if any(w in target for w in [
            "emi", "loan repayment", "credit card payment", "cred", "bajaj finance",
            "home loan", "personal loan", "car loan"
        ]):
            return TransactionCategory.DEBT_SERVICE

        return TransactionCategory.OTHER

    @classmethod
    def check_recurring(cls, text: str) -> bool:
        """Determines if text describes a recurring obligation."""
        lower = text.lower()
        return any(w in lower for w in [
            "recurring", "sip", "monthly", "subscription", "auto-debit", "standing instruction", "emi"
        ])

    @classmethod
    def parse_sms(
        cls,
        raw_text: str,
        user_id: str,
        default_account_id: str = "acc_primary",
        reference_time: Optional[datetime] = None
    ) -> Optional[Transaction]:
        """
        Parses raw SMS text into a validated Transaction contract instance.
        Returns None if no monetary transaction can be confidently parsed.
        """
        if not raw_text or not raw_text.strip():
            return None

        clean_text = raw_text.replace("\n", " ").strip()
        
        amount: Optional[float] = None
        txn_type = cls.parse_transaction_type(clean_text)
        merchant: str = "Unknown Merchant"
        account_id: str = default_account_id
        txn_date: Optional[datetime] = None
        
        # Baseline confidence
        confidence = 0.40

        # Try structured pattern matching
        matched = False
        for pattern in cls.BANK_PATTERNS:
            match = pattern.search(clean_text)
            if match:
                groups = match.groupdict()
                
                # Amount
                if "amount" in groups and groups["amount"]:
                    parsed_amt = cls.parse_amount(groups["amount"])
                    if parsed_amt is not None:
                        amount = parsed_amt
                        confidence += 0.25

                # Type
                if "type" in groups and groups["type"]:
                    txn_type = cls.parse_transaction_type(groups["type"])
                    confidence += 0.10

                # Merchant
                merchant_raw = groups.get("merchant_info") or groups.get("merchant")
                if merchant_raw:
                    merchant = cls.clean_merchant_name(merchant_raw)
                    if merchant != "Unknown Merchant":
                        confidence += 0.15

                # Account
                if "account" in groups and groups["account"]:
                    raw_acc = groups["account"].strip().replace(".", "").replace("X", "").replace("*", "")
                    if raw_acc:
                        account_id = f"acc_{raw_acc}"
                    else:
                        account_id = f"acc_{groups['account'].strip()}"
                    confidence += 0.05

                # Date
                if "date" in groups and groups["date"]:
                    parsed_dt = cls.parse_date(groups["date"])
                    if parsed_dt:
                        txn_date = parsed_dt
                        confidence += 0.05

                matched = True
                break

        # Fallback regex extraction if structured pattern did not match everything
        if amount is None:
            amt_match = re.search(
                r"(?:INR|Rs\.?|₹)\s*([0-9,]+(?:\.[0-9]{1,2})?)",
                clean_text,
                re.IGNORECASE
            )
            if amt_match:
                amount = cls.parse_amount(amt_match.group(1))
                if amount is not None:
                    confidence += 0.25

        if amount is None:
            return None

        # Fallback account extraction if still default
        if account_id == default_account_id:
            acc_match = re.search(r"(?:A\/C|acct|card|ending)\s*(?:XX|\*\*|no\.?)?\s*([X\*\d]{3,8})", clean_text, re.IGNORECASE)
            if acc_match:
                raw_num = acc_match.group(1).replace("X", "").replace("*", "")
                if raw_num:
                    account_id = f"acc_{raw_num}"
                else:
                    account_id = f"acc_{acc_match.group(1)}"
                confidence += 0.05

        # Fallback merchant extraction if still unknown
        if merchant == "Unknown Merchant":
            m_match = re.search(
                r"(?:transfer to|transferred to|paid to|towards|at|to|for|by|vpa)\s+(?!INR|Rs\.?|₹|\d)([A-Za-z0-9\s\.\-_&'/@\(\)]+?)(?:\.|\s+Avl|\s+Available|\s+Bal|\s+Ref|\s+on|\s*$)",
                clean_text,
                re.IGNORECASE
            )
            if m_match:
                candidate = cls.clean_merchant_name(m_match.group(1))
                if candidate != "Unknown Merchant" and candidate.lower() not in ["rs", "inr", "unknown"]:
                    merchant = candidate
                    confidence += 0.10

        # Categorization
        category = cls.categorize_transaction(merchant, clean_text)
        if category != TransactionCategory.OTHER:
            confidence += 0.10
        else:
            # Per docs/ingestion.md: If merchant or category cannot be deduced with high confidence, cap confidence < 0.70
            if merchant == "Unknown Merchant" or confidence > 0.68:
                confidence = min(confidence, 0.65)

        # Date fallback
        if txn_date is None:
            # Try searching anywhere in text for date
            date_match = re.search(r"\b(\d{1,2}[-/\s][A-Za-z]{3,9}[-/\s]\d{2,4}|\d{1,2}[A-Za-z]{3,9}\d{2,4}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b", clean_text)
            if date_match:
                parsed_dt = cls.parse_date(date_match.group(1))
                if parsed_dt:
                    txn_date = parsed_dt
                    confidence += 0.05

        if txn_date is None:
            txn_date = reference_time or datetime.now(timezone.utc)

        # Recurring check
        is_recurring = cls.check_recurring(clean_text)

        confidence = max(0.1, min(1.0, round(confidence, 2)))
        
        # Build deterministic transaction ID
        timestamp_int = int(txn_date.timestamp())
        txn_id = f"tx_sms_{abs(hash(clean_text)) % 1000000:06d}_{timestamp_int}"

        return Transaction(
            transaction_id=txn_id,
            user_id=user_id,
            account_id=account_id,
            amount=amount,
            currency="INR",
            type=txn_type,
            category=category,
            description=merchant if merchant != "Unknown Merchant" else clean_text[:60],
            timestamp=txn_date,
            source="sms",
            confidence=confidence,
            is_recurring=is_recurring,
        )

