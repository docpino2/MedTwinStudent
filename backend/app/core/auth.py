from datetime import UTC, datetime

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.auth import AuthSession, AuthUser
from app.services.auth_service import token_digest, utc

bearer = HTTPBearer(auto_error=False)


def require_credentials(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)) -> str:
    if credentials is None or credentials.scheme.lower() != "bearer" or not 32 <= len(credentials.credentials) <= 128:
        raise HTTPException(status_code=401, detail="Inicia sesión para continuar.", headers={"WWW-Authenticate": "Bearer"})
    return credentials.credentials


def get_current_user(token: str = Depends(require_credentials), db: Session = Depends(get_db)) -> AuthUser:
    session = db.get(AuthSession, token_digest(token))
    if session is None or utc(session.expires_at) <= datetime.now(UTC):
        raise HTTPException(status_code=401, detail="La sesión venció o no es válida.", headers={"WWW-Authenticate": "Bearer"})
    user = db.get(AuthUser, session.user_id)
    if user is None or not user.active:
        raise HTTPException(status_code=401, detail="La sesión no es válida.")
    return user


def require_admin(user: AuthUser = Depends(get_current_user)) -> AuthUser:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Acceso reservado al administrador.")
    return user
