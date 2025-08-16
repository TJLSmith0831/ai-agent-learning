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
├── simple_parser.py    # Function extraction from Python code
├── simple_agent.py     # AI agent pipeline implementation
├── quick_start.py      # Testing & validation utilities
├── requirements.txt    # Dependencies for LLM integration
├── enums.py           # Type definitions and configuration
│
├── CLI Tools:
├── cli_agent.py        # Basic CLI with argparse
├── interactive_cli.py  # Rich interactive CLI interface
├── config_manager.py   # Configuration management
├── cli_testing.py      # CLI testing utilities
├── CLI_GUIDE.md        # CLI development guide
│
└── README.md           # This file
```

## ⚡ Quick Start

### Step 1: Test Your Setup
```bash
python quick_start.py
```
Validates your complete working agent.

### Step 2: Run the Parser
```bash
python simple_parser.py
```
Demonstrates function extraction from Python code.

### Step 3: Run the Agent
```bash
python simple_agent.py
```
Shows the complete agent pipeline in action.

### Step 4: Add LLM Integration
- Get API key from OpenAI or Anthropic  
- Set environment variables (`OPENAI_API_KEY` or `ANTHROPIC_API_KEY`)
- Test with real LLM calls on your Python files

## 💡 Implementation Tips

### Start Simple, Test Often
```bash
# After every change, run this to see progress:
python quick_start.py
```

### Key Components
```python
# simple_parser.py - Extracts function information:
func_name = node.name
arg_names = [arg.arg for arg in node.args.args]  
docstring = ast.get_docstring(node)
```

## 🚨 Common Issues

- **Missing enums.py?** → Should contain LLMClient and DocumentationFormat enums
- **API errors?** → Set environment variables: `export OPENAI_API_KEY=your_key` 
- **Generic responses?** → Customize prompts in `simple_agent.py` reason() method

## 🔌 LLM Integration (Choose One)

### OpenAI (Recommended)
```python
# Add to simple_agent.py act() method:
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

### **CLI Tools**
Command-line interfaces for different use cases:

1. **Basic CLI** (`cli_agent.py`)
   - Argument parsing with argparse
   - Input validation and error handling
   - File I/O and output formatting

2. **Interactive CLI** (`interactive_cli.py`)
   - Rich text output with colors and formatting
   - Progress bars and user prompts
   - Professional CLI appearance

**📖 Complete Guide**: See [`CLI_GUIDE.md`](CLI_GUIDE.md) for detailed documentation

### **Extension Possibilities**
- Multi-language support (JavaScript, TypeScript, etc.)
- VS Code extension integration
- Documentation site generation
- CI/CD pipeline integration

---

🚀 **Get started**: `python quick_start.py`  
📋 **CLI documentation**: [`CLI_GUIDE.md`](CLI_GUIDE.md)