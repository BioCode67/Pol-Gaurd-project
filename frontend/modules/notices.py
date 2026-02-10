import streamlit as st
from datetime import datetime


def show_notices():
    st.markdown("### 📢 실시간 위협 인텔리전스 피드")
    st.write(
        "경찰청 및 금융감독원 데이터를 기반으로 분석한 최신 피싱/스캠 트렌드입니다."
    )

    # --- 1. 검색 및 필터링 섹션 ---
    c1, c2 = st.columns([2, 1])
    with c1:
        st.text_input(
            "🔍 키워드로 보안 위협 검색", placeholder="예: 경찰청, 결제, 사칭..."
        )
    with c2:
        st.selectbox(
            "위험 등급별 보기",
            ["전체", "🚨 긴급(Critical)", "⚠️ 주의(Warning)", "ℹ️ 일반"],
        )

    st.markdown("---")

    # --- 2. 최신 보안 공지 리스트 (Amara 스타일 카드) ---

    # 공지 데이터 1: 긴급
    with st.container():
        st.markdown(
            """
            <div style='background-color: #FEF2F2; border-left: 5px solid #EF4444; padding: 20px; border-radius: 12px; margin-bottom: 20px;'>
                <span style='background-color: #EF4444; color: white; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: bold;'>CRITICAL</span>
                <h4 style='color: #991B1B; margin-top: 10px;'>경찰청 사칭 '교통법규 위반' 스미싱 대량 유포 주의</h4>
                <p style='color: #7F1D1D; font-size: 14px;'>과태료 부과를 사칭한 URL 클릭 시 악성 앱이 설치되어 금융 정보가 탈취됩니다.</p>
                <small style='color: #B91C1C;'>게시일: 2026-02-11 | 출처: 국가수사본부</small>
            </div>
        """,
            unsafe_allow_html=True,
        )

        with st.expander("✅ 상세 대응 수칙 확인"):
            st.write("1. 문자 내 포함된 URL(k-police.net 등) 절대 클릭 금지")
            st.write("2. '정부24' 또는 '교통민원24(efine)' 공식 앱을 통해서만 확인")
            st.write("3. 이미 클릭했다면 비행기 모드 전환 후 서비스 센터 방문")
            st.link_button("🔗 보도자료 원문 보기", "https://www.police.go.kr")

    # 공지 데이터 2: 주의
    with st.container():
        st.markdown(
            """
            <div style='background-color: #FFFBEB; border-left: 5px solid #F59E0B; padding: 20px; border-radius: 12px; margin-bottom: 20px;'>
                <span style='background-color: #F59E0B; color: white; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: bold;'>WARNING</span>
                <h4 style='color: #92400E; margin-top: 10px;'>명절 전후 '택배 주소지 불분명' 스캠 기승</h4>
                <p style='color: #78350F; font-size: 14px;'>택배사를 사칭하여 주소 수정을 유도하는 문자가 증가하고 있습니다.</p>
                <small style='color: #B45309;'>게시일: 2026-02-08 | 출처: 한국인터넷진흥원(KISA)</small>
            </div>
        """,
            unsafe_allow_html=True,
        )

    # 공지 데이터 3: 정보
    with st.container():
        st.markdown(
            """
            <div style='background-color: #F0F9FF; border-left: 5px solid #3B82F6; padding: 20px; border-radius: 12px; margin-bottom: 20px;'>
                <span style='background-color: #3B82F6; color: white; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: bold;'>INFO</span>
                <h4 style='color: #1E40AF; margin-top: 10px;'>Pol-Guard AI 엔진 버전 업데이트 안내 (v1.2)</h4>
                <p style='color: #1E3A8A; font-size: 14px;'>Llama 3.3 기반의 신규 보이스피싱 변조 음성 탐지 로직이 강화되었습니다.</p>
                <small style='color: #2563EB;'>게시일: 2026-02-05 | 내부 공지</small>
            </div>
        """,
            unsafe_allow_html=True,
        )

    # --- 3. 하단 캠페인 섹션 ---
    st.markdown("---")
    st.info(
        "💡 **Tip:** 의심스러운 문자를 받으셨다면 즉시 '🏠 Dashboard' 메뉴에서 AI 분석을 진행하세요."
    )
