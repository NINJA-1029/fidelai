from datetime import datetime
from typing import Any, Dict, Optional
from shared.contracts.contracts import FinancialEvent, Transaction
from backend.ingestion.sms_parser import SMSParser


class FinancialEventNormalizer:
    """
    Normalizes arbitrary incoming financial payloads into canonical FinancialEvent and Transaction instances.
    """

    @staticmethod
    def normalize_sms(user_id: str, raw_sms: str, event_id: Optional[str] = None) -> FinancialEvent:
        transaction = SMSParser.parse_sms(raw_sms, user_id=user_id)
        
        return FinancialEvent(
            event_id=event_id or f"evt_sms_{int(datetime.utcnow().timestamp())}",
            user_id=user_id,
            event_type="transaction_created",
            timestamp=datetime.utcnow(),
            source="sms",
            confidence=transaction.confidence if transaction else 0.4,
            payload={"raw_sms": raw_sms},
            transaction=transaction
        )

    @staticmethod
    def normalize_transaction_dict(user_id: str, data: Dict[str, Any], event_id: Optional[str] = None) -> FinancialEvent:
        txn = Transaction(**data)
        return FinancialEvent(
            event_id=event_id or f"evt_txn_{int(datetime.utcnow().timestamp())}",
            user_id=user_id,
            event_type="transaction_created",
            timestamp=txn.timestamp,
            source=txn.source,
            confidence=txn.confidence,
            payload={"raw_transaction": data},
            transaction=txn
        )
