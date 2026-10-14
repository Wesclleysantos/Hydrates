from fastapi import Depend, HTTPException, status
from fastapi.security import OAuth2PasswordBeares
from app.auth import verificar_token

oauth2_scheme = OAuth2PasswordBeare(tokenUrl="/usuarios/login")

def obter_usuario_atual(
    token: str = Depends(oauth2_scheme),
) -> int:
    try:
        return verificar_token(token)

    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado.",
            headers={"WWW-Authenticate": "Beares"},
        )
    