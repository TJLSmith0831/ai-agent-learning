"""
CLI Tool for AI Documentation Agent

Command-line interface using argparse for the AI documentation generator.
Supports file input, LLM selection, and documentation format configuration.
"""

import argparse
import sys
import os
from pathlib import Path
from simple_agent import DocumentationAgent
from enums import DocumentationFormat, LLMClient


def create_parser() -> argparse.ArgumentParser:
    """
    Create the command-line argument parser.

    :returns: Configured argument parser
    :rtype: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(
        prog="bard-ai-doc",
        description="🤖 AI-powered code documentation generator",
        epilog="Example: bard-ai-doc my_script.py --llm openai --format markdown",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Add required argument for file path
    parser.add_argument("file_path", type=Path, help="Python file to document")

    # Add optional --llm flag
    parser.add_argument(
        "--llm",
        choices=[LLMClient.OPENAI, LLMClient.ANTHROPIC],
        help="LLM provider",
    )

    # Add optional --format flag
    parser.add_argument(
        "--format",
        choices=[fmt.value for fmt in DocumentationFormat],
        help="Doc format",
    )

    # Add --verbose flag for detailed output
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose output",
    )

    # Add --output flag for saving results
    parser.add_argument(
        "--output",
        type=Path,
        help="Output file path",
    )

    return parser


def validate_arguments(args) -> bool:
    """
    Validate and process command-line arguments.

    :param args: Parsed command-line arguments
    :type args: argparse.Namespace
    :returns: True if arguments are valid, False otherwise
    :rtype: bool
    """
    errors = []

    # Check if input file exists
    if not args.file_path.exists():
        errors.append(f"Input file does not exist: {args.file_path}")

    # Check if input file is Python file
    if not args.file_path.suffix == ".py":
        errors.append(f"Input file is not a Python file: {args.file_path}")

    # Check if LLM API keys are available
    if args.llm == LLMClient.OPENAI and not os.getenv("OPENAI_API_KEY"):
        errors.append("OpenAI API key not found in environment variables")
    elif args.llm == LLMClient.ANTHROPIC and not os.getenv("ANTHROPIC_API_KEY"):
        errors.append("Anthropic API key not found in environment variables")

    if errors:
        print("❌ Validation errors:")
        for error in errors:
            print(f"   • {error}")
        sys.exit(1)

    return True


def setup_agent(llm_client, doc_format) -> DocumentationAgent:
    """
    Initialize the documentation agent with specified parameters.

    :param llm_client: LLM client type to use
    :type llm_client: LLMClient
    :param doc_format: Documentation format to generate
    :type doc_format: DocumentationFormat
    :returns: Initialized documentation agent
    :rtype: DocumentationAgent
    """
    try:
        # Create DocumentationAgent instance
        agent = DocumentationAgent(llm_client, doc_format)

        return agent

    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        print("💡 Make sure your API keys are set in environment variables")
        sys.exit(1)


def process_file(agent, file_path, verbose=False) -> dict:
    """
    Process a single file and generate documentation.

    :param agent: Documentation agent instance
    :type agent: DocumentationAgent
    :param file_path: Path to the Python file to process
    :type file_path: str or Path
    :param verbose: Whether to print verbose output
    :type verbose: bool
    :returns: Documentation results dictionary
    :rtype: dict
    """
    if verbose:
        print(f"🔍 Processing file: {file_path}")

    try:
        # Use agent to document the file
        results = agent.document_file(file_path)

        if verbose:
            print(f"✅ Generated documentation for {len(results)} functions")

        return results

    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return None


def format_output(results, output_format) -> str:
    """
    Format the documentation results for display.

    :param results: Documentation results to format
    :type results: dict
    :param output_format: Output format specification
    :type output_format: str
    :returns: Formatted documentation string
    :rtype: str
    :return: Formatted documentation as a string
    """
    if not results:
        return "No functions found to document."

    output = []
    for func_name, data in results.items():
        output.append(f"## {func_name}")
        output.append(data["generated_docs"])
        output.append("")  # Empty line

    return "\n".join(output)


def save_output(content, output_path) -> None:
    """
    Save documentation content to a file.

    :param content: Documentation content to save
    :type content: str
    :param output_path: Path to save the documentation
    :type output_path: Path
    :returns: None
    :rtype: None
    """
    try:
        # Write content to output_path
        output_path.write_text(content)

        print(f"💾 Documentation saved to: {output_path}")

    except Exception as e:
        print(f"❌ Failed to save output: {e}")
        sys.exit(1)


def main() -> None:
    """
    Main CLI entry point for the application.

    :returns: None
    :rtype: None
    """
    # Create parser and parse arguments
    parser = create_parser()
    args = parser.parse_args()

    # Validate arguments
    validate_arguments(args)

    # Setup agent
    agent = setup_agent(args.llm, args.format)

    # Process the file
    results = process_file(agent, args.file_path, args.verbose)

    # Format and display results
    output = format_output(results, args.format)
    print(output)

    # Save to file if output path provided
    if args.output:
        save_output(output, args.output)

    print("🎉 Documentation generation complete!")


if __name__ == "__main__":
    main()

    print("🚧 CLI Tool - Learning Version")
    print("📝 Implement the TODOs to create a working CLI")
    print("💡 Focus on understanding argparse and CLI patterns")
    print()
    print("🎯 Learning Goals:")
    print("   • Command-line argument parsing")
    print("   • Input validation and error handling")
    print("   • User-friendly help and documentation")
    print("   • File I/O and output formatting")
