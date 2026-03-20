import firebase_admin
from firebase_admin import credentials, auth, firestore
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.user_service import UserService
from pydantic import BaseModel
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List

class RoleUpdateBody(BaseModel):
    new_role: str

cred = credentials.Certificate("hogarlimpio-dffeb-firebase-adminsdk-fbsvc-a0be160afb.json")
firebase_admin.initialize_app(cred)

user_service = UserService()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

security = HTTPBearer()

async def get_current_user(res: HTTPAuthorizationCredentials = Depends(security)):
    token = res.credentials
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

def require_role(required_role: str):
    def role_checker(user: dict = Depends(get_current_user)):
        user_role = user.get("role")
        if user_role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User does not have the required role: {required_role}"
            )
        return user
    return role_checker

@app.get("/users/me")
async def read_user_me(user: dict = Depends(get_current_user)):
    return {"uid": user["uid"], "email": user.get("email"), "role": user.get("role")}

@app.get("/cleaners/dashboard")
async def cleaners_dashboard(user: dict = Depends(require_role("personal_limpieza"))):
    return {"message": "Welcome, cleaning staff!"}

@app.get("/cliente/profile")
async def client_profile(user: dict = Depends(require_role("cliente"))):
    return {"message": "Your client profile"}

@app.get("/")
def home():
    return {"message": "Public Hello World"}

@app.get("/admin/users")
async def list_users():
    db = firestore.client()
    users_ref = db.collection("users")
    users = users_ref.stream()
    result = []
    for user in users:
        user_data = user.to_dict()
        user_data["uid"] = user.id
        user_data.pop("created_at", None)
        result.append(user_data)
    return result

# RUTA PARA ELIMINAR USUARIO (Admin solamente)
# Quitamos el admin: dict = Depends(require_role("admin"))
@app.delete("/admin/users/{uid}")
async def delete_user(uid: str): 
    try:
        # 1. Eliminar de Firebase Auth (esto borra el login)
        auth.delete_user(uid)
        
        # 2. Eliminar de Firestore (esto borra los datos de la tabla)
        db = firestore.client()
        db.collection("users").document(uid).delete()
        
        return {"message": "Usuario eliminado correctamente"}
    except Exception as e:
        # Si sale error aquí, lo veremos en la terminal de Python
        print(f"Error en Python: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# Modelo para recibir los datos del frontend
class UserSignup(BaseModel):
    email: str
    password: str
    displayName: str
    role: str

@app.post("/users/signup-sync")
async def sync_user(data: UserSignup):
    try:
        # 1. Crear usuario en Firebase Auth
        user = auth.create_user(
            email=data.email,
            password=data.password,
            display_name=data.displayName
        )

        # 2. Guardar el ROL en Custom Claims (para seguridad)
        auth.set_custom_user_claims(user.uid, {"role": data.role})

        # 3. Guardar información adicional en Firestore
        db = firestore.client()
        db.collection("users").document(user.uid).set({
            "displayName": data.displayName,
            "email": data.email,
            "role": data.role,
            "created_at": firestore.SERVER_TIMESTAMP,
            "status": "active"
        })

        return {"status": "success", "uid": user.uid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/admin/users/{uid}/role")
async def update_user_role(uid: str, body: RoleUpdateBody, admin: dict = Depends(require_role("admin"))):
    user_service.update_user_role(uid, body.new_role)
    return {"message": f"User role updated to {body.new_role}"}

class Trabajador(BaseModel):
    id: str
    nombre: str
    precio: float
    calificacion: float
    zona: str

# RUTA PARA EL DASHBOARD DEL TRABAJADOR
@app.get("/api/cleaner/jobs")
async def get_cleaner_jobs(user: dict = Depends(require_role("personal_limpieza"))):
    # Aquí consultarías Firestore buscando trabajos asignados al UID de Brayan
    return [
        {
            "id": "job_101",
            "hora": "09:00",
            "tipo": "Limpieza Profunda Residencial",
            "direccion": "Calle de la Luna, 45. Edificio Ámbar, 4B",
            "cliente": "Elena Rodriguez",
            "estado": "en_curso"
        }
    ]

# RUTA PARA FINALIZAR TRABAJO
@app.post("/api/cleaner/complete/{job_id}")
async def complete_job(job_id: str, user: dict = Depends(require_role("personal_limpieza"))):
    # Lógica para cambiar estado en la DB y liberar pago
    return {"status": "success", "message": f"Trabajo {job_id} finalizado"}