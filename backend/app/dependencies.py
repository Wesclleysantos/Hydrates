from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.auth import verificar_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/usuarios/login/swagger"
)


def obter_usuario_atual(
    token: str = Depends(oauth2_scheme),
) -> int:
    try:
        return verificar_token(token)

    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )
