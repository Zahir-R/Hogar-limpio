import firebase_admin
from firebase_admin import credentials, auth, firestore, _auth_utils
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import os, uuid

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

class ProfileUpdate(BaseModel):
    displayName: Optional[str] = None
    profile_photo_url: Optional[str] = None
    zona: Optional[str] = None
    experiencia_anios: Optional[float] = None
    tipo_perfil: Optional[str] = None

class ZoneCreate(BaseModel):
    nombre: str
    surcharge: float = 0.0
    active: bool = True

class ZoneUpdate(BaseModel):
    nombre: Optional[str] = None
    surcharge: Optional[float] = None
    active: Optional[bool] = None

class PricingConfig(BaseModel):
    base_rate: float = 30
    room_rate: float = 15
    sqm_rate: float = 0.5
    zone_surcharge_enabled: bool = True
    currency: str = "BOB"

class PricingPreview(BaseModel):
    rooms: int = 1
    sqm: float = 50
    zona: Optional[str] = None

# 3. CONFIGURACIÓN DE FASTAPI
app = FastAPI(title="Hogar Limpio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def calcular_precio(rooms: int, sqm: float, zona: Optional[str] = None) -> float:
    config_doc = db.collection("config").document("pricing").get()
    if not config_doc.exists:
        base_rate, room_rate, sqm_rate = 30, 15, 0.5
    else:
        cfg = config_doc.to_dict()
        base_rate = cfg.get("base_rate", 30)
        room_rate = cfg.get("room_rate", 15)
        sqm_rate = cfg.get("sqm_rate", 0.5)

    total = base_rate + (rooms * room_rate) + (sqm * sqm_rate)

    if zona:
        zonas_ref = db.collection("zonas")
        docs = zonas_ref.where("nombre", "==", zona).where("active", "==", True).stream()
        for doc in docs:
            surcharge = doc.to_dict().get("surcharge", 0)
            total += total * surcharge
            break

    return round(total, 2)

@app.on_event("startup")
def seed_data():
    # Seed zones if empty
    zonas_ref = db.collection("zonas")
    if not any(zonas_ref.limit(1).stream()):
        zonas_ref.add({"nombre": "San Roque", "surcharge": 0.0, "active": True})
        zonas_ref.add({"nombre": "Central", "surcharge": 0.05, "active": True})
        zonas_ref.add({"nombre": "Zona Sur", "surcharge": 0.10, "active": True})

    # Seed pricing config if missing
    pricing_ref = db.collection("config").document("pricing")
    if not pricing_ref.get().exists:
        pricing_ref.set({
            "base_rate": 30,
            "room_rate": 15,
            "sqm_rate": 0.5,
            "zone_surcharge_enabled": True,
            "currency": "BOB"
        })

    # Ensure profile fields added to existing users
    users_ref = db.collection("users")
    for doc in users_ref.stream():
        data = doc.to_dict()
        updates = {}
        if "profile_photo_url" not in data:
            updates["profile_photo_url"] = ""
        if "zona" not in data:
            updates["zona"] = ""
        if "experiencia_anios" not in data:
            updates["experiencia_anios"] = 0
        if "tipo_perfil" not in data:
            updates["tipo_perfil"] = "independiente"
        if "rating_avg" not in data:
            updates["rating_avg"] = 0.0
        if "rating_count" not in data:
            updates["rating_count"] = 0
        if "documents_verified" not in data:
            updates["documents_verified"] = False
        if updates:
            doc.reference.update(updates)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

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
        # Intentar crear en Auth. Si ya existe (creado desde cliente), obtenerlo.
        try:
            user = auth.create_user(
                email=data.email,
                password=data.password,
                display_name=data.displayName
            )
        except _auth_utils.EmailAlreadyExistsError:
            user = auth.get_user_by_email(data.email)

        # Asignar Rol en Claims
        auth.set_custom_user_claims(user.uid, {"role": data.role})
        # Guardar en Firestore (merge para no sobrescribir si ya existe)
        db.collection("users").document(user.uid).set({
            "displayName": data.displayName,
            "email": data.email,
            "role": data.role,
            "created_at": firestore.SERVER_TIMESTAMP,
            "status": "active"
        }, merge=True)

        # Auto-create "Limpieza básica" for new workers
        if data.role == "personal_limpieza":
            existing = db.collection("servicios").where("ofertante_id", "==", user.uid).where("titulo", "==", "Limpieza básica").stream()
            if not any(existing):
                db.collection("servicios").add({
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

@app.get("/users/me")
async def read_user_me(user: dict = Depends(get_current_user)):
    return {"uid": user["uid"], "email": user.get("email"), "role": user.get("role")}

@app.get("/api/users/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    uid = current_user["uid"]
    doc = db.collection("users").document(uid).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="User not found")
    profile = doc.to_dict()
    profile["uid"] = doc.id
    profile.pop("created_at", None)
    return profile

@app.put("/api/users/profile")
async def update_profile(data: ProfileUpdate, current_user: dict = Depends(get_current_user)):
    uid = current_user["uid"]
    updates = {k: v for k, v in data.dict().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    db.collection("users").document(uid).update(updates)
    return {"status": "success", "updated": list(updates.keys())}

from fastapi import UploadFile, File, Form

@app.post("/api/users/profile/photo")
async def upload_profile_photo(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    uid = current_user["uid"]
    ext = os.path.splitext(file.filename)[1] if file.filename else ".jpg"
    filename = f"{uid}_profile{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    content = await file.read()
    with open(filepath, "wb") as f:
        f.write(content)
    url = f"/uploads/{filename}"
    db.collection("users").document(uid).update({"profile_photo_url": url})
    return {"status": "success", "url": url}

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

    if servicio.get("titulo") == "Limpieza básica":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No puedes eliminar el servicio básico")

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

# 8. WORKER LISTING
@app.get("/api/workers")
async def list_workers(zona: Optional[str] = None, current_user: dict = Depends(get_current_user)):
    role = current_user.get("role")
    if role not in ("cliente", "admin"):
        raise HTTPException(status_code=403, detail="Only clients and admins can browse workers")
    users_ref = db.collection("users")
    query = users_ref.where("role", "==", "personal_limpieza")
    if zona:
        query = query.where("zona", "==", zona)
    docs = query.stream()
    workers = []
    for doc in docs:
        data = doc.to_dict()
        data["uid"] = doc.id
        data.pop("created_at", None)
        servicios_docs = db.collection("servicios").where("ofertante_id", "==", doc.id).where("estado", "==", "Aprobado").stream()
        data["servicios"] = []
        for s in servicios_docs:
            sv = s.to_dict()
            sv["id"] = s.id
            data["servicios"].append(sv)
        workers.append(data)
    return workers

@app.get("/api/workers/{uid}/profile")
async def get_worker_profile(uid: str, current_user: dict = Depends(get_current_user)):
    doc = db.collection("users").document(uid).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Worker not found")
    data = doc.to_dict()
    if data.get("role") != "personal_limpieza":
        raise HTTPException(status_code=400, detail="User is not a worker")
    data["uid"] = doc.id
    data.pop("created_at", None)
    servicios_docs = db.collection("servicios").where("ofertante_id", "==", uid).where("estado", "==", "Aprobado").stream()
    data["servicios"] = []
    for s in servicios_docs:
        sv = s.to_dict()
        sv["id"] = s.id
        data["servicios"].append(sv)
    return data

# 9. ZONAS CRUD
@app.get("/api/zonas")
async def list_active_zonas():
    docs = db.collection("zonas").where("active", "==", True).stream()
    result = []
    for doc in docs:
        item = doc.to_dict()
        item["id"] = doc.id
        result.append(item)
    return result

@app.get("/api/admin/zonas")
async def list_all_zonas(admin: dict = Depends(require_role("admin"))):
    docs = db.collection("zonas").stream()
    result = []
    for doc in docs:
        item = doc.to_dict()
        item["id"] = doc.id
        result.append(item)
    return result

@app.post("/api/admin/zonas")
async def create_zona(data: ZoneCreate, admin: dict = Depends(require_role("admin"))):
    ref = db.collection("zonas").add(data.dict())
    return {"status": "success", "id": ref[1].id}

@app.put("/api/admin/zonas/{zona_id}")
async def update_zona(zona_id: str, data: ZoneUpdate, admin: dict = Depends(require_role("admin"))):
    updates = {k: v for k, v in data.dict().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    db.collection("zonas").document(zona_id).update(updates)
    return {"status": "success", "updated": list(updates.keys())}

@app.delete("/api/admin/zonas/{zona_id}")
async def soft_delete_zona(zona_id: str, admin: dict = Depends(require_role("admin"))):
    db.collection("zonas").document(zona_id).update({"active": False})
    return {"status": "success", "message": "Zona desactivada"}

# 10. AVAILABILITY
class TimeSlot(BaseModel):
    start: str
    end: str

class DaySlots(BaseModel):
    monday: List[TimeSlot] = []
    tuesday: List[TimeSlot] = []
    wednesday: List[TimeSlot] = []
    thursday: List[TimeSlot] = []
    friday: List[TimeSlot] = []
    saturday: List[TimeSlot] = []
    sunday: List[TimeSlot] = []

class AvailabilityTemplate(BaseModel):
    weekdays: DaySlots

class DateOverride(BaseModel):
    worker_uid: str
    date: str
    active: bool

@app.get("/api/availability/{worker_uid}")
async def get_availability(worker_uid: str, current_user: dict = Depends(get_current_user)):
    template_doc = db.collection("availability_templates").document(worker_uid).get()
    template = template_doc.to_dict() if template_doc.exists else {}

    from datetime import date, timedelta
    today = date.today()
    overrides = {}
    for i in range(14):
        d = (today + timedelta(days=i)).isoformat()
        override_doc = db.collection("availability").document(worker_uid).collection("overrides").document(d).get()
        if override_doc.exists:
            overrides[d] = override_doc.to_dict()

    return {"template": template, "overrides": overrides}

@app.put("/api/availability")
async def save_availability_template(data: AvailabilityTemplate, current_user: dict = Depends(require_role("personal_limpieza"))):
    uid = current_user["uid"]
    payload = data.dict()
    print(f"[DEBUG] Saving availability for {uid}: {payload}")
    db.collection("availability_templates").document(uid).set(payload, merge=True)
    return {"status": "success"}

@app.post("/api/availability/toggle")
async def toggle_availability_override(data: DateOverride, current_user: dict = Depends(require_role("personal_limpieza"))):
    uid = current_user["uid"]
    if data.worker_uid != uid:
        raise HTTPException(status_code=403, detail="Can only toggle own availability")
    doc_ref = db.collection("availability").document(uid).collection("overrides").document(data.date)
    if data.active:
        doc_ref.set({"active": True, "date": data.date})
    else:
        doc = doc_ref.get()
        if doc.exists:
            doc_ref.delete()
    return {"status": "success"}

# 11. PRICING ENGINE
@app.get("/api/pricing")
async def get_pricing():
    doc = db.collection("config").document("pricing").get()
    if not doc.exists:
        return PricingConfig().dict()
    data = doc.to_dict()
    data.pop("updated_at", None)
    return data

@app.put("/api/admin/pricing")
async def update_pricing(data: PricingConfig, admin: dict = Depends(require_role("admin"))):
    doc_ref = db.collection("config").document("pricing")
    payload = data.dict()
    payload["updated_at"] = firestore.SERVER_TIMESTAMP
    payload["updated_by"] = admin["uid"]
    doc_ref.set(payload, merge=True)
    return {"status": "success"}

@app.post("/api/pricing/calcular")
async def preview_pricing(data: PricingPreview, current_user: dict = Depends(get_current_user)):
    total = calcular_precio(data.rooms, data.sqm, data.zona)
    return {"total": total, "currency": "BOB", "breakdown": {
        "rooms": data.rooms,
        "sqm": data.sqm,
        "zona": data.zona
    }}

# 12. BOOKING LIFECYCLE (RESERVAS)
class CrearReserva(BaseModel):
    worker_uid: str
    servicio_ids: List[str] = []
    fecha: str
    hora_inicio: str
    duracion_horas: float = 2.0
    direccion: str
    zona: str
    rooms: int = 1
    sqm: float = 50

class ReservaAction(BaseModel):
    pass

VALID_TRANSITIONS = {
    "Pendiente": ["Confirmado", "Cancelado"],
    "Confirmado": ["En_curso", "Completado", "Cancelado"],
    "En_curso": ["Completado"],
    "Completado": [],
    "Cancelado": []
}

@app.post("/api/reservas")
async def crear_reserva(data: CrearReserva, current_user: dict = Depends(require_role("cliente"))):
    uid = current_user["uid"]
    total = calcular_precio(data.rooms, data.sqm, data.zona)
    reserva_data = {
        "cliente_uid": uid,
        "worker_uid": data.worker_uid,
        "servicio_ids": data.servicio_ids,
        "servicio_id": data.servicio_ids[0] if data.servicio_ids else "",
        "fecha": data.fecha,
        "hora_inicio": data.hora_inicio,
        "duracion_horas": data.duracion_horas,
        "direccion": data.direccion,
        "zona": data.zona,
        "precio_total": total,
        "estado": "Pendiente",
        "recurrencia": "none",
        "rooms": data.rooms,
        "sqm": data.sqm,
        "created_at": firestore.SERVER_TIMESTAMP,
        "completed_at": None
    }
    ref = db.collection("reservas").add(reserva_data)
    return {"status": "success", "id": ref[1].id, "precio_total": total}

@app.get("/api/reservas")
async def list_reservas(current_user: dict = Depends(get_current_user)):
    uid = current_user["uid"]
    role = current_user.get("role")
    if role == "cliente":
        docs = db.collection("reservas").where("cliente_uid", "==", uid).stream()
    elif role == "personal_limpieza":
        docs = db.collection("reservas").where("worker_uid", "==", uid).stream()
    elif role == "admin":
        docs = db.collection("reservas").stream()
    else:
        raise HTTPException(status_code=403, detail="Unknown role")
    reservas = []
    for doc in docs:
        item = doc.to_dict()
        item["id"] = doc.id
        reservas.append(item)
    return reservas

def _get_reserva(reserva_id: str):
    ref = db.collection("reservas").document(reserva_id)
    doc = ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    data = doc.to_dict()
    data["id"] = doc.id
    return ref, data

def _transition(reserva_id: str, new_state: str, allowed_roles: list = None, uid_checks: list = None):
    ref, reserva = _get_reserva(reserva_id)
    current = reserva["estado"]
    if new_state not in VALID_TRANSITIONS.get(current, []):
        raise HTTPException(status_code=400, detail=f"Cannot transition from {current} to {new_state}")
    ref.update({"estado": new_state})
    if new_state == "Completado":
        ref.update({"completed_at": firestore.SERVER_TIMESTAMP})

    # Auto-manage payment lifecycle
    if new_state == "Confirmado":
        db.collection("payments").document(reserva_id).set({
            "reserva_id": reserva_id,
            "cliente_uid": reserva["cliente_uid"],
            "worker_uid": reserva["worker_uid"],
            "monto": reserva.get("precio_total", 0),
            "comision": round(reserva.get("precio_total", 0) * 0.10, 2),
            "metodo": "qr",
            "estado": "Retenido",
            "created_at": firestore.SERVER_TIMESTAMP,
            "released_at": None
        })
    elif new_state == "Completado":
        pay_ref = db.collection("payments").document(reserva_id)
        pay_doc = pay_ref.get()
        if pay_doc.exists:
            pay_ref.update({"estado": "Liberado", "released_at": firestore.SERVER_TIMESTAMP})
    elif new_state == "Cancelado":
        pay_ref = db.collection("payments").document(reserva_id)
        pay_doc = pay_ref.get()
        if pay_doc.exists:
            pay_ref.update({"estado": "Reembolsado"})

    return {"status": "success", "id": reserva_id, "estado": new_state}

@app.patch("/api/reservas/{reserva_id}/confirmar")
async def confirmar_reserva(reserva_id: str, current_user: dict = Depends(require_role("personal_limpieza"))):
    ref, reserva = _get_reserva(reserva_id)
    if reserva["worker_uid"] != current_user["uid"]:
        raise HTTPException(status_code=403, detail="Not your reservation")
    return _transition(reserva_id, "Confirmado")

@app.patch("/api/reservas/{reserva_id}/completar")
async def completar_reserva(reserva_id: str, current_user: dict = Depends(require_role("cliente"))):
    ref, reserva = _get_reserva(reserva_id)
    if reserva["cliente_uid"] != current_user["uid"]:
        raise HTTPException(status_code=403, detail="Not your reservation")
    return _transition(reserva_id, "Completado")

@app.patch("/api/reservas/{reserva_id}/cancelar")
async def cancelar_reserva(reserva_id: str, current_user: dict = Depends(get_current_user)):
    ref, reserva = _get_reserva(reserva_id)
    uid = current_user["uid"]
    role = current_user.get("role")
    if role != "admin" and reserva["cliente_uid"] != uid and reserva["worker_uid"] != uid:
        raise HTTPException(status_code=403, detail="Not authorized to cancel")
    return _transition(reserva_id, "Cancelado")

# 13. REVIEWS
class CreateReview(BaseModel):
    servicio_id: str
    worker_uid: str
    rating: int  # 1-5
    comment: str = ""

@app.post("/api/reviews")
async def create_review(data: CreateReview, current_user: dict = Depends(require_role("cliente"))):
    uid = current_user["uid"]
    if data.rating < 1 or data.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be 1-5")

    # Verify completed reservation exists with this worker
    reservas_docs = db.collection("reservas").where("cliente_uid", "==", uid).where("worker_uid", "==", data.worker_uid).where("estado", "==", "Completado").stream()
    found = False
    for _ in reservas_docs:
        found = True
        break
    if not found:
        raise HTTPException(status_code=400, detail="No completed reservation found for this service")

    review_ref = db.collection("reviews").add({
        "servicio_id": data.servicio_id,
        "worker_uid": data.worker_uid,
        "client_uid": uid,
        "rating": data.rating,
        "comment": data.comment,
        "created_at": firestore.SERVER_TIMESTAMP
    })

    # Update worker rating_avg and rating_count
    user_ref = db.collection("users").document(data.worker_uid)
    user_doc = user_ref.get()
    if user_doc.exists:
        user_data = user_doc.to_dict()
        count = user_data.get("rating_count", 0)
        avg = user_data.get("rating_avg", 0.0)
        new_count = count + 1
        new_avg = round(((avg * count) + data.rating) / new_count, 2)
        user_ref.update({"rating_count": new_count, "rating_avg": new_avg})

    return {"status": "success", "id": review_ref[1].id}

@app.get("/api/reviews/{worker_uid}")
async def list_reviews(worker_uid: str, current_user: dict = Depends(get_current_user)):
    docs = db.collection("reviews").where("worker_uid", "==", worker_uid).stream()
    result = []
    for doc in docs:
        item = doc.to_dict()
        item["id"] = doc.id
        client_doc = db.collection("users").document(item["client_uid"]).get()
        if client_doc.exists:
            item["clientName"] = client_doc.to_dict().get("displayName", "Cliente")
        else:
            item["clientName"] = "Cliente"
        result.append(item)
    return result

# 14. DOCUMENT UPLOAD (ESCUDO)

class DocumentVerify(BaseModel):
    verified: bool
    worker_uid: str

@app.post("/api/workers/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    tipo: str = Form(...),
    expires_at: str = Form(""),
    current_user: dict = Depends(require_role("personal_limpieza"))
):
    uid = current_user["uid"]
    ext = os.path.splitext(file.filename)[1] if file.filename else ".jpg"
    filename = f"{tipo}_{uuid.uuid4().hex}{ext}"
    doc_ref = db.collection("users").document(uid).collection("documents").add({
        "tipo": tipo,
        "file_url": f"documents/{uid}/{filename}",
        "verified": False,
        "verified_at": None,
        "verified_by": None,
        "expires_at": expires_at,
        "created_at": firestore.SERVER_TIMESTAMP
    })
    return {"status": "success", "id": doc_ref[1].id, "filename": filename}

@app.get("/api/workers/documents")
async def list_documents(current_user: dict = Depends(require_role("personal_limpieza"))):
    uid = current_user["uid"]
    docs = db.collection("users").document(uid).collection("documents").stream()
    result = []
    for doc in docs:
        item = doc.to_dict()
        item["id"] = doc.id
        result.append(item)
    return result

@app.get("/api/admin/workers/documents/pending")
async def pending_documents(admin: dict = Depends(require_role("admin"))):
    users_ref = db.collection("users")
    workers = users_ref.where("role", "==", "personal_limpieza").stream()
    result = []
    for worker in workers:
        docs = db.collection("users").document(worker.id).collection("documents").stream()
        for doc in docs:
            item = doc.to_dict()
            item["id"] = doc.id
            item["worker_uid"] = worker.id
            if not item.get("verified"):
                result.append(item)
    return result

@app.patch("/api/admin/workers/documents/{doc_id}")
async def verify_document(doc_id: str, data: DocumentVerify, admin: dict = Depends(require_role("admin"))):
    worker_uid = data.worker_uid
    doc_ref = db.collection("users").document(worker_uid).collection("documents").document(doc_id)
    doc = doc_ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Document not found")
    updates = {"verified": data.verified, "verified_at": firestore.SERVER_TIMESTAMP, "verified_by": admin["uid"]}
    doc_ref.update(updates)

    all_docs = db.collection("users").document(worker_uid).collection("documents").stream()
    all_verified = all(d.to_dict().get("verified", False) for d in all_docs)
    db.collection("users").document(worker_uid).update({"documents_verified": all_verified})
    return {"status": "success", "documents_verified": all_verified}

# 15. PAYMENT STUB
@app.post("/api/payments/initiate")
async def initiate_payment(data: ReservaAction, current_user: dict = Depends(require_role("cliente"))):
    uid = current_user["uid"]
    doc_ref = db.collection("payments").add({
        "cliente_uid": uid,
        "monto": 0,
        "comision": 0,
        "estado": "Pendiente",
        "created_at": firestore.SERVER_TIMESTAMP
    })
    return {"status": "success", "id": doc_ref[1].id}

@app.get("/api/admin/payments")
async def list_payments(admin: dict = Depends(require_role("admin"))):
    docs = db.collection("payments").stream()
    result = []
    for doc in docs:
        item = doc.to_dict()
        item["id"] = doc.id
        result.append(item)
    return result

@app.get("/api/payments/{reserva_id}")
async def get_payment(reserva_id: str, current_user: dict = Depends(get_current_user)):
    uid = current_user["uid"]
    role = current_user.get("role")
    ref, reserva = _get_reserva(reserva_id)
    if role != "admin" and reserva["cliente_uid"] != uid and reserva["worker_uid"] != uid:
        raise HTTPException(status_code=403, detail="Not authorized")
    ref_doc = db.collection("payments").document(reserva_id).get()
    if ref_doc.exists:
        data = ref_doc.to_dict()
        data["id"] = ref_doc.id
        return data
    return None
