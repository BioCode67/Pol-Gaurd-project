import streamlit as st
import time


def show_ai_agent():
    # 상단 헤더 문구
    st.markdown("### 🤖 피싱 대응 AI 에이전트 (Pol-Coach)")
    st.write("보이스피싱 전문 수사관 AI가 당신의 상황을 실시간으로 정밀 진단합니다.")

    # 1. 채팅 데이터 초기화 (사용자 및 AI 대화 기록 보존)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 2. 버튼 스타일 최적화 (연한 블루 톤 및 Amara 테마 적용)
    st.markdown(
        """
        <style>
        div.stButton > button {
            background: #EFF6FF !important; /* 연한 블루 배경 */
            color: #1E40AF !important;    /* 짙은 블루 텍스트 */
            border: 1px solid #DBEAFE !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            transition: 0.3s all !important;
        }
        div.stButton > button:hover {
            background: #DBEAFE !important;
            border-color: #BFDBFE !important;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # 3. 바로 물어보기 (긴급 상황 키워드 버튼)
    st.markdown("#### 💡 긴급 상황 키워드 진단")
    c1, c2, c3 = st.columns(3)
    if c1.button("📱 모르는 번호 미끼 문자"):
        process_message(
            "모르는 번호로 택배 주소지 확인 문자가 왔습니다. 링크가 포함되어 있어요."
        )
    if c2.button("📞 수사기관/검찰 사칭 전화"):
        process_message(
            "검찰 수사관이라며 제 명의가 도용되었다고, 자산 보호를 위해 돈을 보내라고 합니다."
        )
    if c3.button("💸 지인 사칭 송금 요구"):
        process_message(
            "친한 친구가 카톡으로 급하게 결제할 게 있다며 100만원만 빌려달라고 합니다."
        )

    st.markdown("---")

    # 4. 채팅 인터페이스 (사용자 대화 노출 및 AI 답변 표시)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 5. 사용자 채팅 입력창
    if prompt := st.chat_input("의심되는 상황을 상세히 말씀해 주세요..."):
        process_message(prompt)

    # 6. 디지털 증거 가디언 리포트 (한글 깨짐 없는 TXT 다운로드)
    if st.session_state.messages:
        st.markdown("---")
        st.subheader("📄 디지털 증거 가디언 리포트")
        st.write("상담 내용을 기반으로 경찰 신고용 증거 리포트를 생성합니다.")

        report_data = generate_text_report(st.session_state.messages)

        st.download_button(
            label="📥 증거 리포트(.txt) 즉시 다운로드",
            data=report_data,
            file_name=f"PolGuard_Report_{time.strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True,
        )


def process_message(text):
    """사용자 질문을 먼저 저장하고 전문 수사관 답변을 생성합니다."""
    # 사용자 질문 저장 (리스트에 추가하여 대화창에 노출)
    st.session_state.messages.append({"role": "user", "content": text})

    # 전문 수사관 페르소나 답변 생성
    if "검찰" in text or "수사" in text or "명의" in text:
        full_response = (
            "🚨 **긴급 상황 알림: 경찰청 사이버수사팀입니다.**\n\n"
            "사용자님, 지금 당장 대화를 중단하십시오. 대한민국 수사기관은 절대 전화로 자산 보호를 명목으로 송금을 요구하지 않습니다.\n\n"
            "**전문 형사의 정밀 진단:**\n"
            "* **수법 분석:** 전형적인 '기관 사칭형' 보이스피싱입니다. 상대가 보낸 파일은 사용자님의 폰을 해킹하는 악성 앱일 확률이 100%입니다.\n"
            "* **긴급 조치:** 이미 앱을 설치했다면 비행기 모드로 전환 후, 다른 사람의 전화를 빌려 112에 신고하십시오.\n"
            "* **주의 사항:** 검찰은 절대 카카오톡이나 텔레그램으로 공문서를 보내지 않습니다."
        )
    elif "링크" in text or "문자" in text or "택배" in text:
        full_response = (
            "⚠️ **스미싱 탐지 보고: 지능형 AI 에이전트 분석 결과**\n\n"
            "방금 받으신 문자는 개인정보 탈취를 목적으로 한 '미끼 문자'입니다.\n\n"
            "**수사관 권고 사항:**\n"
            "* **핵심 위험:** 해당 URL은 실제 사이트와 똑같이 만들어진 가짜 페이지로 연결됩니다. 아이디와 비번을 입력하는 순간 금융 자산이 위험해집니다.\n"
            "* **대응 방법:** 링크를 절대 누르지 마시고 번호를 즉시 차단하십시오. 만약 클릭하셨다면 시중 은행에 연락해 '계좌 일괄 지급 정지'를 신청하세요.\n"
            "* **예방:** '메인 탐지기' 메뉴를 통해 해당 URL의 안전도를 한 번 더 검증하십시오."
        )
    else:
        full_response = (
            "안녕하십니까, 폴-가드 전담 수사관입니다. 말씀하신 사례를 분석해 보니 최근 기승을 부리는 변종 스캠 수법과 매우 유사합니다.\n\n"
            "**베테랑의 조언:**\n"
            "* **심리 분석:** 사기꾼들은 지금 사용자님을 심리적으로 압박하여 판단력을 흐리게 만들고 있습니다.\n"
            "* **확인 절차:** 아무리 급한 지인이라도 반드시 목소리를 직접 확인하기 전까지는 1원도 송금해서는 안 됩니다.\n"
            "* **다음 단계:** 이 상담 내역을 리포트로 저장하여 증거로 보관해 두십시오."
        )

    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.rerun()


def generate_text_report(messages):
    """상담 내역을 한글 깨짐 없는 텍스트 파일로 변환"""
    report = "=== Pol-Guard Digital Evidence Report ===\n"
    report += f"발행 일시: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += "피싱·스캠으로부터 안전한 나라, 경찰청과 Pol-Guard가 함께 만듭니다.\n"
    report += "------------------------------------------\n\n"

    for msg in messages:
        role = "사용자(USER)" if msg["role"] == "user" else "AI 수사관(AGENT)"
        # 마크다운 문법(**) 제거 후 텍스트 저장
        content = msg["content"].replace("**", "")
        report += f"[{role}]\n{content}\n\n"

    report += "------------------------------------------\n"
    report += "본 리포트는 Pol-Guard AI에 의해 생성된 상담 증거물입니다.\n"

    return report.encode("utf-8")  # UTF-8 인코딩으로 한글 깨짐 방지
