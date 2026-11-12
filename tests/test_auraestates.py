"""
Test Suite for Aura Estates (Case 09)
Verifies:
1. Mortgage & financial amortization calculations
2. ReportLab PDF brochure generation
3. Residences catalog structure and status
4. FastAPI web routes (/health, /api/residences, /api/calculator/mortgage, /api/showing/book)
5. Bot dispatcher and interactive keyboard handlers
"""
import pytest
from fastapi.testclient import TestClient

import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
for mod in list(sys.modules.keys()):
    if mod.startswith("api") or mod.startswith("bot"):
        sys.modules.pop(mod, None)
if str(PROJECT_ROOT) in sys.path:
    sys.path.remove(str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT))

from api.server import (
    app,
    RESIDENCES_DATA,
    compute_mortgage,
    generate_pdf_brochure
)
from bot.bot import dp, get_residences_keyboard

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["app"] == "AuraEstates"


def test_mortgage_calculation_logic():
    # $10,000,000 price, 30% down, 20 years, 4.5% annual rate
    calc = compute_mortgage(price=10000000.0, down_pct=30.0, term_years=20, annual_rate=4.5)
    assert calc["down_payment"] == 3000000.0
    assert calc["principal"] == 7000000.0
    # Expected monthly ~ $44,288
    assert 40000 < calc["monthly_payment"] < 50000
    assert calc["cap_rate_pct"] == 6.8
    assert calc["annual_rental_yield"] == 680000.0


def test_reportlab_pdf_brochure():
    pdf_bytes = generate_pdf_brochure("Penthouse Sky Villa")
    assert len(pdf_bytes) > 1000
    # PDF magic signature
    assert pdf_bytes.startswith(b'%PDF-')


def test_residences_data_integrity():
    assert len(RESIDENCES_DATA) >= 4
    for r in RESIDENCES_DATA:
        assert r["price"] > 1000000
        assert r["sqm"] > 100
        assert r["status"] in ["Available", "Reserved", "Sold"]
        assert len(r["features"]) >= 3


def test_api_calculator_mortgage_route():
    payload = {
        "price": 12500000,
        "down_payment_pct": 30,
        "term_years": 20,
        "annual_rate": 4.5
    }
    response = client.post("/api/calculator/mortgage", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["principal"] == 8750000.0
    assert data["monthly_payment"] > 50000


def test_api_showing_book_route():
    payload = {
        "name": "Alexandre de Rothschild",
        "phone": "+971 50 123 4567",
        "residence": "penthouse"
    }
    response = client.post("/api/showing/book", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["lead"]["alert_forward"] == "@Idrisov_prod"


def test_bot_dispatcher_and_keyboards():
    assert dp is not None
    assert len(dp.message.handlers) >= 3

    kb = get_residences_keyboard()
    assert len(kb.inline_keyboard) == len(RESIDENCES_DATA)
