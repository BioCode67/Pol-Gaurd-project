import os
import json
import streamlit as st
from groq import Groq
from typing import Optional

# .env 파일 로드 (로컬 테스트용)
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


class PolGuardProcessor:
    def __init__(self, blacklist_path="data/blacklist.csv"):
        """
        AI 엔진 초기화: API 키를 로드하고 Groq 클라이언트를 생성합니다.
        """
        self.api_key = self._load_api_key()
        self.blacklist_path = blacklist_path

        if not self.api_key:
            # 키가 없을 경우 에러 메시지를 띄우지만 앱이 죽지 않도록 설정
            self.client = None
            return

        try:
            # Groq 클라이언트 생성 (키워드 인자 사용)
            self.client = Groq(api_key=self.api_key)
        except Exception as e:
            self.client = None

    def _load_api_key(self):
        """보안 우선순위에 따라 API 키 로드"""
        # 1. Streamlit Secrets (배포 환경)
        try:
            if "GROQ_API_KEY" in st.secrets:
                return st.secrets["GROQ_API_KEY"]
        except:
            pass

        # 2. 환경 변수 (.env 파일)
        return os.getenv("GROQ_API_KEY")

    def analyze(self, text: str, url: Optional[str] = None) -> dict:
        """입력된 텍스트를 분석하여 결과를 반환합니다."""
        if not self.client:
            return {
                "risk_score": 0,
                "verdict": "엔진 미설정",
                "ai_analysis": "API 키가 설정되지 않았습니다. Secrets를 확인하세요.",
                "factors": self._empty_factors(),
            }

        if not text:
            return {
                "risk_score": 0,
                "verdict": "데이터 없음",
                "factors": self._empty_factors(),
            }

        # 시스템 프롬프트
        prompt = f"""
        당신은 대한민국 경찰청 사이버 수사대 소속 AI 수사관입니다.
        다음 메시지의 스캠/피싱 위험도를 분석하여 반드시 JSON 형식으로만 답변하세요.
        
        분석 대상: "{text}"
        
        반드시 포함해야 할 JSON 키:
        {{
            "risk_score": 0~100 사이의 정수,
            "intent": "지인사칭, 기관사칭, 대출사기, 광고 중 하나",
            "reason": "판단 근거 (한국어)",
            "factors": {{
                "content_risk": 0.0~1.0,
                "context_risk": 0.0~1.0,
                "urgency_risk": 0.0~1.0,
                "pattern_match": 0.0~1.0,
                "blacklist_match": 0.0~1.0
            }}
        }}
        """

        try:
            # 모델명을 llama3-8b-8192에서 llama-3.3-70b-versatile로 변경
            print("--- 현재 모델 호출 시도 중: llama-3.3-70b-versatile ---")  # 추가
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
