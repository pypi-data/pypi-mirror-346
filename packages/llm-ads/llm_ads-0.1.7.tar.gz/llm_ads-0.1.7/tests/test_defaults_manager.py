import pytest
from app.services.defaults_manager import DefaultsManager
from app.schemas.publisher_config import PublisherConfigBase

class TestDefaultsManager:
    """Tests for the DefaultsManager service."""
    
    def test_get_app_types(self):
        """Test that get_app_types returns a dictionary of app types."""
        app_types = DefaultsManager.get_app_types()
        
        assert isinstance(app_types, dict)
        assert len(app_types) > 0
        assert "chat" in app_types
        assert "documentation" in app_types
        
    def test_get_default_config(self):
        """Test that get_default_config returns the correct configuration."""
        chat_config = DefaultsManager.get_default_config("chat")
        documentation_config = DefaultsManager.get_default_config("documentation")
        
        # Check for expected config values
        assert chat_config["ad_placement_mode"] == "inline"
        assert chat_config["max_ads"] == 1
        assert chat_config["inline_config"]["max_insertions"] == 1
        
        assert documentation_config["ad_placement_mode"] == "before"
        assert documentation_config["max_ads"] == 1
        assert documentation_config["inline_config"] is None
        
        # Test non-existent app type
        non_existent = DefaultsManager.get_default_config("non_existent")
        assert non_existent is None
        
    def test_get_config_model(self):
        """Test that get_config_model returns a Pydantic model."""
        model = DefaultsManager.get_config_model("chat")
        
        assert isinstance(model, PublisherConfigBase)
        assert model.ad_placement_mode == "inline"
        assert model.max_ads == 1
        assert model.inline_config.max_insertions == 1
        
        # Test non-existent app type
        non_existent = DefaultsManager.get_config_model("non_existent")
        assert non_existent is None
        
    def test_override_config(self):
        """Test that override_config correctly merges configurations."""
        base_config = DefaultsManager.get_default_config("chat")
        
        # Simple override
        overrides = {"max_ads": 3, "debug_mode": True}
        result = DefaultsManager.override_config(base_config, overrides)
        
        assert result["max_ads"] == 3
        assert result["debug_mode"] is True
        assert result["ad_placement_mode"] == "inline"  # Unchanged
        
        # Override with nested fields
        overrides = {
            "ad_placement_mode": "before",
            "inline_config": {
                "max_insertions": 2,
                "tone_matching": False
            }
        }
        result = DefaultsManager.override_config(base_config, overrides)
        
        assert result["ad_placement_mode"] == "before"
        assert result["inline_config"]["max_insertions"] == 2
        assert result["inline_config"]["tone_matching"] is False
        assert result["inline_config"]["blend_style"] == "soft"  # Unchanged
        
    def test_get_optimal_config_for_context(self):
        """Test that get_optimal_config_for_context adjusts configuration based on context."""
        # Test with documentation context
        doc_context = {
            "is_documentation": True,
            "format": "markdown"
        }
        result = DefaultsManager.get_optimal_config_for_context(doc_context)
        
        assert result["ad_placement_mode"] == "before"
        assert result["response_format_preference"] == "markdown"
        
        # Test with factual Q&A context
        qa_context = {
            "is_qa": True,
            "is_factual": True,
            "format": "plain"
        }
        result = DefaultsManager.get_optimal_config_for_context(qa_context)
        
        assert result["inline_config"]["skip_on_factual"] is True
        assert result["response_format_preference"] == "plain" 