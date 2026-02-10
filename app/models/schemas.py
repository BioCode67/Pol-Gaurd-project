from pydantic import BaseModel
from typing import Optional, Dict

class AnalysisRequest(BaseModel):
    text: str
    url: Optional[str] = None

class AnalysisResponse(BaseModel):
    risk_score: float
    verdict: str
    factors: Dict[str, float]