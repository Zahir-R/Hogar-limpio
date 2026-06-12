# HogarLimpio — Agent Guide

## Stack

- **Frontend:** Nuxt 4 + Vue 3 + TailwindCSS (`@nuxtjs/tailwindcss`)
- **Backend:** FastAPI + Firebase Auth + Firestore
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

### Required env vars

Copy `backend/.env.example` → name doesn't matter (backend reads from env directly).
Copy `frontend/.env.example` → `frontend/.env` and fill in your Firebase values.

## Architecture notes

### Backend (3-layer)

The backend follows a strict 3-layer architecture:

```
routers/    → HTTP layer: parse request, call service, return response (thin)
services/   → Business logic: validation, state machines, calculations
repositories/ → Data access: Firestore queries, collection CRUD
```

- **`main.py`** (~60 lines) — app factory: Firebase init, CORS, static mount, `include_router` for all routers, seed data.
- **`shared/firebase.py`** — singleton Firebase init, exports `db` client.
- **`shared/auth.py`** — `get_current_user` and `require_role` dependencies.
- **`models/schemas.py`** — all Pydantic request/response models.
- **Routers** (11 files): `auth`, `admin`, `services`, `workers`, `zones`, `pricing`, `bookings`, `reviews`, `documents`, `availability`, `cleaner`.
- **Services** (9 files): `user`, `service`, `booking`, `review`, `pricing`, `zone`, `availability`, `worker`, `document`.
- **Repositories** (8 files): `user`, `service`, `zone`, `booking`, `review`, `payment`, `availability`, `pricing`.

### General notes

- **CORS** reads from `CORS_ORIGINS` env var (defaults to `http://localhost:3000`).
- **Auth flow:** Firebase Auth SDK client-side → send token to backend via `Authorization: Bearer <token>` → backend verifies with Firebase Admin SDK → reads custom claims for role.
- **Service lifecycle:** `personal_limpieza` creates a service (status `Pendiente`) → `admin` approves/rejects → status changes to `Aprobado`/`Rechazado`. Editing title or price resets to `Pendiente`.

## Important gotchas

- **`backend/.env` is NOT an env file** — it's the backend `.gitignore` content (misnamed). Ignore it.
- Firebase env vars for frontend go in `frontend/.env` with `NUXT_PUBLIC_FIREBASE_*` prefix (used in `nuxt.config.ts`).
- Firebase Admin SDK credential JSON (`hogarlimpio-dffeb-firebase-adminsdk-fbsvc-a0be160afb.json`) lives in `backend/`. It's gitignored. In production, set the `FIREBASE_CREDENTIALS_JSON` env var with the full JSON content.
- **No linter, formatter, typechecker, or tests** configured in this repo.
- Token storage is **inconsistent**: admin dashboard reads from `localStorage('auth_token')`, cleaner dashboard uses `useAuth().getToken()`. Both work.
- Admin creation helper: edit credentials in `backend/create_admin.py` and run it. Supports both `make_admin(email, display_name, password)` and `make_admin_by_uid(uid)`.
