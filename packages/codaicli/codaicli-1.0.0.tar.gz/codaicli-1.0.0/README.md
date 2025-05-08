# Codaicli

[![PyPI version](https://badge.fury.io/py/CodaiCLI.svg)](https://badge.fury.io/py/CodaiCLI)
[![Python Versions](https://img.shields.io/pypi/pyversions/CodaiCLI.svg)](https://pypi.org/project/CodaiCLI/)
[![Tests](https://github.com/chafficui/CodaiCLI/actions/workflows/test.yml/badge.svg)](https://github.com/chafficui/CodaiCLI/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/chafficui/CodaiCLI/branch/main/graph/badge.svg)](https://codecov.io/gh/chafficui/CodaiCLI)

An AI-powered CLI assistant for managing and editing software projects using natural language.

## Features

- 🤖 Multi-provider AI support:
  - OpenAI
  - Google Gemini
  - Anthropic Claude
- ⚙️ Interactive configuration system
- 🔒 Command confirmation for safety
- 📁 Smart file analysis
- 🎯 Natural language project management

## Installation

```bash
# Basic installation
pip install codaicli

# Install with all dependencies
pip install "codaicli[all]"
```

## Quick Start

1. Navigate to your project directory:
```bash
cd your-project
```

2. Run Codaicli:
```bash
codaicli
```

3. Start interacting with your project using natural language!

## Configuration

Run the configuration wizard:
```bash
codaicli configure
```

### API Keys

You'll need API keys for the AI providers you want to use:

- [OpenAI API Key](https://platform.openai.com/api-keys)
- [Google AI Studio API Key](https://makersuite.google.com/app/apikey)
- [Anthropic API Key](https://console.anthropic.com/settings/keys)

### Interactive Configuration

The configuration wizard will guide you through:
1. Setting up API keys
2. Selecting default AI provider
3. Choosing models for each provider
4. Managing configuration profiles

## Commands

Within Codaicli:
- `use openai/gemini/claude` - Switch AI provider
- `help` - Show help information
- `clear` - Clear screen
- `exit` (or `quit`, `q`) - Exit CodaiCLI

## Ignored Files

Create a `.codaiignore` file to specify files and directories to ignore:
```
# Ignore specific files
secrets.txt
*.env

# Ignore directories
node_modules/
venv/
```

## Troubleshooting

### Common Issues

1. **API Key Errors**
   - Verify your API keys are correctly configured
   - Check provider status pages:
     - [OpenAI Status](https://status.openai.com)
     - [Google AI Status](https://status.cloud.google.com)
     - [Anthropic Status](https://status.anthropic.com)

2. **Model Not Found**
   - Ensure you have access to the selected model
   - Check model availability in your region

3. **Installation Issues**
   - Ensure Python 3.8+ is installed
   - Try installing in a virtual environment

4. **Permission Errors**
   - Check file permissions
   - Run with appropriate privileges

## Security Note

- All changes and command executions require user confirmation
- API keys are stored locally in your user directory
- Use `.codaiignore` to protect sensitive files
- No sensitive data is collected or transmitted

## Dependencies

- Python 3.7+
- OpenAI Python SDK
- Google Generative AI SDK
- Anthropic Python SDK
- Rich (for terminal formatting)
- Typer (for CLI interface)
- PyYAML (for configuration)

## License

MIT License - See LICENSE file for details