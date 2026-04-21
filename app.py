import streamlit as st
import pandas as pd
import time
import random

# --- 1. 페이지 기본 설정 ---
st.set_page_config(
    page_title="픽미! 아빠카드 101",
    page_icon="🎲",
    layout="centered"
)

# --- 2. CSS 스타일링 (무적의 레이아웃 & 효과 통합) ---
st.set_option("client.toolbarMode", "viewer") 

st.markdown("""
<style>
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

    .stApp { background-color: var(--app-bg) !important; }
    
    .block-container { 
        width: 100% !important;
        max-width: 360px !important; 
        padding-left: 0 !important;
        padding-right: 0 !important;
        padding-top: 1rem !important; 
        padding-bottom: 1rem !important; 
        margin: 0 auto !important;
        overflow-x: hidden !important; 
    }
    
    /* 🚨 스트림릿 기본 UI (헤더, 하단 워터마크, 깃허브 로고 등) 완벽 암살! */
    [data-testid="stHeader"], header { display: none !important; } /* 상단 여백/헤더 제거 */
    footer { display: none !important; } /* 하단 Made with Streamlit 제거 */
    .stDeployButton { display: none !important; } /* 클라우드 배포 버튼 제거 */
    [data-testid="stToolbar"] { display: none !important; } /* 우측 상단 툴바 메뉴 제거 */
    [data-testid="stStatusWidget"] { display: none !important; } /* 우측 하단 깃허브/왕관 로고 제거 */
    #MainMenu { display: none !important; } /* 햄버거 메뉴 제거 */
            
    
    /* 하단 버튼 영역 그리드 (245px + 65px) */
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
    
    #root div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        width: 100% !important;
        min-width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    .poker-back, .flip-card {
        width: 100% !important;
        max-width: 320px !important; 
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
    
    /* 🌟 황금빛 조커 특수 효과 */
    .golden-joker {
        border: 4px solid #FFD700 !important;
        background: linear-gradient(135deg, #FFFDE7 0%, #FFF8E1 100%) !important;
        animation: goldPulse 0.5s infinite alternate !important;
    }
    .golden-joker-back {
        border: 4px solid #FFD700 !important;
        background: linear-gradient(135deg, #FFF8E1 0%, #FFECB3 100%) !important;
        animation: goldPulse 0.5s infinite alternate !important;
    }
    @keyframes goldPulse {
        0% { box-shadow: 0 0 10px rgba(255,215,0,0.5), inset 0 0 10px rgba(255,215,0,0.3); }
        100% { box-shadow: 0 0 30px rgba(255,215,0,1), inset 0 0 20px rgba(255,215,0,0.6); }
    }
    
    /* 조커 카드 글씨색 가독성 고정 */
    .golden-joker .title-text, .golden-joker-back h3 { color: #B8860B !important; }
    .golden-joker .info-row span, .golden-joker-back .back-title, 
    .golden-joker-back .back-text, .golden-joker .flip-hint, 
    .golden-joker-back .flip-hint, .golden-joker div > span, .golden-joker-back div > span {
        color: #2C3E50 !important; text-shadow: none !important; 
    }

    .flip-card-front { background: var(--card-front-bg); align-items: center; justify-content: center; color: var(--text-main) !important; }
    .flip-card-back { background: var(--card-back-bg); transform: rotateY(180deg); text-align: left; overflow-y: auto; justify-content: flex-start; color: var(--text-main) !important; }

    .emoji-huge { font-size: 85px; margin: 30px auto 15px auto; text-align: center; }
    .title-text { font-size: 24px; font-weight: 900; color: var(--text-title); margin-bottom: 25px; word-break: keep-all; text-align: center; }
    .info-row { display: flex; justify-content: space-between; font-size: 15px; font-weight: bold; margin: 10px 0; color: var(--text-muted); width: 100%; padding: 0 15px; }
    .stamina-stars { color: #FF9B50; letter-spacing: 2px; }
    
    .stage-badge { position: absolute; top: 20px; right: 20px; background: var(--tip-bg); padding: 5px 12px; border-radius: 15px; font-size: 12px; font-weight: bold; color: #E25E3E; }
    .flip-hint { margin-top: auto; font-size: 11px; color: var(--text-muted); font-weight: bold; animation: pulse 1.5s infinite; text-align: center; }
    
    .back-section { margin-bottom: 18px; width: 100%; }
    .back-title { font-size: 14px; font-weight: 900; color: #E25E3E; margin-bottom: 7px; }
    .back-text { font-size: 13.5px; color: var(--text-main); line-height: 1.6; word-break: keep-all; padding-left: 5px; }

    /* 🎆 폭죽 팝업 애니메이션 */
    .fireworks-popup {
        position: absolute; top: -30px; left: 50%; transform: translateX(-50%);
        background: rgba(0,0,0,0.8); color: #FFF; padding: 10px 20px;
        border-radius: 20px; font-weight: 900; font-size: 16px; white-space: nowrap;
        z-index: 1000; animation: popDownUp 3s forwards; pointer-events: none;
    }
    @keyframes popDownUp {
        0% { top: -50px; opacity: 0; transform: translateX(-50%) scale(0.5); }
        15% { top: 20px; opacity: 1; transform: translateX(-50%) scale(1.2); }
        25% { transform: translateX(-50%) scale(1); }
        80% { top: 20px; opacity: 1; transform: translateX(-50%) scale(1); }
        100% { top: -50px; opacity: 0; transform: translateX(-50%) scale(0.5); }
    }

    @keyframes shake { 0%, 100% { transform: rotate(0deg) scale(1); } 25% { transform: rotate(-8deg) scale(1.05); } 75% { transform: rotate(8deg) scale(1.05); } }
    .anim-shake { animation: shake 0.2s infinite; margin: 0 auto; }
    @keyframes pulse { 0%, 100% { opacity: 0.5; } 50% { opacity: 1; } }
    @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-10px); } 100% { transform: translateY(0px); } }
    .crown-icon { animation: float 2s ease-in-out infinite; font-size: 60px; margin-bottom: 15px; display: inline-block; }
    
    #root div[data-testid="stButton"] { width: 100% !important; padding: 0 !important; margin: 0 !important; }
    
    #root button[kind="primary"], #root button[kind="secondary"] {
        -webkit-appearance: none !important; appearance: none !important;
        height: 55px !important; border-radius: 15px !important;
        font-weight: 900 !important; border: none !important;
        transition: all 0.3s ease !important; display: flex !important;
        justify-content: center !important; align-items: center !important;
    }
    
    #root button[kind="primary"] {
        width: 100% !important; max-width: 320px !important; margin: 0 auto !important;
        background: linear-gradient(135deg, #FFD1BA 0%, #FFB5A7 100%) !important;
        background-color: #FFB5A7 !important; color: #4A4A4A !important;
        font-size: 18px !important; box-shadow: 0 4px 15px rgba(255, 181, 167, 0.4) !important;
    }
    
    #root div[data-testid="stHorizontalBlock"] button[kind="primary"] {
        width: 245px !important; min-width: 245px !important; max-width: 245px !important; margin: 0 !important;
    }
    
    #root button[kind="secondary"] {
        width: 65px !important; min-width: 65px !important; max-width: 65px !important;
        padding: 0 !important; background: #B5EAD7 !important; background-color: #B5EAD7 !important; 
        color: #4A4A4A !important; font-size: 22px !important; box-shadow: 0 4px 12px rgba(181, 234, 215, 0.5) !important;
    }
    
    @media (prefers-color-scheme: dark) {
        #root button[kind="primary"] { background: linear-gradient(135deg, #FFAAA5 0%, #FF8B94 100%) !important; background-color: #FF8B94 !important; color: #1A1A1A !important; }
        #root button[kind="secondary"] { background: #A8E6CF !important; background-color: #A8E6CF !important; color: #1A1A1A !important; }
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
    except: return pd.DataFrame()

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
if 'use_joker' not in st.session_state: st.session_state.use_joker = True # 🚨 조커 사용 여부 기본값 True

# ==========================================
# 👑 픽미업 101 인트로
# ==========================================
if not st.session_state.intro_dismissed:
    st.markdown("""<div style="width: 320px; margin: 0 auto; text-align: center; padding: 40px 20px; background: var(--card-front-bg); border-radius: 25px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); border: 4px solid var(--border-color); margin-top: 20px;">
<div class="crown-icon">👑</div><h2 style="color: var(--text-title); margin-bottom: 20px; font-weight: 900; line-height: 1.3;">Pick Me!<br>아빠카드 101</h2>
<p style="color: var(--text-main); line-height: 1.6; font-size: 15px; font-weight: bold; word-break: keep-all;">"국민 아빠 프로듀서님!<br>아이의 웃음을 책임질 101개의<br>레전드 놀이가 기다립니다."</p></div>""", unsafe_allow_html=True)
    st.markdown("<div style='width: 320px; margin: 20px auto;'>", unsafe_allow_html=True)
    if st.button("🎤 오디션장 입장하기", type="primary", use_container_width=True, key="btn_intro"):
        st.session_state.intro_dismissed = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ==========================================
# 🏠 메인 앱 시작
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)

# ⚙️ 설정 화면
if st.session_state.show_settings:
    col_t, col_c = st.columns([4, 1])
    with col_t: 
        st.markdown("<h3 style='color: var(--text-title); margin-top:12px; font-size: 20px; white-space: nowrap; letter-spacing: -0.5px;'>⚙️ 놀이 조건 설정</h3>", unsafe_allow_html=True)
    with col_c: 
        if st.button("✖️", type="secondary", use_container_width=True, key="btn_close"):
            st.session_state.show_settings = False
            st.rerun()
    st.markdown("<hr style='border: 0; border-top: 2px dashed var(--border-color); margin: 10px 0 20px 0;'>", unsafe_allow_html=True)
    st.session_state.chk_기 = st.checkbox("👶 기는아이", value=st.session_state.chk_기)
    st.session_state.chk_걷 = st.checkbox("🧒 걷는아이", value=st.session_state.chk_걷)
    st.session_state.chk_뛰 = st.checkbox("🏃 뛰는아이", value=st.session_state.chk_뛰)
    st.markdown("<br>", unsafe_allow_html=True)
    st.session_state.dad_stam = st.slider("**아빠 체력 범위**", 1, 5, st.session_state.dad_stam)
    st.session_state.kid_stam = st.slider("**아이 소모 체력 범위**", 1, 5, st.session_state.kid_stam)
    st.markdown("<br>", unsafe_allow_html=True)
    st.session_state.keyword = st.text_input("**준비물/상황 (선택)**", value=st.session_state.keyword, placeholder="예: 거실에서, 종이컵")
    # 🚨 조커 카드 사용 여부 체크박스 추가
    st.session_state.use_joker = st.checkbox("👸 엄마 찬스(조커) 포함하기", value=st.session_state.use_joker)

# 🃏 카드 화면
else:
    main_area = st.empty()
    cover_html = """<div style="text-align: center; width: 100%;"><div class="poker-back {shake_class}"><div style="font-family: 'Arial Black', sans-serif; font-size: 24px; color: #FFEBE0; margin-bottom: -5px; letter-spacing: 1px;">Pick Me!</div><div style="font-weight: 900; font-size: 32px; color: #FFFFFF; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); margin-bottom: 15px; letter-spacing: -1px;">아빠카드 101</div><div style="font-size: 85px; filter: drop-shadow(0px 5px 5px rgba(0,0,0,0.3));">🦸‍♂️</div></div></div>"""

    if st.session_state.trigger_shuffle:
        st.session_state.trigger_shuffle = False
        for _ in range(10): 
            main_area.markdown(cover_html.replace("{shake_class}", "anim-shake"), unsafe_allow_html=True)
            time.sleep(0.08)
        
        # 🃏 5% 확률 조커 (설정에서 허용된 경우에만)
        if st.session_state.use_joker and random.random() < 0.05:
            st.session_state.picked_card = {
                '구분아이콘': '🎉', '아이발달단계': '전체이용가', '카드아이콘': '👸', '카드': '엄마 찬스! (조커)',
                '아빠아이콘': '🛋️', '아빠체력': '소모 0 (충전)', '아이아이콘': '📺', '아이체력': '소모 0',
                '필요도구': '리모컨, 소파, 눈치',
                '놀이방법': '1. 조용히 엄마에게 이 카드를 보여줍니다.<br>2. 리모컨을 쥐고 소파와 합체가 됩니다.<br>3. 최소 15분간 자유를 만끽하세요!',
                '아빠꿀팁': '너무 좋아하면 등짝 스매싱이 날아올 수 있으니 비장한 표정을 유지하세요.'
            }
        else:
            stage_keywords = []
            if st.session_state.chk_기: stage_keywords.append("기는아이") 
            if st.session_state.chk_걷: stage_keywords.append("걷는아이")
            if st.session_state.chk_뛰: stage_keywords.append("뛰는아이")
            col_stage = '아이발달단계' if '아이발달단계' in df.columns else '아이구분'
            f_df = df[df[col_stage].astype(str).str.contains("|".join(stage_keywords))] if stage_keywords else pd.DataFrame()
            if not f_df.empty:
                d_min, d_max = st.session_state.dad_stam
                k_min, k_max = st.session_state.kid_stam
                f_df = f_df[(f_df['dad_score']>=d_min)&(f_df['dad_score']<=d_max)&(f_df['kid_score']>=k_min)&(f_df['kid_score']<=k_max)]
            kw = st.session_state.keyword.strip()
            if not f_df.empty and kw:
                f_df = f_df[f_df['카드'].astype(str).str.contains(kw) | f_df['필요도구'].astype(str).str.contains(kw)]
            
            if len(f_df) > 0:
                card_data = f_df.sample(1).iloc[0].to_dict()
                missions = ["외계인 목소리로 놀아주기", "아이에게 극존칭 쓰기", "놀이 끝날 때 엉덩이 춤 춰주기", "놀이 중간에 3번 '사랑해' 말하기", "한 손만 사용해서 놀아주기", "로봇 연기하며 놀아주기"]
                card_data['놀이방법'] += f"<br><br><b style='color:#E25E3E;'>🤪 오늘의 특별 미션:</b><br>{random.choice(missions)}"
                st.session_state.picked_card = card_data
            else: st.session_state.picked_card = "empty"
        st.rerun()

    if st.session_state.picked_card is None:
        main_area.markdown(cover_html.replace("{shake_class}", ""), unsafe_allow_html=True)
    elif st.session_state.picked_card == "empty":
        main_area.warning("⚠️ 조건에 맞는 놀이가 없어요. ⚙️ 설정에서 조건을 변경해주세요!")
    else:
        c = st.session_state.picked_card
        
        is_joker = "조커" in c.get('카드', '')
        joker_front_class = "golden-joker" if is_joker else ""
        joker_back_class = "golden-joker-back" if is_joker else ""
        
        # 🚨 조커 카드 당첨 시 축하 풍선 발동!
        if is_joker: st.balloons()
        
        # 꿀팁 배경색 (조커 여부에 따라 결정)
        tip_bg = "background: rgba(255, 215, 0, 0.25); color: #2C3E50;" if is_joker else "background: var(--tip-bg);"
        
        # 🎆 5성급 꿀잠 카드 폭죽 이펙트
        fireworks_html = "<div class='fireworks-popup'>🎇 팡! 육퇴 확정 꿀잠 보장! 🎆</div>" if c.get('아이체력') == '★★★★★' else ""
        
        main_area.markdown(f"""<div style="text-align: center; width: 100%; position: relative;">{fireworks_html}<label class="flip-card"><input type="checkbox" style="display: none;"><div class="flip-card-inner"><div class="card-panel flip-card-front {joker_front_class}"><div style="position: absolute; top: 20px; left: 20px; text-align: left; line-height: 1.1;"><span style="font-size: 12px; font-weight: 900; color: #E25E3E;">Pick Me!</span><br><span style="font-size: 15px; font-weight: 900;">아빠카드 101 🦸‍♂️</span></div><div class="stage-badge">{c.get('구분아이콘','')} {c.get('아이발달단계','')}</div><div class="emoji-huge">{c.get('카드아이콘','🦸‍♂️')}</div><div class="title-text">{c.get('카드','놀이')}</div><hr style="border: 0; border-top: 2px dashed var(--border-color); margin: 15px 0; width: 100%;"><div class="info-row"><span>{c.get('아빠아이콘','👨')} 아빠 체력</span><span class="stamina-stars">{c.get('아빠체력','')}</span></div><div class="info-row"><span>{c.get('아이아이콘','👶')} 아이 체력</span><span class="stamina-stars">{c.get('아이체력','')}</span></div><div class="flip-hint">👆 터치해서 뒷면 보기 🔄</div></div><div class="card-panel flip-card-back {joker_back_class}"><div style="position: absolute; top: 20px; left: 20px; text-align: left; line-height: 1.1;"><span style="font-size: 12px; font-weight: 900; color: #E25E3E;">Pick Me!</span><br><span style="font-size: 15px; font-weight: 900;">아빠카드 101 🦸‍♂️</span></div><div class="stage-badge">{c.get('구분아이콘','')} {c.get('아이발달단계','')}</div><h3 style="margin-top: 35px; color:var(--text-title); font-size: 1.1em;">{c.get('카드아이콘','🦸‍♂️')} {c.get('카드','')}</h3><hr style="border: 0; border-top: 1px solid var(--border-color); margin: 10px 0 15px 0; width: 100%;"><div class="back-section"><div class="back-title">🎒 필요 도구</div><div class="back-text">{c.get('필요도구','')}</div></div><div class="back-section"><div class="back-title">📝 놀이 방법</div><div class="back-text">{c.get('놀이방법','')}</div></div><div class="back-section"><div class="back-title">💡 아빠 꿀팁</div><div class="back-text" style="{tip_bg} padding:15px; border-radius:12px;">{c.get('아빠꿀팁','')}</div></div><div class="flip-hint">👆 다시 터치해서 앞면 보기 🔄</div></div></div></label></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    b_main, b_sub = st.columns([4, 1]) 
    with b_main:
        if st.button("🎲 Pick Me!" if st.session_state.picked_card is None else "🔄 다시 뽑기!", type="primary", use_container_width=True, key="btn_main"):
            st.session_state.trigger_shuffle = True
            st.rerun()
    with b_sub:
        if st.button("⚙️", type="secondary", use_container_width=True, key="btn_setting"):
            st.session_state.show_settings = True
            st.rerun()
