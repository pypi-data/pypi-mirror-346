import datetime
from unittest import mock
import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.authentication import UnauthenticatedUser
from starlette.requests import HTTPConnection, Request
from starlette.responses import Response
from starlette.testclient import TestClient

from kupala import Kupala
from kupala.authentication import (
    SESSION_HASH_KEY,
    SESSION_IDENTITY_KEY,
    Authentication,
    AuthenticationError,
    Authenticator,
    AuthenticatorBackend,
    BaseUser,
    ChainAuthenticator,
    CurrentUser,
    DatabaseUserLoader,
    HTTPBasicAuthenticator,
    Identity,
    SessionAuthenticator,
    make_session_auth_hash,
    update_session_auth_hash,
    user_registered,
)
from kupala.passwords import PasswordHasher
from kupala.routing import CallNext, RouteGroup
from tests.models import User


class MemoryUserLoader:
    def __init__(self, users: list[User]) -> None:
        self.users: dict[str, User] = {user.identity: user for user in users}

    async def __call__(self, conn: HTTPConnection, identity: str) -> BaseUser | None:
        return self.users.get(identity)


class _DummyAuthenticator(Authenticator):
    def __init__(self, user: BaseUser | None) -> None:
        self.user = user

    async def authenticate(self, conn: HTTPConnection) -> Identity | None:
        if self.user:
            return Identity(
                id=self.user.identity,
                user=self.user,
                scopes=[],
                authenticator=type(self),
            )
        return None


class TestSessionAuthenticator:
    async def test_authenticates(self) -> None:
        user = User(email="root")
        user_loader = MemoryUserLoader([user])

        conn = HTTPConnection(
            {
                "type": "http",
                "app": Kupala(secret_key="key!"),
                "session": {SESSION_IDENTITY_KEY: "root"},
            }
        )
        authenticator = SessionAuthenticator(user_loader=user_loader)
        identity = await authenticator.authenticate(conn)
        assert identity
        assert identity.id == "root"

    async def test_not_authenticated(self) -> None:
        user = User(email="root")
        user_loader = MemoryUserLoader([user])

        conn = HTTPConnection(
            {
                "type": "http",
                "app": Kupala(secret_key="key!"),
                "session": {},
            }
        )
        authenticator = SessionAuthenticator(user_loader=user_loader)
        assert not await authenticator.authenticate(conn)

    async def test_no_user(self) -> None:
        user = User(email="test")
        user_loader = MemoryUserLoader([user])

        conn = HTTPConnection(
            {
                "type": "http",
                "app": Kupala(secret_key="key!"),
                "session": {SESSION_IDENTITY_KEY: "root"},
            }
        )
        authenticator = SessionAuthenticator(user_loader=user_loader)
        assert not await authenticator.authenticate(conn)

    async def test_extracts_user_scopes(self) -> None:
        user = User(email="root", scopes=["admin"])
        user_loader = MemoryUserLoader([user])

        authenticator = SessionAuthenticator(user_loader=user_loader)
        conn = HTTPConnection(
            {
                "type": "http",
                "app": Kupala(secret_key="key!"),
                "session": {SESSION_IDENTITY_KEY: "root"},
            }
        )
        identity = await authenticator.authenticate(conn)
        assert identity
        assert identity.scopes == ["admin"]

    async def test_validates_session_hash(self) -> None:
        user = User(email="root", password="password")
        user_loader = MemoryUserLoader([user])
        user_loader = MemoryUserLoader([user])

        authenticator = SessionAuthenticator(user_loader=user_loader)
        conn = HTTPConnection(
            {
                "type": "http",
                "app": Kupala(secret_key="key!"),
                "session": {
                    SESSION_IDENTITY_KEY: "root",
                    SESSION_HASH_KEY: make_session_auth_hash(user, "key!"),
                },
            }
        )
        assert await authenticator.authenticate(conn)

        # simulate password change flow
        user.password = "new password"
        assert not await authenticator.authenticate(conn)
        update_session_auth_hash(conn, user, "key!")
        assert await authenticator.authenticate(conn)

    async def test_validates_invalid_session_hash(self) -> None:
        user = User(email="root", password="password")
        user_loader = MemoryUserLoader([user])

        authenticator = SessionAuthenticator(user_loader=user_loader)
        conn = HTTPConnection(
            {
                "type": "http",
                "app": Kupala(secret_key="key!"),
                "session": {
                    SESSION_IDENTITY_KEY: "root",
                    SESSION_HASH_KEY: "bad hash",
                },
            }
        )
        assert not await authenticator.authenticate(conn)

    async def test_update_session_hash(self) -> None:
        user = User(email="root", password="password")
        user_loader = MemoryUserLoader([user])

        authenticator = SessionAuthenticator(user_loader=user_loader)
        conn = HTTPConnection(
            {
                "type": "http",
                "app": Kupala(secret_key="key!"),
                "session": {
                    SESSION_IDENTITY_KEY: "root",
                    SESSION_HASH_KEY: "bad hash",
                },
            }
        )
        assert not await authenticator.authenticate(conn)

        update_session_auth_hash(conn, user, "key!")
        assert await authenticator.authenticate(conn)


class TestChainAuthenticator:
    async def test_authenticates(self) -> None:
        user = User(email="root")
        authenticator = ChainAuthenticator(
            _DummyAuthenticator(None),
            _DummyAuthenticator(user),
        )
        conn = HTTPConnection({"type": "http"})
        assert await authenticator.authenticate(conn)

    async def test_not_authenticates(self) -> None:
        backend = ChainAuthenticator(
            _DummyAuthenticator(None),
            _DummyAuthenticator(None),
        )
        conn = HTTPConnection({"type": "http"})
        assert not await backend.authenticate(conn)


class TestAuthenticatorBackend:
    async def test_authenticates(self) -> None:
        user = User(email="root")
        backend = AuthenticatorBackend(_DummyAuthenticator(user))
        result = await backend.authenticate(HTTPConnection({"type": "http"}))
        assert result
        credentials, authenticated_user = result
        assert credentials.scopes == []
        assert authenticated_user.identity == "root"

    async def test_not_authenticates(self) -> None:
        backend = AuthenticatorBackend(_DummyAuthenticator(None))
        assert not await backend.authenticate(HTTPConnection({"type": "http"}))


class TestHTTPBasicAuthenticator:
    async def test_authenticates_with_valid_credentials(self) -> None:
        app = Kupala(secret_key="key!")
        app.state[Authentication] = mock.MagicMock(
            passwords=mock.AsyncMock(
                averify=mock.AsyncMock(return_value=True),
            ),
        )

        user = User(email="root", password="hashed_password")
        user_loader = MemoryUserLoader([user])
        authenticator = HTTPBasicAuthenticator(user_loader)

        conn = HTTPConnection(
            {
                "type": "http",
                "app": app,
                "headers": [
                    (b"authorization", "Basic cm9vdDpjb3JyZWN0X3Bhc3N3b3Jk".encode("utf-8"))
                ],  # root:correct_password
            }
        )

        identity = await authenticator.authenticate(conn)

        assert identity is not None
        assert identity.id == "root"
        assert identity.user == user

    async def test_updates_session_auth_hash(self) -> None:
        app = Kupala(secret_key="key!")
        app.state[Authentication] = mock.MagicMock(
            passwords=mock.AsyncMock(
                averify=mock.AsyncMock(return_value=True),
            ),
        )

        user = User(email="root", password="hashed_password")
        user_loader = MemoryUserLoader([user])
        authenticator = HTTPBasicAuthenticator(user_loader)

        conn = HTTPConnection(
            {
                "type": "http",
                "app": app,
                "headers": [
                    (b"authorization", "Basic cm9vdDpjb3JyZWN0X3Bhc3N3b3Jk".encode("utf-8"))
                ],  # root:correct_password
                "session": {},
            }
        )

        await authenticator.authenticate(conn)
        assert SESSION_HASH_KEY in conn["session"]

    async def test_fails_with_invalid_password(self) -> None:
        app = Kupala(secret_key="key!")
        hasher = PasswordHasher()
        app.state[Authentication] = mock.MagicMock(
            passwords=hasher,
        )

        user = User(email="root", password=hasher.make("secret"))
        user_loader = MemoryUserLoader([user])
        authenticator = HTTPBasicAuthenticator(user_loader)

        conn = HTTPConnection(
            {
                "type": "http",
                "app": app,
                "headers": [(b"authorization", b"Basic cm9vdDpjb3JyZWN0X3Bhc3N3b3Jk")],  # root:correct_password
            }
        )

        assert not await authenticator.authenticate(conn)

    async def test_fails_with_nonexistent_user(self) -> None:
        app = Kupala(secret_key="key!")
        app.state[Authentication] = mock.MagicMock(
            passwords=mock.AsyncMock(spec=PasswordHasher),
        )

        user_loader = MemoryUserLoader([])
        authenticator = HTTPBasicAuthenticator(user_loader)

        conn = HTTPConnection(
            {
                "type": "http",
                "app": app,
                "headers": [(b"authorization", b"Basic cm9vdDpjb3JyZWN0X3Bhc3N3b3Jk")],  # root:correct_password
            }
        )

        assert not await authenticator.authenticate(conn)

    async def test_fails_with_no_authorization_header(self) -> None:
        app = Kupala(secret_key="key!")
        app.state[Authentication] = mock.MagicMock(
            passwords=mock.AsyncMock(spec=PasswordHasher),
        )

        user_loader = MemoryUserLoader([])
        authenticator = HTTPBasicAuthenticator(user_loader)

        conn = HTTPConnection({"type": "http", "app": app, "headers": []})

        assert not await authenticator.authenticate(conn)

    async def test_fails_with_non_basic_auth(self) -> None:
        app = Kupala(secret_key="key!")
        app.state[Authentication] = mock.MagicMock(
            passwords=mock.AsyncMock(spec=PasswordHasher),
        )

        user_loader = MemoryUserLoader([])
        authenticator = HTTPBasicAuthenticator(user_loader)

        conn = HTTPConnection(
            {
                "type": "http",
                "app": app,
                "headers": [(b"authorization", b"Key abc")],
            }
        )

        assert not await authenticator.authenticate(conn)

    async def test_raises_error_with_invalid_basic_header(self) -> None:
        app = Kupala(secret_key="key!")
        app.state[Authentication] = mock.MagicMock(
            passwords=mock.AsyncMock(spec=PasswordHasher),
        )

        user_loader = MemoryUserLoader([])
        authenticator = HTTPBasicAuthenticator(user_loader)

        conn = HTTPConnection(
            {
                "type": "http",
                "app": app,
                "headers": [(b"authorization", b"Basic")],
            }
        )

        with pytest.raises(AuthenticationError, match="Invalid basic header. No credentials provided."):
            assert not await authenticator.authenticate(conn)

    async def test_raises_error_with_invalid_basic_header_spaces(self) -> None:
        app = Kupala(secret_key="key!")
        app.state[Authentication] = mock.MagicMock(
            passwords=mock.AsyncMock(spec=PasswordHasher),
        )

        user_loader = MemoryUserLoader([])
        authenticator = HTTPBasicAuthenticator(user_loader)

        conn = HTTPConnection(
            {
                "type": "http",
                "app": app,
                "headers": [(b"authorization", b"Basic abc abc")],
            }
        )

        with pytest.raises(AuthenticationError, match="Invalid basic header. No spaces allowed."):
            assert not await authenticator.authenticate(conn)

    async def test_raises_error_with_invalid_base64_encoding(self) -> None:
        app = Kupala(secret_key="key!")
        app.state[Authentication] = mock.MagicMock(
            passwords=mock.AsyncMock(spec=PasswordHasher),
        )

        user_loader = MemoryUserLoader([])
        authenticator = HTTPBasicAuthenticator(user_loader)

        conn = HTTPConnection(
            {
                "type": "http",
                "app": app,
                "headers": [(b"authorization", b"Basic abc")],
            }
        )

        with pytest.raises(
            AuthenticationError, match="Invalid basic header. Credentials not correctly base64 encoded."
        ):
            assert not await authenticator.authenticate(conn)

    async def test_extracts_user_scopes(self) -> None:
        app = Kupala(secret_key="key!")
        app.state[Authentication] = mock.MagicMock(
            passwords=mock.AsyncMock(
                averify=mock.AsyncMock(return_value=True),
            ),
        )

        user = User(email="root", password="hashed_password", scopes=["admin"])
        user_loader = MemoryUserLoader([user])
        authenticator = HTTPBasicAuthenticator(user_loader)

        conn = HTTPConnection(
            {
                "type": "http",
                "app": app,
                "headers": [(b"authorization", b"Basic cm9vdDpjb3JyZWN0X3Bhc3N3b3Jk")],  # root:correct_password
            }
        )

        identity = await authenticator.authenticate(conn)
        assert identity
        assert identity.scopes == ["admin"]


class TestDependencies:
    def test_current_user(self) -> None:
        group = RouteGroup()

        @group.get("/")
        async def view(user: CurrentUser[User]) -> Response:
            return Response(user.identity)

        async def user_middleware(request: Request, call_next: CallNext) -> Response:
            request.scope["user"] = User(email="1")
            return await call_next(request)

        app = Kupala(secret_key="key!", routes=group, middleware=[user_middleware])
        with TestClient(app) as client:
            response = client.get("/")
            assert response.text == "1"

    def test_current_user_error(self) -> None:
        group = RouteGroup()

        @group.get("/")
        async def view(user: CurrentUser[User]) -> Response:
            return Response(user.identity)

        async def user_middleware(request: Request, call_next: CallNext) -> Response:
            request.scope["user"] = UnauthenticatedUser()
            return await call_next(request)

        app = Kupala(secret_key="key!", routes=group, middleware=[user_middleware])
        with TestClient(app) as client:
            response = client.get("/")
            assert response.status_code == 401


class TestSQLAlchemyUserLoader:
    async def test_loads_user_by_identity(self, dbsession: AsyncSession) -> None:
        loader = DatabaseUserLoader(User, lambda identity: User.id == identity)
        user = await loader(
            HTTPConnection(
                {
                    "type": "http",
                    "state": {"dbsession": dbsession},
                }
            ),
            "1",
        )
        assert user
        assert user.id == 1

    async def test_not_loads_user_by_identity(self, dbsession: AsyncSession) -> None:
        loader = DatabaseUserLoader(User, lambda identity: User.id == identity)
        user = await loader(
            HTTPConnection(
                {
                    "type": "http",
                    "state": {"dbsession": dbsession},
                }
            ),
            "-1",
        )
        assert not user


class TestBaseUser:
    def test_identity(self) -> None:
        email = uuid.uuid4().hex
        user = User(email=email)
        assert user.identity == email

    def test_display_name(self) -> None:
        user = User(email="1")
        assert user.display_name == "1"

    def test_is_authenticated(self) -> None:
        user = User(email="1")
        assert user.is_authenticated

    def test_is_active(self) -> None:
        user = User(email="1")
        assert user.is_active

    def test_is_not_active(self) -> None:
        user = User(email="1", deactivated_at=datetime.datetime.now(datetime.UTC))
        assert not user.is_active

    def test_get_password_hash(self) -> None:
        user = User(email="1", password="password")
        assert user.get_password_hash() == "password"

    def test_get_scopes(self) -> None:
        user = User(email=uuid.uuid4().hex, scopes=[])
        assert user.get_scopes() == []

    async def test_register(self, dbsession: AsyncSession) -> None:
        email = uuid.uuid4().hex
        spy = mock.AsyncMock()
        async with dbsession.begin_nested():
            user_registered.connect(spy)
            user = await User.register(dbsession, email=email, password_hash="password", name="name")
            await dbsession.commit()

        spy.assert_called_once_with(User, user=user)
        assert user.email == email
