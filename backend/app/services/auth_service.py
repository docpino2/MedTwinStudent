import hashlib
import secrets
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException
from pwdlib import PasswordHash
from pydantic import TypeAdapter
from sqlalchemy import Engine, delete, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.auth import AuthSession, AuthUser
from app.schemas.auth import AuthUserView, LoginRequest, LoginResponse, PilotAccount

password_hasher = PasswordHash.recommended()
_dummy_hash = password_hasher.hash(secrets.token_urlsafe(32))
LOGIN_ERROR = "Correo o contraseña incorrectos, o acceso temporalmente bloqueado."


def utc(value: datetime) -> datetime:
    return value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)


def token_digest(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def initialize_auth(bind: Engine) -> None:
    # Bootstrap only these new tables; existing account permissions/passwords are preserved.
    AuthUser.__table__.create(bind, checkfirst=True)
    AuthSession.__table__.create(bind, checkfirst=True)
    accounts = TypeAdapter(list[PilotAccount]).validate_json(settings.pilot_accounts_json.get_secret_value())
    with Session(bind) as db:
        for account in accounts:
            hashed = account.password_hash.get_secret_value()
            if not hashed.startswith("$argon2id$"):
                raise RuntimeError("La cuenta de piloto requiere un hash Argon2id.")
            email = account.email.strip().casefold()
            values = dict(email=email, display_name=account.display_name, role=account.role, password_hash=hashed)
            if bind.dialect.name == "postgresql":
                db.execute(pg_insert(AuthUser).values(**values).on_conflict_do_nothing(index_elements=[AuthUser.email]))
            elif db.scalar(select(AuthUser).where(AuthUser.email == email)) is None:
                db.add(AuthUser(**values))
        db.commit()


def login(db: Session, request: LoginRequest) -> LoginResponse:
    now = datetime.now(UTC)
    user = db.scalar(select(AuthUser).where(AuthUser.email == request.email).with_for_update())
    if user is None or not user.active:
        password_hasher.verify(request.password.get_secret_value(), _dummy_hash)
        raise HTTPException(status_code=401, detail=LOGIN_ERROR)
    if user.locked_until and utc(user.locked_until) > now:
        raise HTTPException(status_code=401, detail=LOGIN_ERROR)
    if user.locked_until:
        user.failed_attempts = 0
        user.locked_until = None
    if not password_hasher.verify(request.password.get_secret_value(), user.password_hash):
        user.failed_attempts += 1
        if user.failed_attempts >= 5:
            user.locked_until = now + timedelta(minutes=15)
        db.commit()
        raise HTTPException(status_code=401, detail=LOGIN_ERROR)

    user.failed_attempts = 0
    user.locked_until = None
    token = secrets.token_urlsafe(32)
    expires_at = now + timedelta(hours=settings.auth_session_hours)
    db.execute(delete(AuthSession).where(AuthSession.expires_at <= now))
    db.add(AuthSession(token_hash=token_digest(token), user_id=user.id, expires_at=expires_at))
    db.commit()
    return LoginResponse(access_token=token, expires_at=expires_at, user=AuthUserView.model_validate(user))
