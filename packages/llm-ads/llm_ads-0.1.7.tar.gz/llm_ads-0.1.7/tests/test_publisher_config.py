import pytest
import asyncio
from fastapi import FastAPI
from starlette.testclient import TestClient
from httpx import AsyncClient
import json
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.models.database import Base
from app.models.publisher_config import PublisherConfig
from app.models.publisher import Publisher
from app.schemas.publisher_config import PublisherConfigCreate, PublisherConfigResponse
from app.routers.publisher_config_routes import router as publisher_config_router
from app.auth import get_current_user, UserRole, User

# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create async engine
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create session
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

# Dependency override
async def get_test_db():
    async with TestingSessionLocal() as session:
        yield session

async def get_test_current_user():
    """Mock authenticated user for testing."""
    test_user = User(
        id=1,
        email="test@example.com",
        name="Test User",
        role=UserRole.PUBLISHER,
        publisher_id="test-publisher",
        is_active=True
    )
    return test_user

# Create tables
@pytest.fixture(scope="module")
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Seed test data
    async with TestingSessionLocal() as session:
        publisher = Publisher(
            publisher_id="test-publisher",
            name="Test Publisher",
            email="test@example.com"
        )
        session.add(publisher)
        await session.commit()

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# Create test app
@pytest.fixture(scope="module")
def test_app():
    app = FastAPI()
    app.include_router(publisher_config_router)
    
    # Override dependencies
    app.dependency_overrides[get_current_user] = get_test_current_user
    
    # Run setup
    return app

@pytest.fixture(scope="module")
def client(test_app):
    return TestClient(test_app)

# Tests
@pytest.mark.asyncio
async def test_create_publisher_config(setup_db, test_app):
    """Test creating a new publisher configuration."""
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        config_data = {
            "ad_placement_mode": "inline",
            "max_ads": 2,
            "inline_config": {
                "max_insertions": 1,
                "insertion_strategy": "discourse",
                "blend_style": "soft",
                "insert_after_paragraphs": 1,
                "tone_matching": True,
                "skip_on_factual": True
            }
        }
        
        response = await ac.post("/publisher-configs/", json=config_data)
        assert response.status_code == 200
        data = response.json()
        
        assert data["ad_placement_mode"] == "inline"
        assert data["max_ads"] == 2
        assert data["inline_config"]["skip_on_factual"] == True
        assert data["publisher_id"] == "test-publisher"

@pytest.mark.asyncio
async def test_get_publisher_config(setup_db, test_app):
    """Test retrieving publisher configuration."""
    # First create a config
    async with TestingSessionLocal() as session:
        config = PublisherConfig(
            publisher_id="test-publisher",
            ad_placement_mode="before",
            max_ads=3,
            debug_mode=True
        )
        session.add(config)
        await session.commit()
        config_id = config.id
    
    # Now test retrieval
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        response = await ac.get(f"/publisher-configs/{config_id}")
        assert response.status_code == 200
        data = response.json()
        
        assert data["ad_placement_mode"] == "before"
        assert data["max_ads"] == 3
        assert data["debug_mode"] == True

@pytest.mark.asyncio
async def test_update_publisher_config(setup_db, test_app):
    """Test updating publisher configuration."""
    # First create a config
    async with TestingSessionLocal() as session:
        config = PublisherConfig(
            publisher_id="test-publisher",
            ad_placement_mode="after",
            max_ads=1
        )
        session.add(config)
        await session.commit()
        config_id = config.id
    
    # Now test update
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        update_data = {
            "ad_placement_mode": "inline",
            "inline_config": {
                "max_insertions": 2,
                "blend_style": "branded"
            }
        }
        
        response = await ac.put(f"/publisher-configs/{config_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        
        assert data["ad_placement_mode"] == "inline"
        assert data["max_ads"] == 1  # Unchanged
        assert data["inline_config"]["max_insertions"] == 2
        assert data["inline_config"]["blend_style"] == "branded"

@pytest.mark.asyncio
async def test_delete_publisher_config(setup_db, test_app):
    """Test deleting publisher configuration."""
    # First create a config
    async with TestingSessionLocal() as session:
        config = PublisherConfig(
            publisher_id="test-publisher",
            ad_placement_mode="after"
        )
        session.add(config)
        await session.commit()
        config_id = config.id
    
    # Now test delete
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        response = await ac.delete(f"/publisher-configs/{config_id}")
        assert response.status_code == 204
        
        # Verify it's gone
        response = await ac.get(f"/publisher-configs/{config_id}")
        assert response.status_code == 404 