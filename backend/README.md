# LM-Inspect AI - Python FastAPI Backend

FastAPI backend for **LM-Inspect AI** (Legal Metrology Compliance & AI Detection Platform).

## 🚀 Overview

This backend provides a high-performance REST API designed to support the frontend application. It implements all 11 required endpoints, provides mock inspection datasets out-of-the-box, and establishes a modular architecture ready for integrating:
- **OCR Engines**: `PaddleOCR` (multilingual high-resolution) and `PyTesseract`.
- **AI Models**: Spatial bounding box regression, Document Layout Analysis (`LayoutLMv3`), and NER declaration classification.
- **Legal Metrology Rule Engine**: Validation under the *Legal Metrology (Packaged Commodities) Rules, 2011* (Rule 6 declarations, Rule 5 Table-I numeral heights, Rule 6(11) Unit Sale Price).

---

## 📂 Architecture

```
backend/
├── app/
│   ├── main.py                  # FastAPI application entrypoint, CORS, static mounts
│   ├── config.py                # Environment settings (upload directory, CORS, ports)
│   ├── models/                  # Pydantic schemas mirroring frontend contracts
│   │   ├── common.py            # BoundingBox, RuleReference, Enums
│   │   ├── declaration.py       # DeclarationField, extract & validate models
│   │   ├── inspection.py        # Inspection, AnalyzeRequest, ComplianceResult
│   │   ├── product.py           # Product schemas
│   │   ├── violation.py         # Violation schemas
│   │   ├── dashboard.py         # DashboardStats & Analytics schemas
│   │   └── report.py            # InspectionReport (Form II statutory memo)
│   ├── api/v1/                  # REST Controllers under /api/v1
│   │   ├── images.py            # POST /images/upload (multipart image upload)
│   │   ├── inspections.py       # POST /inspections/analyze, GET /inspections/history,
│   │   │                        # GET /inspections/{id}/compliance, GET /inspections/{id}/report
│   │   ├── declarations.py      # POST /declarations/extract (OCR + AI pipeline trigger)
│   │   ├── rules.py             # POST /rules/validate (Rule Engine evaluation)
│   │   ├── violations.py        # GET /violations (query by severity, status, inspectionId)
│   │   ├── products.py          # GET /products/{id}
│   │   ├── dashboard.py         # GET /dashboard/stats
│   │   └── analytics.py         # GET /analytics/summary
│   ├── services/                # Pluggable service layer
│   │   ├── store.py             # In-memory repository with thread-safe data operations
│   │   ├── ocr_service.py       # OCR engine interface + mock & PaddleOCR/Tesseract stubs
│   │   ├── ai_model_service.py  # AI declaration extractor interface + LayoutLM stubs
│   │   ├── rule_engine.py       # Statutory Legal Metrology Rules 2011 validator
│   │   └── report_service.py    # Form II statutory inspection notice generator
│   └── data/
│       ├── lmpc_rules.py        # Statutory rules definition (Rule 6(1)(a)-(e), Rule 5, Rule 6(11))
│       └── seed_data.py         # Baseline dataset matching frontend mock
├── uploads/                     # Storage directory for uploaded product packaging images
├── requirements.txt             # Python dependencies
├── run.py                       # Server runner
└── test_api.py                  # API verification suite
```

---

## 🛠️ Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Backend Server
```bash
python run.py
```
Or with Uvicorn:
```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at:
- **Base API**: `http://localhost:8000/api/v1`
- **Swagger Documentation**: `http://localhost:8000/docs`
- **Redoc Documentation**: `http://localhost:8000/redoc`

---

## 🔗 Connecting with Frontend

To connect the existing frontend to this backend:
1. In the project root `.env` file, set:
   ```env
   VITE_API_BASE_URL=http://localhost:8000/api/v1
   VITE_USE_MOCK=false
   ```
2. Start or refresh the Vite frontend (`npm run dev`).
3. All requests (new inspection analysis, uploads, dashboard metrics, reports) will now be served live by the FastAPI backend.

---

## 🧪 Running Automated API Tests

```bash
python test_api.py
```
This tests all 11 endpoints to ensure contract adherence and payload compatibility.
