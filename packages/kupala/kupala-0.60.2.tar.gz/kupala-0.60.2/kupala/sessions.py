import datetime
import typing

from starlette.middleware import Middleware
from starsessions import (
    CookieStore,
    ImproperlyConfigured,
    InMemoryStore,
    JsonSerializer,
    Serializer,
    SessionAutoloadMiddleware,
    SessionError,
    SessionMiddleware,
    SessionNotLoaded,
    SessionStore,
    generate_session_id,
    get_session_handler,
    get_session_id,
    get_session_metadata,
    get_session_remaining_seconds,
    regenerate_session_id,
)

from kupala import Kupala

try:
    from starsessions.stores.redis import RedisStore  # type: ignore[import]
except ImportError:

    class RedisStore:
        def __init__(self, *args, **kwargs):
            raise ImproperlyConfigured(
                "RedisStore requires the `redis` package. "
                "Install it with `pip install starsessions[redis]`."
            )


__all__ = [
    "Sessions",
    "SessionMiddleware",
    "SessionAutoloadMiddleware",
    "SessionStore",
    "JsonSerializer",
    "Serializer",
    "Middleware",
    "get_session_handler",
    "generate_session_id",
    "get_session_id",
    "get_session_metadata",
    "get_session_remaining_seconds",
    "ImproperlyConfigured",
    "CookieStore",
    "InMemoryStore",
    "SessionError",
    "SessionNotLoaded",
    "RedisStore",
    "regenerate_session_id",
]


class Sessions:
    def __init__(
        self,
        store: SessionStore,
        *,
        autoload: bool = False,
        autoload_patterns: list[str | typing.Pattern[str]] | None = None,
        rolling: bool = True,
        lifetime: datetime.timedelta = datetime.timedelta(days=14),
        cookie_name: str = "session",
        cookie_same_site: str = "lax",
        cookie_https_only: bool = True,
        cookie_domain: str | None = None,
        cookie_path: str = "/",
        serializer: Serializer | None = None,
    ) -> None:
        self.rolling = rolling
        self.store = store
        self.lifetime = lifetime
        self.cookie_name = cookie_name
        self.cookie_same_site = cookie_same_site
        self.cookie_https_only = cookie_https_only
        self.cookie_domain = cookie_domain
        self.cookie_path = cookie_path
        self.serializer = serializer or JsonSerializer()
        self.autoload = autoload
        self.autoload_patterns = autoload_patterns or []

    def configure(self, app: Kupala) -> None:
        app.asgi_middleware.append(
            Middleware(
                SessionMiddleware,
                store=self.store,
                lifetime=self.lifetime,
                rolling=self.rolling,
                cookie_name=self.cookie_name,
                cookie_same_site=self.cookie_same_site,
                cookie_https_only=self.cookie_https_only,
                cookie_domain=self.cookie_domain,
                cookie_path=self.cookie_path,
                serializer=self.serializer,
            ),
        )
        if self.autoload:
            app.asgi_middleware.append(
                Middleware(SessionAutoloadMiddleware, paths=self.autoload_patterns)
            )
