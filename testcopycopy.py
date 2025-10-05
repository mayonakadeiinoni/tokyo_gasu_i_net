# app.py
import streamlit as st

# ページ設定
st.set_page_config(page_title="選挙候補者情報システム", layout="wide")

# CSS：スライド＋フェードアニメーション
st.markdown("""
<style>
@keyframes slideIn {
  0% {opacity: 0; transform: translateX(50px);}
  100% {opacity: 1; transform: translateX(0);}
}
.view {
  animation: slideIn 0.4s ease;
}
.candidate-card {
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 15px;
  background: #fff;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# データ
candidates = [
    {"id": 1, "name": "佐藤 太郎", "party": "自民党", "policy": "経済再生・農業振興"},
    {"id": 2, "name": "鈴木 花子", "party": "立憲民主党", "policy": "子育て支援・教育改革"},
    {"id": 3, "name": "田中 一郎", "party": "公明党", "policy": "福祉強化・中小企業支援"},
]

# クエリ取得
query_params = st.query_params
view = query_params.get("view", ["list"])[0]
id_param = query_params.get("id", [None])[0]

# 一覧ページ
if view == "list":
    st.markdown('<div class="view">', unsafe_allow_html=True)
    st.header("📊 候補者一覧")
    for c in candidates:
        st.markdown(f"""
        <div class="candidate-card">
            <h4>{c["name"]}</h4>
            <p>{c["party"]}｜{c["policy"]}</p>
            <button onclick="window.location.search='?view=detail&id={c["id"]}'">
                詳細を見る
            </button>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 詳細ページ
elif view == "detail" and id_param:
    cand = next((x for x in candidates if str(x["id"]) == id_param), None)
    if cand:
        st.markdown('<div class="view">', unsafe_allow_html=True)
        st.header(f"🧑‍💼 {cand['name']} の詳細情報")
        st.write(f"所属政党：{cand['party']}")
        st.write(f"重点政策：{cand['policy']}")
        if st.button("← 一覧に戻る"):
            st.query_params["view"] = "list"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
