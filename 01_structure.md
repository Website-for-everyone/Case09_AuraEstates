# АРХИТЕКТУРА И СПЕЦИФИКАЦИЯ ПРОЕКТА: Aura Estates

> **Проект:** Aura Estates (Case 09) — Элитная недвижимость (Quiet Luxury, Liquid Glass & Concierge Bot)  
> **Клиент / Заказчик:** Ultra-High-Net-Worth Real Estate Agency / Портфолио Даниэля Идрисова (@Idrisov_prod)  
> **Чек проекта:** 250 000 ₽ | **Срок:** 10 дней (Дедлайн: 2026-11-20)  
> **Дедлайн MVP (80%):** 2026-11-16  
> **Тип договора:** Договор СМЗ с ИП/ООО (Чек «Мой Налог»)

---

## 🛠 Технологический стек
- **Frontend / UI:** Vanilla JS, CSS3 Liquid Glass & Frosted Glassmorphism, Champagne Gold (#D4AF37), Alabaster (#F5F2EB), Deep Obsidian (#0A0B0D), SVG Floor Plans, Video Flyover Overlays
- **Backend & Logic:** Python 3.12, FastAPI, Uvicorn, ReportLab (PDF Brochure Generator), Financial Mortgage Math
- **Telegram Bot:** Aiogram 3.x, VIP Concierge Bot, PDF Prospectus Delivery, Showing Scheduler
- **Автоматизация & Интеграции:** Direct VIP Lead Forwarding to @Idrisov_prod, Automated PDF Brochure Export
- **Тестирование:** Pytest, Unit & Smoke Tests

---

## 🏛 Архитектурная схема
```
[ Клиент / Инвестор ] ──► [ Liquid Glass Web Showcase ] ──► [ Interactive Floor Plan & View Filter ]
         │                                                      │
         ▼                                                      ▼
[ Mortgage & Yield Calc ] ──► [ FastAPI Backend ] ◄──────────► [ PDF Brochure Engine (ReportLab) ]
                                     │
                                     ▼
                [ VIP Concierge Bot (Aiogram 3.x) ] ──► [ Alert to @Idrisov_prod ]
```

---

## 🔐 Переменные окружения (.env.example)
```env
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
WEB_HOST=0.0.0.0
WEB_PORT=8009
OWNER_TG_ID=1387913438
ENVIRONMENT=production
```

---

## 🔗 Ресурсы и ссылки
- **Репозиторий GitHub:** https://github.com/Website-for-everyone/Case09_AuraEstates
- **Dev-сервер / Preview URL:** http://localhost:8009
- **Чат проекта в Telegram:** @Idrisov_prod
