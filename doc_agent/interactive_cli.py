"""
Interactive CLI with Rich Output

Modern CLI interface for the AI documentation generator.
Features rich text formatting, progress bars, and interactive prompts.
"""

import os
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

from simple_agent import DocumentationAgent
from enums import LLMClient, DocumentationFormat


class InteractiveCLI:
    """
    Interactive CLI with rich formatting and user experience.

    Provides a modern command-line interface with colors, progress bars,
    and interactive prompts for the AI documentation generator.
    """

    def __init__(self):
        # Initialize rich Console
        self.console = Console()
        self.colors = {
            "success": "green",
            "error": "red",
            "warning": "yellow",
            "info": "blue",
            "accent": "cyan",
        }

        self.agent = None

    def print_banner(self) -> None:
        """
        Display the application welcome banner.

        :returns: None
        :rtype: None
        """
        # Create a rich Panel with banner text
        banner = Panel.fit(
            "🤖 Interactive AI Documentation Generator",
            style="bold",
            border_style="green",
        )
        self.console.print(banner)
        self.console.print("=" * 50)

    def get_file_path(self) -> Path:
        """
        Interactively prompt user for Python file to process.

        :returns: Path to the selected Python file
        :rtype: Path
        """

        # Add file picker suggestions
        python_files = [f for f in os.listdir() if f.endswith(".py")]
        self.console.print("Available Python files:")
        for i, file in enumerate(python_files, 1):
            self.console.print(f"{i}. {file}")

        # Use rich Prompt to get file path
        file_path = Prompt.ask("Enter Python file path")
        path = Path(file_path)

        # Add file validation loop
        while not path.exists() or path.suffix != ".py":
            self.console.print("❌ File not found or not a Python file. Try again.")
            file_path = Prompt.ask("Enter Python file path")
            path = Path(file_path)

        return path

    def choose_llm_provider(self) -> LLMClient:
        """
        Interactively prompt user to select LLM provider.

        :returns: Selected LLM client type
        :rtype: LLMClient
        """
        # Use rich Prompt with choices
        llm_provider = Prompt.ask(
            "Choose LLM", choices=[LLMClient.OPENAI, LLMClient.ANTHROPIC]
        )

        # Check API key availability and warn user
        if llm_provider == LLMClient.OPENAI and not os.getenv("OPENAI_API_KEY"):
            self.console.print("❌ OpenAI API key not found in environment variables")
            return None
        elif llm_provider == LLMClient.ANTHROPIC and not os.getenv("ANTHROPIC_API_KEY"):
            self.console.print(
                "❌ Anthropic API key not found in environment variables"
            )
            return None

        return llm_provider

    def choose_doc_format(self) -> DocumentationFormat:
        """
        Interactively prompt user to select documentation format.

        :returns: Selected documentation format
        :rtype: DocumentationFormat
        """
        # Create rich Table showing format options
        table = Table(title="Choose Documentation Format")
        table.add_column("Format", justify="left")
        table.add_column("Description", justify="left")

        for fmt in DocumentationFormat:
            table.add_row(fmt.name, fmt.value)

        self.console.print(table)

        # Use Prompt with enum choices
        doc_format = Prompt.ask(
            "Choose Documentation Format",
            choices=[fmt.name for fmt in DocumentationFormat],
        )

        return DocumentationFormat[doc_format]

    def setup_agent(
        self, llm_client: LLMClient, doc_format: DocumentationFormat
    ) -> DocumentationAgent:
        """
        Initialize documentation agent with progress indication.

        :param llm_client: LLM client to use
        :type llm_client: LLMClient
        :param doc_format: Documentation format to generate
        :type doc_format: DocumentationFormat
        :returns: Initialized documentation agent or None if failed
        :rtype: DocumentationAgent or None
        """
        # Use rich Progress or Spinner during setup
        with self.console.status("Setting up AI agent...", spinner="dots"):
            try:
                self.agent = DocumentationAgent(llm_client, doc_format)
                return self.agent
            except Exception as e:
                self.console.print(f"❌ Failed to initialize agent: {e}", style="red")
                return None

    def process_file_with_progress(self, file_path: Path) -> Optional[dict]:
        """
        Process Python file with progress indication.

        :param file_path: Path to the Python file to process
        :type file_path: Path
        :returns: Documentation results or None if failed
        :rtype: Optional[dict]
        """
        with self.console.status(
            f"Documenting {file_path.name}...", spinner="bouncingBar"
        ):
            try:
                return self.agent.document_file(str(file_path))
            except Exception as e:
                self.console.print(f"❌ Failed to process file: {e}", style="red")
                return None

    def display_results(self, results: dict) -> None:
        """
        Display documentation results with rich formatting.

        :param results: Documentation generation results
        :type results: dict
        :returns: None
        :rtype: None
        """
        if not results:
            self.console.print("📭 No functions found to document")
            return

        # Create rich Table for results overview
        table = Table(title="Results Overview")
        table.add_column("Function Name", justify="left")
        table.add_column("Arguments", justify="left")
        table.add_column("Documentation Length", justify="left")

        for func_name, data in results.items():
            # Convert function arguments to string if they're not already
            args = (
                str(data["original_function"].args)
                if hasattr(data["original_function"], "args")
                else "No args"
            )
            table.add_row(
                func_name,
                args,
                str(len(data["generated_docs"])),
            )

        self.console.print(table)

        # Display each function's documentation in Panels
        for func_name, data in results.items():
            panel = Panel(
                Syntax(
                    data["generated_docs"], "python", theme="dark", line_numbers=True
                ),
                title=func_name,
                border_style="green",
            )
            self.console.print(panel)

    def save_results_interactively(self, results: dict) -> None:
        """
        Interactively save documentation results to file.

        :param results: Documentation generation results
        :type results: dict
        :returns: None
        :rtype: None
        """
        # Ask user if they want to save
        save = Confirm.ask("Save results to file?")
        if not save:
            return

        output_path = Prompt.ask("Enter output file path")

        # Show save progress and confirmation
        with self.console.status(f"Saving results to {output_path}...", spinner="dots"):
            try:
                with open(output_path, "w", encoding="utf-8") as f:
                    for func_name, data in results.items():
                        f.write(f"# {func_name}\n")
                        f.write(data["generated_docs"])
                        f.write("\n\n")
                self.console.print(f"✅ Results saved to {output_path}")
            except Exception as e:
                self.console.print(f"❌ Failed to save: {e}")

    def handle_batch_mode(self):
        """
        Handle batch processing mode for multiple files.

        :returns: None
        :rtype: None
        """
        # Use rich file picker or glob patterns
        file_path = self.get_file_path()
        llm_client = self.choose_llm_provider()
        doc_format = self.choose_doc_format()

        # Initialize agent
        if not self.setup_agent(llm_client, doc_format):
            return

        # Process file
        results = self.process_file_with_progress(file_path)

        # Show results
        if results:
            self.display_results(results)
            self.save_results_interactively(results)

    def run(self):
        """
        Execute the main interactive CLI workflow.

        :returns: None
        :rtype: None
        """
        # Add try/catch for graceful error handling
        try:
            self.print_banner()

            # Interactive setup flow
            file_path = self.get_file_path()
            llm_client = self.choose_llm_provider()
            doc_format = self.choose_doc_format()

            # Initialize agent
            if not self.setup_agent(llm_client, doc_format):
                return

            # Process file
            results = self.process_file_with_progress(file_path)

            # Show results
            if results:
                self.display_results(results)
                self.save_results_interactively(results)

        except Exception as e:
            self.console.print(f"❌ Error: {e}", style="red")

        self.console.print("\n🎉 Thanks for using the AI Documentation Generator!")


def main():
    """
    Entry point for the interactive CLI application.

    :returns: None
    :rtype: None
    """
    cli = InteractiveCLI()
    cli.run()


if __name__ == "__main__":
    main()
