from fastapi import FastAPI
from app.config import settings
from app.usuarios.routes import router as usuarios_router
from app.bebidas.routes import router as bebidas_router
from app.consumos.routes import router as consumos_router
from app.metas.routes import router as metas_router
from app.configuracoes.routes import router as configuracoes_router
from app.conquistas.routes import router as conquistas_router

app = FastAPI(
    title = settings.APP_NAME,
    debug = settings.APP_DEBUG,
)

app.include_router(usuarios_router)
app.include_router(bebidas_router)
app.include_router(consumos_router)
app.include_router(metas_router)
app.include_router(configuracoes_router)
app.include_router(conquistas_router)

@app.get("/")
def inicio():
    return {
        "mensagem": "API Hydrates funcionando!",
    }
