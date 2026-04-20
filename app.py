import streamlit as st
import pandas as pd
import random

# 페이지 설정 (모바일 최적화 및 타이틀)
st.set_page_config(
    page_title="픽미! 아빠게임 101",
    page_icon="🎲",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 1. 스타일링 (CSS) ---
# 캡처화면의 UI 디자인을 그대로 구현하기 위한 커스텀 CSS입니다.
st.markdown("""
<style>
    /* 전체 배경색 및 폰트 설정 */
    .stApp {
        background-color: #F7F9FC;
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* 메인 컨테이너 스타일 */
    .main-container {
        max-width: 450px;
        margin: 0 auto;
        padding: 20px;
    }

    /* 타이틀 섹션 */
    .title-section {
        text-align: center;
        margin-bottom: 30px;
    }
    .title-emoji {
        font-size: 3rem;
        margin-bottom: 10px;
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #333;
        margin: 0;
    }
    .main-title .highlight {
        color: #FF9B50;
    }
    .sub-title {
        font-size: 1rem;
        color: #888;
        margin-top: 5px;
    }

    /* 섹션 타이틀 (숫자 아이콘 포함) */
    .section-header {
        display: flex;
        items-center;
        gap: 10px;
        margin-bottom: 15px;
        font-size: 1.1rem;
        font-weight: 700;
        color: #333;
    }
    .section-number {
        background-color: #FF9B50;
        color: white;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: flex;
        items-center;
        justify-content: center;
        font-size: 0.8rem;
    }

    /* Step 1: 연령 선택 버튼 스타일 (Streamlit Radio 커스텀) */
    div[data-testid="stRadio"] > div {
        display: flex;
        gap: 10px;
        justify-content: space-between;
    }
    div[data-testid="stRadio"] label {
        flex: 1;
        background-color: white;
        border: 2px solid #EEE;
        border-radius: 12px;
        padding: 15px 10px;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s;
        font-weight: 500;
        color: #555;
    }
    /* 선택된 상태 */
    div[data-testid="stRadio"] label[data-selected="true"] {
        border-color: #FF9B50;
        background-color: #FFF5EE;
        color: #FF9B50;
        font-weight: 700;
    }
    /* 라디오 버튼 자체 숨기기 */
    div[data-testid="stRadio"] input[type="radio"] {
        display: none;
    }

    /* Step 2: 체력 설정 섹션 박스 */
    .stamina-box {
        background-color: #F2F5F9;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 25px;
    }
    .stamina-row {
        margin-bottom: 15px;
    }
    .stamina-header {
        display: flex;
        justify-content: space-between;
        items-center;
        margin-bottom: 5px;
    }
    .stamina-label {
        font-size: 0.9rem;
        font-weight: 500;
        color: #666;
    }
    .stamina-stars {
        color: #FF9B50;
        font-weight: 700;
    }

    /* Step 3: 키워드 입력창 스타일 */
    .stTextArea textarea {
        background-color: #F7F9FC;
        border-radius: 12px;
        border: 1px solid #EEE;
        padding: 15px;
    }

    /* 메인 액션 버튼 (오늘 뭐 하고 놀까?) */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #FF9B50 0%, #E25E3E 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 18px;
        font-size: 1.3rem;
        font-weight: 700;
        box-shadow: 0 4px 10px rgba(226, 94, 62, 0.3);
        transition: all 0.2s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(226, 94, 62, 0.4);
    }
    .stButton > button:active {
        transform: translateY(0);
    }

    /* --- 결과 화면 (카드) 스타일 --- */
    .result-header {
        text-align: center;
        margin-bottom: 20px;
    }
    .result-badge {
        background-color: #FFF5EE;
        color: #E25E3E;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 1px;
    }
    .result-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin-top: 10px;
        color: #333;
    }
    .result-title .sparkle { color: #FF9B50; }

    /* 카드 컨테이너 */
    .card-container {
        background-color: white;
        border-radius: 25px;
        padding: 30px 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        position: relative;
        margin-bottom: 20px;
        border: 4px solid white; /* 3D 효과용 */
    }

    /* 카드 상단 발달단계 배지 */
    .card-stage-badge {
        position: absolute;
        top: 15px;
        right: 15px;
        background-color: #F7F9FC;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.8rem;
        color: #666;
        display: flex;
        items-center;
        gap: 5px;
    }

    /* 카드 이모지 및 제목 */
    .card-emoji {
        font-size: 6rem;
        text-align: center;
        margin: 20px 0;
    }
    .card-play-title {
        font-size: 2rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 30px;
        color: #333;
    }

    /* 카드 하단 체력 정보 박스 */
    .card-info-box {
        background-color: #F7F9FC;
        border-radius: 15px;
        padding: 15px;
    }
    .card-info-row {
        display: flex;
        justify-content: space-between;
        items-center;
        margin-bottom: 8px;
    }
    .card-info-label {
        font-size: 0.9rem;
        color: #666;
        display: flex;
        items-center;
        gap: 5px;
    }
    .card-info-stars {
        color: #FF9B50;
    }
    .card-hint {
        text-align: center;
        font-size: 0.8rem;
        color: #AAA;
        margin-top: 10px;
    }

    /* 캡처화면 하단 버튼 (조건 변경) */
    .secondary-button > button {
        width: 100%;
        background-color: white;
        color: #666;
        border: 2px solid #EEE;
        border-radius: 15px;
        padding: 15px;
        font-weight: 700;
    }

</style>
""", unsafe_allow_html=True)

# --- 2. 데이터 로드 및 전처리 ---
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("daddy_cards.xlsx")
        # 데이터 정제 (★ 문자를 숫자로 변환하는 등의 전처리 필요 시 여기서 수행)
        # 예시데이터의 ★ 점수를 세어서 숫자로 변환 (실제 데이터 형식에 맞게 수정 필요)
        if '아빠체력' in df.columns:
            df['dad_score'] = df['아빠체력'].astype(str).str.count('★')
        if '아이체력' in df.columns:
            df['kid_score'] = df['아이체력'].astype(str).str.count('★')
        return df
    except FileNotFoundError:
        st.error("daddy_cards.xlsx 파일을 찾을 수 없습니다. GitHub에 올렸는지 확인해주세요.")
        return pd.DataFrame()

df = load_data()

# 세션 상태 초기화 (결국 셔플된 카드를 저장하기 위함)
if 'selected_card' not in st.session_state:
    st.session_state.selected_card = None

# --- 3. 화면 렌더링 로직 ---

st.markdown('<div class="main-container">', unsafe_allow_html=True)

# 결과 화면이 있다면 결과 화면을, 없다면 메인 화면을 보여줍니다.
if st.session_state.selected_card is None:
    
    # === [화면 1] 메인 (필터 및 검색) ===
    
    # 타이틀 세팅
    st.markdown(f"""
    <div class="title-section">
        <div class="title-emoji">👨‍👧</div>
        <h1 class="main-title">아빠카드 <span class="highlight">100선</span></h1>
        <p class="sub-title">우리아이 맞춤형 놀이 큐레이션</p>
    </div>
    """, unsafe_allow_html=True)

    # Step 1: 연령 선택
    st.markdown(f"""
    <div class="section-header">
        <div class="section-number">1</div>
        우리 아이는 지금?
    </div>
    """, unsafe_allow_html=True)
    # 라디오 버튼의 캡션을 이모지와 함께 구성하여 CSS로 스타일링
    stage = st.radio(
        "stage_select",
        ["👶 기기", "🧒 걷기", "🏃 뛰기"],
        horizontal=True,
        label_visibility="collapsed"
    )
    # 실제 데이터 필터링을 위해 이모지 제거
    clean_stage = stage.split(" ")[1]

    st.markdown("<br>", unsafe_allow_html=True) # 간격

    # Step 2: 체력 설정
    st.markdown(f"""
    <div class="section-header">
        <div class="section-number">2</div>
        오늘의 체력 설정
    </div>
    <div class="stamina-box">
    """, unsafe_allow_html=True)
    
    # Streamlit Slider 사용 및 CSS로 스타일 매칭
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<div class="stamina-label">아빠 체력 한계</div>', unsafe_allow_html=True)
        dad_stamina = st.slider("dad_slider", 1, 5, 3, label_visibility="collapsed")
    with col2:
        st.markdown(f'<div class="stamina-stars">{"⭐" * dad_stamina}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True) # 간격

    col3, col4 = st.columns([3, 1])
    with col3:
        st.markdown('<div class="stamina-label">아이 체력 소모</div>', unsafe_allow_html=True)
        kid_stamina = st.slider("kid_slider", 1, 5, 5, label_visibility="collapsed")
    with col4:
        st.markdown(f'<div class="stamina-stars">{"⭐" * kid_stamina}</div>', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True) # stamina-box 닫기

    # Step 3: 키워드 입력
    st.markdown(f"""
    <div class="section-header">
        <div class="section-number">3</div>
        준비물 또는 상황 입력
    </div>
    """, unsafe_allow_html=True)
    keyword = st.text_area("keyword_input", placeholder="예: 거실에 굴러다니는 종이컵, 힘 안드는 놀이", label_visibility="collapsed")

    st.markdown("<br><br>", unsafe_allow_html=True) # 간격

    # 셔플 버튼
    if st.button("🎲 오늘 뭐 하고 놀까?", use_container_width=True):
        # --- 셔플 로직 ---
        # 1. 기본적인 Hard Filter (발달단계)
        filtered_df = df[df['아이발달단계'].str.contains(clean_stage)]
        
        # 2. 체력 필터 (사용자 설정 값 이하/이상의 로직 적용 가능, 여기서는 MVP로 랜덤 선택)
        # TODO: 추후 RAG/Agent 도입 시 stamina 및 keyword 복합 분석 로직 추가
        
        if not filtered_df.empty:
            # 랜덤 한 개 선택
            selected = filtered_df.sample(n=1).iloc[0]
            st.session_state.selected_card = selected # 세션에 저장
            st.rerun() # 화면 새로고침하여 결과 화면 표시
        else:
            st.warning("조건에 맞는 놀이가 없어요. 조건을 변경해보세요!")

else:
    # === [화면 2] 결과 (카드 앞면 - Retrieval View) ===
    # 캡처화면의 '추천 놀이를 뽑았어요!' 화면 구현
    
    card = st.session_state.selected_card

    # 상단 뱃지 및 타이틀
    st.markdown(f"""
    <div class="result-header">
        <span class="result-badge">RESULT</span>
        <h1 class="result-title"><span class="sparkle">✨</span> 추천 놀이를 뽑았어요!</h1>
    </div>
    """, unsafe_allow_html=True)

    # --- 카드 컨테이너 (CSS Flip 효과는 추후 RAG 구현 시 뒷면과 함께 추가) ---
    st.markdown(f"""
    <div class="card-container">
        <div class="card-stage-badge">
            {card['구분아이콘']} {card['아이발달단계']}
        </div>
        
        <div class="card-emoji">{card['카드아이콘']}</div>
        <div class="card-play-title">{card['제목']}</div>
        
        <div class="card-info-box">
            <div class="card-info-row">
                <div class="card-info-label">
                    {card['아빠아이콘']} 아빠 체력
                </div>
                <div class="card-info-stars">
                    {card['아빠체력']}
                </div>
            </div>
            <div class="card-info-row">
                <div class="card-info-label">
                    {card['아이아이콘']} 아이 체력
                </div>
                <div class="card-info-stars">
                    {card['아이체력']}
                </div>
            </div>
        </div>
        
        <div class="card-hint">(카드를 터치하면 상세 가이드가 나옵니다 - 추후 RAG 구현)</div>
    </div>
    """, unsafe_allow_html=True)

    # 하단 버튼 액션
    if st.button("🎲 오늘 뭐 하고 놀까? (다시 뽑기)", use_container_width=True):
        # 다시 뽑기 로직 (메인화면의 셔플 로직과 동일, 세션 상태 업데이트)
        # TODO: 메모리 기능 도입 시 이전 카드 제외 로직 추가
        st.session_state.selected_card = None # 우선 메인으로 돌려서 다시 뽑게 함 (MVP)
        st.rerun()

    # 조건 변경 버튼 (메인화면으로 돌아가기)
    st.markdown('<div class="secondary-button">', unsafe_allow_html=True)
    if st.button("🏠 조건 다시 설정", use_container_width=True):
        st.session_state.selected_card = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) # main-container 닫기