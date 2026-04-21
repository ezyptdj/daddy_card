import streamlit as st
import pandas as pd
import time

# --- 1. 페이지 기본 설정 ---
st.set_page_config(
    page_title="픽미! 아빠카드 101",
    page_icon="🎲",
    layout="centered"
)

# --- 2. CSS 스타일링 (무적의 레이아웃 & 카드 내장형 타이틀) ---
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
    
    /* 🚨 앱 전체 컨테이너 넓이 잠금 */
    .block-container { 
        width: 100% !important;
        max-width: 360px !important; 
        padding-left: 0 !important;
        padding-right: 0 !important;
        padding-top: 1rem !important; /* 상단 제목이 사라졌으므로 여백 살짝 줌 */
        padding-bottom: 1rem !important; 
        margin: 0 auto !important;
        overflow-x: hidden !important; 
    }
    
    /* 헤더 제거 */
    [data-testid="stHeader"], header { display: none !important; }
    
    /* 🚨 CSS GRID 레이아웃 (메인 앱 버튼용: 245px + 65px = 320px) */
    #root div[data-testid="stHorizontalBlock"] {
        display: grid !important;
        grid-template-columns: 245px 65px !important; 
        gap: 10px !important; 
        width: 320px !important;
        min-width: 320px !important;
        max-width: 320px !important; 
        margin: 0 auto !important;
        padding: 0 !important;
    }
    
    #root div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child {
        width: 245px !important;
        min-width: 245px !important;
        max-width: 245px !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    #root div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:last-child {
        width: 65px !important;
        min-width: 65px !important;
        max-width: 65px !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* 🦸‍♂️ 카드 및 애니메이션 크기 (320px) */
    .poker-back, .flip-card {
        width: 100% !important;
        max-width: 320px !important; 
        height: 520px !important;
        margin: 0 auto !important; 
    }
    
    /* 커버 덱(뒷면)에 Flex Column 추가하여 타이틀 예쁘게 중앙 정렬 */
    .poker-back {
        border-radius: 25px;
        background-color: #E25E3E; 
        background-image: repeating-linear-gradient(45deg, rgba(255,255,255,0.1) 25%, transparent 25%, transparent 75%, rgba(255,255,255,0.1) 75%, rgba(255,255,255,0.1)), repeating-linear-gradient(45deg, rgba(255,255,255,0.1) 25%, transparent 25%, transparent 75%, rgba(255,255,255,0.1) 75%, rgba(255,255,255,0.1));
        background-position: 0 0, 20px 20px;
        background-size: 40px 40px;
        border: 12px solid white;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        display: flex !important;
        flex-direction: column !important; 
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

    /* 내부 요소 위치 조정 (좌상단 로고 공간 확보) */
    .emoji-huge { font-size: 85px; margin: 40px auto 15px auto; text-align: center; }
    .title-text { font-size: 24px; font-weight: 900; color: var(--text-title); margin-bottom: 25px; word-break: keep-all; text-align: center; }
    .info-row { display: flex; justify-content: space-between; font-size: 15px; font-weight: bold; margin: 10px 0; color: var(--text-muted); width: 100%; padding: 0 15px; }
    .stamina-stars { color: #FF9B50; letter-spacing: 2px; }
    
    /* 뱃지 위치 수정 (좌측 로고와 대칭) */
    .stage-badge { position: absolute; top: 20px; right: 20px; background: var(--tip-bg); padding: 5px 12px; border-radius: 15px; font-size: 12px; font-weight: bold; color: #E25E3E; }
    .flip-hint { margin-top: auto; font-size: 11px; color: var(--text-muted); font-weight: bold; animation: pulse 1.5s infinite; text-align: center; }
    
    .back-section { margin-bottom: 18px; width: 100%; }
    .back-title { font-size: 14px; font-weight: 900; color: #E25E3E; margin-bottom: 7px; }
    .back-text { font-size: 13.5px; color: var(--text-main); line-height: 1.6; word-break: keep-all; padding-left: 5px; }

    @keyframes shake { 0%, 100% { transform: rotate(0deg) scale(1); } 25% { transform: rotate(-8deg) scale(1.05); } 75% { transform: rotate(8deg) scale(1.05); } }
    .anim-shake { animation: shake 0.2s infinite; margin: 0 auto; }
    @keyframes pulse { 0%, 100% { opacity: 0.5; } 50% { opacity: 1; } }
    
    /* 👑 왕관 둥둥 애니메이션 */
    @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-10px); } 100% { transform: translateY(0px); } }
    .crown-icon { animation: float 2s ease-in-out infinite; font-size: 60px; margin-bottom: 15px; display: inline-block; }
    
    /* 🎨 버튼 공통 디자인 초기화 */
    #root div[data-testid="stButton"] { width: 100% !important; padding: 0 !important; margin: 0 !important; }
    
    #root button[kind="primary"], #root button[kind="secondary"] {
        -webkit-appearance: none !important; 
        appearance: none !important;
        height: 55px !important;
        border-radius: 15px !important;
        font-weight: 900 !important;
        border: none !important;
        transition: all 0.3s ease !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
    
    /* 🎤 팝업의 "입장하기" 버튼 (기본 320px 풀사이즈 적용) */
    #root button[kind="primary"] {
        width: 100% !important;
        max-width: 320px !important;
        margin: 0 auto !important;
        background: linear-gradient(135deg, #FFD1BA 0%, #FFB5A7 100%) !important;
        background-color: #FFB5A7 !important; 
        color: #4A4A4A !important;
        font-size: 18px !important; 
        box-shadow: 0 4px 15px rgba(255, 181, 167, 0.4) !important;
    }
    
    /* 🎲 하단 메인 영역의 "뽑기" 버튼 (245px로 축소 덮어쓰기) */
    #root div[data-testid="stHorizontalBlock"] button[kind="primary"] {
        width: 245px !important;
        min-width: 245px !important;
        max-width: 245px !important;
        margin: 0 !important;
    }
    
    /* ⚙️ 설정 & ✖️ 닫기 버튼 (Secondary) -> 크기 65px 고정 */
    #root button[kind="secondary"] {
        width: 65px !important;
        min-width: 65px !important;
        max-width: 65px !important;
        padding: 0 !important; 
        background: #B5EAD7 !important; 
        background-color: #B5EAD7 !important; 
        color: #4A4A4A !important;
        font-size: 22px !important; 
        box-shadow: 0 4px 12px rgba(181, 234, 215, 0.5) !important;
    }
    
    /* 🌙 다크모드 버튼 */
    @media (prefers-color-scheme: dark) {
        #root button[kind="primary"] {
            background: linear-gradient(135deg, #FFAAA5 0%, #FF8B94 100%) !important;
            background-color: #FF8B94 !important;
            color: #1A1A1A !important;
            box-shadow: 0 4px 15px rgba(255, 139, 148, 0.4) !important;
        }
        #root button[kind="secondary"] {
            background: #A8E6CF !important;
            background-color: #A8E6CF !important; 
            color: #1A1A1A !important;
            box-shadow: 0 4px 12px rgba(168, 230, 207, 0.4) !important;
        }
    }
    
    #root button[kind="primary"]:hover, #root button[kind="secondary"]:hover { 
        transform: translateY(-2px) !important; 
        filter: brightness(1.05); 
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

# --- 4. 세션 상태 ---
if 'intro_dismissed' not in st.session_state: st.session_state.intro_dismissed = False
if 'show_settings' not in st.session_state: st.session_state.show_settings = False
if 'chk_기' not in st.session_state: st.session_state.chk_기 = True
if 'chk_걷' not in st.session_state: st.session_state.chk_걷 = True
if 'chk_뛰' not in st.session_state: st.session_state.chk_뛰 = True
if 'dad_stam' not in st.session_state: st.session_state.dad_stam = (1, 5)
if 'kid_stam' not in st.session_state: st.session_state.kid_stam = (1, 5)
if 'keyword' not in st.session_state: st.session_state.keyword = ""
if 'picked_card' not in st.session_state: st.session_state.picked_card = None
if 'trigger_shuffle' not in st.session_state: st.session_state.trigger_shuffle = False

# ==========================================
# 👑 픽미업 101 인트로 (스플래시 화면)
# ==========================================
if not st.session_state.intro_dismissed:
    st.markdown("""
    <div style="width: 320px; margin: 0 auto; text-align: center; padding: 40px 20px; background: var(--card-front-bg); border-radius: 25px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); border: 4px solid var(--border-color); margin-top: 20px; margin-bottom: 20px;">
        <div class="crown-icon">👑</div>
        <h2 style="color: var(--text-title); margin-bottom: 20px; font-weight: 900; line-height: 1.3;">Pick Me!<br>아빠카드 101</h2>
        <p style="color: var(--text-main); line-height: 1.6; font-size: 15px; font-weight: bold; word-break: keep-all;">
            "국민 아빠 프로듀서님!<br>
            아이의 웃음을 책임질 101개의<br>레전드 놀이가 기다리고 있습니다."
        </p>
        <p style="color: var(--text-muted); font-size: 13.5px; margin-top: 20px; word-break: keep-all;">
            오늘 밤, 아이의 꿀잠을 이끌어낼<br>
            <b>최종 데뷔조(1-Pick) 놀이</b>는 무엇일까요?<br>
            당신의 놀이에 픽미업 하세요! 👇
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='width: 320px; margin: 0 auto;'>", unsafe_allow_html=True)
    
    if st.button("🎤 거실(오디션장)로 입장하기", type="primary", use_container_width=True, key="btn_intro"):
        st.session_state.intro_dismissed = True
        st.rerun()
        
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop() # 인트로가 떠 있을 땐 뒤의 메인 화면 렌더링 중지

# ==========================================
# 🏠 메인 앱 시작 (상단 공통 타이틀 완전 제거)
# ==========================================

# ⚙️ 설정 화면
if st.session_state.show_settings:
    col_t, col_c = st.columns([4, 1])
    with col_t:
        st.markdown("<h3 style='color: var(--text-title); margin-top:12px; margin-bottom:0; font-size: 20px; white-space: nowrap; letter-spacing: -0.5px;'>⚙️ 놀이 조건 설정</h3>", unsafe_allow_html=True)
    with col_c:
        if st.button("✖️", type="secondary", use_container_width=True, key="btn_close"):
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

# 🦸‍♂️ 메인 카드 화면
else:
    main_area = st.empty()
    
    # 덱 커버(poker-back)에 들어갈 공식 로고 HTML (초기 & 셔플 시 사용)
    cover_html = """
    <div style="text-align: center; width: 100%;">
        <div class="poker-back {shake_class}">
            <div style="font-family: 'Arial Black', sans-serif; font-size: 24px; color: #FFEBE0; margin-bottom: -5px; letter-spacing: 1px;">Pick Me!</div>
            <div style="font-weight: 900; font-size: 32px; color: #FFFFFF; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); margin-bottom: 15px; letter-spacing: -1px;">아빠카드 101</div>
            <div style="font-size: 85px; filter: drop-shadow(0px 5px 5px rgba(0,0,0,0.3));">🦸‍♂️</div>
        </div>
    </div>
    """

    if st.session_state.trigger_shuffle:
        st.session_state.trigger_shuffle = False
        if df.empty:
            main_area.error("데이터가 없습니다.")
        else:
            for _ in range(10): 
                # 흔들리는 애니메이션 클래스(anim-shake) 추가
                main_area.markdown(cover_html.replace("{shake_class}", "anim-shake"), unsafe_allow_html=True)
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
        # 애니메이션 없는 정적인 덱 커버
        main_area.markdown(cover_html.replace("{shake_class}", ""), unsafe_allow_html=True)
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
        
        <div style="position: absolute; top: 20px; left: 20px; text-align: left; line-height: 1.1;">
            <span style="font-size: 12px; font-weight: 900; color: #E25E3E; display: block; letter-spacing: 0.5px;">Pick Me!</span>
            <span style="font-size: 15px; font-weight: 900; color: var(--text-main); display: block; letter-spacing: -0.5px;">아빠카드 101 <span style="font-size: 14px;">🦸‍♂️</span></span>
        </div>
        
        <div class="stage-badge">{c.get('구분아이콘', '')} {c.get('아이발달단계', c.get('아이구분', ''))}</div>
        <div class="emoji-huge">{c.get('카드아이콘', c.get('아이콘', '🦸‍♂️'))}</div>
        <div class="title-text">{c.get('카드', c.get('제목', '놀이'))}</div>
        <hr style="border: 0; border-top: 2px dashed var(--border-color); margin: 15px 0; width: 100%;">
        <div class="info-row"><span>{c.get('아빠아이콘', '👨')} 아빠 체력</span><span class="stamina-stars">{c.get('아빠체력', '★★★')}</span></div>
        <div class="info-row"><span>{c.get('아이아이콘', '👶')} 아이 체력</span><span class="stamina-stars">{c.get('아이체력', '★★★')}</span></div>
        <div class="flip-hint">👆 카드를 터치해서 뒷면 보기 🔄</div>
        </div>
        
        <div class="card-panel flip-card-back">
        
        <div style="position: absolute; top: 20px; left: 20px; text-align: left; line-height: 1.1;">
            <span style="font-size: 12px; font-weight: 900; color: #E25E3E; display: block; letter-spacing: 0.5px;">Pick Me!</span>
            <span style="font-size: 15px; font-weight: 900; color: var(--text-main); display: block; letter-spacing: -0.5px;">아빠카드 101 <span style="font-size: 14px;">🦸‍♂️</span></span>
        </div>
        
        <div class="stage-badge">{c.get('구분아이콘', '')} {c.get('아이발달단계', c.get('아이구분', ''))}</div>
        <h3 style="margin-top: 35px; color:var(--text-title); font-size: 1.1em;">{c.get('카드아이콘', '🦸‍♂️')} {c.get('카드', '제목')}</h3>
        <hr style="border: 0; border-top: 1px solid var(--border-color); margin: 10px 0 15px 0;">
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

    # 🎯 하단 버튼 영역
    st.markdown("<br>", unsafe_allow_html=True)
    b_main, b_sub = st.columns([4, 1]) 
    with b_main:
        lbl = "🎲 Pick Me!" if st.session_state.picked_card is None else "🔄 다시 뽑기!"
        if st.button(lbl, type="primary", use_container_width=True, key="btn_main"):
            st.session_state.trigger_shuffle = True
            st.rerun()
    with b_sub:
        if st.button("⚙️", type="secondary", use_container_width=True, key="btn_setting"):
            st.session_state.show_settings = True
            st.rerun()
