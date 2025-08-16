"""
Simple Documentation Agent

Implements the core Perceive → Reason → Act pattern for automated code documentation.
Supports multiple LLM providers and documentation formats.
"""

from typing import List
import os
from openai import OpenAI
from anthropic import Anthropic
from dotenv import load_dotenv
from simple_parser import extract_functions, FunctionInfo
from enums import LLMClient, DocumentationFormat, DocumentationFormatExamples

load_dotenv()


class DocumentationAgent:
    """
    Minimal AI agent for generating code documentation

    Follows the three-phase pattern:
    1. PERCEIVE: Parse code and extract functions
    2. REASON: Build context and prepare prompts
    3. ACT: Generate documentation using LLM
    """

    def __init__(
        self,
        llm_client: LLMClient,
        doc_format: DocumentationFormat = DocumentationFormat.RST,
    ):
        """
        Initialize the documentation agent.

        :param llm_client: LLM provider to use for documentation generation
        :type llm_client: LLMClient
        :param doc_format: Documentation format to generate
        :type doc_format: DocumentationFormat
        :raises AgentException: If llm_client or doc_format is invalid
        """
        if llm_client is None:
            raise AgentException("LLM client not initialized!")

        if llm_client not in LLMClient._value2member_map_:
            raise AgentException("Unsupported LLM client!")

        if doc_format not in DocumentationFormat._value2member_map_:
            raise AgentException("Unsupported documentation format!")

        self.llm_type = llm_client
        self.doc_format = doc_format
        self.doc_format_example = DocumentationFormatExamples[doc_format.name]

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
        Extract function information from Python source code.

        :param file_path: Path to the Python file to analyze
        :type file_path: str
        :returns: List of function information objects
        :rtype: List[FunctionInfo]
        """
        print(f"🔍 Analyzing file: {file_path}")
        functions = extract_functions(file_path)
        print(f"📊 Found {len(functions)} functions to document")
        return functions

    def reason(self, function: FunctionInfo) -> str:
        """
        Build context and generate prompt for LLM documentation generation.

        :param function: Function information to generate documentation for
        :type function: FunctionInfo
        :returns: Formatted prompt for LLM
        :rtype: str
        """
        prompt = f"""
        You are a Python docstring generator.

        Goal:
        Return exactly the function declaration line and its docstring in {self.doc_format.value} 
        style.
        Do not include any function body statements. Do not add any text before or after.
        Do not wrap the output in code fences.

        Source function (for analysis only; do not copy the body):
        <<<SOURCE
        {function.source_code}
        SOURCE>>>

        Style guide (authoritative example; follow its sections and syntax exactly):
        <<<STYLE
        {self.doc_format_example}
        STYLE>>>

        Strict output contract:
        1) Preserve the original declaration EXACTLY (decorators, async, name, parameters, defaults, type hints, return type).
        2) Immediately follow it with a correctly indented {self.doc_format.value} docstring.
        3) Docstring must include:
        - A concise one-line summary.
        - A parameters section and a returns section formatted per {self.doc_format.value}.
        4) If there are no parameters or no return value, handle that according to the style in the STYLE block (omit or mark None, as appropriate).
        5) Do not invent types that are not present or reasonably inferable; prefer what is annotated.
        6) Any example usage must remain inside the docstring as an Examples section; never emit code outside the docstring.
        7) Output only the declaration and its docstring—nothing else.
        """

        return prompt.strip()

    def act(self, prompt: str) -> str:
        """
        Generate documentation using the configured LLM.

        :param prompt: Formatted prompt for documentation generation
        :type prompt: str
        :returns: Generated documentation text
        :rtype: str
        """

        try:
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
        Generate documentation for a single function using the complete workflow.

        :param function: Function information to document
        :type function: FunctionInfo
        :returns: Generated documentation text
        :rtype: str
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
        Generate documentation for all functions in a Python file.

        :param file_path: Path to the Python file to document
        :type file_path: str
        :returns: Dictionary mapping function names to documentation results
        :rtype: dict
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
    Demonstrate the documentation agent capabilities.

    :param llm_client: LLM provider to use for demonstration
    :type llm_client: LLMClient
    """
    print("🚀 Simple Documentation Agent Demo")
    print("=" * 50)

    # Create agent with no LLM (uses mock responses)
    agent = DocumentationAgent(llm_client=llm_client)

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
    Custom exception for documentation agent errors.
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
