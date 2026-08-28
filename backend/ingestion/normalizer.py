from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from shared.contracts.contracts import (
    FinancialEvent,
    Transaction,
    TransactionCategory,
    TransactionType,
)
from backend.ingestion.sms_parser import SMSParser


class FinancialEventNormalizer:
    """
    Normalizes arbitrary incoming financial payloads (SMS, Receipts, CSV rows, manual entries)
    into canonical FinancialEvent and Transaction instances adhering strictly to shared contracts.
    """

    @staticmethod
    def normalize_sms(
        user_id: str,
        raw_sms: str,
        event_id: Optional[str] = None,
        timestamp: Optional[datetime] = None,
        sender: Optional[str] = None,
    ) -> FinancialEvent:
        """
        Normalizes raw SMS banking notifications into a canonical FinancialEvent.
        """
        now = timestamp or datetime.now(timezone.utc)
        transaction = SMSParser.parse_sms(raw_sms, user_id=user_id, reference_time=now)
        available_balance = SMSParser.extract_available_balance(raw_sms)

        payload: Dict[str, Any] = {
            "raw_sms": raw_sms,
            "raw_text": raw_sms,
        }
        if sender:
            payload["sender"] = sender
        if available_balance is not None:
            payload["available_balance"] = available_balance
        if transaction:
            payload["extracted_category"] = transaction.category.value
            payload["account_id"] = transaction.account_id

        confidence = transaction.confidence if transaction else 0.20
        event_timestamp = transaction.timestamp if transaction else now
        unique_event_id = event_id or f"evt_sms_{abs(hash(raw_sms)) % 1000000:06d}_{int(event_timestamp.timestamp())}"

        return FinancialEvent(
            event_id=unique_event_id,
            user_id=user_id,
            event_type="transaction_created",
            timestamp=event_timestamp,
            source="sms",
            confidence=confidence,
            payload=payload,
            transaction=transaction,
        )

    @staticmethod
    def normalize_transaction_dict(
        user_id: str,
        data: Dict[str, Any],
        event_id: Optional[str] = None,
    ) -> FinancialEvent:
        """
        Normalizes a raw transaction dictionary into a canonical FinancialEvent.
        """
        if "user_id" not in data:
            data["user_id"] = user_id
        if "timestamp" not in data:
            data["timestamp"] = datetime.now(timezone.utc)
        elif isinstance(data["timestamp"], str):
            try:
                data["timestamp"] = datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
            except ValueError:
                data["timestamp"] = datetime.now(timezone.utc)

        txn = Transaction(**data)
        unique_event_id = event_id or f"evt_txn_{abs(hash(txn.transaction_id)) % 1000000:06d}_{int(txn.timestamp.timestamp())}"

        return FinancialEvent(
            event_id=unique_event_id,
            user_id=user_id,
            event_type="transaction_created",
            timestamp=txn.timestamp,
            source=txn.source,
            confidence=txn.confidence,
            payload={"raw_transaction": data},
            transaction=txn,
        )

    @staticmethod
    def normalize_receipt(
        user_id: str,
        receipt_data: Dict[str, Any],
        event_id: Optional[str] = None,
    ) -> FinancialEvent:
        """
        Normalizes receipt OCR or digitized line-item structures into a FinancialEvent.
        """
        now = datetime.now(timezone.utc)
        raw_ts = receipt_data.get("timestamp")
        if isinstance(raw_ts, str):
            try:
                ts = datetime.fromisoformat(raw_ts.replace("Z", "+00:00"))
            except ValueError:
                ts = now
        elif isinstance(raw_ts, datetime):
            ts = raw_ts
        else:
            ts = now

        amount = float(receipt_data.get("total_amount") or receipt_data.get("amount", 0.0))
        merchant = receipt_data.get("merchant_name") or receipt_data.get("merchant") or "Unknown Merchant"
        confidence = float(receipt_data.get("confidence", 0.95))
        
        # Categorize receipt based on merchant or explicit category
        explicit_cat = receipt_data.get("category")
        if explicit_cat and explicit_cat in TransactionCategory._value2member_map_:
            category = TransactionCategory(explicit_cat)
        else:
            category = SMSParser.categorize_transaction(merchant, str(receipt_data.get("items", [])))

        receipt_id = receipt_data.get("receipt_id", f"rcpt_{int(ts.timestamp())}")
        txn_id = f"tx_rcpt_{abs(hash(receipt_id)) % 1000000:06d}_{int(ts.timestamp())}"

        txn = Transaction(
            transaction_id=txn_id,
            user_id=user_id,
            account_id=receipt_data.get("account_id", "acc_primary"),
            amount=amount,
            currency=receipt_data.get("currency", "INR"),
            type=TransactionType.DEBIT,
            category=category,
            description=f"Receipt: {merchant}",
            timestamp=ts,
            source="receipt",
            confidence=confidence,
            is_recurring=False,
        )

        unique_event_id = event_id or f"evt_rcpt_{abs(hash(receipt_id)) % 1000000:06d}_{int(ts.timestamp())}"

        return FinancialEvent(
            event_id=unique_event_id,
            user_id=user_id,
            event_type="transaction_created",
            timestamp=ts,
            source="receipt",
            confidence=confidence,
            payload={"raw_receipt": receipt_data},
            transaction=txn,
        )

    @staticmethod
    def normalize_csv_row(
        user_id: str,
        row: Dict[str, Any],
        column_mapping: Optional[Dict[str, str]] = None,
        event_id: Optional[str] = None,
    ) -> FinancialEvent:
        """
        Normalizes a single CSV tabular row into a canonical FinancialEvent.
        """
        mapping = column_mapping or {
            "date": "date",
            "description": "description",
            "amount": "amount",
            "type": "type",
            "account": "account_id",
            "category": "category",
        }

        # Resolve field values
        def get_val(key_canonical: str, default: Any = None) -> Any:
            mapped_key = mapping.get(key_canonical, key_canonical)
            return row.get(mapped_key, row.get(key_canonical, default))

        date_val = get_val("date")
        parsed_dt = None
        if isinstance(date_val, str):
            parsed_dt = SMSParser.parse_date(date_val)
        if parsed_dt is None:
            parsed_dt = datetime.now(timezone.utc)

        raw_amount = get_val("amount", 0.0)
        amount = float(str(raw_amount).replace(",", "").replace("INR", "").replace("Rs.", "").strip())

        raw_type = str(get_val("type", "debit")).lower()
        if "credit" in raw_type or "cr" == raw_type:
            txn_type = TransactionType.CREDIT
        else:
            txn_type = TransactionType.DEBIT

        description = str(get_val("description", "Bank CSV Transaction")).strip()
        account_id = str(get_val("account", "acc_primary")).strip()
        
        raw_cat = get_val("category")
        if raw_cat and str(raw_cat).lower() in TransactionCategory._value2member_map_:
            category = TransactionCategory(str(raw_cat).lower())
        else:
            category = SMSParser.categorize_transaction(description, description)

        txn_id = f"tx_csv_{abs(hash(f'{parsed_dt.isoformat()}_{amount}_{description}')) % 1000000:06d}_{int(parsed_dt.timestamp())}"

        txn = Transaction(
            transaction_id=txn_id,
            user_id=user_id,
            account_id=account_id if account_id.startswith("acc_") else f"acc_{account_id}",
            amount=abs(amount),
            currency="INR",
            type=txn_type,
            category=category,
            description=description,
            timestamp=parsed_dt,
            source="csv",
            confidence=0.98,
            is_recurring=SMSParser.check_recurring(description),
        )

        unique_event_id = event_id or f"evt_csv_{abs(hash(txn_id)) % 1000000:06d}_{int(parsed_dt.timestamp())}"

        return FinancialEvent(
            event_id=unique_event_id,
            user_id=user_id,
            event_type="transaction_created",
            timestamp=parsed_dt,
            source="csv",
            confidence=0.98,
            payload={"raw_csv_row": row},
            transaction=txn,
        )

    @staticmethod
    def normalize_manual(
        user_id: str,
        transaction_data: Dict[str, Any],
        event_id: Optional[str] = None,
    ) -> FinancialEvent:
        """
        Normalizes a user manual transaction input with authoritative 1.0 confidence.
        """
        now = datetime.now(timezone.utc)
        raw_ts = transaction_data.get("timestamp")
        if isinstance(raw_ts, str):
            try:
                ts = datetime.fromisoformat(raw_ts.replace("Z", "+00:00"))
            except ValueError:
                ts = now
        elif isinstance(raw_ts, datetime):
            ts = raw_ts
        else:
            ts = now

        amount = float(transaction_data["amount"])
        raw_type = str(transaction_data.get("type", "debit")).lower()
        txn_type = TransactionType.CREDIT if "credit" in raw_type else TransactionType.DEBIT

        cat_str = str(transaction_data.get("category", "other")).lower()
        category = TransactionCategory(cat_str) if cat_str in TransactionCategory._value2member_map_ else TransactionCategory.OTHER

        txn_id = transaction_data.get("transaction_id") or f"tx_man_{abs(hash(str(transaction_data))) % 1000000:06d}_{int(ts.timestamp())}"

        txn = Transaction(
            transaction_id=txn_id,
            user_id=user_id,
            account_id=transaction_data.get("account_id", "acc_primary"),
            amount=amount,
            currency=transaction_data.get("currency", "INR"),
            type=txn_type,
            category=category,
            description=transaction_data.get("description", "Manual Entry"),
            timestamp=ts,
            source="manual",
            confidence=1.0,
            is_recurring=bool(transaction_data.get("is_recurring", False)),
        )

        unique_event_id = event_id or f"evt_man_{abs(hash(txn_id)) % 1000000:06d}_{int(ts.timestamp())}"

        return FinancialEvent(
            event_id=unique_event_id,
            user_id=user_id,
            event_type="transaction_created",
            timestamp=ts,
            source="manual",
            confidence=1.0,
            payload={"manual_input": transaction_data},
            transaction=txn,
        )

    @classmethod
    def normalize_batch(
        cls,
        user_id: str,
        items: List[Dict[str, Any]],
    ) -> List[FinancialEvent]:
        """
        Normalizes a list of heterogeneous raw input items.
        """
        events: List[FinancialEvent] = []
        for item in items:
            source = item.get("source", "unknown")
            if source == "sms" and "raw_text" in item:
                events.append(cls.normalize_sms(user_id, item["raw_text"]))
            elif source == "receipt":
                events.append(cls.normalize_receipt(user_id, item))
            elif source == "csv":
                events.append(cls.normalize_csv_row(user_id, item))
            elif source == "manual":
                events.append(cls.normalize_manual(user_id, item))
            else:
                events.append(cls.normalize_transaction_dict(user_id, item))
        return events

