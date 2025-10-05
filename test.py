# -*- coding: utf-8 -*-
# 📊 選挙候補者情報システム（Streamlit版・疑似画面遷移付き）

from __future__ import annotations
import streamlit as st
from typing import List, Dict, Any
from pathlib import Path
import base64
import re, html, unicodedata
from textwrap import dedent
from collections import Counter
import pandas as pd

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
/* ===== ベース ===== */
.stApp {
  background: linear-gradient(135deg, #ECECFF 0%, #F8F8FF 100%);
  font-family: -apple-system, BlinkMacSystemFont, "Hiragino Sans", "Yu Gothic", "Noto Sans JP", sans-serif;
}

/* ---- 「上の白帯と重なる」対策：上パディングを確保 ---- */
.block-container{
  max-width: 1080px;
  margin-left:auto; margin-right:auto;
  padding: 28px 16px 0;   /* ← 上に余白を足す */
}
.app-header, .chips, .detail-card{ max-width: 880px; margin-left:auto; margin-right:auto; }

/* ヘッダー */
.app-header { color:#4a4a6a; margin: 6px 0 18px; }
.app-header h1 { font-size:2.0rem; margin-bottom:.2rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }
.app-header .subtitle { font-size:1rem; opacity:.9; }

/* ヘッダーは左・中央・右の3列。中央見出しは常に真正面 */
.header-row{ display:grid; grid-template-columns: 1fr auto 1fr; align-items:center; }
.header-center{ text-align:center; }
.header-right{ justify-self:end; }

/* 地域バッジ */
.region-badge{
  display:inline-block; padding:6px 12px; border-radius:999px;
  background:#eef2ff; color:#334155; border:1px solid #c7d2fe;
  font-weight:700; white-space:nowrap; box-shadow:0 1px 2px rgba(0,0,0,.06);
}
.region-note{ font-size:.85em; color:#64748b; margin-left:.4em; }

/* 画面コンテナ & アニメーション */
.page { background: transparent; }
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

/* ===== フィルタ行の見た目・揃え ===== */
.filters .stSelectbox > label,
.filters .stTextInput > label{ margin-bottom:6px; }
.filters .clear-col .stButton>button{ width:100%; } /* 幅を検索欄に揃える */

/* フィルタ表示（チップ）*/
.chips { display:flex; gap:8px; flex-wrap:wrap; align-items:center; background:#f8f9ff; border-radius:8px; padding:8px 12px; }
.chip-label { font-weight:700; color:#666; margin-right:4px; }
.chip { display:inline-flex; align-items:center; gap:6px; background:white; padding:6px 12px; border-radius:20px; font-size:.85em; color:#333; 
        box-shadow: 0 2px 4px rgba(0,0,0,.08); }

/* ===== 候補者カード（高さを揃える） ===== */
.candidate-card {
  background:white; border-radius:16px; padding:16px; text-align:center;
  box-shadow: 0 4px 12px rgba(0,0,0,.08);
  transition: transform .2s ease, box-shadow .2s ease, border .2s ease;
  border: 2px solid transparent;
  display:flex; flex-direction:column;
  min-height: 360px;      /* ★ カードの最小高を固定 */
}
.candidate-card:hover { transform: translateY(-6px); box-shadow: 0 8px 24px rgba(0,0,0,.12); }
.candidate-card.selected { border: 3px solid #667eea; box-shadow: 0 8px 24px rgba(102,126,234,.3); }

.candidate-photo { width:120px; height:120px; border-radius:50%; margin: 0 auto 12px; display:flex; align-items:center; justify-content:center; 
  color:white; font-size:2.4rem; font-weight:700; box-shadow: 0 5px 15px rgba(0,0,0,.2); border: 3px solid; overflow:hidden; position:relative; }
.candidate-name { font-size:1.1rem; font-weight:700; color:#333; margin-bottom:6px; min-height:1.4em; }
.candidate-tags { font-size:.85rem; color:#888; margin-bottom:8px; display:flex; gap:8px; justify-content:center; flex-wrap:wrap; min-height:1.6em; }
.tag { background:#f0f0f0; padding:3px 8px; border-radius:4px; white-space:nowrap; }
.candidate-party { display:inline-block; padding: 4px 12px; border-radius: 20px; font-size:.9rem; margin-bottom:8px; font-weight:700; border: 2px solid; }
.party-icon { margin-right:6px; font-size:1.1em; }

/* ブリーフは 3 行で省略（高さをそろえる） */
.candidate-brief {
  font-size:.9rem; color:#777; line-height:1.5;
  display:-webkit-box; -webkit-line-clamp:3; -webkit-box-orient: vertical;
  overflow:hidden; min-height: calc(1.5em * 3);
}

/* カード内のアクション（詳細を見る）を下に固定 */
.card-actions { margin-top:auto; }
.card-actions .btn {
  display:block; width:100%; text-align:center;
  padding:10px 12px; border-radius:8px; border:1px solid #e2e8f0;
  background:#fff; font-weight:700; box-shadow: 0 1px 2px rgba(0,0,0,.05);
  text-decoration:none; color:#334155;
}
.card-actions .btn:hover{ background:#f8fafc; }

/* 詳細カード（モーダル相当）*/
.detail-card { background:white; border-radius:16px; padding:24px; box-shadow: 0 8px 32px rgba(0,0,0,.15); }
.detail-header { text-align:center; padding-bottom:12px; border-bottom: 2px solid #f0f0f0; margin-bottom:16px; }
.modal-photo { width:150px; height:150px; border-radius:50%; margin: 0 auto 12px; display:flex; align-items:center; justify-content:center; 
  color:white; font-size:3rem; font-weight:700; box-shadow: 0 10px 25px rgba(0,0,0,.2); border: 4px solid; overflow:hidden; position:relative; }
.section-title { font-size:1.2rem; font-weight:700; color:#667eea; margin: 16px 0 8px; padding-left: 12px; border-left: 4px solid #667eea; }
.manifesto-list { list-style:none; padding-left:0; margin:0; }
.manifesto-list li { padding:12px; margin: 0 0 10px; background:#f8f9ff; border-left: 4px solid #667eea; border-radius:5px; }
.candidate-photo img,.modal-photo img{ width:100%; height:100%; object-fit:cover; display:block; }

/* 主なスタンス 表 */
.stance-table{ width:100%; border-collapse:collapse; margin-top:8px; font-size:14px; }
.stance-table th, .stance-table td{ padding:10px 12px; border-top:1px solid #eee; vertical-align:middle; text-align:center; }
.stance-table th{ width:60%; color:#333; font-weight:600; }

/* バッジ */
.stance-badge{ display:inline-block; padding:8px 16px; border-radius:999px; font-weight:700; line-height:1.25; letter-spacing:.02em; box-shadow:inset 0 0 0 1px rgba(0,0,0,.05); white-space:nowrap; }
@media (min-width: 900px){ .stance-badge{ font-size:1.15rem; padding:10px 18px; } }
.stance-badge.pro{      background:#e6f4ea; color:#137333; }
.stance-badge.partial1{ background:#fff7e5; color:#8a6d1d; }
.stance-badge.neutral{  background:#f1f3f4; color:#3c4043; }
.stance-badge.partial2{ background:#fff3e0; color:#8a6d1d; }
.stance-badge.con{      background:#fce8e6; color:#c5221f; }
.stance-badge.unknown{  background:#e8f0fe; color:#1967d2; }

.stance-legend{ margin-top:4px; font-size:12px; color:#666; display:flex; gap:8px; flex-wrap:wrap; justify-content:center; }

/* 政党カラー */
.photo-自民党  { background: linear-gradient(135deg, #3d94c3 0%, #2b7a9e 100%); border-color:#236680; }
.party-自民党  { background:#e8f4f8; color:#2b7a9e; border-color:#2b7a9e; }

.photo-民主党  { background: linear-gradient(135deg, #e89060 0%, #d77840 100%); border-color:#b8623a; }
.party-民主党  { background:#fff5ed; color:#d77840; border-color:#d77840; }

.photo-立憲民主党{ background: linear-gradient(135deg, #9a5fb8 0%, #7d4a9a 100%); border-color:#603b7a; }
.party-立憲民主党{ background:#f5eef8; color:#7d4a9a; border-color:#7d4a9a; }

/* 互換（旧名称） */
.photo-立憲社会党{ background: linear-gradient(135deg, #9a5fb8 0%, #7d4a9a 100%); border-color:#603b7a; }
.party-立憲社会党{ background:#f5eef8; color:#7d4a9a; border-color:#7d4a9a; }

.photo-社民党  { background: linear-gradient(135deg, #55a563 0%, #3d8b4a 100%); border-color:#2e6b38; }
.party-社民党  { background:#eef8f0; color:#3d8b4a; border-color:#3d8b4a; }

.photo-共産党  { background: linear-gradient(135deg, #e66b6b 0%, #c83e3e 100%); border-color:#a83232; }
.party-共産党  { background:#fdeaea; color:#c83e3e; border-color:#c83e3e; }

.photo-社会党  { background: linear-gradient(135deg, #4F8FCB 0%, #2E6FA6 100%); border-color:#2E6FA6; }
.party-社会党  { background:#e8f1fb; color:#2E6FA6; border-color:#2E6FA6; }

.photo-無所属  { background: linear-gradient(135deg, #616161 0%, #424242 100%); border-color:#212121; }
.party-無所属  { background:#f5f5f5; color:#424242; border-color:#757575; }

/* 党アイコンの画像サイズ */
.party-icon img{ width:1.15em; height:1.15em; object-fit:contain; vertical-align:-0.18em; display:inline-block; }
</style>
""",
    unsafe_allow_html=True,
)

from data import candidates
CANDIDATES: List[Dict[str, Any]] = candidates

# ---------- 地域（region）: 正規化 & 多数派検出 ----------
def _norm_region(s: str) -> str:
    s = unicodedata.normalize("NFKC", s or "")
    s = re.sub(r"\s+", "", s)
    s = s.replace("東京都", "東京")
    return s

def _detect_common_region(cands: List[Dict[str, Any]]):
    regs = [_norm_region(c.get("region","")) for c in cands if c.get("region")]
    if not regs: return None, 0
    cnt = Counter(regs)
    top, n_top = cnt.most_common(1)[0]
    others = sum(cnt.values()) - n_top
    return top, others

REGION, REGION_OTHERS = _detect_common_region(CANDIDATES)

# ===== スタンス定義 =====
TOPIC_ORDER = ["消費税増税", "夫婦別姓", "外国人参政権", "原発再稼働", "憲法改正", "同性婚"]

STANCE_CANON = {
    "賛成":"賛成","反対":"反対","一部賛成":"一部賛成","一部反対":"一部反対",
    "条件付き賛成":"一部賛成","条件付き反対":"一部反対","部分賛成":"一部賛成","部分反対":"一部反対",
    "どちらとも言えない":"中立","どちらともいえない":"中立","中立":"中立","保留":"中立",
    "不明":"未回答","わからない":"未回答","回答しない":"未回答","無回答":"未回答",
}
STANCE_META = {
    "賛成":     {"icon":"✅","class":"pro","desc":"基本的に賛成の立場"},
    "一部賛成": {"icon":"⚖️","class":"partial1","desc":"条件付き・一部賛成"},
    "中立":     {"icon":"➖","class":"neutral","desc":"賛否を明確にせず"},
    "一部反対": {"icon":"🤷‍♀️","class":"partial2","desc":"条件付き・一部反対"},
    "反対":     {"icon":"❌","class":"con","desc":"基本的に反対の立場"},
    "未回答":   {"icon":"❓","class":"unknown","desc":"情報が見つからない／未回答"},
}
def _normalize_stance(v: str) -> str:
    s = (v or "").strip()
    if not s: return "未回答"
    s2 = STANCE_CANON.get(s, s)
    return s2 if s2 in STANCE_META else "未回答"

# ---------- 党アイコン ----------
PARTY_ICON_DEFAULT = {
    "自民党":"🏛️","民主党":"👨‍👩‍👧","立憲民主党":"🏥","社民党":"🌿","共産党":"🗣️","社会党":"🏫","無所属":"🧭"
}

@st.cache_data(show_spinner=False)
def _data_uri_from_file(path: str) -> str:
    p = Path(path)
    if not p.exists(): return ""
    ext = p.suffix.lower()
    mime = "image/png" if ext == ".png" else ("image/jpeg" if ext in [".jpg",".jpeg"] else "image/png")
    b64 = base64.b64encode(p.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"

def set_party_icon_from_file(party: str, path: str):
    uri = _data_uri_from_file(path)
    if uri:
        PARTY_ICON_DEFAULT[party] = f'<img src="{uri}" alt="{party}">'
    else:
        st.warning(f"党アイコン画像が見つかりません: {path}")

set_party_icon_from_file("自民党", "zimin.png")
set_party_icon_from_file("民主党", "minsh.png")
set_party_icon_from_file("立憲民主党", "rikken.png")
set_party_icon_from_file("社民党", "shamin.png")

# ---------- 顔写真（自動割当） ----------
IMAGE_FILES = [
    "asano.png","kawarada.png","hiratuka.png","murakami.png","yanagisawa.png",
    "men1.png","men2.png","woman1.png","woman2.png","woman3.png",
]
IMG_URI = {fn: _data_uri_from_file(fn) for fn in IMAGE_FILES}

PHOTO_MAP_BY_ID = { 1:"asano.png", 2:"kawarada.png", 3:"hiratuka.png", 4:"murakami.png", 5:"woman1.png" }
PHOTO_MAP_BY_NAME = {
    "佐藤太郎":"asano.png","鈴木次郎":"kawarada.png","田中三郎":"hiratuka.png",
    "加藤花":"murakami.png","石原さくら":"woman1.png",
}

FEM_HINTS = ("子","美","花","華","さくら","桜","奈","香","莉","恵","江", "さやか", "みさき", "まりこ", "まい", "あい", "あかね")
MEN_POOL   = ["men1.png","men2.png"]
WOMEN_POOL = ["woman1.png","woman2.png","woman3.png"]

def _photo_uri_for(c: Dict[str, Any]) -> str | None:
    p = c.get("photo")
    if not p:
        p = PHOTO_MAP_BY_ID.get(c.get("id")) or PHOTO_MAP_BY_NAME.get(c.get("name"))
    if not p:
        name = c.get("name","")
        is_female = any(h in name for h in FEM_HINTS)
        pool = WOMEN_POOL if is_female else MEN_POOL
        seed = c.get("id") if isinstance(c.get("id"), int) else abs(hash(name))
        p = pool[seed % len(pool)]
    uri = IMG_URI.get(p)
    return uri if uri else None

# --------------------------------
# ルーティング補助
# --------------------------------
def _set_query_params(**params):
    try:
        st.query_params.clear()
        for k, v in params.items():
            if v is not None: st.query_params[k] = str(v)
    except Exception:
        st.experimental_set_query_params(**{k: str(v) for k, v in params.items() if v is not None})

def nav_to_list_clear():
    _set_query_params(view="list", clear="1"); st.rerun()

def consume_clear_if_needed():
    try:
        has_clear = "clear" in st.query_params
    except Exception:
        has_clear = "clear" in st.experimental_get_query_params()
    if has_clear:
        st.session_state["party_filter"]  = "すべて"
        st.session_state["policy_filter"] = "すべて"
        st.session_state["search_input"]  = ""
        st.session_state["selected_id"]   = None
        _set_query_params(view="list"); st.rerun()

def get_query_params():
    view, cid = "list", None
    try:
        qp = st.query_params
        view = qp.get("view","list"); cid = qp.get("id",None)
    except Exception:
        qp = st.experimental_get_query_params()
        view = qp.get("view",["list"])[0] if "view" in qp else "list"
        cid  = qp.get("id",[None])[0] if "id" in qp else None
    return view, cid

def nav_to(view: str, cid: int | None = None):
    try:
        st.query_params.clear(); st.query_params["view"] = view
        if cid is not None: st.query_params["id"] = str(cid)
    except Exception:
        if cid is not None: st.experimental_set_query_params(view=view, id=str(cid))
        else: st.experimental_set_query_params(view=view)
    st.rerun()

def get_party_icon(party: str, fallback: str | None) -> str:
    return fallback or PARTY_ICON_DEFAULT.get(party, "🏛️")

# --------------------------------
# フィルタ・検索
# --------------------------------
if "party_filter" not in st.session_state:  st.session_state.party_filter  = "すべて"
if "policy_filter" not in st.session_state: st.session_state.policy_filter = "すべて"
if "search_input" not in st.session_state:  st.session_state.search_input  = ""

def apply_filters(data: List[Dict[str, Any]], party: str, policy: str, search: str) -> List[Dict[str, Any]]:
    search = (search or "").strip()
    out = []
    for c in data:
        ok_party  = (party == "すべて") or (c.get("party") == party)
        ok_policy = (policy == "すべて") or (c.get("keyPolicy") == policy)
        ok_search = (not search) or (search in c.get("name",""))
        if ok_party and ok_policy and ok_search: out.append(c)
    return out

# --------------------------------
# コンポーネント描画
# --------------------------------
def render_header():
    if REGION:
        note = f"<span class='region-note'>※表記差 {REGION_OTHERS} 件</span>" if REGION_OTHERS>0 else ""
        region_badge = f"<span class='region-badge'>🗺 {html.escape(REGION)}{note}</span>"
    else:
        region_badge = ""
    st.markdown(dedent(f"""
    <div class="app-header">
      <div class="header-row">
        <div class="header-left"></div>
        <div class="header-center">
          <h1>選挙候補者情報システム</h1>
          <p class="subtitle">候補者の公約・政策を確認して、あなたの一票を決めましょう</p>
        </div>
        <div class="header-right">{region_badge}</div>
      </div>
    </div>
    """), unsafe_allow_html=True)

def candidate_card_html(c: Dict[str, Any]) -> str:
    party = c.get("party","無所属")
    photo_class = f"photo-{party}"
    party_class = f"party-{party}"
    name = c.get("name","")
    key_policy = c.get("keyPolicy","")
    brief = c.get("brief","")
    party_icon = get_party_icon(party, c.get("partyIcon"))
    photo_uri = _photo_uri_for(c)
    photo_html = f'<img src="{photo_uri}" alt="{html.escape(name)}">' if photo_uri else html.escape(c.get("initial",""))

    tags = []
    if key_policy: tags.append(f'<span class="tag">🎯 {html.escape(key_policy)}</span>')
    tags_html = "".join(tags)

    # ★ 詳細リンクをカード内に配置して高さを揃える
    return f"""
    <div class="candidate-card">
      <div>
        <div class="candidate-photo {photo_class}">{photo_html}</div>
        <div class="candidate-name">{html.escape(name)}</div>
        <div class="candidate-tags">{tags_html}</div>
        <div class="candidate-party {party_class}">
          <span class="party-icon">{party_icon}</span>{html.escape(party)}
        </div>
        <div class="candidate-brief">{html.escape(brief)}</div>
      </div>
      <div class="card-actions">
        <a class="btn" href="?view=detail&id={c.get('id')}">詳細を見る ➜</a>
      </div>
    </div>
    """

def detail_html(c: Dict[str, Any]) -> str:
    party = c.get("party","無所属")
    photo_class = f"photo-{party}"
    party_class = f"party-{party}"
    key_policy = c.get("keyPolicy","")
    brief = c.get("brief","")
    party_icon = get_party_icon(party, c.get("partyIcon"))
    initial = c.get("initial","")
    name = c.get("name","")
    career = c.get("career","")
    photo_uri = _photo_uri_for(c)
    photo_html = f'<img src="{photo_uri}" alt="{html.escape(name)}">' if photo_uri else html.escape(initial)

    # 公約: promise1..N を数字順に
    promises = []
    for k, v in c.items():
        if k.startswith("promise") and v:
            m = re.findall(r"\d+", k); num = int(m[0]) if m else 0
            promises.append((num, v))
    promises.sort(key=lambda t: t[0])
    manifesto_items = "\n".join([f"<li>{html.escape(v)}</li>" for _, v in promises])

    # 主なスタンス
    comparisons = c.get("comparisons", {}) or {}
    comparisons_html = ""
    if comparisons:
        def _order_key(topic: str) -> int:
            try: return TOPIC_ORDER.index(topic)
            except ValueError: return len(TOPIC_ORDER) + 1

        rows = []
        for topic, raw in sorted(comparisons.items(), key=lambda kv: _order_key(kv[0])):
            stance = _normalize_stance(raw)
            m = STANCE_META.get(stance, STANCE_META["未回答"])
            badge_class = m.get("class","unknown")
            badge_icon  = m.get("icon","❓")
            badge_desc  = html.escape(m.get("desc",""), quote=True)
            t = html.escape(topic); s = html.escape(stance)
            rows.append(
                f'<tr><th class="stance-topic">{t}</th>'
                f'<td class="stance-value"><span class="stance-badge {badge_class}" title="{badge_desc}">{badge_icon} {s}</span></td></tr>'
            )
        legend = ' '.join([
            '<span class="stance-badge pro">✅ 賛成</span>',
            '<span class="stance-badge partial1">⚖️ 一部賛成</span>',
            '<span class="stance-badge neutral">➖ 中立</span>',
            '<span class="stance-badge partial2">🤷‍♀️ 一部反対</span>',
            '<span class="stance-badge con">❌ 反対</span>',
            '<span class="stance-badge unknown">❓ 未回答</span>',
        ])
        comparisons_html = dedent(f"""
        <div class="section">
          <div class="section-title">📌 主なスタンス</div>
          <div class="stance-legend">{legend}</div>
          <table class="stance-table" aria-label="政策ごとの賛否一覧">
            <tbody>
              {'\n'.join(rows)}
            </tbody>
          </table>
        </div>
        """).strip()

    return dedent(f"""
    <div class="detail-card">
      <div class="detail-header">
        <div class="modal-photo {photo_class}">{photo_html}</div>
        <h2 style="margin:0 0 8px 0;">{html.escape(name)}</h2>
        <div class="candidate-party {party_class}" style="display:inline-block;">
          <span class="party-icon">{party_icon}</span>{html.escape(party)}
        </div>
      </div>
      <div class="section">
        <div class="section-title">📋 主な公約</div>
        <ul class="manifesto-list">{manifesto_items}</ul>
      </div>
      <div class="section">
        <div class="section-title">💼 経歴・実績</div>
        <div style="line-height:1.8; color:#555;">{html.escape(career)}</div>
      </div>
      {comparisons_html}
      <div class="section">
        <div class="section-title">🎯 重点政策</div>
        <p style="margin:0; font-weight:bold;">分野：{html.escape(key_policy)}</p>
        <div style="line-height:1.8; color:#555;">{html.escape(brief)}</div>
      </div>
    </div>
    """).strip()

# --------------------------------
# 一覧ページ
# --------------------------------
def render_list_page():
    render_header()
    consume_clear_if_needed()

    # ★ フィルタ行：入れ子の列で検索とクリアを横並びに
    st.markdown('<div class="filters">', unsafe_allow_html=True)
    fc1, fc2, fc34 = st.columns([1, 1, 3], gap="large")
    with fc1:
        party_options = ["すべて"] + sorted({c.get("party","無所属") for c in CANDIDATES})
        st.selectbox("政党", options=party_options, key="party_filter")
    with fc2:
        policy_options = ["すべて"] + sorted({c.get("keyPolicy","") for c in CANDIDATES if c.get("keyPolicy")})
        st.selectbox("政策テーマ", options=policy_options, key="policy_filter")
    with fc34:
        c3, c4 = st.columns([4, 1], gap="small")
        with c3:
            st.text_input("候補者名で検索", key="search_input", placeholder="例：田中 / 佐藤 など")
        with c4:
            st.markdown('<div class="clear-col">', unsafe_allow_html=True)
            if st.button("🧹 すべてクリア", use_container_width=True):
                nav_to_list_clear()
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # アクティブフィルタ（チップ）
    chips = []
    if st.session_state.party_filter != "すべて":
        chips.append(f"<span class='chip'>政党：{html.escape(st.session_state.party_filter)}</span>")
    if st.session_state.policy_filter != "すべて":
        chips.append(f"<span class='chip'>政策：{html.escape(st.session_state.policy_filter)}</span>")
    if st.session_state.search_input.strip():
        chips.append(f"<span class='chip'>検索：『{html.escape(st.session_state.search_input.strip())}』</span>")
    if chips:
        st.markdown("<div class='chips'><span class='chip-label'>現在の条件：</span>" + "".join(chips) + "</div>", unsafe_allow_html=True)

    st.divider()

    # グリッド
    items = apply_filters(CANDIDATES, st.session_state.party_filter, st.session_state.policy_filter, st.session_state.search_input)
    if not items:
        st.info("該当する候補者が見つかりません。条件を調整してください。")
        return

    N_COLS = 4
    cols = st.columns(N_COLS, gap="large")
    for idx, c in enumerate(items):
        with cols[idx % N_COLS]:
            st.markdown(candidate_card_html(c), unsafe_allow_html=True)

    if st.button("比較する", key="go_compare", use_container_width=True):
        nav_to("compare")

# --------------------------------
# 詳細ページ
# --------------------------------
def render_detail_page(cid_str: str | None):
    render_header()

    bc1, bc2 = st.columns([1, 6])
    with bc1:
        if st.button("← 一覧へ戻る", use_container_width=True):
            _set_query_params(view="list"); st.rerun()
    with bc2:
        if st.button("🧹 すべてクリア", use_container_width=True):
            nav_to_list_clear()

    candidate = None
    try:
        cid = int(cid_str) if cid_str is not None else None
    except ValueError:
        cid = None
    if cid is not None:
        for c in CANDIDATES:
            if c["id"] == cid:
                candidate = c; break
    if not candidate:
        st.warning("対象の候補者が見つかりません。")
        return

    st.markdown(detail_html(candidate), unsafe_allow_html=True)

    same_party = [c for c in CANDIDATES if c.get("party")==candidate.get("party") and c["id"]!=candidate["id"]]
    if same_party:
        st.markdown("#### 同じ政党の候補者")
        cols = st.columns(min(4, len(same_party)), gap="large")
        for i, c in enumerate(same_party):
            with cols[i % len(cols)]:
                st.markdown(candidate_card_html(c), unsafe_allow_html=True)

# --------------------------------
# 比較ページ（簡易表）
# --------------------------------
def render_compare_page():
    render_header()
    st.subheader("候補者ごとの比較表")

    labels = [f"{c.get('name','')}（{c.get('party','無所属')}）" for c in CANDIDATES]
    label_to_obj = {labels[i]: CANDIDATES[i] for i in range(len(CANDIDATES))}

    selected = st.multiselect("比較したい候補者", options=labels, default=[])

    if st.button("← 一覧へ戻る", use_container_width=True):
        _set_query_params(view="list"); st.rerun()

    if not selected:
        st.info("候補者を1人以上選んでね。")
        return

    show_comparisons = st.checkbox("争点", value=True)
    show_promises    = st.checkbox("行いたい政策", value=False)
    show_career      = st.checkbox("基本情報", value=False)

    rows = []

    if show_career:
        row = {"項目": "年齢"}
        for label in selected: row[label] = label_to_obj[label].get("age","") or ""
        rows.append(row)

        row = {"項目": "経歴"}
        for label in selected: row[label] = label_to_obj[label].get("career","") or ""
        rows.append(row)

    if show_promises:
        row = {"項目": "重点政策"}
        for label in selected: row[label] = label_to_obj[label].get("keyPolicy","") or ""
        rows.append(row)

        row = {"項目": "政策説明"}
        for label in selected: row[label] = label_to_obj[label].get("brief","") or ""
        rows.append(row)

        PROMISE_MAX = 4
        for i in range(1, PROMISE_MAX + 1):
            key = f"promise{i}"
            row = {"項目": f"📋 公約{i}"}
            for label in selected: row[label] = label_to_obj[label].get(key,"") or ""
            rows.append(row)

    if show_comparisons:
        topics, seen = [], set()
        for label in selected:
            for t in (label_to_obj[label].get("comparisons") or {}).keys():
                if t not in seen: seen.add(t); topics.append(t)
        for t in topics:
            row = {"項目": f"⚖️ {t}"}
            for label in selected:
                stance = (label_to_obj[label].get("comparisons") or {}).get(t,"")
                row[label] = stance
            rows.append(row)

    if not rows:
        st.info("上のチェックボックスで出したい“かたまり”を選んでね。")
        return

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)

# --------------------------------
# ルーティング
# --------------------------------
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
