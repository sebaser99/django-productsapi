from sqlalchemy import Column, Integer, String, DateTime

from .database import Base

from pydantic import BaseModel

from datetime import datetime

from typing import List, Optional

import json

 

# Modelo de SQLAlchemy

class UserModel(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, index=True)

    signup_ts = Column(DateTime, default=datetime.utcnow)

    valores = Column(String)  # Puedes manejar esto como JSON, pero podría ser útil usar JSONB en PostgreSQL

 

# Esquema Pydantic para crear un usuario

class UserCreate(BaseModel):

    name: str

    signup_ts: Optional[datetime] = None  # Cambiar a Optional

    valores: List[int] = []  # Usar List en lugar de list para mayor claridad
    

# Esquema Pydantic para la respuesta del usuario
class User(BaseModel):
    id: int
    name: str
    signup_ts: datetime
    valores: List[int] = []

    class Config:
         from_attributes = True   # 
         
# Funciones para manejar el almacenamiento
def serialize_values(values):
    return json.dumps(values)  # Serializa la lista a JSON

def deserialize_values(values):
    return json.loads(values) 