"""
Simple Code Parser - 2 Hour Learning Version

This is a dramatically simplified version focused on getting results quickly.
We'll only extract functions and their basic information - no complex AST visiting.

Learning Goal: Understand how to extract code structure programmatically
Time: 15-20 minutes to implement the TODOs
"""

import ast
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class FunctionInfo:
    """
    Simple container for function information
    """

    name: str
    args: List[str]
    source_code: str
    line_number: int
    docstring: Optional[str] = None


def extract_functions(file_path: str) -> List[FunctionInfo]:
    """
    Extract function information from a Python file

    This is the PERCEIVE phase of our agent - gathering information.

    :returns: List of FunctionInfo objects
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()

        # Parse the source code into an Abstract Syntax Tree
        tree = ast.parse(source_code)
        source_lines = source_code.splitlines()

        functions = []

        # Walk through all nodes in the AST
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Extract function information
                func_name = node.name

                # Extract argument names
                arg_names = []
                for arg in node.args.args:
                    arg_names.append(arg.arg)

                # Get source code for this function
                start_line = node.lineno - 1  # AST uses 1-based line numbers
                end_line = node.end_lineno if node.end_lineno else start_line + 1
                func_source = "\n".join(source_lines[start_line:end_line])

                # Get docstring if it exists
                docstring = ast.get_docstring(node=node)

                # Create function info object
                func_info = FunctionInfo(
                    name=func_name,
                    args=arg_names,
                    source_code=func_source,
                    line_number=node.lineno,
                    docstring=docstring,
                )

                functions.append(func_info)

        return functions

    except SyntaxError as e:
        print(f"❌ Syntax error in {file_path}: {e}")
        return []
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return []
    except Exception as e:
        print(f"❌ Error parsing {file_path}: {e}")
        return []


def demo_parser():
    """
    Test the parser on this very file
    """
    print("🔍 Testing Parser on This File")
    print("=" * 40)

    functions = extract_functions(__file__)

    print(f"Found {len(functions)} functions:")
    for func in functions:
        print(f"\n📝 Function: {func.name}")
        print(f"   Args: {func.args}")
        print(f"   Line: {func.line_number}")
        print(f"   Has docstring: {'Yes' if func.docstring else 'No'}")

        # Show first 100 characters of source
        preview = func.source_code.replace("\n", " ")[:100]
        print(f"   Source preview: {preview}...")


if __name__ == "__main__":
    print("🚀 Simple Parser - 2 Hour Learning Version")
    print("\n💡 TODO: Implement the function extraction logic!")
    print("📍 Look for 'TODO' comments in extract_functions()")
    print("\n🎯 Goal: Extract function names, arguments, and source code")

    demo_parser()
