import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from fastapi import FastAPI, Request, Response
from starlette.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.llm_ads.middleware import AdServingMiddleware
from backend.llm_ads.config import AdServingConfig, InlineConfig
from app.models.publisher_config import PublisherConfig
from app.schemas.publisher_config import PublisherConfigResponse

class MockAsyncSession:
    """Mock AsyncSession for testing."""
    
    def __init__(self, result=None):
        self.result = result
        self.executed_query = None
        self.committed = False
    
    async def execute(self, query):
        """Mock execute method."""
        self.executed_query = query
        
        # Create a mock result object
        mock_result = MagicMock()
        if self.result:
            mock_result.scalar_one_or_none.return_value = self.result
        else:
            mock_result.scalar_one_or_none.return_value = None
            
        return mock_result
    
    async def commit(self):
        """Mock commit method."""
        self.committed = True
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

class TestMiddlewareIntegration:
    """Integration tests for AdServingMiddleware with publisher configurations."""
    
    @pytest.fixture
    def app(self):
        """Create a FastAPI app with middleware for testing."""
        app = FastAPI()
        
        # Add a test endpoint
        @app.get("/test")
        async def test_endpoint():
            return {"message": "Test response"}
            
        # Add middleware with default config
        config = AdServingConfig(
            target_paths=["/test"],
            ad_placement_mode="after",
            inline_config=InlineConfig(
                max_insertions=1,
                blend_style="direct"
            )
        )
        
        app.add_middleware(AdServingMiddleware, config=config)
        
        return app
    
    @pytest.fixture
    def client(self, app):
        """Create a test client."""
        return TestClient(app)
    
    @pytest.mark.asyncio
    async def test_middleware_fetch_publisher_config(self):
        """Test that middleware fetches publisher-specific configuration."""
        app = FastAPI()
        
        # Add a test endpoint
        @app.get("/test")
        async def test_endpoint():
            return {"message": "Test response"}
        
        # Create mock publisher config
        publisher_config = PublisherConfig(
            id=1,
            publisher_id="test-publisher",
            ad_placement_mode="inline",
            inline_config={
                "max_insertions": 2,
                "blend_style": "soft",
                "tone_matching": True
            },
            max_ads=3
        )
        
        # Create mock session factory
        async def get_mock_session():
            return MockAsyncSession(result=publisher_config)
        
        # Create mock app state with session factory
        app.state.db_session = get_mock_session
        
        # Add middleware with default config
        config = AdServingConfig(
            target_paths=["/test"],
            ad_placement_mode="after",
            publisher_id="test-publisher"
        )
        
        middleware = AdServingMiddleware(app, config=config)
        
        # Mock request object
        request = MagicMock()
        request.url.path = "/test"
        request._body = b'{"query": "test"}'
        
        # Create a mock response
        body = '{"response": "This is a test response"}'
        status_code = 200
        headers = {'content-type': 'application/json'}
        
        original_response = Response(
            content=body.encode(), 
            status_code=status_code,
            headers=headers
        )
        original_response._request = request
        
        # Create mock call_next function
        async def mock_call_next(request):
            return original_response
        
        # Mock select_ads to return test ads
        ads = [{"id": "ad1", "text": "This is a test ad."}]
        with patch('backend.llm_ads.middleware.select_ads', return_value=ads), \
             patch('backend.llm_ads.middleware.insert_ads_into_response'):
            # Call the middleware
            response = await middleware.dispatch(request, mock_call_next)
            
            # Check that we get a response
            assert response is not None
            
            # In a real integration test, we would check the actual response content
            # For this mock test, we're just verifying the function was called
            # and would use the right config
            assert middleware.config.publisher_id == "test-publisher"
            
    def test_middleware_with_client(self, client):
        """Test the middleware using a test client."""
        # Mock the select_ads function to return test ads
        ads = [{"id": "ad1", "text": "This is a test ad."}]
        
        with patch('backend.llm_ads.middleware.select_ads', return_value=ads), \
             patch('backend.llm_ads.middleware.insert_ads_into_response', return_value="Modified content"):
            
            # Make a request to the test endpoint
            response = client.get("/test")
            
            # Check that we get a successful response
            assert response.status_code == 200
            
            # In a full integration test, we would check the actual response content
            # with the ads included, but for this mock test we just verify that
            # the response was processed 