import streamlit as st


def show_academy():
    st.markdown("### 🎓 Pol-Academy: 실전 보안 훈련소")
    st.write("실제 발생한 피싱 사례를 통해 대응 능력을 키워보세요.")

    if "quiz_step" not in st.session_state:
        st.session_state.quiz_step = 0
    if "score" not in st.session_state:
        st.session_state.score = 0

    # [🚀 고도화 3번] 등급 시스템 도입
    progress = st.session_state.quiz_step / 4  # 총 4문제 기준
    st.progress(progress, text=f"현재 보안 훈련 진행도: {int(progress*100)}%")

    quizzes = [
        {
            "case": "[국제발신] 해외인증번호 [9402] 발송. 본인 아닐 시 즉시 소비자 센터(02-123-4567) 신고 요망.",
            "is_phishing": True,
            "exp": "전형적인 '기관 사칭' 유도입니다. 공식 번호가 아닌 일반 유선전화 유도는 100% 피싱입니다.",
        },
        {
            "case": "[우체국] 주소지 불분명으로 배송이 보류되었습니다. 주소 수정: http://k-post.net/check",
            "is_phishing": True,
            "exp": "공식 도메인(.go.kr)이 아닌 주소는 클릭하지 마세요. 스미싱의 주된 수법입니다.",
        },
        {
            "case": "[국민건강보험] 건강검진 대상자입니다. 상세 내용은 공식 홈페이지에서 확인하세요.",
            "is_phishing": False,
            "exp": "링크가 없고 공식 사이트 방문을 유도하는 내용은 안전한 알림일 가능성이 높습니다.",
        },
        {
            "case": "(광고) [OO은행] 고객님께만 드리는 저금리 대환 대출 안내. 한도 1억원, 금리 2.5%",
            "is_phishing": True,
            "exp": "먼저 찾아오는 저금리 대출 광고는 대출 사기(스캠)의 전형적인 시작입니다.",
        },
    ]

    if st.session_state.quiz_step < len(quizzes):
        q = quizzes[st.session_state.quiz_step]

        st.markdown(
            f"""
        <div style='background:white; padding:30px; border-radius:20px; border:1px solid #E2E8F0; margin:20px 0;'>
            <h4 style='margin-top:0;'>💡 실전 퀴즈 {st.session_state.quiz_step + 1}</h4>
            <p style='font-size:18px; color:#1E293B; line-height:1.6;'>"{q['case']}"</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns(2)
        if c1.button("🚨 이건 피싱이다", use_container_width=True):
            process_answer(q, True)
        if c2.button("✅ 정상적인 연락이다", use_container_width=True):
            process_answer(q, False)
    else:
        finish_quiz()


def process_answer(q, user_choice):
    if user_choice == q["is_phishing"]:
        st.balloons()
        st.success("✅ 정답입니다! 정확한 판단입니다.")
        st.session_state.score += 1
    else:
        st.error(f"❌ 틀렸습니다. 다시 한번 확인해볼까요?")

    st.info(f"**해설:** {q['exp']}")
    st.button(
        "다음 문제로 넘어가기",
        on_click=lambda: setattr(
            st.session_state, "quiz_step", st.session_state.quiz_step + 1
        ),
    )


def finish_quiz():
    score = st.session_state.score
    rank = (
        "🥇 보안 마스터"
        if score == 4
        else "🥈 보안 전문가" if score >= 2 else "🥉 보안 꿈나무"
    )

    st.markdown(
        f"""
    <div style='text-align:center; padding:40px; background:#F0F9FF; border-radius:24px; border:2px solid #3B82F6;'>
        <h2>🎉 모든 훈련을 마쳤습니다!</h2>
        <h1 style='color:#2563EB;'>최종 등급: {rank}</h1>
        <p>당신의 보안 지수: {score}/4</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if st.button("처음부터 다시 하기"):
        st.session_state.quiz_step = 0
        st.session_state.score = 0
        st.rerun()
