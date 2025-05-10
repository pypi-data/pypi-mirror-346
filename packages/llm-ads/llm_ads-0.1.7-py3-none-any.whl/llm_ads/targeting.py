from typing import List, Any, Optional
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from .config import AdServingConfig
import json
from loguru import logger
from .models.ad import Ad
import httpx

def mock_ads_db():
    return [
        {
            "id": 1,
            "title": "Tech Gadget",
            "category": "tech",
            "type": "banner",
            "target_keywords": ["tech", "gadget", "trends", "ai"]
        },
        {
            "id": 2,
            "title": "Finance App",
            "category": "finance",
            "type": "banner",
            "target_keywords": ["finance", "money", "invest", "app"]
        },
        {
            "id": 3,
            "title": "Travel Deal",
            "category": "travel",
            "type": "video",
            "target_keywords": ["travel", "deal", "vacation"]
        },
    ]

def get_prompt_text(prompt):
    logger.info(f"Processing prompt input: {prompt}")
    if isinstance(prompt, str):
        return prompt
    if isinstance(prompt, bytes):
        try:
            data = json.loads(prompt.decode())
            logger.info(f"Decoded bytes to JSON: {data}")
            return data.get("prompt", "")
        except Exception as e:
            logger.error(f"Failed to decode bytes: {e}")
            # Try to return the raw bytes as a string
            try:
                return prompt.decode()
            except:
                return ""
    if hasattr(prompt, "prompt"):
        return prompt.prompt
    if isinstance(prompt, dict) and "prompt" in prompt:
        return prompt["prompt"]
    logger.warning(f"Could not extract prompt from input: {prompt}")
    return ""

async def select_ads(prompt: Any, config: AdServingConfig) -> list[dict]:
    logger.info("Selecting ads from remote API")
    prompt_text = get_prompt_text(prompt)
    
    # If no prompt text could be extracted, return empty list
    if not prompt_text:
        logger.warning("No prompt text extracted, returning empty ad list")
        return []
    
    payload = {
        "prompt": prompt_text,
        "categories": config.ad_categories,
        "publisher_id": config.publisher_id,
        "max_ads": config.max_ads
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{config.api_base_url}/ads/select", 
                json=payload,
                timeout=5.0  # Add timeout to prevent hanging
            )
            response.raise_for_status()
            ads = response.json()
            logger.info(f"Selected {len(ads)} ads from remote API")
            return ads
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error during ad selection: {e}")
        return []
    except httpx.RequestError as e:
        logger.error(f"Request error during ad selection: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error during ad selection: {e}")
        return []

# Fallback function that uses local mock data in case the API is unavailable
def select_ads_local(prompt: Any, config: AdServingConfig) -> List[dict]:
    logger.info("Selecting ads from local mock database")
    ads = mock_ads_db()
    
    # Filter by category
    if config.ad_categories:
        ads = [ad for ad in ads if ad["category"] in config.ad_categories]
    
    # Exclude types
    if config.exclude_types:
        ads = [ad for ad in ads if ad["type"] not in config.exclude_types]
    
    # Limit number
    return ads[:config.max_ads]