from pydantic import BaseModel, Field, root_validator
from typing import List, Optional, Literal

class InlineConfig(BaseModel):
    """Configuration options for inline ad placement."""
    max_insertions: int = Field(default=1, description="Maximum number of ads to insert inline")
    insertion_strategy: Literal["discourse", "sentence_boundary"] = Field(
        default="discourse", 
        description="Strategy for segmenting text for ad insertion"
    )
    blend_style: Literal["soft", "direct", "branded"] = Field(
        default="soft", 
        description="Style to use when blending ads into content"
    )
    insert_after_paragraphs: int = Field(
        default=1, 
        description="Number of paragraphs to show before inserting first ad"
    )
    custom_prefix: Optional[str] = Field(
        default=None, 
        description="Custom prefix text to use before ad"
    )
    custom_suffix: Optional[str] = Field(
        default=None, 
        description="Custom suffix text to use after ad"
    )
    tone_matching: bool = Field(
        default=True, 
        description="Whether to match tone with surrounding content"
    )
    skip_on_factual: bool = Field(
        default=False, 
        description="Skip inline ads for factual/Q&A responses"
    )

class AdServingConfig(BaseModel):
    ad_categories: Optional[List[str]] = Field(default=None, description="Preferred ad categories")
    exclude_types: Optional[List[str]] = Field(default=None, description="Ad types to exclude")
    max_ads: int = Field(default=2, description="Maximum number of ads to show")
    debug: bool = Field(default=False, description="Enable debug logging")
    target_paths: Optional[List[str]] = Field(default_factory=lambda: ["/chat/"])
    environment: str = Field(default="production", description="Environment: production or staging")
    api_base_url: Optional[str] = Field(default=None, description="API base URL")
    publisher_id: Optional[str] = Field(default=None, description="Publisher ID")
    
    # New placement fields for ad placement control
    ad_placement_mode: Literal["before", "after", "inline"] = Field(
        default="after", 
        description="Where to place ads relative to content"
    )
    inline_config: Optional[InlineConfig] = Field(
        default=None, 
        description="Configuration for inline ad placement"
    )
    response_format: Optional[Literal["plain", "markdown", "html", "json", "code"]] = Field(
        default=None,
        description="Format of the response content"
    )

    @root_validator(pre=True)
    def set_api_base_url(cls, values):
        env = values.get("environment", "production")
        if not values.get("api_base_url"):
            if env == "staging":
                values["api_base_url"] = "https://staging-api.yourplatform.com"
            else:
                values["api_base_url"] = "https://api.yourplatform.com"
        return values

    @root_validator
    def validate_inline_config(cls, values):
        """Ensure inline_config is present when mode is 'inline'"""
        if values.get("ad_placement_mode") == "inline" and not values.get("inline_config"):
            values["inline_config"] = InlineConfig()
        return values 