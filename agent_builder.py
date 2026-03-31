#!/usr/bin/env python3
"""
AI Agent Builder - Using Ollama (free local AI)
"""
import json
import requests
from typing import Dict, List, Any

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder"

class AgentNode:
    """Represents a node in the agent workflow"""

    def __init__(self, node_type: str, config: Dict):
        self.node_type = node_type
        self.config = config
        self.node_id = config.get("id", f"{node_type}_{id(self)}")

    def execute(self, input_data: str) -> Dict:
        """Execute the node based on its type"""
        if self.node_type == "llm":
            return self._execute_llm(input_data)
        elif self.node_type == "prompt":
            return self._execute_prompt(input_data)
        elif self.node_type == "output":
            return self._execute_output(input_data)
        return {"output": f"[{self.node_type}] {input_data}"}

    def _execute_llm(self, input_data: str) -> Dict:
        """Execute LLM node using Ollama"""
        try:
            model = self.config.get("model", MODEL)
            temperature = self.config.get("temperature", 0.7)

            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": model,
                    "prompt": input_data,
                    "stream": False,
                    "options": {"temperature": temperature}
                },
                timeout=self.config.get("timeout", 30)
            )
            if response.status_code == 200:
                return {"output": response.json().get("response", "No response")}
        except Exception as e:
            return {"output": f"Ollama error: {e}", "error": str(e)}
        return {"output": "Ollama not running"}

    def _execute_prompt(self, input_data: str) -> Dict:
        """Process input with a prompt template"""
        template = self.config.get("template", "{input}")
        output = template.format(input=input_data)
        return {"output": output}

    def _execute_output(self, input_data: str) -> Dict:
        """Format and return the final output"""
        format_type = self.config.get("format", "text")
        if format_type == "json":
            try:
                return {"output": json.dumps({"result": input_data})}
            except:
                return {"output": input_data}
        return {"output": input_data}

class AgentBuilder:
    def __init__(self):
        self.nodes = []
    
    def add_node(self, node_type: str, config: Dict):
        node = AgentNode(node_type, config)
        self.nodes.append(node)
        return node
    
    def execute(self, input_data: str) -> str:
        result = {"output": input_data}
        for node in self.nodes:
            result = node.execute(result["output"])
        return result.get("output", "No output")

def create_sample_agent():
    builder = AgentBuilder()
    builder.add_node("llm", {"name": "assistant"})
    return builder

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true")
    args = parser.parse_args()
    
    print("🤖 AI Agent Builder (Ollama)")
    print("=" * 40)
    
    if args.build:
        builder = create_sample_agent()
        result = builder.execute("Hello! What can you do?")
        print(f"💬 {result[:200]}")

if __name__ == "__main__":
    main()
