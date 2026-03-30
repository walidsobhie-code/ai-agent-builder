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
    def __init__(self, node_type: str, config: Dict):
        self.node_type = node_type
        self.config = config
    
    def execute(self, input_data: str) -> Dict:
        if self.node_type == "llm":
            return self._execute_llm(input_data)
        return {"output": f"[{self.node_type}] {input_data}"}
    
    def _execute_llm(self, input_data: str) -> Dict:
        try:
            response = requests.post(
                OLLAMA_URL,
                json={"model": MODEL, "prompt": input_data, "stream": False},
                timeout=30
            )
            if response.status_code == 200:
                return {"output": response.json().get("response", "No response")}
        except Exception as e:
            return {"output": f"Ollama error: {e}"}
        return {"output": "Ollama not running"}

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
