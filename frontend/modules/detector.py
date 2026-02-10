import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time
import sys
import os
import json
from datetime import datetime

# 1. 경로 설정 및 모듈 로드
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.append(project_root)

# 데이터 저장 경로 설정
REPORT_FILE = os.path.join(project_root, "data", "reports.json")

try:
    from ai_engine.processor import PolGuardProcessor
    from ai_engine.voice_processor import VoiceTranscriber
except ImportError as e:
    st.error(f"❌ 모듈 로드 오류: {e}")


# [🚨 핵심 해결] 리포트 저장 함수 정의
def save_report(res):
    """분석 결과를 JSON 파일에 저장합니다."""
    if not os.path.exists(os.path.dirname(REPORT_FILE)):
        os.makedirs(os.path.dirname(REPORT_FILE))

    # 기존 데이터 로드
    reports = []
    if os.path.exists(REPORT_FILE):
        try:
            with open(REPORT_FILE, "r", encoding="utf-8") as f:
                reports = json.load(f)
        except:
            reports = []

    # 새 리포트 추가
    res["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reports.insert(0, res)  # 최신순 저장

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(reports, f, ensure_ascii=False, indent=4)


def show_detector():
    # 세션 상태 초기화
    if "engine" not in st.session_state:
        st.session_state.engine = PolGuardProcessor()
    if "transcriber" not in st.session_state:
        st.session_state.transcriber = VoiceTranscriber()

    st.markdown("### 🔍 실시간 지능형 탐지 엔진")
    st.write("AI가 메시지와 음성을 실시간으로 대조하여 피싱 위협을 차단합니다.")

    tab1, tab2 = st.tabs(["💬 문자/카톡 분석", "🎙️ 실시간 통화 분석"])

    # --- 탭 1: 문자 분석 ---
    with tab1:
        input_text = st.text_area(
            "메시지 내용 입력", placeholder="내용을 붙여넣으세요...", height=150
        )
        if st.button("🚀 메시지 분석 시작", key="txt_btn", use_container_width=True):
            if input_text.strip():
                with st.spinner("패턴 분석 중..."):
                    try:
                        res = st.session_state.engine.analyze(input_text)
                    except AttributeError:
                        res = st.session_state.engine.analyze_text(input_text)
                    save_report(res)
                    display_result(res)
            else:
                st.warning("내용을 입력해주세요.")

    # --- 탭 2: 실시간 통화 분석 ---
    with tab2:
        st.markdown("#### 📡 실시간 음성 스트리밍 모니터링")
        audio_file = st.file_uploader(
            "음성/영상 파일 업로드 (mp4, mp3)", type=["mp4", "mp3", "wav"]
        )

        if audio_file:
            if audio_file.name.endswith("mp4"):
                st.video(audio_file)
            else:
                st.audio(audio_file)

            if st.button("🔴 실시간 스트리밍 분석 시작", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()
                wave_chart = st.empty()

                with st.spinner("분석 중..."):
                    full_text = st.session_state.transcriber.transcribe(audio_file)
                    words = full_text.split()

                    # 실시간 시각화 시뮬레이션
                    for i in range(len(words)):
                        wave_chart.line_chart(np.random.randn(20))
                        status_text.markdown(
                            f"**📡 모니터링:** {' '.join(words[:i+1])}"
                        )

                        danger_keywords = [
                            "검찰",
                            "계좌",
                            "이체",
                            "수사",
                            "보안카드",
                            "금감원",
                        ]
                        if any(kw in words[i] for kw in danger_keywords):
                            st.toast(f"🚨 위험 키워드: {words[i]}", icon="⚠️")

                        progress_bar.progress((i + 1) / len(words))
                        time.sleep(0.2)

                try:
                    res = st.session_state.engine.analyze(full_text)
                except AttributeError:
                    res = st.session_state.engine.analyze_text(full_text)

                save_report(res)
                display_result(res, is_voice=True)


def display_result(res, is_voice=False):
    risk = res.get("risk_score", 0)
    color = "#EF4444" if risk >= 60 else "#F59E0B" if risk >= 30 else "#10B981"

    st.markdown("---")
    st.markdown(
        f"#### 종합 판정: <span style='color:{color}'>{res.get('verdict')}</span>",
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
        )
        st.plotly_chart(fig, use_container_width=True)

    if risk >= 60:
        st.error("🚨 **즉각적인 대응이 필요합니다!**")
        st.link_button(
            "📞 경찰청 신고 (112)", "https://www.police.go.kr", use_container_width=True
        )
