import streamlit as st
import pandas as pd
import numpy as np

# 페이지 설정
st.set_page_config(
    page_title="간단한 데이터 앱",
    page_icon="📊",
    layout="wide"
)

# 제목
st.title("📊 간단한 데이터 분석 앱")
st.write("Streamlit과 Pandas를 사용한 기본 데이터 앱입니다!")

# 사이드바
st.sidebar.header("설정")
data_size = st.sidebar.slider("데이터 크기", 10, 1000, 100)
chart_type = st.sidebar.selectbox("차트 타입", ["line_chart", "bar_chart", "area_chart"])

# 샘플 데이터 생성
@st.cache_data
def generate_data(size):
    dates = pd.date_range('2023-01-01', periods=size, freq='D')
    data = {
        '날짜': dates,
        '판매량': np.random.randint(50, 200, size),
        '수익': np.random.randint(1000, 5000, size),
        '지역': np.random.choice(['서울', '부산', '대구', '인천'], size)
    }
    return pd.DataFrame(data)

# 데이터 생성
df = generate_data(data_size)

# 메인 컨텐츠를 두 개 컬럼으로 나누기
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 데이터 시각화")
    
    # 선택된 차트 타입으로 표시
    chart_data = df.set_index('날짜')[['판매량', '수익']]
    
    if chart_type == "line_chart":
        st.line_chart(chart_data)
    elif chart_type == "bar_chart":
        st.bar_chart(chart_data['판매량'])
    else:
        st.area_chart(chart_data)

with col2:
    st.subheader("📊 데이터 통계")
    
    # 기본 통계
    st.write("**기본 통계:**")
    st.dataframe(df.describe())
    
    # 지역별 평균
    st.write("**지역별 평균 판매량:**")
    region_avg = df.groupby('지역')['판매량'].mean().round(2)
    st.bar_chart(region_avg)

# 원본 데이터 표시
st.subheader("📋 원본 데이터")

# 필터링 옵션
selected_region = st.selectbox("지역 선택", ['전체'] + list(df['지역'].unique()))

if selected_region != '전체':
    filtered_df = df[df['지역'] == selected_region]
else:
    filtered_df = df

# 데이터 표시
st.dataframe(
    filtered_df.sort_values('날짜', ascending=False),
    use_container_width=True
)

# 요약 정보
st.subheader("📋 요약")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("총 데이터", len(filtered_df))
    
with col2:
    st.metric("평균 판매량", f"{filtered_df['판매량'].mean():.1f}")
    
with col3:
    st.metric("평균 수익", f"{filtered_df['수익'].mean():,.0f}원")
    
with col4:
    st.metric("최고 판매일", filtered_df.loc[filtered_df['판매량'].idxmax(), '날짜'].strftime('%Y-%m-%d'))

# 파일 다운로드
st.subheader("💾 데이터 다운로드")
csv = filtered_df.to_csv(index=False, encoding='utf-8-sig')
st.download_button(
    label="CSV 다운로드 📥",
    data=csv,
    file_name='sales_data.csv',
    mime='text/csv'
)