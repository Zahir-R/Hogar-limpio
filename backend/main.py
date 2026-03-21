import firebase_admin
from firebase_admin import credentials, auth, firestore
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional

# 1. CONFIGURACIÓN DE FIREBASE (ORDEN CORRECTO)
# Primero cargamos las credenciales
cred = credentials.Certificate("hogarlimpio-dffeb-firebase-adminsdk-fbsvc-a0be160afb.json")

# Segundo inicializamos la app
firebase_admin.initialize_app(cred)

# Tercero creamos el cliente de la base de datos
db = firestore.client()

# 2. MODELOS DE DATOS (PYDANTIC)
class RoleUpdateBody(BaseModel):
    new_role: str

class UserSignup(BaseModel):
    email: str
    password: str
    displayName: str
    role: str

class UserUpdate(BaseModel):
    new_name: str
    new_role: str

# 3. CONFIGURACIÓN DE FASTAPI
app = FastAPI(title="Hogar Limpio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

security = HTTPBearer()

# 4. DEPENDENCIAS DE SEGURIDAD
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

# 5. RUTAS PÚBLICAS Y DE USUARIO
@app.get("/")
def home():
    return {"message": "Hogar Limpio API Running"}

@app.post("/users/signup-sync")
async def sync_user(data: UserSignup):
    try:
        # Crear en Auth
        user = auth.create_user(
            email=data.email,
            password=data.password,
            display_name=data.displayName
        )
        # Asignar Rol en Claims
        auth.set_custom_user_claims(user.uid, {"role": data.role})
        # Guardar en Firestore
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

@app.get("/users/me")
async def read_user_me(user: dict = Depends(get_current_user)):
    return {"uid": user["uid"], "email": user.get("email"), "role": user.get("role")}

# 6. RUTAS DE ADMINISTRADOR
@app.get("/admin/users")
async def list_users(admin: dict = Depends(require_role("admin"))):
    users_ref = db.collection("users")
    docs = users_ref.stream()
    result = []
    for doc in docs:
        user_data = doc.to_dict()
        user_data["uid"] = doc.id
        user_data.pop("created_at", None)
        result.append(user_data)
    return result

@app.post("/admin/users/{uid}/update")
async def update_user(uid: str, data: UserUpdate, admin=Depends(require_role("admin"))):
    try:
        # 1. Actualizar en Firebase Auth (Nombre)
        auth.update_user(uid, display_name=data.new_name)
        
        # 2. Actualizar Rol en Custom Claims
        auth.set_custom_user_claims(uid, {"role": data.new_role})
        
        # 3. Actualizar en Firestore (Ambos)
        db.collection("users").document(uid).update({
            "role": data.new_role,
            "displayName": data.new_name
        })
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/admin/users/{uid}")
async def delete_user(uid: str, admin: dict = Depends(require_role("admin"))): 
    try:
        auth.delete_user(uid)
        db.collection("users").document(uid).delete()
        return {"message": "Usuario eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 7. RUTAS DE TRABAJADOR (CLEANER)
@app.get("/api/cleaner/jobs")
async def get_cleaner_jobs(user: dict = Depends(require_role("personal_limpieza"))):
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

@app.post("/api/cleaner/complete/{job_id}")
async def complete_job(job_id: str, user: dict = Depends(require_role("personal_limpieza"))):
    return {"status": "success", "message": f"Trabajo {job_id} finalizado"}