import sys
import os
import streamlit as st

# 1. 경로 설정 및 모듈 임포트
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.detector import show_detector
from modules.academy import show_academy
from modules.reports import show_reports
from modules.notices import show_notices

# 2. 페이지 설정 (Amara 스타일의 넓은 레이아웃)
st.set_page_config(
    page_title="Pol-Guard AI 피싱 대응 플랫폼",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 3. 통합 프리미엄 UI 스타일링 (아이콘 텍스트 완벽 박멸 + Amara 테마)
st.markdown(
    """
    <style>
    /* 폰트 로드: Pretendard */
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    /* [🚨 중요] 시스템 아이콘 텍스트(keyboard_double_arrow_right 등) 박멸 */
    [data-testid="stHeader"]::before,
    [data-testid="stHeader"] > div,
    [data-testid="stSidebarNav"] span,
    [data-testid="stSidebarNav"] div:not([class*="st-key"]),
    .st-emotion-cache-16idsys p,
    .st-emotion-cache-z5fcl4,
    .st-emotion-cache-1pxm88,
    span[data-testid="stHeaderActionElements"],
    button[kind="header"] {
        display: none !important;
        visibility: hidden !important;
        font-size: 0px !important;
        text-indent: -9999px !important;
    }

    /* 전체 배경색: Amara 특유의 아주 연한 그레이 블루 */
    .stApp {
        background-color: #F8FAFC !important;
        color: #1E293B !important;
        font-family: 'Pretendard', -apple-system, sans-serif !important;
    }

    /* 사이드바 디자인: 화이트 배경 + 세련된 경계선 */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    
    /* 사이드바 메뉴 텍스트만 살리기 */
    [data-testid="stSidebarNav"] ul li a span {
        font-size: 15px !important;
        visibility: visible !important;
        display: block !important;
        text-indent: 0px !important;
        color: #64748B !important;
        font-weight: 500 !important;
        margin-left: 10px;
    }

    /* 카드(Card) 디자인: Amara 스타일의 소프트 쉐도우와 넓은 여백 */
    div[data-testid="stVerticalBlock"] > div.stBlock, 
    .stTabs [data-baseweb="tab-panel"],
    div.stExpander,
    div[data-testid="element-container"] > div.stAlert {
        background-color: #FFFFFF !important;
        border: 1px solid #F1F5F9 !important;
        border-radius: 24px !important;
        padding: 2.5rem !important; /* 여백 대폭 확대 */
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 2rem !important;
    }

    /* 상단 대시보드 배너 */
    .hero-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #FFFFFF;
        padding: 25px 40px;
        border-radius: 20px;
        border: 1px solid #E2E8F0;
        margin-bottom: 35px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .hero-title-main { font-size: 24px; font-weight: 800; color: #0F172A; }
    .hero-tag { 
        background-color: #DBEAFE; 
        color: #2563EB; 
        padding: 6px 14px; 
        border-radius: 8px; 
        font-size: 13px; 
        font-weight: 600; 
    }

    /* 버튼 디자인: Amara 스타일 선명한 블루 그라데이션 */
    .stButton>button {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        height: 3.8rem !important;
        width: 100% !important;
        transition: 0.3s all cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 20px rgba(37, 99, 235, 0.3) !important;
    }

    /* 탭 메뉴: 세련된 언더라인 */
    .stTabs [data-baseweb="tab-list"] { gap: 30px !important; }
    .stTabs [data-baseweb="tab"] {
        color: #94A3B8 !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        height: 60px !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #2563EB !important;
        border-bottom: 3px solid #2563EB !important;
    }

    /* 메트릭(숫자) 강조 */
    [data-testid="stMetricValue"] {
        color: #1E40AF !important;
        font-weight: 800 !important;
        font-size: 2.5rem !important;
    }
    
    /* 텍스트 가시성 */
    h1, h2, h3, p, label { color: #0F172A !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# 4. 사이드바 구성 (Amara 스타일 메뉴)
with st.sidebar:
    st.image("assets/logo.png", width=150)
    selected = option_menu(
        menu_title="Pol-Guard 센터",
        options=[
            "🤖 피싱 대응 AI 에이전트",  # 1순위: 에이전트
            "🔍 메인 탐지기",  # 2순위: 탐지기
            "📋 탐지 리포트 보관함",  # 3순위: 보관함
            "🎓 보안 훈련소",  # 4순위: 훈련소
            "📢 최신 보안 공지",  # 5순위: 공지
        ],
        icons=["robot", "search", "clipboard-data", "mortarboard", "megaphone"],
        menu_icon="shield-shaded",
        default_index=0,
    )
    st.markdown("---")
    st.caption("© 2026 Pol-Guard AI Project")

# 5. 상단 섹션 배너 (Amara 스타일 상단바)
st.markdown(
    f"""
    <div class="hero-container">
        <div>
            <span class="hero-title-main">Welcome back, 주형님 👋</span>
            <p style="color:#64748B; margin:5px 0 0 0; font-size:14px;">현재 {menu[2:]} 시스템이 최적화 상태로 가동 중입니다.</p>
        </div>
        <div class="hero-tag">
            Engine: Llama-3.3-70B Active
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# 6. 페이지 라우팅
if menu == "🏠 Dashboard":
    show_detector()
elif menu == "🎓 Academy":
    show_academy()
elif menu == "📋 Reports":
    show_reports()
elif menu == "📢 Notices":
    show_notices()
