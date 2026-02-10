import streamlit as st
import requests
import plotly.graph_objects as go


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

        if st.button("🔍 Pol-Guard 전문 분석 실행"):
            if not user_input:
                st.warning("분석할 텍스트 내용을 입력해야 합니다.")
            else:
                with st.spinner("AI 가디언이 다차원 분석을 수행 중입니다..."):
                    res = requests.post(
                        "http://localhost:8000/analyze",
                        json={"text": user_input, "url": url_input},
                    ).json()
                    st.session_state["last_res"] = res

    with col2:
        if "last_res" in st.session_state:
            res = st.session_state["last_res"]
            f = res["factors"]

            # 전문가용 레이더 차트 (5대 핵심 지표)
            categories = [
                "금전유도",
                "기관사칭",
                "심리압박",
                "기술적패턴",
                "블랙리스트",
            ]
            values = [
                f["content_risk"],
                f["context_risk"],
                f["urgency_risk"],
                f["pattern_match"],
                f["blacklist_match"],
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
        st.markdown("---")
        st.markdown(f"### 📑 AI 종합 판정 리포트: **{res['verdict']}**")

        c1, c2, c3 = st.columns(3)
        c1.metric("종합 위험도", f"{res['risk_score']}%")
        c2.metric("사칭 가능성", "매우 높음" if f["context_risk"] > 0.7 else "낮음")
        c3.metric("데이터 신뢰도", "보호나라 DB 연동됨")

        # 전문가의 권고 사항
        with st.expander("📝 보안 전문가 권고 사항 확인"):
            if res["risk_score"] > 60:
                st.error(
                    "1. 절대 링크를 누르지 말고 해당 번호를 차단하세요.\n2. 이미 클릭했다면 비행기 모드를 켜고 악성 앱 검사를 수행하세요."
                )
            else:
                st.success(
                    "알려진 위협은 없으나, 출처가 불분명한 링크는 항상 주의가 필요합니다."
                )
