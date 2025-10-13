from fastapi import FastAPI, HTTPException, status, Depends, Security
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from bson.errors import InvalidId
import pymongo
from decouple import config
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from pymongo import MongoClient

# ---- Config / Env ----
MONGO_URI = config("MONGO_URI", default="mongodb://localhost:27017")
SECRET_KEY = config("SECRET_KEY", default="secretkey123")
ALGORITHM = config("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(config("ACCESS_TOKEN_EXPIRE_MINUTES", default="60"))

# ---- MongoDB ----
client = pymongo.MongoClient(MONGO_URI)
db = client["emotional_tracker"]

# ---- Função de dependência do DB ----
def get_db():
    """
    Retorna o banco de dados real ou o cliente injetado (usado em testes com mongomock).
    """
    db = client["emotional_tracker"]
    return db

# ---- App ----
app = FastAPI(title="Emotional Tracker API", version="1.0")
API_PREFIX = "/api/v1"

# ---- Security ----
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_PREFIX}/auth/token")

def hash_password(password: str) -> str:
    password = password[:72]
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    payload = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def parse_objectid(id: str) -> ObjectId:
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")

def serialize(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    return doc

# ---- Models ----
class UserIn(BaseModel):
    nome: str
    email: EmailStr
    idade: int = Field(..., ge=0)
    senha: str = Field(..., min_length=6, max_length=72)

class UserOut(BaseModel):
    id: str
    nome: str
    email: EmailStr
    idade: int

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class Diary(BaseModel):
    user_id: str
    data: str
    texto: str

class Emotion(BaseModel):
    user_id: str
    tipo: str
    intensidade: int = Field(..., ge=1, le=10)

class SupportCenter(BaseModel):
    nome: str
    telefone: str
    endereco: str

class Assessment(BaseModel):
    user_id: str
    avaliacao: str
    data: str

# ---- CRUD ----
def create(collection, data: dict):
    result = collection.insert_one(data)
    return {"id": str(result.inserted_id)}

def read(collection, id: str):
    doc = collection.find_one({"_id": parse_objectid(id)})
    if not doc:
        raise HTTPException(404, "Não encontrado")
    return serialize(doc)

def list_all(collection):
    return [serialize(d) for d in collection.find()]

def update(collection, id: str, data: dict):
    result = collection.update_one({"_id": parse_objectid(id)}, {"$set": data})
    if not result.matched_count:
        raise HTTPException(404, "Não encontrado")
    return {"mensagem": "Atualizado"}

def delete(collection, id: str):
    result = collection.delete_one({"_id": parse_objectid(id)})
    if not result.deleted_count:
        raise HTTPException(404, "Não encontrado")
    return {"mensagem": "Deletado"}

def registrar_atividade(user_id: str, acao: str, detalhes: str = "", db=Depends(get_db)):
    log = {
        "user_id": user_id,
        "acao": acao,
        "detalhes": detalhes,
        "timestamp": datetime.utcnow()
    }
    db["logs"].insert_one(log)


# ---- Auth Helpers ----
def get_user_by_email(email: str, db=Depends(get_db)):
    return db["users"].find_one({"email": email})


def authenticate(email: str, password: str):
    user = get_user_by_email(email)
    if user and verify_password(password, user["password_hash"]):
        return user

async def get_current_user(token: str = Security(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Não autorizado",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(email)
    if not user:
        raise credentials_exception
    return {
        "id": str(user["_id"]),
        "nome": user["nome"],
        "email": user["email"],
        "idade": user["idade"]
    }

# ---- Auth Endpoints ---- 
# ---- Auth Endpoints ---- 
@app.post(f"{API_PREFIX}/auth/register", status_code=201)
def register(user: UserIn, db=Depends(get_db)):
    if get_user_by_email(user.email, db):
        raise HTTPException(400, "Email já cadastrado")
    hashed = hash_password(user.senha)
    user_dict = user.dict()
    user_dict.pop("senha")
    user_dict["password_hash"] = hashed
    user_dict["created_at"] = datetime.utcnow()
    user_id = create(db["users"], user_dict)["id"]
    registrar_atividade(user_id, "registro_usuario", f"Usuário {user.email} registrado", db)
    return {"id": user_id}


@app.post(f"{API_PREFIX}/auth/token", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user = authenticate(form.username, form.password, db)
    if not user:
        raise HTTPException(401, "Email ou senha incorretos")
    token = create_access_token({"sub": user["email"]})
    registrar_atividade(str(user["_id"]), "login", f"Usuário {user['email']} logado", db)
    return {"access_token": token}


@app.get(f"{API_PREFIX}/me", response_model=UserOut)
async def me(current_user: dict = Depends(get_current_user)):
    return current_user


# ---- Users ----
@app.get(f"{API_PREFIX}/users")
def users(current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    registrar_atividade(current_user["id"], "listar_usuarios", db=db)
    return list_all(db["users"])


@app.get(f"{API_PREFIX}/users/{{id}}")
def user(id: str, current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    registrar_atividade(current_user["id"], "visualizar_usuario", f"ID {id}", db=db)
    return read(db["users"], id)


@app.put(f"{API_PREFIX}/users/{{id}}")
def update_user(id: str, user: UserIn, current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    data = user.dict()
    data["password_hash"] = hash_password(data.pop("senha"))
    registrar_atividade(current_user["id"], "editar_usuario", f"ID {id}", db=db)
    return update(db["users"], id, data)


@app.delete(f"{API_PREFIX}/users/{{id}}", status_code=204)
def delete_user(id: str, current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    registrar_atividade(current_user["id"], "deletar_usuario", f"ID {id}", db=db)
    delete(db["users"], id)


# ---- Diaries ----
@app.post(f"{API_PREFIX}/diaries", status_code=201)
def create_diary(diary: Diary, current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    if diary.user_id != current_user["id"]:
        raise HTTPException(403, "Apenas seu próprio diário")
    registrar_atividade(current_user["id"], "criar_diario", db=db)
    return create(db["diaries"], diary.dict())


@app.get(f"{API_PREFIX}/diaries/user/{{user_id}}")
def user_diaries(user_id: str, current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    if user_id != current_user["id"]:
        raise HTTPException(403, "Acesso negado")
    registrar_atividade(current_user["id"], "listar_diarios", db=db)
    return [serialize(d) for d in db["diaries"].find({"user_id": user_id})]


# ---- Emotions ----
@app.post(f"{API_PREFIX}/emotions", status_code=201)
def create_emotion(emotion: Emotion, current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    registrar_atividade(current_user["id"], "criar_emocao", db=db)
    return create(db["emotions"], emotion.dict())


@app.get(f"{API_PREFIX}/emotions/user/{{user_id}}")
def user_emotions(user_id: str, current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    if user_id != current_user["id"]:
        raise HTTPException(403, "Acesso negado")
    registrar_atividade(current_user["id"], "listar_emocoes", db=db)
    return [serialize(e) for e in db["emotions"].find({"user_id": user_id})]


# ---- Support Centers ----
@app.post(f"{API_PREFIX}/supportcenters", status_code=201)
def create_center(center: SupportCenter, current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    registrar_atividade(current_user["id"], "criar_centro_apoio", db=db)
    return create(db["supportcenters"], center.dict())


# ---- Assessments ----
@app.post(f"{API_PREFIX}/assessments", status_code=201)
def create_assessment(assessment: Assessment, current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    registrar_atividade(current_user["id"], "criar_avaliacao", db=db)
    return create(db["assessments"], assessment.dict())


@app.get(f"{API_PREFIX}/assessments/user/{{user_id}}")
def user_assessments(user_id: str, current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    if user_id != current_user["id"]:
        raise HTTPException(403, "Acesso negado")
    registrar_atividade(current_user["id"], "listar_avaliacoes", db=db)
    return [serialize(a) for a in db["assessments"].find({"user_id": user_id})]
