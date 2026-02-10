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

try:
    from ai_engine.processor import PolGuardProcessor
    from ai_engine.voice_processor import VoiceTranscriber

    # 실시간 녹음 기능을 위한 라이브러리
    from streamlit_mic_recorder import mic_recorder
except ImportError as e:
    st.error(f"❌ 필수 라이브러리 로드 실패: {e}")


# [🚨 핵심] 리포트 저장 함수 (reports.py 중복 문제 방지용 내장)
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

    # [🚀 고도화] 3개의 배너(탭)로 구성
    tab1, tab2, tab3 = st.tabs(
        ["💬 문자/카톡 분석", "📂 음성 파일 분석", "🔴 실시간 직접 녹음"]
    )

    # --- 탭 1: 문자/카톡 분석 ---
    with tab1:
        st.markdown("#### 📝 텍스트 기반 위협 탐지")
        input_text = st.text_area(
            "메시지 전문을 입력하세요",
            placeholder="예: [국제발신] 해외인증번호 [9402] 발송. 본인 아닐 시 신고 요망...",
            height=150,
        )
        if st.button("🚀 메시지 분석 시작", key="btn_text", use_container_width=True):
            if input_text.strip():
                with st.spinner("패턴 분석 및 위협 등급 산출 중..."):
                    try:
                        res = st.session_state.engine.analyze(input_text)
                    except:
                        res = st.session_state.engine.analyze_text(input_text)
                    save_report(res)
                    display_result(res)
            else:
                st.warning("분석할 내용을 입력해주세요.")

    # --- 탭 2: 음성 파일 분석 ---
    with tab2:
        st.markdown("#### 📂 기존 녹음 파일 정밀 분석")
        audio_file = st.file_uploader(
            "통화 녹음 파일 업로드 (mp4, mp3, wav)", type=["mp4", "mp3", "wav"]
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
        st.write("스피커폰 통화 중이거나 주변 의심 음성을 즉시 녹음하여 분석합니다.")

        # 실시간 녹음 UI 컴포넌트
        audio_record = mic_recorder(
            start_prompt="⏺️ 실시간 녹음 시작",
            stop_prompt="⏹️ 녹음 중지 및 즉시 분석",
            just_once=False,
            use_container_width=True,
            format="wav",
            key="recorder",
        )

        if audio_record:
            # 녹음된 바이트를 파일 객체로 변환
            audio_bytes = BytesIO(audio_record["bytes"])
            audio_bytes.name = "live_recording.wav"
            st.audio(audio_record["bytes"])

            if st.button(
                "🔍 녹음 내용 AI 정밀 진단", key="btn_live", use_container_width=True
            ):
                process_voice_analysis(audio_bytes)


def process_voice_analysis(audio_data):
    """음성 분석 공통 프로세스 및 실시간 시각화"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    wave_chart = st.empty()

    with st.spinner("AI 신호 처리 및 텍스트 데이터 추출 중..."):
        full_text = st.session_state.transcriber.transcribe(audio_data)
        words = full_text.split()

        # 실시간 스트리밍 시각화 연출
        for i in range(len(words)):
            wave_chart.line_chart(np.random.randn(20))
            status_text.markdown(f"**📡 데이터 추출 중:** {' '.join(words[:i+1])}")

            # 위험 키워드 발견 시 즉시 알림
            danger_keywords = [
                "검찰",
                "계좌",
                "이체",
                "수사",
                "금감원",
                "대출",
                "보안카드",
            ]
            if any(kw in words[i] for kw in danger_keywords):
                st.toast(f"🚨 위협 패턴 감지: {words[i]}", icon="⚠️")

            progress_bar.progress((i + 1) / len(words))
            time.sleep(0.1)

    try:
        res = st.session_state.engine.analyze(full_text)
    except:
        res = st.session_state.engine.analyze_text(full_text)

    save_report(res)
    display_result(res, is_voice=True)


def display_result(res, is_voice=False):
    risk = res.get("risk_score", 0)
    color = "#EF4444" if risk >= 60 else "#F59E0B" if risk >= 30 else "#10B981"

    st.markdown("---")
    st.markdown(
        f"#### 종합 분석 판정: <span style='color:{color}'>{res.get('verdict')}</span>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        st.metric("위험 지수", f"{risk}%")
        st.info(f"**🕵️ AI 정밀 진단 리포트:**\n\n{res.get('ai_analysis')}")

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
            margin=dict(t=30, b=30, l=40, r=40),
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

    # 고위험군 긴급 대응 섹션
    if risk >= 60:
        st.error(
            "🚨 **심각한 위협이 확인되었습니다! 아래 행동 강령을 즉시 실행하세요.**"
        )

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(
                """<div style='background:#FEF2F2; padding:15px; border-radius:12px; border:1px solid #FCA5A5;'>
                        <b style='color:#B91C1C;'>1. 즉시 중단</b><br><small>통화를 끊고 메시지를 삭제하세요.</small></div>""",
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                """<div style='background:#FEF2F2; padding:15px; border-radius:12px; border:1px solid #FCA5A5;'>
                        <b style='color:#B91C1C;'>2. 지급 정지</b><br><small>거래 은행 고객센터에 전화를 거세요.</small></div>""",
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown(
                """<div style='background:#FEF2F2; padding:15px; border-radius:12px; border:1px solid #FCA5A5;'>
                        <b style='color:#B91C1C;'>3. 수사기관 신고</b><br><small>112 또는 1332로 신고하세요.</small></div>""",
                unsafe_allow_html=True,
            )

        st.write("")
        b1, b2 = st.columns(2)
        b1.link_button(
            "📞 경찰청 신고 (112)", "https://www.police.go.kr", use_container_width=True
        )
        b2.link_button(
            "🏦 금감원 신고 (1332)", "https://fss.or.kr", use_container_width=True
        )
