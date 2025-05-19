import os
import requests
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from openai import OpenAI

# Load API keys
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

ROUTING_PROMPT_TEMPLATE = """
You are an intelligent assistant capable of choosing the best tool for answering user queries.

Available tools:
1. web_search - Use this for real-time or recent information such as news, events, weather, prices.
2. rag - Use this for company-specific/internal knowledge like policies, handbooks, documentation, etc.
3. llm - Use this for general knowledge, reasoning, explanation, or creative writing.
4. rag_archive - Use this to archive or save new knowledge, notes, documents, or updates into the internal knowledge base.

Decide the best tool to use for this user query:
"{query}"

Respond in the following format:
Tool: <tool_name>
Reason: <brief reason>
"""

def decide_tool(query: str) -> dict:
    prompt = ROUTING_PROMPT_TEMPLATE.format(query=query)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )
    content = response.choices[0].message.content
    lines = content.strip().splitlines()

    tool, reason = "", ""
    for line in lines:
        if line.lower().startswith("tool:"):
            tool = line.split(":")[1].strip().lower()
        elif line.lower().startswith("reason:"):
            reason = line.split(":", 1)[1].strip()
    return {"tool": tool, "reason": reason}

def clean_for_archiving(raw_input: str) -> str:
    prompt = f"Extract clean structured text for archiving from the following message:\n{raw_input}"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content

def rag_archive_handler(cleaned_content: str):
    embeddings = OpenAIEmbeddings()
    db = Chroma(persist_directory="./chroma_store", embedding_function=embeddings)
    doc = Document(page_content=cleaned_content, metadata={"source": "user_input"})
    db.add_documents([doc])
    return "✅ Content archived to RAG (ChromaDB) successfully."

def rag_query_handler(query: str):
    embeddings = OpenAIEmbeddings()
    db = Chroma(persist_directory="./chroma_store", embedding_function=embeddings)
    results = db.similarity_search(query, k=3)

    if not results:
        return "❌ No matching documents found."

    context = "\n\n".join([doc.page_content for doc in results])
    prompt = f"""You are an assistant answering based only on the context provided.

Context:
{context}

Question:
{query}

If the answer is not present in the context, respond with: "❌ Sorry, I couldn’t find an exact answer in the knowledge base."
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    return response.choices[0].message.content.strip()

def web_search_handler(query: str):
    if not SERPER_API_KEY:
        return "❌ SERPER_API_KEY is not set. Please export it as an environment variable."

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {"q": query, "num": 3}
    response = requests.post("https://google.serper.dev/search", headers=headers, json=payload)

    if response.status_code != 200:
        return f"❌ Web search failed: {response.status_code}"

    data = response.json()
    results = data.get("organic", [])
    if not results:
        return "❌ No web results found."

    return "\n\n".join([f"🔗 {r['title']}\n{r['link']}\n{r['snippet']}" for r in results[:3]])

def handle_query(query: str):
    decision = decide_tool(query)
    print(f"\n🧠 Tool selected: {decision['tool']}")
    print(f"📌 Reason: {decision['reason']}\n")

    if decision["tool"] == "rag_archive":
        cleaned = clean_for_archiving(query)
        print("🔹 Cleaned content for archiving:\n", cleaned)
        print(rag_archive_handler(cleaned))

    elif decision["tool"] == "rag":
        print("🔍 Synthesizing answer from RAG context:\n")
        print(rag_query_handler(query))

    elif decision["tool"] == "web_search":
        print("🌐 Searching the web...\n")
        print(web_search_handler(query))

    elif decision["tool"] == "llm":
        print("🤖 General response (LLM):\n")
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": query}],
            temperature=0.7,
        )
        print(response.choices[0].message.content)

    else:
        print(f"⚠️ Tool not implemented: {decision['tool']}")

# 🚀 CLI loop
if __name__ == "__main__":
    print("📥 Enter your message (type 'exit' to quit):")
    while True:
        user_input = input("\n🗨️  You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("👋 Exiting. Goodbye!")
            break
        handle_query(user_input)

