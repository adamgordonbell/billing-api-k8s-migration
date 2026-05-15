"""Flask entry point for billing-api."""

import os

from flask import Flask, jsonify, request

from billing_api import __version__
from billing_api.invoices import InvoiceStore

app = Flask(__name__)
store = InvoiceStore(os.environ["BILLING_DB_URL"])


@app.get("/health")
def health():
    return jsonify(status="ok", version=__version__)


@app.get("/invoices/<invoice_id>")
def get_invoice(invoice_id: str):
    invoice = store.get(invoice_id)
    if invoice is None:
        return jsonify(error="not_found"), 404
    return jsonify(invoice)


@app.post("/invoices")
def create_invoice():
    payload = request.get_json(force=True)
    invoice = store.create(payload)
    return jsonify(invoice), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
