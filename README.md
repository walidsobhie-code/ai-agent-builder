# 🤖 AI Agent Builder

> **Build AI agents with drag-and-drop** — No coding required. Create autonomous agents with tools, memory, and LLM integration in minutes.

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)

[🚀 Try Live Demo](https://huggingface.co/spaces/my-ai-stack/ai-agent-builder)
[🚀 Try Live Demo](https://huggingface.co/spaces/my-ai-stack/ai-agent-builder)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/walidsobhie-code/ai-agent-builder)](https://github.com/walidsobhie-code/ai-agent-builder/stargazers)

## 🎯 What It Does

```
Build: [LLM] → [Tools] → [Memory] → [Output]
Ask:   "Find the best flight from Dubai to Riyadh"

Agent: Searches web → Checks calendar → Books flight → Confirms email ✅
```

Build agents that **actually do things** — search the web, run code, send emails, use APIs.

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🧠 **GPT-4 Powered** | State-of-the-art language model |
| 🔧 **Tool Plugins** | Web search, calculator, API calls |
| 💾 **Memory** | Remember conversation context |
| 🤖 **Multi-Agent** | Orchestrate multiple agents |
| 🎛️ **Gradio UI** | Visual agent builder |
| 🐳 **Docker Ready** | One-command deployment |

## 🚀 Quick Start

### Install
```bash
git clone https://github.com/walidsobhie-code/ai-agent-builder.git
cd ai-agent-builder
pip install -r requirements.txt
cp .env.example .env
# Add your OPENAI_API_KEY
```

### Build Your First Agent
```python
from agent_builder import AgentBuilder

# Create agent
builder = AgentBuilder()

# Add LLM
builder.add_node("llm", {
    "model": "gpt-4",
    "temperature": 0.7
})

# Add tools
builder.add_tool(
    name="web_search",
    func=lambda q: f"Results for: {q}",
    description="Search the web"
)

# Ask questions
result = builder.execute("Find Operations Manager jobs in Dubai")
print(result)
```

### Or Use the Web UI
```bash
python gradio_app.py
# Opens: http://localhost:7860
```

## 🎨 Visual Builder Demo

```
┌──────────────────────────────────────────────────────────┐
│  🤖 AI Agent Builder                                    │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────┐    ┌─────────┐    ┌─────────────┐       │
│  │   LLM   │───▶│  TOOLS  │───▶│   MEMORY    │       │
│  │  GPT-4  │    │ Search  │    │  Conversation│       │
│  └─────────┘    │ Calculate│    └─────────────┘       │
│                  │ API Call │                            │
│                  └─────────┘                            │
│                                                          │
│  💬 "Book a flight to Dubai for tomorrow"               │
│  🔍 Searching flights...                                 │
│  ✈️ Found: Emirates EK123 at 2:30 PM                   │
│  ✅ Booking confirmed!                                  │
└──────────────────────────────────────────────────────────┘
```

## 🔧 Built-in Tools

| Tool | What It Does |
|------|---------------|
| 🌐 `web_search` | Search Google/Bing |
| 🧮 `calculator` | Run math calculations |
| 📧 `send_email` | Send email notifications |
| 📅 `check_calendar` | Check calendar availability |
| 📊 `run_code` | Execute Python code |
| 🔍 `vector_search` | Search knowledge base |

## 📖 Example Agents

### Research Agent
```python
builder = AgentBuilder()
builder.add_node("llm", {"model": "gpt-4", "temperature": 0.3})
builder.add_tool("web_search", search_web)
result = builder.execute("Research AI trends in Gulf region")
```

### Job Hunter Agent
```python
builder = AgentBuilder()
builder.add_node("llm", {"model": "gpt-4"})
builder.add_tool("web_search", search_linkedin)
builder.add_tool("send_email", send_application)
result = builder.execute("Apply to Operations Manager jobs in Saudi")
```

## 🐳 Docker

```bash
docker build -t agent-builder .
docker run -p 7860:7860 -e OPENAI_API_KEY=your_key agent-builder
```

## 📁 Project Structure

```
ai-agent-builder/
├── agent_builder.py      # Core builder
├── gradio_app.py       # Web UI
├── requirements.txt
├── Dockerfile
└── examples/
    ├── research_agent.py
    └── job_hunter_agent.py
```

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## ⭐ Support

Star the repo if you find it useful!

---

**Built with ❤️ by [walidsobhie-code](https://github.com/walidsobhie-code)**

## 🖥️ Demo Screenshot

![Agent Builder Demo](ai-agent-builder_test.png)

## 🗺️ Roadmap

- [ ] [Planned] Web version / hosted demo
- [ ] [Planned] API endpoint for production use
- [ ] [Planned] Support for more languages
- [ ] [In Progress] Performance optimizations
- [ ] [Done] Gradio web interface
- [ ] [Done] Docker deployment

## 🏢 Used By

> Have a project using this? Send a PR to add your company!

- *(coming soon — be the first to list your project!)*

## 🤝 Contributors

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

[![GitHub Contributors](https://contrib.rocks/image?repo=my-ai-stack/ai-agent-builder)](https://github.com/my-ai-stack/ai-agent-builder/graphs/contributors)
