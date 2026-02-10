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
    /* 1. 전체 배경: 깨끗하고 밝은 그레이 화이트 */
    .stApp {
        background-color: #F8FAFC !important;
        color: #1E293B !important;
    }

    /* 2. 사이드바: 화이트 배경에 은은한 경계선 */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    [data-testid="stSidebar"] * {
        color: #475569 !important;
    }

    /* 3. 카드 레이아웃: Amara 스타일의 둥근 모서리와 소프트 쉐도우 */
    div[data-testid="stVerticalBlock"] > div.stBlock, 
    .stTabs [data-baseweb="tab-panel"],
    div.stExpander {
        background-color: #FFFFFF !important;
        border: 1px solid #F1F5F9 !important;
        border-radius: 20px !important;
        padding: 30px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
        margin-bottom: 24px !important;
    }

    /* 4. 헤더 및 텍스트 색상 강제 지정 */
    h1, h2, h3, p, span, label {
        color: #0F172A !important;
        font-family: 'Pretendard', sans-serif !important;
    }

    /* 5. 버튼: Amara의 선명한 블루 포인트 컬러 */
    .stButton>button {
        background-color: #3B82F6 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        width: 100% !important;
        height: 3.5rem !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        background-color: #2563EB !important;
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.3) !important;
        transform: translateY(-1px);
    }

    /* 6. 입력창 (텍스트 에어리어) 디자인 */
    .stTextArea textarea {
        background-color: #F8FAFC !important;
        color: #1E293B !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }
    .stTextArea textarea:focus {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 1px #3B82F6 !important;
    }

    /* 7. 탭 메뉴: 세련된 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px !important;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px !important;
        background-color: transparent !important;
        border-radius: 10px 10px 0 0 !important;
        color: #64748B !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #3B82F6 !important;
        border-bottom: 2px solid #3B82F6 !important;
    }

    /* 8. 메트릭(숫자) 강조 */
    [data-testid="stMetricValue"] {
        color: #1E40AF !important;
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
