%%writefile app.py
import streamlit as st
import pandas as pd
import datetime
import os

# 1. 기본 설정 및 데이터 파일 경로
FILE_NAME = 'digital_car_log.csv'

# 차량 목록
VEHICLES = [
    "1톤 포터 (93머 0940)",
    "스파크 (337서 4139)",
    "그랜드스타렉스 (70루 0533)"
]

# 점검 항목 리스트
CHECK_ITEMS = [
    "엔진오일", "라디에터", "밧데리", "브레이크", 
    "펜벨트", "타이어", "전기설비", "각종게이지", "기타"
]

def load_data():
    if os.path.exists(FILE_NAME):
        return pd.read_csv(FILE_NAME)
    else:
        columns = [
            "날짜", "요일", "차량번호", "운전자", "동승자",
            "출발지", "출발시간", "경유지", "도착지", "도착시간",
            "주행거리(Km)", "누적주행거리(Km)", "업무내용",
            "주유량", "주유금액", "점검사항_특이점", "작성일시"
        ]
        return pd.DataFrame(columns=columns)

def save_data(df):
    df.to_csv(FILE_NAME, index=False)

# 앱 UI 레이아웃
st.set_page_config(page_title="차량운행일지", page_icon="🚐")
st.title("🚐 밀알희망일터 차량운행일지")

tab1, tab2 = st.tabs(["📝 운행일지 작성", "📊 운행 기록 조회"])

with tab1:
    st.subheader("오늘의 운행 정보를 입력해주세요")
    with st.form("log_form"):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("운행 일자", datetime.date.today())
            vehicle = st.selectbox("차량 선택", VEHICLES)
            driver = st.text_input("운전자 성명")
            passenger = st.text_input("동승자")
        with col2:
            purpose = st.text_input("용무 (업무내용)")
            start_point = st.text_input("출발지", value="작업장")
            start_time = st.time_input("출발 시간", datetime.time(9, 0))
            end_point = st.text_input("도착지")
            end_time = st.time_input("도착 시간", datetime.time(18, 0))

        st.markdown("---")
        st.write("🚗 **주행 및 주유 정보**")
        c1, c2, c3 = st.columns(3)
        distance = c1.number_input("금일 주행거리(Km)", min_value=0.0, step=0.1)
        total_distance = c2.number_input("현재 누적 주행거리(Km)", min_value=0.0, step=0.1)
        fuel_amount = c3.number_input("주유량(L)", min_value=0.0, step=0.1)
        
        st.markdown("---")
        st.write("🔧 **일일 점검 사항 (이상 있는 곳만 체크)**")
        check_results = []
        cols = st.columns(4)
        for i, item in enumerate(CHECK_ITEMS):
            with cols[i % 4]:
                if st.checkbox(item):
                    check_results.append(item)
        
        note = st.text_area("특이사항 및 정비내역", placeholder="내용 입력")
        submitted = st.form_submit_button("운행일지 등록하기", use_container_width=True)
        
        if submitted:
            if not driver:
                st.error("운전자 성명을 입력해주세요!")
            else:
                df = load_data()
                new_data = {
                    "날짜": date,
                    "요일": date.strftime("%A"),
                    "차량번호": vehicle,
                    "운전자": driver,
                    "동승자": passenger,
                    "출발지": start_point,
                    "출발시간": start_time,
                    "경유지": "",
                    "도착지": end_point,
                    "도착시간": end_time,
                    "주행거리(Km)": distance,
                    "누적주행거리(Km)": total_distance,
                    "업무내용": purpose,
                    "주유량": fuel_amount,
                    "주유금액": 0,
                    "점검사항_특이점": f"점검필요: {', '.join(check_results)} / {note}",
                    "작성일시": datetime.datetime.now()
                }
                df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
                save_data(df)
                st.success("저장되었습니다!")

with tab2:
    st.subheader("📂 축적된 데이터 확인")
    df = load_data()
    if not df.empty:
        st.dataframe(df.sort_values(by="날짜", ascending=False), use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 엑셀(CSV) 다운로드", csv, "운행일지.csv", "text/csv")
    else:
        st.info("데이터가 없습니다.")
