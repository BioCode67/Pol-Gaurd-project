import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime


def show_notices():
    st.markdown("### 📡 실시간 위협 인텔리전스 & 미디어 피드")
    st.write("외부 보안 전문 기관의 실시간 정보와 최신 예방 교육 영상을 제공합니다.")

    # --- 1. 위협 현황 브리핑 ---
    st.markdown("#### 📊 금주 주요 위협 지표")
    threat_stats = pd.DataFrame(
        {
            "유형": ["보이스피싱", "스미싱(SMS)", "메신저피싱", "기타 스캠"],
            "발생건수": [124, 452, 89, 45],
        }
    )

    m1, m2, m3 = st.columns([1.5, 1, 1])
    with m1:
        fig = px.pie(
            threat_stats,
            values="발생건수",
            names="유형",
            hole=0.6,
            color_discrete_sequence=px.colors.sequential.Blues_r,
        )
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=180, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    with m2:
        st.metric("오늘의 위험 등급", "⚠️ 주의", delta="+12%", delta_color="inverse")
    with m3:
        st.metric("주요 키워드", "연말정산")

    st.markdown("---")

    # --- 2. [신규] 최신 예방 교육 영상 섹션 ---
    st.markdown("#### 📺 실시간 보안 브리핑 및 예방 영상")
    v_col1, v_col2 = st.columns(2)

    with v_col1:
        st.markdown(
            """
            <div style='background: white; padding: 15px; border-radius: 16px; border: 1px solid #E2E8F0; box-shadow: 0 4px 6px rgba(0,0,0,0.05);'>
                <p style='font-weight: 700; margin-bottom: 10px; color: #1E293B;'>🎬 [경찰청] 보이스피싱 실제 범행 음성</p>
            </div>
        """,
            unsafe_allow_html=True,
        )
        # 실제 경찰청 홍보 영상이나 관련 시뮬레이션 영상 주소를 넣으세요
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    with v_col2:
        st.markdown(
            """
            <div style='background: white; padding: 15px; border-radius: 16px; border: 1px solid #E2E8F0; box-shadow: 0 4px 6px rgba(0,0,0,0.05);'>
                <p style='font-weight: 700; margin-bottom: 10px; color: #1E293B;'>🎬 [금감원] 스미싱 예방 수칙 가이드</p>
            </div>
        """,
            unsafe_allow_html=True,
        )
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    st.markdown("---")

    # --- 3. 고도화된 보안 공지 카드 (Amara 스타일) ---
    notices_data = [
        {
            "level": "🚨 긴급(Critical)",
            "title": "국세청 연말정산 환급금 안내 사칭 스미싱 대량 유포",
            "date": "2026-02-11",
            "source": "KISA 보안공지",
            "desc": "환급금 신청을 유도하는 URL 클릭 시 악성 앱이 설치되어 자산이 탈취될 수 있습니다.",
            "guide": "국세청 공식 앱을 통해서만 환급 정보를 확인하세요.",
            "link": "https://www.boho.or.kr",
        }
    ]

    for note in notices_data:
        is_critical = "🚨" in note["level"]
        theme_color = "#EF4444" if is_critical else "#F59E0B"
        bg_color = "#FEF2F2" if is_critical else "#FFFBEB"

        st.markdown(
            f"""
            <div style='background-color: {bg_color}; border-left: 6px solid {theme_color}; padding: 25px; border-radius: 16px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);'>
                <div style='display: flex; justify-content: space-between;'>
                    <div style='background-color: {theme_color}; color: white; padding: 4px 12px; border-radius: 8px; font-size: 11px; font-weight: 800;'>{note["level"]}</div>
                    <small style='color: #64748B;'>{note["date"]} | {note["source"]}</small>
                </div>
                <h4 style='color: #0F172A; margin: 15px 0 10px 0;'>{note["title"]}</h4>
                <p style='color: #334155; font-size: 14px;'>{note["desc"]}</p>
                <div style='background: white; padding: 12px; border-radius: 8px; border: 1px dashed {theme_color};'>
                    <span style='color: {theme_color}; font-weight: 700;'>✅ 대응:</span> {note["guide"]}
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )
        st.link_button(f"🔗 원문 자료 확인하기", note["link"], use_container_width=True)
