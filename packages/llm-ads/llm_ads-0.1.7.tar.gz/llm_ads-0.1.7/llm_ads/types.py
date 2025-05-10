from typing import TypedDict, List, Optional
from datetime import datetime

class Ad(TypedDict):
    id: int
    title: str
    description: str
    category: str
    target_keywords: List[str]
    ctr: float
    score: float

class TargetingContext(TypedDict, total=False):
    prompt: str
    user_id: Optional[int]
    categories: Optional[List[str]]
    keywords: Optional[List[str]] 