from fastapi import APIRouter, Depends, Response
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.core.auth import get_current_user, require_admin, require_credentials
from app.core.database import get_db
from app.models.auth import AuthSession, AuthUser
from app.schemas.auth import AuthUserView, LoginRequest, LoginResponse
from app.services.auth_service import login, token_digest

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def sign_in(request: LoginRequest, response: Response, db: Session = Depends(get_db)) -> LoginResponse:
    response.headers["Cache-Control"] = "no-store"
    return login(db, request)


@router.get("/me", response_model=AuthUserView)
def me(response: Response, user: AuthUser = Depends(get_current_user)) -> AuthUser:
    response.headers["Cache-Control"] = "no-store"
    return user


@router.post("/logout", status_code=204)
def sign_out(token: str = Depends(require_credentials), db: Session = Depends(get_db)) -> Response:
    db.execute(delete(AuthSession).where(AuthSession.token_hash == token_digest(token)))
    db.commit()
    return Response(status_code=204, headers={"Cache-Control": "no-store"})


@router.get("/users", response_model=list[AuthUserView], dependencies=[Depends(require_admin)])
def list_accounts(db: Session = Depends(get_db)) -> list[AuthUser]:
    return list(db.scalars(select(AuthUser).order_by(AuthUser.email)))
