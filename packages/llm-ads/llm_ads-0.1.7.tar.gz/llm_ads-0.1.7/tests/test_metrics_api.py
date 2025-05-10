import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
import json
from datetime import datetime, timedelta

from app.routers.placement_metrics_routes import router as metrics_router
from app.services.performance_tracker import AdPerformanceTracker
from app.auth import get_current_user, UserRole, User

# Mock authenticated user for testing
async def get_test_publisher():
    """Mock authenticated publisher user for testing."""
    test_user = User(
        id=1,
        email="test@example.com",
        name="Test Publisher",
        role=UserRole.PUBLISHER,
        publisher_id="test-publisher",
        is_active=True
    )
    return test_user

# Mock admin user for testing
async def get_test_admin():
    """Mock authenticated admin user for testing."""
    test_user = User(
        id=2,
        email="admin@example.com",
        name="Test Admin",
        role=UserRole.ADMIN,
        publisher_id=None,
        is_active=True
    )
    return test_user

class TestMetricsAPI:
    """Tests for the metrics collection API."""
    
    @pytest.fixture
    def publisher_app(self):
        """Create a FastAPI app with publisher authentication for testing."""
        app = FastAPI()
        app.include_router(metrics_router)
        
        # Override the authentication dependency
        app.dependency_overrides[get_current_user] = get_test_publisher
        
        return app
    
    @pytest.fixture
    def admin_app(self):
        """Create a FastAPI app with admin authentication for testing."""
        app = FastAPI()
        app.include_router(metrics_router)
        
        # Override the authentication dependency
        app.dependency_overrides[get_current_user] = get_test_admin
        
        return app
    
    @pytest.fixture
    def publisher_client(self, publisher_app):
        """Create a test client with publisher authentication."""
        return TestClient(publisher_app)
    
    @pytest.fixture
    def admin_client(self, admin_app):
        """Create a test client with admin authentication."""
        return TestClient(admin_app)
    
    def test_get_metrics_by_type_publisher(self, publisher_client):
        """Test that publishers can access their own metrics."""
        # Mock return value for get_metrics_by_placement_type
        mock_metrics = [
            {
                "placement_type": "inline",
                "impressions": 100,
                "clicks": 10,
                "conversions": 2,
                "click_through_rate": 0.1,
                "conversion_rate": 0.2
            },
            {
                "placement_type": "after",
                "impressions": 200,
                "clicks": 15,
                "conversions": 3,
                "click_through_rate": 0.075,
                "conversion_rate": 0.2
            }
        ]
        
        # Patch the AdPerformanceTracker.get_metrics_by_placement_type method
        with patch.object(
            AdPerformanceTracker, 
            'get_metrics_by_placement_type', 
            new_callable=AsyncMock,
            return_value=mock_metrics
        ):
            # Make the request
            response = publisher_client.get("/placement-metrics/by-type")
            
            # Check that the response is successful
            assert response.status_code == 200
            
            # Check that the response contains the mock metrics
            data = response.json()
            assert "results" in data
            assert len(data["results"]) == 2
            assert data["results"][0]["placement_type"] == "inline"
            assert data["results"][0]["impressions"] == 100
            assert data["results"][1]["placement_type"] == "after"
            assert data["results"][1]["impressions"] == 200
    
    def test_get_metrics_by_type_with_filters(self, publisher_client):
        """Test filtering metrics by placement type and date range."""
        # Mock return value for get_metrics_by_placement_type
        mock_metrics = [
            {
                "placement_type": "inline",
                "impressions": 100,
                "clicks": 10,
                "conversions": 2,
                "click_through_rate": 0.1,
                "conversion_rate": 0.2
            }
        ]
        
        # Patch the AdPerformanceTracker.get_metrics_by_placement_type method
        with patch.object(
            AdPerformanceTracker, 
            'get_metrics_by_placement_type', 
            new_callable=AsyncMock,
            return_value=mock_metrics
        ) as mock_method:
            # Make the request with filters
            from_date = (datetime.now() - timedelta(days=7)).isoformat()
            to_date = datetime.now().isoformat()
            
            response = publisher_client.get(
                f"/placement-metrics/by-type?placement_type=inline&from_date={from_date}&to_date={to_date}"
            )
            
            # Check that the response is successful
            assert response.status_code == 200
            
            # Check that the method was called with the right parameters
            call_args = mock_method.call_args[1]
            assert call_args["publisher_id"] == "test-publisher"
            assert call_args["placement_type"] == "inline"
            assert isinstance(call_args["from_date"], datetime)
            assert isinstance(call_args["to_date"], datetime)
    
    def test_record_click(self, publisher_client):
        """Test recording an ad click."""
        # Mock return value for record_click
        mock_metrics = {
            "id": 1,
            "publisher_id": "test-publisher",
            "ad_id": "test-ad",
            "placement_type": "inline",
            "impressions": 100,
            "clicks": 11,  # Incremented
            "conversions": 2,
            "click_through_rate": 0.11,
            "conversion_rate": 0.1818
        }
        
        # Patch the AdPerformanceTracker.record_click method
        with patch.object(
            AdPerformanceTracker, 
            'record_click', 
            new_callable=AsyncMock,
            return_value=mock_metrics
        ) as mock_method:
            # Make the request
            response = publisher_client.post(
                "/placement-metrics/record-click/test-ad?placement_type=inline"
            )
            
            # Check that the response is successful
            assert response.status_code == 200
            
            # Check that the method was called with the right parameters
            call_args = mock_method.call_args[1]
            assert call_args["publisher_id"] == "test-publisher"
            assert call_args["ad_id"] == "test-ad"
            assert call_args["placement_type"] == "inline"
            
            # Check the response data
            data = response.json()
            assert data["success"] is True
            assert data["metrics"]["clicks"] == 11
            assert data["metrics"]["impressions"] == 100
            assert data["metrics"]["click_through_rate"] == 0.11
    
    def test_unauthorized_access(self, admin_app):
        """Test that unauthorized users cannot access metrics."""
        # Create a client without authentication override
        unauthenticated_client = TestClient(FastAPI())
        unauthenticated_client.app.include_router(metrics_router)
        
        # Try to access metrics
        response = unauthenticated_client.get("/placement-metrics/by-type")
        
        # Check that the response is unauthorized (depends on how your auth is set up)
        # This might be 401 (Unauthorized) or 403 (Forbidden)
        assert response.status_code in (401, 403) 