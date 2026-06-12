from fastapi import APIRouter, Depends
from models.schemas import CrearReserva, ReservaAction
from services.booking_service import BookingService
from shared.auth import get_current_user, require_role

router = APIRouter(tags=["bookings"])
booking_service = BookingService()


@router.post("/api/reservas")
async def crear_reserva(data: CrearReserva, current_user: dict = Depends(require_role("cliente"))):
    return booking_service.create(current_user["uid"], data)


@router.get("/api/reservas")
async def list_reservas(current_user: dict = Depends(get_current_user)):
    return booking_service.list(current_user["uid"], current_user.get("role"))


@router.patch("/api/reservas/{reserva_id}/confirmar")
async def confirmar_reserva(reserva_id: str, current_user: dict = Depends(require_role("personal_limpieza"))):
    return booking_service.confirm(reserva_id, current_user["uid"])


@router.patch("/api/reservas/{reserva_id}/completar")
async def completar_reserva(reserva_id: str, current_user: dict = Depends(require_role("cliente"))):
    return booking_service.complete(reserva_id, current_user["uid"])


@router.patch("/api/reservas/{reserva_id}/cancelar")
async def cancelar_reserva(reserva_id: str, current_user: dict = Depends(get_current_user)):
    return booking_service.cancel(reserva_id, current_user)


@router.post("/api/payments/initiate")
async def initiate_payment(data: ReservaAction, current_user: dict = Depends(require_role("cliente"))):
    from firebase_admin import firestore
    from shared.firebase import db
    doc_ref = db.collection("payments").add({
        "cliente_uid": current_user["uid"],
        "monto": 0, "comision": 0, "estado": "Pendiente",
        "created_at": firestore.SERVER_TIMESTAMP
    })
    return {"status": "success", "id": doc_ref[1].id}


@router.get("/api/admin/payments")
async def list_payments(admin: dict = Depends(require_role("admin"))):
    from repositories.payment_repo import PaymentRepository
    return PaymentRepository().list_all()


@router.get("/api/payments/{reserva_id}")
async def get_payment(reserva_id: str, current_user: dict = Depends(get_current_user)):
    return booking_service.get_payment(reserva_id, current_user)
