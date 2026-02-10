import streamlit as st
import time


def show_academy():
    st.markdown("### 🎓 Pol-Academy: 지능형 보안 훈련소")
    st.write("최신 피싱 시나리오를 통해 당신의 디지털 방어력을 테스트하고 강화하세요.")

    # 1. 세션 상태 초기화
    if "quiz_step" not in st.session_state:
        st.session_state.quiz_step = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "show_exp" not in st.session_state:
        st.session_state.show_exp = False

    # 2. 상단 진행 상태 및 대시보드
    col_p, col_s = st.columns([3, 1])
    with col_p:
        progress = st.session_state.quiz_step / 4
        st.progress(progress, text=f"훈련 진행률: {int(progress*100)}%")
    with col_s:
        st.metric("현재 점수", f"{st.session_state.score * 25}점")

    st.markdown("---")

    # 3. 실전 훈련 시나리오 (제안서 기반)
    quizzes = [
        {
            "type": "📱 스미싱 사례",
            "case": "[국제발신] 해외인증번호 [9402] 발급. 본인 아닐 시 즉시 소비자 센터(02-123-4567) 신고 요망.",
            "is_phishing": True,
            "exp": "전형적인 '기관 사칭' 유도입니다. 공식 번호가 아닌 일반 유선전화로의 유도는 100% 피싱입니다.",
            "tag": "#기관사칭 #금전탈취",
        },
        {
            "type": "📦 배송 스캠",
            "case": "[우체국] 주소지 불분명으로 배송이 보류되었습니다. 아래 주소에서 수정 바랍니다: http://k-post.net/check",
            "is_phishing": True,
            "exp": "공식 도메인(.go.kr)이 아닌 주소는 절대 클릭하지 마세요. 악성 앱 설치의 주범입니다.",
            "tag": "#스미싱 #URL사기",
        },
        {
            "type": "✅ 공공 알림",
            "case": "[국민건강보험] 2026년 건강검진 대상자입니다. 상세 일정은 공식 홈페이지나 'The건강보험' 앱에서 확인하세요.",
            "is_phishing": False,
            "exp": "링크가 포함되지 않고 공식 앱 방문을 유도하는 방식은 안전한 알림의 전형입니다.",
            "tag": "#정부공지 #안전",
        },
        {
            "type": "💸 대출 스캠",
            "case": "(광고) [OO은행] 주형 님만을 위한 특별 저금리 대환 대출 안내. 한도 1.5억, 금리 연 2.1% 즉시 승인.",
            "is_phishing": True,
            "exp": "먼저 찾아오는 저금리 대출 광고는 99% 사기입니다. 은행은 문자로 대출 권유를 하지 않습니다.",
            "tag": "#대출사기 #개인정보취득",
        },
    ]

    # 4. 퀴즈 UI 렌더링 (Amara 스타일 적용)
    if st.session_state.quiz_step < len(quizzes):
        q = quizzes[st.session_state.quiz_step]

        # 훈련 카드
        st.markdown(
            f"""
            <div style='background-color: white; padding: 35px; border-radius: 24px; border: 1px solid #E2E8F0; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05); margin-bottom: 25px;'>
                <span style='background-color: #EFF6FF; color: #3B82F6; padding: 5px 12px; border-radius: 8px; font-size: 12px; font-weight: 700;'>{q['type']}</span>
                <p style='font-size: 20px; color: #1E293B; line-height: 1.6; font-weight: 500; margin-top: 20px;'>"{q['case']}"</p>
                <div style='margin-top: 15px;'>
                    <span style='color: #64748B; font-size: 13px;'>{q['tag']}</span>
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )

        # 사용자 선택 버튼
        c1, c2 = st.columns(2)
        if c1.button("🚨 이건 피싱이다", use_container_width=True, key="btn_phish"):
            check_answer(q, True)
        if c2.button(
            "✅ 정상적인 연락이다", use_container_width=True, key="btn_normal"
        ):
            check_answer(q, False)

        # 해설 노출 섹션
        if st.session_state.show_exp:
            st.markdown(
                f"""
                <div style='background-color: #F8FAFC; padding: 20px; border-radius: 16px; border-left: 4px solid #3B82F6; margin-top: 20px;'>
                    <p style='font-weight: 700; color: #1E293B; margin-bottom: 5px;'>🛡️ AI 보안 코치 해설</p>
                    <p style='color: #475569; font-size: 14px;'>{q['exp']}</p>
                </div>
            """,
                unsafe_allow_html=True,
            )
            if st.button("다음 훈련으로 이동 ➡️", use_container_width=True):
                st.session_state.quiz_step += 1
                st.session_state.show_exp = False
                st.rerun()
    else:
        display_finish_card()


def check_answer(q, user_choice):
    if user_choice == q["is_phishing"]:
        st.toast("✅ 정확한 판단입니다!", icon="🎉")
        st.session_state.score += 1
    else:
        st.toast("❌ 위험한 판단입니다. 해설을 확인하세요.", icon="⚠️")
    st.session_state.show_exp = True
    st.rerun()


def display_finish_card():
    score = st.session_state.score
    rank = (
        "🥇 보안 마스터"
        if score == 4
        else "🥈 보안 전문가" if score >= 2 else "🥉 보안 꿈나무"
    )

    st.markdown(
        f"""
        <div style='text-align: center; padding: 50px; background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%); border-radius: 30px; border: 2px solid #3B82F6;'>
            <h2 style='color: #1E40AF; margin-bottom: 10px;'>🎉 훈련 종료!</h2>
            <p style='color: #64748B; margin-bottom: 20px;'>주형 님의 보안 인지 능력을 분석한 결과입니다.</p>
            <div style='background: white; display: inline-block; padding: 20px 40px; border-radius: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);'>
                <h1 style='margin: 0; color: #2563EB;'>{rank}</h1>
                <p style='margin: 5px 0 0 0; color: #475569;'>최종 보안 점수: {score * 25}점</p>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    if st.button("🔄 처음부터 다시 훈련하기", use_container_width=True):
        st.session_state.quiz_step = 0
        st.session_state.score = 0
        st.session_state.show_exp = False
        st.rerun()
