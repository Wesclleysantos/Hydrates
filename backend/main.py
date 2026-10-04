from fastapi import FastAPI
app = FastAPI(title="Hydrates API")

@app.get("/")
def inicio():
    return {"mensagem": "Bem-vindo à API do Hydrates!"}
