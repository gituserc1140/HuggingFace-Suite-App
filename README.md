# 🤗 HuggingFace Suite App

[![GitHub](https://img.shields.io/badge/GitHub-gituserc1140%2FHuggingFace--Suite--App-24292e?logo=github)](https://github.com/gituserc1140/HuggingFace-Suite-App)
[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-ea4aaa?logo=github-sponsors)](https://github.com/sponsors/gituserc1140)

A **Streamlit** web app that gives you a suite of NLP tools powered by the [Hugging Face Inference API](https://huggingface.co/inference-api). Enter your own Hugging Face API key directly in the sidebar — no configuration files needed.

---

## ✨ Features

| Tab | Task | Model |
|-----|------|-------|
| 😊 Sentiment | Sentiment or emotion classification | `distilbert-base-uncased-finetuned-sst-2-english`, `j-hartmann/emotion-english-distilroberta-base` |
| 📝 Summarise | Condense long articles (short / medium / detailed) | `facebook/bart-large-cnn` |
| 🌐 Translate | English → French / Spanish / German / Italian / Portuguese | `Helsinki-NLP/opus-mt-en-*` |
| ❓ Q&A | Answer questions from a passage with confidence | `deepset/roberta-base-squad2` |
| 🏷️ Entities | Named entity and keyword extraction | `dslim/bert-base-NER` |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/gituserc1140/HuggingFace-Suite-App.git
cd HuggingFace-Suite-App
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

The app opens in your browser at `http://localhost:8501`.

---

## 🔑 Adding Your API Key

1. Sign up or log in at [huggingface.co](https://huggingface.co).
2. Go to **Settings → Access Tokens** and create a token (a free account is sufficient for the Inference API).
3. Paste the token into the **Hugging Face API Key** field in the app's sidebar.

> **Tip:** You can also supply the key without typing it every time by setting the `HUGGINGFACE_API_KEY` environment variable or adding it to your [Streamlit secrets file](https://docs.streamlit.io/develop/concepts/connections/secrets-management) (`~/.streamlit/secrets.toml`):
>
> ```toml
> HUGGINGFACE_API_KEY = "hf_xxxxxxxxxxxxxxxxxx"
> ```

The app will use the sidebar value first; it falls back to the secret/env variable if the sidebar is empty.

---

## 📦 Project Structure

```
HuggingFace-Suite-App/
├── app.py            # Main Streamlit application
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## ❤️ Support

If you find this project useful, consider [sponsoring on GitHub](https://github.com/sponsors/gituserc1140) — it helps keep the project going!
