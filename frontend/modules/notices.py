import streamlit as st
import pandas as pd
from datetime import datetime


def show_notices():
    st.markdown("### 📡 실시간 보안 위협 인텔리전스 (KISA/경찰청 연동)")
    st.write(
        "외부 보안 전문 기관의 실시간 피드를 수집하여 최신 피싱 위협 정보를 제공합니다."
    )

    # --- 1. 실시간 데이터 수집 상태 표시 (시뮬레이션) ---
    with st.status("외부 데이터 동기화 중...", expanded=False) as status:
        st.write("KISA 보안 공지 서버 연결... ✅")
        st.write("경찰청 사이버수사국 보도자료 분석... ✅")
        st.write("최신 스미싱 키워드 DB 갱신... ✅")
        status.update(
            label="실시간 위협 정보 동기화 완료", state="complete", expanded=False
        )

    # --- 2. 검색 및 위험 등급 필터 ---
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input(
            "🔍 위협 키워드 검색", placeholder="예: 연말정산, 결제, 수사기관..."
        )
    with col2:
        filter_level = st.selectbox(
            "위험 등급", ["전체", "🚨 긴급", "⚠️ 주의", "ℹ️ 정보"]
        )

    st.markdown("---")

    # --- 3. 고도화된 보안 공지 데이터 (실제 데이터 형태 모사) ---
    notices_data = [
        {
            "level": "🚨 긴급",
            "title": "국세청 연말정산 환급금 사칭 스미싱 기승",
            "date": "2026-02-11",
            "source": "KISA 보안공지",
            "desc": "환급금 확인을 위해 특정 URL 클릭을 유도하며, 클릭 시 좀비폰 악성 앱이 설치됩니다.",
            "guide": "국세청 홈택스 공식 앱을 통해서만 환급 정보를 확인하세요.",
            "link": "https://www.boho.or.kr",
        },
        {
            "level": "⚠️ 주의",
            "title": "안드로이드 보안 업데이트 권고 (Zero-day 취약점)",
            "date": "2026-02-10",
            "source": "Android Security",
            "desc": "이미지 파일 실행만으로 기기 권한이 탈취되는 취약점이 발견되었습니다. 즉시 업데이트가 필요합니다.",
            "guide": "설정 > 소프트웨어 업데이트에서 최신 버전으로 갱신하세요.",
            "link": "https://source.android.com/security/bulletin",
        },
        {
            "level": "ℹ️ 정보",
            "title": "Pol-Guard AI 피싱 패턴 DB 정기 업데이트",
            "date": "2026-02-09",
            "source": "내부 공지",
            "desc": "변종 보이스피싱 스크립트 500여 건이 AI 학습 데이터에 추가되었습니다.",
            "guide": "최신 분석 정확도가 약 2.4% 향상되었습니다.",
            "link": "#",
        },
    ]

    # --- 4. Amara 스타일 리스트 렌더링 ---
    for note in notices_data:
        # 필터링 로직
        if filter_level != "전체" and note["level"] != filter_level:
            continue
        if search_query and search_query not in note["title"]:
            continue

        bg_color = (
            "#FEF2F2"
            if "긴급" in note["level"]
            else "#FFFBEB" if "주의" in note["level"] else "#F0F9FF"
        )
        border_color = (
            "#EF4444"
            if "긴급" in note["level"]
            else "#F59E0B" if "주의" in note["level"] else "#3B82F6"
        )
        text_color = (
            "#991B1B"
            if "긴급" in note["level"]
            else "#92400E" if "주의" in note["level"] else "#1E40AF"
        )

        st.markdown(
            f"""
            <div style='background-color: {bg_color}; border-left: 5px solid {border_color}; padding: 25px; border-radius: 16px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.02);'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <span style='background-color: {border_color}; color: white; padding: 4px 12px; border-radius: 8px; font-size: 12px; font-weight: 800;'>{note["level"]}</span>
                    <small style='color: #64748B;'>{note["date"]} | {note["source"]}</small>
                </div>
                <h4 style='color: {text_color}; margin: 15px 0 10px 0;'>{note["title"]}</h4>
                <p style='color: #334155; font-size: 14px; line-height: 1.6;'>{note["desc"]}</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

        with st.expander("🛡️ 피해 방지 행동 수칙"):
            st.info(note["guide"])
            if note["link"] != "#":
                st.link_button("🔗 원문 자료 확인하기", note["link"])

    # --- 5. 실시간 피싱 키워드 클라우드 (추가 고도화) ---
    st.markdown("---")
    st.subheader("🔥 실시간 급상승 피싱 키워드")
    st.write("현재 가장 많이 수집되는 피싱 문자 내 키워드입니다.")

    keywords = [
        "#환급금",
        "#과태료",
        "#배송지오류",
        "#수사관사칭",
        "#대출심사",
        "#인증번호",
    ]
    cols = st.columns(len(keywords))
    for i, kw in enumerate(keywords):
        cols[i].markdown(
            f"<span style='background:#E2E8F0; padding:5px 10px; border-radius:20px; font-size:12px; font-weight:600;'>{kw}</span>",
            unsafe_allow_html=True,
        )
