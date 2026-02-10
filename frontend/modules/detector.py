import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time
import sys
import os
import json
from datetime import datetime
from io import BytesIO

# 1. 경로 설정 및 모듈 로드
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.append(project_root)

# 데이터 저장 경로 설정
REPORT_FILE = os.path.join(project_root, "data", "reports.json")

# [🚨 핵심 해결] 라이브러리 임포트 여부를 전역 변수로 관리
MIC_RECORDER_AVAILABLE = False
try:
    from ai_engine.processor import PolGuardProcessor
    from ai_engine.voice_processor import VoiceTranscriber

    # 라이브러리 로드 시도
    from streamlit_mic_recorder import mic_recorder

    MIC_RECORDER_AVAILABLE = True
except ImportError:
    st.error("❌ 'streamlit-mic-recorder' 라이브러리를 찾을 수 없습니다.")
    st.info(
        "💡 해결 방법: 프로젝트 루트의 'requirements.txt' 파일에 'streamlit-mic-recorder'를 추가하고 다시 푸시(p)하세요."
    )


# 리포트 저장 함수 (내부 정의)
def save_report(res):
    if not os.path.exists(os.path.dirname(REPORT_FILE)):
        os.makedirs(os.path.dirname(REPORT_FILE))

    reports = []
    if os.path.exists(REPORT_FILE):
        try:
            with open(REPORT_FILE, "r", encoding="utf-8") as f:
                reports = json.load(f)
        except:
            reports = []

    res["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reports.insert(0, res)

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(reports, f, ensure_ascii=False, indent=4)


def show_detector():
    if "engine" not in st.session_state:
        st.session_state.engine = PolGuardProcessor()
    if "transcriber" not in st.session_state:
        st.session_state.transcriber = VoiceTranscriber()

    st.markdown("### 🔍 실시간 지능형 탐지 엔진")
    st.write("AI가 다양한 채널의 위협 데이터를 실시간으로 대조하여 피싱을 차단합니다.")

    # 3개의 배너(탭) 구성
    tab1, tab2, tab3 = st.tabs(
        ["💬 문자/카톡 분석", "📂 음성 파일 분석", "🔴 실시간 직접 녹음"]
    )

    # --- 탭 1: 문자/카톡 분석 ---
    with tab1:
        st.markdown("#### 📝 텍스트 기반 위협 탐지")
        input_text = st.text_area(
            "메시지 전문 입력",
            placeholder="분석할 메시지 내용을 붙여넣으세요...",
            height=150,
        )
        if st.button("🚀 메시지 분석 시작", key="btn_text", use_container_width=True):
            if input_text.strip():
                with st.spinner("AI 정밀 분석 중..."):
                    try:
                        res = st.session_state.engine.analyze(input_text)
                    except:
                        res = st.session_state.engine.analyze_text(input_text)
                    save_report(res)
                    display_result(res)

    # --- 탭 2: 음성 파일 분석 ---
    with tab2:
        st.markdown("#### 📂 기존 녹음 파일 정밀 분석")
        audio_file = st.file_uploader(
            "파일 업로드 (mp4, mp3, wav)", type=["mp4", "mp3", "wav"]
        )
        if audio_file:
            if audio_file.name.endswith("mp4"):
                st.video(audio_file)
            else:
                st.audio(audio_file)
            if st.button(
                "🔵 파일 인텔리전스 분석 시작", key="btn_file", use_container_width=True
            ):
                process_voice_analysis(audio_file)

    # --- 탭 3: 실시간 직접 녹음 분석 ---
    with tab3:
        st.markdown("#### 🎤 현장 음성 실시간 캡처")
        if MIC_RECORDER_AVAILABLE:
            st.write("마이크 버튼을 눌러 즉시 녹음을 시작하고 AI 분석을 요청하세요.")

            audio_record = mic_recorder(
                start_prompt="⏺️ 실시간 녹음 시작",
                stop_prompt="⏹️ 녹음 중지 및 즉시 분석",
                just_once=False,
                use_container_width=True,
                format="wav",
                key="recorder",
            )

            if audio_record:
                audio_bytes = BytesIO(audio_record["bytes"])
                audio_bytes.name = "live_recording.wav"
                st.audio(audio_record["bytes"])
                if st.button(
                    "🔍 녹음 내용 AI 정밀 진단",
                    key="btn_live",
                    use_container_width=True,
                ):
                    process_voice_analysis(audio_bytes)
        else:
            st.warning(
                "⚠️ 실시간 녹음 기능이 현재 비활성화 상태입니다. 라이브러리(streamlit-mic-recorder) 설치가 필요합니다."
            )


def process_voice_analysis(audio_data):
    """음성 분석 공통 프로세스 및 코덱 에러 대응"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    wave_chart = st.empty()

    with st.spinner("🎙️ AI 신호 분석 및 텍스트 데이터 추출 중..."):
        try:
            # 1. 음성 데이터를 텍스트로 변환 (STT)
            full_text = st.session_state.transcriber.transcribe(audio_data)

            if not full_text or len(full_text.strip()) == 0:
                st.error(
                    "❌ 분석 실패: 음성에서 유효한 텍스트를 추출할 수 없습니다. (마이크 설정을 확인하세요)"
                )
                return

            words = full_text.split()

            # 2. 실시간 모니터링 시뮬레이션
            for i in range(len(words)):
                wave_chart.line_chart(np.random.randn(20))
                status_text.markdown(f"**📡 데이터 모니터링:** {' '.join(words[:i+1])}")

                # 경찰청 권고 위험 키워드 탐지
                danger_keywords = [
                    "검찰",
                    "계좌",
                    "이체",
                    "수사",
                    "금감원",
                    "대출",
                    "명의",
                ]
                if any(kw in words[i] for kw in danger_keywords):
                    st.toast(f"🚨 위협 패턴 감지: {words[i]}", icon="⚠️")

                progress_bar.progress((i + 1) / len(words))
                time.sleep(0.1)

            # 3. LLM 엔진 최종 분석
            try:
                res = st.session_state.engine.analyze(full_text)
            except:
                res = st.session_state.engine.analyze_text(full_text)

            save_report(res)
            display_result(res, is_voice=True)

        except Exception as e:
            st.error(f"❌ 데이터 분석 중 오류 발생: {e}")
            st.info(
                "💡 mp4 파일의 경우 코덱 호환성 문제가 발생할 수 있습니다. wav나 mp3 파일을 권장합니다."
            )


def display_result(res, is_voice=False):
    """분석 결과 시각화 및 경찰청 신고 연동"""
    risk = res.get("risk_score", 0)
    # 점수가 1 미만(0.95 등)으로 넘어올 경우를 대비해 보정
    if risk <= 1.0 and risk > 0:
        risk = int(risk * 100)
    color = "#EF4444" if risk >= 60 else "#F59E0B" if risk >= 30 else "#10B981"
    st.markdown("---")
    st.markdown(
        f"#### 종합 분석 판정: <span style='color:{color}'>{res.get('verdict')}</span>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        st.metric("위험 점수", f"{risk}%")
        st.info(f"**🕵️ AI 정밀 진단:**\n\n{res.get('ai_analysis')}")

    with col2:
        factors = res.get("factors", {})
        categories = ["금전유도", "기관사칭", "심리압박", "패턴일치", "블랙리스트"]
        values = [
            factors.get(k, 0)
            for k in [
                "content_risk",
                "context_risk",
                "urgency_risk",
                "pattern_match",
                "blacklist_match",
            ]
        ]

        # 레이더 차트를 통한 위협 유형 시각화
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
            margin=dict(t=30, b=30, l=30, r=30),
        )
        st.plotly_chart(fig, use_container_width=True)

    # 🚨 고위험군 대응 조치
    if risk >= 60:
        st.error("🚨 **즉각적인 대응이 필요합니다!** 지시된 계좌로 송금하지 마세요.")
        btn_c1, btn_c2 = st.columns(2)
        btn_c1.link_button(
            "📞 경찰청 신고 (112)", "https://www.police.go.kr", use_container_width=True
        )
        btn_c2.link_button(
            "🏦 금감원 신고 (1332)", "https://fss.or.kr", use_container_width=True
        )
