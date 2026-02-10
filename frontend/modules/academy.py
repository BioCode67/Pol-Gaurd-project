import streamlit as st
import time


def show_learning_resources():
    st.markdown("---")
    st.subheader("📚 유형별 피싱 예방 완벽 가이드")
    st.write("범죄자들의 최신 수법을 미리 알고 대처하면 피해를 99% 막을 수 있습니다.")

    # 1. 탭을 활용한 카테고리별 학습 자료
    l_tab1, l_tab2, l_tab3 = st.tabs(
        ["📱 스미싱(SMS)", "🎙️ 보이스피싱", "💬 메신저피싱"]
    )

    with l_tab1:
        st.markdown(
            """
            <div style='background-color: #F0F9FF; padding: 20px; border-radius: 15px; border-left: 5px solid #3B82F6;'>
                <h4 style='color: #1E40AF; margin-top: 0;'>🔗 스미싱(Smishing) 예방 수칙</h4>
                <p style='font-size: 14px; color: #1E3A8A;'>문자에 포함된 링크(URL)를 통해 악성 앱 설치를 유도하는 수법입니다.</p>
                <ul style='font-size: 13px; color: #334155;'>
                    <li><b>출처 불분명 링크 클릭 금지:</b> 택배, 과태료, 지인 부고 등을 사칭한 URL은 절대 누르지 마세요.</li>
                    <li><b>번호 변조 확인:</b> 공공기관은 010 번호로 문자를 보내지 않습니다.</li>
                    <li><b>백신 프로그램 설치:</b> 모바일 백신을 항상 최신 버전으로 유지하세요.</li>
                </ul>
            </div>
        """,
            unsafe_allow_html=True,
        )
        st.info(
            "💡 **가디언 팁:** 만약 링크를 클릭했다면 즉시 비행기 모드를 켜고 서비스 센터를 방문하세요."
        )

    with l_tab2:
        st.markdown(
            """
            <div style='background-color: #FEF2F2; padding: 20px; border-radius: 15px; border-left: 5px solid #EF4444;'>
                <h4 style='color: #991B1B; margin-top: 0;'>📞 보이스피싱(Voice Phishing) 대응법</h4>
                <p style='font-size: 14px; color: #7F1D1D;'>전화로 공공기관이나 금융기관을 사칭하여 금전을 요구합니다.</p>
                <ul style='font-size: 13px; color: #475569;'>
                    <li><b>수사기관 사칭 주의:</b> 검찰, 경찰은 절대 전화로 돈을 요구하거나 보안카드를 묻지 않습니다.</li>
                    <li><b>지급 정지 요청:</b> 피해 발생 시 즉시 은행 고객센터(112, 1332)에 연락하여 계좌를 동결하세요.</li>
                    <li><b>원격 제어 앱 금지:</b> 상대방이 시키는 대로 앱을 설치하는 행위는 절대 금물입니다.</li>
                </ul>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with l_tab3:
        st.markdown(
            """
            <div style='background-color: #FFFBEB; padding: 20px; border-radius: 15px; border-left: 5px solid #F59E0B;'>
                <h4 style='color: #92400E; margin-top: 0;'>👥 메신저피싱(Messenger Phishing) 확인법</h4>
                <p style='font-size: 14px; color: #78350F;'>카카오톡 등으로 지인을 사칭해 긴급하게 돈을 빌려달라고 합니다.</p>
                <ul style='font-size: 13px; color: #475569;'>
                    <li><b>유선 확인 필수:</b> 아무리 급하다 해도 반드시 본인과 직접 통화하여 사실을 확인하세요.</li>
                    <li><b>해외 로그인 차단:</b> 카카오톡 설정에서 타국가 로그인 제한 기능을 활성화하세요.</li>
                    <li><b>금전 요구 거절:</b> 계좌 번호를 먼저 보내며 입금을 재촉한다면 99% 피싱입니다.</li>
                </ul>
            </div>
        """,
            unsafe_allow_html=True,
        )

    # 2. 하단 행동 강령 카드 (Amara 스타일)
    st.markdown("#### 🚨 피해 발생 시 3대 핵심 행동 강령")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """<div style='background:#F8FAFC; padding:15px; border-radius:12px; border:1px solid #E2E8F0; text-align:center;'>
                    <b style='color:#1E40AF;'>1. 즉시 신고</b><br><small>112(경찰) 또는 1332(금감원)</small></div>""",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """<div style='background:#F8FAFC; padding:15px; border-radius:12px; border:1px solid #E2E8F0; text-align:center;'>
                    <b style='color:#1E40AF;'>2. 지급 정지</b><br><small>거래 은행에 즉시 연락</small></div>""",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """<div style='background:#F8FAFC; padding:15px; border-radius:12px; border:1px solid #E2E8F0; text-align:center;'>
                    <b style='color:#1E40AF;'>3. 증거 보존</b><br><small>메시지/통화내역 캡처</small></div>""",
            unsafe_allow_html=True,
        )


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
    show_learning_resources()


def handle_choice(q, user_choice, reply_text):
    st.session_state.user_reply = reply_text
    st.session_state.show_exp = True
    if user_choice == q["is_phishing"]:
        st.session_state.is_correct = True
        st.session_state.score += 1
    else:
        st.session_state.is_correct = False
    st.rerun()
