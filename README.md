
# 🔎 Agentic Research Engine

An intelligent, multi-tool **AI research assistant** built with Streamlit, LangChain, Groq, and DuckDuckGo — capable of fetching **real-time insights**, **summarizing research**, and even **showing images** based on your questions.

<img width="1366" height="610" alt="Screenshot 2025-07-26 231917" src="https://github.com/user-attachments/assets/c9e4d1d2-db1f-470b-bea5-c31a4ea5030d" />

---

## 🚀 Features

- **Multi-source search** (DuckDuckGo, Wikipedia, Arxiv)
- **Image search + preview** with DuckDuckGo Images
- Powered by **Groq's LLaMA 3-70B** for fast, intelligent answers
- **Conversational memory** for multi-turn questions
- Tool-based agent with LangChain’s `initialize_agent`
- Clean **Streamlit UI** with session tracking & chat history
- Fully local session state – no external storage needed

---

## 🧠 Example Queries

| 🔬 Research | 🖼️ Visual Search |
|------------|-----------------|
| *"What is quantum computing?"* | *"Show me images of neural networks"* |
| *"Latest research on LLMs"* | *"Find pictures of the Eiffel Tower"* |
| *"Tell me about reinforcement learning"* | *"Images of fusion reactors"* |

---

## 🛠️ Tech Stack

- **[LangChain](https://github.com/langchain-ai/langchain)** – Agents, Tools, Memory
- **[Groq](https://groq.com/)** – Ultra-fast inference with `llama3-70b-8192`
- **[DuckDuckGo Search](https://pypi.org/project/duckduckgo-search/)** – Web and image results
- **[Arxiv API](https://arxiv.org/help/api/)** – Scientific paper search
- **[Wikipedia API](https://www.mediawiki.org/wiki/API:Main_page)** – General knowledge
- **[Streamlit](https://streamlit.io/)** – Interactive web UI

---

## 🔧 How to Run

1. **Clone the repo**

```bash
git clone https://github.com/mharoon1578/agentic-research-engine.git
cd agentic-search-engine
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set up your API key**

You’ll need a [Groq API Key](https://console.groq.com/). Paste it into the sidebar when the app loads.

4. **Run the app**

```bash
streamlit run app.py
```

---

## 📂 File Structure

```
📦 agentic-search-engine/
├── app.py
├── requirements.txt
└── README.md
```

---

## 📜 License

MIT License. Free to use, fork, and extend.

---

## 🙌 Contribute

Pull requests welcome! Got feature ideas or want to add more tools (e.g., YouTube, News, PDFs)?  
Open an issue or ping me on [LinkedIn](https://www.linkedin.com/in/muhammad-haroon-a097a9342/).

---

## 💡 Inspiration

This project was built as a personal weekend challenge to explore:
- Agentic AI systems
- Real-time search with LLMs
- Minimal, usable research UIs

---

## ⭐ Give it a Star

If you find this useful, feel free to ⭐ the repo!
