from fastapi import FastAPI
from app.config import settings
from app.usuarios.routes import router as usuarios_router

app = FastAPI(
    tittle = settings.APP_NAME,
    debug = settings.APP_DEBUG,
)

app.include_router(usuarios_router)

@app.get("/")
def inicio():
    return {
        "mensagem": "API Hydrates funcionando!",
    }
