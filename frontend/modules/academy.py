import streamlit as st
import time


def show_academy():
    # 1. 스타일 정의 (카카오톡 UI 및 배지 시스템)
    st.markdown(
        """
        <style>
        .chat-container { background-color: #BACEE0; padding: 25px; border-radius: 20px; margin-bottom: 20px; display: flex; flex-direction: column; min-height: 300px; }
        .bubble { padding: 12px 18px; border-radius: 18px; margin-bottom: 12px; max-width: 85%; font-size: 15px; line-height: 1.5; position: relative; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .opponent { background-color: #FFFFFF; align-self: flex-start; border-top-left-radius: 2px; color: #000000; }
        .me { background-color: #FEE500; align-self: flex-end; border-top-right-radius: 2px; margin-left: auto; color: #3C1E1E; font-weight: 500; }
        .sender-name { font-size: 12px; color: #4E5968; margin-bottom: 4px; margin-left: 5px; }
        .badge-container { display: flex; align-items: center; background: white; padding: 12px 25px; border-radius: 50px; border: 2px solid #3B82F6; margin-bottom: 25px; }
        .badge-icon { font-size: 26px; margin-right: 12px; }
        .badge-text { font-weight: 800; color: #1E40AF; font-size: 16px; }
        </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🎓 Pol-Academy: 실전 대화형 보안 훈련소")

    # 세션 상태 초기화
    if "quiz_step" not in st.session_state:
        st.session_state.quiz_step = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "show_exp" not in st.session_state:
        st.session_state.show_exp = False
    if "user_reply" not in st.session_state:
        st.session_state.user_reply = ""
    if "is_correct" not in st.session_state:
        st.session_state.is_correct = False

    # 상단 배지 및 진행도
    score = st.session_state.score
    rank_info = {
        0: ("🌱", "보안 꿈나무"),
        1: ("🛡️", "보안 가디언"),
        2: ("🥈", "보안 전문가"),
        3: ("🥇", "보안 마스터"),
        4: ("👑", "전설의 가디언"),
    }
    badge_icon, rank_name = rank_info.get(score, ("👑", "전설의 가디언"))

    st.markdown(
        f'<div class="badge-container"><span class="badge-icon">{badge_icon}</span><div class="badge-text">등급: {rank_name} ({score}점)</div></div>',
        unsafe_allow_html=True,
    )

    progress = st.session_state.quiz_step / 4
    st.progress(progress, text=f"훈련 완수율: {int(progress*100)}%")

    # 퀴즈 데이터
    quizzes = [
        {
            "sender": "김철수 대리",
            "case": "대리님! 저 급하게 결제할 게 있는데 폰 액정이 깨져서 연락이 안 돼요. 50만원만 먼저 보내주시면 퇴근하고 바로 입금해 드릴게요. [계좌: 00은행 123...]",
            "is_phishing": True,
            "exp": "지인을 사칭한 긴급 금전 요구는 전형적인 메신저 피싱입니다. 반드시 유선 전화로 본인 확인을 거쳐야 합니다.",
            "tag": "#지인사칭 #금전요구",
        },
        {
            "sender": "우체국 알림톡",
            "case": "[우체국] 주소지 불분명으로 배송이 보류되었습니다. 아래 링크를 통해 주소지 확인 및 재배송 신청 바랍니다: http://k-post.net/check",
            "is_phishing": True,
            "exp": "공식 기관은 .net이나 .xyz 같은 생소한 도메인을 사용하지 않습니다. 클릭 시 악성 앱이 설치될 수 있습니다.",
            "tag": "#스미싱 #URL사기",
        },
        {
            "sender": "국민건강보험",
            "case": "2026년 건강검진 대상자 안내입니다. 상세 일정과 검진 기관은 공식 홈페이지나 'The건강보험' 앱에서 안전하게 확인하세요.",
            "is_phishing": False,
            "exp": "외부 링크가 없고 공식 사이트나 앱 방문을 직접 유도하는 메시지는 안전한 보안 공정입니다.",
            "tag": "#정부공지 #안전",
        },
        {
            "sender": "OO은행",
            "case": "(광고) 고객님만을 위한 특별 저금리 대환 대출 안내. 정부 지원 상품 선착순 한도 1.5억, 금리 연 2.1% 즉시 승인 가능합니다.",
            "is_phishing": True,
            "exp": "금융기관은 모바일 메시지로 먼저 대출 상담을 제안하거나 링크 클릭을 유도하지 않습니다.",
            "tag": "#대출스캠 #정부지원사칭",
        },
    ]
    if st.session_state.quiz_step < len(quizzes):
        q = quizzes[st.session_state.quiz_step]

        # 카톡 대화창 UI
        st.markdown(
            f"<div class='sender-name'>{q['sender']}</div>", unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="chat-container"><div class="bubble opponent">{q["case"]}</div>'
            + (
                f'<div class="bubble me">{st.session_state.user_reply}</div>'
                if st.session_state.show_exp
                else ""
            )
            + "</div>",
            unsafe_allow_html=True,
        )

        if not st.session_state.show_exp:
            c1, c2 = st.columns(2)
            if c1.button("🚨 이건 피싱이다", use_container_width=True):
                handle_choice(q, True, "⚠️ 수상한데요? 신고하고 차단하겠습니다.")
            if c2.button("✅ 정상 연락이다", use_container_width=True):
                handle_choice(q, False, "네, 알겠습니다! 확인해볼게요.")
        else:
            # 결과 피드백
            if st.session_state.is_correct:
                st.success(f"🎯 정답입니다! {q['exp']}")
                if st.button("다음 훈련으로 이동 ➡️", use_container_width=True):
                    st.session_state.quiz_step += 1
                    st.session_state.show_exp = False
                    st.rerun()
            else:
                st.error(f"⚠️ 오답입니다! {q['exp']}")
                if st.button("다시 판단해보기 🔄", use_container_width=True):
                    st.session_state.show_exp = False
                    st.rerun()
    else:
        st.balloons()
        st.markdown(
            "<h2 style='text-align:center;'>👑 모든 훈련을 마쳤습니다!</h2>",
            unsafe_allow_html=True,
        )
        if st.button("처음부터 다시 하기"):
            st.session_state.quiz_step = 0
            st.session_state.score = 0
            st.rerun()


def handle_choice(q, user_choice, reply_text):
    st.session_state.user_reply = reply_text
    st.session_state.show_exp = True
    if user_choice == q["is_phishing"]:
        st.session_state.is_correct = True
        st.session_state.score += 1
    else:
        st.session_state.is_correct = False
    st.rerun()
