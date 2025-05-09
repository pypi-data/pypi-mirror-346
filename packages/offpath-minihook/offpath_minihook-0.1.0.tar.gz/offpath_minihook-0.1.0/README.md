# Offpath Mini-Hook

A lightweight security hook for LLM agents that provides real-time policy enforcement, interception, and monitoring.

## Quick Start

```python
# 1. Set API endpoint
import os
os.environ["OPENAI_API_BASE"] = "https://api.offpath.ai/v1"

# 2. Import Offpath
import offpath

# 3. Secure all tools
offpath.secure_all()
```

## Features

- Protection against tool misuse
- Prompt injection detection
- Policy enforcement
- Works with LangChain and OpenAI function calling

## Installation

```bash
pip install offpath-minihook
```

## Configuration

Set environment variables:

```bash
export OFFPATH_API_URL="https://api.offpath.ai"
export OFFPATH_API_KEY="your-api-key"
```

## Usage

### Securing LangChain

```python
import offpath
offpath.secure_langchain()
```

### Securing OpenAI

```python
import offpath
offpath.secure_openai()
```

### Securing Individual Functions

```python
from offpath import get_instance

offpath = get_instance()

@offpath.secure_tool("shell")
def run_command(cmd):
    import subprocess
    return subprocess.check_output(cmd, shell=True)
```
