import os
import json
import streamlit as st
from groq import Groq
from typing import Optional


class PolGuardProcessor:
    def __init__(self, blacklist_path="data/blacklist.csv"):
        # 1. API 키 로드 로직
        self.api_key = None

        # Streamlit Cloud 환경 (Secrets)
        if "GROQ_API_KEY" in st.secrets:
            self.api_key = st.secrets["GROQ_API_KEY"]

        # 로컬 환경 (환경변수 혹은 직접 입력)
        if not self.api_key:
            # 주형 님이 주신 키를 로컬 테스트용으로 사용
            self.api_key = os.environ.get("GROQ_API_KEY")

        # 2. Groq 클라이언트 생성
        try:
            self.client = Groq(api_key=self.api_key)
        except Exception as e:
            st.error(f"Groq 초기화 실패: {e}")
            raise

        self.blacklist_path = blacklist_path

    def analyze(self, text: str, url: Optional[str] = None) -> dict:
        if not text:
            return {
                "risk_score": 0,
                "verdict": "데이터 없음",
                "factors": self._empty_factors(),
            }

        # 시스템 프롬프트: AI 수사관 페르소나 부여
        prompt = f"""
        당신은 대한민국 경찰청 사이버 수사대 소속 AI 수사관입니다.
        다음 메시지의 스캠/피싱 위험도를 분석하여 반드시 JSON 형식으로만 답변하세요.
        
        분석 대상 문장: "{text}"
        
        반드시 아래의 JSON 키를 포함해야 합니다:
        {{
            "risk_score": 0에서 100 사이의 정수,
            "intent": "지인사칭, 기관사칭, 대출사기, 광고 중 하나",
            "reason": "판단 근거 (한국어로 친절하게 설명)",
            "factors": {{
                "content_risk": 0.0~1.0 사이 실수,
                "context_risk": 0.0~1.0 사이 실수,
                "urgency_risk": 0.0~1.0 사이 실수,
                "pattern_match": 0.0~1.0 사이 실수,
                "blacklist_match": 0.0~1.0 사이 실수
            }}
        }}
        """

        try:
            # 💡 모델명을 최신 지원 모델인 llama-3.3-70b-versatile로 변경했습니다.
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
            # 에러 발생 시 사용자에게 친절한 피드백 제공
            return {
                "risk_score": 0,
                "verdict": "분석 일시 중단",
                "ai_analysis": f"AI 분석 엔진 통신 오류: {str(e)}",
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
