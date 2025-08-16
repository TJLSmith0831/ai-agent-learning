"""
Simple Documentation Agent - 2 Hour Learning Version

This implements the core Perceive → Reason → Act pattern in the simplest way possible.
Focus on getting a working agent, not perfect code.

Learning Goal: Understand AI agent architecture and LLM integration
Time: 30-40 minutes to implement the TODOs
"""

from typing import List
import os
from openai import OpenAI
from anthropic import Anthropic
from dotenv import load_dotenv
from simple_parser import extract_functions, FunctionInfo
from constants import LLMClient

load_dotenv()


class SimpleDocumentationAgent:
    """
    Minimal AI agent for generating code documentation

    Follows the three-phase pattern:
    1. PERCEIVE: Parse code and extract functions
    2. REASON: Build context and prepare prompts
    3. ACT: Generate documentation using LLM
    """

    def __init__(self, llm_client: LLMClient):
        """
        Initialize the agent

        llm_client: Your LLM client (OpenAI, Anthropic, etc.)
        """
        if llm_client is None:
            raise AgentException("LLM client not initialized!")

        if llm_client not in LLMClient._value2member_map_:
            raise AgentException("Unsupported LLM client!")

        self.llm_type = llm_client
        
        if llm_client == LLMClient.OPENAI:
            self.llm_client = OpenAI(
                api_key=os.environ.get("OPENAI_API_KEY"),
            )
        elif llm_client == LLMClient.ANTHROPIC:
            self.llm_client = Anthropic(
                api_key=os.environ.get("ANTHROPIC_API_KEY"),
            )

    def perceive(self, file_path: str) -> List[FunctionInfo]:
        """
        PHASE 1: PERCEIVE - Gather information about the code

        This is where the agent "sees" what it's working with.
        """
        print(f"🔍 Analyzing file: {file_path}")
        functions = extract_functions(file_path)
        print(f"📊 Found {len(functions)} functions to document")
        return functions

    def reason(self, function: FunctionInfo) -> str:
        """
        PHASE 2: REASON - Build context and prepare for action

        This is where the agent decides what to do with the information.
        For documentation, this means building a good prompt.
        """
        # Build a prompt for the LLM
        # Include:
        # - Clear task description
        # - The function code
        # - Instructions for output format

        prompt = f"""
            Task: Write a Python docstring for this function

            Function to document:
            {function.source_code}

            Instructions: 
            - Write in reStructuredText (reST) format
            - Include Args and Returns sections
            - Be specific about what the function does
            - Include a description of the function's purpose
            - Include a description of example usages and where in the codebase it is used

            Generated docstring:
        """

        return prompt.strip()

    def act(self, prompt: str) -> str:
        """
        PHASE 3: ACT - Generate the documentation

        This is where the agent produces its output.
        """

        try:
            # Check if we have API keys - if not, return mock response
            if self.llm_type == LLMClient.OPENAI and not os.environ.get("OPENAI_API_KEY"):
                return "📝 Mock OpenAI response: This is where the generated docstring would appear."
            elif self.llm_type == LLMClient.ANTHROPIC and not os.environ.get("ANTHROPIC_API_KEY"):
                return "📝 Mock Anthropic response: This is where the generated docstring would appear."
            
            # Real LLM calls
            if self.llm_type == LLMClient.OPENAI:
                response = self.llm_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=300,
                )
                return response.choices[0].message.content
            elif self.llm_type == LLMClient.ANTHROPIC:
                response = self.llm_client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=300,
                    messages=[{"role": "user", "content": prompt}],
                )
                return response.content[0].text
            else:
                raise ValueError(f"Unsupported LLM client: {self.llm_type}")

        except Exception as e:
            return f"❌ Error calling LLM: {e}"

    def document_function(self, function: FunctionInfo) -> str:
        """
        Complete workflow: Perceive → Reason → Act for a single function
        """
        print(f"\n📝 Documenting function: {function.name}")

        # Reason: Build the prompt
        prompt = self.reason(function)
        print(f"💭 Built prompt ({len(prompt)} characters)")

        # Act: Generate documentation
        documentation = self.act(prompt)
        print(f"✅ Generated documentation ({len(documentation)} characters)")

        return documentation

    def document_file(self, file_path: str) -> dict:
        """
        Complete workflow: Document all functions in a file

        This demonstrates the full agent pipeline.
        """
        print(f"\n🤖 Starting documentation generation for: {file_path}")
        print("=" * 60)

        # Phase 1: PERCEIVE - Analyze the file
        functions = self.perceive(file_path)

        if not functions:
            print("❌ No functions found to document")
            return {}

        # Process each function through Reason → Act
        results = {}
        for function in functions:
            doc = self.document_function(function)
            results[function.name] = {
                "original_function": function,
                "generated_docs": doc,
            }

        print(
            f"\n🎉 Documentation complete! Generated docs for {len(results)} functions"
        )
        return results


def demo_agent(llm_client: LLMClient):
    """
    Demonstrate the agent on this very file
    """
    print("🚀 Simple Documentation Agent Demo")
    print("=" * 50)

    # Create agent with no LLM (uses mock responses)
    agent = SimpleDocumentationAgent(llm_client=llm_client)

    # Document this file
    results = agent.document_file(__file__)

    # Show results
    print("\n📋 Generated Documentation:")
    print("=" * 50)

    for func_name, result in results.items():
        print(f"\n## Function: {func_name}")
        print(f"Original args: {result['original_function'].args}")
        print(f"Generated docs:\n{result['generated_docs']}")


class AgentException(Exception):
    """
    Exception for agent errors
    """


if __name__ == "__main__":
    print("🤖 Simple Documentation Agent - 2 Hour Learning Version")
    print("\n💡 TODOs to implement:")
    print("1. Improve the prompt in reason() method")
    print("2. Add real LLM integration in act() method")
    print("3. Test with your own Python files")
    print("\n🎯 Goal: Create a working agent that generates docstrings")

    print("\n🤖 Testing with OpenAI")
    demo_agent(llm_client=LLMClient.OPENAI)
    print("\n🤖 Testing with Anthropic")
    demo_agent(llm_client=LLMClient.ANTHROPIC)
