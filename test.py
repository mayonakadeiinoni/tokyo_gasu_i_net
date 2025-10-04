import streamlit as st

# ページ設定
st.set_page_config(
    page_title="選挙候補者情報システム",
    page_icon="📊",
    layout="wide"
)

# カスタムCSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .candidate-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        margin-bottom: 20px;
        transition: transform 0.3s;
    }
    .candidate-card:hover {
        transform: translateY(-5px);
    }
    h1 {
        color: white;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    .subtitle {
        color: white;
        text-align: center;
        font-size: 1.1em;
        margin-bottom: 30px;
    }
    .candidate-name {
        font-size: 1.5em;
        font-weight: bold;
        color: #333;
        margin-bottom: 10px;
    }
    .party-badge {
        display: inline-block;
        padding: 5px 15px;
        background: #f0f0f0;
        border-radius: 20px;
        font-size: 0.9em;
        color: #666;
        margin-bottom: 10px;
    }
    .section-title {
        font-size: 1.2em;
        font-weight: bold;
        color: #667eea;
        margin-top: 20px;
        margin-bottom: 10px;
        padding-left: 10px;
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# 候補者データ
candidates = [
    {
        "id": 1,
        "name": "田中 太郎",
        "party": "A党",
        "initial": "田",
        "brief": "経済成長と地域活性化を推進",
        "manifesto": [
            "中小企業支援のための減税措置を拡大",
            "地域経済活性化のための特別予算1000億円",
            "デジタル化推進による行政効率化",
            "若者の起業支援制度の創設"
        ],
        "career": "経済学博士。大手企業で20年の経営経験を持ち、前回の選挙で初当選。経済委員会の委員として活動。",
        "policy": "地域経済の活性化と雇用創出を最優先課題とし、特に若者や女性の働きやすい環境づくりに注力しています。",
        "theme": "経済"
    },
    {
        "id": 2,
        "name": "佐藤 花子",
        "party": "B党",
        "initial": "佐",
        "brief": "教育と子育て支援の充実",
        "manifesto": [
            "高校までの教育完全無償化",
            "保育士の待遇改善と保育所の増設",
            "給食費の無償化を全国展開",
            "教員の働き方改革の推進"
        ],
        "career": "元小学校教師。教育現場での15年の経験を活かし、子育て世代の代弁者として活動中。2期目。",
        "policy": "すべての子どもたちが平等に質の高い教育を受けられる社会の実現を目指しています。",
        "theme": "教育"
    },
    {
        "id": 3,
        "name": "鈴木 一郎",
        "party": "C党",
        "initial": "鈴",
        "brief": "医療制度改革と高齢者支援",
        "manifesto": [
            "地域医療体制の強化と医師不足の解消",
            "介護職員の給与を全国平均+30%に引き上げ",
            "高齢者向け健康促進プログラムの拡充",
            "がん検診の無料化を推進"
        ],
        "career": "医師として30年のキャリア。地域医療に貢献し、医療政策の専門家として3期目の当選。",
        "policy": "誰もが安心して医療を受けられる社会保障制度の構築を目指しています。",
        "theme": "医療"
    },
    {
        "id": 4,
        "name": "山田 美咲",
        "party": "A党",
        "initial": "山",
        "brief": "環境保護とクリーンエネルギー",
        "manifesto": [
            "2035年までに再生可能エネルギー比率50%達成",
            "電気自動車購入補助金の大幅拡充",
            "プラスチック削減条例の制定",
            "森林保全と都市緑化の推進"
        ],
        "career": "環境NGOで活動後、政界へ。環境問題に精通し、国際会議での交渉経験も豊富。初当選。",
        "policy": "持続可能な社会の実現と次世代への責任ある環境政策を推進します。",
        "theme": "環境"
    },
    {
        "id": 5,
        "name": "中村 健一",
        "party": "無所属",
        "initial": "中",
        "brief": "地域密着型の政治改革",
        "manifesto": [
            "議員報酬の30%削減と政治資金の透明化",
            "住民投票制度の拡充",
            "地域コミュニティ活性化のための基金創設",
            "若者の政治参加を促進する教育プログラム"
        ],
        "career": "元市議会議員。市民運動のリーダーとして地域課題の解決に尽力。今回無所属で挑戦。",
        "policy": "市民の声を直接政治に反映させる、開かれた政治の実現を目指します。",
        "theme": "政治改革"
    },
    {
        "id": 6,
        "name": "小林 真理子",
        "party": "B党",
        "initial": "小",
        "brief": "女性の活躍推進と働き方改革",
        "manifesto": [
            "男女の賃金格差を5年以内に解消",
            "育児休業中の所得保障を100%に",
            "テレワーク推進のための企業支援",
            "ハラスメント対策の強化"
        ],
        "career": "弁護士として労働問題に取り組み、多くの女性労働者を支援。2期目の挑戦。",
        "policy": "性別に関係なく、すべての人が能力を発揮できる社会を創ります。",
        "theme": "労働"
    }
]

# ヘッダー
st.markdown("<h1>📊 選挙候補者情報システム</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>候補者の公約・政策を確認して、あなたの一票を決めましょう</p>", unsafe_allow_html=True)

# フィルター部分
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    party_filter = st.selectbox(
        "政党で絞り込み",
        ["すべて", "A党", "B党", "C党", "無所属"]
    )

with col2:
    theme_filter = st.selectbox(
        "政策テーマで絞り込み",
        ["すべて", "経済", "教育", "医療", "環境", "政治改革", "労働"]
    )

with col3:
    search_text = st.text_input("候補者名で検索", "")

st.markdown("---")

# フィルタリング
filtered_candidates = candidates

if party_filter != "すべて":
    filtered_candidates = [c for c in filtered_candidates if c["party"] == party_filter]

if theme_filter != "すべて":
    filtered_candidates = [c for c in filtered_candidates if c["theme"] == theme_filter]

if search_text:
    filtered_candidates = [c for c in filtered_candidates if search_text.lower() in c["name"].lower()]

# 候補者一覧表示
st.markdown(f"### 候補者一覧 ({len(filtered_candidates)}名)")

# 3列のグリッドレイアウト
cols_per_row = 3
for i in range(0, len(filtered_candidates), cols_per_row):
    cols = st.columns(cols_per_row)
    for j in range(cols_per_row):
        if i + j < len(filtered_candidates):
            candidate = filtered_candidates[i + j]
            with cols[j]:
                with st.container():
                    # 候補者カード
                    st.markdown(f"""
                    <div style='background: white; padding: 20px; border-radius: 15px; 
                                box-shadow: 0 5px 15px rgba(0,0,0,0.2); text-align: center;'>
                        <div style='width: 100px; height: 100px; border-radius: 50%; 
                                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                    margin: 0 auto 15px; display: flex; align-items: center; 
                                    justify-content: center; color: white; font-size: 2.5em; 
                                    font-weight: bold;'>
                            {candidate['initial']}
                        </div>
                        <div style='font-size: 1.3em; font-weight: bold; color: #333; margin-bottom: 8px;'>
                            {candidate['name']}
                        </div>
                        <div style='display: inline-block; padding: 5px 15px; background: #f0f0f0; 
                                    border-radius: 20px; font-size: 0.9em; color: #666; margin-bottom: 10px;'>
                            {candidate['party']}
                        </div>
                        <div style='font-size: 0.9em; color: #777;'>
                            {candidate['brief']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 詳細表示ボタン
                    if st.button(f"詳細を見る", key=f"btn_{candidate['id']}", use_container_width=True):
                        st.session_state.selected_candidate = candidate['id']

# 選択された候補者の詳細表示
if 'selected_candidate' in st.session_state:
    selected = next((c for c in candidates if c['id'] == st.session_state.selected_candidate), None)
    
    if selected:
        st.markdown("---")
        st.markdown("## 📋 候補者詳細情報")
        
        # 候補者の基本情報
        col_left, col_right = st.columns([1, 3])
        
        with col_left:
            st.markdown(f"""
            <div style='text-align: center;'>
                <div style='width: 150px; height: 150px; border-radius: 50%; 
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            margin: 0 auto; display: flex; align-items: center; 
                            justify-content: center; color: white; font-size: 3em; 
                            font-weight: bold;'>
                    {selected['initial']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_right:
            st.markdown(f"### {selected['name']}")
            st.markdown(f"**所属政党:** {selected['party']}")
            st.markdown(f"**重点テーマ:** {selected['theme']}")
            st.markdown(f"_{selected['brief']}_")
        
        # 公約
        st.markdown("<div class='section-title'>📋 主な公約</div>", unsafe_allow_html=True)
        for manifesto_item in selected['manifesto']:
            st.markdown(f"- {manifesto_item}")
        
        # 経歴
        st.markdown("<div class='section-title'>💼 経歴・実績</div>", unsafe_allow_html=True)
        st.write(selected['career'])
        
        # 重点政策
        st.markdown("<div class='section-title'>🎯 重点政策</div>", unsafe_allow_html=True)
        st.write(selected['policy'])
        
        # 閉じるボタン
        if st.button("閉じる", use_container_width=True):
            del st.session_state.selected_candidate
            st.rerun()