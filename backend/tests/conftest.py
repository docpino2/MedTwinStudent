import pytest

from app.core.auth import get_current_user
from app.main import app
from app.models.auth import AuthUser


@pytest.fixture(autouse=True)
def authenticated_service_tests(request):
    if request.node.get_closest_marker("auth"):
        yield
        return
    previous = app.dependency_overrides.copy()
    app.dependency_overrides[get_current_user] = lambda: AuthUser(
        id="test-admin", email="admin@example.test", display_name="Administrador de prueba", role="admin", active=True,
    )
    yield
    app.dependency_overrides.clear()
    app.dependency_overrides.update(previous)
