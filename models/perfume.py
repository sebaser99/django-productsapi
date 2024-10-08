from sqlalchemy import Column, Integer, String, Double, Boolean, Float

from .database import Base

from pydantic import BaseModel, validator

from typing import Optional

import json


# Modelo de SQLAlchemy

class PerfumeModel(Base):

    __tablename__ = "perfumes"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, index=True)

    casa = Column(String, index=False)

    mililitros = Column(Integer,  index=False)  
    
    precio = Column(Float, index=False)# Puedes manejar esto como JSON, pero podría ser útil usar JSONB en PostgreSQL

    stock = Column(Integer,  index=False)  
    
    inDiscount = Column(Boolean, index=False)
 

# Esquema Pydantic para crear un usuario

class PerfumCreate(BaseModel):

    name : Optional[str] = None

    casa : Optional[str] = None

    mililitros : Optional[int] = None  
    
    precio : Optional[float] = None

    stock : Optional[int] = None  
    
    inDiscount : Optional[bool] = False 
    

# Esquema Pydantic para la respuesta del usuario
class Perfume(BaseModel):
    id: int
    name: str
    casa : str
    mililitros : int
    precio : float
    stock : int
    inDiscount : bool
    
    @validator('mililitros')
    def mililitros_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('mililitros must be positive')
        return v
    @validator('precio')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('price must be positive')
        return v
    
    @validator('stock')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('stock must be positive')
        return v
   

    class Config:
         from_attributes = True   # 
         
# Funciones para manejar el almacenamiento
def serialize_values(values):
    return json.dumps(values)  # Serializa la lista a JSON

def deserialize_values(values):
    return json.loads(values) 