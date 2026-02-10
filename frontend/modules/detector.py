import streamlit as st
import plotly.graph_objects as go
import sys
import os

# 1. 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.append(project_root)

# 2. 필요한 모듈들 임포트
try:
    from ai_engine.processor import PolGuardProcessor
    from ai_engine.voice_processor import VoiceTranscriber
    from .reports import save_report
except ImportError as e:
    st.error(f"❌ 모듈 로드 오류: {e}")
    print(f"Import Error details: {e}")


def show_detector():
    # 엔진 및 음성처리기 초기화
    if "engine" not in st.session_state:
        st.session_state.engine = PolGuardProcessor()
    if "transcriber" not in st.session_state:
        st.session_state.transcriber = VoiceTranscriber()

    st.title("🔍 실시간 스미싱/보이스피싱 탐지")

    # 탭 메뉴 구성 (텍스트 분석 / 음성 분석)
    tab1, tab2 = st.tabs(["💬 문자/카톡 분석", "🎙️ 통화 녹음 분석"])

    # --- 탭 1: 텍스트 분석 ---
    with tab1:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("### 📥 메시지 분석")
            user_input = st.text_area(
                "메시지 전문",
                placeholder="내용을 입력하세요...",
                height=150,
                key="txt_input",
            )
            if st.button("🚀 메시지 분석 시작", use_container_width=True):
                if user_input.strip():
                    with st.spinner("AI 분석 중..."):
                        res = st.session_state.engine.analyze(user_input)
                        st.session_state["last_res"] = res
                        save_report(res)
                else:
                    st.warning("텍스트를 입력해주세요.")

    # --- 탭 2: 음성 분석 (주형 님이 원하신 공간!) ---
    with tab2:
        st.markdown("### 📥 통화 녹음 파일 분석")
        audio_file = st.file_uploader(
            audio_file=st.file_uploader(
                "파일 업로드 (mp3, wav, m4a, mp4)", type=["mp3", "wav", "m4a", "mp4"]
            )
        )

        if audio_file is not None:
            # 영상 파일일 경우 화면에 플레이어를 표시
            if audio_file.name.endswith("mp4"):
                st.video(audio_file)
            else:
                st.audio(audio_file)
            if st.button("🎤 음성 인식 및 분석 시작", use_container_width=True):
                with st.spinner("음성을 텍스트로 변환하고 있습니다..."):
                    # 1. STT 실행
                    transcribed_text = st.session_state.transcriber.transcribe(
                        audio_file
                    )

                    if "❌" in transcribed_text:  # 에러 발생 시
                        st.error(transcribed_text)
                    else:
                        st.success("✅ 음성 인식 성공!")
                        st.info(f"**변환된 내용:** {transcribed_text}")

                        # 2. 변환된 텍스트로 AI 분석 실행
                        with st.spinner("AI가 위험도를 분석 중입니다..."):
                            res = st.session_state.engine.analyze(transcribed_text)
                            st.session_state["last_res"] = res
                            save_report(res)

    # --- 공통 결과 표시 구역 (차트 및 리포트) ---
    if "last_res" in st.session_state:
        st.markdown("---")
        res = st.session_state["last_res"]

        c_left, c_right = st.columns([1, 1])

        with c_left:
            # 위험도 수치 및 판정
            risk = res.get("risk_score", 0)
            color = "red" if risk >= 60 else "orange" if risk >= 30 else "green"
            st.subheader(f"종합 판정: :{color}[{res.get('verdict', '분석 불가')}]")
            st.metric("위험 점수", f"{risk}%")
            st.write(f"**🕵️ 분석 근거:** {res.get('ai_analysis', '내용 없음')}")

        with c_right:
            # 레이더 차트 시각화
            f = res.get("factors", {})
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

            fig = go.Figure(
                data=go.Scatterpolar(
                    r=values + [values[0]],
                    theta=categories + [categories[0]],
                    fill="toself",
                    line_color="#FF4B4B",
                )
            )
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                showlegend=False,
                margin=dict(l=20, r=20, t=20, b=20),
            )
            st.plotly_chart(fig, use_container_width=True)
