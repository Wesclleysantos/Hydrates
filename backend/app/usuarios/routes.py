from fastapi import APIRouter, status
from pydantic import BaseModel, EmailStr, Field
from app.usuarios import controller

router = APIRouter(
    prefix = "/usuarios",
    tags = ["Usuários"],
)

class CadastroUsuario(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    email: EmailStr
    senha: str = Field(min_length=8)
    peso: float | None = Field(default=None, gt=0, le=999.99)
    idade: int | None = Field(default=None, gt=0, le=150)

@router.post("", status_code=status.HTTP_201_CREATED)
def cadastrar(dados: CadastroUsuario):
    return controller.cadastrar_usuario(
        nome = dados.nome,
        email = str(dados.email),
        senha = dados.senha,
        peso = dados.peso,
        idade = dados.idade,
    )

class LoginUsuario(BaseModel):
    email: EmailStr
    senha: str = Field(min_length=1)

@router.post("/login")
def login(dados: LoginUsuario):
    return controller.login_usuario(
        email=str(dados.email),
        senha=dados.senha,
    )