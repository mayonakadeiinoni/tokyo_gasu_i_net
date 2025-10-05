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

from data import candidates

CANDIDATES: List[Dict[str, Any]] = candidates


PARTY_ICON_DEFAULT = {"自民党": "🏛️", "民主党": "👨‍👩‍👧", "立憲社会党": "🏥", "社会党": "🌿", "共産党": "🗣️"}


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
        ok_policy = (policy == "すべて") or (c.get("keyPolicy") == policy)
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
  <h1>選挙候補者情報システム</h1>
  <p class="subtitle">候補者の公約・政策を確認して、あなたの一票を決めましょう</p>
</div>
""",
        unsafe_allow_html=True,
    )
#   partyIcon  initial  manifesto
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
   # manifesto = c.get("manifesto", []) or []
    ## promise
    manifesto = []
    for key,item in c.items():
        if key.startswith("promise"):
            manifesto.append(item)
    print(f"manifesto:{manifesto}")        
    career = c.get("career", "")
    #policy = c.get("policy", "")

    manifesto_items = "\n".join([f"<li>{m}</li>" for m in manifesto if not m == ""])

    return f"""<div class="detail-card"><div class="detail-header">
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
            options=["すべて","自民党","民主党","立憲社会党", "社会党", "共産党"],
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
    if st.button("比較する", key=f"1", use_container_width=True):
                nav_to("compare")


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
# 比較ページ
# --------------------------------

def compare_html(c: Dict[str, Any]) -> str:
    render_header()
    
    party = c.get("party", "無所属")
    photo_class = f"photo-{party}"
    party_class = f"party-{party}"
    party_icon = get_party_icon(party, c.get("partyIcon"))

    initial = c.get("initial", "")
    name = c.get("name", "")
   # manifesto = c.get("manifesto", []) or []
    ## promise
    manifesto = []
    for key,item in c.items():
        if key.startswith("promise"):
            manifesto.append(item)
    print(f"manifesto:{manifesto}")        
    career = c.get("career", "")
    #policy = c.get("policy", "")

    manifesto_items = "\n".join([f"<li>{m}</li>" for m in manifesto if not m == ""])

    return f"""<div class="detail-card"><div class="detail-header">
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
    </div>
    """

import pandas as pd
def render_compare_page():
    render_header()
    st.subheader("候補者ごとの比較表")

    # 候補者リストを作る（「名前（政党）」表示）
    labels = [f"{c.get('name','')}（{c.get('party','無所属')}）" for c in CANDIDATES]
    label_to_obj = {labels[i]: CANDIDATES[i] for i in range(len(CANDIDATES))}

    # どの候補を比べる？
    selected = st.multiselect(
        "比較したい候補者",
        options=labels,
        default=labels[:min(0, len(labels))]
    )

    #
    if st.button("← 一覧へ戻る", use_container_width=True):
        _set_query_params(view="list"); st.rerun()

    if not selected:
        st.info("候補者を1人以上選んでね。")
        return

    show_comparisons = st.checkbox("争点", value=True)
    show_promises    = st.checkbox("行いたい政策", value=False)
    show_career      = st.checkbox("基本情報", value=False)

    # 表データを作る 
    rows = []

    
    if show_career:
        row = {"項目": "年齢"}
        for label in selected:
            row[label] = label_to_obj[label].get("age", "") or ""
    
        row = {"項目": "経歴"}
        for label in selected:
            row[label] = label_to_obj[label].get("career", "") or ""
        rows.append(row)
    
  #      "keyPolicy":"経済",#重点政策分野
  #  "brief":"農業と地域産業の振興を通じて、地元の暮らしを守り、次世代につながる地域社会を築きます。",#重点政策
    if show_promises:
        row = {"項目": "重点政策"}
        for label in selected:
            row[label] = label_to_obj[label].get("keyPolicy", "") or ""
        rows.append(row)
        
        row = {"項目": "政策説明"}
        for label in selected:
            row[label] = label_to_obj[label].get("brief", "") or ""
        rows.append(row)
        
        row = {"項目": "経歴"}
        for label in selected:
            row[label] = label_to_obj[label].get("career", "") or ""
        rows.append(row)
        PROMISE_MAX = 4  
        for i in range(1, PROMISE_MAX + 1):
            key = f"promise{i}"
            row = {"項目": f"📋 公約{i}"}
            for label in selected:
                row[label] = label_to_obj[label].get(key, "") or ""
            rows.append(row)

    if show_comparisons:
        topics = []
        seen = set()
        for label in selected:
            comps = (label_to_obj[label].get("comparisons") or {})
            for t in comps.keys():
                if t not in seen:
                    seen.add(t); topics.append(t)
    
        for t in topics:
            row = {"項目": f"⚖️ {t}"}
            for label in selected:
                stance = (label_to_obj[label].get("comparisons") or {}).get(t, "")
                row[label] = stance
            rows.append(row)




   

    # 表にする
    if not rows:
        st.info("上のチェックボックスで出したい“かたまり”を選んでね。")
        return

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)

    
    
    


view, cid = get_query_params()
enter_class = "enter-right" if view == "detail" else "enter-left"
st.markdown(f"<div class='page {enter_class}'>", unsafe_allow_html=True)

if view == "detail":
    render_detail_page(cid)
elif view == "compare":
     render_compare_page()
else:
    render_list_page()

st.markdown("</div>", unsafe_allow_html=True)
