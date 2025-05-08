# 🧠 AI Research Assistant

This project automates web research using `CrewAI`, `Tavily`, and `Trafilatura` with structured multi-agent reasoning. It includes web search, content parsing, context synthesis, and final summarization using an LLM.

## 🔧 Features

- **Web Search Agent** using Tavily  
- **Content Fetcher Agent** to download & parse articles with `trafilatura`  
- **Context Generator** saving rich content to `context_output.md`  
- **Final Answer Agent** generating summaries from parsed context  
- Fully modular `CrewAI` agent-task pipeline  
- Custom LLM support via Groq’s API (`gemma2-9b-it`)

---

## 🚀 Usage

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create a `.env` file:

```env
TAVILY_API_KEY=your_tavily_key
GROQ_API_KEY=your_groq_key
```

---

### 3. Run the Assistant

```bash
python3 -m agent
```

You’ll be prompted for a research query. The assistant will:

1. Search the web via Tavily  
2. Fetch & parse top links  
3. Format the content using `trafilatura`  
4. Save it to `context_output.md`  
5. Generate a final structured summary saved/displayed from `research_output.md`

---

## 📂 File Structure

```
├── agent.py                  # Entrypoint  
├── requirements.txt          # Dependencies
└── .env                      # Environment variables  
```
