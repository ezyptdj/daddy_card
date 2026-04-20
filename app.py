import streamlit as st
import pandas as pd
import time

# --- 1. 페이지 기본 설정 (중앙 집중 레이아웃 유지) ---
st.set_page_config(
    page_title="픽미! 아빠게임 101",
    page_icon="🎲",
    layout="centered", 
    initial_sidebar_state="collapsed" # 좌측 상단 > 버튼으로 열기
)

# --- 2. CSS 스타일링 (폰트/여백 축소 & 다크/라이트 모드 대응) ---
st.set_option("client.toolbarMode", "viewer") 

st.markdown("""
<style>
    /* 기본 배경 */
    .stApp { background-color: #F4F6F9; }
            
    /* 상단 여백 */
    .block-container { padding-top: 3rem !important; }
            
    footer { visibility: hidden !important; }
    /* 🌓 라이트/다크 모드 컬러 변수 설정 */
    :root {
        --card-front-bg: #FFFFFF;
        --card-back-bg: #FFF9F2;
        --text-main: #1A202C;
        --text-title: #2C3E50;
        --text-muted: #4A5568;
        --border-color: #E2E8F0;
        --tip-bg: #FFF0E5;
        --btn-text: #4A4A4A;
    }
    @media (prefers-color-scheme: dark) {
        :root {
            --card-front-bg: #2D3748;
            --card-back-bg: #1A202C;
            --text-main: #F7FAFC;
            --text-title: #E2E8F0;
            --text-muted: #A0AEC0;
            --border-color: #4A5568;
            --tip-bg: #2D3748;
            --btn-text: #1A1A1A;
        }
    }

    /* 🚨 상단 여백 한 줄로 축소 & 기본 배경색은 Streamlit 테마에 맡김 */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    
    /* 우측 상단 지저분한 아이콘 숨김 */
    [data-testid="stHeaderActionElements"] { display: none !important; }
    .stAppDeployButton { display: none !important; }
    #MainMenu { display: none !important; }
    footer { display: none !important; }
    
    /* 포커 카드 뒷면 */
    .poker-back {
        width: 340px; 
        height: 520px;
        margin: 0 auto !important;
        border-radius: 25px;
        background-color: #E25E3E; 
        background-image: repeating-linear-gradient(45deg, rgba(255,255,255,0.1) 25%, transparent 25%, transparent 75%, rgba(255,255,255,0.1) 75%, rgba(255,255,255,0.1)), repeating-linear-gradient(45deg, rgba(255,255,255,0.1) 25%, transparent 25%, transparent 75%, rgba(255,255,255,0.1) 75%, rgba(255,255,255,0.1));
        background-position: 0 0, 20px 20px;
        background-size: 40px 40px;
        border: 12px solid white;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    /* 3D 카드 애니메이션 */
    .flip-card {
        background-color: transparent;
        width: 340px; 
        height: 520px;
        perspective: 1000px;
        margin: 0 auto !important;
        cursor: pointer;
        display: block;
    }
    .flip-card-inner {
        position: relative;
        width: 100%;
        height: 100%;
        text-align: center;
        transition: transform 0.6s cubic-bezier(0.4, 0.2, 0.2, 1);
        transform-style: preserve-3d;
    }
    .flip-card input[type="checkbox"]:checked ~ .flip-card-inner { transform: rotateY(180deg); }
    
    /* 카드 앞면/뒷면 패널 */
    .card-panel {
        position: absolute;
        width: 100%;
        height: 100%;
        -webkit-backface-visibility: hidden;
        backface-visibility: hidden;
        border-radius: 25px;
        padding: 30px 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border: 4px solid var(--border-color);
        display: flex;
        flex-direction: column;
    }
    
    .flip-card-front { background: var(--card-front-bg); align-items: center; justify-content: center; color: var(--text-main) !important; }
    .flip-card-back { background: var(--card-back-bg); transform: rotateY(180deg); text-align: left; overflow-y: auto; justify-content: flex-start; color: var(--text-main) !important; }

    /* 📏 카드 내부 글자 및 UI (전체적으로 1단계 축소) */
    .emoji-huge { font-size: 85px; margin: 20px auto; text-align: center; }
    .title-text { font-size: 24px; font-weight: 900; color: var(--text-title); margin-bottom: 25px; word-break: keep-all; text-align: center; }
    .info-row { display: flex; justify-content: space-between; font-size: 15px; font-weight: bold; margin: 10px 0; color: var(--text-muted); width: 100%; padding: 0 15px; }
    .stamina-stars { color: #FF9B50; letter-spacing: 2px; }
    .stage-badge { position: absolute; top: 15px; right: 15px; background: var(--tip-bg); padding: 5px 12px; border-radius: 15px; font-size: 12px; font-weight: bold; color: #E25E3E; }
    .flip-hint { margin-top: auto; font-size: 11px; color: var(--text-muted); font-weight: bold; animation: pulse 1.5s infinite; text-align: center; }
    
    .back-section { margin-bottom: 18px; width: 100%; }
    .back-title { font-size: 14px; font-weight: 900; color: #E25E3E; margin-bottom: 7px; }
    .back-text { font-size: 13.5px; color: var(--text-main); line-height: 1.6; word-break: keep-all; padding-left: 5px; }

    @keyframes shake { 0%, 100% { transform: rotate(0deg) scale(1); } 25% { transform: rotate(-8deg) scale(1.05); } 75% { transform: rotate(8deg) scale(1.05); } }
    .anim-shake { animation: shake 0.2s infinite; display: block; margin: 0 auto; }
    @keyframes pulse { 0%, 100% { opacity: 0.5; } 50% { opacity: 1; } }
    
    /* 폭주기관차 버튼 제압 */
    div.stButton, div[data-testid="stButton"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        margin-top: 10px;
    }
    div[data-testid="stButton"] > button { 
        width: 340px !important;       
        min-width: 340px !important;
        max-width: 340px !important;
        margin: 0 auto !important;
        background: linear-gradient(135deg, #FFD1BA 0%, #FFB5A7 100%) !important;
        color: var(--btn-text) !important;
        border: none !important;
        font-size: 20px !important; /* 폰트 축소 */
        font-weight: 900 !important; 
        padding: 16px !important; 
        border-radius: 15px !important; 
        box-shadow: 0 4px 15px rgba(255, 181, 167, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stButton"] > button:hover { 
        transform: translateY(-2px) !important; 
        box-shadow: 0 6px 20px rgba(255, 181, 167, 0.6) !important; 
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 데이터 로드 ---
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("daddy_cards.xlsx")
        df = df.fillna("")
        df.columns = df.columns.str.replace(' ', '')
        
        if '아빠체력' in df.columns:
            df['dad_score'] = df['아빠체력'].astype(str).str.count('★').replace(0, 1).astype(int)
        if '아이체력' in df.columns:
            df['kid_score'] = df['아이체력'].astype(str).str.count('★').replace(0, 1).astype(int)
            
        return df
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
        return pd.DataFrame()

df = load_data()

if 'picked_card' not in st.session_state: st.session_state.picked_card = None
if 'trigger_shuffle' not in st.session_state: st.session_state.trigger_shuffle = False

# ==========================================
# ⬅️ 좌측 UI: 사이드바 (설정창)
# ==========================================
with st.sidebar:
    st.markdown("### ⚙️ 놀이 조건 설정")
    st.markdown("**1. 아이 발달 단계**")
    chk_기 = st.checkbox("👶 기는아이", value=True)
    chk_걷 = st.checkbox("🧒 걷는아이", value=True)
    chk_뛰 = st.checkbox("🏃 뛰는아이", value=True)
    
    stage_keywords = []
    if chk_기: stage_keywords.append("기는아이") 
    if chk_걷: stage_keywords.append("걷는아이")
    if chk_뛰: stage_keywords.append("뛰는아이")
    
    st.markdown("<br>", unsafe_allow_html=True)
    dad_stam_slider = st.slider("**2. 아빠 체력 범위**", 1, 5, (1, 5))
    kid_stam_slider = st.slider("**3. 아이 소모 체력 범위**", 1, 5, (1, 5))
    
    st.markdown("<br>", unsafe_allow_html=True)
    keyword = st.text_input("**4. 준비물/상황 (선택사항)**", placeholder="예: 거실에서, 종이컵")

# ==========================================
# ➡️ 중앙 UI 및 셔플 로직
# ==========================================
# 테마 감응형 타이틀 변수 적용
st.markdown("<h1 style='text-align: center; color: var(--text-title); margin-bottom: 20px; font-size: 2.2em;'>👨‍👧 픽미! 아빠게임 101</h1>", unsafe_allow_html=True)

main_area = st.empty()

# 셔플 상태 로직
if st.session_state.trigger_shuffle:
    st.session_state.trigger_shuffle = False
    
    if df.empty:
        main_area.error("데이터가 없습니다.")
    else:
        for _ in range(12): 
            anim_html = """
<div style="text-align: center; width: 100%;">
<div class="poker-back anim-shake">
<div style="font-size: 85px; margin: 0 auto;">🃏</div>
</div>
<h3 style="color: var(--text-muted); margin-top: 15px; font-size: 1.1em;">조건에 맞는 카드를 찾는 중...</h3>
</div>
"""
            main_area.markdown(anim_html, unsafe_allow_html=True)
            time.sleep(0.08)
        
        col_stage = '아이발달단계' if '아이발달단계' in df.columns else '아이구분'
        
        if stage_keywords:
            pattern = "|".join(stage_keywords)
            filtered_df = df[df[col_stage].astype(str).str.contains(pattern, na=False)]
        else:
            filtered_df = pd.DataFrame()
        
        if not filtered_df.empty and 'dad_score' in filtered_df.columns:
            dad_min, dad_max = dad_stam_slider
            kid_min, kid_max = kid_stam_slider
            filtered_df = filtered_df[
                (filtered_df['dad_score'] >= dad_min) & (filtered_df['dad_score'] <= dad_max) &
                (filtered_df['kid_score'] >= kid_min) & (filtered_df['kid_score'] <= kid_max)
            ]
        
        col_title_name = '카드' if '카드' in df.columns else '제목'
        if not filtered_df.empty and keyword.strip():
            filtered_df = filtered_df[
                filtered_df[col_title_name].astype(str).str.contains(keyword) | 
                filtered_df['필요도구'].astype(str).str.contains(keyword)
            ]
        
        if len(filtered_df) > 0:
            st.session_state.picked_card = filtered_df.sample(1).iloc[0].to_dict()
            st.rerun()
        else:
            st.session_state.picked_card = "empty"
            st.rerun()

# --- 화면 렌더링 ---
if st.session_state.picked_card is None:
    main_area.markdown("""
<div style="text-align: center; width: 100%;">
<div class="poker-back">
<div style="font-size: 85px; margin: 0 auto;">🃏</div>
</div>
<h3 style="color: var(--text-muted); margin-top: 20px; font-size: 1.2em;">좌측(>) 메뉴에서 조건을 맞추고 버튼을 눌러주세요!</h3>
</div>
""", unsafe_allow_html=True)
    
elif isinstance(st.session_state.picked_card, str) and st.session_state.picked_card == "empty":
    main_area.warning("⚠️ 선택하신 조건에 맞는 놀이가 없습니다. 좌측 설정창에서 범위를 넓히거나 키워드를 지워주세요!")
    
else:
    card = st.session_state.picked_card
    c_stage_icon = card.get('구분아이콘', '')
    c_stage = card.get('아이발달단계', card.get('아이구분', ''))
    c_icon = card.get('카드아이콘', card.get('아이콘', '🃏'))
    c_title = card.get('카드', card.get('제목', '이름 없는 놀이')) 
    c_dad_icon = card.get('아빠아이콘', '👨')
    c_dad_sta = card.get('아빠체력', '★★★')
    c_kid_icon = card.get('아이아이콘', '👶')
    c_kid_sta = card.get('아이체력', '★★★')
    c_tools = card.get('필요도구', '없음')
    c_method = card.get('놀이방법', '자유롭게 놀아주세요!')
    c_tip = card.get('아빠꿀팁', '아빠의 센스를 발휘해보세요!')
    
    html_flip_card = f"""
<div style="text-align: center; width: 100%;">
<h3 style="color: #E25E3E; margin-bottom: 20px; font-size: 1.2em;">✨ 추천 놀이를 뽑았어요!</h3>
<label class="flip-card">
<input type="checkbox" style="display: none;">
<div class="flip-card-inner">
<div class="card-panel flip-card-front">
<div class="stage-badge">{c_stage_icon} {c_stage}</div>
<div class="emoji-huge">{c_icon}</div>
<div class="title-text">{c_title}</div>
<hr style="border: 0; border-top: 2px dashed var(--border-color); margin: 20px 0; width: 100%;">
<div class="info-row">
<span>{c_dad_icon} 아빠 체력</span>
<span class="stamina-stars">{c_dad_sta}</span>
</div>
<div class="info-row">
<span>{c_kid_icon} 아이 체력</span>
<span class="stamina-stars">{c_kid_sta}</span>
</div>
<div class="flip-hint">👆 카드를 터치해서 뒷면 보기 🔄</div>
</div>
<div class="card-panel flip-card-back">
<div class="stage-badge">{c_stage_icon} {c_stage}</div>
<h3 style="margin-top: 10px; color:var(--text-title); font-size: 1.1em;">{c_icon} {c_title}</h3>
<hr style="border: 0; border-top: 1px solid var(--border-color); margin: 15px 0;">
<div class="back-section">
<div class="back-title">🎒 필요 도구</div>
<div class="back-text">{c_tools}</div>
</div>
<div class="back-section">
<div class="back-title">📝 놀이 방법</div>
<div class="back-text">{c_method}</div>
</div>
<div class="back-section">
<div class="back-title">💡 아빠 꿀팁</div>
<div class="back-text" style="background:var(--tip-bg); padding:15px; border-radius:12px;">{c_tip}</div>
</div>
<div class="flip-hint">👆 다시 터치해서 앞면 보기 🔄</div>
</div>
</div>
</label>
</div>
"""
    main_area.markdown(html_flip_card, unsafe_allow_html=True)

# ==========================================
# ➡️ 무조건 정중앙에 꽂히는 2중 잠금 버튼 레이아웃
# ==========================================
col1, col2, col3 = st.columns([1, 1.4, 1])

with col2:
    btn_label = "🎲 Pick Me!" if st.session_state.picked_card is None else "🔄 다시 Pick Me!"
    if st.button(btn_label, type="primary", use_container_width=True):
        st.session_state.trigger_shuffle = True
        st.rerun()