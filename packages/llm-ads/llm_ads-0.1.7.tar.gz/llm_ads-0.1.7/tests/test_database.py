import pytest
import pytest_asyncio
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.models.campaign import Campaign
from app.models.ad import Ad

@pytest_asyncio.fixture(scope="function")
async def test_db():
    """
    Create a test database session for running tests.
    Uses an in-memory SQLite database for testing.
    """
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session
        await session.rollback()
        
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()

@pytest.mark.asyncio
async def test_create_campaign(test_db: AsyncSession):
    """Test creating a new campaign"""
    campaign = Campaign(
        title="Test Campaign",
        description="Test Description",
        budget=1000.0,
        status="active"
    )
    
    test_db.add(campaign)
    await test_db.commit()
    await test_db.refresh(campaign)
    
    assert campaign.id is not None
    assert campaign.title == "Test Campaign"
    assert campaign.budget == 1000.0

@pytest.mark.asyncio
async def test_create_ad_with_campaign(test_db: AsyncSession):
    """Test creating an ad associated with a campaign"""
    # Create a campaign first
    campaign = Campaign(
        title="Test Campaign",
        description="Test Description",
        budget=1000.0,
        status="active"
    )
    test_db.add(campaign)
    await test_db.commit()
    await test_db.refresh(campaign)
    
    # Create an ad associated with the campaign
    ad = Ad(
        title="Test Ad",
        content="Test Content",
        campaign_id=campaign.id,
        status="active",
        target_audience="general"
    )
    test_db.add(ad)
    await test_db.commit()
    await test_db.refresh(ad)
    
    assert ad.id is not None
    assert ad.campaign_id == campaign.id
    assert ad.title == "Test Ad"

@pytest.mark.asyncio
async def test_query_campaign(test_db: AsyncSession):
    """Test querying campaigns"""
    # Create test campaigns
    campaigns = [
        Campaign(title=f"Campaign {i}", 
                description=f"Description {i}", 
                budget=1000.0 * i,
                status="active")
        for i in range(3)
    ]
    
    for campaign in campaigns:
        test_db.add(campaign)
    await test_db.commit()
    
    # Query all campaigns
    result = await test_db.execute(select(Campaign))
    db_campaigns = result.scalars().all()
    assert len(db_campaigns) == 3
    
    # Query specific campaign
    result = await test_db.execute(
        select(Campaign).where(Campaign.title == "Campaign 1")
    )
    campaign = result.scalar_one_or_none()
    assert campaign is not None
    assert campaign.budget == 1000.0 