import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

# 저장될 파일 경로
REPORT_FILE = "data/reports.json"


def save_report(report_data):
    """분석 결과를 JSON 파일에 저장합니다."""
    # data 폴더가 없으면 생성
    if not os.path.exists("data"):
        os.makedirs("data")

    # 기존 데이터 로드
    reports = []
    if os.path.exists(REPORT_FILE):
        try:
            with open(REPORT_FILE, "r", encoding="utf-8") as f:
                reports = json.load(f)
        except:
            reports = []

    # 새 데이터 추가 (시간 정보 포함)
    report_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reports.insert(0, report_data)  # 최신순 정렬을 위해 앞에 추가

    # 파일 저장
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(reports, f, ensure_ascii=False, indent=4)


def show_reports():
    """저장된 리포트 목록을 보여주는 화면"""
    st.title("📂 탐지 리포트 보관함")
    st.write("그동안 분석했던 피싱 의심 사례들을 확인하고 관리하세요.")

    if not os.path.exists(REPORT_FILE):
        st.info("아직 저장된 리포트가 없습니다. 분석을 먼저 진행해 주세요!")
        return

    with open(REPORT_FILE, "r", encoding="utf-8") as f:
        reports = json.load(f)

    if not reports:
        st.info("저장된 리포트가 비어 있습니다.")
        return

    # 대시보드 요약
    df = pd.DataFrame(reports)
    c1, c2, c3 = st.columns(3)
    c1.metric("총 분석 건수", len(reports))
    c2.metric("평균 위험도", f"{int(df['risk_score'].mean())}%")
    c3.metric("최근 분석", reports[0]["timestamp"].split(" ")[0])

    st.markdown("---")

    # 개별 리포트 리스트
    for i, rep in enumerate(reports):
        with st.expander(
            f"[{rep['timestamp']}] {rep['intent']} - 위험도: {rep['risk_score']}%"
        ):
            st.write(f"**결과:** {rep['verdict']}")
            st.write(f"**분석 내용:** {rep['ai_analysis']}")
            if st.button(f"삭제하기", key=f"del_{i}"):
                reports.pop(i)
                with open(REPORT_FILE, "w", encoding="utf-8") as f:
                    json.dump(reports, f, ensure_ascii=False, indent=4)
                st.rerun()
