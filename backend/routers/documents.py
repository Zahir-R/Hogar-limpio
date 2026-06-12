from fastapi import APIRouter, Depends, UploadFile, File, Form
from models.schemas import DocumentVerify
from services.document_service import DocumentService
from shared.auth import require_role

router = APIRouter(tags=["documents"])
document_service = DocumentService()


@router.post("/api/workers/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    tipo: str = Form(...),
    expires_at: str = Form(""),
    current_user: dict = Depends(require_role("personal_limpieza"))
):
    return await document_service.upload(current_user["uid"], file, tipo, expires_at)


@router.get("/api/workers/documents")
async def list_documents(current_user: dict = Depends(require_role("personal_limpieza"))):
    return document_service.list_mine(current_user["uid"])


@router.get("/api/admin/workers/documents/pending")
async def pending_documents(admin: dict = Depends(require_role("admin"))):
    return document_service.list_pending()


@router.patch("/api/admin/workers/documents/{doc_id}")
async def verify_document(doc_id: str, data: DocumentVerify, admin: dict = Depends(require_role("admin"))):
    return document_service.verify(doc_id, data.worker_uid, admin["uid"], data.verified)
