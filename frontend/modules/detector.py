import streamlit as st
import plotly.graph_objects as go
import sys
import os

# 1. 경로 설정: 프로젝트 루트를 경로에 추가하여 ai_engine을 찾을 수 있게 함
# Streamlit Cloud 배포 환경에서도 경로를 찾을 수 있도록 설정합니다.
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.append(project_root)

# 2. 직접 AI 엔진 로직 임포트
try:
    from ai_engine.processor import PolGuardProcessor
except ImportError:
    st.error(
        "AI 엔진 모듈(ai_engine.processor)을 찾을 수 없습니다. 폴더 구조를 확인해주세요."
    )

# 3. 세션 상태에 엔진 초기화 (최초 1회만 실행)
if "engine" not in st.session_state:
    try:
        st.session_state.engine = PolGuardProcessor()
    except Exception as e:
        st.error(f"AI 엔진 초기화 실패: {e}")


def show_detector():
    st.info(
        "💡 **전문가 팁**: 발신번호가 '010'으로 시작하는 공공기관 문자는 99% 피싱입니다."
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 📥 정밀 분석 요청")
        user_input = st.text_area(
            "메시지 전문",
            placeholder="수신한 문자의 전체 내용을 복사해 붙여넣으세요...",
            height=200,
        )
        url_input = st.text_input(
            "🔗 포함된 URL", placeholder="http://으로 시작하는 링크 주소"
        )

        # 🚀 정밀 분석 시작 버튼
        if st.button("🚀 정밀 분석 시작"):
            if not user_input and not url_input:
                st.warning("내용을 입력해주세요.")
            else:
                with st.spinner("AI 가디언이 다차원 분석을 수행 중입니다..."):
                    try:
                        # ⚠️ 핵심: requests.post 대신 로컬 세션의 엔진을 직접 호출
                        # 이 방식은 백엔드 서버(Uvicorn) 없이도 동작합니다.
                        res = st.session_state.engine.analyze(user_input, url_input)
                        st.session_state["last_res"] = res
                        st.session_state["last_input"] = {
                            "text": user_input,
                            "url": url_input,
                        }
                    except Exception as e:
                        st.error(f"AI 분석 중 오류 발생: {e}")

    with col2:
        if "last_res" in st.session_state:
            res = st.session_state["last_res"]
            # ai_engine/processor.py에서 정의된 factors를 가져옵니다.
            f = res.get("factors", {})

            # 전문가용 레이더 차트 (5대 핵심 지표)
            # 리스크 점수가 0~1 사이의 값이라고 가정합니다.
            categories = [
                "금전유도",
                "기관사칭",
                "심리압박",
                "기술적패턴",
                "블랙리스트",
            ]

            # 엔진 응답 구조에 맞게 안전하게 값을 가져옵니다.
            values = [
                f.get("content_risk", 0),
                f.get("context_risk", 0),
                f.get("urgency_risk", 0),
                f.get("pattern_match", 0),
                f.get("blacklist_match", 0),
            ]

            fig = go.Figure()
            fig.add_trace(
                go.Scatterpolar(
                    r=values + [values[0]],
                    theta=categories + [categories[0]],
                    fill="toself",
                    line_color="#002244",
                    fillcolor="rgba(0, 34, 68, 0.3)",
                )
            )
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 1.2])),
                margin=dict(l=40, r=40, t=20, b=20),
            )
            st.plotly_chart(fig, use_container_width=True)

    # 하단 전문 판정 리포트
    if "last_res" in st.session_state:
        res = st.session_state["last_res"]
        f = res.get("factors", {})

        st.markdown("---")
        st.markdown(
            f"### 📑 AI 종합 판정 리포트: **{res.get('verdict', '판정 불가')}**"
        )

        c1, c2, c3 = st.columns(3)
        c1.metric("종합 위험도", f"{res.get('risk_score', 0)}%")

        # 사칭 가능성 로직
        context_risk = f.get("context_risk", 0)
        c2.metric("사칭 가능성", "매우 높음" if context_risk > 0.7 else "낮음")
        c3.metric("데이터 신뢰도", "Groq Llama-3 AI 분석")

        # 분석 사유 표시 (Groq AI가 제공하는 구체적인 이유)
        if "ai_analysis" in res:
            st.info(f"🔍 **AI 분석 근거**: {res['ai_analysis']}")

        # 전문가의 권고 사항
        with st.expander("📝 보안 전문가 권고 사항 확인"):
            risk_score = res.get("risk_score", 0)
            if risk_score > 60:
                st.error(
                    "1. 절대 링크를 누르지 말고 해당 번호를 차단하세요.\n"
                    "2. 이미 클릭했다면 비행기 모드를 켜고 악성 앱 검사를 수행하세요.\n"
                    "3. 지인 사칭의 경우 반드시 유선 전화로 본인 여부를 확인하세요."
                )
            else:
                st.success(
                    "알려진 위협은 없으나, 출처가 불분명한 링크는 항상 주의가 필요합니다."
                )
