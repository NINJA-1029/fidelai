# Ingestion Pipeline and Data Normalization

## 1. Scope

The Ingestion layer (`backend/ingestion/`) is responsible for receiving unstructured or semi-structured raw financial artifacts, extracting relevant dimensions, assigning confidence scores, and generating standardized `FinancialEvent` and `Transaction` instances.

---

## 2. Supported Ingestion Channels

### 1. SMS Bank Notifications
- Input: Raw transactional SMS strings from Indian financial institutions (e.g. HDFC, ICICI, SBI, Axis).
- Regex and Pattern Extraction:
  - Amount and Currency (e.g. `INR 12,000.00`, `Rs. 12000`)
  - Transaction Type (`debited` -> `debit`, `credited` -> `credit`)
  - Account reference (`A/C XX4102`)
  - Merchant/Payee description (`Care Diagnostics`, `Swiggy`, `Amazon`)
  - Confidence calculation: Based on completeness of regex field captures.

### 2. Receipt OCR / Line Item Data
- Input: JSON representing digitized merchant receipts.
- Extraction: Merchant name, total amount, line item breakdown, category assignment.

### 3. Bank CSV / Open Banking Feed
- Input: Tabular transaction rows.
- Normalization: Column mapping to canonical `Transaction` fields, duplicate hash detection based on `(timestamp, amount, description, account_id)`.

### 4. Manual Transaction Entry
- Input: Flutter form submission.
- Confidence: Fixed at `1.0` (direct user input).

---

## 3. Data Extraction and Provenance Rules

- No Fabrication: If a merchant name or category cannot be deduced with high confidence, set `category = TransactionCategory.OTHER` and mark `confidence < 0.70`.
- Immutability of Raw Text: Always store the raw SMS or receipt string inside `FinancialEvent.payload` for auditability and explainability.
