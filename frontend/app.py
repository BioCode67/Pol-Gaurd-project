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
    /* 1. 전체 배경: 딥 네이비 그라데이션 및 텍스트 색상 강제 지정 */
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #0f172a, #020617) !important;
        color: #f1f5f9 !important;
    }

    /* 2. 글자 색상 통합 제어 (가장 중요) */
    h1, h2, h3, p, span, label, li, .stMarkdown {
        color: #f1f5f9 !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* 3. 사이드바: 반투명 유리 질감 */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    [data-testid="stSidebar"] * {
        color: #94a3b8 !important;
    }

    /* 4. 카드(컨테이너): 이미지와 같은 둥근 모서리와 은은한 글로우 효과 */
    div[data-testid="stVerticalBlock"] > div.stBlock, 
    .stTabs [data-baseweb="tab-panel"],
    div.stExpander {
        background-color: rgba(30, 41, 59, 0.4) !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        border-radius: 20px !important;
        padding: 25px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4) !important;
    }

    /* 5. 버튼: TECBE.AI의 밝은 블루 포인트 컬러 */
    .stButton>button {
        background: #0ea5e9 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        width: 100% !important;
        padding: 12px !important;
        transition: 0.3s ease all !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 20px rgba(14, 165, 233, 0.5);
        background: #38bdf8 !important;
    }

    /* 6. 입력창 (텍스트 에어리어) 스타일 */
    .stTextArea textarea {
        background-color: rgba(15, 23, 42, 0.8) !important;
        color: #e2e8f0 !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 12px !important;
    }

    /* 7. 탭 메뉴 가시성 확보 */
    .stTabs [data-baseweb="tab"] {
        color: #94a3b8 !important;
        font-weight: 600 !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #38bdf8 !important;
        border-bottom-color: #38bdf8 !important;
    }

    /* 8. 메트릭(숫자) 강조 */
    [data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-weight: 800 !important;
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
