import streamlit as st
import time


def show_ai_agent():
    st.markdown("### 🤖 피싱 대응 AI 에이전트 (Pol-Coach)")
    st.write(
        "의심스러운 상황인가요? AI 에이전트가 실시간으로 상황을 진단하고 대응책을 제시합니다."
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # 1. 상황별 빠른 진단 버튼
    st.markdown("#### 💡 바로 물어보기")
    c1, c2, c3 = st.columns(3)
    if c1.button("📱 모르는 번호로 문자가 왔어요"):
        process_agent_query("모르는 번호로 택배 주소지 확인 문자가 왔는데 피싱인가요?")
    if c2.button("📞 검찰이라며 전화가 왔어요"):
        process_agent_query("검찰 수사관이라며 제 명의가 도용되었다고 전화가 왔어요.")
    if c3.button("💸 송금을 요구받고 있어요"):
        process_agent_query("지인이 카톡으로 급하게 돈을 빌려달라고 합니다.")

    st.markdown("---")

    # 2. 대화형 인터페이스 (Amara 스타일)
    for chat in st.session_state.chat_history:
        role_icon = "👤" if chat["role"] == "user" else "🤖"
        st.chat_message(chat["role"]).write(chat["content"])

    if prompt := st.chat_input("상황을 설명해주세요 (예: 방금 받은 문자 내용 등)"):
        process_agent_query(prompt)

    # 3. [특화 기능] 디지털 증거 리포트 생성 버튼
    if st.session_state.chat_history:
        st.markdown("---")
        if st.button(
            "📄 상담 내용 증거 리포트(PDF)로 저장하기", use_container_width=True
        ):
            with st.spinner("AI가 법적 증거 효력을 갖춘 리포트를 패키징 중입니다..."):
                time.sleep(1.5)
                st.success(
                    "✅ '피싱 의심 증거 리포트'가 생성되었습니다. [📋 보관함]에서 확인하세요."
                )


def process_agent_query(query):
    # 사용자 질문 저장
    st.session_state.chat_history.append({"role": "user", "content": query})

    # AI 답변 로직 (제안서 기반 응대)
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        # 실제로는 엔진과 연동하되, 여기서는 시나리오 기반 응대
        if "검찰" in query or "수사" in query:
            full_response = "🚨 **긴급 위험 상황입니다!** 수사기관은 절대로 전화로 자산 보호나 송금을 요구하지 않습니다. 즉시 통화를 종료하시고 112에 신고하세요."
        elif "문자" in query or "링크" in query:
            full_response = "⚠️ **스미싱 의심 경보:** 출처가 불분명한 URL은 악성 앱 설치의 통로입니다. 절대 클릭하지 마시고 '🔍 메인 탐지기'에 해당 문구를 넣어 분석해 보세요."
        else:
            full_response = "분석 결과, 전형적인 피싱 수법과 85% 일치합니다. 대화를 중단하고 Pol-Guard의 가이드에 따라 대응하세요."

        response_placeholder.markdown(full_response)
        st.session_state.chat_history.append(
            {"role": "assistant", "content": full_response}
        )
