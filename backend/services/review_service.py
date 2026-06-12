from fastapi import HTTPException, status
from firebase_admin import firestore
from repositories.review_repo import ReviewRepository
from repositories.booking_repo import BookingRepository
from repositories.user_repo import UserRepository


class ReviewService:
    def __init__(self):
        self.repo = ReviewRepository()
        self.booking_repo = BookingRepository()
        self.user_repo = UserRepository()

    def create(self, cliente_uid, data):
        if data.rating < 1 or data.rating > 5:
            raise HTTPException(status_code=400, detail="Rating must be 1-5")

        reservas = self.booking_repo.find_completed(cliente_uid, data.worker_uid)
        found = any(True for _ in reservas)
        if not found:
            raise HTTPException(
                status_code=400,
                detail="No completed reservation found for this service"
            )

        review_ref = self.repo.create({
            "servicio_id": data.servicio_id,
            "worker_uid": data.worker_uid,
            "client_uid": cliente_uid,
            "rating": data.rating,
            "comment": data.comment,
            "created_at": firestore.SERVER_TIMESTAMP
        })

        user_data = self.user_repo.get(data.worker_uid)
        if user_data:
            count = user_data.get("rating_count", 0)
            avg = user_data.get("rating_avg", 0.0)
            new_count = count + 1
            new_avg = round(((avg * count) + data.rating) / new_count, 2)
            self.user_repo.update(data.worker_uid, {
                "rating_count": new_count,
                "rating_avg": new_avg
            })

        return {"status": "success", "id": review_ref[1].id}

    def list_by_worker(self, worker_uid):
        return self.repo.list_by_worker(worker_uid)
