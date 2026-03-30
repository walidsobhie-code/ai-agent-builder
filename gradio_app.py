#!/usr/bin/env python3
"""
AI Agent Builder - Gradio Web Interface
Build AI agents with a visual workflow editor
"""
import os
import json
import gradio as gr
from agent_builder import AgentBuilder, LLMNode, ToolNode, MemoryNode

# Global builder
builder = None


def create_agent(prompt, model="gpt-4"):
    """Create a simple agent"""
    global builder

    try:
        builder = AgentBuilder()
        builder.add_llm_node("llm", model, prompt)
        builder.add_memory_node("memory", "buffer")

        return f"✅ Agent created with model: {model}\n\nPrompt: {prompt}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


def run_agent(message):
    """Run the agent with a message"""
    global builder

    if builder is None:
        return "⚠️  No agent created. Create one first!"

    try:
        result = builder.execute(message)
        return f"**You:** {message}\n\n**Agent:** {result}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


def export_workflow():
    """Export workflow as JSON"""
    global builder

    if builder is None:
        return "{}"

    return builder.to_json()


def import_workflow(json_str):
    """Import workflow from JSON"""
    global builder

    try:
        builder = AgentBuilder.from_json(json_str)
        return f"✅ Imported workflow with {len(builder.nodes)} nodes"
    except Exception as e:
        return f"❌ Error: {str(e)}"


# Build Gradio Interface
with gr.Blocks(title="AI Agent Builder", theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🤖 AI Agent Builder")
    gr.Markdown("Build autonomous AI agents with visual workflows")

    with gr.Tab("💬 Chat"):
        gr.Markdown("### Chat with your agent")

        with gr.Row():
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(height=400)
                msg = gr.Textbox(
                    placeholder="Send a message to your agent...",
                    show_label=False
                )
                with gr.Row():
                    submit_btn = gr.Button("Send", variant="primary")
                    clear_btn = gr.Button("Clear")

            with gr.Column(scale=1):
                gr.Markdown("### Create Agent")
                with gr.Column():
                    agent_prompt = gr.Textbox(
                        label="System Prompt",
                        value="You are a helpful AI assistant.",
                        lines=3
                    )
                    model_select = gr.Dropdown(
                        ["gpt-4", "gpt-3.5-turbo", "claude-3-sonnet"],
                        value="gpt-4",
                        label="Model"
                    )
                    create_btn = gr.Button("Create Agent")

        create_btn.click(
            create_agent,
            inputs=[agent_prompt, model_select],
            outputs=[msg]
        )

        def respond(message, history):
            response = run_agent(message)
            history.append((message, response))
            return "", history

        submit_btn.click(respond, [msg, chatbot], [msg, chatbot])
        msg.submit(respond, [msg, chatbot], [msg, chatbot])
        clear_btn.click(lambda: (None, []), outputs=[msg, chatbot])

    with gr.Tab("🔧 Workflow"):
        gr.Markdown("### Workflow JSON Editor")

        gr.Markdown("Export your workflow to share, or import an existing workflow.")

        with gr.Row():
            with gr.Column():
                workflow_json = gr.Textbox(
                    label="Workflow JSON",
                    lines=20,
                    placeholder="{}"
                )

                with gr.Row():
                    export_btn = gr.Button("📤 Export")
                    import_btn = gr.Button("📥 Import")

            with gr.Column():
                workflow_status = gr.Textbox(label="Status", lines=5)

        export_btn.click(export_workflow, outputs=[workflow_json])
        import_btn.click(import_workflow, inputs=[workflow_json], outputs=[workflow_status])

    with gr.Tab("ℹ️ About"):
        gr.Markdown("""
        ## AI Agent Builder

        A visual node-based builder for AI agents:

        ### Features
        - 🎯 **LLM Nodes** - Connect GPT-4, Claude, Gemini
        - 🛠️ **Tool Nodes** - Add custom tools
        - 💾 **Memory** - Persistent conversation history
        - 🔄 **Workflow** - Visual node connections
        - 📦 **Export/Import** - Share agent configs

        ### Node Types
        - **LLM Node** - Text generation with AI models
        - **Tool Node** - Execute custom functions
        - **Memory Node** - Store conversation history
        - **Condition Node** - Branching logic

        ### Requirements
        - Python 3.10+
        - LangChain
        - OpenAI API key (or Anthropic)
        """)

# Launch
if __name__ == "__main__":
    print("🚀 Starting AI Agent Builder Web UI...")
    print("   Open http://localhost:7863 in your browser")
    app.launch(server_name="0.0.0.0", server_port=7863)