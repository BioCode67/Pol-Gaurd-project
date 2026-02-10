import streamlit as st
import plotly.graph_objects as go
import sys
import os

# 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.append(project_root)

try:
    from ai_engine.processor import PolGuardProcessor
    from ai_engine.voice_processor import VoiceTranscriber
    from .reports import save_report
except ImportError as e:
    st.error(f"❌ 모듈 로드 오류: {e}")


def show_detector():
    if "engine" not in st.session_state:
        st.session_state.engine = PolGuardProcessor()
    if "transcriber" not in st.session_state:
        st.session_state.transcriber = VoiceTranscriber()

    st.markdown("### 🔍 실시간 지능형 탐지 엔진")

    tab1, tab2 = st.tabs(["💬 문자/카톡 분석", "🎙️ 통화 녹음 분석"])

    # --- 탭 1: 텍스트 분석 ---
    with tab1:
        input_text = st.text_area(
            "분석할 메시지 내용을 입력하세요",
            placeholder="예: [국제발신] 고객님 결제 승인 완료...",
            height=150,
        )
        if st.button("실시간 분석 시작", key="btn_text"):
            if input_text:
                with st.spinner("AI가 피싱 패턴을 정밀 분석 중입니다..."):
                    res = st.session_state.engine.analyze_text(input_text)
                    save_report(res)
                    display_result(res)
            else:
                st.warning("분석할 내용을 입력해주세요.")

    # --- 탭 2: 음성 분석 ---
    with tab2:
        audio_file = st.file_uploader(
            "통화 녹음 파일 업로드 (mp4, mp3, wav)", type=["mp4", "mp3", "wav"]
        )
        if st.button("음성 분석 시작", key="btn_audio"):
            if audio_file:
                with st.spinner("음성을 텍스트로 변환하고 분석 중입니다..."):
                    text = st.session_state.transcriber.transcribe(audio_file)
                    res = st.session_state.engine.analyze_text(text)
                    save_report(res)
                    display_result(res, is_voice=True)


def display_result(res, is_voice=False):
    risk = res.get("risk_score", 0)
    color = "#EF4444" if risk >= 60 else "#F59E0B" if risk >= 30 else "#10B981"

    st.markdown(
        f"#### 분석 결과: <span style='color:{color}'>{res.get('verdict', '분석 완료')}</span>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        st.metric("위험 점수", f"{risk}%")
        st.info(f"**🕵️ AI 분석 근거:**\n\n{res.get('ai_analysis', '내용 없음')}")

    with col2:
        f = res.get("factors", {})
        categories = ["금전유도", "기관사칭", "심리압박", "패턴일치", "블랙리스트"]
        values = [
            f.get("content_risk", 0),
            f.get("context_risk", 0),
            f.get("urgency_risk", 0),
            f.get("pattern_match", 0),
            f.get("blacklist_match", 0),
        ]

        fig = go.Figure(
            data=go.Scatterpolar(
                r=values + [values[0]],
                theta=categories + [categories[0]],
                fill="toself",
                line_color=color,
            )
        )
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            height=300,
            margin=dict(t=20, b=20, l=40, r=40),
        )
        st.plotly_chart(fig, use_container_width=True)

    # [🚀 고도화 2번] 긴급 대응 시스템 추가
    if risk >= 60:
        st.markdown("---")
        st.error("🚨 **심각한 피싱 위협이 감지되었습니다! 아래 지침을 즉시 따르세요.**")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(
                """<div style='background:#FEE2E2; padding:15px; border-radius:10px; border:1px solid #EF4444;'>
                        <p style='margin:0; font-weight:bold; color:#B91C1C;'>1. 즉시 중단</p>
                        <p style='font-size:12px; color:#7F1D1D;'>통화를 끊고 링크 클릭이나 송금을 즉시 멈추세요.</p>
                        </div>""",
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                """<div style='background:#FEE2E2; padding:15px; border-radius:10px; border:1px solid #EF4444;'>
                        <p style='margin:0; font-weight:bold; color:#B91C1C;'>2. 계좌 정지</p>
                        <p style='font-size:12px; color:#7F1D1D;'>거래 은행 고객센터에 연락하여 지급 정지를 요청하세요.</p>
                        </div>""",
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown(
                """<div style='background:#FEE2E2; padding:15px; border-radius:10px; border:1px solid #EF4444;'>
                        <p style='margin:0; font-weight:bold; color:#B91C1C;'>3. 앱 삭제</p>
                        <p style='font-size:12px; color:#7F1D1D;'>상대방이 설치하라고 한 앱(원격제어 등)을 즉시 삭제하세요.</p>
                        </div>""",
                unsafe_allow_html=True,
            )

        st.write("")
        b1, b2 = st.columns(2)
        b1.link_button("📞 경찰청 신고 (112)", "https://www.police.go.kr")
        b2.link_button("🏦 금감원 피해 신고 (1332)", "https://fss.or.kr")
