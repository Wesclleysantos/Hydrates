from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UsuarioCadastro(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    nickname: Optional[str] = None
    email: EmailStr
    senha: str = Field(min_length=8)
    idade: int = Field(gt=0, le=120)
    peso: float = Field(gt=0, le=500)
