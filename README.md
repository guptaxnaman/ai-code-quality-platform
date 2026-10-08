# AI-Assisted Code Quality Analysis Platform

A small full-stack application for reviewing Python code. Paste code into the web app, run an analysis, and get a readable report covering common quality issues, complexity, and improvement suggestions.

Frontend and backend live in the same repository.

## Features
- React frontend
- Flask REST API
- Python AST-based analysis
- Complexity estimate
- Common issue detection
- Improvement suggestions
- PostgreSQL support through `DATABASE_URL`
- SQLite fallback for quick local setup
- Analysis history
- Input validation and error handling

## Structure
```text
ai-code-quality-platform/
├── backend/
│   ├── app.py
│   ├── analyzer.py
│   ├── database.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   └── package.json
├── .gitignore
└── README.md
```

## Run locally

### Backend
Python 3.10+ recommended.

```bash
cd backend
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

Then:
```bash
pip install -r requirements.txt
python app.py
```

API: `http://localhost:5000`

By default it uses SQLite. To use PostgreSQL, create `backend/.env` from `.env.example` and set `DATABASE_URL`.

Example:
```text
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/codequality
```

### Frontend
Open another terminal:
```bash
cd frontend
npm install
npm run dev
```

Open the URL shown by Vite, normally `http://localhost:5173`.

## API

`POST /api/analyze`
```json
{"code":"def add(a, b):\n    return a + b"}
```

`GET /api/history` returns recent saved analyses.

## Important
The application works without an external AI API. Suggestions are generated from deterministic code-analysis rules, so no API key is required. If an AI provider is added later, keep secrets in environment variables.
