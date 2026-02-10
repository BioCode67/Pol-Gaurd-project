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
    /* 1. 전체 배경색 (어두운 네이비 그레이) */
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
    }
    
    /* 2. 사이드바 스타일 (더 어둡게) */
    [data-testid="stSidebar"] {
        background-color: #010409;
        border-right: 1px solid #30363d;
    }
    
    /* 3. 카드형 컨테이너 (배경보다 약간 밝은 색으로 입체감 부여) */
    div.stBlock, div.stExpander, .stTabs [data-baseweb="tab-panel"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    /* 4. 텍스트 입력창 및 텍스트 영역 */
    .stTextArea textarea, .stTextInput input {
        background-color: #0d1117 !important;
        color: #e6edf3 !important;
        border: 1px solid #30363d !important;
    }
    
    /* 5. 탭 메뉴 디자인 */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        color: #8b949e;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #58a6ff;
        border-bottom-color: #58a6ff;
    }

    /* 6. 메트릭(숫자) 스타일 */
    [data-testid="stMetricValue"] {
        color: #58a6ff !important;
        font-weight: bold;
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
