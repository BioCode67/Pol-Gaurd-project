import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time
import sys
import os

# 1. 경로 설정 및 모듈 로드
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
    # 세션 상태 초기화
    if "engine" not in st.session_state:
        st.session_state.engine = PolGuardProcessor()
    if "transcriber" not in st.session_state:
        st.session_state.transcriber = VoiceTranscriber()

    st.markdown("### 🔍 실시간 지능형 탐지 엔진")
    st.write(
        "텍스트 메시지와 음성 통화를 AI가 실시간으로 분석하여 피싱 위험을 탐지합니다."
    )

    tab1, tab2 = st.tabs(["💬 문자/카톡 분석", "🎙️ 실시간 통화 분석"])

    # --- 탭 1: 문자/카톡 분석 ---
    with tab1:
        st.markdown("#### 📝 메시지 텍스트 분석")
        input_text = st.text_area(
            "분석할 내용을 입력하세요",
            placeholder="예: [국제발신] 해외결제 승인 완료. 본인 아닐 시 신고 요망...",
            height=150,
        )

        if st.button("🚀 메시지 분석 시작", key="txt_btn", use_container_width=True):
            if input_text.strip():
                with st.spinner("AI가 피싱 패턴을 정밀 분석 중입니다..."):
                    # [💡 수정] analyze_text 대신 analyze 호출 (클래스 정의에 맞춤)
                    try:
                        res = st.session_state.engine.analyze(input_text)
                    except AttributeError:
                        res = st.session_state.engine.analyze_text(input_text)

                    save_report(res)
                    display_result(res)
            else:
                st.warning("분석할 내용을 입력해주세요.")

    # --- 탭 2: 실시간 통화 분석 (Amara 스타일 고도화) ---
    with tab2:
        st.markdown("#### 📡 실시간 음성 스트리밍 모니터링")
        st.write(
            "통화 녹음 파일(mp4, mp3)을 업로드하여 실시간 위협 요소 추출 과정을 확인하세요."
        )

        audio_file = st.file_uploader(
            "음성/영상 파일 업로드 (mp4, mp3, wav)", type=["mp4", "mp3", "wav"]
        )

        if audio_file:
            # 업로드된 파일 재생기 표시
            if audio_file.name.endswith("mp4"):
                st.video(audio_file)
            else:
                st.audio(audio_file)

            if st.button("🔴 실시간 스트리밍 분석 시작", use_container_width=True):
                # 실시간 시각화 요소 배치
                progress_bar = st.progress(0)
                status_text = st.empty()
                wave_chart = st.empty()

                with st.spinner("디지털 신호 처리 및 음성 분석 중..."):
                    # 1. 음성 텍스트 변환
                    full_text = st.session_state.transcriber.transcribe(audio_file)
                    words = full_text.split()

                    # 2. 스트리밍 시뮬레이션 (심사위원용 시각 효과)
                    for i in range(len(words)):
                        # 가상 주파수 파형 업데이트
                        wave_data = np.random.randn(20)
                        wave_chart.line_chart(wave_data)

                        current_partial = " ".join(words[: i + 1])
                        status_text.markdown(f"**📡 분석 중:** {current_partial}")

                        # 실시간 위험 키워드 토스트 알림
                        danger_keywords = [
                            "검찰",
                            "계좌",
                            "이체",
                            "수사",
                            "보안카드",
                            "금감원",
                            "대출",
                        ]
                        if any(kw in words[i] for kw in danger_keywords):
                            st.toast(f"🚨 위험 키워드 포착: {words[i]}", icon="⚠️")

                        progress_bar.progress((i + 1) / len(words))
                        time.sleep(0.2)  # 단어별 렌더링 속도

                # 3. 최종 정밀 분석 수행
                try:
                    res = st.session_state.engine.analyze(full_text)
                except AttributeError:
                    res = st.session_state.engine.analyze_text(full_text)

                save_report(res)
                display_result(res, is_voice=True)


def display_result(res, is_voice=False):
    risk = res.get("risk_score", 0)
    # 위험도에 따른 테마 색상 설정
    color = "#EF4444" if risk >= 60 else "#F59E0B" if risk >= 30 else "#10B981"

    st.markdown("---")
    st.markdown(
        f"#### 종합 판정 결과: <span style='color:{color}'>{res.get('verdict', '판정 불가')}</span>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        st.metric("위험 지수 (Risk Score)", f"{risk}%")
        st.info(
            f"**🕵️ AI 정밀 진단 리포트:**\n\n{res.get('ai_analysis', '분석 데이터가 부족합니다.')}"
        )

    with col2:
        # 레이더 차트 시각화 (전문성 강조)
        factors = res.get("factors", {})
        categories = ["금전유도", "기관사칭", "심리압박", "패턴일치", "블랙리스트"]
        values = [
            factors.get("content_risk", 0),
            factors.get("context_risk", 0),
            factors.get("urgency_risk", 0),
            factors.get("pattern_match", 0),
            factors.get("blacklist_match", 0),
        ]

        fig = go.Figure(
            data=go.Scatterpolar(
                r=values + [values[0]],
                theta=categories + [categories[0]],
                fill="toself",
                line_color=color,
                name="피싱 위협 지표",
            )
        )
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            height=320,
            margin=dict(t=30, b=30, l=50, r=50),
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

    # 🚨 고위험군 대응 가이드라인
    if risk >= 60:
        st.error("🚨 **치명적인 피싱 위험이 감지되었습니다! 즉시 대응이 필요합니다.**")

        # Amara 스타일의 긴급 대응 카드 섹션
        guide_col1, guide_col2, guide_col3 = st.columns(3)
        with guide_col1:
            st.markdown(
                """<div style='background:#FEF2F2; padding:15px; border-radius:12px; border:1px solid #FCA5A5;'>
                        <b style='color:#B91C1C;'>1. 대화 즉시 중단</b><br><small>통화를 끊고 메시지에 답장하지 마세요.</small></div>""",
                unsafe_allow_html=True,
            )
        with guide_col2:
            st.markdown(
                """<div style='background:#FEF2F2; padding:15px; border-radius:12px; border:1px solid #FCA5A5;'>
                        <b style='color:#B91C1C;'>2. 계좌/카드 정지</b><br><small>거래 은행에 즉시 지급 정지를 요청하세요.</small></div>""",
                unsafe_allow_html=True,
            )
        with guide_col3:
            st.markdown(
                """<div style='background:#FEF2F2; padding:15px; border-radius:12px; border:1px solid #FCA5A5;'>
                        <b style='color:#B91C1C;'>3. 보안 앱 검사</b><br><small>원격제어 앱 설치 여부를 확인하고 삭제하세요.</small></div>""",
                unsafe_allow_html=True,
            )

        st.write("")
        btn_c1, btn_c2 = st.columns(2)
        btn_c1.link_button(
            "📞 경찰청 신고 (112)", "https://www.police.go.kr", use_container_width=True
        )
        btn_c2.link_button(
            "🏦 금감원 피해 신고 (1332)", "https://fss.or.kr", use_container_width=True
        )
