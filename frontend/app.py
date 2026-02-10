import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from modules.detector import show_detector
from modules.academy import show_academy
from modules.reports import show_reports
from modules.notices import show_notices

# 1. 페이지 설정 및 전문적인 테마 적용
st.set_page_config(
    page_title="Pol-Guard AI 피싱 대응 플랫폼", page_icon="🛡️", layout="wide"
)

st.markdown(
    """
    <style>
    /* 1. 전체 배경: 딥 다크 블루 그라데이션 */
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #0f172a, #020617);
        color: #f1f5f9;
    }

    /* 2. 사이드바: 반투명 유리 질감 */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* 3. 카드(컨테이너): 이미지와 같은 둥근 모서리와 은은한 글로우 효과 */
    div.stBlock, .stTabs [data-baseweb="tab-panel"] {
        background-color: rgba(30, 41, 59, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 24px !important;
        padding: 24px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }

    /* 4. 버튼: TECBE.AI의 밝은 블루 포인트 컬러 */
    .stButton>button {
        background: #38bdf8 !important;
        color: #0f172a !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        transition: all 0.3s ease;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.6);
        color: #ffffff !important;
    }

    /* 5. 텍스트 가시성 및 폰트 스타일 */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.02em;
        color: #f8fafc !important;
    }
    
    /* 6. 입력창 가독성 확보 */
    .stTextArea textarea {
        background-color: rgba(15, 23, 42, 0.8) !important;
        color: #38bdf8 !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 16px !important;
    }

    /* 7. 메트릭 강조 */
    [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        color: #38bdf8 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. 사이드바 메뉴 (더 깔끔하게 구성)
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=80)
    st.title("Pol-Guard")
    st.markdown("---")
    menu = st.radio(
        "서비스 메뉴",
        [
            "🏠 메인 탐지기",
            "🎓 Pol-Academy",
            "📋 탐지 리포트 보관함",
            "📢 최신 보안 공지",
        ],
        index=0,
    )
    st.markdown("---")
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
