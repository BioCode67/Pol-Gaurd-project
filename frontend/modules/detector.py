import streamlit as st
import plotly.graph_objects as go
import sys
import os

# 1. 경로 설정 (ai_engine 폴더를 인식하게 함)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.append(project_root)

# 2. 직접 AI 엔진 로직 임포트
try:
    from ai_engine.processor import PolGuardProcessor
except ImportError:
    st.error("❌ 시스템 경로 설정 오류: ai_engine 폴더를 찾을 수 없습니다.")


# 3. 분석 화면 구성 함수
def show_detector():
    # [중요] 세션 상태에 엔진이 없으면 즉시 초기화
    if "engine" not in st.session_state:
        try:
            st.session_state.engine = PolGuardProcessor()
        except Exception as e:
            st.error(f"❌ 엔진 초기화 실패: {e}")
            return

    st.title("🔍 실시간 스미싱 탐지 가디언")
    st.info(
        "💡 **전문가 팁**: 정부기관이나 은행은 절대로 010 번호로 링크를 보내지 않습니다."
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 📥 정밀 분석 요청")
        user_input = st.text_area(
            "메시지 전문",
            placeholder="수신한 문자의 전체 내용을 복사해 붙여넣으세요...",
            height=200,
            key="input_text",
        )
        url_input = st.text_input("🔗 포함된 URL (선택사항)", placeholder="http://...")

        if st.button("🚀 정밀 분석 시작", use_container_width=True):
            if not user_input.strip():
                st.warning("분석할 텍스트를 입력해주세요.")
            else:
                with st.spinner("Llama-3.3 엔진이 다차원 분석을 수행 중입니다..."):
                    try:
                        # st.session_state에 저장된 엔진을 사용하여 직접 분석
                        res = st.session_state.engine.analyze(user_input, url_input)
                        st.session_state["last_res"] = res
                    except Exception as e:
                        st.error(f"⚠️ 분석 엔진 오류: {e}")

    with col2:
        if "last_res" in st.session_state:
            res = st.session_state["last_res"]
            f = res.get("factors", {})

            # 전문가용 레이더 차트 구성
            categories = [
                "금전유도",
                "기관사칭",
                "심리압박",
                "기술적패턴",
                "블랙리스트",
            ]
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
                    line_color="#FF4B4B",
                    fillcolor="rgba(255, 75, 75, 0.3)",
                )
            )
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                margin=dict(l=40, r=40, t=20, b=20),
            )
            st.plotly_chart(fig, use_container_width=True)

    # 하단 판정 결과 리포트
    if "last_res" in st.session_state:
        res = st.session_state["last_res"]
        st.markdown("---")

        # 위험도에 따른 색상 결정
        risk = res.get("risk_score", 0)
        color = "red" if risk >= 60 else "orange" if risk >= 30 else "green"

        st.markdown(
            f"### 📑 AI 종합 판정 리포트: :{color}[{res.get('verdict', '분석 중')}]"
        )

        c1, c2, c3 = st.columns(3)
        c1.metric("종합 위험도", f"{risk}%")
        c2.metric("위험 유형", res.get("intent", "기타"))
        c3.metric("데이터 엔진", "Llama-3.3 70B")

        if "ai_analysis" in res:
            st.warning(f"**🕵️ 분석 근거:** {res['ai_analysis']}")

        with st.expander("📝 대응 가이드라인 (보안 전문가 제언)"):
            if risk >= 60:
                st.error(
                    "🚨 **즉시 대응 필요**\n- 해당 번호를 스팸으로 신고 및 차단하십시오.\n- 링크를 클릭했다면 스마트폰 백신을 돌리고 '시티즌코난' 앱을 실행하세요."
                )
            else:
                st.success(
                    "✅ **주의 사항**\n- 현재로서는 큰 위협이 발견되지 않았습니다.\n- 하지만 모르는 번호의 링크는 항상 의심하는 습관이 중요합니다."
                )
