from fastapi import FastAPI
from app.models.schemas import AnalysisRequest
from ai_engine.processor import PolGuardProcessor
from app.services.guardian_service import GuardianService

app = FastAPI(title="Pol-Guard Backend")
processor = PolGuardProcessor()
guardian = GuardianService()

@app.post("/analyze")
async def analyze_endpoint(data: AnalysisRequest):
    return processor.analyze(data.text, data.url)

@app.post("/report")
async def report_endpoint(data: AnalysisRequest):
    analysis = processor.analyze(data.text, data.url)
    return guardian.save_report(data.text, analysis)

@app.get("/academy/quiz")
async def get_quiz():
    return [{"q": "검찰은 카톡으로 영장을 보내지 않는다?", "a": "O"}]