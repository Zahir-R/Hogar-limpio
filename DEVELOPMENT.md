# Hogar Limpio — Development Plan

## Role

You are an expert full-stack developer implementing Hogar Limpio, a cleaning services platform built with FastAPI (Python 3.14) + Firebase Auth/Firestore + Nuxt 4 + Vue 3 + TailwindCSS. You have read and write access to all files.

---

## Instructions

- Read the relevant files before making changes
- Follow patterns already established in the codebase
- After each block, update `SDD.md` to mark features as done and note any spec changes
- Run `npm run build` in `frontend/` after each frontend change to verify no errors
- Run `python -c "import ast; ast.parse(open('main.py', encoding='utf-8').read())"` in `backend/` after each backend change to verify syntax
- Keep `AGENTS.md` updated with any new gotchas discovered during implementation

---

## Steps — Implementation order

### Block 0 — Bug fixes (done)

| # | What | Files changed |
|---|------|---------------|
| 0a | Admin delete user missing auth header | `admin/dashboard.vue` |
| 0b | Signup flow missing client-side login | `signup.vue`, `useAuth.ts`, `login.vue` |
| 0c | Unify token storage (all use `useAuth().getToken()` with localStorage fallback) | `useAuth.ts`, `login.vue`, `admin/dashboard.vue` |

---

### Block 2a — Backend: extend user profile

Add fields to `users/{uid}` for `personal_limpieza`:
```
profile_photo_url: string,
zona: string,
experiencia_anios: number,
tipo_perfil: "independiente" | "dedicado",
rating_avg: number (default 0.0),
rating_count: number (default 0),
documents_verified: bool (default false)
```

Endpoints:
- `GET /api/users/profile` — requires Bearer, returns caller's full Firestore doc
- `PUT /api/users/profile` — requires Bearer, partial update of caller's `users/{uid}` doc

Pydantic model for profile update:
```python
class ProfileUpdate(BaseModel):
    displayName: Optional[str] = None
    profile_photo_url: Optional[str] = None
    zona: Optional[str] = None
    experiencia_anios: Optional[int] = None
    tipo_perfil: Optional[str] = None  # "independiente" | "dedicado"
```

---

### Block 2b — Frontend: worker profile page

Depends on: 2a, 3a

- New route `/cleaner/profile`
- Form fields: displayName, profile_photo_url, zona (dropdown from `GET /api/zonas`), experiencia_anios, tipo_perfil (radio: independiente/dedicado)
- Load from `GET /api/users/profile` on mount, save via `PUT /api/users/profile`
- Sidebar link "Mi Perfil" in cleaner dashboard
- Show `documents_verified` badge (wired in Block 9)

---

### Block 3a — Backend: zones CRUD

- Firestore collection `zonas/{id}`: `{ nombre: string, surcharge: float, active: bool }`
- On server startup, if collection empty, seed: San Roque (0.0), Central (0.0), Zona Sur (0.05)
- `GET /api/zonas` — public, returns active only (`.where("active", "==", True)`)
- `GET /api/admin/zonas` — admin, returns all
- `POST /api/admin/zonas` — admin, body `{ nombre, surcharge, active }`
- `PUT /api/admin/zonas/{id}` — admin, partial update
- `DELETE /api/admin/zonas/{id}` — admin, soft-delete (`active = False`)

---

### Block 3b — Frontend: admin zones tab

Depends on: 3a

- Add "Zonas" tab button to admin sidebar + inline nav
- Table: Nombre, Surcharge (%), Active (toggle switch)
- "Add Zone" button at top, inline edit on click, delete button per row
- Load from `GET /api/admin/zonas`, save via `POST/PUT`

---

### Block 4a — Backend: worker listing

Depends on: 2a, 3a

- `GET /api/workers` — requires `cliente` or `admin`. Query `users` where `role == "personal_limpieza"`. Optional `?zona=X` filter. Return: `uid, displayName, email, profile_photo_url, zona, experiencia_anios, tipo_perfil, rating_avg, rating_count, documents_verified`
- `GET /api/workers/{uid}/profile` — requires auth. Returns single worker full profile + their approved servicios (query `servicios` where `ofertante_id == uid AND estado == "Aprobado"`)

---

### Block 4b — Frontend: client browse workers

Depends on: 4a

- Replace hardcoded `trabajadores` array in `client-dashboard.vue` with real data from `GET /api/workers`
- Zone filter dropdown populated from `GET /api/zonas`
- Worker card displays: photo (or initial fallback), name, zone, experiencia_anios, star rating, verification badge
- Wire "Agendar" button as placeholder (connects in Block 7)

---

### Block 5a — Backend: pricing engine

- Firestore single doc `config/pricing`:
  ```json
  { "base_rate": 30, "room_rate": 15, "sqm_rate": 0.5, "zone_surcharge_enabled": true, "currency": "BOB" }
  ```
- `GET /api/pricing` — public, returns config
- `PUT /api/admin/pricing` — admin, updates config
- Function `calcular_precio(rooms: int, sqm: float, zona: str) -> float`:
  ```
  total = base_rate + (rooms * room_rate) + (sqm * sqm_rate)
  if zone_surcharge_enabled:
      lookup zona surcharge from zonas collection
      total *= (1 + surcharge)
  return round(total, 2)
  ```
- `POST /api/pricing/calcular` — requires auth. Body `{ rooms, sqm, zona }`. Returns `{ precio_total }`.

---

### Block 5b — Frontend: admin pricing form

Depends on: 5a

- Add "Precios" tab to admin dashboard
- Form with number inputs: Base Rate, Room Rate, SQM Rate, Zone Surcharge toggle
- Load from `GET /api/pricing`, save via `PUT /api/admin/pricing`

---

### Block 6a — Backend: availability

Depends on: 2a

- `availability_templates/{worker_uid}` (single doc):
  ```json
  {
    "weekdays": {
      "monday": [{ "start": "09:00", "end": "12:00" }, { "start": "14:00", "end": "17:00" }],
      "tuesday": [],
      ...
    },
    "timezone": "America/La_Paz"
  }
  ```
- `availability/{worker_uid}/overrides/{date}`: `{ date: "2026-06-15", active: bool }`
- `GET /api/availability/{worker_uid}` — requires auth. Returns expanded slots for next 14 days (template minus override-inactive dates)
- `PUT /api/availability` — requires `personal_limpieza`. Replaces caller's template
- `POST /api/availability/toggle` — requires `personal_limpieza`. Body `{ date, active }`. Creates/updates override

---

### Block 6b — Frontend: availability editor

Depends on: 6a

- New route `/cleaner/availability`, sidebar link "Disponibilidad"
- Weekly grid: 7 columns (Mon-Sun), each with ordered time slot list. Each slot has start/end time pickers
- "Add slot" / "Remove" buttons per day
- Load from `GET /api/availability/{uid}` on mount, save via `PUT /api/availability`
- Date override section: date picker + active/inactive toggle

---

### Block 7a — Backend: booking lifecycle

Depends on: 4a, 5a, 6a

- Firestore `reservas/{id}`:
  ```json
  {
    "cliente_uid": string,
    "worker_uid": string,
    "servicio_id": string,
    "fecha": Timestamp,
    "hora_inicio": string,
    "duracion_horas": 2,
    "direccion": string,
    "zona": string,
    "precio_total": float,
    "estado": "Pendiente" | "Confirmado" | "En_curso" | "Completado" | "Cancelado",
    "recurrencia": "none" | "semanal" | "quincenal",
    "created_at": Timestamp,
    "completed_at": Timestamp | null
  }
  ```
- State machine: Pendiente -> Confirmado -> En_curso -> Completado. Any state -> Cancelado.
- `POST /api/reservas` — requires `cliente`. Body `{ worker_uid, servicio_id, fecha, hora_inicio, direccion, zona }`. Auto-calls `calcular_precio()`. Estado = Pendiente.
- `GET /api/reservas` — requires auth. If `cliente`, return own. If `personal_limpieza`, return assigned. If `admin`, return all.
- `PATCH /api/reservas/{id}/confirmar` — requires `personal_limpieza`. Estado must be Pendiente.
- `PATCH /api/reservas/{id}/completar` — requires `cliente`. Estado must be En_curso.
- `PATCH /api/reservas/{id}/cancelar` — requires auth (must be involved party). Any estado.
- Each transition validates current estado; reject with 400 if invalid.

---

### Block 7b — Frontend: booking form

Depends on: 7a, 6a

- Booking modal/route triggered from client "Agendar" button (Block 4b)
- Fields: worker (pre-filled), date (date picker, only available dates from Block 6a), time slot (from available), address, recurrence (none/weekly/biweekly)
- Price preview section: calls `POST /api/pricing/calcular` with rooms + sqm inputs
- Submit: `POST /api/reservas`. Redirect to `/client/bookings` on success

---

### Block 7c — Frontend: booking dashboards

Depends on: 7a

- New route `/client/bookings` — table with columns: Worker, Service, Date, Time, Address, Price, Status. Cancel button (Pendiente/Confirmado only). Complete button (En_curso only).
- Cleaner dashboard — "Reservas" section below "Mis Servicios". Shows assigned reservations with Confirm button.
- Admin dashboard — "Reservas" tab read-only table of all reservations.

---

### Block 8a — Backend: reviews

Depends on: 7a

- `reviews/{id}`: `{ servicio_id, worker_uid, client_uid, rating (1-5), comment, created_at }`
- `POST /api/reviews` — requires `cliente`. Validates client has a completed reserva with this worker. On success, update `users/{worker_uid}.rating_avg` and `.rating_count`.
- `GET /api/reviews/{worker_uid}` — requires auth. Returns list of reviews.

---

### Block 8b — Frontend: review UI

Depends on: 8a

- After client clicks "Completar", show star rating modal (1-5 clickable stars + optional comment)
- Worker profile shows rating_avg as stars + rating_count
- On booking detail: if Completado and no review yet, show "Leave review" button

---

### Block 9a — Backend: Escudo document upload

Depends on: 2a

- Firebase Storage path: `documents/{uid}/{tipo}_{timestamp}.{ext}`
- `users/{uid}/documents/{id}` subcollection:
  ```json
  {
    "tipo": "ci_front" | "ci_back" | "felcc" | "domicilio",
    "file_url": string,
    "verified": false,
    "verified_at": null,
    "verified_by": null,
    "expires_at": Timestamp,
    "created_at": Timestamp
  }
  ```
- `POST /api/workers/documents/upload` — requires `personal_limpieza`. Multipart: tipo (string), file (binary), expires_at (ISO date string).
- `GET /api/workers/documents` — list caller's docs
- `GET /api/admin/workers/documents/pending` — admin, unverified docs
- `PATCH /api/admin/workers/documents/{id}` — admin, body `{ verified: bool }`. If all 4 types verified, set `users/{worker_uid}.documents_verified = true`.
- Requires `firebase-admin` storage import.

---

### Block 9b — Frontend: document upload UI

Depends on: 9a

- "Documentos" section on `/cleaner/profile` page
- 4 rows: CI front, CI back, FELCC, Domicilio. Each with: upload file input, status badge (Verificado/Pendiente/Rechazado), expiry date if verified

---

### Block 9c — Frontend: admin Escudo panel

Depends on: 9a

- "Escudo" tab in admin dashboard
- Table: Worker name, Document type, Upload date, Expiry date. Actions: Verify, Reject.
- Click row to see all documents for that worker

---

### Block 10a — Backend: payment stub

Depends on: 7a

- `payments/{id}`: `{ reserva_id, cliente_uid, worker_uid, monto, comision (monto * 0.10), metodo: "qr", estado, created_at, released_at }`
- Auto-triggered by booking state:
  - Confirmado -> create payment `Retenido`
  - Completado -> set `Liberado`, `released_at`
  - Cancelado -> set `Reembolsado`
- `GET /api/payments/{reserva_id}` — caller must be involved or admin
- `GET /api/admin/payments` — admin, all payments

---

### Block 10b — Frontend: payment display

Depends on: 10a

- Client booking detail: payment row (amount, commission, status badge)
- Admin "Pagos" tab: table of all payments (Booking ID, Client, Worker, Amount, Commission, Status, Created, Released)

---

## End Goal

A fully functional platform where:
- Clients browse verified workers by zone, book with calculated pricing, pay digitally, and leave reviews
- Workers manage availability, receive bookings, upload verification documents, and get paid
- Admins validate services, review documents, configure zones/pricing, and oversee all transactions

---

## Nuances

### Repository structure
- Backend is monolithic `main.py` — do NOT create separate files in `routers/`, `services/`, `repositories/`, `models/` dirs
- All new Pydantic models and route handlers go in `backend/main.py`

### Auth & tokens
- Auth flow: Firebase SDK client-side -> Bearer token -> Admin SDK verifies -> custom claims for role
- Token storage: `useAuth().getToken()` is canonical. Falls back to `localStorage.getItem('auth_token')` if Firebase session not yet restored on hard refresh
- Both `useAuth().login()` and `useAuth().signup()` store the token in localStorage automatically

### Backend execution
- Run: `python -m fastapi dev main.py` from `backend/` directory (NOT `fastapi.exe` directly — that has hardcoded stale paths)
- CORS only allows `http://localhost:3000`
- File is UTF-8 (accented Spanish text). Python imports read it as UTF-8. If you use `open()` directly, always pass `encoding='utf-8'`

### Virtual environment
- Use `venv\` (Windows — has `Scripts\`), NOT `.venv\` (Unix-style with `bin/`)
- Activate: `venv\Scripts\activate`

### Configuration files
- `frontend/.env` has Firebase vars with `NUXT_PUBLIC_FIREBASE_*` prefix (consumed by `nuxt.config.ts`)
- `backend/.env` is a misnamed `.gitignore` — ignore it
- Firebase Admin SDK credential JSON (`hogarlimpio-dffeb-firebase-adminsdk-fbsvc-a0be160afb.json`) lives in `backend/` and is gitignored
- `backend/create_admin.py` is a standalone helper to bootstrap an admin user

### SDD management
- After each block implementation:
  1. Update `SDD.md` §8 (roadmap) to mark block as Done
  2. Update `SDD.md` Appendix B (feature mapping) status
  3. If implementation diverged from spec, update the relevant section to match what was built

### No tooling
- No linters, formatters, typecheckers, or tests are configured
- Verification is manual: build frontend with `npm run build`, check backend syntax with `ast.parse()`, then test manually via browser at `http://localhost:3000`
