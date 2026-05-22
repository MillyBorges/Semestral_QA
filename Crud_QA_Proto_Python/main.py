from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional
from contextlib import asynccontextmanager
import sqlite3
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="User Management API", 
    description="Uma API CRUD simples baseada no sistema fornecido.",
    lifespan=lifespan
)

DATABASE = "banco_usuarios.db"

# ==========================================
# 1. MODELOS DE DADOS (Pydantic)
# ==========================================
class UserBase(BaseModel):
    nome: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# ==========================================
# 2. CONFIGURAÇÃO DO BANCO DE DADOS
# ==========================================
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')
        conn.commit()



# ==========================================
# 3. ENDPOINTS CRUD
# ==========================================

@app.post("/usuarios/", response_model=User, status_code=201)
def create_user(user: UserCreate, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("INSERT INTO usuarios (nome, email) VALUES (?, ?)", (user.nome, user.email))
    db.commit()
    user_id = cursor.lastrowid
    return {"id": user_id, "nome": user.nome, "email": user.email}

@app.get("/usuarios/", response_model=List[User])
def read_users(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios")
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

@app.get("/usuarios/{user_id}", response_model=User)
def read_user(user_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return dict(row)

@app.put("/usuarios/{user_id}", response_model=User)
def update_user(user_id: int, user: UserCreate, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("UPDATE usuarios SET nome = ?, email = ? WHERE id = ?", (user.nome, user.email, user_id))
    db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"id": user_id, "nome": user.nome, "email": user.email}

@app.delete("/usuarios/{user_id}", status_code=204)
def delete_user(user_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
    db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return None

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
