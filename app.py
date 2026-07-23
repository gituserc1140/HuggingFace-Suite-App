import html
import os

import streamlit as st
from huggingface_hub import InferenceClient
from huggingface_hub.errors import HfHubHTTPError

GITHUB_REPO_URL = "https://github.com/gituserc1140/HuggingFace-Suite-App"
GITHUB_SPONSORS_URL = "https://github.com/sponsors/gituserc1140"
LOW_CONFIDENCE_THRESHOLD = 0.2
MAX_DISPLAYED_KEYWORDS = 15

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


@st.cache_resource
def make_client(api_key: str) -> InferenceClient:
    return InferenceClient(token=api_key)


def _handle_hf_error(exc: Exception) -> None:
    if isinstance(exc, HfHubHTTPError) and exc.response is not None:
        status = exc.response.status_code
        if status == 401:
            show_error("Authentication failed – please check your Hugging Face API key.")
            return
        if status == 403:
            show_error("Access forbidden – your API key may lack the required permissions.")
            return
        if status == 503:
            show_error("The model is still loading on the server. Please wait a moment and try again.")
            return
        show_error(f"API error {status}: {exc}")
        return
    show_error(str(exc))


def show_result(text: str) -> None:
    st.markdown('<div class="result-label">✅ Result</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="result-card">{html.escape(str(text))}</div>',
        unsafe_allow_html=True,
    )


def show_error(message: str) -> None:
    text = str(message).strip() or "An unexpected error occurred. Please try again."
    st.markdown(
        f'<div class="error-card">⚠️ {html.escape(text)}</div>',
        unsafe_allow_html=True,
    )


def tab_sentiment(api_key: str) -> None:
    st.markdown("Classify text by **sentiment** or **emotion**.")
    mode = st.selectbox(
        "Analysis mode",
        ["Positive / Negative", "Emotion labels"],
        key="sa_mode",
    )
    text = st.text_area("Enter text:", "I absolutely love this product!", key="sa_input")
    if st.button("Analyse Sentiment", key="sa_btn"):
        if not text.strip():
            st.warning("Please enter some text first.")
            return
        with st.spinner("Analysing…"):
            try:
                client = make_client(api_key)
                if mode == "Emotion labels":
                    model = "j-hartmann/emotion-english-distilroberta-base"
                else:
                    model = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
                results = client.text_classification(
                    text,
                    model=model,
                )
                top = results[0]
                show_result(f"{top.label} (confidence: {top.score:.1%})")
            except Exception as exc:
                _handle_hf_error(exc)


def tab_generation(api_key: str) -> None:
    st.markdown("Continue a prompt with **text generation** using GPT-2.")
    prompt = st.text_area("Enter a prompt:", "Once upon a time in a galaxy far away,", key="gen_input")
    max_tokens = st.slider("Max new tokens", 20, 200, 80, key="gen_tokens")
    if st.button("Generate Text", key="gen_btn"):
        if not prompt.strip():
            st.warning("Please enter a prompt first.")
            return
        with st.spinner("Generating…"):
            try:
                client = make_client(api_key)
                generated = client.text_generation(
                    prompt,
                    model="gpt2",
                    max_new_tokens=max_tokens,
                )
                show_result(generated)
            except Exception as exc:
                _handle_hf_error(exc)


def tab_summarization(api_key: str) -> None:
    st.markdown("Generate a concise **summary** of a longer passage.")
    length_choice = st.select_slider(
        "Summary length",
        options=["Short", "Medium", "Detailed"],
        value="Medium",
        key="sum_length",
    )
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
            try:
                client = make_client(api_key)
                length_settings = {
                    "Short": (20, 60),
                    "Medium": (40, 110),
                    "Detailed": (80, 180),
                }
                min_length, max_length = length_settings[length_choice]
                result = client.summarization(
                    article,
                    model="facebook/bart-large-cnn",
                    min_length=min_length,
                    max_length=max_length,
                )
                show_result(result.summary_text)
            except Exception as exc:
                _handle_hf_error(exc)


def tab_translation(api_key: str) -> None:
    language_options = {
        "French": "Helsinki-NLP/opus-mt-en-fr",
        "Spanish": "Helsinki-NLP/opus-mt-en-es",
        "German": "Helsinki-NLP/opus-mt-en-de",
        "Italian": "Helsinki-NLP/opus-mt-en-it",
        "Portuguese": "Helsinki-NLP/opus-mt-en-pt",
    }
    st.markdown("Translate text **from English** into your selected target language.")
    target_language = st.selectbox(
        "Target language",
        list(language_options.keys()),
        index=0,
        key="tr_lang",
    )
    text = st.text_area("Enter English text:", "Hello, how are you today?", key="tr_input")
    if st.button("Translate", key="tr_btn"):
        if not text.strip():
            st.warning("Please enter some text first.")
            return
        with st.spinner("Translating…"):
            try:
                client = make_client(api_key)
                model = language_options[target_language]
                result = client.translation(text, model=model)
                show_result(result.translation_text)
            except Exception as exc:
                _handle_hf_error(exc)


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
            try:
                client = make_client(api_key)
                result = client.question_answering(
                    question=question,
                    context=context,
                    model="deepset/roberta-base-squad2",
                )
                raw_answer = getattr(result, "answer", None)
                if raw_answer is None:
                    st.warning("No strong answer was found in the provided context.")
                    return
                answer = str(raw_answer).strip()
                confidence = float(getattr(result, "score", 0.0))
                if answer == "":
                    st.warning("No strong answer was found in the provided context.")
                    return
                if confidence < LOW_CONFIDENCE_THRESHOLD:
                    st.warning("Low-confidence answer — consider adding more context or clarifying the question.")
                show_result(f"{answer}\n\nConfidence: {confidence:.1%}")
            except Exception as exc:
                _handle_hf_error(exc)


def tab_entities(api_key: str) -> None:
    st.markdown("Extract **named entities and keywords** from your text.")
    text = st.text_area(
        "Enter text:",
        (
            "Apple CEO Tim Cook visited Paris to discuss AI partnerships with "
            "European startups and researchers."
        ),
        key="ner_input",
    )
    if st.button("Extract Entities", key="ner_btn"):
        if not text.strip():
            st.warning("Please enter some text first.")
            return
        with st.spinner("Extracting entities…"):
            try:
                client = make_client(api_key)
                entities = client.token_classification(
                    text,
                    model="dslim/bert-base-NER",
                    aggregation_strategy="simple",
                )
                if not entities:
                    st.warning("No named entities were detected.")
                    return

                lines = []
                keywords = []
                for entity in entities:
                    word = str(getattr(entity, "word", "")).strip()
                    label = str(
                        getattr(entity, "entity_group", getattr(entity, "entity", "ENTITY")),
                    ).strip()
                    score = float(getattr(entity, "score", 0.0))
                    if not word:
                        continue
                    lines.append(f"- {word} ({label}, confidence: {score:.1%})")
                    keywords.append(word.lower())

                unique_keywords = []
                seen = set()
                for keyword in keywords:
                    if keyword in seen:
                        continue
                    seen.add(keyword)
                    unique_keywords.append(keyword)

                keyword_text = ", ".join(unique_keywords[:MAX_DISPLAYED_KEYWORDS])
                details = "\n".join(lines)
                if keyword_text:
                    details += f"\n\nKeywords: {keyword_text}"
                show_result(details)
            except Exception as exc:
                _handle_hf_error(exc)


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
    tabs = st.tabs(["😊 Sentiment", "📝 Summarise", "🌐 Translate", "❓ Q&A", "🏷️ Entities"])

    with tabs[0]:
        tab_sentiment(api_key)
    with tabs[1]:
        tab_summarization(api_key)
    with tabs[2]:
        tab_translation(api_key)
    with tabs[3]:
        tab_qa(api_key)
    with tabs[4]:
        tab_entities(api_key)


if __name__ == "__main__":
    main()
