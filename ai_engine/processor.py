import pandas as pd
import os
from typing import Optional


# 백엔드 서버 실행 uvicorn app.main:app --reload --port 8000
class PolGuardProcessor:
    def __init__(self, blacklist_path="data/blacklist.csv"):
        # 가중치 상향 조정
        self.weights = {"content": 0.5, "context": 0.4, "urgency": 0.3}
        self.alpha = 2.0  # 패턴 가중치 강화
        self.beta = 5.0  # 블랙리스트 가중치 대폭 강화 (걸리면 바로 고위험)
        self.blacklist_path = blacklist_path
        self.blacklist = []
        self._load_blacklist()

    def _load_blacklist(self):
        if os.path.exists(self.blacklist_path):
            try:
                # 인코딩 문제 방지
                df = pd.read_csv(self.blacklist_path)
                if "url" in df.columns:
                    self.blacklist = df["url"].astype(str).tolist()
            except Exception as e:
                print(f"블랙리스트 로드 실패: {e}")
                self.blacklist = []

    def analyze(self, text: str, url: Optional[str] = None) -> dict:
        # 텍스트가 None일 경우 빈 문자열로 처리 (에러 방지)
        if text is None:
            text = ""

        # 1. Ci 계산
        context_val = (
            1.0
            if any(w in text for w in ["검찰", "경찰", "지방지검", "국세청", "법원"])
            else 0.1
        )
        content_val = (
            1.0
            if any(w in text for w in ["입금", "송금", "계좌", "카드결제", "대출상담"])
            else 0.1
        )
        urgency_val = (
            1.0
            if any(w in text for w in ["즉시", "금일 마감", "구속", "정지 예정"])
            else 0.2
        )

        c_scores = {
            "content": content_val,
            "context": context_val,
            "urgency": urgency_val,
        }
        sum_ci = sum(self.weights[k] * c_scores[k] for k in self.weights)

        # 2. P (패턴) & B (블랙리스트)
        is_suspicious_pattern = "http" in text and any(
            x in text for x in ["bit.ly", "t.ly", "nuly.do", "c11.kr"]
        )
        p_factor = 1.5 if is_suspicious_pattern else 0.2

        # 블랙리스트 대조 강화
        b_factor = 1.0 if url and any(url in b for b in self.blacklist) else 0.0

        # 3. 공식 적용 (상수 조정으로 점수 민감도 향상)
        # 블랙리스트에 있으면 무조건 높은 점수가 나오도록 설계
        r_score = sum_ci + (self.alpha * p_factor) + (self.beta * b_factor)

        # 정규화 로직 변경: 기준치를 50점으로 하향하거나 승수를 조정
        normalized = min(round(r_score * 15, 2), 100.0)

        # 블랙리스트 직행 티켓 (강력 추천)
        if b_factor > 0:
            normalized = 100.0

        return {
            "risk_score": normalized,
            "verdict": "🚨 고위험 (피싱 의심)" if normalized >= 50 else "✅ 안전함",
            "factors": {
                "content_risk": round(content_val, 2),
                "context_risk": round(context_val, 2),
                "urgency_risk": round(urgency_val, 2),
                "pattern_match": p_factor,
                "blacklist_match": b_factor,
            },
        }
