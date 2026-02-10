import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime


def show_notices():
    # 1. 상단 헤더 섹션 (제안서의 '공공 연계성' 및 '신뢰도' 강조)
    st.markdown("### 📡 실시간 위협 인텔리전스 (KISA · 경찰청 연동)")
    st.write(
        "국내외 보안 기관에서 수집된 실시간 피싱 트렌드와 대응 지침을 미디어와 함께 제공합니다."
    )

    # --- 2. 위협 현황 브리핑 (대시보드형 시각화) ---
    st.markdown("#### 📊 금주 주요 위협 지표")

    # 가상의 통계 데이터 생성 (PRD 3.2 고도화된 데이터 활용 반영)
    threat_stats = pd.DataFrame(
        {
            "유형": ["보이스피싱", "스미싱(SMS)", "메신저피싱", "기타 스캠"],
            "발생건수": [124, 452, 89, 45],
        }
    )

    m1, m2, m3 = st.columns([1.5, 1, 1])

    with m1:
        # 도넛 차트로 위협 점유율 표시
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
        st.metric(
            "오늘의 위험 등급", "⚠️ 주의", delta="어제 대비 +12%", delta_color="inverse"
        )
        st.caption("지역별 발생 밀도 기반 산출")

    with m3:
        st.metric(
            "가장 빈번한 키워드",
            "연말정산",
            help="현재 스미싱 문구에서 가장 많이 발견되는 단어",
        )
        st.caption("KISA 실시간 스팸 DB 연동")

    st.markdown("---")

    # --- 3. [복구] 최신 예방 교육 영상 섹션 (폴-아카데미 연동) ---
    st.markdown("#### 📺 실시간 보안 브리핑 및 예방 영상")
    v_col1, v_col2 = st.columns(2)

    with v_col1:
        st.markdown(
            """
            <div style='background: white; padding: 15px; border-radius: 16px; border: 1px solid #E2E8F0; box-shadow: 0 4px 6px rgba(0,0,0,0.05);'>
                <p style='font-weight: 700; margin-bottom: 10px; color: #1E293B; font-size: 14px;'>🎬 [경찰청] 보이스피싱 실제 범행 사례</p>
            </div>
        """,
            unsafe_allow_html=True,
        )
        # 경찰청 공식 홍보 영상 등 관련 URL로 교체 가능
        st.video("https://youtu.be/nYLGDNQAjWQ?si=rk6xmO0-O4P3vIjS")

    with v_col2:
        st.markdown(
            """
            <div style='background: white; padding: 15px; border-radius: 16px; border: 1px solid #E2E8F0; box-shadow: 0 4px 6px rgba(0,0,0,0.05);'>
                <p style='font-weight: 700; margin-bottom: 10px; color: #1E293B; font-size: 14px;'>🎬 [금감원] 스미싱 예방 수칙 가이드</p>
            </div>
        """,
            unsafe_allow_html=True,
        )
        st.video("https://youtu.be/TOd3QEFfl34?si=EegZfWzXfZ_Ee4mJ")

    st.markdown("---")

    # --- 4. 검색 및 필터 (UX 최적화) ---
    f_col1, f_col2 = st.columns([3, 1])
    with f_col1:
        search_query = st.text_input(
            "🔍 특정 위협 키워드 검색",
            placeholder="예: 경찰청 사칭, 과태료, 긴급지원금...",
        )
    with f_col2:
        filter_level = st.selectbox(
            "위험도 필터", ["전체", "🚨 긴급(Critical)", "⚠️ 주의(Warning)", "ℹ️ 일반"]
        )

    # --- 5. 고도화된 보안 공지 카드 (Amara 스타일) ---
    notices_data = [
        {
            "level": "🚨 긴급(Critical)",
            "title": "국세청 연말정산 환급금 안내 사칭 스미싱 대량 유포",
            "date": "2026-02-11",
            "source": "KISA 보안공지",
            "risk_score": 98,
            "desc": "환급금 신청을 유도하는 URL(hometax-portal.xyz) 클릭 시 원격 제어 앱이 설치되어 자산이 탈취될 수 있습니다.",
            "guide": "국세청은 절대 문자 메시지로 환급금 신청 링크를 보내지 않습니다. 공식 홈택스 앱을 통해서만 확인하세요.",
            "link": "https://www.boho.or.kr",
        },
        {
            "level": "⚠️ 주의(Warning)",
            "title": "경찰청 사칭 '교통법규 위반 고지서' 사칭 주의",
            "date": "2026-02-10",
            "source": "경찰청 사이버수사국",
            "risk_score": 75,
            "desc": "실제 고지서와 유사한 양식으로 발송되며, 로그인 정보를 요구하는 가짜 경찰청 페이지로 연결됩니다.",
            "guide": "고지서의 사실 여부는 경찰청 교통민원24(이파인) 공식 홈페이지에서 직접 조회해야 합니다.",
            "link": "https://www.efine.go.kr",
        },
    ]

    for note in notices_data:
        # 필터링 및 검색 로직
        if filter_level != "전체" and note["level"] != filter_level:
            continue
        if search_query and search_query not in note["title"]:
            continue

        # 위험 등급별 테마 설정
        is_critical = "🚨" in note["level"]
        theme_color = "#EF4444" if is_critical else "#F59E0B"
        bg_color = "#FEF2F2" if is_critical else "#FFFBEB"

        # 카드 렌더링
        st.markdown(
            f"""
            <div style='background-color: {bg_color}; border-left: 6px solid {theme_color}; padding: 25px; border-radius: 16px; margin-bottom: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);'>
                <div style='display: flex; justify-content: space-between; align-items: flex-start;'>
                    <div style='background-color: {theme_color}; color: white; padding: 4px 12px; border-radius: 8px; font-size: 11px; font-weight: 800;'>{note["level"]}</div>
                    <small style='color: #64748B;'>{note["date"]} | {note["source"]}</small>
                </div>
                <h4 style='color: #0F172A; margin: 15px 0 10px 0; font-size: 18px;'>{note["title"]}</h4>
                <p style='color: #334155; font-size: 14px; line-height: 1.6; margin-bottom: 10px;'>{note["desc"]}</p>
                <div style='background-color: rgba(255,255,255,0.6); padding: 12px; border-radius: 8px; border: 1px dashed {theme_color};'>
                    <span style='color: {theme_color}; font-weight: 700; font-size: 13px;'>✅ 대응 지침:</span>
                    <span style='color: #1E293B; font-size: 13px;'> {note["guide"]}</span>
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )

        # 상세 링크 버튼
        if note["link"] != "#":
            st.link_button(
                f"🔗 {note['source']} 공식 자료 원문 확인",
                note["link"],
                use_container_width=True,
            )

    # --- 6. [복구] 실시간 위험 키워드 클라우드 ---
    st.markdown("---")
    st.subheader("🔥 실시간 탐지 급상승 키워드")
    st.write(
        "AI 엔진이 현재 수집 중인 위협 패턴에서 가장 빈번하게 등장하는 단어입니다."
    )

    keywords = [
        "#환급금신청",
        "#과태료부과",
        "#주소지불명",
        "#수사관사칭",
        "#대출금리",
        "#보안인증",
    ]
    cols = st.columns(len(keywords))

    for i, kw in enumerate(keywords):
        cols[i].markdown(
            f"""
            <div style='background:#E2E8F0; padding:10px 5px; border-radius:12px; text-align:center; font-size:12px; font-weight:700; color:#475569; box-shadow: inset 0 1px 2px rgba(0,0,0,0.05);'>
                {kw}
            </div>
        """,
            unsafe_allow_html=True,
        )

    # 하단 팁 섹션
    st.markdown("---")
    st.info(
        "💡 **AI 보안 코치:** 최근 '연말정산' 관련 스미싱이 급증하고 있습니다. 국세청 사칭 문자의 링크는 절대 클릭하지 마세요!"
    )
