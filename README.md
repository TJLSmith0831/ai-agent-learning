# AI Agent for Code Documentation - 2 Hour Learning Project

> **⚡ Fast Track Learning**: Build a working AI agent that generates code documentation in just 2 hours! This streamlined version focuses on hands-on implementation with immediate results.

## What You'll Learn

### Core AI Agent Concepts (In 2 Hours!)
- **Agent Architecture**: Perceive → Reason → Act pattern through direct implementation
- **AST Parsing**: Extract function information from Python code using built-in tools
- **LLM Integration**: Connect your agent to OpenAI, Anthropic, or local models
- **Prompt Engineering**: Write effective prompts that generate useful documentation

### Technical Skills You'll Gain
- **Python AST Module**: Parse code structure programmatically
- **API Integration**: Make real LLM calls with proper error handling  
- **Code Analysis**: Understand how to extract meaningful information from source code
- **Agent Design Patterns**: Build systems that can perceive, reason, and act

## Project Structure

```
ai-agent-learning/
├── simple_parser.py   # Step 1: Extract functions from code (20 min)
├── simple_agent.py    # Step 2: Build the AI agent pipeline (40 min) 
├── quick_start.py     # Testing & validation at each step
├── requirements.txt   # Dependencies for LLM integration
├── CLAUDE.md          # Guide for Claude Code users
└── README.md          # This file
```

## ⚡ 2-Hour Quick Start

### Step 1: Test Your Setup (5 minutes)
```bash
python quick_start.py
```
This validates your complete working agent!

### Step 2: Understand the Parser (10 minutes)
```bash
python simple_parser.py  # See function extraction in action
```

### Step 3: Explore the Agent (20 minutes) 
```bash
python simple_agent.py  # See complete agent pipeline
```

### Step 4: Add Real LLM (30-60 minutes)
- Get API key from OpenAI or Anthropic  
- Set environment variables (`OPENAI_API_KEY` or `ANTHROPIC_API_KEY`)
- Test with real LLM calls on your own Python files

### Step 5: Celebrate! (5 minutes)
You now have a working AI agent that can analyze code and generate documentation!

## 💡 Implementation Tips

### Start Simple, Test Often
```bash
# After every change, run this to see progress:
python quick_start.py
```

### Key Components to Understand
```python
# simple_parser.py - Extracts function information:
func_name = node.name
arg_names = [arg.arg for arg in node.args.args]  
docstring = ast.get_docstring(node)
```

## 🚨 Common Issues

- **Missing constants.py?** → Create it with `from enum import Enum; class LLMClient(Enum): OPENAI = "openai"; ANTHROPIC = "anthropic"`
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

## 🎯 Success Check

✅ **Project Status: COMPLETE & READY TO USE**

You'll know it's working when:
- [x] All files exist and run without errors
- [x] `python quick_start.py` demonstrates working agent pipeline  
- [x] Parser extracts functions from Python files
- [x] Agent can generate documentation (with API keys)

## 🚀 What's Next?

Once your basic agent works, you can expand it:
- Add class documentation support
- Process multiple files
- Connect with VS Code
- Build other types of code agents (testing, refactoring, etc.)

---

🚀 **Ready to build? Run**: `python quick_start.py`