import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session
from app.main import app

@pytest.mark.asyncio
async def test_create_short_url(client: AsyncClient, test_db: Session):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/shorten", json={"url": "https://example.com"})
        assert response.status_code == 200
        assert "short_url" in response.json()

@pytest.mark.asyncio
async def test_redirect_url(client: AsyncClient, test_db: Session):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/shorten", json={"url": "https://example.com"})
        assert response.status_code == 200
        short_url = response.json()["short_url"]
        short_key = short_url.split("/")[-1]

        response = await ac.get(f"/{short_key}", follow_redirects=False)
        assert response.status_code in [200, 307]
        if response.status_code == 307:
            assert response.headers["location"] == "https://example.com"

@pytest.mark.asyncio
async def test_get_url_stats(client: AsyncClient, test_db: Session):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/shorten", json={"url": "https://example.com"})
        assert response.status_code == 200
        short_url = response.json()["short_url"]
        short_key = short_url.split("/")[-1]

        response = await ac.get(f"/stats/{short_key}")
        assert response.status_code == 200
        assert response.json()["click_count"] >= 0
