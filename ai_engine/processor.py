import os
import streamlit as st
from groq import Groq
import json
from typing import Optional


class PolGuardProcessor:
    def __init__(self, blacklist_path="data/blacklist.csv"):
        # API Key는 Streamlit Cloud 설정에서 관리하는 것이 보안상 좋습니다.
        # 로컬 테스트용으로 여기에 직접 넣거나 환경변수를 쓰세요.
        api_key = st.secrets["GROQ_API_KEY"]
        self.client = Groq(api_key)
        self.blacklist_path = blacklist_path

    def analyze(self, text: str, url: Optional[str] = None) -> dict:
        if not text:
            return {"risk_score": 0, "verdict": "데이터 없음"}

        # AI에게 부여하는 '전문가 페르소나'와 '분석 지침'
        prompt = f"""
        당신은 대한민국 경찰청 산하 사이버 수사대의 AI 수사관입니다.
        다음 메시지를 분석하여 스캠(사기) 또는 피싱 여부를 판별하세요.
        특히 '아빠, 나 급해' 같은 사회공학적 기법(Social Engineering)을 중점적으로 보십시오.

        메시지 내용: "{text}"

        결과는 반드시 다음 JSON 형식으로만 출력하세요:
        {{
            "risk_score": 0~100 사이 정수,
            "intent": "의도 분류(예: 지인사칭, 기관사칭, 일반 등)",
            "reason": "왜 그렇게 판단했는지 한국어로 짧게 설명"
        }}
        """

        try:
            # Groq Llama 3를 이용한 초고속 추론
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192",  # 혹은 llama3-70b-8192
                response_format={"type": "json_object"},  # JSON 응답 강제
            )

            ai_res = json.loads(chat_completion.choices[0].message.content)
            score = ai_res["risk_score"]

            return {
                "risk_score": score,
                "verdict": "🚨 고위험 (피싱 의심)" if score >= 60 else "✅ 안전함",
                "ai_analysis": ai_res["reason"],
                "intent": ai_res["intent"],
                "factors": {
                    "content_risk": score / 100,
                    "context_risk": 0.8 if ai_res["intent"] != "일반" else 0.1,
                    "urgency_risk": 0.9 if "급해" in text else 0.2,
                    "pattern_match": 1.0 if url else 0.2,
                    "blacklist_match": 0.0,  # 필요시 기존 블랙리스트 로직 추가 가능
                },
            }
        except Exception as e:
            return {"risk_score": 50, "verdict": "AI 분석 오류", "ai_analysis": str(e)}
