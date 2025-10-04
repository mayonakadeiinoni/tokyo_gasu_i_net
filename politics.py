import streamlit as st

st.set_page_config(
    page_title="選挙候補者情報システム",
    page_icon="📊",
    layout="wide"
)

st.markdown(
    """
    <style>
    /* 背景のグラデーション */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }
    /* メインコンテナは背景を透過して余白を調整 */
    .block-container {
        padding-top: 20px;
        padding-bottom: 40px;
        background: transparent !important;
    }

    /* ヘッダ文字の装飾 */
    .app-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        margin-bottom: 0.3rem;
    }
    .app-subtitle {
        color: rgba(255,255,255,0.95);
        font-size: 1.05rem;
        margin-bottom: 1.2rem;
    }

    /* カード風のボックス */
    .search-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 1rem 1.2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.18);
        margin-bottom: 1.2rem;
    }

    /* 候補者カード */
    .candidate-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 18px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.12);
        transition: transform .2s ease, box-shadow .2s ease;
        margin-bottom: 12px;
        min-height: 220px;
    }
    .candidate-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 16px 36px rgba(0,0,0,0.22);
    }
    .candidate-photo {
        width: 84px;
        height: 84px;
        border-radius: 50%;
        margin: 0 auto 10px auto;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #ffffff;
        font-size: 2.1rem;
        font-weight: 800;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .candidate-name {
        text-align: center;
        font-weight: 700;
        color: #333;
        font-size: 1.06rem;
        margin-bottom: 4px;
    }
    .candidate-party {
        text-align: center;
        display: inline-block;
        padding: 4px 10px;
        background: #f0f0f0;
        border-radius: 999px;
        font-size: 0.85rem;
        color: #666;
        margin: 0 auto 6px auto;
    }
    .candidate-brief {
        text-align: center;
        font-size: 0.92rem;
        color: #777;
        line-height: 1.5;
        min-height: 44px;
    }

    /* セクション見出し */
    .section-title {
        font-size: 1.1rem;
        font-weight: 800;
        color: #667eea;
        border-left: 4px solid #667eea;
        padding-left: 10px;
        margin: 14px 0 8px 0;
    }
    .manifesto li {
        padding: 8px 10px;
        margin-bottom: 8px;
        background: #f8f9ff;
        border-left: 4px solid #667eea;
        border-radius: 6px;
        list-style: none;
    }

    /* ボタンの下に少し余白 */
    .stButton > button {
        width: 100%;
        margin-top: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="app-title">選挙候補者情報システム</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">候補者の情報を検索・閲覧できます</div>', unsafe_allow_html=True)
st.markdown('<div class="search-card">', unsafe_allow_html=True)
st.header("候補者を検索")
search_query = st.text_input("候補者名または政党名を入力してください", "")
st.markdown('</div>', unsafe_allow_html=True)

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

#候補者一覧表示
if not search_query:
    st.header("候補者一覧")
    cols = st.columns(3)
    for idx, candidate in enumerate(candidates):
        with cols[idx % 3]:
            st.markdown('<div class="candidate-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="candidate-photo">{candidate["name"][0]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="candidate-name">{candidate["name"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="candidate-party">{candidate["party"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="candidate-brief">{candidate["brief"]}</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title">マニフェスト</div>', unsafe_allow_html=True)
            manifesto_html = '<ul class="manifesto">'
            for item in candidate["manifesto"]:
                manifesto_html += f'<li>{item}</li>'
            manifesto_html += '</ul>'
            st.markdown(manifesto_html, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# 検索結果の表示
if search_query:
    filtered_candidates = [
        c for c in candidates if search_query in c["name"] or search_query in c["party"]
    ]
    if filtered_candidates:
        for candidate in filtered_candidates:
            st.markdown('<div class="candidate-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="candidate-photo">{candidate["name"][0]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="candidate-name">{candidate["name"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="candidate-party">{candidate["party"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="candidate-brief">{candidate["brief"]}</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title">マニフェスト</div>', unsafe_allow_html=True)
            manifesto_html = '<ul class="manifesto">'
            for item in candidate["manifesto"]:
                manifesto_html += f'<li>{item}</li>'
            manifesto_html += '</ul>'
            st.markdown(manifesto_html, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("該当する候補者が見つかりませんでした。")