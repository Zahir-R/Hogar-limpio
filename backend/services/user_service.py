import base64
import mimetypes
from fastapi import HTTPException, UploadFile
from firebase_admin import auth, firestore, _auth_utils
from repositories.user_repo import UserRepository
from repositories.service_repo import ServiceRepository


class UserService:
    def __init__(self):
        self.repo = UserRepository()
        self.service_repo = ServiceRepository()

    def sync_user(self, data):
        try:
            try:
                user = auth.create_user(
                    email=data.email,
                    password=data.password,
                    display_name=data.displayName
                )
            except _auth_utils.EmailAlreadyExistsError:
                user = auth.get_user_by_email(data.email)

            auth.set_custom_user_claims(user.uid, {"role": data.role})

            self.repo.set(user.uid, {
                "displayName": data.displayName,
                "email": data.email,
                "role": data.role,
                "created_at": firestore.SERVER_TIMESTAMP,
                "status": "active"
            })

            if data.role == "personal_limpieza":
                exists = self.service_repo.exists(
                    "ofertante_id", user.uid, "titulo", "Limpieza básica"
                )
                if not exists:
                    self.service_repo.create({
                        "titulo": "Limpieza básica",
                        "descripcion": "Servicio estándar de limpieza general",
                        "precio": 0,
                        "categoria": "General",
                        "ofertante_id": user.uid,
                        "estado": "Aprobado",
                        "created_at": firestore.SERVER_TIMESTAMP
                    })

            return {"status": "success", "uid": user.uid}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_profile(self, uid):
        profile = self.repo.get(uid)
        if not profile:
            raise HTTPException(status_code=404, detail="User not found")
        return profile

    def update_profile(self, uid, data):
        updates = {k: v for k, v in data.model_dump().items() if v is not None}
        if not updates:
            raise HTTPException(status_code=400, detail="No fields to update")
        self.repo.update(uid, updates)
        return {"status": "success", "updated": list(updates.keys())}

    async def upload_photo(self, uid, file: UploadFile):
        content = await file.read()
        mime = file.content_type or mimetypes.guess_type(file.filename or "")[0] or "image/jpeg"
        b64 = base64.b64encode(content).decode("utf-8")
        data_url = f"data:{mime};base64,{b64}"
        self.repo.update(uid, {"profile_photo_url": data_url})
        return {"status": "success", "url": data_url}

    def list_users(self):
        return self.repo.list_all()

    def admin_update(self, uid, data):
        try:
            auth.update_user(uid, display_name=data.new_name)
            auth.set_custom_user_claims(uid, {"role": data.new_role})
            self.repo.update(uid, {
                "role": data.new_role,
                "displayName": data.new_name
            })
            return {"status": "success"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def admin_delete(self, uid):
        try:
            auth.delete_user(uid)
            self.repo.delete(uid)
            return {"message": "Usuario eliminado correctamente"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
