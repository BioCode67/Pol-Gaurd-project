import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from modules.detector import show_detector
from modules.academy import show_academy
from modules.reports import show_reports
from modules.notices import show_notices

# 1. 페이지 설정
st.set_page_config(
    page_title="Pol-Guard | AI 피싱 통합 관제", layout="wide", page_icon="🛡️"
)

# 2. 전역 스타일링 (모든 페이지 공통 적용)
st.markdown(
    """
    <style>
    .stApp { background-color: #ffffff; }
    .hero-section {
        background: linear-gradient(135deg, #002244 0%, #004080 100%);
        padding: 50px 20px; border-radius: 20px; color: white; text-align: center; margin-bottom: 30px;
    }
    .hero-title { font-size: 2.8rem; font-weight: 800; }
    .hero-subtitle { font-size: 1.1rem; opacity: 0.9; }
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. 사이드바 내비게이션
with st.sidebar:
    st.image("https://www.police.go.kr/static/portal/img/common/logo.png", width=150)
    st.markdown("### **서비스 메뉴**")
    menu = st.selectbox(
        "이동할 기능을 선택하세요",
        [
            "🏠 메인 탐지기",
            "🎓 Pol-Academy",
            "📋 탐지 리포트 보관함",
            "📢 최신 보안 공지",
        ],
    )
    st.write("---")
    st.caption("© 2026 Pol-Guard Project")

# 4. 공통 배너 출력
st.markdown(
    f"""
    <div class="hero-section">
        <div class="hero-title">🛡️ Pol-Guard</div>
        <div class="hero-subtitle">대한민국 경찰청 AI 기반 실시간 피싱 대응 플랫폼 - {menu[2:]}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# 5. 메뉴별 페이지 로드
if menu == "🏠 메인 탐지기":
    show_detector()
elif menu == "🎓 Pol-Academy":
    show_academy()
elif menu == "📋 탐지 리포트 보관함":
    show_reports()
elif menu == "📢 최신 보안 공지":
    show_notices()
