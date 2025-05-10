from fastapi import Response
from typing import List, Dict, Any, Union
from .config import AdServingConfig, InlineConfig
import json
import re
from loguru import logger

def segment_response(response_text: str, strategy: str = "discourse", format_type: str = "plain") -> List[str]:
    """
    Segment the response text into units based on the chosen strategy and format type.
    
    Args:
        response_text: The LLM-generated text
        strategy: The segmentation strategy ("discourse" or "sentence_boundary")
        format_type: The format of the response ("plain", "markdown", "html", "json", "code")
        
    Returns:
        List of text segments
    """
    # Handle different formats appropriately
    if format_type in ["markdown", "html"]:
        return segment_markup(response_text, format_type)
    elif format_type in ["json", "code"]:
        # For structured content, just return the whole text as one segment
        # The placement engine will handle these specially
        return [response_text]
    
    # Plain text segmentation based on strategy
    if strategy == "discourse":
        # Split by paragraph or discourse unit
        return [p for p in response_text.split("\n\n") if p.strip()]
    elif strategy == "sentence_boundary":
        # Simple sentence splitting - in production, you'd use a more robust approach like NLTK
        sentences = []
        for paragraph in response_text.split("\n\n"):
            # Simple regex to split on sentence boundaries
            for sentence in re.split(r'(?<=[.!?])\s+', paragraph):
                if sentence.strip():
                    sentences.append(sentence.strip())
        return sentences
    else:
        # Default fallback - just return the whole text as one segment
        return [response_text]

def segment_markup(response_text: str, format_type: str) -> List[str]:
    """
    Segment markup content (HTML or Markdown) safely.
    
    Args:
        response_text: The markup text
        format_type: "markdown" or "html"
        
    Returns:
        List of segments at safe insertion points
    """
    if format_type == "markdown":
        # Avoid breaking code blocks, headers, etc.
        segments = []
        current_segment = ""
        in_code_block = False
        
        for line in response_text.split("\n"):
            # Check for code block delimiters
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                
            current_segment += line + "\n"
            
            # Only break segments at paragraph boundaries when not in a code block
            if line.strip() == "" and not in_code_block and current_segment:
                segments.append(current_segment)
                current_segment = ""
                
        if current_segment:
            segments.append(current_segment)
            
        return segments
    
    elif format_type == "html":
        # Basic HTML segmentation - in production, use a proper HTML parser
        # This simple version just splits at closing paragraph tags
        segments = []
        current = ""
        for part in re.split(r'(</p>|</div>|</section>)', response_text):
            current += part
            if part in ["</p>", "</div>", "</section>"]:
                segments.append(current)
                current = ""
        
        if current:
            segments.append(current)
            
        return segments
    
    # Fallback
    return [response_text]

def detect_format_type(text: str) -> str:
    """
    Detect the format type of the response text.
    
    Args:
        text: The text to analyze
        
    Returns:
        Format type: "plain", "markdown", "html", "json", or "code"
    """
    # Check for JSON
    if text.strip().startswith(("{", "[")):
        try:
            json.loads(text)
            return "json"
        except:
            pass
    
    # Check for code
    if "```" in text or text.count("\n") > 5 and any(
        line.strip().startswith(("def ", "class ", "import ", "from ")) for line in text.split("\n")
    ):
        return "code"
    
    # Check for HTML
    if "<html" in text.lower() or "<body" in text.lower() or text.count("<") > 5:
        return "html"
        
    # Check for Markdown
    if text.count("#") > 3 or "**" in text or "__" in text:
        return "markdown"
        
    # Default to plain text
    return "plain"

def is_factual_response(text: str) -> bool:
    """
    Determine if a response is primarily factual/Q&A style.
    
    Args:
        text: The text to analyze
        
    Returns:
        True if the text appears to be a factual response
    """
    # Simple heuristic based on length and structure
    if len(text) < 200:  # Short responses tend to be factual
        return True
        
    # Check for question-answer patterns
    if text.count("?") > 0 and text.count("\n\n") < 3:
        return True
        
    return False

async def insert_ads_into_response(response: Response, ads: List[Dict[str, Any]], config: AdServingConfig) -> Response:
    """
    Insert ads into the response body.
    This is a placeholder implementation - you can enhance it based on your needs.
    """
    try:
        # Get the response body
        body = await response.body()
        
        # Parse the response body
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            # If the response is not JSON, return as is
            return response
            
        # Add ads to the response
        if isinstance(data, dict):
            data['ads'] = ads
        elif isinstance(data, list):
            data.append({'ads': ads})
            
        # Update the response body
        response.body = json.dumps(data).encode()
        response.headers['content-length'] = str(len(response.body))
        
        return response
    except Exception as e:
        # If anything goes wrong, return the original response
        return response

async def insert_ads_into_response_old(response: Response, ads: List[dict], config: AdServingConfig) -> Response:
    """Insert ads into the response."""
    try:
        if response.media_type == "application/json":
            data = json.loads(response.body.decode()) if hasattr(response, 'body') else {}
            
            # Add ads to the response
            data["ads"] = [{
                "id": ad["id"],
                "title": ad["title"],
                "description": ad["description"],
                "category": ad["category"],
                "score": ad["score"],
                "ctr": ad["ctr"]
            } for ad in ads]
            
            # Add targeting info if in debug mode
            if config.debug:
                data["targeting_info"] = {
                    "total_ads_found": len(ads),
                    "categories": config.ad_categories,
                    "scores": {ad["title"]: ad["score"] for ad in ads}
                }
            
            response.body = json.dumps(data).encode()
            
        elif response.media_type == "text/plain":
            text = response.body.decode() if hasattr(response, 'body') else ""
            
            # Format ads as text
            ad_text = "\n\n---\nRelevant Ads:\n"
            for ad in ads:
                ad_text += f"\n• {ad['title']}: {ad['description']}"
                if config.debug:
                    ad_text += f" (Score: {ad['score']:.2f}, CTR: {ad['ctr']:.2%})"
            
            response.body = (text + ad_text).encode()
            
    except Exception as e:
        # Log error but don't break the response
        print(f"Error inserting ads into response: {e}")
        
    return response 