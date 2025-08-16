"""
Quick Start - Get Results in 15 Minutes!

This file shows you how to go from zero to working AI agent quickly.
Perfect for testing your implementation and seeing immediate results.

Run this file at each step to see your progress!
"""

import os
from simple_parser import extract_functions
from simple_agent import SimpleDocumentationAgent
from constants import LLMClient


def test_step_1_parser():
    """
    Test Step 1: Can we extract functions from code?
    """
    print("🔍 STEP 1: Testing Function Extraction")
    print("=" * 40)

    # Create a sample Python file to test on
    sample_code = '''
def add(x, y):
    """
    Add two numbers together.
    """
    return x + y

def multiply(a, b):
    result = a * b
    return result

class Calculator:
    def subtract(self, x, y):
        return x - y
'''

    # Write sample to temporary file
    test_file = "temp_test.py"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(sample_code)

    try:
        # Test the parser
        functions = extract_functions(test_file)

        print(f"✅ Success! Found {len(functions)} functions:")
        for func in functions:
            print(f"   📝 {func.name}({', '.join(func.args)})")

        if len(functions) >= 2:
            print("🎉 Parser working correctly!")
            return True
        else:
            print(
                "❌ Expected at least 2 functions, implement the TODOs in simple_parser.py"
            )
            return False

    finally:
        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)


def test_step_2_agent():
    """
    Test Step 2: Can we create prompts and generate docs?
    """
    print("\n🤖 STEP 2: Testing Agent Pipeline")
    print("=" * 40)

    # Create agent (no LLM needed for this test)
    agent = SimpleDocumentationAgent(llm_client=LLMClient.OPENAI)

    # Test on the quick_start.py file itself
    try:
        results = agent.document_file(__file__)

        if results:
            print(f"✅ Success! Generated docs for {len(results)} functions:")
            for func_name in results.keys():
                print(f"   📝 {func_name}")
            print("🎉 Agent pipeline working!")
            return True
        else:
            print("❌ No documentation generated. Check the TODOs in simple_agent.py")
            return False

    except Exception as e:
        print(f"❌ Error in agent: {e}")
        return False


def test_step_3_real_llm():
    """
    Test Step 3: Real LLM integration (optional)
    """
    print("\n🚀 STEP 3: Testing Real LLM Integration")
    print("=" * 40)

    print("💡 This step requires an API key for OpenAI or Anthropic")
    print("📝 For now, the agent uses mock responses")
    print("🔑 To use real LLM:")
    print("   1. Get API key from OpenAI or Anthropic")
    print("   2. Implement the TODO in simple_agent.py act() method")
    print("   3. Run this test again")

    # You could add real LLM testing here once implemented
    return True


def show_next_steps():
    """
    Show what to do after basic setup works
    """
    print("\n🎯 NEXT STEPS FOR LEARNING")
    print("=" * 40)

    print("✨ Your Basic Agent is Working! Now try:")
    print()

    print("🔧 IMMEDIATE IMPROVEMENTS (5-10 minutes each):")
    print("   1. Better prompts - Add examples and context to simple_agent.py")
    print("   2. Error handling - Handle edge cases in parsing")
    print("   3. Output formatting - Make generated docs look better")
    print()

    print("🚀 NEXT FEATURES (15-30 minutes each):")
    print("   4. Class documentation - Extend parser to handle classes")
    print("   5. File-level docs - Generate module-level documentation")
    print("   6. Quality scoring - Rate the generated documentation")
    print()

    print("💡 ADVANCED FEATURES (1+ hours each):")
    print("   7. Interactive mode - Let user approve/reject suggestions")
    print("   8. Multiple files - Process entire directories")
    print("   9. Code analysis - Add complexity analysis and recommendations")
    print("   10. Integration - Connect with VS Code or documentation sites")
    print()

    print("📚 LEARNING RESOURCES:")
    print("   - Python AST module: https://docs.python.org/3/library/ast.html")
    print("   - OpenAI API docs: https://platform.openai.com/docs")
    print("   - Prompt engineering: https://www.promptingguide.ai/")


def main():
    """
    Run all tests and show progress
    """
    print("🚀 QUICK START - AI Agent Learning")
    print("⏱️  Goal: Working agent in 15 minutes")
    print("📋 This tests your implementation step by step")
    print()

    # Test each step
    step1_pass = test_step_1_parser()

    if step1_pass:
        step2_pass = test_step_2_agent()

        if step2_pass:
            test_step_3_real_llm()
            show_next_steps()
        else:
            print("\n❌ Step 2 failed. Fix simple_agent.py TODOs first.")
    else:
        print("\n❌ Step 1 failed. Fix simple_parser.py TODOs first.")

    print("\n" + "=" * 50)
    print("🎓 Keep building and learning!")


if __name__ == "__main__":
    main()
