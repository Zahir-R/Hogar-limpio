import firebase_admin
from firebase_admin import credentials, auth, firestore
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

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


class ServiceSchema(BaseModel):
    titulo: str
    descripcion: str
    precio: float
    categoria: str
    ofertante_id: str
    estado: str = Field(default="Pendiente")
    created_at: Optional[datetime] = None


class ServiceUpdateSchema(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    categoria: Optional[str] = None


class AdminValidationBody(BaseModel):
    estado: str


def _get_servicio_document(servicio_id: str):
    servicio_ref = db.collection("servicios").document(servicio_id)
    servicio_doc = servicio_ref.get()
    if not servicio_doc.exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Servicio no encontrado")
    servicio = servicio_doc.to_dict()
    servicio["id"] = servicio_doc.id
    return servicio_ref, servicio


@app.post("/api/servicios/registrar")
async def registrar_servicio(data: ServiceSchema, user: dict = Depends(require_role("personal_limpieza"))):
    # SPEC: Si se registra -> estado forzado a Pendiente y created_at con timestamp de servidor
    try:
        servicio_data = data.dict()
        servicio_data["estado"] = "Pendiente"
        servicio_data["ofertante_id"] = user.get("uid")
        servicio_data["created_at"] = firestore.SERVER_TIMESTAMP

        nuevo_ref = db.collection("servicios").document()
        nuevo_ref.set(servicio_data)

        return {"status": "success", "id": nuevo_ref.id, "message": "Servicio registrado en estado Pendiente"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/api/servicios/mis-servicios")
async def listar_mis_servicios(user: dict = Depends(require_role("personal_limpieza"))):
    # SPEC: Obtener solo servicios del ofertante actual
    ofertante_id = user.get("uid")
    docs = db.collection("servicios").where("ofertante_id", "==", ofertante_id).stream()
    servicios = []
    for doc in docs:
        item = doc.to_dict()
        item["id"] = doc.id
        servicios.append(item)
    return servicios


@app.put("/api/servicios/{servicio_id}")
async def editar_servicio(servicio_id: str, data: ServiceUpdateSchema, user: dict = Depends(require_role("personal_limpieza"))):
    # SPEC: Si se edita titulo o precio -> estado vuelve a Pendiente
    servicio_ref, servicio = _get_servicio_document(servicio_id)

    if servicio.get("ofertante_id") != user.get("uid"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado para editar este servicio")

    if not any([data.titulo, data.descripcion, data.precio, data.categoria]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Al menos un campo debe ser actualizado")

    actualizacion = {}
    if data.titulo is not None and data.titulo != servicio.get("titulo"):
        actualizacion["titulo"] = data.titulo
        actualizacion["estado"] = "Pendiente"
    if data.precio is not None and data.precio != servicio.get("precio"):
        actualizacion["precio"] = data.precio
        actualizacion["estado"] = "Pendiente"
    if data.descripcion is not None:
        actualizacion["descripcion"] = data.descripcion
    if data.categoria is not None:
        actualizacion["categoria"] = data.categoria

    servicio_ref.update(actualizacion)

    return {"status": "success", "message": "Servicio actualizado", "updated_fields": actualizacion}


@app.delete("/api/servicios/{servicio_id}")
async def eliminar_servicio(servicio_id: str, user: dict = Depends(require_role("personal_limpieza"))):
    servicio_ref, servicio = _get_servicio_document(servicio_id)

    if servicio.get("ofertante_id") != user.get("uid"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado para eliminar este servicio")

    servicio_ref.delete()
    return {"status": "success", "message": "Servicio eliminado"}


@app.get("/api/admin/servicios/pendientes")
async def servicios_pendientes(admin: dict = Depends(require_role("admin"))):
    # SPEC: El admin solo ve servicios con estado Pendiente
    docs = db.collection("servicios").where("estado", "==", "Pendiente").stream()
    pendientes = []
    for doc in docs:
        item = doc.to_dict()
        item["id"] = doc.id
        pendientes.append(item)
    return pendientes


@app.patch("/api/admin/servicios/{servicio_id}/validar")
async def validar_servicio(servicio_id: str, data: AdminValidationBody, admin: dict = Depends(require_role("admin"))):
    # SPEC: El admin puede validar solo con Aprobado o Rechazado
    estado_validado = data.estado.strip().title()
    if estado_validado not in ["Aprobado", "Rechazado"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Estado de validación inválido")

    servicio_ref, servicio = _get_servicio_document(servicio_id)
    servicio_ref.update({"estado": estado_validado})

    return {"status": "success", "id": servicio_id, "estado": estado_validado}
