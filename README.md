
# 🧠 Intelligent Query Router with LLM + RAG + Web Search

This project is an **AI assistant** that intelligently chooses the best tool to answer a user’s query using:

- 🌐 Real-time web search (via [Serper.dev](https://serper.dev/))
- 📚 Retrieval-Augmented Generation (RAG) using ChromaDB
- 🤖 General reasoning with OpenAI's GPT-4
- 🗃️ Archival of new knowledge into a local vector store

---

## 📦 Features

- 🔀 **Tool routing**: Uses GPT-4 to decide how a query should be handled.
- 🧠 **LLM answering**: For general-purpose reasoning or creative queries.
- 🔍 **RAG search**: Retrieve answers from your internal knowledge base.
- 🗄️ **RAG archiving**: Clean and store new content to the vector DB.
- 🌐 **Web search**: Get fresh info from the internet via Serper API.
- 🖥️ **Command-line interface**: Simple terminal chat experience.

---

## 🧰 Requirements

- Python 3.8+
- OpenAI account + API key
- Serper.dev account + API key

---

## 🧪 Installation

1. **Clone the repository**:

```bash
git clone https://github.com/your-username/intelligent-query-router.git
cd intelligent-query-router
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

3. **Set environment variables**:

```bash
export OPENAI_API_KEY=your_openai_key
export SERPER_API_KEY=your_serper_key
```

You can also store them in a `.env` file and load it using `python-dotenv`.

---

## 🚀 Usage

Run the CLI:

```bash
python assistant.py
```

Example prompt:

```text
🗨️  You: What is the latest news on AI regulations?
```

The assistant will:

- Decide the right tool (`web_search`)
- Perform the web search
- Return top results from Google via Serper.dev

---

## 🧠 Tool Routing Logic

The assistant decides between the following tools:

| Tool          | Purpose                                                     |
|---------------|-------------------------------------------------------------|
| `web_search`  | For live info: news, weather, prices, etc.                 |
| `rag`         | For internal knowledge base search                         |
| `llm`         | For reasoning, creative writing, general questions         |
| `rag_archive` | For saving new content (company notes, updates, etc.)      |

It uses GPT-4 with a prompt to make this decision based on your query.

---

## 📚 Knowledge Base (Chroma)

- Stored locally in `./chroma_store`
- Vector search is powered by `OpenAIEmbeddings`

To archive content:

```text
🗨️  You: Save this update: "Our policy on hybrid work changed to 3 days/week from office."
```

---

## 🔍 Web Search (Serper)

- Uses `https://google.serper.dev/search` endpoint
- Returns top 3 organic results

Example:

```text
🗨️  You: What are the latest stock prices of Apple?
```

---

## 🧾 File Structure

```
.
├── assistant.py           # Main program logic
├── chroma_store/          # Local vector store for RAG
├── README.md              # Documentation
└── requirements.txt       # Python dependencies
```

---

## 📄 Example `.env` file

```env
OPENAI_API_KEY=your_openai_key
SERPER_API_KEY=your_serper_key
```

---

## 🧩 Future Enhancements

- Web UI with Streamlit or Gradio
- LangChain Agents and tool plugins
- Memory storage with LangChain's `ConversationBufferMemory`

---

## 📝 License

MIT License. See [LICENSE](LICENSE) for more info.

---

## ✨ Credits

- [LangChain](https://www.langchain.com/)
- [OpenAI API](https://platform.openai.com/)
- [Serper.dev](https://serper.dev/)
- [ChromaDB](https://www.trychroma.com/)
