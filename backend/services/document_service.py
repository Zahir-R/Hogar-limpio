import base64
import uuid
from fastapi import HTTPException, UploadFile
from firebase_admin import firestore
from repositories.user_repo import UserRepository


class DocumentService:
    def __init__(self):
        self.user_repo = UserRepository()

    async def upload(self, worker_uid, file: UploadFile, tipo: str, expires_at: str):
        content = await file.read()
        mime = file.content_type or "application/octet-stream"
        b64 = base64.b64encode(content).decode("utf-8")
        data_url = f"data:{mime};base64,{b64}"

        doc_ref = self.user_repo.add_to_subcollection(worker_uid, "documents", {
            "tipo": tipo,
            "file_url": data_url,
            "verified": False,
            "verified_at": None,
            "verified_by": None,
            "expires_at": expires_at,
            "created_at": firestore.SERVER_TIMESTAMP
        })
        return {"status": "success", "id": doc_ref[1].id, "filename": f"{tipo}_{uuid.uuid4().hex}"}

    def list_mine(self, worker_uid):
        docs = self.user_repo.get_subcollection(worker_uid, "documents")
        result = []
        for doc in docs:
            item = doc.to_dict()
            item["id"] = doc.id
            result.append(item)
        return result

    def list_pending(self):
        workers = self.user_repo.stream_all_with_role("personal_limpieza")
        result = []
        for worker in workers:
            docs = self.user_repo.get_subcollection(worker.id, "documents")
            for doc in docs:
                item = doc.to_dict()
                item["id"] = doc.id
                item["worker_uid"] = worker.id
                if not item.get("verified"):
                    result.append(item)
        return result

    def verify(self, doc_id, worker_uid, admin_uid, verified):
        doc = self.user_repo.get_subcollection_doc(worker_uid, "documents", doc_id)
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Document not found")

        self.user_repo.update(
            worker_uid,
            {"documents_verified": False}
        )

        doc_ref = doc.reference
        doc_ref.update({
            "verified": verified,
            "verified_at": firestore.SERVER_TIMESTAMP,
            "verified_by": admin_uid
        })

        all_docs = self.user_repo.get_subcollection(worker_uid, "documents")
        all_verified = all(d.to_dict().get("verified", False) for d in all_docs)
        self.user_repo.update(worker_uid, {"documents_verified": all_verified})

        return {"status": "success", "documents_verified": all_verified}
