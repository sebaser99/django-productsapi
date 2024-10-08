from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from models.database import SessionLocal, Base, engine
from models.perfume import PerfumeModel, PerfumCreate, Perfume
from typing import List
import logging


router = APIRouter()


def get_db(): # función que proporciona una sesión de base de datos a los endpoints.
    db = SessionLocal()
    try:
        yield db # para crear contexto: al finalizar la solicitud, la sesión se cierra
    finally:
        db.close()
        
@router.post("/perfumes/", response_model=Perfume)
def create_perfume(perfume: PerfumCreate, db: Session = Depends(get_db)):
    new_perfume = PerfumeModel(
        name= perfume.name,
        casa=perfume.casa,
        mililitros=perfume.mililitros,
        precio=perfume.precio,
        stock=perfume.stock,
        inDiscount=perfume.inDiscount or False
    )
    db.add(new_perfume)
    db.commit()
    db.refresh(new_perfume)
    return new_perfume

@router.get('/perfumes/', response_model=List[Perfume])
def read_perfumes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    perfumes = db.query(PerfumeModel).offset(skip).limit(limit).all()
    return perfumes

@router.get('/perfumes/{perfume_id}', response_model=Perfume)
def get_perfume(perfume_id = int, db: Session = Depends(get_db)):
    perfume = db.query(PerfumeModel).filter(PerfumeModel.id == perfume_id).first()
    if not perfume:
        raise HTTPException(status_code=404, detail="Perfume no encontrado")
    return perfume


@router.put('/perfumes/{perfume_id}', response_model=Perfume)
def update_user(perfume_id: int, perfume: PerfumCreate, db: Session = Depends(get_db)):
    db_perfume = db.query(PerfumeModel).filter(PerfumeModel.id == perfume_id).first()
    if not db_perfume:
        raise HTTPException(status_code=404, detail="Perfume no encontrado")
    for key, value in perfume.dict().items():
        setattr(db_perfume, key, value)
    db.commit()
   
    logging.info(f"Usuario actualizado exitosamente: {db_perfume}")
    return db_perfume

# Endpoint para borrar un usuario
@router.delete('/perfumes/{perfume_id}', response_model=Perfume)
def delete_perfume(perfume_id: int, db: Session = Depends(get_db)):
    db_perfume = db.query(PerfumeModel).filter(PerfumeModel.id == perfume_id).first()
    if not db_perfume:
        raise HTTPException(status_code=404, detail="Perfume no encontrado")
    db.delete(db_perfume)
    db.commit()
    logging.info(f"Perfume eliminado: {db_perfume}")
    return db_perfume
 
