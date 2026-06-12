import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from shared.firebase import db
from routers import (
    auth, admin, services, workers, zones, pricing,
    bookings, reviews, documents, availability, cleaner
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Hogar Limpio API")

origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(services.router)
app.include_router(workers.router)
app.include_router(zones.router)
app.include_router(pricing.router)
app.include_router(bookings.router)
app.include_router(reviews.router)
app.include_router(documents.router)
app.include_router(availability.router)
app.include_router(cleaner.router)


@app.on_event("startup")
def seed_data():
    zonas_ref = db.collection("zonas")
    if not any(zonas_ref.limit(1).stream()):
        zonas_ref.add({"nombre": "San Roque", "surcharge": 0.0, "active": True})
        zonas_ref.add({"nombre": "Central", "surcharge": 0.05, "active": True})
        zonas_ref.add({"nombre": "Zona Sur", "surcharge": 0.10, "active": True})

    pricing_ref = db.collection("config").document("pricing")
    if not pricing_ref.get().exists:
        pricing_ref.set({
            "base_rate": 30, "room_rate": 15, "sqm_rate": 0.5,
            "zone_surcharge_enabled": True, "currency": "BOB"
        })

    users_ref = db.collection("users")
    for doc in users_ref.stream():
        data = doc.to_dict()
        updates = {}
        if "profile_photo_url" not in data:
            updates["profile_photo_url"] = ""
        if "zona" not in data:
            updates["zona"] = ""
        if "experiencia_anios" not in data:
            updates["experiencia_anios"] = 0
        if "tipo_perfil" not in data:
            updates["tipo_perfil"] = "independiente"
        if "rating_avg" not in data:
            updates["rating_avg"] = 0.0
        if "rating_count" not in data:
            updates["rating_count"] = 0
        if "documents_verified" not in data:
            updates["documents_verified"] = False
        if updates:
            doc.reference.update(updates)

    logger.info("Seed data complete")


@app.get("/")
def home():
    return {"message": "Hogar Limpio API Running"}


@app.get("/health")
def health():
    return {"status": "healthy"}
