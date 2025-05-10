import io
import os.path

import jinja2
import pytest
from async_storages import FileStorage, MemoryBackend
from starlette.datastructures import UploadFile
from starlette.requests import Request
from starlette.responses import Response
from starlette.testclient import TestClient

from kupala import Kupala
from kupala.files import Files, StaticFiles, static_url
from kupala.routing import Route
from kupala.templating import Templates


class TestStaticFiles:
    def test_static_files(self) -> None:
        app = Kupala(
            secret_key="key!",
            extensions=[
                StaticFiles(packages=[("tests", "assets")]),
            ],
        )
        with TestClient(app) as client:
            response = client.get("/static/somefile.txt")
            assert response.status_code == 200
            assert response.headers["content-type"] == "text/plain; charset=utf-8"
            assert response.text == "somecontent\n"

    def test_static_files_directory(self) -> None:
        this_dir = os.path.dirname(__file__)
        app = Kupala(
            secret_key="key!",
            extensions=[
                StaticFiles(directory=os.path.join(this_dir, "assets")),
            ],
        )
        with TestClient(app) as client:
            response = client.get("/static/somefile.txt")
            assert response.status_code == 200
            assert response.headers["content-type"] == "text/plain; charset=utf-8"
            assert response.text == "somecontent\n"

    def test_static_files_default_route_name(self) -> None:
        app = Kupala(
            secret_key="key!",
            extensions=[
                StaticFiles(packages=[("tests", "assets")]),
            ],
        )
        url = app.url_path_for("static", path="somefile.txt")
        assert url == "/static/somefile.txt"

    def test_static_files_route_name(self) -> None:
        app = Kupala(
            secret_key="key!",
            extensions=[
                StaticFiles(route_name="assets", packages=[("tests", "assets")]),
            ],
        )
        url = app.url_path_for("assets", path="somefile.txt")
        assert url == "/static/somefile.txt"

    def test_static_files_default_url_prefix(self) -> None:
        app = Kupala(
            secret_key="key!",
            extensions=[
                StaticFiles(packages=[("tests", "assets")]),
            ],
        )
        url = app.url_path_for("static", path="somefile.txt")
        assert url == "/static/somefile.txt"

    def test_static_files_url_prefix(self) -> None:
        app = Kupala(
            secret_key="key!",
            extensions=[
                StaticFiles(url_prefix="/assets", packages=[("tests", "assets")]),
            ],
        )
        url = app.url_path_for("static", path="somefile.txt")
        assert url == "/assets/somefile.txt"

    def test_template_helper(self) -> None:
        async def view(request: Request) -> Response:
            return Templates.of(request.app).render_to_response(request, "index.html")

        app = Kupala(
            secret_key="key!",
            routes=[Route("/", view)],
            extensions=[
                Templates(
                    template_loaders=[jinja2.DictLoader({"index.html": "{{ static_url('somefile.txt') }}"})],
                ),
                StaticFiles(url_prefix="/assets", packages=[("tests", "assets")]),
            ],
        )
        with TestClient(app) as client:
            response = client.get("/")
            assert response.status_code == 200
            assert response.text.startswith("http://testserver/assets/somefile.txt")


class TestStaticUrl:
    @pytest.fixture
    def http_request(self) -> Request:
        return Request(
            {
                "type": "http",
                "method": "GET",
                "url": "http://testserver/",
                "headers": [],
                "server": ("testserver", 80),
                "path": "/",
                "app": Kupala(secret_key="key!", extensions=[StaticFiles(packages=[("tests", "assets")])]),
            }
        )

    def test_generates_url(self, http_request: Request) -> None:
        url = static_url(http_request, "/image.jpg")
        assert url.path == "/static/image.jpg"

    def test_cache_prefix_no_debug(self, http_request: Request) -> None:
        http_request.app.debug = False
        url = static_url(http_request, "/image.jpg")
        url2 = static_url(http_request, "/image.jpg")
        assert url == url2

    def test_cache_prefix_debug(self, http_request: Request) -> None:
        http_request.app.debug = True
        url = static_url(http_request, "/image.jpg")
        url2 = static_url(http_request, "/image.jpg")
        assert url != url2

    @pytest.mark.parametrize("image_url", ["http://example.com/image.jpg", "https://example.com/image.jpg"])
    def test_ignores_http(self, http_request: Request, image_url: str) -> None:
        url = static_url(http_request, image_url)
        assert url == url


class TestFiles:
    async def test_serves_files(self) -> None:
        files = Files(
            default="memory",
            storages={
                "memory": FileStorage(MemoryBackend()),
            },
        )
        app = Kupala(
            secret_key="key!",
            extensions=[files],
        )
        await files.write("somefile.txt", b"somecontent\n")
        with TestClient(app) as client:
            response = client.get("/media/somefile.txt")
            assert response.status_code == 200
            assert response.headers["content-type"] == "text/plain; charset=utf-8"
            assert response.text == "somecontent\n"

    async def test_serves_files_custom_route_name(self) -> None:
        files = Files(
            default="memory",
            route_name="files",
            storages={
                "memory": FileStorage(MemoryBackend()),
            },
        )
        app = Kupala(
            secret_key="key!",
            extensions=[files],
        )
        url = app.url_path_for("files", path="somefile.txt")
        assert url == "/media/somefile.txt"

    async def test_serves_files_custom_url_prefix(self) -> None:
        files = Files(
            default="memory",
            url_prefix="/files",
            storages={
                "memory": FileStorage(MemoryBackend()),
            },
        )
        app = Kupala(
            secret_key="key!",
            extensions=[files],
        )
        url = app.url_path_for("media", path="somefile.txt")
        assert url == "/files/somefile.txt"

    async def test_serves_files_custom_default(self) -> None:
        files = Files(
            default="second",
            url_prefix="/files",
            storages={
                "memory": FileStorage(MemoryBackend()),
                "second": FileStorage(MemoryBackend()),
            },
        )
        app = Kupala(
            secret_key="key!",
            extensions=[files],
        )
        url = app.url_path_for("media", path="somefile.txt")
        assert url == "/files/somefile.txt"

    async def test_serves_files_invalid_default(self) -> None:
        with pytest.raises(AssertionError):
            Files(
                default="missing",
                url_prefix="/files",
                storages={
                    "memory": FileStorage(MemoryBackend()),
                },
            )


class TestFilesMethodsIntegration:
    @pytest.fixture
    async def files_instance(self) -> Files:
        return Files(
            default="memory",
            storages={"memory": FileStorage(MemoryBackend())},
        )

    async def test_write_and_exists(self, files_instance: Files) -> None:
        await files_instance.write("test.txt", b"test content")
        assert await files_instance.exists("test.txt")
        assert not await files_instance.exists("nonexistent.txt")

    async def test_open_and_read(self, files_instance: Files) -> None:
        await files_instance.write("test.txt", b"test content")
        async with await files_instance.open("test.txt") as file:
            content = await file.read()
            assert content == b"test content"

    async def test_readlines(self, files_instance: Files) -> None:
        await files_instance.write("test.txt", b"line1\nline2\nline3")
        lines = []
        async for line in await files_instance.readlines("test.txt"):
            lines.append(line)
        assert lines == [b"line1\n", b"line2\n", b"line3"]

    async def test_delete(self, files_instance: Files) -> None:
        await files_instance.write("test.txt", b"test content")
        assert await files_instance.exists("test.txt")
        await files_instance.delete("test.txt")
        assert not await files_instance.exists("test.txt")

    async def test_delete_many(self, files_instance: Files) -> None:
        await files_instance.write("file1.txt", b"content1")
        await files_instance.write("file2.txt", b"content2")
        assert await files_instance.exists("file1.txt")
        assert await files_instance.exists("file2.txt")
        await files_instance.delete_many(["file1.txt", "file2.txt"])
        assert not await files_instance.exists("file1.txt")
        assert not await files_instance.exists("file2.txt")

    async def test_upload(self, files_instance: Files) -> None:
        upload_file = UploadFile(io.BytesIO(b"test content"), filename="test.txt")

        file_path = await files_instance.upload(upload_file, "uploads")
        assert await files_instance.exists(file_path)
        async with await files_instance.open(file_path) as file:
            content = await file.read()
            assert content == b"test content"

    async def test_get_storage(self, files_instance: Files) -> None:
        storage = files_instance.get_storage("memory")
        assert isinstance(storage, FileStorage)

    async def test_of_method(self) -> None:
        files = Files(
            default="memory",
            storages={"memory": FileStorage(MemoryBackend())},
        )
        app = Kupala(
            secret_key="key!",
            extensions=[files],
        )
        assert Files.of(app) is files
