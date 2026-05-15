"""Invoice persistence layer. Backed by Postgres via SQLAlchemy."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Invoice:
    id: str
    customer_id: str
    amount_cents: int
    currency: str
    status: str


class InvoiceStore:
    def __init__(self, db_url: str):
        self.db_url = db_url

    def get(self, invoice_id: str) -> Optional[dict]:
        # SQL elided for brevity; real implementation queries Postgres.
        raise NotImplementedError

    def create(self, payload: dict) -> dict:
        raise NotImplementedError
