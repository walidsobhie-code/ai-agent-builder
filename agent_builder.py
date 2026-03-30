#!/usr/bin/env python3
"""
AI Agent Builder - Visual node-based agent builder with LangChain
"""
import json
import os
import argparse
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

# Try to import LangChain
try:
    from langchain.agents import AgentExecutor, load_agent
    from langchain.chat_models import ChatOpenAI, ChatAnthropic
    from langchain.tools import Tool
    from langchain.memory import ConversationBufferMemory
    from langchain.schema import HumanMessage, AIMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False


@dataclass
class AgentNode:
    """Base node for agent workflow"""
    node_id: str
    node_type: str  # llm, tool, memory, condition, input, output
    config: Dict[str, Any] = field(default_factory=dict)
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)


class LLMNode(AgentNode):
    """LLM node for text generation"""

    def __init__(self, node_id: str, config: Dict[str, Any]):
        super().__init__(node_id, "llm", config)
        self.model = config.get("model", "gpt-4")
        self.temperature = config.get("temperature", 0.7)
        self.system_prompt = config.get("system_prompt", "You are a helpful assistant.")
        self.llm = None

        if LANGCHAIN_AVAILABLE:
            try:
                if "claude" in self.model.lower():
                    self.llm = ChatAnthropic(model=self.model, temperature=self.temperature)
                else:
                    self.llm = ChatOpenAI(model=self.model, temperature=self.temperature)
            except Exception as e:
                print(f"⚠️  Failed to initialize LLM: {e}")

    def execute(self, context: Dict) -> str:
        """Execute LLM node"""
        user_input = context.get("input", "")

        if not LANGCHAIN_AVAILABLE or self.llm is None:
            return f"[Demo] Response from {self.model}: {user_input[:50]}..."

        try:
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_input}
            ]
            response = self.llm.invoke(messages)
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            return f"[Error] {str(e)}"


class ToolNode(AgentNode):
    """Tool node for executing functions"""

    def __init__(self, node_id: str, config: Dict[str, Any]):
        super().__init__(node_id, "tool", config)
        self.tool_name = config.get("tool", "search")
        self.tool_func = config.get("function", self._default_tool)

    def _default_tool(self, query: str) -> str:
        """Default tool function"""
        return f"Tool executed: {query}"

    def execute(self, context: Dict) -> Any:
        """Execute tool node"""
        input_data = context.get("input", "")

        if callable(self.tool_func):
            return self.tool_func(input_data)
        return self._default_tool(input_data)


class MemoryNode(AgentNode):
    """Memory node for storing conversation history"""

    def __init__(self, node_id: str, config: Dict[str, Any]):
        super().__init__(node_id, "memory", config)
        self.memory_type = config.get("type", "buffer")  # buffer, summary, kg
        self.max_tokens = config.get("max_tokens", 2000)
        self.memory = None

        if LANGCHAIN_AVAILABLE:
            self.memory = ConversationBufferMemory(
                max_token_limit=self.max_tokens,
                return_messages=True
            )

    def execute(self, context: Dict) -> Dict:
        """Execute memory node"""
        last_input = context.get("input", "")
        last_output = context.get("last_result", "")

        if self.memory:
            self.memory.chat_memory.add_user_message(last_input)
            self.memory.chat_memory.add_ai_message(last_output)

        return {
            "type": self.memory_type,
            "stored": True,
            "input": last_input,
            "output": last_output
        }

    def get_history(self) -> List[Dict]:
        """Get conversation history"""
        if self.memory:
            messages = self.memory.chat_memory.messages
            return [{"role": "ai" if isinstance(m, AIMessage) else "user",
                     "content": m.content} for m in messages]
        return []


class ConditionNode(AgentNode):
    """Condition node for branching logic"""

    def __init__(self, node_id: str, config: Dict[str, Any]):
        super().__init__(node_id, "condition", config)
        self.condition = config.get("condition", "always_true")

    def execute(self, context: Dict) -> str:
        """Execute condition node"""
        if self.condition == "always_true":
            return "true"
        # Add more conditions as needed
        return "false"


class AgentBuilder:
    """Visual node-based agent builder"""

    def __init__(self):
        self.nodes: Dict[str, AgentNode] = {}
        self.connections: List[tuple] = []
        self.context: Dict = {"input": "", "memory": [], "last_result": None}

    def add_node(self, node: AgentNode) -> AgentNode:
        """Add a node to the workflow"""
        self.nodes[node.node_id] = node
        return node

    def add_llm_node(self, node_id: str, model: str = "gpt-4",
                     system_prompt: str = "You are helpful.") -> LLMNode:
        """Add an LLM node"""
        config = {"model": model, "system_prompt": system_prompt}
        node = LLMNode(node_id, config)
        return self.add_node(node)

    def add_tool_node(self, node_id: str, tool_name: str,
                     tool_func=None) -> ToolNode:
        """Add a tool node"""
        config = {"tool": tool_name, "function": tool_func}
        node = ToolNode(node_id, config)
        return self.add_node(node)

    def add_memory_node(self, node_id: str, memory_type: str = "buffer") -> MemoryNode:
        """Add a memory node"""
        config = {"type": memory_type}
        node = MemoryNode(node_id, config)
        return self.add_node(node)

    def connect(self, from_node: str, to_node: str):
        """Connect two nodes"""
        self.connections.append((from_node, to_node))

    def execute(self, input_data: str, start_node: str = None) -> str:
        """Execute the agent workflow"""
        self.context = {
            "input": input_data,
            "memory": [],
            "last_result": None
        }

        if not self.nodes:
            return "No nodes in workflow"

        # Simple sequential execution
        for node_id, node in self.nodes.items():
            result = node.execute(self.context)
            self.context["last_result"] = result
            if isinstance(result, str):
                self.context["input"] = result  # Chain outputs

        return self.context.get("last_result", "No output")

    def to_json(self) -> str:
        """Export workflow as JSON"""
        workflow = {
            "nodes": [
                {
                    "id": node.node_id,
                    "type": node.node_type,
                    "config": node.config
                }
                for node in self.nodes.values()
            ],
            "connections": self.connections
        }
        return json.dumps(workflow, indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> 'AgentBuilder':
        """Import workflow from JSON"""
        workflow = json.loads(json_str)
        builder = cls()

        for node_data in workflow.get("nodes", []):
            node_type = node_data.get("type")
            node_id = node_data.get("id")
            config = node_data.get("config", {})

            if node_type == "llm":
                builder.add_llm_node(node_id, config.get("model"), config.get("system_prompt"))
            elif node_type == "tool":
                builder.add_tool_node(node_id, config.get("tool"))
            elif node_type == "memory":
                builder.add_memory_node(node_id, config.get("type"))

        for from_node, to_node in workflow.get("connections", []):
            builder.connect(from_node, to_node)

        return builder


def main():
    parser = argparse.ArgumentParser(
        description='AI Agent Builder - Visual workflow builder',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--interactive', '-i', action='store_true', help='Interactive mode')
    parser.add_argument('--input', help='Input text for agent')
    parser.add_argument('--workflow', '-w', help='Load workflow from JSON file')
    parser.add_argument('--export', '-e', help='Export workflow to JSON file')

    args = parser.parse_args()

    print("🤖 AI Agent Builder")
    print("=" * 40)

    if not LANGCHAIN_AVAILABLE:
        print("⚠️  LangChain not installed. Running in demo mode.")
        print("   Install: pip install langchain openai anthropic")
        print()

    builder = AgentBuilder()

    # Add sample nodes
    builder.add_llm_node("llm_1", "gpt-4", "You are a helpful coding assistant.")
    builder.add_memory_node("memory_1", "buffer")
    builder.add_tool_node("tool_1", "search")

    # Connect nodes
    builder.connect("llm_1", "memory_1")

    if args.workflow and os.path.exists(args.workflow):
        with open(args.workflow, 'r') as f:
            builder = AgentBuilder.from_json(f.read())
        print(f"📂 Loaded workflow from: {args.workflow}")

    if args.export:
        with open(args.export, 'w') as f:
            f.write(builder.to_json())
        print(f"💾 Exported workflow to: {args.export}")
        return

    if args.interactive:
        print("Interactive mode. Type 'quit' to exit.")
        print("Commands: add-llm, add-tool, add-memory, show, export")
        print()

        while True:
            user_input = input("You: ")
            if user_input.lower() in ('quit', 'exit', 'q'):
                break

            result = builder.execute(user_input)
            print(f"Agent: {result}")
            print()

    elif args.input:
        result = builder.execute(args.input)
        print(f"✅ Output: {result}")

    else:
        # Demo run
        result = builder.execute("Hello! Help me write a Python function.")
        print(f"✅ Agent output: {result}")
        print()
        print("📖 Use --interactive for interactive mode")
        print("📖 Use --workflow to load a workflow JSON")


if __name__ == '__main__':
    main()