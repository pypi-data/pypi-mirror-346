import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from unittest.mock import patch, MagicMock
import json
from datetime import datetime

from app.schemas.ad_strategist import (
    AdStrategyRequest,
    InputMethod,
    CampaignGoal,
    AdFormat,
    TargetAudienceAttributes,
    CampaignStrategy,
    AdVariant
)
from app.models.ad_strategist import AdStrategy, AdVariant as AdVariantModel
from app.main import app
from app.models.database import get_async_session

# Mock data for testing
mock_target_audience = TargetAudienceAttributes(
    age_range=["25-34", "35-44"],
    gender=["Male", "Female"],
    interests=["Technology", "Finance"]
)

mock_strategy_request = {
    "input_method": InputMethod.URL,
    "product_url": "https://example.com/product",
    "campaign_goals": [CampaignGoal.CONVERSION, CampaignGoal.ENGAGEMENT],
    "target_audience": mock_target_audience.dict(),
    "ad_formats": [AdFormat.SOCIAL_MEDIA_POST, AdFormat.SEARCH_AD],
    "tone": "Professional"
}

mock_campaign_strategy = {
    "main_selling_points": ["Feature 1", "Feature 2"],
    "target_keywords": ["keyword1", "keyword2"],
    "messaging_approach": "Feature-focused",
    "tone_and_voice": "Professional and informative",
    "value_proposition": "Save time and increase productivity"
}

mock_ad_variant = {
    "format": AdFormat.SOCIAL_MEDIA_POST,
    "title": "Try Our Product",
    "content": "This is a great product that helps you save time.",
    "call_to_action": "Buy Now",
    "target_platform": "Facebook"
}

mock_url_analysis_result = {
    "title": "Product Title",
    "description": "Product description",
    "keywords": ["keyword1", "keyword2"],
    "main_features": ["feature1", "feature2"],
    "pricing_info": "$99.99"
}

# Fixtures
@pytest.fixture
def mock_analyze_url():
    with patch('app.services.llm_integration.analyze_url') as mock:
        mock.return_value = mock_url_analysis_result
        yield mock

@pytest.fixture
def mock_generate_campaign_strategy():
    with patch('app.services.llm_integration.generate_campaign_strategy') as mock:
        mock.return_value = CampaignStrategy(**mock_campaign_strategy)
        yield mock

@pytest.fixture
def mock_generate_ad_variants():
    with patch('app.services.llm_integration.generate_ad_variants') as mock:
        mock.return_value = [AdVariant(**mock_ad_variant)]
        yield mock

@pytest.fixture
def mock_get_current_user():
    with patch('app.auth.get_current_user') as mock:
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.role = "advertiser"
        mock.return_value = mock_user
        yield mock

# Unit Tests
@pytest.mark.asyncio
async def test_analyze_url(mock_analyze_url, mock_get_current_user):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/ad-strategist/analyze-url?url=https://example.com/product")
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == mock_url_analysis_result["title"]
        assert data["description"] == mock_url_analysis_result["description"]
        assert data["keywords"] == mock_url_analysis_result["keywords"]

@pytest.mark.asyncio
async def test_create_strategy(
    mock_generate_campaign_strategy, 
    mock_generate_ad_variants, 
    mock_get_current_user
):
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Mock the database session
        with patch('app.models.database.get_async_session') as mock_session:
            mock_session.return_value = MagicMock(spec=AsyncSession)
            
            response = await client.post(
                "/ad-strategist/",
                json=mock_strategy_request
            )
            
            assert response.status_code == 201
            data = response.json()
            assert data["strategy"]["value_proposition"] == mock_campaign_strategy["value_proposition"]
            assert len(data["ad_variants"]) == 1
            assert data["ad_variants"][0]["format"] == mock_ad_variant["format"]

@pytest.mark.asyncio
async def test_list_strategies(mock_get_current_user):
    mock_strategies = [
        {
            "id": 1,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "input_method": "url",
            "campaign_brief": None,
            "product_url": "https://example.com/product",
            "campaign_goals": ["conversion", "engagement"],
            "ad_formats": ["social_media_post", "search_ad"],
            "value_proposition": "Save time and increase productivity",
            "variant_count": 2
        }
    ]
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Mock the ad_strategist_service.list_ad_strategies function
        with patch('app.services.ad_strategist_service.list_ad_strategies') as mock_list:
            mock_list.return_value = mock_strategies
            
            response = await client.get("/ad-strategist/")
            
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert data[0]["id"] == mock_strategies[0]["id"]
            assert data[0]["value_proposition"] == mock_strategies[0]["value_proposition"]

@pytest.mark.asyncio
async def test_get_strategy(mock_get_current_user):
    mock_strategy = {
        "id": 1,
        "user_id": 1,
        "request": mock_strategy_request,
        "strategy": mock_campaign_strategy,
        "ad_variants": [mock_ad_variant],
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Mock the ad_strategist_service.get_ad_strategy function
        with patch('app.services.ad_strategist_service.get_ad_strategy') as mock_get:
            mock_get.return_value = mock_strategy
            
            response = await client.get("/ad-strategist/1")
            
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == mock_strategy["id"]
            assert data["strategy"]["value_proposition"] == mock_strategy["strategy"]["value_proposition"]
            assert len(data["ad_variants"]) == 1

@pytest.mark.asyncio
async def test_track_variant_performance(mock_get_current_user):
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Mock the ad_strategist_service.update_ad_variant_performance function
        with patch('app.services.ad_strategist_service.update_ad_variant_performance') as mock_update:
            mock_update.return_value = True
            
            response = await client.post("/ad-strategist/variants/1/performance?impressions=10&clicks=2")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            mock_update.assert_called_once_with(1, 10, 2, None)

@pytest.mark.asyncio
async def test_delete_strategy(mock_get_current_user):
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Mock the ad_strategist_service.delete_ad_strategy function
        with patch('app.services.ad_strategist_service.delete_ad_strategy') as mock_delete:
            mock_delete.return_value = True
            
            response = await client.delete("/ad-strategist/1")
            
            assert response.status_code == 204
            mock_delete.assert_called_once_with(1, 1, None) 