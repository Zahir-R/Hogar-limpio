from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

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

class CreateReview(BaseModel):
    servicio_id: str
    worker_uid: str
    rating: int
    comment: str = ""

class DocumentVerify(BaseModel):
    verified: bool
    worker_uid: str
