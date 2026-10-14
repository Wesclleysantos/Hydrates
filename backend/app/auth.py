from datetime import datetime, timedelta, timezone
import jwt
from app.config import settings

def criar_token_acesso(usuario_id: int) -> str:
    if not settings.JWT_SECRET_KEY:
        raise RuntimeError("JWT_SECRET_KEY não configurada.")

    agora = datetime.now(timezone.utc)

    payload = {
        "sub": str(usuario_id),
        "iat": agora,
        "exp": agora + timedelta(
            minutes=settings.JWT_EXPIRE_MINUTES
        ),
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    return token

def verificar_token(token: str) -> int:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

        usuario_id = payload.get("sub")

        if usuario_id is None:
            raise ValueError("Token sem identificação do usúario.")
        
        return int(usuario_id)

    except jwt.InvalidTokenError:
        raise ValueError("Token inválido ou expirado.")
    