# HogarLimpio — Agent Guide

## Stack

- **Frontend:** Nuxt 4 + Vue 3 + TailwindCSS (`@nuxtjs/tailwindcss`)
- **Backend:** FastAPI (single `main.py`) + Firebase Auth + Firestore
- **Roles:** `admin`, `cliente`, `personal_limpieza`

## Quick start

```sh
# Backend (Python)
cd backend
.venv\Scripts\activate          # Windows
pip install fastapi uvicorn firebase-admin python-multipart pydantic[email]
fastapi dev main.py             # http://localhost:8000

# Frontend (Nuxt)
cd frontend
npm install
npm run dev                     # http://localhost:3000
```

## Architecture notes

- **Backend is monolithic** — all routes live in `backend/main.py`. The `routers/`, `services/`, `repositories/`, `models/` dirs are stale/empty and are **not used** by `main.py`.
- **CORS** only allows `http://localhost:3000`.
- **Auth flow:** Firebase Auth SDK client-side → send token to backend via `Authorization: Bearer <token>` → backend verifies with Firebase Admin SDK → reads custom claims for role.
- **Service lifecycle:** `personal_limpieza` creates a service (status `Pendiente`) → `admin` approves/rejects → status changes to `Aprobado`/`Rechazado`. Editing title or price resets to `Pendiente`.

## Important gotchas

- **`backend/.env` is NOT an env file** — it's the backend `.gitignore` content (misnamed). Ignore it.
- Firebase env vars for frontend go in `frontend/.env` with `NUXT_PUBLIC_FIREBASE_*` prefix (used in `nuxt.config.ts`).
- Firebase Admin SDK credential JSON (`hogarlimpio-dffeb-firebase-adminsdk-fbsvc-a0be160afb.json`) lives in `backend/`. It's gitignored.
- **No linter, formatter, typechecker, or tests** configured in this repo.
- Token storage is **inconsistent**: admin dashboard reads from `localStorage('auth_token')`, cleaner dashboard uses `useAuth().getToken()`. Both work.
- Admin creation helper: edit credentials in `backend/create_admin.py` and run it.
