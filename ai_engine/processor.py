import os
import json
import streamlit as st
from groq import Groq
from typing import Optional


class PolGuardProcessor:
    def __init__(self, blacklist_path="data/blacklist.csv"):
        # 1. API 키 로드 (코드에 직접 쓰지 않습니다)
        self.api_key = None

        # Streamlit Cloud 환경 (Secrets)
        if "GROQ_API_KEY" in st.secrets:
            self.api_key = st.secrets["GROQ_API_KEY"]

        # 로컬 환경 (환경변수 사용)
        if not self.api_key:
            self.api_key = os.environ.get("GROQ_API_KEY")

        # 2. 키가 없을 경우 안내 (에러 방지)
        if not self.api_key:
            st.error("🔑 Groq API Key가 설정되지 않았습니다. 관리자 설정을 확인하세요.")
            return

        # 3. Groq 클라이언트 생성
        try:
            self.client = Groq(api_key=self.api_key)
        except Exception as e:
            st.error(f"Groq 초기화 실패: {e}")

        self.blacklist_path = blacklist_path

    def analyze(self, text: str, url: Optional[str] = None) -> dict:
        if not hasattr(self, "client") or not self.client:
            return {
                "risk_score": 0,
                "verdict": "엔진 미가동",
                "factors": self._empty_factors(),
            }

        if not text:
            return {
                "risk_score": 0,
                "verdict": "데이터 없음",
                "factors": self._empty_factors(),
            }

        prompt = f"""
        당신은 대한민국 경찰청 사이버 수사대 소속 AI 수사관입니다.
        다음 메시지의 스캠/피싱 위험도를 분석하여 반드시 JSON 형식으로만 답변하세요.
        내용: "{text}"
        형식: {{"risk_score": 정수, "intent": "분류", "reason": "설명", "factors": {{"content_risk": 0~1, "context_risk": 0~1, "urgency_risk": 0~1, "pattern_match": 0~1, "blacklist_match": 0~1}}}}
        """

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                response_format={"type": "json_object"},
            )

            ai_res = json.loads(chat_completion.choices[0].message.content)
            score = ai_res.get("risk_score", 0)

            return {
                "risk_score": score,
                "verdict": "🚨 고위험 (피싱 의심)" if score >= 60 else "✅ 안전함",
                "ai_analysis": ai_res.get("reason", "분석 완료"),
                "intent": ai_res.get("intent", "일반"),
                "factors": ai_res.get("factors", self._empty_factors()),
            }
        except Exception as e:
            return {
                "risk_score": 0,
                "verdict": "분석 오류",
                "ai_analysis": f"AI 통신 에러: {str(e)}",
                "factors": self._empty_factors(),
            }

    def _empty_factors(self):
        return {
            "content_risk": 0.0,
            "context_risk": 0.0,
            "urgency_risk": 0.0,
            "pattern_match": 0.0,
            "blacklist_match": 0.0,
        }
