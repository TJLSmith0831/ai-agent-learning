# AI Agent for Code Documentation

> **⚡ Production Ready**: A working AI agent that generates code documentation using modern LLMs. Features multiple documentation formats and CLI interfaces.

## Features

### Core Capabilities
- **Agent Architecture**: Implements Perceive → Reason → Act pattern for code analysis
- **AST Parsing**: Extracts function information from Python code using built-in tools
- **LLM Integration**: Supports OpenAI, Anthropic, and local models
- **Multiple Formats**: Generate documentation in RST, Markdown, Google, NumPy, and more

### Technical Implementation
- **Python AST Module**: Programmatic code structure parsing
- **API Integration**: Real LLM calls with proper error handling  
- **Code Analysis**: Meaningful information extraction from source code
- **CLI Tools**: Multiple interfaces from basic to interactive

## Project Structure

```
ai-agent-learning/
├── CLAUDE.md            # Project instructions for Claude Code
├── requirements.txt     # Dependencies for LLM integration
│
├── doc_agent/           # Complete AI agent implementation
│   ├── CLI_GUIDE.md     # Comprehensive CLI development guide
│   ├── simple_parser.py # Function extraction from Python code
│   ├── simple_agent.py  # AI agent pipeline implementation
│   ├── quick_start.py   # Testing & validation utilities
│   ├── enums.py         # Type definitions and configuration
│   ├── cli_agent.py     # Basic CLI with argparse
│   ├── interactive_cli.py # Rich interactive CLI interface
│   ├── config_manager.py # Configuration management
│   └── testing/         # Test utilities
│
└── README.md            # This file
```

## ⚡ Quick Start

### Step 1: Test Your Setup
```bash
python doc_agent/quick_start.py
```
Validates your complete working agent.

### Step 2: Run the Parser
```bash
python doc_agent/simple_parser.py
```
Demonstrates function extraction from Python code.

### Step 3: Run the Agent
```bash
python doc_agent/simple_agent.py
```
Shows the complete agent pipeline in action.

### Step 4: Add LLM Integration
- Get API key from OpenAI or Anthropic  
- Set environment variables (`OPENAI_API_KEY` or `ANTHROPIC_API_KEY`)
- Test with real LLM calls on your Python files

### Step 5: CLI Development
```bash
# Start with basic CLI implementation
python doc_agent/cli_agent.py my_script.py --format markdown

# Progress to interactive CLI
python doc_agent/interactive_cli.py

# Add configuration management
ai-doc config --set default_llm openai
```

## 💡 Implementation Tips

### Start Simple, Test Often
```bash
# After every change, run this to see progress:
python doc_agent/quick_start.py
```

### Key Components
```python
# doc_agent/simple_parser.py - Extracts function information:
func_name = node.name
arg_names = [arg.arg for arg in node.args.args]  
docstring = ast.get_docstring(node)
```

## 🚨 Common Issues

- **Missing enums.py?** → Should contain LLMClient and DocumentationFormat enums
- **API errors?** → Set environment variables: `export OPENAI_API_KEY=your_key` 
- **Generic responses?** → Customize prompts in `doc_agent/simple_agent.py` reason() method

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

**argparse**: No external dependencies, simple single-command tools, standard library solution

**click**: Most popular, huge ecosystem, complex multi-command tools, lots of documentation

**typer**: Type hints and modern Python, FastAPI-style development, automatic CLI generation

## 🔌 LLM Integration (Choose One)

### OpenAI (Recommended)
```python
# Add to doc_agent/simple_agent.py act() method:
import openai
client = openai.OpenAI(api_key="your-key")
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=300
)
return response.choices[0].message.content
```

### Anthropic Claude
```python
import anthropic
client = anthropic.Anthropic(api_key="your-key")
response = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=300,
    messages=[{"role": "user", "content": prompt}]
)
return response.content[0].text
```

### Local (Free)
```bash
# Install Ollama: https://ollama.ai
ollama pull codellama
```

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

### **3. Configuration Hierarchy**
```
Environment Variables  (highest priority)
    ↓
CLI Arguments
    ↓  
Config File
    ↓
Built-in Defaults     (lowest priority)
```

## 🎯 Status Check

✅ **Project Status: PRODUCTION READY**

Working features:
- [x] All files exist and run without errors
- [x] `python quick_start.py` demonstrates working agent pipeline  
- [x] Parser extracts functions from Python files
- [x] Agent generates documentation (with API keys)

## 🚀 Usage

### **Core Agent**
✅ Working AI documentation agent with Perceive → Reason → Act pattern

### **CLI Development Guide**
Progressive implementation from basic to advanced CLI tools:

#### **Phase 1: Basic CLI** 
**Focus**: Argparse fundamentals and CLI structure
```bash
python doc_agent/cli_agent.py my_script.py --llm openai --format markdown
```
**Key Features**: Argument parsing, input validation, error handling, help documentation

#### **Phase 2: Interactive CLI**
**Focus**: Rich user experience with modern CLI libraries
```bash
python doc_agent/interactive_cli.py
```
**Key Features**: Rich text output, progress bars, interactive prompts, professional appearance

#### **Phase 3: Configuration Management**
**Focus**: User preferences and settings persistence
```bash
ai-doc config --show
ai-doc config --set default_llm anthropic
```
**Key Features**: Configuration hierarchy, cross-platform support, data validation

#### **Phase 4: Testing & Production**
**Focus**: Testing strategies and deployment
**Key Features**: Unit testing, mocking, integration testing, package distribution

**📖 Complete Guide**: See [`doc_agent/CLI_GUIDE.md`](doc_agent/CLI_GUIDE.md) for detailed implementation

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

### **Distribution Options**
- **PyPI**: `twine upload dist/*`
- **GitHub Releases**: Automated with GitHub Actions
- **Homebrew**: For macOS users
- **Docker**: Containerized distribution

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

---

🚀 **Get started**: `python quick_start.py`  
📋 **CLI documentation**: [`doc_agent/CLI_GUIDE.md`](doc_agent/CLI_GUIDE.md)