from fastapi import APIRouter, Depends
from models.schemas import PricingConfig, PricingPreview
from services.pricing_service import PricingService
from shared.auth import get_current_user, require_role

router = APIRouter(tags=["pricing"])
pricing_service = PricingService()


@router.get("/api/pricing")
async def get_pricing():
    return pricing_service.get_config()


@router.put("/api/admin/pricing")
async def update_pricing(data: PricingConfig, admin: dict = Depends(require_role("admin"))):
    return pricing_service.update_config(admin["uid"], data)


@router.post("/api/pricing/calcular")
async def preview_pricing(data: PricingPreview, current_user: dict = Depends(get_current_user)):
    total = pricing_service.calculate(data.rooms, data.sqm, data.zona)
    return {
        "total": total,
        "currency": "BOB",
        "breakdown": {"rooms": data.rooms, "sqm": data.sqm, "zona": data.zona}
    }
