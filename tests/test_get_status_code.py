import pytest

from main import get_status_codes

from aiohttp import ClientSession


class MockResponse:
    def __init__(self, status_code, method):
        self.status = status_code
        self.method = method


class MockContextManager:
    def __init__(self, code, method):
        self.code = code
        self.method = method

    async def __aenter__(self):
        return MockResponse(self.code, self.method)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return None


@pytest.mark.asyncio
async def test_send_not_url_string():
    res = await get_status_codes("some string")
    assert res is None


# @pytest.mark.skip
@pytest.mark.asyncio
async def test_send_url():
    res = await get_status_codes("https://www.google.com/")
    assert res == {"https://www.google.com/": {"GET": 200, "HEAD": 200}}


@pytest.mark.asyncio
async def test_send_url_mock(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockContextManager(200, "GET")

    def mock_post(*args, **kwargs):
        return MockContextManager(405, "POST")

    def mock_put(*args, **kwargs):
        return MockContextManager(405, "PUT")

    def mock_patch(*args, **kwargs):
        return MockContextManager(405, "PATCH")

    def mock_delete(*args, **kwargs):
        return MockContextManager(405, "DELETE")

    def mock_head(*args, **kwargs):
        return MockContextManager(200, "HEAD")

    def mock_options(*args, **kwargs):
        return MockContextManager(405, "OPTIONS")

    monkeypatch.setattr(ClientSession, "get", mock_get)
    monkeypatch.setattr(ClientSession, "post", mock_post)
    monkeypatch.setattr(ClientSession, "put", mock_put)
    monkeypatch.setattr(ClientSession, "patch", mock_patch)
    monkeypatch.setattr(ClientSession, "delete", mock_delete)
    monkeypatch.setattr(ClientSession, "head", mock_head)
    monkeypatch.setattr(ClientSession, "options", mock_options)

    res = await get_status_codes("https://www.google.com/")
    assert res == {"https://www.google.com/": {"GET": 200, "HEAD": 200}}
