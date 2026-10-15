from fastapi import FastAPI
from app.config import settings
from app.usuarios.routes import router as usuarios_router
from app.bebidas.routes import router as bebidas_router
from app.consumos.routes import router as consumos_router

app = FastAPI(
    title = settings.APP_NAME,
    debug = settings.APP_DEBUG,
)

app.include_router(usuarios_router)
app.include_router(bebidas_router)
app.include_router(consumos_router)

@app.get("/")
def inicio():
    return {
        "mensagem": "API Hydrates funcionando!",
    }
