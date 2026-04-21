import streamlit as st
import pandas as pd
import time

# --- 1. 페이지 기본 설정 ---
st.set_page_config(
    page_title="픽미! 아빠게임 101",
    page_icon="🎲",
    layout="centered"
)

# --- 2. CSS 스타일링 ---
st.set_option("client.toolbarMode", "viewer") 

st.markdown("""
<style>
    /* 🌓 라이트/다크 모드 컬러 변수 */
    :root {
        --app-bg: #FDF8F5; 
        --card-front-bg: #FFFFFF;
        --card-back-bg: #FFF4E6; 
        --text-main: #2C3E50;
        --text-title: #E25E3E; 
        --text-muted: #718096;
        --border-color: #FBD38D; 
        --tip-bg: #FFEBE0;
        --btn-text: #4A4A4A;
    }
    
    @media (prefers-color-scheme: dark) {
        :root {
            --app-bg: #262A33; 
            --card-front-bg: #323844;
            --card-back-bg: #2D323C;
            --text-main: #F7FAFC;
            --text-title: #FFB5A7; 
            --text-muted: #A0AEC0;
            --border-color: #4A5568;
            --tip-bg: #3E4553;
            --btn-text: #1A1A1A;
        }
    }

    /* 기본 배경 */
    .stApp { background-color: var(--app-bg) !important; }
    
    /* 앱 전체 컨테이너 모바일 최적화 */
    .block-container { 
        max-width: 360px !important; 
        padding-top: 1.5rem !important; 
        padding-bottom: 1rem !important; 
        margin: 0 auto !important;
    }
    
    /* 🚨 상단 Streamlit 헤더 및 지저분한 요소 완전 제거 */
    [data-testid="stHeader"], header, [data-testid="stHeaderActionElements"], .stAppDeployButton, #MainMenu, footer { 
        display: none !important; 
    }
    
    /* 🃏 포커 카드 & 애니메이션 카드 크기 완벽 고정 (커지는 현상 방지) */
    .poker-back, .flip-card {
        width: 320px !important; 
        height: 520px !important;
        margin: 0 auto !important; 
    }
    .poker-back {
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
    
    .flip-card { background-color: transparent; perspective: 1000px; cursor: pointer; display: block; }
    .flip-card-inner { position: relative; width: 100%; height: 100%; text-align: center; transition: transform 0.6s cubic-bezier(0.4, 0.2, 0.2, 1); transform-style: preserve-3d; }
    .flip-card input[type="checkbox"]:checked ~ .flip-card-inner { transform: rotateY(180deg); }
    
    .card-panel {
        position: absolute; width: 100%; height: 100%;
        -webkit-backface-visibility: hidden; backface-visibility: hidden;
        border-radius: 25px; padding: 30px 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border: 4px solid var(--border-color);
        display: flex; flex-direction: column;
    }
    .flip-card-front { background: var(--card-front-bg); align-items: center; justify-content: center; color: var(--text-main) !important; }
    .flip-card-back { background: var(--card-back-bg); transform: rotateY(180deg); text-align: left; overflow-y: auto; justify-content: flex-start; color: var(--text-main) !important; }

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
    
    /* 공통 버튼 스타일 */
    button[data-testid="baseButton-primary"], button[data-testid="baseButton-secondary"] {
        border-radius: 15px !important; 
        font-weight: 900 !important; 
        padding: 14px !important; 
        height: 55px !important;
        transition: all 0.3s ease !important;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    /* 🎲 메인 뽑기 버튼 (Primary) - 기존 파스텔 코랄 복구 */
    button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #FFD1BA 0%, #FFB5A7 100%) !important;
        color: #4A4A4A !important;
        border: none !important;
        font-size: 18px !important; 
        box-shadow: 0 4px 15px rgba(255, 181, 167, 0.4) !important;
    }
    button[data-testid="baseButton-primary"]:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(255, 181, 167, 0.6) !important; }
    
    /* ⚙️ 설정 & ✖️ 닫기 버튼 (Secondary) - 새로운 파스텔 민트/그린 */
    button[data-testid="baseButton-secondary"] {
        background: linear-gradient(135deg, #E2F0CB 0%, #B5EAD7 100%) !important;
        color: #4A4A4A !important;
        border: none !important;
        font-size: 18px !important; 
        box-shadow: 0 4px 15px rgba(181, 234, 215, 0.4) !important;
    }
    button[data-testid="baseButton-secondary"]:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(181, 234, 215, 0.6) !important; }
    
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

# --- 4. 세션 상태 (상태유지) ---
if 'show_settings' not in st.session_state: st.session_state.show_settings = False
if 'chk_기' not in st.session_state: st.session_state.chk_기 = True
if 'chk_걷' not in st.session_state: st.session_state.chk_걷 = True
if 'chk_뛰' not in st.session_state: st.session_state.chk_뛰 = True
if 'dad_stam' not in st.session_state: st.session_state.dad_stam = (1, 5)
if 'kid_stam' not in st.session_state: st.session_state.kid_stam = (1, 5)
if 'keyword' not in st.session_state: st.session_state.keyword = ""
if 'picked_card' not in st.session_state: st.session_state.picked_card = None
if 'trigger_shuffle' not in st.session_state: st.session_state.trigger_shuffle = False

# 공통 타이틀 (제목 복구)
st.markdown("<h1 style='text-align: center; color: var(--text-title); margin-bottom: 20px; font-size: 2.2em;'>👨‍👧 픽미! 아빠게임 101</h1>", unsafe_allow_html=True)

# ==========================================
# ⚙️ 설정 화면 (카드와 동일한 넓이로 출력)
# ==========================================
if st.session_state.show_settings:
    
    # 설정창 제목과 닫기 버튼 가로 정렬 (✖️ 아이콘 적용)
    col_title, col_close = st.columns([4, 1], gap="small")
    with col_title:
        st.markdown("<h3 style='color: var(--text-title); margin-top:5px;'>⚙️ 놀이 조건 설정</h3>", unsafe_allow_html=True)
    with col_close:
        if st.button("✖️", type="secondary", use_container_width=True):
            st.session_state.show_settings = False
            st.rerun()
            
    st.markdown("<hr style='border: 0; border-top: 2px dashed var(--border-color); margin: 10px 0 20px 0;'>", unsafe_allow_html=True)
    
    st.markdown("**1. 아이 발달 단계**")
    st.session_state.chk_기 = st.checkbox("👶 기는아이", value=st.session_state.chk_기)
    st.session_state.chk_걷 = st.checkbox("🧒 걷는아이", value=st.session_state.chk_걷)
    st.session_state.chk_뛰 = st.checkbox("🏃 뛰는아이", value=st.session_state.chk_뛰)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.session_state.dad_stam = st.slider("**2. 아빠 체력 범위**", 1, 5, st.session_state.dad_stam)
    st.session_state.kid_stam = st.slider("**3. 아이 소모 체력 범위**", 1, 5, st.session_state.kid_stam)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.session_state.keyword = st.text_input("**4. 준비물/상황 (선택사항)**", value=st.session_state.keyword, placeholder="예: 거실에서, 종이컵")

# ==========================================
# 🃏 메인 화면 (카드 & 하단 두 개의 버튼)
# ==========================================
else:
    main_area = st.empty()

    # 셔플 상태 로직
    if st.session_state.trigger_shuffle:
        st.session_state.trigger_shuffle = False
        
        if df.empty:
            main_area.error("데이터가 없습니다.")
        else:
            for _ in range(10): 
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
            
            stage_keywords = []
            if st.session_state.chk_기: stage_keywords.append("기는아이") 
            if st.session_state.chk_걷: stage_keywords.append("걷는아이")
            if st.session_state.chk_뛰: stage_keywords.append("뛰는아이")
            
            col_stage = '아이발달단계' if '아이발달단계' in df.columns else '아이구분'
            
            if stage_keywords:
                pattern = "|".join(stage_keywords)
                filtered_df = df[df[col_stage].astype(str).str.contains(pattern, na=False)]
            else:
                filtered_df = pd.DataFrame()
            
            if not filtered_df.empty and 'dad_score' in filtered_df.columns:
                dad_min, dad_max = st.session_state.dad_stam
                kid_min, kid_max = st.session_state.kid_stam
                filtered_df = filtered_df[
                    (filtered_df['dad_score'] >= dad_min) & (filtered_df['dad_score'] <= dad_max) &
                    (filtered_df['kid_score'] >= kid_min) & (filtered_df['kid_score'] <= kid_max)
                ]
            
            col_title_name = '카드' if '카드' in df.columns else '제목'
            kw = st.session_state.keyword.strip()
            if not filtered_df.empty and kw:
                filtered_df = filtered_df[
                    filtered_df[col_title_name].astype(str).str.contains(kw) | 
                    filtered_df['필요도구'].astype(str).str.contains(kw)
                ]
            
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
    <div style="font-size: 85px; margin: 0 auto;">🃏</div>
    </div>
    <h3 style="color: var(--text-muted); margin-top: 20px; font-size: 1.2em;">아래 버튼을 눌러 놀이를 뽑아주세요!</h3>
    </div>
    """, unsafe_allow_html=True)
        
    elif isinstance(st.session_state.picked_card, str) and st.session_state.picked_card == "empty":
        main_area.warning("⚠️ 조건에 맞는 놀이가 없어요. 우측 하단의 ⚙️ 설정창에서 조건을 변경해주세요!")
        
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

    # 🎯 하단 버튼 영역 (메인 버튼 + 설정 버튼)
    st.markdown("<br>", unsafe_allow_html=True)
    
    btn_col_main, btn_col_sub = st.columns([4, 1], gap="small") 
    
    with btn_col_main:
        btn_label = "🎲 Pick Me!" if st.session_state.picked_card is None else "🔄 다시 뽑기!"
        if st.button(btn_label, type="primary", use_container_width=True):
            st.session_state.trigger_shuffle = True
            st.rerun()
            
    with btn_col_sub:
        if st.button("⚙️", type="secondary", use_container_width=True):
            st.session_state.show_settings = True
            st.rerun()
