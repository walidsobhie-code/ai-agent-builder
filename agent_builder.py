#!/usr/bin/env python3
"""
AI Agent Builder - Build AI agents with LangChain
No-code platform for creating autonomous AI agents
"""
import os
import json
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

try:
    from langchain.agents import AgentExecutor, create_openai_functions_agent
    from langchain_openai import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain.tools import Tool
    from langchain.memory import ConversationBufferMemory
    from langchain.schema import HumanMessage, AIMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

load_dotenv()

class AgentNode:
    """Individual agent node"""
    def __init__(self, node_type: str, config: Dict[str, Any]):
        self.node_type = node_type
        self.config = config
        self.name = config.get("name", node_type)
        self.description = config.get("description", "")
    
    def execute(self, input_data: str, context: Dict) -> Dict:
        if self.node_type == "llm":
            return self._execute_llm(input_data, context)
        elif self.node_type == "tool":
            return self._execute_tool(input_data, context)
        elif self.node_type == "memory":
            return self._execute_memory(input_data, context)
        return {"output": f"[{self.node_type}] {input_data}"}
    
    def _execute_llm(self, input_data: str, context: Dict) -> Dict:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return {"output": f"[LLM] {input_data} - Needs OPENAI_API_KEY"}
        
        if not LANGCHAIN_AVAILABLE:
            return {"output": f"[LLM] {input_data} - Needs LangChain"}
        
        model = self.config.get("model", "gpt-4")
        temperature = float(self.config.get("temperature", 0.7))
        
        llm = ChatOpenAI(model=model, temperature=temperature, openai_api_key=api_key)
        response = llm.invoke(input_data)
        
        return {"output": response.content, "type": "text"}
    
    def _execute_tool(self, input_data: str, context: Dict) -> Dict:
        tool_name = self.config.get("tool", "web_search")
        return {"output": f"[Tool: {tool_name}] Executed on: {input_data}", "tool": tool_name}
    
    def _execute_memory(self, input_data: str, context: Dict) -> Dict:
        return {"output": "[Memory] Context stored", "type": "memory"}

class AgentBuilder:
    """Build AI agents with LangChain"""
    
    def __init__(self):
        self.nodes: List[AgentNode] = []
        self.tools: List[Tool] = []
        self.memory = None
        self.llm = None
    
    def add_node(self, node_type: str, config: Dict) -> AgentNode:
        """Add a node to the agent"""
        node = AgentNode(node_type, config)
        self.nodes.append(node)
        return node
    
    def set_llm(self, model: str = "gpt-4", temperature: float = 0.7):
        """Set the LLM for the agent"""
        self.add_node("llm", {"model": model, "temperature": temperature})
    
    def add_tool(self, name: str, func, description: str):
        """Add a tool to the agent"""
        tool = Tool(name=name, func=func, description=description)
        self.tools.append(tool)
        return tool
    
    def build(self) -> AgentExecutor:
        """Build the LangChain agent"""
        if not LANGCHAIN_AVAILABLE:
            raise ImportError("LangChain not available. Run: pip install langchain langchain-openai")
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set in .env")
        
        self.llm = ChatOpenAI(model="gpt-4", openai_api_key=api_key)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI assistant."),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            human_prefix="Human",
            ai_prefix="AI"
        )
        
        agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        return AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True
        )
    
    def execute(self, input_data: str) -> str:
        """Execute the agent"""
        if not self.nodes:
            return "No nodes added. Use builder.add_node()"
        
        context = {"input": input_data, "history": []}
        
        for node in self.nodes:
            result = node.execute(input_data, context)
            if result.get("output"):
                input_data = result["output"]
                context["last_result"] = result
        
        return context.get("last_result", {}).get("output", "No output")

def create_sample_agent() -> AgentBuilder:
    """Create a sample AI agent"""
    builder = AgentBuilder()
    
    # Add LLM node
    builder.add_node("llm", {
        "name": "assistant",
        "model": "gpt-4",
        "temperature": 0.7,
        "prompt": "You are a helpful assistant specialized in operations management."
    })
    
    # Add web search tool
    def web_search(query: str) -> str:
        return f"Search results for: {query}"
    
    builder.add_tool(
        name="web_search",
        func=web_search,
        description="Search the web for information"
    )
    
    # Add calculator tool
    def calculator(expression: str) -> str:
        try:
            result = eval(expression)
            return f"Result: {result}"
        except:
            return "Invalid expression"
    
    builder.add_tool(
        name="calculator", 
        func=calculator,
        description="Calculate a mathematical expression"
    )
    
    return builder

def main():
    parser = __import__("argparse").ArgumentParser(description="AI Agent Builder")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    parser.add_argument("--build", action="store_true", help="Build and test agent")
    args = parser.parse_args()
    
    print("🤖 AI Agent Builder with LangChain")
    print("=" * 50)
    
    if args.build:
        try:
            builder = create_sample_agent()
            print("✅ Agent created successfully!")
            
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                agent = builder.build()
                print("✅ LangChain agent compiled!")
                result = agent.invoke({"input": "Hello, what can you do?"})
                print(f"💬 Response: {result['output'][:200]}")
            else:
                print("⚠️ Add OPENAI_API_KEY to .env to enable full functionality")
        
        except Exception as e:
            print(f"❌ Error: {e}")
    
    elif args.interactive:
        builder = create_sample_agent()
        print("\n💬 Interactive mode - Type 'exit' to quit")
        while True:
            query = input("\nYou: ")
            if query.lower() == 'exit':
                break
            result = builder.execute(query)
            print(f"AI: {result[:500]}")
    
    else:
        print("""
🤖 AI Agent Builder

Usage:
  python agent_builder.py --build        Build and test agent
  python agent_builder.py -i            Interactive chat mode

Or create your own agent:
  from agent_builder import AgentBuilder
  
  builder = AgentBuilder()
  builder.add_node("llm", {"model": "gpt-4"})
  builder.add_tool("search", my_search_func, "Search the web")
  
  result = builder.execute("Your question here")
        """)

if __name__ == "__main__":
    main()
