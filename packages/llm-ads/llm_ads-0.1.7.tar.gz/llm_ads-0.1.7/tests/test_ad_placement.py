import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import Response
from backend.llm_ads.middleware import AdServingMiddleware
from backend.llm_ads.config import AdServingConfig, InlineConfig

class TestAdPlacementEngine:
    """Tests for the ad placement engine functionality."""
    
    @pytest.fixture
    def middleware(self):
        """Create a middleware instance for testing."""
        app = MagicMock()
        config = AdServingConfig(
            ad_placement_mode="after",
            inline_config=InlineConfig(
                max_insertions=1,
                insertion_strategy="discourse",
                blend_style="soft",
                insert_after_paragraphs=1,
                tone_matching=True,
                skip_on_factual=True
            )
        )
        middleware = AdServingMiddleware(app, config)
        return middleware
    
    @pytest.mark.asyncio
    async def test_append_ads(self, middleware):
        """Test appending ads to the response."""
        # Create a response
        response = Response(content="This is a test response.", media_type="text/plain")
        
        # Create sample ads
        ads = [
            {"id": "ad1", "text": "This is an ad."},
            {"id": "ad2", "text": "This is another ad."}
        ]
        
        # Apply the placement
        result = await middleware._append_ads(response, ads)
        content = result.body.decode()
        
        # Check that the original content is preserved
        assert "This is a test response." in content
        
        # Check that ads are appended
        assert "This is an ad." in content
        assert "This is another ad." in content
        
        # Check that ads come after the original content
        original_pos = content.find("This is a test response.")
        ad1_pos = content.find("This is an ad.")
        ad2_pos = content.find("This is another ad.")
        
        assert original_pos < ad1_pos
        assert original_pos < ad2_pos
    
    @pytest.mark.asyncio
    async def test_prepend_ads(self, middleware):
        """Test prepending ads to the response."""
        # Create a response
        response = Response(content="This is a test response.", media_type="text/plain")
        
        # Create sample ads
        ads = [
            {"id": "ad1", "text": "This is an ad."},
            {"id": "ad2", "text": "This is another ad."}
        ]
        
        # Apply the placement
        result = await middleware._prepend_ads(response, ads)
        content = result.body.decode()
        
        # Check that the original content is preserved
        assert "This is a test response." in content
        
        # Check that ads are prepended
        assert "This is an ad." in content
        assert "This is another ad." in content
        
        # Check that ads come before the original content
        original_pos = content.find("This is a test response.")
        ad1_pos = content.find("This is an ad.")
        ad2_pos = content.find("This is another ad.")
        
        assert ad1_pos < original_pos
        assert ad2_pos < original_pos
    
    @pytest.mark.asyncio
    async def test_insert_inline_ads(self, middleware):
        """Test inserting ads inline within the response."""
        # Create a response with multiple paragraphs
        response_text = """First paragraph.
        
        Second paragraph.
        
        Third paragraph.
        
        Fourth paragraph."""
        
        response = Response(content=response_text, media_type="text/plain")
        
        # Create sample ads
        ads = [
            {"id": "ad1", "text": "This is an ad."},
            {"id": "ad2", "text": "This is another ad."}
        ]
        
        # Override the detect_format_type to always return "plain"
        middleware.utils.detect_format_type = MagicMock(return_value="plain")
        
        # Apply the placement with the current config
        result = await middleware._insert_inline_ads(response, ads, "plain")
        content = result.body.decode()
        
        # Check that the original content is preserved (all paragraphs)
        assert "First paragraph." in content
        assert "Second paragraph." in content
        assert "Third paragraph." in content
        assert "Fourth paragraph." in content
        
        # Check that at least one ad is inserted
        assert "This is an ad." in content
    
    @pytest.mark.asyncio
    async def test_factual_response_skip(self, middleware):
        """Test that factual responses skip inline ads when configured."""
        # Create a factual response
        response_text = "The capital of France is Paris."
        response = Response(content=response_text, media_type="text/plain")
        
        # Create sample ads
        ads = [{"id": "ad1", "text": "This is an ad."}]
        
        # Override is_factual_response to return True
        middleware.utils.is_factual_response = MagicMock(return_value=True)
        
        # Set config to skip factual responses
        config = AdServingConfig(
            ad_placement_mode="inline",
            inline_config=InlineConfig(
                max_insertions=1,
                insertion_strategy="discourse",
                blend_style="soft",
                insert_after_paragraphs=1,
                tone_matching=True,
                skip_on_factual=True
            )
        )
        
        # Mock the _append_ads method to verify it's called
        middleware._append_ads = AsyncMock()
        
        # Apply the placement logic
        await middleware._place_ads_in_response(response, ads, config)
        
        # Check that _append_ads was called instead of _insert_inline_ads
        middleware._append_ads.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_json_format_handling(self, middleware):
        """Test handling of JSON format responses."""
        # Create a JSON response
        response_text = '{"result": "success", "data": {"value": 42}}'
        response = Response(content=response_text, media_type="application/json")
        
        # Create sample ads
        ads = [{"id": "ad1", "text": "This is an ad."}]
        
        # Mock the _handle_json_format method
        middleware._handle_json_format = AsyncMock()
        middleware.utils.detect_format_type = MagicMock(return_value="json")
        
        # Apply the placement logic
        config = AdServingConfig(ad_placement_mode="after")
        await middleware._place_ads_in_response(response, ads, config)
        
        # Check that _handle_json_format was called
        middleware._handle_json_format.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_code_format_handling(self, middleware):
        """Test handling of code format responses."""
        # Create a code response
        response_text = """
        def example():
            return 42
            
        # This is a comment
        x = example()
        print(x)
        """
        response = Response(content=response_text, media_type="text/plain")
        
        # Create sample ads
        ads = [{"id": "ad1", "text": "This is an ad."}]
        
        # Mock the _handle_code_format method
        middleware._handle_code_format = AsyncMock()
        middleware.utils.detect_format_type = MagicMock(return_value="code")
        
        # Apply the placement logic
        config = AdServingConfig(ad_placement_mode="after")
        await middleware._place_ads_in_response(response, ads, config)
        
        # Check that _handle_code_format was called
        middleware._handle_code_format.assert_called_once() 