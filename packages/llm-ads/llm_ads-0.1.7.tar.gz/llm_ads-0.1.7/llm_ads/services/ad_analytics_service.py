import httpx
from .config import AdServingConfig
from loguru import logger

async def record_ad_impression(ad_id: int, prompt: str, config):
    logger.info(f"Recording ad impression for ad_id={ad_id}")
    payload = {
        "ad_id": ad_id,
        "prompt": prompt,
        "publisher_id": config.publisher_id
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{config.api_base_url}/analytics/impression", json=payload)
            response.raise_for_status()
            logger.info("Ad impression recorded via remote API")
        except httpx.HTTPStatusError as e:
            logger.error(f"Error recording impression: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error recording impression: {str(e)}")

async def record_ad_click(ad_id: int, prompt: str, config):
    logger.info(f"Recording ad click for ad_id={ad_id}")
    payload = {
        "ad_id": ad_id,
        "prompt": prompt,
        "publisher_id": config.publisher_id
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{config.api_base_url}/analytics/click", json=payload)
            response.raise_for_status()
            logger.info("Ad click recorded via remote API")
        except httpx.HTTPStatusError as e:
            logger.error(f"Error recording click: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error recording click: {str(e)}") 