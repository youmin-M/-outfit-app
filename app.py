import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="오늘 뭐 입지?", page_icon="👗", layout="centered")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("👗 오늘 뭐 입지?")
st.markdown("날씨와 옷장 정보를 입력하면 AI가 코디를 추천해드려요!")
st.divider()

st.subheader("🌤️ 오늘 날씨")
col1, col2 = st.columns(2)
with col1:
    temp = st.selectbox("온도", ["매우 추움 (0도 이하)", "추움 (0~10도)", "선선함 (10~17도)", "따뜻함 (17~23도)", "더움 (23~28도)", "매우 더움 (28도 이상)"])
with col2:
    weather = st.selectbox("날씨", ["맑음", "흐림", "비", "눈", "바람 강함"])

st.divider()

st.subheader("👚 옷장에 있는 옷")
col1, col2 = st.columns(2)
with col1:
    tops = st.multiselect("상의", ["반팔 티", "긴팔 티", "셔츠", "니트", "후드티", "맨투맨", "블라우스"])
    outer = st.multiselect("아우터", ["없음", "얇은 가디건", "재킷", "코트", "패딩", "트렌치코트", "바람막이"])
with col2:
    bottoms = st.multiselect("하의", ["청바지", "슬랙스", "면바지", "레깅스", "미니스커트", "롱스커트", "반바지"])
    shoes = st.multiselect("신발", ["운동화", "구두", "로퍼", "부츠", "슬리퍼", "샌들"])

st.divider()

st.subheader("📅 오늘 일정")
occasion = st.selectbox("어디 가세요?", ["출근 / 학교", "데이트", "친구 약속 (캐주얼)", "집에서 쉬기", "운동", "공식 행사 / 면접"])

extra = st.text_input("✏️ 추가 요청사항 (선택)", placeholder="예: 편한 게 좋아요, 미니멀한 스타일 선호해요")

st.divider()

if st.button("✨ 코디 추천받기", type="primary", use_container_width=True):
    if not tops and not bottoms:
        st.warning("상의 또는 하의를 최소 하나는 선택해주세요!")
    else:
        prompt = f"""오늘의 날씨와 옷장 정보를 바탕으로 코디를 추천해줘.

날씨: {temp}, {weather}
옷장:
- 상의: {', '.join(tops) if tops else '없음'}
- 하의: {', '.join(bottoms) if bottoms else '없음'}
- 아우터: {', '.join(outer) if outer else '없음'}
- 신발: {', '.join(shoes) if shoes else '없음'}
오늘 일정: {occasion}
추가 요청: {extra if extra else '없음'}

아래 형식으로 코디 2가지를 추천해줘:

✨ 추천 코디 1
- 상의:
- 하의:
- 아우터:
- 신발:
→ 이 코디의 포인트 한 줄

✨ 추천 코디 2
- 상의:
- 하의:
- 아우터:
- 신발:
→ 이 코디의 포인트 한 줄

💡 오늘 날씨 스타일 팁: (한 줄)

친근하고 자연스러운 말투로 짧게 써줘."""

        with st.spinner("코디 추천 중... 👗"):
            try:
                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(prompt)
                st.success("코디 추천 완료! 오늘도 멋진 하루 보내세요 😊")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"오류가 발생했어요: {str(e)}\nAPI 키를 확인해주세요.")

with st.expander("💬 사용 팁"):
    st.markdown("""
    - 옷장에 있는 옷을 **최대한 많이** 선택할수록 더 정확한 추천이 가능해요
    - 추가 요청사항에 스타일 취향을 적으면 더 맞춤화된 추천을 받을 수 있어요
    - **예시**: "밝은 색 선호", "레이어드 스타일 좋아함", "최대한 편하게"
    """)
