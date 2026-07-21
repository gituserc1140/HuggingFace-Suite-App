import html
import os

import requests
import streamlit as st

HF_API_URL = "https://api-inference.huggingface.co/models/"

GITHUB_REPO_URL = "https://github.com/gituserc1140/HuggingFace-Suite-App"
GITHUB_SPONSORS_URL = "https://github.com/sponsors/gituserc1140"

_CSS = """
<style>
/* ── Page background ───────────────────────────────────────────── */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}
[data-testid="stHeader"] { background: transparent; }

/* ── Hero banner ───────────────────────────────────────────────── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.2rem;
}
.hero h1 {
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(90deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
}
.hero p {
    color: #cbd5e1;
    font-size: 1.05rem;
    margin-top: 0;
}

/* ── Social buttons row ────────────────────────────────────────── */
.social-buttons {
    display: flex;
    justify-content: center;
    gap: 0.8rem;
    flex-wrap: wrap;
    margin-bottom: 1.6rem;
}
.social-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.4rem 1.1rem;
    border-radius: 8px;
    font-size: 0.9rem;
    font-weight: 600;
    text-decoration: none !important;
    transition: opacity 0.2s;
}
.social-btn:hover { opacity: 0.82; }
.btn-github {
    background: #24292e;
    color: #fff !important;
    border: 1px solid rgba(255,255,255,0.15);
}
.btn-sponsor {
    background: linear-gradient(135deg, #db61a2, #ea4aaa);
    color: #fff !important;
    border: none;
}

/* ── Tab bar ───────────────────────────────────────────────────── */
[data-testid="stTabs"] [role="tablist"] {
    gap: 0.5rem;
    border-bottom: 2px solid #3730a3;
}
[data-testid="stTabs"] [role="tab"] {
    background: rgba(255,255,255,0.05);
    border-radius: 10px 10px 0 0;
    padding: 0.5rem 1.2rem;
    color: #a5b4fc !important;
    font-weight: 600;
    border: none;
    transition: background 0.2s;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #6d28d9, #3b82f6);
    color: #fff !important;
}

/* ── Result card ───────────────────────────────────────────────── */
.result-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(167,139,250,0.35);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    color: #e2e8f0;
    font-size: 1rem;
    line-height: 1.7;
    white-space: pre-wrap;
    word-break: break-word;
    margin-top: 1rem;
}
.result-label {
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #a78bfa;
    margin-bottom: 0.4rem;
}

/* ── Error card ────────────────────────────────────────────────── */
.error-card {
    background: rgba(239,68,68,0.12);
    border: 1px solid rgba(239,68,68,0.45);
    border-radius: 14px;
    padding: 1.2rem 1.6rem;
    color: #fca5a5;
    font-size: 0.97rem;
    margin-top: 1rem;
}

/* ── Buttons ───────────────────────────────────────────────────── */
[data-testid="stButton"] button {
    background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.45rem 1.2rem !important;
    font-weight: 600 !important;
    transition: opacity 0.2s !important;
}
[data-testid="stButton"] button:hover { opacity: 0.85 !important; }

/* ── Sidebar ───────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: rgba(15,12,41,0.85);
    border-right: 1px solid rgba(167,139,250,0.2);
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div { color: #cbd5e1 !important; }
[data-testid="stSidebar"] h2 {
    color: #a78bfa !important;
    font-size: 1.1rem;
}

/* ── Alert / Warning ───────────────────────────────────────────── */
[data-testid="stAlert"] p { color: #ffffff !important; }
[data-testid="stSpinner"] p { color: #a5b4fc !important; }
</style>
"""


def get_configured_api_key() -> str:
    if "HUGGINGFACE_API_KEY" in st.secrets:
        return st.secrets["HUGGINGFACE_API_KEY"]
    return os.getenv("HUGGINGFACE_API_KEY", "")


def hf_post(model: str, payload: dict, api_key: str) -> dict:
    headers = {"Authorization": "Bearer " + api_key}
    try:
        response = requests.post(
            f"{HF_API_URL}{model}",
            headers=headers,
            json=payload,
            timeout=60,
        )
        try:
            data = response.json()
        except ValueError:
            data = response.text
        return {"status": response.status_code, "data": data}
    except requests.exceptions.ConnectionError:
        return {"status": 0, "data": "Connection error – check your network connection and API key."}
    except requests.exceptions.Timeout:
        return {"status": 0, "data": "Request timed out. The model may be loading; please try again in a moment."}
    except requests.exceptions.RequestException as exc:
        return {"status": 0, "data": str(exc)}


def show_result(text: str) -> None:
    st.markdown('<div class="result-label">✅ Result</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="result-card">{html.escape(str(text))}</div>',
        unsafe_allow_html=True,
    )


def show_error(message: str) -> None:
    st.markdown(
        f'<div class="error-card">⚠️ {html.escape(str(message))}</div>',
        unsafe_allow_html=True,
    )


def tab_sentiment(api_key: str) -> None:
    st.markdown("Classify the **sentiment** of any text (positive / negative).")
    text = st.text_area("Enter text:", "I absolutely love this product!", key="sa_input")
    if st.button("Analyse Sentiment", key="sa_btn"):
        if not text.strip():
            st.warning("Please enter some text first.")
            return
        with st.spinner("Analysing…"):
            result = hf_post(
                "distilbert-base-uncased-finetuned-sst-2-english",
                {"inputs": text},
                api_key,
            )
        if result["status"] == 200:
            data = result["data"]
            if isinstance(data, list) and data:
                top = data[0]
                if isinstance(top, list):
                    top = top[0]
                label = top.get("label", "N/A")
                score = top.get("score", 0)
                show_result(f"{label} (confidence: {score:.1%})")
            else:
                show_result(str(data))
        else:
            show_error(f"API error {result['status']}: {result['data']}")


def tab_generation(api_key: str) -> None:
    st.markdown("Continue a prompt with **text generation** using GPT-2.")
    prompt = st.text_area("Enter a prompt:", "Once upon a time in a galaxy far away,", key="gen_input")
    max_tokens = st.slider("Max new tokens", 20, 200, 80, key="gen_tokens")
    if st.button("Generate Text", key="gen_btn"):
        if not prompt.strip():
            st.warning("Please enter a prompt first.")
            return
        with st.spinner("Generating…"):
            result = hf_post(
                "gpt2",
                {"inputs": prompt, "parameters": {"max_new_tokens": max_tokens}},
                api_key,
            )
        if result["status"] == 200:
            data = result["data"]
            generated = data[0].get("generated_text", str(data)) if isinstance(data, list) else str(data)
            show_result(generated)
        else:
            show_error(f"API error {result['status']}: {result['data']}")


def tab_summarization(api_key: str) -> None:
    st.markdown("Generate a concise **summary** of a longer passage.")
    article = st.text_area(
        "Paste your article or text:",
        (
            "The Amazon rainforest, also known as Amazonia, is a moist broadleaf tropical rainforest "
            "in the Amazon biome that covers most of the Amazon basin of South America. "
            "This basin encompasses 7,000,000 km2 (2,700,000 sq mi), of which "
            "5,500,000 km2 (2,100,000 sq mi) are covered by the rainforest. "
            "This region includes territory belonging to nine nations and 3,344 formally acknowledged "
            "indigenous territories."
        ),
        height=180,
        key="sum_input",
    )
    if st.button("Summarise", key="sum_btn"):
        if not article.strip():
            st.warning("Please paste some text first.")
            return
        with st.spinner("Summarising…"):
            result = hf_post(
                "facebook/bart-large-cnn",
                {"inputs": article},
                api_key,
            )
        if result["status"] == 200:
            data = result["data"]
            summary = data[0].get("summary_text", str(data)) if isinstance(data, list) else str(data)
            show_result(summary)
        else:
            show_error(f"API error {result['status']}: {result['data']}")


def tab_translation(api_key: str) -> None:
    st.markdown("Translate text **from English to French** using Helsinki-NLP.")
    text = st.text_area("Enter English text:", "Hello, how are you today?", key="tr_input")
    if st.button("Translate", key="tr_btn"):
        if not text.strip():
            st.warning("Please enter some text first.")
            return
        with st.spinner("Translating…"):
            result = hf_post(
                "Helsinki-NLP/opus-mt-en-fr",
                {"inputs": text},
                api_key,
            )
        if result["status"] == 200:
            data = result["data"]
            translation = (
                data[0].get("translation_text", str(data)) if isinstance(data, list) else str(data)
            )
            show_result(translation)
        else:
            show_error(f"API error {result['status']}: {result['data']}")


def tab_qa(api_key: str) -> None:
    st.markdown("Ask a **question** about a passage of text.")
    context = st.text_area(
        "Context (the passage to search):",
        (
            "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France. "
            "It is named after the engineer Gustave Eiffel, whose company designed and built the tower "
            "from 1887 to 1889 as the entrance arch for the 1889 World's Fair."
        ),
        height=140,
        key="qa_context",
    )
    question = st.text_input("Your question:", "When was the Eiffel Tower built?", key="qa_question")
    if st.button("Get Answer", key="qa_btn"):
        if not context.strip() or not question.strip():
            st.warning("Please provide both a context and a question.")
            return
        with st.spinner("Finding answer…"):
            result = hf_post(
                "deepset/roberta-base-squad2",
                {"inputs": {"question": question, "context": context}},
                api_key,
            )
        if result["status"] == 200:
            data = result["data"]
            answer = data.get("answer", str(data)) if isinstance(data, dict) else str(data)
            show_result(answer)
        else:
            show_error(f"API error {result['status']}: {result['data']}")


def main() -> None:
    st.set_page_config(
        page_title="HuggingFace Suite App",
        page_icon="🤗",
        layout="centered",
    )
    st.markdown(_CSS, unsafe_allow_html=True)

    # ── Hero ───────────────────────────────────────────────────────
    st.markdown(
        """
        <div class="hero">
            <h1>🤗 HuggingFace Suite</h1>
            <p>A collection of NLP tools powered by the Hugging Face Inference API.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Social buttons ─────────────────────────────────────────────
    st.markdown(
        f"""
        <div class="social-buttons">
            <a class="social-btn btn-github" href="{GITHUB_REPO_URL}" target="_blank" rel="noopener">
                &#11088; GitHub
            </a>
            <a class="social-btn btn-sponsor" href="{GITHUB_SPONSORS_URL}" target="_blank" rel="noopener">
                &#10084;&#65039; Sponsor
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Sidebar ────────────────────────────────────────────────────
    st.sidebar.header("Settings")
    api_key_input = st.sidebar.text_input(
        "Hugging Face API Key",
        type="password",
        help=(
            "Paste your Hugging Face API key here. "
            "You can also set it via the HUGGINGFACE_API_KEY environment variable "
            "or Streamlit secrets."
        ),
    )
    st.sidebar.markdown(
        "Get a free key at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).",
    )

    stripped = api_key_input.strip()
    api_key = stripped if stripped else get_configured_api_key()

    if not api_key:
        st.warning(
            "Please enter your Hugging Face API key in the sidebar to get started.",
        )
        st.stop()

    # ── Task tabs ──────────────────────────────────────────────────
    tabs = st.tabs(["😊 Sentiment", "✍️ Generation", "📝 Summarise", "🌐 Translate", "❓ Q&A"])

    with tabs[0]:
        tab_sentiment(api_key)
    with tabs[1]:
        tab_generation(api_key)
    with tabs[2]:
        tab_summarization(api_key)
    with tabs[3]:
        tab_translation(api_key)
    with tabs[4]:
        tab_qa(api_key)


if __name__ == "__main__":
    main()
