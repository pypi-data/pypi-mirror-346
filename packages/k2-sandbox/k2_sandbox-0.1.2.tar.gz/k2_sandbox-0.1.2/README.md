# K2 Sandbox

K2 Sandbox is a Python SDK for running LLM-generated code in isolated Docker container environments. It provides a secure way to execute untrusted code with filesystem access, network capabilities, and stateful execution.

## Features

- Secure code execution in isolated Docker containers
- Support for Python, JavaScript, and TypeScript execution
- Stateful execution (variable persistence between runs)
- File system operations
- Process management
- Terminal interaction

## Installation

```bash
pip install k2-sandbox
```

## Quick Start

```python
from k2_sandbox import Sandbox

# Optionally, set the API URL if needed
# This is useful if your API server is not at the default http://localhost:3000
# and you don't want to set it via environment variable or for every sandbox instance.
Sandbox.set_default_api_url("https://your-k2-api-server.com")

# Create and use a code interpreter sandbox
with Sandbox.create_code_interpreter() as sandbox:
    execution = sandbox.run_code("x = 41; x + 1")
    print(f"Result: {execution.text}")  # Output: 42
```

## Documentation

For detailed documentation, see the [API Reference](docs/api_reference.md).

## License

MIT
