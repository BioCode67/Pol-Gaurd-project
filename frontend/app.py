import sys
import os
import streamlit as st

# 경로 설정
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.detector import show_detector
from modules.academy import show_academy
from modules.reports import show_reports
from modules.notices import show_notices

# 1. 페이지 설정
st.set_page_config(
    page_title="Pol-Guard AI 피싱 대응 플랫폼", page_icon="🛡️", layout="wide"
)

# 2. 통합 프리미엄 UI 스타일링 (Amara 스타일 + 아이콘 오류 완벽 박멸)
st.markdown(
    """
    <style>
    /* 폰트 로드 */
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    /* 전체 배경 및 텍스트 */
    .stApp {
        background-color: #F8FAFC !important;
        color: #1E293B !important;
        font-family: 'Pretendard', sans-serif !important;
    }

    /* [🚨 핵심] 아이콘 이름(텍스트) 노출 완벽 박멸 */
    [data-testid="stSidebarNav"] span, 
    [data-testid="stSidebarNav"] div,
    .st-emotion-cache-16idsys p,
    .st-emotion-cache-z5fcl4,
    .st-emotion-cache-1pxm88,
    span[data-testid="stHeaderActionElements"],
    div[class*="st-key-"] p {
        font-size: 0px !important;
        line-height: 0 !important;
        visibility: hidden !important;
        display: none !important;
        text-indent: -9999px !important;
    }

    /* 사이드바 메뉴 텍스트만 다시 살리기 */
    [data-testid="stSidebarNav"] ul li a span {
        font-size: 16px !important;
        visibility: visible !important;
        display: block !important;
        text-indent: 0px !important;
        color: #475569 !important;
        font-weight: 500 !important;
    }

    /* 사이드바 디자인 */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    
    /* 카드 디자인 (입체감 강화) */
    div[data-testid="stVerticalBlock"] > div.stBlock, 
    .stTabs [data-baseweb="tab-panel"],
    div.stExpander,
    div[data-testid="element-container"] > div.stAlert {
        background-color: #FFFFFF !important;
        border: 1px solid #F1F5F9 !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
        margin-bottom: 1.5rem !important;
    }

    /* 상단 배너 디자인 */
    .hero-section {
        background: linear-gradient(135deg, #002D5D 0%, #0056b3 100%);
        padding: 40px;
        border-radius: 24px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 25px rgba(0,45,93,0.2);
    }
    .hero-title { font-size: 32px; font-weight: 800; margin-bottom: 10px; }
    .hero-subtitle { font-size: 16px; opacity: 0.9; }

    /* 버튼 디자인 */
    .stButton>button {
        background: #3B82F6 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        height: 3.5rem !important;
        width: 100% !important;
        transition: 0.3s all ease !important;
    }
    .stButton>button:hover {
        background: #2563EB !important;
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.4) !important;
        transform: translateY(-2px);
    }

    /* 탭 메뉴 */
    .stTabs [data-baseweb="tab-list"] { gap: 10px !important; }
    .stTabs [data-baseweb="tab"] {
        height: 50px !important;
        color: #64748B !important;
        font-weight: 600 !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #3B82F6 !important;
        border-bottom-color: #3B82F6 !important;
    }

    /* 가시성 확보: 모든 헤더 텍스트 검정색 강제 */
    h1, h2, h3, p, label { color: #0F172A !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. 사이드바 구성
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

# 4. 상단 섹션 배너
st.markdown(
    f"""
    <div class="hero-section">
        <div class="hero-title">🛡️ Pol-Guard AI</div>
        <div class="hero-subtitle">대한민국 경찰청 AI 기반 실시간 피싱 대응 플랫폼 - {menu[2:]}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# 5. 페이지 라우팅
if menu == "🏠 메인 탐지기":
    show_detector()
elif menu == "🎓 Pol-Academy":
    show_academy()
elif menu == "📋 탐지 리포트 보관함":
    show_reports()
elif menu == "📢 최신 보안 공지":
    show_notices()
