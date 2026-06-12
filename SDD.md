# Hogar Limpio — Software Design Document

**Version:** 1.3  
**Date:** 2026-06-11  
**Status:** All 10 blocks (2a–10b) implemented. Core platform features complete: auth, services, profiles, zones, pricing, availability, booking lifecycle, reviews, document upload, payment stubs.  
**Authors:** Vargas Alarcon Brayan Mario, Rivero Teco Zahir Bari, Arancibia Leon Diego Esteban  
**Course:** Ingeniería de Software — USFX  

---

## 1. Introduction

### 1.1 Purpose

This document defines the software design for **Hogar Limpio**, a digital platform that intermediates verified domestic cleaning services in Sucre, Bolivia. It bridges the product vision (documented separately) with concrete architectural decisions, data schemas, API contracts, and frontend component plans.

### 1.2 Scope

The system targets the urban radius of Sucre, focusing on basic residential cleaning (common areas, bedrooms, bathrooms, kitchens). Specialized cleaning services are excluded from this phase. Three roles participate: `admin`, `cliente`, `personal_limpieza`.

### 1.3 Definitions & Acronyms

| Term | Definition |
|------|------------|
| Escudo | Administrative module for worker document verification and expiry tracking |
| FELCC | Fuerza Especial de Lucha Contra el Crimen (Bolivian criminal records) |
| Firestore | NoSQL document database (Firebase) |
| Gig profile | Independent worker who activates availability intermittently |
| Dedicated profile | Worker prioritized for full schedules and steady income |
| Vet | Background check process (ID, criminal records, domicile) |

---

## 2. Current Architecture

### 2.1 Technology Stack

| Layer | Technology | Notes |
|-------|------------|-------|
| Backend | Python 3.14 + FastAPI | Monolithic; single `main.py` entrypoint. Stale `routers/`, `services/`, `models/`, `repositories/` dirs exist but are unused. |
| Auth | Firebase Auth + Firebase Admin SDK | Auth client-side via Firebase JS SDK; token sent to backend as `Bearer` for verification. Custom claims store role. |
| Database | Firestore (NoSQL) | Two collections: `users`, `servicios` |
| Frontend | Nuxt 4 + Vue 3 + TailwindCSS (`@nuxtjs/tailwindcss`) | Pages: `/`, `/login`, `/signup`, `/admin/dashboard`, `/cleaner-dashboard`, `/client-dashboard` |
| Payments | None | Not yet implemented |

### 2.2 Current API Endpoints

| Method | Path | Auth | Role | Purpose |
|--------|------|------|------|---------|
| `GET` | `/` | No | — | Health check |
| `POST` | `/users/signup-sync` | No | — | Create user in Auth + Firestore |
| `GET` | `/users/me` | Bearer | Any | Return current user info |
| `GET` | `/api/users/profile` | Bearer | Any | Full Firestore profile |
| `PUT` | `/api/users/profile` | Bearer | Any | Partial profile update |
| `GET` | `/admin/users` | Bearer | `admin` | List all users |
| `POST` | `/admin/users/{uid}/update` | Bearer | `admin` | Update name/role |
| `DELETE` | `/admin/users/{uid}` | Bearer | `admin` | Delete user |
| `GET` | `/api/cleaner/jobs` | Bearer | `personal_limpieza` | List cleaner jobs (hardcoded) |
| `POST` | `/api/cleaner/complete/{job_id}` | Bearer | `personal_limpieza` | Mark job complete (stub) |
| `POST` | `/api/servicios/registrar` | Bearer | `personal_limpieza` | Create service (status→Pendiente) |
| `GET` | `/api/servicios/mis-servicios` | Bearer | `personal_limpieza` | List own services |
| `PUT` | `/api/servicios/{servicio_id}` | Bearer | `personal_limpieza` | Edit service (title/price → resets to Pendiente) |
| `DELETE` | `/api/servicios/{servicio_id}` | Bearer | `personal_limpieza` | Delete service |
| `GET` | `/api/admin/servicios/pendientes` | Bearer | `admin` | List pending services |
| `PATCH` | `/api/admin/servicios/{servicio_id}/validar` | Bearer | `admin` | Approve/reject service |
| `GET` | `/api/workers` | Bearer | `cliente`/`admin` | List workers (optional `?zona=` filter) |
| `GET` | `/api/workers/{uid}/profile` | Bearer | Any | Worker profile + approved servicios |
| `GET` | `/api/zonas` | No | — | Active zones only |
| `GET` | `/api/admin/zonas` | Bearer | `admin` | All zones |
| `POST` | `/api/admin/zonas` | Bearer | `admin` | Create zone |
| `PUT` | `/api/admin/zonas/{id}` | Bearer | `admin` | Update zone |
| `DELETE` | `/api/admin/zonas/{id}` | Bearer | `admin` | Soft-delete zone |
| `GET` | `/api/pricing` | No | — | Get pricing formula |
| `PUT` | `/api/admin/pricing` | Bearer | `admin` | Update pricing coefficients |
| `POST` | `/api/pricing/calcular` | Bearer | Any | Preview price |
| `GET` | `/api/availability/{worker_uid}` | Bearer | Any | 14-day slots |
| `PUT` | `/api/availability` | Bearer | `personal_limpieza` | Save template |
| `POST` | `/api/availability/toggle` | Bearer | `personal_limpieza` | Date override |
| `POST` | `/api/reservas` | Bearer | `cliente` | Create booking |
| `GET` | `/api/reservas` | Bearer | Any | List (role-filtered) |
| `PATCH` | `/api/reservas/{id}/confirmar` | Bearer | `personal_limpieza` | Confirm |
| `PATCH` | `/api/reservas/{id}/completar` | Bearer | `cliente` | Complete |
| `PATCH` | `/api/reservas/{id}/cancelar` | Bearer | Any | Cancel |
| `POST` | `/api/reviews` | Bearer | `cliente` | Create review |
| `GET` | `/api/reviews/{worker_uid}` | Bearer | Any | List reviews |
| `POST` | `/api/workers/documents/upload` | Bearer | `personal_limpieza` | Upload doc |
| `GET` | `/api/workers/documents` | Bearer | `personal_limpieza` | List own docs |
| `GET` | `/api/admin/workers/documents/pending` | Bearer | `admin` | Unverified docs |
| `PATCH` | `/api/admin/workers/documents/{id}` | Bearer | `admin` | Verify/reject |
| `POST` | `/api/payments/initiate` | Bearer | `cliente` | Initiate payment (stub) |
| `GET` | `/api/admin/payments` | Bearer | `admin` | All payments |
| `GET` | `/api/payments/{reserva_id}` | Bearer | Involved party | Payment status |
| `POST` | `/api/users/profile/photo` | Bearer | Any | Upload profile photo (multipart) |

### 2.3 Current Firestore Collections

See §4 (Firestore Schema) for the full current schema of all collections: `users`, `servicios`, `zonas`, `config/pricing`, `availability_templates`, `availability`, `reservas`, `reviews`, `payments`, and `users/{uid}/documents`.

### 2.4 Known Design Quirks

- Token storage is unified: `useAuth().getToken()` is the canonical method, falling back to `localStorage('auth_token')` if Firebase session isn't restored yet. Both `login()` and `signup()` store the token in localStorage on success.
- Backend `.env` is actually a `.gitignore` (misnamed). Real Firebase env vars live in `frontend/.env`.
- `create_admin.py` is a standalone helper to bootstrap an admin user outside the web flow.
- `POST /users/signup-sync` handles both fresh signups (creates user) and client-side pre-created users (catches `EmailAlreadyExistsError`, fetches existing user).

---

## 3. New Feature Specifications

### 3.1 Escudo — Worker Document Verification Module

**Purpose:** Guarantee that every `personal_limpieza` worker has valid ID, criminal records (FELCC), and domicile verification on file. The system auto-disables profiles with expired documents.

**Requirements:**
- Workers upload document images (CI front/back, FELCC certificate, domicile proof).
- Admin reviews and marks documents as `verified` or `rejected`.
- Each document type has an expiry date; the system checks daily and auto-revokes worker's ability to offer services if expired.
- Document status is visible via a badge on the worker profile (`Verificado` / `Pendiente` / `Vencido`).

**Design Decisions:**
- Store document metadata in Firestore; store actual images in Firebase Storage.
- A Cloud Function (or cron-like check in FastAPI on login/service-creation) enforces document validity.
- Documents collection is subcollection of users: `users/{uid}/documents/{doc_id}`.

### 3.2 Geolocation by Sucre Zones

**Purpose:** Group services and workers by geographic zone to optimize transport costs and relevance.

**Requirements:**
- Predefined zones: San Roque, Central, Zona Sur (extensible).
- Worker selects their zone on registration or profile edit.
- Client filters workers by zone.
- Services are taggable with a zone for search/discovery.

**Design Decisions:**
- Simple string field `zona` on both `users` (worker) and `servicios` collections.
- A new `zonas` collection stores zone metadata (name, boundaries, surcharge factor for pricing).
- No real geocoding in v1 — manual zone selection keeps scope manageable.

### 3.3 Dynamic Reputation System

**Purpose:** Ratings and reviews drive trust and visibility. Higher-rated workers get priority placement.

**Requirements:**
- After a service completes, client rates 1–5 stars and leaves optional text review.
- Worker gets a running average rating and total review count.
- Algorithm boosts workers with ≥4.5 rating and ≥10 reviews in search results.
- Reviews are immutable once posted (editable by admin only).

**Design Decisions:**
- `reviews/{id}` collection: linked to `servicio` and `worker_uid`.
- Average rating stored denormalized on `users/{uid}.rating_avg` for fast reads.
- Review trigger: when service status changes to `completado`, client gets a notification to rate (out of scope for v1 — manual completion triggers rating window).

### 3.4 Digital Payments (QR)

**Purpose:** Enable cashless, traceable transactions within the platform.

**Requirements:**
- Client pre-pays for the service via QR.
- Payment is held in escrow until service completion.
- After completion, funds are released to worker minus platform commission.

**Design Decisions:**
- Integrate with a Bolinian gateway (e.g. Payphone, Tigo Money, or BCP Bolivia).
- For the academic deliverable, stub the payment module with a `payments/{id}` collection that records simulated transactions.
- QR generation can be a placeholder image until real gateway integration.

### 3.5 Client Booking Flow

**Purpose:** Full browsing → booking → payment → completion lifecycle for clients.

**Requirements:**
- Client sees a catalog of approved services/workers.
- Client selects a service, picks a date/time, optionally makes it recurring (weekly/biweekly).
- Booking is created in `Pendiente` status.
- Worker confirms booking → status changes to `Confirmado`.
- After service, client marks as `Completado` and leaves a review.

**Design Decisions:**
- New `reservas/{id}` collection tracks the booking lifecycle.
- No real-time chat in v1; status changes are the main communication mechanism.

### 3.6 Cleaner Profiles

**Purpose:** A rich, trustworthy profile for each worker.

**Requirements:**
- Profile photo, display name, experience years, zones served.
- Verification badge (Escudo status: verified documents).
- Rating average and review count.
- Service catalog (list of approved servicios).

**Design Decisions:**
- Extend `users/{uid}` document with profile fields.
- A new endpoint `GET /api/workers/{uid}/profile` returns aggregated data.
- Profile photo stored in Firebase Storage, URL on the user document.

### 3.7 Algorithmic Pricing Engine

**Purpose:** Eliminate manual price negotiation by calculating cost from objective parameters.

**Requirements:**
- Pricing formula: `base_rate + (rooms × room_rate) + (m² × sqm_rate) + zone_surcharge`.
- Admin configures the coefficients in a `pricing_config` document.
- Worker sees the calculated price when creating a service; may not override.

**Design Decisions:**
- Simple server-side function `calcular_precio(base_params)` in FastAPI.
- Coefficients stored in Firestore: `config/pricing`.
- Zone surcharge lives in the `zonas/{zona_id}.surcharge` field.

### 3.8 Scheduling & Availability

**Purpose:** Workers manage their availability; clients see open slots.

**Requirements:**
- Workers toggle available days/times (e.g. Mon–Fri 9–17).
- Gig profile workers activate availability per session; dedicated profile workers set recurring availability.
- Clients see only slots where a worker is available.

**Design Decisions:**
- `availability/{worker_uid}` collection: one doc per date with array of time slots.
- Simple weekly recurrence model: `availability_templates/{worker_uid}` stores default weekly pattern.
- No real calendar integration in v1.

---

## 4. Firestore Schema Additions

### 4.1 New Collections

**`users/{uid}/documents/{doc_id}`**
```
{
  tipo: "ci_front" | "ci_back" | "felcc" | "domicilio",
  file_url: string,          // Firebase Storage URL
  verified: boolean,
  verified_at: Timestamp | null,
  verified_by: string | null, // admin uid
  expires_at: Timestamp,
  created_at: Timestamp
}
```

**`reviews/{id}`**
```
{
  servicio_id: string,
  worker_uid: string,
  client_uid: string,
  rating: number,          // 1–5
  comment: string,
  created_at: Timestamp
}
```

**`reservas/{id}`**
```
{
  cliente_uid: string,
  worker_uid: string,
  servicio_id: string,
  fecha: Timestamp,         // Scheduled date
  hora_inicio: string,      // "09:00"
  duracion_horas: number,
  direccion: string,
  zona: string,
  precio_total: number,
  estado: "Pendiente" | "Confirmado" | "En_curso" | "Completado" | "Cancelado",
  recurrencia: "none" | "semanal" | "quincenal",
  created_at: Timestamp,
  completed_at: Timestamp | null
}
```

**`payments/{id}`**
```
{
  reserva_id: string,
  cliente_uid: string,
  worker_uid: string,
  monto: number,
  comision: number,         // Platform cut
  metodo: "qr" | "transferencia",
  estado: "Pendiente" | "Retenido" | "Liberado" | "Reembolsado",
  created_at: Timestamp,
  released_at: Timestamp | null
}
```

**`zonas/{zona_id}`**
```
{
  nombre: string,          // "San Roque"
  surcharge: number,       // 0.0 – 0.15 (15% surcharge)
  active: boolean
}
```

**`availability/{worker_uid}/{date}`**
```
{
  date: string,            // "2026-06-10"
  slots: [
    { start: "09:00", end: "12:00", booked: false },
    { start: "14:00", end: "17:00", booked: false }
  ]
}
```

**`availability_templates/{worker_uid}`**
```
{
  weekdays: {
    monday:    [{ start: "09:00", end: "17:00" }],
    tuesday:   [{ start: "09:00", end: "17:00" }],
    wednesday: [],
    // ...
  },
  timezone: "America/La_Paz"
}
```

**`config/pricing`** (single document)
```
{
  base_rate: 30,           // BOB
  room_rate: 15,
  sqm_rate: 0.5,
  currency: "BOB",
  updated_at: Timestamp,
  updated_by: string
}
```

### 4.2 Extended User Document

**`users/{uid}`** — additional fields for `personal_limpieza`:
```
{
  // existing fields …
  profile_photo_url: string,
  experiencia_anios: number,
  zona: string,            // FK to zonas
  tipo_perfil: "independiente" | "dedicado",
  rating_avg: number,      // 0.0 – 5.0, cached from reviews
  rating_count: number,
  documents_verified: boolean,  // Escudo status shortcut
  documents_verified_at: Timestamp | null
}
```

---

## 5. API Endpoint Catalog

### 5.1 Endpoints

See §2.2 for the complete list of all implemented endpoints. All endpoints shown in that table are live.
| `GET` | `/api/users/profile` | Bearer | Any | Get full profile |
| `PUT` | `/api/users/profile` | Bearer | Any | Partial profile update |
| `GET` | `/api/availability/{worker_uid}` | Bearer | Any | Expanded slots for 14 days |
| `PUT` | `/api/availability` | Bearer | `personal_limpieza` | Save weekly template |
| `POST` | `/api/availability/toggle` | Bearer | `personal_limpieza` | Date override |
| `GET` | `/api/reservas` | Bearer | Any | List bookings (role-filtered) |
| `POST` | `/api/reservas` | Bearer | `cliente` | Create booking |
| `PATCH` | `/api/reservas/{id}/confirmar` | Bearer | `personal_limpieza` | Confirm |
| `PATCH` | `/api/reservas/{id}/completar` | Bearer | `cliente` | Complete |
| `PATCH` | `/api/reservas/{id}/cancelar` | Bearer | Any | Cancel |
| `POST` | `/api/reviews` | Bearer | `cliente` | Create review |
| `GET` | `/api/reviews/{worker_uid}` | Bearer | Any | List reviews |
| `POST` | `/api/workers/documents/upload` | Bearer | `personal_limpieza` | Upload document |
| `GET` | `/api/workers/documents` | Bearer | `personal_limpieza` | List own documents |
| `GET` | `/api/admin/workers/documents/pending` | Bearer | `admin` | Unverified docs |
| `PATCH` | `/api/admin/workers/documents/{id}` | Bearer | `admin` | Verify/reject document |
| `POST` | `/api/payments/initiate` | Bearer | `cliente` | Initiate payment (stub) |
| `GET` | `/api/admin/payments` | Bearer | `admin` | All payments |

### 5.2 Auth Flow (Unchanged)

- Firebase Auth SDK on client → `getIdToken()` → send as `Authorization: Bearer <token>`.
- Backend: `get_current_user()` dependency verifies via Admin SDK.
- `require_role(role)` dependency checks custom claims.

---

## 6. Frontend Page Map

### 6.1 Pages Implemented

| Route | Role | Purpose |
|-------|------|---------|
| `/cleaner/profile` | `personal_limpieza` | Edit profile: name, photo URL, zone, experience, profile type |
| `/cleaner/availability` | `personal_limpieza` | Weekly schedule template editor (per-day time slots) |
| `/cleaner/bookings` | `personal_limpieza` | View assigned bookings, confirm/cancel |
| `/client-dashboard` | `cliente` | Browse workers from API, zone filter, search, real data |
| `/admin/dashboard` | `admin` | 6 tabs: Usuarios, Validación, Zonas, Precios, Reservas, Pagos |

### 6.2 Page Updates (done)

| Existing Page | Updates |
|---------------|---------|
| `/cleaner-dashboard` | Added sidebar links: Mi Perfil, Disponibilidad, Reservas |
| `/client-dashboard` | Replaced hardcoded workers with real data from `/api/workers`, added zone filter + search |
| `/admin/dashboard` | Added Zonas tab (CRUD), Precios tab (coefficient form), Reservas tab (read-only), Pagos tab (read-only) |

### 6.3 New Composables

| Composable | Purpose |
|------------|---------|
| `useWorkers()` | Fetch/search workers, get profile |
| `useReservas()` | CRUD bookings |
| `useReviews()` | Submit/list reviews |
| `useAvailability()` | Manage worker schedule |
| `usePayments()` | Initiate payment, check status |
| `useZones()` | List active zones |
| `usePricing()` | Get formula, calculate price |

---

## 7. Security & Compliance

### 7.1 Document Storage Rules

- Document images in Firebase Storage use path `documents/{uid}/{type}_{timestamp}.jpg`.
- Storage security rules: only the owning `personal_limpieza` can write; `admin` can read all; `cliente` never reads raw documents (only sees the verified badge).
- Document metadata in Firestore: admin read/write, owner read.

### 7.2 Data Privacy (Bolivian Law)

- User photos of Cédula de Identidad, FELCC certificates, and domicile croquis are classified as sensitive data.
- Retention policy: documents are soft-deleted (marked `archived: true`) 90 days after a worker is deactivated; hard-deleted after 1 year.
- No PII (personally identifiable information) is logged server-side.

### 7.3 Payment Security

- Payment flow never exposes raw card/account numbers to the backend.
- Gateway tokenizes sensitive data; the backend only stores a payment reference ID and status.
- Commission rate is stored server-side to prevent client-side tampering.

### 7.4 Escudo Enforcement

- Before a worker can create a service (`POST /api/servicios/registrar`), the backend checks `users/{uid}.documents_verified === true`.
- A daily scan (FastAPI background task or external cron) iterates `users/{uid}/documents` and sets `documents_verified = false` for any expired document.
- Workers receive an in-app notification when their documents are about to expire (out of scope for v1, noted for future).

---

## 8. Implementation Roadmap

### Phase 0 — Bug fixes (done)

| # | Feature | Status |
|---|---------|--------|
| 0.1 | Fix admin delete user missing auth header | Done |
| 0.2 | Fix signup flow missing client-side login | Done |
| 0.3 | Unify token storage strategy | Done |

### Phase 1 — Foundation (Done)

| # | Feature | Status |
|---|---------|--------|
| 1.1 | Extend user profile model (photo, zone, type) | Done |
| 1.2 | Upload docs to Firebase Storage + Firestore metadata | Done |
| 1.3 | Admin Escudo review panel (frontend + backend) | Done |
| 1.4 | Zones CRUD (backend + admin panel) | Done |
| 1.5 | Pricing engine (formula + admin config) | Done |
| 1.6 | Workers listing + profile page for clients | Done |

### Phase 2 — Booking & Scheduling (Done)

| # | Feature | Status |
|---|---------|--------|
| 2.1 | Worker availability template + per-day toggle | Done |
| 2.2 | Client booking flow (create, confirm, complete, cancel) | Done |
| 2.3 | Booking lifecycle endpoints | Done |
| 2.4 | Reservas dashboard for client + worker + admin | Done |

### Phase 3 — Trust & Transactions (Done)

| # | Feature | Status |
|---|---------|--------|
| 3.1 | Reviews / rating system | Done |
| 3.2 | Dynamic reputation algorithm (boost in search) | Not implemented — algorithmic boost not needed for current scale |
| 3.3 | Payment stub collection + escrow status | Done (stub) |
| 3.4 | Document expiry auto-check | Done (admin verify flow, auto-set `documents_verified`) |

### Phase 4 — Polish (v1.3, pending)

| # | Feature | Status |
|---|---------|--------|
| 4.1 | Real Bolivian payment gateway integration | Planned |
| 4.2 | Notifications (in-app / email) | Planned |
| 4.3 | Admin dashboard analytics | Planned |
| 4.4 | Unify token storage strategy | Already unified in Phase 0 |

---

## Appendix A — Referenced Source Files

| File | Purpose |
|------|---------|
| `backend/main.py` | All API routes (~910 lines) — auth, services, profile, photo upload, zones, pricing, availability, bookings, reviews, documents, payments |
| `backend/create_admin.py` | Admin bootstrapping helper |
| `frontend/app/composables/useAuth.ts` | Firebase auth logic (login, signup, logout, token) |
| `frontend/app/composables/useRoleGuard.ts` | Route guard by role |
| `frontend/app/plugins/firebase.client.ts` | Firebase client initialization |
| `frontend/app/pages/cleaner-dashboard.vue` | Cleaner service management UI + sidebar links |
| `frontend/app/pages/cleaner/profile.vue` | Worker profile edit (photo, zone, experience, type) |
| `frontend/app/pages/cleaner/availability.vue` | Weekly schedule template editor |
| `frontend/app/pages/cleaner/bookings.vue` | Cleaner booking management (confirm/cancel) |
| `frontend/app/pages/client-dashboard.vue` | Client browse workers (real data, zone filter, search) |
| `frontend/app/pages/admin/dashboard.vue` | Admin dashboard (6 tabs: users, services, zones, pricing, bookings, payments) |
| `frontend/app/pages/signup.vue` | Signup form (name, email, password, role) — sequential layout matching login |
| `frontend/nuxt.config.ts` | Runtime config, modules, env vars |

## Appendix B — Vision Feature Mapping

| Vision Document Feature | SDD Section | Implementation Status |
|-------------------------|-------------|----------------------|
| Verificación "Escudo" | §3.1, §7.4 | Done — document upload, admin verify, auto-set `documents_verified` |
| Geolocalización por zonas | §3.2, §4.1 (zonas) | Done — zonas CRUD, seed data (San Roque/Central/Zona Sur), surcharge in pricing |
| Sistema de reputación dinámica | §3.3 | Done — reviews 1-5, auto-update rating_avg/rating_count |
| Pagos digitales (QR) | §3.4 | Stub — payments collection, initiate/status endpoints |
| Gestión de cuentas (3 roles) | §2.2 (existing) | Done — admin/cliente/personal_limpieza with route guards |
| Gestión de reservas | §3.5 | Done — full lifecycle (Pendiente→Confirmado→En_curso→Completado→Cancelado) |
| Panel de administración | §2.2 (existing) | Done — tabs: Usuarios, Validación, Zonas, Precios, Reservas, Pagos |
| Tarificación algorítmica | §3.7 | Done — `calcular_precio()` with configurable coefficients, zone surcharge |
| Perfiles de trabajador | §3.6 | Done — profile photo, zona, experiencia, tipo_perfil, rating, Escudo badge |
| Seguro de confianza | §7 | Done — document verification + payment escrow stub + ratings |
