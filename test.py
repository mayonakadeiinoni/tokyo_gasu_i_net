# app.py
# -*- coding: utf-8 -*-
# 📊 選挙候補者情報システム（Streamlit版・疑似画面遷移付き）
# - URLクエリパラメータ（view, id）を使って「一覧」と「詳細」を切り替え
# - ボタンクリックでクエリを更新 → st.rerun() により再描画
# - CSSアニメーション（左右スライド＋フェード）で「画面遷移っぽさ」を演出
# - 1ファイルでそのまま実行可能

from __future__ import annotations
import streamlit as st
from typing import List, Dict, Any

# --------------------------------
# ページ設定
# --------------------------------
st.set_page_config(
    page_title="選挙候補者情報システム",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------
# CSS（画面遷移のアニメーション含む）
# --------------------------------
st.markdown(
    """
<style>
.stApp {
  background: linear-gradient(135deg, #ECECFF 0%, #F8F8FF 100%);
  font-family: -apple-system, BlinkMacSystemFont, "Hiragino Sans", "Yu Gothic", "Noto Sans JP", sans-serif;
}

/* ヘッダー */
.app-header { text-align:center; color:#4a4a6a; margin: 6px 0 18px; }
.app-header h1 { font-size:2.0rem; margin-bottom:.2rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }
.app-header .subtitle { font-size:1rem; opacity:.9; }

/* 画面コンテナ & アニメーション */
.page {
  background: transparent;
}
@media (prefers-reduced-motion: no-preference) {
  .enter-left  { animation: slideInFromLeft .28s ease both; }
  .enter-right { animation: slideInFromRight .28s ease both; }
}
@keyframes slideInFromLeft {
  from { opacity: 0; transform: translateX(-10px); }
  to   { opacity: 1; transform: translateX(0); }
}
@keyframes slideInFromRight {
  from { opacity: 0; transform: translateX(10px); }
  to   { opacity: 1; transform: translateX(0); }
}

/* フィルタ表示（チップ）*/
.chips { display:flex; gap:8px; flex-wrap:wrap; align-items:center; background:#f8f9ff; border-radius:8px; padding:8px 12px; }
.chip-label { font-weight:700; color:#666; margin-right:4px; }
.chip { display:inline-flex; align-items:center; gap:6px; background:white; padding:6px 12px; border-radius:20px; font-size:.85em; color:#333; 
        box-shadow: 0 2px 4px rgba(0,0,0,.08); }

/* 候補者カード */
.candidate-card { background:white; border-radius:16px; padding:16px; text-align:center; 
  box-shadow: 0 4px 12px rgba(0,0,0,.08); transition: transform .2s ease, box-shadow .2s ease, border .2s ease; border: 2px solid transparent; }
.candidate-card:hover { transform: translateY(-6px); box-shadow: 0 8px 24px rgba(0,0,0,.12); }
.candidate-card.selected { border: 3px solid #667eea; box-shadow: 0 8px 24px rgba(102,126,234,.3); }

.candidate-photo { width:120px; height:120px; border-radius:50%; margin: 0 auto 12px; display:flex; align-items:center; justify-content:center; 
  color:white; font-size:2.4rem; font-weight:700; box-shadow: 0 5px 15px rgba(0,0,0,.2); border: 3px solid; }
.candidate-name { font-size:1.1rem; font-weight:700; color:#333; margin-bottom:6px; }
.candidate-tags { font-size:.85rem; color:#888; margin-bottom:8px; display:flex; gap:8px; justify-content:center; flex-wrap:wrap; }
.tag { background:#f0f0f0; padding:3px 8px; border-radius:4px; white-space:nowrap; }
.candidate-party { display:inline-block; padding: 4px 12px; border-radius: 20px; font-size:.9rem; margin-bottom:8px; font-weight:700; border: 2px solid; }
.party-icon { margin-right:6px; font-size:1.1em; }
.candidate-brief { font-size:.9rem; color:#777; line-height:1.5; min-height: 3em; }

/* 詳細カード（モーダル相当）*/
.detail-card { background:white; border-radius:16px; padding:24px; box-shadow: 0 8px 32px rgba(0,0,0,.15); }
.detail-header { text-align:center; padding-bottom:12px; border-bottom: 2px solid #f0f0f0; margin-bottom:16px; }
.modal-photo { width:150px; height:150px; border-radius:50%; margin: 0 auto 12px; display:flex; align-items:center; justify-content:center; 
  color:white; font-size:3rem; font-weight:700; box-shadow: 0 10px 25px rgba(0,0,0,.2); border: 4px solid; }
.section-title { font-size:1.2rem; font-weight:700; color:#667eea; margin: 16px 0 8px; padding-left: 12px; border-left: 4px solid #667eea; }
.manifesto-list { list-style:none; padding-left:0; margin:0; }
.manifesto-list li { padding:12px; margin: 0 0 10px; background:#f8f9ff; border-left: 4px solid #667eea; border-radius:5px; }

/* 政党カラー */
.photo-A党 { background: linear-gradient(135deg, #3d94c3 0%, #2b7a9e 100%); border-color:#236680; }
.photo-B党 { background: linear-gradient(135deg, #e89060 0%, #d77840 100%); border-color:#b8623a; }
.photo-C党 { background: linear-gradient(135deg, #9a5fb8 0%, #7d4a9a 100%); border-color:#603b7a; }
.photo-D党 { background: linear-gradient(135deg, #55a563 0%, #3d8b4a 100%); border-color:#2e6b38; }
.photo-無所属 { background: linear-gradient(135deg, #616161 0%, #424242 100%); border-color:#212121; }

.party-A党 { background:#e8f4f8; color:#2b7a9e; border-color:#2b7a9e; }
.party-B党 { background:#fff5ed; color:#d77840; border-color:#d77840; }
.party-C党 { background:#f5eef8; color:#7d4a9a; border-color:#7d4a9a; }
.party-D党 { background:#eef8f0; color:#3d8b4a; border-color:#3d8b4a; }
.party-無所属 { background:#f5f5f5; color:#424242; border-color:#757575; }
</style>
""",
    unsafe_allow_html=True,
)

# --------------------------------
# データ（HTML版を移植）
# --------------------------------
CANDIDATES: List[Dict[str, Any]] = [
    {
        "id": 1,
        "name": "田中 太郎",
        "party": "A党",
        "partyIcon": "🏛️",
        "initial": "田",
        "region": "東京1区",
        "keyPolicy": "経済",
        "brief": "経済成長と地域活性化を推進",
        "manifesto": [
            "中小企業支援のための減税措置を拡大",
            "地域経済活性化のための特別予算1000億円",
            "デジタル化推進による行政効率化",
            "若者の起業支援制度の創設",
        ],
        "career": "経済学博士。大手企業で20年の経営経験を持ち、前回の選挙で初当選。経済委員会の委員として活動。",
        "policy": "地域経済の活性化と雇用創出を最優先課題とし、特に若者や女性の働きやすい環境づくりに注力しています。",
        "theme": "経済",
    },
    {
        "id": 2,
        "name": "佐藤 花子",
        "party": "B党",
        "partyIcon": "👨‍👩‍👧",
        "initial": "佐",
        "region": "神奈川2区",
        "keyPolicy": "教育",
        "brief": "教育と子育て支援の充実",
        "manifesto": [
            "高校までの教育完全無償化",
            "保育士の待遇改善と保育所の増設",
            "給食費の無償化を全国展開",
            "教員の働き方改革の推進",
        ],
        "career": "元小学校教師。教育現場での15年の経験を活かし、子育て世代の代弁者として活動中。2期目。",
        "policy": "すべての子どもたちが平等に質の高い教育を受けられる社会の実現を目指しています。",
        "theme": "教育",
    },
    {
        "id": 3,
        "name": "鈴木 一郎",
        "party": "C党",
        "partyIcon": "🏥",
        "initial": "鈴",
        "region": "大阪3区",
        "keyPolicy": "医療",
        "brief": "医療制度改革と高齢者支援",
        "manifesto": [
            "地域医療体制の強化と医師不足の解消",
            "介護職員の給与を全国平均+30%に引き上げ",
            "高齢者向け健康促進プログラムの拡充",
            "がん検診の無料化を推進",
        ],
        "career": "医師として30年のキャリア。地域医療に貢献し、医療政策の専門家として3期目の当選。",
        "policy": "誰もが安心して医療を受けられる社会保障制度の構築を目指しています。",
        "theme": "医療",
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
            "森林保全と都市緑化の推進",
        ],
        "career": "環境NGOで活動後、政界へ。環境問題に精通し、国際会議での交渉経験も豊富。初当選。",
        "policy": "持続可能な社会の実現と次世代への責任ある環境政策を推進します。",
        "theme": "環境",
    },
    {
        "id": 5,
        "name": "中村 健一",
        "party": "無所属",
        "partyIcon": "🗣️",
        "initial": "中",
        "region": "埼玉4区",
        "keyPolicy": "政治改革",
        "brief": "地域密着型の政治改革",
        "manifesto": [
            "議員報酬の30%削減と政治資金の透明化",
            "住民投票制度の拡充",
            "地域コミュニティ活性化のための基金創設",
            "若者の政治参加を促進する教育プログラム",
        ],
        "career": "元市議会議員。市民運動のリーダーとして地域課題の解決に尽力。今回無所属で挑戦。",
        "policy": "市民の声を直接政治に反映させる、開かれた政治の実現を目指します。",
        "theme": "政治改革",
    },
    {
        "id": 6,
        "name": "小林 真理子",
        "party": "B党",
        "partyIcon": "👨‍👩‍👧",
        "initial": "小",
        "region": "愛知2区",
        "keyPolicy": "労働",
        "brief": "女性の活躍推進と働き方改革",
        "manifesto": [
            "男女の賃金格差を5年以内に解消",
            "育児休業中の所得保障を100%に",
            "テレワーク推進のための企業支援",
            "ハラスメント対策の強化",
        ],
        "career": "弁護士として労働問題に取り組み、多くの女性労働者を支援。2期目の挑戦。",
        "policy": "性別に関係なく、すべての人が能力を発揮できる社会を創ります。",
        "theme": "労働",
    },
]

PARTY_ICON_DEFAULT = {"A党": "🏛️", "B党": "👨‍👩‍👧", "C党": "🏥", "D党": "🌿", "無所属": "🗣️"}


# --------------------------------
# ルーティング補助
# --------------------------------
def _set_query_params(**params):
    try:
        st.query_params.clear()
        for k, v in params.items():
            if v is not None:
                st.query_params[k] = str(v)
    except Exception:
        st.experimental_set_query_params(**{k: str(v) for k, v in params.items() if v is not None})

def nav_to_list_clear():
    """一覧ビューへ遷移しつつ clear=1 を立てる（この後 rerun）"""
    _set_query_params(view="list", clear="1")
    st.rerun()

def consume_clear_if_needed():
    """
    ?clear=1 が付与されていたら、ウィジェット生成前に初期化して
    ?view=list に戻す（clear は消して2重実行を防止）
    """
    try:
        has_clear = "clear" in st.query_params
    except Exception:
        has_clear = "clear" in st.experimental_get_query_params()
    if has_clear:
        # ここはウィジェット生成前に呼ぶこと
        st.session_state["party_filter"] = "すべて"
        st.session_state["policy_filter"] = "すべて"
        st.session_state["search_input"] = ""
        # （任意）詳細選択の解除
        st.session_state["selected_id"] = None
        # clear を除去して list へ固定 → 再実行
        _set_query_params(view="list")
        st.rerun()

def get_query_params():
    """view ('list' or 'detail'), id (str|None) を取得（新旧API両対応）"""
    view, cid = "list", None
    try:
        # 新API（1.30+）
        qp = st.query_params
        view = qp.get("view", "list")
        cid = qp.get("id", None)
    except Exception:
        # 旧API
        qp = st.experimental_get_query_params()
        view = qp.get("view", ["list"])[0] if "view" in qp else "list"
        cid = qp.get("id", [None])[0] if "id" in qp else None
    return view, cid


def nav_to(view: str, cid: int | None = None):
    """URLクエリを更新して再描画（新旧API両対応）"""
    try:
        st.query_params.clear()
        st.query_params["view"] = view
        if cid is not None:
            st.query_params["id"] = str(cid)
    except Exception:
        if cid is not None:
            st.experimental_set_query_params(view=view, id=str(cid))
        else:
            st.experimental_set_query_params(view=view)
    st.rerun()


def get_party_icon(party: str, fallback: str | None) -> str:
    return fallback or PARTY_ICON_DEFAULT.get(party, "🏛️")


# --------------------------------
# フィルタ・検索
# --------------------------------
if "party_filter" not in st.session_state:
    st.session_state.party_filter = "すべて"
if "policy_filter" not in st.session_state:
    st.session_state.policy_filter = "すべて"
if "search_input" not in st.session_state:
    st.session_state.search_input = ""

def clear_all():
    st.session_state.party_filter = "すべて"
    st.session_state.policy_filter = "すべて"
    st.session_state.search_input = ""

def apply_filters(data: List[Dict[str, Any]], party: str, policy: str, search: str) -> List[Dict[str, Any]]:
    search = (search or "").strip()
    out = []
    for c in data:
        ok_party  = (party == "すべて") or (c.get("party") == party)
        ok_policy = (policy == "すべて") or (c.get("theme") == policy)
        ok_search = (not search) or (search in c.get("name", ""))
        if ok_party and ok_policy and ok_search:
            out.append(c)
    return out


# --------------------------------
# コンポーネント描画
# --------------------------------
def render_header():
    st.markdown(
        """
<div class="app-header">
  <h1>📊 選挙候補者情報システム</h1>
  <p class="subtitle">候補者の公約・政策を確認して、あなたの一票を決めましょう</p>
</div>
""",
        unsafe_allow_html=True,
    )

def candidate_card_html(c: Dict[str, Any]) -> str:
    party = c.get("party", "無所属")
    photo_class = f"photo-{party}"
    party_class = f"party-{party}"
    initial = c.get("initial", "")
    name = c.get("name", "")
    region = c.get("region", "")
    key_policy = c.get("keyPolicy", "")
    brief = c.get("brief", "")
    party_icon = get_party_icon(party, c.get("partyIcon"))

    tags = []
    if region:     tags.append(f'<span class="tag">📍 {region}</span>')
    if key_policy: tags.append(f'<span class="tag">🎯 {key_policy}</span>')
    tags_html = "".join(tags)

    return f"""
    <div class="candidate-card">
      <div class="candidate-photo {photo_class}">{initial}</div>
      <div class="candidate-name">{name}</div>
      <div class="candidate-tags">{tags_html}</div>
      <div class="candidate-party {party_class}">
        <span class="party-icon">{party_icon}</span>{party}
      </div>
      <div class="candidate-brief">{brief}</div>
    </div>
    """

def detail_html(c: Dict[str, Any]) -> str:
    party = c.get("party", "無所属")
    photo_class = f"photo-{party}"
    party_class = f"party-{party}"
    party_icon = get_party_icon(party, c.get("partyIcon"))

    initial = c.get("initial", "")
    name = c.get("name", "")
    manifesto = c.get("manifesto", []) or []
    career = c.get("career", "")
    policy = c.get("policy", "")

    manifesto_items = "\n".join([f"<li>{m}</li>" for m in manifesto])

    return f"""
    <div class="detail-card">
      <div class="detail-header">
        <div class="modal-photo {photo_class}">{initial}</div>
        <h2 style="margin:0 0 8px 0;">{name}</h2>
        <div class="candidate-party {party_class}" style="display:inline-block;">
          <span class="party-icon">{party_icon}</span>{party}
        </div>
      </div>

      <div class="section">
        <div class="section-title">📋 主な公約</div>
        <ul class="manifesto-list">{manifesto_items}</ul>
      </div>

      <div class="section">
        <div class="section-title">💼 経歴・実績</div>
        <div style="line-height:1.8; color:#555;">{career}</div>
      </div>

      <div class="section">
        <div class="section-title">🎯 重点政策</div>
        <div style="line-height:1.8; color:#555;">{policy}</div>
      </div>
    </div>
    """


# --------------------------------
# 一覧ページ
# --------------------------------
def render_list_page():
    render_header()
    consume_clear_if_needed()

    # フィルタ行
    fc1, fc2, fc3, fc4 = st.columns([1, 1, 2, 1])
    with fc1:
        st.selectbox(
            "政党",
            options=["すべて", "A党", "B党", "C党", "D党", "無所属"],
            key="party_filter",
        )
    with fc2:
        st.selectbox(
            "政策テーマ",
            options=["すべて", "経済", "教育", "医療", "環境"],
            key="policy_filter",
        )
    with fc3:
        st.text_input("候補者名で検索", key="search_input", placeholder="例：田中 / 佐藤 など")
    with fc4:
        if st.button("🧹 すべてクリア", use_container_width=True):
            nav_to_list_clear()

    # アクティブフィルタ（チップ）
    chips = []
    if st.session_state.party_filter != "すべて":
        chips.append(f"<span class='chip'>政党：{st.session_state.party_filter}</span>")
    if st.session_state.policy_filter != "すべて":
        chips.append(f"<span class='chip'>政策：{st.session_state.policy_filter}</span>")
    if st.session_state.search_input.strip():
        chips.append(f"<span class='chip'>検索：『{st.session_state.search_input.strip()}』</span>")
    if chips:
        st.markdown(
            "<div class='chips'><span class='chip-label'>現在の条件：</span>" + "".join(chips) + "</div>",
            unsafe_allow_html=True,
        )

    st.divider()

    # グリッド
    items = apply_filters(CANDIDATES, st.session_state.party_filter, st.session_state.policy_filter, st.session_state.search_input)
    if not items:
        st.info("該当する候補者が見つかりません。条件を調整してください。")
        return

    N_COLS = 4
    cols = st.columns(N_COLS, gap="large")
    for idx, c in enumerate(items):
        col = cols[idx % N_COLS]
        with col:
            st.markdown(candidate_card_html(c), unsafe_allow_html=True)
            # ここが「画面遷移」：URLクエリを detail に切り替えて再描画
            if st.button("詳細を見る ➜", key=f"goto_{c['id']}", use_container_width=True):
                nav_to("detail", c["id"])

#save
# --------------------------------
# 詳細ページ
# --------------------------------
def render_detail_page(cid_str: str | None):
    render_header()

    # パンくず & 戻る
    bc1, bc2 = st.columns([1, 6])
    with bc1:
        if st.button("← 一覧へ戻る", use_container_width=True):
            _set_query_params(view="list")
            st.rerun()
    with bc2:
        if st.button("🧹 すべてクリア", use_container_width=True):
            nav_to_list_clear()

    # 対象候補
    candidate = None
    try:
        cid = int(cid_str) if cid_str is not None else None
    except ValueError:
        cid = None
    if cid is not None:
        for c in CANDIDATES:
            if c["id"] == cid:
                candidate = c
                break
    if not candidate:
        st.warning("対象の候補者が見つかりません。")
        return

    st.markdown(detail_html(candidate), unsafe_allow_html=True)

    # 下部に同じ政党の他候補などを出す場合の例（任意）
    same_party = [c for c in CANDIDATES if c["party"] == candidate["party"] and c["id"] != candidate["id"]]
    if same_party:
        st.markdown("#### 同じ政党の候補者")
        cols = st.columns(min(4, len(same_party)), gap="large")
        for i, c in enumerate(same_party):
            with cols[i % len(cols)]:
                st.markdown(candidate_card_html(c), unsafe_allow_html=True)
                if st.button("この候補を見る ➜", key=f"goto_same_{c['id']}", use_container_width=True):
                    nav_to("detail", c["id"])


# --------------------------------
# ルーティング（表示面のアニメーション方向も合わせる）
# --------------------------------
view, cid = get_query_params()
enter_class = "enter-right" if view == "detail" else "enter-left"
st.markdown(f"<div class='page {enter_class}'>", unsafe_allow_html=True)

if view == "detail":
    render_detail_page(cid)
else:
    render_list_page()

st.markdown("</div>", unsafe_allow_html=True)
