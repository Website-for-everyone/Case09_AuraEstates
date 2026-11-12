# Aura Estates (Case 09) — Ultra-Luxury Real Estate & VIP Concierge

> **Quiet Luxury & Liquid Glass UI • Interactive Architectural Floor Plans • Panoramic View Filter • Mortgage & Yield Engine • VIP Concierge Bot**

![Quiet Luxury](https://img.shields.io/badge/Aesthetic-Quiet%20Luxury%20%7C%20Liquid%20Glass-D4AF37?style=flat-square)
![Floor Plans](https://img.shields.io/badge/Floorplan-Interactive%20SVG-0A0B0D?style=flat-square)
![VIP Concierge](https://img.shields.io/badge/Telegram-VIP%20Concierge%20%2B%20PDF-blue?style=flat-square)

---

## 🎯 Features
1. **Quiet Luxury & Liquid Glass Visual Aesthetics:** Translucent frosted glassmorphism panels, champagne gold accents (#D4AF37), deep obsidian background (#0A0B0D), ambient cinematic drone flyover loop.
2. **Interactive Architectural Floor Plan:**
   - Multi-tier residency selector: **Penthouse Sky Villa**, **Horizon Residence**, **Royal Duplex**, **Garden Suite**.
   - Interactive SVG floor plans showing lot availability (Available / Reserved / Sold), square meters, terrace dimensions, ceiling heights, and pricing.
3. **Panoramic Window View Filter:**
   - Sort and preview penthouses by view: **Ocean Horizon**, **Sunset Skyline**, **Alpine Mountains**, **Central Park**.
4. **Mortgage & Rental Yield Calculator:**
   - Financial modeling calculating down payment, monthly amortization payment, total interest, and capitalization rate (annual rental yield ROI %).
5. **VIP Concierge Telegram Bot:**
   - Property photo showcase.
   - Dynamic custom **PDF Brochure Generator** powered by ReportLab sent directly into the user's chat.
   - Private showing tour booking with automatic lead dispatch to `@Idrisov_prod`.

---

## 🚀 Quick Start

### 1. Web & API Server
```bash
cd Case09_AuraEstates
pip install -r requirements.txt
python api/server.py
```
Open [http://localhost:8009](http://localhost:8009) in your browser.

### 2. Telegram Bot
```bash
python bot/bot.py
```

### 3. Run Tests
```bash
pytest tests/test_auraestates.py -v
```
