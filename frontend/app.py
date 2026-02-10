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

# 2. Amara 스타일 프리미엄 UI 스타일링 (아이콘 텍스트 오류 박멸 포함)
st.markdown(
    """
    <style>
    /* 폰트 로드: Pretendard */
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    /* 전체 배경 및 기본 텍스트 설정 */
    .stApp {
        background-color: #F8FAFC !important;
        color: #1E293B !important;
        font-family: 'Pretendard', sans-serif !important;
    }

    /* [🚨 중요] 'keyboard_double_arrow_right' 및 'arrow_drop_down' 텍스트 박멸 */
    /* 아이콘 폰트 로드 실패 시 나타나는 텍스트를 화면 밖으로 밀어내고 숨깁니다. */
    [data-testid="stSidebarNav"] span, 
    [data-testid="stSidebarNav"] div,
    [data-testid="stExpander"] svg + div,
    .st-emotion-cache-16idsys p,
    .st-emotion-cache-z5fcl4,
    .st-emotion-cache-1pxm88,
    .st-emotion-cache-6q9sum,
    span[data-testid="stHeaderActionElements"] {
        font-size: 0px !important;
        line-height: 0 !important;
        visibility: hidden !important;
        display: none !important;
        text-indent: -9999px !important;
    }

    /* 사이드바 메뉴 텍스트만 정상적으로 다시 살리기 */
    [data-testid="stSidebarNav"] ul li a span {
        font-size: 16px !important;
        visibility: visible !important;
        display: block !important;
        text-indent: 0px !important;
        color: #475569 !important;
        font-weight: 500 !important;
    }

    /* 사이드바 디자인: 화이트 배경 + 세밀한 경계선 */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    
    /* 카드(컨테이너) 디자인: Amara 특유의 소프트 쉐도우와 둥근 모서리 */
    div[data-testid="stVerticalBlock"] > div.stBlock, 
    .stTabs [data-baseweb="tab-panel"],
    div.stExpander,
    div[data-testid="element-container"] > div.stAlert {
        background-color: #FFFFFF !important;
        border: 1px solid #F1F5F9 !important;
        border-radius: 20px !important;
        padding: 2.5rem !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
        margin-bottom: 2rem !important;
    }

    /* 상단 배너 섹션 (Amara 스타일 헤더) */
    .hero-section {
        background-color: #FFFFFF;
        padding: 30px 40px;
        border-radius: 20px;
        border: 1px solid #E2E8F0;
        margin-bottom: 30px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .hero-text-group { text-align: left; }
    .hero-title { font-size: 24px; font-weight: 800; color: #0F172A; margin-bottom: 4px; }
    .hero-subtitle { font-size: 14px; color: #64748B; }
    .status-badge {
        background-color: #EFF6FF;
        color: #3B82F6;
        padding: 8px 16px;
        border-radius: 10px;
        font-weight: 600;
        font-size: 13px;
    }

    /* 버튼 디자인: Amara 전용 선명한 블루 */
    .stButton>button {
        background-color: #3B82F6 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        height: 3.5rem !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.2) !important;
    }
    .stButton>button:hover {
        background-color: #2563EB !important;
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.3) !important;
        transform: translateY(-1px);
    }

    /* 탭 메뉴 디자인 */
    .stTabs [data-baseweb="tab-list"] { gap: 15px !important; }
    .stTabs [data-baseweb="tab"] {
        height: 50px !important;
        color: #64748B !important;
        font-weight: 600 !important;
        font-size: 15px !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #3B82F6 !important;
        border-bottom: 3px solid #3B82F6 !important;
    }

    /* 입력창(Text Area) 보정 */
    .stTextArea textarea {
        background-color: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 14px !important;
        color: #1E293B !important;
    }

    /* 가시성 확보: 모든 헤더 텍스트 딥 네이비 강제 */
    h1, h2, h3, p, label { color: #0F172A !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. 사이드바 구성 (Amara 스타일 메뉴)
with st.sidebar:
    st.markdown(
        "<div style='padding: 20px 0;'><h2 style='color:#3B82F6; margin-bottom:0;'>🛡️ Pol-Guard</h2><p style='font-size:12px; color:#64748B;'>AI 피싱 대응 플랫폼</p></div>",
        unsafe_allow_html=True,
    )
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

# 4. 상단 섹션 배너 (Amara 스타일 레이아웃)
st.markdown(
    f"""
    <div class="hero-section">
        <div class="hero-text-group">
            <div class="hero-title">안녕하세요, 주형님 👋</div>
            <div class="hero-subtitle">실시간 지능형 분석 시스템이 작동 중입니다. ({menu[2:]})</div>
        </div>
        <div class="status-badge">
            AI Engine: Llama 3.3 Active
        </div>
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
