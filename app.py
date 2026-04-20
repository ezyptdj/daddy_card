import streamlit as st
import pandas as pd
import time

# --- 1. 페이지 기본 설정 ---
st.set_page_config(
    page_title="픽미! 아빠게임 101",
    page_icon="🎲",
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- 2. CSS 스타일링 (모바일 최적화 및 헤더/푸터 박멸) ---
st.markdown("""
<style>
    .stApp { background-color: #F4F6F9; }
    
    /* 🚨 1. 상단/하단 모든 스트림릿 브랜딩 강제 삭제 및 클릭 방지 */
    header { visibility: hidden !important; height: 0 !important; min-height: 0 !important; }
    footer { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    #MainMenu { visibility: hidden !important; }
    /* 하단 Manage App 버튼 영역 강제 투명화 및 높이 삭제 */
    .viewerBadge_container__1QSob { display: none !important; }
    .stAppDeployButton { display: none !important; }

    /* 🚨 2. 모바일 상단 여백 및 타이틀 최적화 */
    /* 메인 컨테이너의 상단 여백(Padding)을 0으로 강제 조정 */
    .block-container { 
        padding-top: 0rem !important; 
        padding-bottom: 0rem !important;
        margin-top: -30px !important; /* 상단 빈 공간을 위로 바짝 올림 */
    }
    
    .main-title-text { 
        text-align: center; 
        color: #2C3E50; 
        font-size: 24px !important; /* 모바일에 맞춰 크기 축소 */
        font-weight: 900;
        margin-bottom: 5px !important;
        margin-top: 0px !important;
    }

    /* 포커 카드 뒷면 */
    .poker-back {
        width: 320px; /* 모바일 폭을 고려해 소폭 축소 */
        height: 480px;
        margin: 0 auto !important;
        border-radius: 25px;
        background-color: #E25E3E; 
        background-image: repeating-linear-gradient(45deg, rgba(255,255,255,0.1) 25%, transparent 25%, transparent 75%, rgba(255,255,255,0.1) 75%, rgba(255,255,255,0.1)), repeating-linear-gradient(45deg, rgba(255,255,255,0.1) 25%, transparent 25%, transparent 75%, rgba(255,255,255,0.1) 75%, rgba(255,255,255,0.1));
        background-position: 0 0, 20px 20px;
        background-size: 40px 40px;
        border: 10px solid white;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    /* 3D 카드 애니메이션 */
    .flip-card {
        background-color: transparent;
        width: 320px; 
        height: 480px;
        perspective: 1000px;
        margin: 0 auto !important;
        cursor: pointer;
        display: block;
    }
    .flip-card-inner {
        position: relative;
        width: 100%;
        height: 100%;
        transition: transform 0.6s cubic-bezier(0.4, 0.2, 0.2, 1);
        transform-style: preserve-3d;
    }
    .flip-card input[type="checkbox"]:checked ~ .flip-card-inner { transform: rotateY(180deg); }
    
    .card-panel {
        position: absolute;
        width: 100%;
        height: 100%;
        -webkit-backface-visibility: hidden;
        backface-visibility: hidden;
        border-radius: 25px;
        padding: 25px 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border: 4px solid white;
        display: flex;
        flex-direction: column;
    }
    
    .flip-card-front { background: white; align-items: center; justify-content: center; }
    .flip-card-back { background: #FFF9F2; transform: rotateY(180deg); text-align: left; overflow-y: auto; justify-content: flex-start; }

    .emoji-huge { font-size: 80px; margin: 10px auto; text-align: center; }
    .card-title-text { font-size: 24px; font-weight: 900; color: #2C3E50; margin-bottom: 15px; text-align: center; }
    .info-row { display: flex; justify-content: space-between; font-size: 15px; font-weight: bold; margin: 8px 0; color: #555; width: 100%; padding: 0 10px; }
    .stamina-stars { color: #FF9B50; letter-spacing: 1px; }
    
    /* 대기 상태 안내 문구 조절 */
    .waiting-text {
        color: #666;
        font-size: 15px !important;
        line-height: 1.5;
        margin-top: 20px;
        text-align: center;
        font-weight: 500;
    }

    /* 버튼 스타일 */
    div.stButton, div[data-testid="stButton"] {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
        margin-top: 5px;
    }
    div[data-testid="stButton"] > button { 
        width: 320px !important; 
        max-width: 320px !important;
        background: linear-gradient(135deg, #FFD1BA 0%, #FFB5A7 100%) !important;
        color: #4A4A4A !important;
        border: none !important;
        font-size: 20px !important; 
        font-weight: 900 !important; 
        padding: 14px !important; 
        border-radius: 15px !important; 
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
# ⬅️ 좌측 UI: 사이드바
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
# ➡️ 중앙 UI
# ==========================================
# 타이틀 (여백 최소화)
st.markdown("<div class='main-title-text'>👨‍👧 픽미! 아빠게임 101</div>", unsafe_allow_html=True)

main_area = st.empty()

# 셔플 로직
if st.session_state.trigger_shuffle:
    st.session_state.trigger_shuffle = False
    if not df.empty:
        for _ in range(12): 
            anim_html = """
<div style="text-align: center; width: 100%;">
<div class="poker-back anim-shake">
<div style="font-size: 80px; margin: 0 auto;">🃏</div>
</div>
<h3 style="color: #666; font-size: 15px; margin-top: 15px;">조건에 맞는 카드를 찾는 중...</h3>
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
            filtered_df = filtered_df[(filtered_df['dad_score'] >= dad_min) & (filtered_df['dad_score'] <= dad_max) & (filtered_df['kid_score'] >= kid_min) & (filtered_df['kid_score'] <= kid_max)]
        
        col_title_name = '카드' if '카드' in df.columns else '제목'
        if not filtered_df.empty and keyword.strip():
            filtered_df = filtered_df[filtered_df[col_title_name].astype(str).str.contains(keyword) | filtered_df['필요도구'].astype(str).str.contains(keyword)]
        
        if len(filtered_df) > 0:
            st.session_state.picked_card = filtered_df.sample(1).iloc[0].to_dict()
            st.rerun()
        else:
            st.session_state.picked_card = "empty"
            st.rerun()

# 화면 렌더링
if st.session_state.picked_card is None:
    main_area.markdown("""
<div style="text-align: center; width: 100%;">
<div class="poker-back">
<div style="font-size: 80px; margin: 0 auto;">🃏</div>
</div>
<div class="waiting-text">좌측(>>) 메뉴에서 조건을 맞추고<br>버튼을 눌러주세요!</div>
</div>
""", unsafe_allow_html=True)
    
elif isinstance(st.session_state.picked_card, str) and st.session_state.picked_card == "empty":
    main_area.warning("⚠️ 조건에 맞는 놀이가 없습니다.")
    
else:
    card = st.session_state.picked_card
    c_title = card.get('카드', card.get('제목', '이름 없는 놀이'))
    html_flip_card = f"""
<div style="text-align: center; width: 100%;">
<div style="color: #E25E3E; font-size: 16px; font-weight: 700; margin-bottom: 10px;">✨ 추천 놀이를 뽑았어요!</div>
<label class="flip-card">
<input type="checkbox" style="display: none;">
<div class="flip-card-inner">
<div class="card-panel flip-card-front">
<div class="stage-badge">{card.get('구분아이콘', '')} {card.get('아이발달단계', '')}</div>
<div class="emoji-huge">{card.get('카드아이콘', '🃏')}</div>
<div class="card-title-text">{c_title}</div>
<hr style="border: 0; border-top: 2px dashed #E2E8F0; margin: 15px 0; width: 100%;">
<div class="info-row"><span>{card.get('아빠아이콘', '👨')} 아빠 체력</span><span class="stamina-stars">{card.get('아빠체력', '')}</span></div>
<div class="info-row"><span>{card.get('아이아이콘', '👶')} 아이 체력</span><span class="stamina-stars">{card.get('아이체력', '')}</span></div>
<div class="flip-hint">👆 카드를 터치해서 뒷면 보기 🔄</div>
</div>
<div class="card-panel flip-card-back">
<div class="stage-badge">{card.get('구분아이콘', '')} {card.get('아이발달단계', '')}</div>
<h3 style="margin-top: 10px; color:#2C3E50; text-align:center;">{c_title}</h3>
<hr style="border: 0; border-top: 1px solid #E2E8F0; margin: 10px 0;">
<div class="back-section"><div class="back-title">🎒 필요 도구</div><div class="back-text">{card.get('필요도구', '')}</div></div>
<div class="back-section"><div class="back-title">📝 놀이 방법</div><div class="back-text">{card.get('놀이방법', '')}</div></div>
<div class="back-section"><div class="back-title">💡 아빠 꿀팁</div><div class="back-text" style="background:#FFF5EE; padding:12px; border-radius:12px;">{card.get('아빠꿀팁', '')}</div></div>
<div class="flip-hint">👆 다시 터치해서 앞면 보기 🔄</div>
</div>
</div>
</label>
</div>
"""
    main_area.markdown(html_flip_card, unsafe_allow_html=True)

# 버튼 (1:1:1 레이아웃 없이 중앙 배치)
col1, col2, col3 = st.columns([0.1, 1, 0.1])
with col2:
    btn_label = "🎲 Pick Me!" if st.session_state.picked_card is None else "🔄 다시 Pick Me!"
    if st.button(btn_label, type="primary", use_container_width=True):
        st.session_state.trigger_shuffle = True
        st.rerun()