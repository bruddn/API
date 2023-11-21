from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI()

class Cliente(BaseModel):
    id: int
    nome: str
    hora: datetime
    atendimento: str

fila_de_clientes: List[Cliente] = []

@app.get("/")
def home():
    return {"mensagem": "Bem-vindo à página de espera"}

@app.get("/fila/")
def exibir_fila():
    if not fila_de_clientes:
        raise HTTPException(status_code=200, detail="Fila vazia")
    return {"clientes": fila_de_clientes}

@app.get("/fila/{id}")
def mostrar_cliente(id: int):
    cliente = next((c for c in fila_de_clientes if c.id == id), None)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return {"cliente": cliente}

@app.post("/fila/")
def novo_cliente(cliente: Cliente):
    if len(cliente.nome) > 20:
        raise HTTPException(status_code=400, detail="Nome deve ter no máximo 20 caracteres")
    if cliente.atendimento not in ["N", "P"]:
        raise HTTPException(status_code=400, detail="Atendimento deve ser 'N' ou 'P'")
    
    if fila_de_clientes:
        cliente.id = fila_de_clientes[-1].id + 1
    else:
        cliente.id = 1
    
    fila_de_clientes.append(cliente)
    return {"mensagem": "Você está na fila!"}

@app.put("/fila/")
def atualizar_cliente(id:int, cliente: Cliente):
    index = next((i for i, c in enumerate(fila_de_clientes) if c.id == id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    fila_de_clientes[index] = cliente
    return {"mensagem": "Fila atualizada"}

@app.delete("/fila/{id}")
def apagar_cliente(id: int):
    cliente = next((c for c in fila_de_clientes if c.id == id), None)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    fila_de_clientes.remove(cliente)
    return {"mensagem": "Cliente removido!"}