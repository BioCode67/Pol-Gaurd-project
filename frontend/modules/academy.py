import streamlit as st
import time


def show_academy():
    # 1. 스타일 정의 (카카오톡 UI 및 배지 시스템 CSS)
    st.markdown(
        """
        <style>
        .chat-container { background-color: #BACEE0; padding: 25px; border-radius: 20px; margin-bottom: 20px; display: flex; flex-direction: column; }
        .bubble { padding: 12px 18px; border-radius: 18px; margin-bottom: 12px; max-width: 85%; font-size: 15px; line-height: 1.5; position: relative; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .opponent { background-color: #FFFFFF; align-self: flex-start; border-top-left-radius: 2px; color: #000000; }
        .me { background-color: #FEE500; align-self: flex-end; border-top-right-radius: 2px; margin-left: auto; color: #3C1E1E; }
        .sender-name { font-size: 12px; color: #4E5968; margin-bottom: 4px; margin-left: 5px; }
        .badge-container { display: flex; align-items: center; background: white; padding: 12px 25px; border-radius: 50px; border: 2px solid #3B82F6; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(59, 130, 246, 0.1); }
        .badge-icon { font-size: 26px; margin-right: 12px; }
        .badge-text { font-weight: 800; color: #1E40AF; font-size: 16px; }
        </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🎓 Pol-Academy: 실전 대화형 보안 훈련소")
    st.write(
        "카카오톡 대화 시나리오를 통해 피싱 수법을 간파하고 전설의 보안 배지를 획득하세요."
    )

    # 2. 세션 상태 초기화 (주형 님 기존 로직 유지)
    if "quiz_step" not in st.session_state:
        st.session_state.quiz_step = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "show_exp" not in st.session_state:
        st.session_state.show_exp = False

    # 3. 상단 대시보드 및 실시간 배지 시스템
    score = st.session_state.score
    rank_info = {
        0: ("🌱", "보안 꿈나무"),
        1: ("🛡️", "보안 가디언"),
        2: ("🥈", "보안 전문가"),
        3: ("🥇", "보안 마스터"),
        4: ("👑", "전설의 가디언"),
    }
    badge_icon, rank_name = rank_info.get(score, ("👑", "전설의 가디언"))

    # 실시간 배지 UI
    st.markdown(
        f"""
        <div class="badge-container">
            <span class="badge-icon">{badge_icon}</span>
            <div class="badge-text">현재 보안 등급: {rank_name} <span style='color:#64748B; font-weight:400; font-size:13px; margin-left:10px;'>({score}/4 정답)</span></div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # 진척도 표시 (주형 님 기존 로직)
    progress = st.session_state.quiz_step / 4
    st.progress(progress, text=f"훈련 진행률: {int(progress*100)}%")

    st.markdown("---")

    # 4. 실전 훈련 시나리오 데이터
    quizzes = [
        {
            "sender": "김철수 대리 (지인사칭)",
            "case": "주형님! 저 급하게 결제할 게 있는데 폰이 고장나서요. 50만원만 먼저 보내주시면 저녁에 바로 드릴게요. [계좌번호: 00은행 123...]",
            "is_phishing": True,
            "exp": "지인을 사칭한 긴급 금전 요구는 전형적인 메신저 피싱입니다. 반드시 전화로 본인 확인을 거쳐야 합니다.",
            "tag": "#메신저피싱 #지인사칭",
        },
        {
            "sender": "우체국 알림톡 (스미싱)",
            "case": "[우체국] 주소지 불분명으로 배송이 보류되었습니다. 아래 주소에서 주소지 확인 및 재배송 신청 바랍니다: http://k-post.net/check",
            "is_phishing": True,
            "exp": "공식 기관은 절대 .net이나 .xyz 같은 생소한 도메인을 사용하지 않습니다. 클릭 시 악성 앱이 설치될 수 있습니다.",
            "tag": "#스미싱 #URL사기",
        },
        {
            "sender": "국민건강보험 (정상)",
            "case": "2026년 건강검진 대상자 안내입니다. 상세 일정과 검진 기관은 공식 홈페이지나 'The건강보험' 앱에서 확인하세요.",
            "is_phishing": False,
            "exp": "외부 링크가 없고 공식 사이트나 앱 방문을 직접 유도하는 메시지는 안전한 보안 공정입니다.",
            "tag": "#정부공지 #안전",
        },
        {
            "sender": "OO은행 장팀장 (대출사기)",
            "case": "(광고) [OO은행] 주형 님만을 위한 특별 저금리 대환 대출 안내. 한도 1.5억, 금리 연 2.1% 즉시 승인 가능합니다.",
            "is_phishing": True,
            "exp": "먼저 찾아오는 저금리 대출 유도는 사기일 가능성이 매우 높습니다. 금융기관은 문자로 대출 상담을 제안하지 않습니다.",
            "tag": "#대출스캠 #금전탈취",
        },
    ]

    # 5. 퀴즈 UI 렌더링 (카톡 대화형 UI)
    if st.session_state.quiz_step < len(quizzes):
        q = quizzes[st.session_state.quiz_step]

        # 카톡 대화창 UI
        st.markdown(
            f"<div class='sender-name'>{q['sender']}</div>", unsafe_allow_html=True
        )
        st.markdown(
            f"""
            <div class="chat-container">
                <div class="bubble opponent">{q['case']}</div>
                {f'<div class="bubble me">음... 이건 AI 분석이 필요한 상황 같네요!</div>' if st.session_state.show_exp else ''}
            </div>
        """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<p style='color:#64748B; font-size:12px; margin-bottom:20px;'>{q['tag']}</p>",
            unsafe_allow_html=True,
        )

        # 선택 버튼 (주형 님 버튼 구조 유지 및 디자인 최적화)
        if not st.session_state.show_exp:
            c1, c2 = st.columns(2)
            if c1.button("🚨 이건 피싱이다", use_container_width=True, key="btn_phish"):
                check_answer_logic(q, True)
            if c2.button(
                "✅ 정상적인 연락이다", use_container_width=True, key="btn_normal"
            ):
                check_answer_logic(q, False)
        else:
            # 해설 노출 (주형 님 기존 스타일 보강)
            st.markdown(
                f"""
                <div style='background-color: #F8FAFC; padding: 20px; border-radius: 16px; border-left: 4px solid #3B82F6; margin-top: 10px; margin-bottom:20px;'>
                    <p style='font-weight: 700; color: #1E293B; margin-bottom: 5px;'>🛡️ AI 보안 코치 정밀 진단</p>
                    <p style='color: #475569; font-size: 14px;'>{q['exp']}</p>
                </div>
            """,
                unsafe_allow_html=True,
            )
            if st.button("다음 대화 상황으로 이동 ➡️", use_container_width=True):
                st.session_state.quiz_step += 1
                st.session_state.show_exp = False
                st.rerun()
    else:
        display_finish_card_v2(score, rank_name, badge_icon)


def check_answer_logic(q, user_choice):
    if user_choice == q["is_phishing"]:
        st.toast("✅ 정확한 판단입니다! 보안 능력이 향상되었습니다.", icon="🎉")
        st.session_state.score += 1
    else:
        st.toast("❌ 위험한 판단입니다! 해설을 반드시 확인하세요.", icon="⚠️")
    st.session_state.show_exp = True
    st.rerun()


def display_finish_card_v2(score, rank_name, badge_icon):
    # 주형 님 기존 결과 카드에 배지 애니메이션 추가
    st.balloons()
    st.markdown(
        f"""
        <div style='text-align: center; padding: 50px; background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%); border-radius: 30px; border: 2px solid #3B82F6;'>
            <h2 style='color: #1E40AF; margin-bottom: 10px;'>🎉 보안 훈련 최종 완료!</h2>
            <p style='color: #475569; margin-bottom: 25px;'>주형 님의 보안 인지 능력을 분석한 결과입니다.</p>
            <div style='background: white; display: inline-block; padding: 30px 50px; border-radius: 25px; box-shadow: 0 10px 25px rgba(59, 130, 246, 0.2);'>
                <div style='font-size: 60px; margin-bottom: 10px;'>{badge_icon}</div>
                <h1 style='margin: 0; color: #2563EB; font-size: 28px;'>{rank_name}</h1>
                <p style='margin: 10px 0 0 0; color: #64748B; font-weight:600;'>최종 보안 점수: {score * 25}점</p>
            </div>
            <p style='margin-top: 25px; color: #1E40AF; font-size: 14px; font-weight:500;'>당신은 이제 디지털 세상의 든든한 가디언입니다!</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    if st.button("🔄 처음부터 다시 훈련하기 (점수 초기화)", use_container_width=True):
        st.session_state.quiz_step = 0
        st.session_state.score = 0
        st.session_state.show_exp = False
        st.rerun()
