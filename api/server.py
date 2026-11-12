"""
Aura Estates // FastAPI Backend & PDF Brochure Engine
Case 09 — Ultra-Luxury Real Estate Showcase & VIP Concierge
"""
import io
import math
from typing import Dict, Any, List
from pathlib import Path
from fastapi import FastAPI, Query, HTTPException, Response
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

app = FastAPI(title="Aura Estates API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent
WEB_DIR = BASE_DIR / "web"


RESIDENCES_DATA = [
    {
        "id": "penthouse",
        "name": "Penthouse Sky Villa",
        "price": 12500000,
        "price_formatted": "$12,500,000",
        "sqm": 480,
        "terrace_sqm": 110,
        "floor": "48–49 (Пентхаус)",
        "view": "180° Панорама океана",
        "status": "Available",
        "features": ["Частный инфинити-бассейн", "Личный лифт", "SPA-зона с хамамом", "Винная комната"]
    },
    {
        "id": "horizon",
        "name": "Horizon Residence",
        "price": 7800000,
        "price_formatted": "$7,800,000",
        "sqm": 310,
        "terrace_sqm": 65,
        "floor": "34 (Угловая секция)",
        "view": "Закатный скайлайн",
        "status": "Reserved",
        "features": ["Панорамное остекление 3.8м", "Мастер-блок с двумя гардеробными", "Умный дом Lutron"]
    },
    {
        "id": "duplex",
        "name": "Royal Duplex",
        "price": 9200000,
        "price_formatted": "$9,200,000",
        "sqm": 395,
        "terrace_sqm": 85,
        "floor": "22–23 (Двухуровневый)",
        "view": "Альпийские горы и залив",
        "status": "Available",
        "features": ["Второй свет высотой 7.2м", "Терраса с камином", "Кухня Bulthaup с техникой Gaggenau"]
    },
    {
        "id": "garden",
        "name": "Garden Suite",
        "price": 5400000,
        "price_formatted": "$5,400,000",
        "sqm": 240,
        "terrace_sqm": 40,
        "floor": "1 (Собственный патио)",
        "view": "Центральный парк",
        "status": "Sold",
        "features": ["Приватный сад с оранжереей", "Отдельный вход", "Зона BBQ из натурального гранита"]
    }
]


class MortgageRequest(BaseModel):
    price: float
    down_payment_pct: float = 30.0
    term_years: int = 20
    annual_rate: float = 4.5


class ShowingRequest(BaseModel):
    name: str
    phone: str
    residence: str = "penthouse"


def compute_mortgage(price: float, down_pct: float, term_years: int, annual_rate: float) -> Dict[str, Any]:
    down_payment = price * (down_pct / 100.0)
    principal = price - down_payment
    monthly_rate = (annual_rate / 100.0) / 12.0
    num_payments = term_years * 12

    if monthly_rate > 0:
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** num_payments) / (((1 + monthly_rate) ** num_payments) - 1)
    else:
        monthly_payment = principal / num_payments

    total_paid = monthly_payment * num_payments
    total_interest = max(0.0, total_paid - principal)
    cap_rate = 6.8
    annual_rental_income = price * (cap_rate / 100.0)

    return {
        "price": price,
        "down_payment": round(down_payment, 2),
        "principal": round(principal, 2),
        "monthly_payment": round(monthly_payment, 2),
        "total_interest": round(total_interest, 2),
        "total_paid": round(total_paid, 2),
        "cap_rate_pct": cap_rate,
        "annual_rental_yield": round(annual_rental_income, 2)
    }


def generate_pdf_brochure(residence_name: str) -> bytes:
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Dark background
    p.setFillColor(colors.HexColor("#0A0B0D"))
    p.rect(0, 0, width, height, fill=1, stroke=0)

    # Gold Decorative Header Frame
    p.setStrokeColor(colors.HexColor("#D4AF37"))
    p.setLineWidth(1.5)
    p.rect(36, 36, width - 72, height - 72, fill=0, stroke=1)

    # Monogram & Brand
    p.setFillColor(colors.HexColor("#D4AF37"))
    p.setFont("Helvetica-Bold", 24)
    p.drawCentredString(width / 2.0, height - 80, "AURA ESTATES")

    p.setFont("Helvetica", 10)
    p.setFillColor(colors.HexColor("#F5E6C8"))
    p.drawCentredString(width / 2.0, height - 100, "PRIVATE ARCHITECTURAL COLLECTION // DE LUXE")

    # Thin separator line
    p.setStrokeColor(colors.HexColor("#D4AF37"))
    p.setLineWidth(0.8)
    p.line(100, height - 115, width - 100, height - 115)

    # Residence Title & Price
    p.setFont("Helvetica-Bold", 20)
    p.setFillColor(colors.white)
    p.drawString(60, height - 160, residence_name.upper())

    target_res = next((r for r in RESIDENCES_DATA if r["name"].lower() == residence_name.lower()), RESIDENCES_DATA[0])

    p.setFont("Helvetica-Bold", 16)
    p.setFillColor(colors.HexColor("#D4AF37"))
    p.drawString(60, height - 190, f"ESTIMATED VALUE: {target_res['price_formatted']}")

    # Specs table
    p.setFont("Helvetica", 11)
    p.setFillColor(colors.HexColor("#E2D9CC"))
    specs = [
        f"Living Area: {target_res['sqm']} sq.m",
        f"Panoramic Terrace: {target_res['terrace_sqm']} sq.m",
        f"Floor Level: {target_res['floor']}",
        f"Horizon Orientation: {target_res['view']}",
        f"Market Status: {target_res['status']}",
    ]
    y = height - 230
    for s in specs:
        p.drawString(70, y, f"• {s}")
        y -= 22

    # Key Features
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.HexColor("#D4AF37"))
    p.drawString(60, y - 20, "ARCHITECTURAL SPECIFICATIONS:")
    y -= 45

    p.setFont("Helvetica", 10)
    p.setFillColor(colors.HexColor("#CCCCCC"))
    for feat in target_res["features"]:
        p.drawString(70, y, f"✦ {feat}")
        y -= 20

    # Concierge Contact Box
    p.setStrokeColor(colors.HexColor("#38BDF8"))
    p.setLineWidth(1)
    p.rect(60, 60, width - 120, 90, fill=0, stroke=1)

    p.setFont("Helvetica-Bold", 11)
    p.setFillColor(colors.HexColor("#38BDF8"))
    p.drawString(80, 125, "VIP CONCIERGE & PRIVATE SHOWINGS")

    p.setFont("Helvetica", 9)
    p.setFillColor(colors.HexColor("#E2D9CC"))
    p.drawString(80, 105, "Personal showings arranged with private helicopter transfer upon request.")
    p.drawString(80, 90, "Direct inquiries: @Idrisov_prod | Telegram Concierge Bot Active 24/7")
    p.drawString(80, 75, "Strict Confidentiality Guaranteed (NDA Required).")

    p.showPage()
    p.save()
    return buffer.getvalue()


@app.get("/health")
async def health_check():
    return {"status": "ok", "app": "AuraEstates", "version": "1.0.0"}


@app.get("/api/residences")
async def get_residences():
    return JSONResponse(content=RESIDENCES_DATA)


@app.post("/api/calculator/mortgage")
async def api_calculate_mortgage(req: MortgageRequest):
    result = compute_mortgage(req.price, req.down_payment_pct, req.term_years, req.annual_rate)
    return JSONResponse(content=result)


@app.get("/api/brochure/download")
async def api_download_brochure(residence: str = Query("Penthouse Sky Villa")):
    pdf_bytes = generate_pdf_brochure(residence)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=Aura_Brochure_{residence.replace(' ', '_')}.pdf"}
    )


@app.post("/api/showing/book")
async def book_showing(req: ShowingRequest):
    lead = {
        "project": "AuraEstates",
        "client_name": req.name,
        "phone": req.phone,
        "residence": req.residence,
        "status": "CONFIRMED_PENDING_VIP_CONTACT",
        "alert_forward": "@Idrisov_prod"
    }
    return JSONResponse(content={"status": "success", "lead": lead})


if WEB_DIR.exists():
    app.mount("/", StaticFiles(directory=str(WEB_DIR), html=True), name="web")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8009, reload=False)
