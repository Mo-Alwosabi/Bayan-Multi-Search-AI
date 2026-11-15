import datetime
import time
from threading import Thread
import streamlit as st
from main import graph, llm

st.set_page_config(
    page_title="بيان AI | Bayan Multi-Search Intelligence",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# Cyber-Cyan & Deep Indigo RTL Theme (Mohammed Alwosabi)
# ============================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Cairo', system-ui, -apple-system, sans-serif;
        direction: rtl;
        text-align: right;
    }

    .stApp {
        background: radial-gradient(circle at top right, #0f172a 0%, #060913 55%, #030712 100%);
        color: #f1f5f9;
    }

    .bayan-hero {
        background: linear-gradient(135deg, rgba(12, 20, 40, 0.95) 0%, rgba(22, 34, 68, 0.85) 100%);
        border: 1px solid rgba(56, 189, 248, 0.28);
        border-radius: 18px;
        padding: 1.8rem 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 12px 40px -10px rgba(56, 189, 248, 0.18);
    }

    .bayan-badge {
        display: inline-block;
        background: rgba(56, 189, 248, 0.14);
        border: 1px solid rgba(56, 189, 248, 0.4);
        color: #7dd3fc;
        padding: 0.25rem 0.85rem;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }

    .bayan-title {
        font-size: 2.1rem;
        font-weight: 900;
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 0.4rem 0;
    }

    .bayan-subtitle {
        color: #cbd5e1;
        font-size: 1.02rem;
        margin: 0;
    }

    .bayan-card {
        background: rgba(12, 20, 40, 0.88);
        border: 1px solid rgba(129, 140, 248, 0.24);
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
    }

    .score-high {
        background: rgba(56, 189, 248, 0.15);
        border-right: 4px solid #38bdf8;
        padding: 0.55rem 0.9rem;
        border-radius: 8px;
        color: #e0f2fe;
        margin-bottom: 0.5rem;
    }

    .score-mid {
        background: rgba(129, 140, 248, 0.15);
        border-right: 4px solid #818cf8;
        padding: 0.55rem 0.9rem;
        border-radius: 8px;
        color: #e0e7ff;
        margin-bottom: 0.5rem;
    }

    .score-low {
        background: rgba(244, 63, 94, 0.14);
        border-right: 4px solid #fb7185;
        padding: 0.55rem 0.9rem;
        border-radius: 8px;
        color: #ffe4e6;
        margin-bottom: 0.5rem;
    }

    .bayan-footer {
        margin-top: 2.5rem;
        padding-top: 1.2rem;
        border-top: 1px solid rgba(56, 189, 248, 0.18);
        text-align: center;
        color: #94a3b8;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Sidebar: System Architecture & Engineer Attribution
# ============================================================
with st.sidebar:
    st.markdown("### ⚡ منظومة بيان AI")
    st.caption("Bayan Multi-Search Intelligence Engine")
    st.markdown("---")
    st.markdown(
        """
        **مصادر الاسترجاع المتوازية:**
        - 🌐 **Google SERP** — نتائج الويب الموثوقة
        - 🔷 **Bing SERP** — تغطية بحثية مكمّلة
        - 💬 **Reddit Communities** — تجارب ونقاشات حقيقية
        """
    )
    st.markdown("---")
    st.markdown(
        """
        **تطوير وهندسة:**  
        **محمد الوصابي (Mohammed Alwosabi)**  
        *AI & ML Systems Engineer*  
        [GitHub @Mo-Alwosabi](https://github.com/Mo-Alwosabi)
        """
    )

# ============================================================
# Hero Banner
# ============================================================
st.markdown(
    """
    <div class="bayan-hero">
        <div class="bayan-badge">● LangGraph 9-Node Multi-Source Pipeline</div>
        <h1 class="bayan-title">بيان AI — محرك البحث والتحليل متعدد المصادر</h1>
        <p class="bayan-subtitle">
            تنفيذ استعلامات متوازية عبر Google و Bing و Reddit، مع تحليل مستقل لكل مصدر ودمج معرفي ذكي في إجابة موحّدة وموثّقة.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

user_question = st.text_input(
    "اكتب سؤالك أو موضوع البحث هنا:",
    placeholder="مثال: ما هي أفضل معماريات RAG المحلية لتشغيلها على GPU بسعة 8GB VRAM؟",
)


def highlight_score_class(score_text: str) -> str:
    try:
        score = float(str(score_text).strip())
    except Exception:
        score = 5.0
    if score >= 7:
        return "score-high"
    if score >= 4:
        return "score-mid"
    return "score-low"


def safe_score(text: str) -> float:
    try:
        raw = llm.invoke([{"role": "user", "content": f"قيم هذه النتيجة من 0-10 برقم فقط: {text}"}]).content
        return float(str(raw).strip().split()[0])
    except Exception:
        return 5.0


def get_insight(text: str) -> str:
    messages = [{"role": "user", "content": f"اعطيني Insight سريع ومهم لهذه النتيجة: {text}"}]
    return llm.invoke(messages).content


def get_summary(results: list, source_name: str) -> str:
    content = "\n".join(str(r) for r in results)
    messages = [{"role": "user", "content": f"اعطني ملخص شامل ومختصر لمصدر {source_name}: {content}"}]
    return llm.invoke(messages).content


if user_question.strip():
    st.info("🔎 جاري تشغيل وكلاء البحث المتوازيين عبر Google و Bing و Reddit...")

    initial_state = {
        "messages": [{"role": "user", "content": user_question}],
        "user_question": user_question,
        "google_results": None,
        "bing_results": None,
        "reddit_results": None,
        "selected_reddit_urls": None,
        "reddit_post_data": None,
        "google_analysis": None,
        "bing_analysis": None,
        "reddit_analysis": None,
        "final_answer": None,
    }

    col1, col2, col3 = st.columns(3)
    with col1:
        google_progress = st.progress(0, text="Google SERP: 0%")
    with col2:
        bing_progress = st.progress(0, text="Bing SERP: 0%")
    with col3:
        reddit_progress = st.progress(0, text="Reddit Communities: 0%")

    result_box: dict = {}

    def run_graph(state_payload: dict) -> None:
        try:
            result_box["state"] = graph.invoke(state_payload)
        except Exception as exc:
            result_box["error"] = str(exc)

    thread = Thread(target=run_graph, args=(initial_state,))
    thread.start()

    for i in range(0, 101, 10):
        google_progress.progress(i, text=f"Google SERP: {i}%")
        bing_progress.progress(i, text=f"Bing SERP: {i}%")
        reddit_progress.progress(i, text=f"Reddit Communities: {i}%")
        time.sleep(0.15)

    thread.join()
    google_progress.empty()
    bing_progress.empty()
    reddit_progress.empty()

    if "error" in result_box:
        st.error(f"تعذر إتمام البحث: {result_box['error']}")
    else:
        final_state = result_box.get("state", {})
        col_google, col_bing = st.columns(2)

        with col_google:
            st.subheader("🌐 تحليلات Google SERP")
            google_results = final_state.get("google_results") or []
            if google_results:
                scored_google = sorted(
                    [(r, safe_score(r)) for r in google_results],
                    key=lambda item: item[1],
                    reverse=True,
                )
                google_summary = get_summary([r for r, _ in scored_google], "Google")
                st.markdown(f"**📝 ملخص Google:** {google_summary}")
                for idx, (result, score) in enumerate(scored_google, 1):
                    css_cls = highlight_score_class(str(score))
                    st.markdown(
                        f"<div class='{css_cls}'><b>النتيجة {idx} (التقييم: {score}/10)</b></div>",
                        unsafe_allow_html=True,
                    )
                    with st.expander(f"🔹 تفاصيل ورؤية النتيجة {idx}"):
                        st.write("🔹 النتيجة:", result)
                        st.write("💡 Insight:", get_insight(str(result)))
            else:
                st.caption("لم يتم إرجاع نتائج إضافية من Google.")

        with col_bing:
            st.subheader("🔷 تحليلات Bing SERP")
            bing_results = final_state.get("bing_results") or []
            if bing_results:
                scored_bing = sorted(
                    [(r, safe_score(r)) for r in bing_results],
                    key=lambda item: item[1],
                    reverse=True,
                )
                bing_summary = get_summary([r for r, _ in scored_bing], "Bing")
                st.markdown(f"**📝 ملخص Bing:** {bing_summary}")
                for idx, (result, score) in enumerate(scored_bing, 1):
                    css_cls = highlight_score_class(str(score))
                    st.markdown(
                        f"<div class='{css_cls}'><b>النتيجة {idx} (التقييم: {score}/10)</b></div>",
                        unsafe_allow_html=True,
                    )
                    with st.expander(f"🔹 تفاصيل ورؤية النتيجة {idx}"):
                        st.write("🔹 النتيجة:", result)
                        st.write("💡 Insight:", get_insight(str(result)))
            else:
                st.caption("لم يتم إرجاع نتائج إضافية من Bing.")

        st.markdown("---")
        st.subheader("💡 الإجابة النهائية الموحّدة — بيان AI")
        synthesized = final_state.get("final_answer")
        if synthesized:
            st.markdown(f"<div class='bayan-card'>{synthesized}</div>", unsafe_allow_html=True)
            filename_txt = f"bayan_answer_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            st.download_button(
                "💾 تحميل الإجابة النهائية (TXT)",
                synthesized,
                file_name=filename_txt,
                mime="text/plain",
            )
        else:
            st.warning("لم يتم توليد إجابة نهائية بعد.")

st.markdown(
    """
    <div class="bayan-footer">
        <strong>بيان AI (Bayan Multi-Search AI)</strong> | محرك البحث والتحليل متعدد الوكلاء<br/>
        تم التطوير والهندسة بواسطة <strong>محمد الوصابي (Mohammed Alwosabi)</strong> • AI & ML Systems Engineer
    </div>
    """,
    unsafe_allow_html=True,
)
