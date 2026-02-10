import streamlit as st


def show_academy():
    if "quiz_step" not in st.session_state:
        st.session_state.quiz_step = 0
    if "score" not in st.session_state:
        st.session_state.score = 0

    quizzes = [
        {
            "case": "[국제발신] 해외인증번호 [9402] 발송.",
            "is_phishing": True,
            "exp": "전형적인 상담원 연결 유도 피싱입니다.",
        },
        {
            "case": "[경찰청] 과태료 고지서 확인: http://police-scam.net",
            "is_phishing": True,
            "exp": "공식 도메인이 아닌 .net 링크는 위험합니다.",
        },
        {
            "case": "[쿠팡] 배송이 완료되었습니다.",
            "is_phishing": False,
            "exp": "일반적인 알림 문자입니다.",
        },
    ]

    if st.session_state.quiz_step < len(quizzes):
        q = quizzes[st.session_state.quiz_step]
        st.info(
            f"**문제 {st.session_state.quiz_step + 1}:** 다음은 피싱일까요?\n\n> {q['case']}"
        )

        c1, c2 = st.columns(2)
        if c1.button("🚨 피싱이다"):
            if q["is_phishing"]:
                st.success("정답!")
                st.session_state.score += 1
            else:
                st.error("오답!")
            st.write(f"해설: {q['exp']}")
            st.button(
                "다음",
                on_click=lambda: setattr(
                    st.session_state, "quiz_step", st.session_state.quiz_step + 1
                ),
            )
        if c2.button("✅ 정상이다"):
            if not q["is_phishing"]:
                st.success("정답!")
                st.session_state.score += 1
            else:
                st.error("오답!")
            st.write(f"해설: {q['exp']}")
            st.button(
                "다음",
                on_click=lambda: setattr(
                    st.session_state, "quiz_step", st.session_state.quiz_step + 1
                ),
            )
    else:
        st.success(f"완료! 점수: {st.session_state.score}/{len(quizzes)}")
        if st.button("다시 하기"):
            st.session_state.quiz_step = 0
            st.session_state.score = 0
            st.rerun()
