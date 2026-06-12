from typing import Optional
from fastapi import APIRouter, Depends
from services.worker_service import WorkerService
from shared.auth import get_current_user

router = APIRouter(tags=["workers"])
worker_service = WorkerService()


@router.get("/api/workers")
async def list_workers(zona: Optional[str] = None, current_user: dict = Depends(get_current_user)):
    return worker_service.list(zona, current_user)


@router.get("/api/workers/{uid}/profile")
async def get_worker_profile(uid: str, current_user: dict = Depends(get_current_user)):
    return worker_service.get_profile(uid)
