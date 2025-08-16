# CLI Tool Development Guide

## 🎯 Implementation Guide: From Basic to Advanced

This guide covers CLI development patterns for the AI documentation agent.

### **Phase 1: Basic CLI - `cli_agent.py`**
**Focus**: Argparse fundamentals and CLI structure

```bash
# Goal: Create a working command-line interface
python cli_agent.py my_script.py --llm openai --format markdown
```

**Key Features:**
- **Argument Parsing**: Required vs optional arguments
- **User Input Validation**: File existence, enum choices
- **Error Handling**: Graceful failures with helpful messages
- **Help Documentation**: Auto-generated usage information

**Implementation TODOs:**
1. `create_parser()` - Define CLI arguments and options
2. `validate_arguments()` - Input validation and error messages
3. `setup_agent()` - Initialize your AI agent with CLI args
4. `main()` - Connect parsing → validation → processing → output

### **Phase 2: Interactive CLI - `interactive_cli.py`**
**Focus**: Rich user experience with modern CLI libraries

```bash
# Goal: Beautiful, interactive CLI with progress bars and colors
python interactive_cli.py
```

**Key Features:**
- **Rich Text Output**: Colors, formatting, panels, tables
- **Progress Indication**: Spinners and progress bars for long operations
- **Interactive Prompts**: User choices, confirmations, file pickers
- **Professional Appearance**: Consistent visual design

**Library Choice (pick one):**
- **rich**: Beautiful terminal output (`pip install rich`)
- **click**: Popular CLI framework (`pip install click`) 
- **typer**: Modern type-based CLI (`pip install typer`)

**Implementation TODOs:**
1. Install your chosen library
2. `InteractiveCLI` class - Set up rich console and styling
3. Interactive prompts for file selection, LLM choice, format
4. Progress bars during AI processing
5. Formatted output display with syntax highlighting

### **Phase 3: Configuration - `config_manager.py`**
**Focus**: User preferences and settings persistence

```bash
# Goal: Save user preferences across CLI sessions
ai-doc config --show
ai-doc config --set default_llm anthropic
```

**Key Features:**
- **Configuration Hierarchy**: ENV vars > CLI args > config file > defaults
- **Cross-Platform**: Proper config directory location (XDG spec)
- **Data Validation**: Type checking and constraint validation
- **Configuration Migration**: Handling config format changes

**Implementation TODOs:**
1. `AgentConfig` dataclass - Type-safe configuration structure
2. `ConfigManager._get_config_dir()` - Cross-platform config location
3. `load_config()` - JSON parsing with fallbacks and validation
4. `get_env_overrides()` - Environment variable integration
5. `merge_config()` - Configuration precedence resolution

### **Phase 4: Testing - `cli_testing.py`**
**Focus**: Testing strategies for command-line tools

**Key Features:**
- **Unit Testing**: Testing CLI components in isolation
- **Mocking**: External dependencies (LLM APIs, file system)
- **Integration Testing**: End-to-end workflow validation
- **Error Scenarios**: Testing edge cases and failure modes

**Implementation TODOs:**
1. Test configuration loading and validation
2. Mock LLM clients for reliable testing
3. File system operation testing with temporary directories
4. CLI argument parsing and validation tests
5. Error handling and exit code testing

## 🛠️ CLI Design Principles

### **1. User Experience First**
```bash
# Good: Clear, intuitive commands
ai-doc document my_file.py

# Bad: Cryptic, hard to remember
ai-doc -m doc -f my_file.py -t rst
```

### **2. Fail Fast with Helpful Messages**
```bash
❌ Error: File 'missing.py' not found
💡 Did you mean: 'my_script.py'?
```

### **3. Consistent Patterns**
- Use same option names across subcommands (`--verbose`, `--output`)
- Consistent exit codes (0 = success, 1 = error, 130 = user cancel)
- Standard flag conventions (`-v` for verbose, `-h` for help)

### **4. Configuration Hierarchy**
```
Environment Variables  (highest priority)
    ↓
CLI Arguments
    ↓  
Config File
    ↓
Built-in Defaults     (lowest priority)
```

## 📚 CLI Framework Comparison

| Feature | argparse | click | typer |
|---------|----------|-------|-------|
| **Learning Curve** | Medium | Low | Low |
| **Dependencies** | None | click | typer, click |
| **Type Safety** | Manual | Decorators | Automatic |
| **Subcommands** | Verbose | Clean | Clean |
| **Testing** | Manual setup | Built-in | Built-in |
| **Auto Help** | Good | Excellent | Excellent |

### **When to Choose Each:**

**argparse**: 
- No external dependencies allowed
- Simple single-command tools
- Standard library solution

**click**:
- Most popular, huge ecosystem
- Complex multi-command tools
- Lots of documentation and examples

**typer**:
- Type hints and modern Python
- FastAPI-style development
- Automatic CLI generation from types

## 🎓 Extension Ideas

### **Immediate Improvements** (5-10 min each):
1. **Better Error Messages**: Add suggestions and context
2. **Command Aliases**: Short versions of common commands
3. **Auto-completion**: Shell completion for commands and files
4. **Colored Output**: Consistent color scheme for status messages

### **Feature Extensions** (15-30 min each):
1. **Watch Mode**: Monitor files and regenerate docs automatically
2. **Template System**: Custom documentation templates
3. **Integration**: Connect with VS Code, documentation sites
4. **Multi-language**: Support for JavaScript, TypeScript, etc.

### **Advanced Features** (1+ hour each):
1. **Plugin System**: User-installable extensions
2. **Distributed Processing**: Process large codebases in parallel
3. **Quality Metrics**: Score and improve documentation quality
4. **CI/CD Integration**: GitHub Actions, pre-commit hooks

## 🔍 Common CLI Patterns

### **Progress Indication**
```python
# Long operations need feedback
with Progress() as progress:
    task = progress.add_task("Processing...", total=len(files))
    for file in files:
        process_file(file)
        progress.advance(task)
```

### **Interactive Confirmations**
```python
# Dangerous operations need confirmation
if Confirm.ask("This will overwrite existing docs. Continue?"):
    proceed_with_operation()
```

### **Graceful Error Recovery**
```python
try:
    result = risky_operation()
except SpecificError as e:
    console.print(f"[red]Error:[/red] {e}")
    console.print("[yellow]Suggestion:[/yellow] Try running with --verbose")
    sys.exit(1)
```

### **Configuration Management**
```python
# Multiple configuration sources
config = merge_configs(
    defaults=DEFAULT_CONFIG,
    config_file=load_config_file(),
    env_vars=get_env_overrides(),
    cli_args=parse_args()
)
```

## 🚀 Production Deployment

### **Making Your CLI Installable**

1. **Package Structure**:
```
ai-doc-agent/
├── src/
│   └── ai_doc_agent/
│       ├── __init__.py
│       ├── cli.py
│       └── core/
├── tests/
├── setup.py
└── pyproject.toml
```

2. **Entry Points** (setup.py):
```python
entry_points={
    'console_scripts': [
        'ai-doc=ai_doc_agent.cli:main',
    ],
}
```

3. **Installation**:
```bash
pip install -e .  # Development install
pip install ai-doc-agent  # Production install
```

### **Distribution**
- **PyPI**: `twine upload dist/*`
- **GitHub Releases**: Automated with GitHub Actions
- **Homebrew**: For macOS users
- **Docker**: Containerized distribution

---

**🎉 Congratulations!** 

By completing all phases, you've learned:
- CLI argument parsing and validation
- Modern user interface design
- Configuration management
- Professional error handling
- Testing strategies
- Production deployment

Your CLI tool is now ready for real-world use and can serve as a template for future CLI projects!