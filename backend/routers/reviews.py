from fastapi import APIRouter, Depends
from models.schemas import CreateReview
from services.review_service import ReviewService
from shared.auth import get_current_user, require_role

router = APIRouter(tags=["reviews"])
review_service = ReviewService()


@router.post("/api/reviews")
async def create_review(data: CreateReview, current_user: dict = Depends(require_role("cliente"))):
    return review_service.create(current_user["uid"], data)


@router.get("/api/reviews/{worker_uid}")
async def list_reviews(worker_uid: str, current_user: dict = Depends(get_current_user)):
    return review_service.list_by_worker(worker_uid)
