from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response
from .config import AdServingConfig, InlineConfig
from .targeting import select_ads
from .utils import insert_ads_into_response, detect_format_type, segment_response, is_factual_response
from loguru import logger
from .services.ad_analytics_service import record_ad_impression
import json
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

class AdServingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, config: AdServingConfig = None):
        super().__init__(app)
        self.config = config or AdServingConfig()
        logger.info(f"AdServingMiddleware initialized with config: {self.config}")

    async def dispatch(self, request: Request, call_next):
        # Only process LLM prompt endpoints
        if request.url.path not in self.config.target_paths:
            logger.info(f"Skipping middleware for path: {request.url.path}")
            return await call_next(request)
            
        logger.info(f"Processing request for path: {request.url.path}")
        
        # Get the request body
        body = await request.body()
        logger.info(f"Request body: {body.decode() if isinstance(body, bytes) else body}")
        
        # We need to set the body back since we've consumed it
        request._body = body
        
        try:
            # Try to get publisher-specific configuration
            publisher_config = await self._get_publisher_config(request)
            
            # Merge publisher config with default config if available
            if publisher_config:
                logger.info(f"Using publisher-specific configuration: {publisher_config}")
                config = self._merge_configs(publisher_config)
            else:
                config = self.config
            
            # Select ads from remote API
            ads = await select_ads(body, config)
            logger.info(f"Selected ads in middleware: {json.dumps(ads, indent=2)}")
            
            # Store ads in request state
            request.state.selected_ads = ads
            
            # Store placement configuration in request state for access in endpoints
            request.state.ad_placement_config = {
                "mode": config.ad_placement_mode,
                "inline_config": config.inline_config.dict() if config.inline_config else None,
                "response_format": config.response_format
            }
            
            # Continue with the request
            response = await call_next(request)
            
            # Process response with ad placement
            if ads and hasattr(response, 'body'):
                try:
                    response = await self._place_ads_in_response(response, ads, config)
                except Exception as e:
                    logger.error(f"Error placing ads in response: {str(e)}")
            
            # Try to record impressions after the response has been generated
            try:
                for ad in ads:
                    await record_ad_impression(
                        ad_id=ad["id"],
                        prompt=body.decode() if isinstance(body, bytes) else str(body),
                        config=config
                    )
            except Exception as e:
                # Log the error but don't fail the request
                logger.error(f"Error recording ad impressions: {str(e)}")
            
            return response
            
        except Exception as e:
            logger.error(f"Error in ad serving middleware: {e}")
            # Ensure we don't abort the request even if ad serving fails
            return await call_next(request)
    
    async def _get_publisher_config(self, request: Request) -> dict:
        """
        Get publisher-specific configuration from the database.
        """
        try:
            # Try to get publisher_id from request or session
            publisher_id = None
            
            # Check if user is authenticated and has publisher_id
            if hasattr(request.state, "user") and hasattr(request.state.user, "publisher_id"):
                publisher_id = request.state.user.publisher_id
            
            # Also check request headers for publisher_id
            if not publisher_id and "x-publisher-id" in request.headers:
                publisher_id = request.headers.get("x-publisher-id")
            
            # If no publisher_id, return None
            if not publisher_id:
                return None
            
            # Get async session from app state
            if not hasattr(request.app.state, "db_session"):
                logger.warning("No database session found in app state")
                return None
            
            async with request.app.state.db_session() as session:
                # Import here to avoid circular imports
                from app.models.publisher_config import PublisherConfig
                
                # Get publisher config from database
                result = await session.execute(
                    select(PublisherConfig)
                    .where(PublisherConfig.publisher_id == publisher_id)
                    .where(PublisherConfig.is_active == True)
                )
                config = result.scalar_one_or_none()
                
                if not config:
                    return None
                
                # Convert to dict
                return config.to_dict()
                
        except Exception as e:
            logger.error(f"Error getting publisher configuration: {e}")
            return None
    
    def _merge_configs(self, publisher_config: dict) -> AdServingConfig:
        """
        Merge publisher-specific configuration with default configuration.
        """
        # Create a copy of the default config
        merged_config = AdServingConfig(
            publisher_id=self.config.publisher_id,
            api_base_url=self.config.api_base_url,
            target_paths=self.config.target_paths,
            environment=self.config.environment
        )
        
        # Update with publisher-specific values
        if "ad_placement_mode" in publisher_config:
            merged_config.ad_placement_mode = publisher_config["ad_placement_mode"]
            
        if "inline_config" in publisher_config and publisher_config["inline_config"]:
            merged_config.inline_config = InlineConfig(**publisher_config["inline_config"])
            
        if "response_format_preference" in publisher_config:
            merged_config.response_format = publisher_config["response_format_preference"]
            
        if "ad_categories" in publisher_config:
            merged_config.ad_categories = publisher_config["ad_categories"]
            
        if "exclude_types" in publisher_config:
            merged_config.exclude_types = publisher_config["exclude_types"]
            
        if "max_ads" in publisher_config:
            merged_config.max_ads = publisher_config["max_ads"]
            
        if "debug_mode" in publisher_config:
            merged_config.debug = publisher_config["debug_mode"]
            
        return merged_config
    
    async def _place_ads_in_response(self, response: Response, ads: list, config: AdServingConfig) -> Response:
        """
        Place ads in the response according to the configured placement mode.
        """
        try:
            # Get the response body
            body = response.body.decode()
            
            # Determine the response format
            format_type = config.response_format or detect_format_type(body)
            logger.info(f"Detected response format: {format_type}")
            
            # Store placement information in request state for metrics recording
            placement_info = {
                "placement_type": config.ad_placement_mode,
                "response_format": format_type,
                "response_length": len(body),
                "placement_config": config.inline_config.dict() if config.ad_placement_mode == "inline" and config.inline_config else None
            }
            
            # Handle different formats
            if format_type == "json":
                response = await self._handle_json_format(response, ads)
                
            elif format_type == "code":
                response = await self._handle_code_format(response, ads)
            
            # For text-based formats, use the placement mode
            elif config.ad_placement_mode == "before":
                response = await self._prepend_ads(response, ads)
                
            elif config.ad_placement_mode == "after":
                response = await self._append_ads(response, ads)
                
            elif config.ad_placement_mode == "inline":
                # Special case: check if we should skip inline for factual responses
                is_factual = is_factual_response(body)
                placement_info["is_factual_response"] = is_factual
                
                if config.inline_config and config.inline_config.skip_on_factual and is_factual:
                    logger.info("Skipping inline ads for factual response, using 'after' placement instead")
                    placement_info["placement_type"] = "after"  # Update the placement type
                    response = await self._append_ads(response, ads)
                else:
                    response = await self._insert_inline_ads(response, ads, format_type, config)
            
            else:
                # Default to append
                placement_info["placement_type"] = "after"
                response = await self._append_ads(response, ads)
            
            # Store placement info in response headers for tracking
            response.headers["X-Ad-Placement-Type"] = placement_info["placement_type"]
            response.headers["X-Ad-Response-Format"] = format_type
            
            # Try to record metrics for each ad
            try:
                from app.services.performance_tracker import AdPerformanceTracker
                
                # Only record if we have access to the database
                if hasattr(response, "_request") and hasattr(response._request.app.state, "db_session"):
                    session = response._request.app.state.db_session()
                    publisher_id = config.publisher_id
                    
                    for ad in ads:
                        segment_position = None
                        if placement_info["placement_type"] == "inline" and "segment_position" in ad:
                            segment_position = ad["segment_position"]
                            
                        await AdPerformanceTracker.record_impression(
                            session=session,
                            publisher_id=publisher_id,
                            ad_id=ad["id"],
                            placement_type=placement_info["placement_type"],
                            placement_config=placement_info.get("placement_config"),
                            response_format=format_type,
                            response_length=placement_info["response_length"],
                            segment_position=segment_position
                        )
            except Exception as e:
                logger.error(f"Error recording placement metrics: {str(e)}")
                # Don't let metrics recording failure affect the response
                pass
                
            return response
                
        except Exception as e:
            logger.error(f"Error in _place_ads_in_response: {str(e)}")
            return response
    
    async def _handle_json_format(self, response: Response, ads: list) -> Response:
        """Handle JSON format responses by adding ads as a field."""
        try:
            data = json.loads(response.body)
            if isinstance(data, dict):
                data["ads"] = ads
            elif isinstance(data, list):
                # For list responses, append an ads object at the end
                data.append({"ads": ads})
                
            response.body = json.dumps(data).encode()
            response.headers["content-length"] = str(len(response.body))
        except:
            logger.error("Failed to handle JSON format")
            
        return response
        
    async def _handle_code_format(self, response: Response, ads: list) -> Response:
        """Handle code format by appending ads as comments after the code."""
        try:
            code = response.body.decode()
            
            # Format ads as comments
            ad_text = "\n\n# SPONSORED CONTENT\n"
            for ad in ads:
                ad_text += f"# {ad['title']}: {ad['description']}\n"
                
            response.body = (code + ad_text).encode()
            response.headers["content-length"] = str(len(response.body))
        except:
            logger.error("Failed to handle code format")
            
        return response
        
    async def _prepend_ads(self, response: Response, ads: list) -> Response:
        """Prepend ads to the response."""
        try:
            content = response.body.decode()
            
            # Format ads section
            ad_text = "SPONSORED CONTENT\n"
            for ad in ads:
                ad_text += f"- {ad['title']}: {ad['description']}\n"
            
            ad_text += "\n---\n\n"
            
            # Combine and update
            response.body = (ad_text + content).encode()
            response.headers["content-length"] = str(len(response.body))
        except:
            logger.error("Failed to prepend ads")
            
        return response
        
    async def _append_ads(self, response: Response, ads: list) -> Response:
        """Append ads to the response."""
        try:
            content = response.body.decode()
            
            # Format ads section
            ad_text = "\n\n---\n\nSPONSORED CONTENT\n"
            for ad in ads:
                ad_text += f"- {ad['title']}: {ad['description']}\n"
            
            # Combine and update
            response.body = (content + ad_text).encode()
            response.headers["content-length"] = str(len(response.body))
        except:
            logger.error("Failed to append ads")
            
        return response
        
    async def _insert_inline_ads(self, response: Response, ads: list, format_type: str, config: AdServingConfig = None) -> Response:
        """Insert ads inline within the response content."""
        try:
            content = response.body.decode()
            inline_config = config.inline_config if config else self.config.inline_config
            
            if not inline_config:
                # Fallback to after if no inline config
                return await self._append_ads(response, ads)
            
            # Segment the content based on format and strategy
            segments = segment_response(
                content, 
                strategy=inline_config.insertion_strategy,
                format_type=format_type
            )
            
            # If we couldn't segment, fall back to after placement
            if not segments or len(segments) <= 1:
                logger.info("Content too short for inline ads, using 'after' placement")
                return await self._append_ads(response, ads)
            
            # Determine where to insert ads
            result = []
            ad_index = 0
            insertions = 0
            
            # Insert first ad after specified number of paragraphs
            first_ad_position = min(inline_config.insert_after_paragraphs, len(segments) - 1)
            
            for i, segment in enumerate(segments):
                result.append(segment)
                
                # Insert ad after the specified position, and then periodically
                if (i == first_ad_position or 
                    (i > first_ad_position and 
                     (i - first_ad_position) % 3 == 0) and  # Every 3 segments after first ad
                    ad_index < len(ads) and 
                    insertions < inline_config.max_insertions):
                    
                    # Format ad with appropriate style
                    ad = ads[ad_index]
                    
                    if inline_config.blend_style == "direct":
                        ad_text = f"\n[Advertisement] {ad['title']}: {ad['description']}\n"
                    elif inline_config.blend_style == "branded":
                        ad_text = f"\nSponsored: {ad['title']} - {ad['description']}\n"
                    else:  # soft
                        # Choose a natural transition
                        transitions = [
                            "You might be interested in",
                            "By the way,",
                            "Related to this,",
                            "You may find this helpful:",
                            "Worth mentioning:"
                        ]
                        import random
                        prefix = inline_config.custom_prefix or random.choice(transitions)
                        ad_text = f"\n{prefix} {ad['description']}\n"
                    
                    result.append(ad_text)
                    ad_index += 1
                    insertions += 1
            
            # Combine and update
            response.body = "".join(result).encode()
            response.headers["content-length"] = str(len(response.body))
            
        except Exception as e:
            logger.error(f"Failed to insert inline ads: {str(e)}")
            # Fallback to after placement
            return await self._append_ads(response, ads)
            
        return response 