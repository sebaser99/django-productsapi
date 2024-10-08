from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import SessionLocal, Base, engine
from models.user import UserModel, UserCreate, User
from routes.perfumes import router as perfumes_router
from typing import List
import json
import logging

logging.basicConfig(level=logging.INFO) # Esto establecerá el nivel de logging a INFO, lo que significa que verás mensajes informativos

app = FastAPI()

# Crear las tablas en la base de datos al iniciar
Base.metadata.create_all(bind=engine)

# Dependencia para obtener la sesión de la base de datos
def get_db(): # función que proporciona una sesión de base de datos a los endpoints.
    db = SessionLocal()
    try:
        yield db # para crear contexto: al finalizar la solicitud, la sesión se cierra
    finally:
        db.close()

@app.get('/')
def index():
    return {'mensaje': 'Bienvenidos a la API de Productos'}

# Endpoint para obtener todos los usuarios
@app.get('/user/', response_model=List[User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(UserModel).offset(skip).limit(limit).all()
    logging.info(f"Recuperando usuarios: {users}")
    for user in users:
        user.valores = json.loads(user.valores)
    return users

# Endpoint para crear un nuevo usuario
@app.post('/user/', response_model=User)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    logging.info(f"Creando usuario: {user}")
    db_user = UserModel(
        name=user.name,
        signup_ts=user.signup_ts,
        valores=json.dumps(user.valores)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_user.valores = json.loads(db_user.valores)
    logging.info(f"Usuario creado: {db_user}")
    return db_user

# Endpoint para actualizar un usuario existente
@app.put('/user/{user_id}', response_model=User)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for key, value in user.dict().items():
        setattr(db_user, key, value)
     # Asegúrate de manejar 'valores' correctamente
    if 'valores' in user.dict():
        db_user.valores = json.dumps(user.valores)  
    db.commit()
    valores_list = json.loads(db_user.valores) if db_user.valores else [] 
    response_user = UserModel(
        id=db_user.id,
        name=db_user.name,
        signup_ts=db_user.signup_ts,
        valores=valores_list
    )
    logging.info(f"Usuario actualizado exitosamente: {db_user}")
    return response_user

# Endpoint para borrar un usuario
@app.delete('/user/{user_id}', response_model=User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(db_user)
    db.commit()
    valores_list = json.loads(db_user.valores) if db_user.valores else [] 
    response_user = UserModel(
        id=db_user.id,
        name=db_user.name,
        signup_ts=db_user.signup_ts,
        valores=valores_list
    )
    logging.info(f"Usuario eliminado: {db_user}")
    return response_user
 
# Incluye el router de items
app.include_router(perfumes_router) # lo que sugiere que hay más endpoints relacionados con # "items" definidos en otro archivo

@app.get("/favicon.ico")
async def favicon():
    return {}