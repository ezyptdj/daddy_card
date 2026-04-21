import streamlit as st
import pandas as pd
import time

# --- 1. 페이지 기본 설정 ---
st.set_page_config(
    page_title="픽미! 아빠카드 101",
    page_icon="🎲",
    layout="centered"
)

# --- 2. CSS 스타일링 (절대 픽셀값 강제 고정 및 모바일 버그 완벽 차단) ---
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
    }
    
    @media (prefers-color-scheme: dark) {
        :root {
            --app-bg: #1A1C23; 
            --card-front-bg: #2D323C;
            --card-back-bg: #242831;
            --text-main: #ECEFF4;
            --text-title: #FFB5A7; 
            --text-muted: #9BA3AF;
            --border-color: #4A5568;
            --tip-bg: #3E4553;
        }
    }

    /* 기본 배경 */
    .stApp { background-color: var(--app-bg) !important; }
    
    /* 🚨 앱 전체 넓이를 320px로 무조건 잠금! (카드 넓이와 100% 동일) */
    .block-container { 
        width: 320px !important; 
        min-width: 320px !important;
        max-width: 320px !important; 
        padding-left: 0 !important;
        padding-right: 0 !important;
        padding-top: 0.1rem !important; 
        padding-bottom: 1rem !important; 
        margin: 0 auto !important;
        overflow-x: hidden !important;
    }
    
    /* 헤더 제거 */
    [data-testid="stHeader"], header { display: none !important; }
    
    /* 📱 Streamlit의 가로 배열(Columns)을 픽셀 단위로 강제 통제 */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        width: 320px !important;
        gap: 10px !important; /* 버튼 사이 간격 딱 10px */
    }
    
    /* 왼쪽 컬럼 (제목 or 메인 뽑기 버튼) -> 무조건 255px */
    div[data-testid="column"]:nth-child(1) {
        width: 255px !important;
        min-width: 255px !important;
        max-width: 255px !important;
        flex: 0 0 255px !important;
        padding: 0 !important;
    }
    
    /* 오른쪽 컬럼 (설정 버튼 or 닫기 버튼) -> 무조건 55px (정사각형 만들기) */
    div[data-testid="column"]:nth-child(2) {
        width: 55px !important;
        min-width: 55px !important;
        max-width: 55px !important;
        flex: 0 0 55px !important;
        padding: 0 !important;
    }

    /* 🃏 카드 크기도 320px로 완벽 일치 */
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
    .anim-shake { animation: shake 0.2s infinite; margin: 0 auto; }
    @keyframes pulse { 0%, 100% { opacity: 0.5; } 50% { opacity: 1; } }
    
    /* 🎨 버튼 공통 디자인 (모바일 렌더링 오류 방지) */
    button {
        -webkit-appearance: none !important; 
        appearance: none !important;
        border-radius: 15px !important; 
        font-weight: 900 !important; 
        height: 55px !important;
        margin: 0 !important;
        padding: 0 !important;
        transition: all 0.3s ease !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        border: none !important;
    }
    
    /* 🎲 메인 뽑기 버튼 (Primary) -> 길이 255px 고정 */
    button[data-testid="baseButton-primary"] {
        width: 255px !important;
        background: linear-gradient(135deg, #FFD1BA 0%, #FFB5A7 100%) !important;
        background-color: #FFB5A7 !important; 
        color: #4A4A4A !important;
        font-size: 18px !important; 
        box-shadow: 0 4px 15px rgba(255, 181, 167, 0.4) !important;
    }
    
    /* ⚙️ 설정 & ✖️ 닫기 버튼 (Secondary) -> 가로 55px, 세로 55px 정사각형 고정! (단색 적용) */
    button[data-testid="baseButton-secondary"] {
        width: 55px !important;
        background-image: none !important; /* 그라데이션 제거 (모바일 하얗게 나오는 버그 원인) */
        background-color: #B5EAD7 !important; /* 무조건 칠해지는 단색 파스텔 민트 */
        color: #4A4A4A !important;
        font-size: 22px !important; /* 아이콘 크기 키움 */
        box-shadow: 0 4px 12px rgba(181, 234, 215, 0.5) !important;
    }
    
    /* 🌙 다크모드 버튼 색상 변경 (Secondary 버튼 단색 유지) */
    @media (prefers-color-scheme: dark) {
        button[data-testid="baseButton-primary"] {
            background: linear-gradient(135deg, #FFAAA5 0%, #FF8B94 100%) !important;
            background-color: #FF8B94 !important;
            color: #1A1A1A !important;
        }
        button[data-testid="baseButton-secondary"] {
            background-color: #A8E6CF !important; /* 다크모드용 단색 민트 */
            color: #1A1A1A !important;
        }
    }
    
    button:hover { transform: translateY(-2px) !important; filter: brightness(1.05); }
    
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

# --- 4. 세션 상태 ---
if 'show_settings' not in st.session_state: st.session_state.show_settings = False
if 'chk_기' not in st.session_state: st.session_state.chk_기 = True
if 'chk_걷' not in st.session_state: st.session_state.chk_걷 = True
if 'chk_뛰' not in st.session_state: st.session_state.chk_뛰 = True
if 'dad_stam' not in st.session_state: st.session_state.dad_stam = (1, 5)
if 'kid_stam' not in st.session_state: st.session_state.kid_stam = (1, 5)
if 'keyword' not in st.session_state: st.session_state.keyword = ""
if 'picked_card' not in st.session_state: st.session_state.picked_card = None
if 'trigger_shuffle' not in st.session_state: st.session_state.trigger_shuffle = False

# 공통 타이틀
st.markdown("<h1 style='text-align: center; color: var(--text-title); margin-bottom: 15px; font-size: 1.8em; white-space: nowrap;'>👨‍👧 픽미! 아빠카드 101</h1>", unsafe_allow_html=True)

# ==========================================
# ⚙️ 설정 화면
# ==========================================
if st.session_state.show_settings:
    # 255px(제목) + 55px(버튼) 조합
    col_t, col_c = st.columns([4, 1])
    with col_t:
        st.markdown("<h3 style='color: var(--text-title); margin-top:12px; margin-bottom:0;'>⚙️ 놀이 조건 설정</h3>", unsafe_allow_html=True)
    with col_c:
        if st.button("✖️", type="secondary", key="btn_close"):
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
# 🃏 메인 화면
# ==========================================
else:
    main_area = st.empty()

    if st.session_state.trigger_shuffle:
        st.session_state.trigger_shuffle = False
        if df.empty:
            main_area.error("데이터가 없습니다.")
        else:
            for _ in range(10): 
                # 텍스트 모두 지우고 애니메이션만 표시
                anim_html = '<div style="text-align: center; width: 100%;"><div class="poker-back anim-shake"><div style="font-size: 85px; margin: 0 auto;">🃏</div></div></div>'
                main_area.markdown(anim_html, unsafe_allow_html=True)
                time.sleep(0.08)
            
            stage_keywords = []
            if st.session_state.chk_기: stage_keywords.append("기는아이") 
            if st.session_state.chk_걷: stage_keywords.append("걷는아이")
            if st.session_state.chk_뛰: stage_keywords.append("뛰는아이")
            
            col_stage = '아이발달단계' if '아이발달단계' in df.columns else '아이구분'
            if stage_keywords:
                pattern = "|".join(stage_keywords)
                f_df = df[df[col_stage].astype(str).str.contains(pattern, na=False)]
            else:
                f_df = pd.DataFrame()
            
            if not f_df.empty:
                d_min, d_max = st.session_state.dad_stam
                k_min, k_max = st.session_state.kid_stam
                f_df = f_df[(f_df['dad_score'] >= d_min) & (f_df['dad_score'] <= d_max) & (f_df['kid_score'] >= k_min) & (f_df['kid_score'] <= k_max)]
            
            col_t_n = '카드' if '카드' in df.columns else '제목'
            kw = st.session_state.keyword.strip()
            if not f_df.empty and kw:
                f_df = f_df[f_df[col_t_n].astype(str).str.contains(kw) | f_df['필요도구'].astype(str).str.contains(kw)]
            
            if len(f_df) > 0:
                st.session_state.picked_card = f_df.sample(1).iloc[0].to_dict()
                st.rerun()
            else:
                st.session_state.picked_card = "empty"
                st.rerun()

    if st.session_state.picked_card is None:
        # 문구 없이 뒷면만 깔끔하게 표시
        main_area.markdown('<div style="text-align: center; width: 100%;"><div class="poker-back"><div style="font-size: 85px; margin: 0 auto;">🃏</div></div></div>', unsafe_allow_html=True)
    elif st.session_state.picked_card == "empty":
        main_area.warning("⚠️ 조건에 맞는 놀이가 없어요. ⚙️ 설정에서 조건을 변경해주세요!")
    else:
        c = st.session_state.picked_card
        html_card = f"""
        <div style="text-align: center; width: 100%;">
        <label class="flip-card">
        <input type="checkbox" style="display: none;">
        <div class="flip-card-inner">
        <div class="card-panel flip-card-front">
        <div class="stage-badge">{c.get('구분아이콘', '')} {c.get('아이발달단계', c.get('아이구분', ''))}</div>
        <div class="emoji-huge">{c.get('카드아이콘', c.get('아이콘', '🃏'))}</div>
        <div class="title-text">{c.get('카드', c.get('제목', '놀이'))}</div>
        <hr style="border: 0; border-top: 2px dashed var(--border-color); margin: 20px 0; width: 100%;">
        <div class="info-row"><span>{c.get('아빠아이콘', '👨')} 아빠 체력</span><span class="stamina-stars">{c.get('아빠체력', '★★★')}</span></div>
        <div class="info-row"><span>{c.get('아이아이콘', '👶')} 아이 체력</span><span class="stamina-stars">{c.get('아이체력', '★★★')}</span></div>
        <div class="flip-hint">👆 카드를 터치해서 뒷면 보기 🔄</div>
        </div>
        <div class="card-panel flip-card-back">
        <div class="stage-badge">{c.get('구분아이콘', '')} {c.get('아이발달단계', c.get('아이구분', ''))}</div>
        <h3 style="margin-top: 10px; color:var(--text-title); font-size: 1.1em;">{c.get('카드아이콘', '🃏')} {c.get('카드', '제목')}</h3>
        <hr style="border: 0; border-top: 1px solid var(--border-color); margin: 15px 0;">
        <div class="back-section"><div class="back-title">🎒 필요 도구</div><div class="back-text">{c.get('필요도구', '없음')}</div></div>
        <div class="back-section"><div class="back-title">📝 놀이 방법</div><div class="back-text">{c.get('놀이방법', '자유롭게 놀기')}</div></div>
        <div class="back-section"><div class="back-title">💡 아빠 꿀팁</div><div class="back-text" style="background:var(--tip-bg); padding:15px; border-radius:12px;">{c.get('아빠꿀팁', '센스 발휘!')}</div></div>
        <div class="flip-hint">👆 다시 터치해서 앞면 보기 🔄</div>
        </div>
        </div>
        </label>
        </div>
        """
        main_area.markdown(html_card, unsafe_allow_html=True)

    # 🎯 하단 버튼 영역 (255px + 55px = 320px 완벽 조립)
    st.markdown("<br>", unsafe_allow_html=True)
    b_main, b_sub = st.columns([4, 1]) 
    with b_main:
        lbl = "🎲 Pick Me!" if st.session_state.picked_card is None else "🔄 다시 뽑기!"
        if st.button(lbl, type="primary", key="btn_main"):
            st.session_state.trigger_shuffle = True
            st.rerun()
    with b_sub:
        if st.button("⚙️", type="secondary", key="btn_setting"):
            st.session_state.show_settings = True
            st.rerun()
