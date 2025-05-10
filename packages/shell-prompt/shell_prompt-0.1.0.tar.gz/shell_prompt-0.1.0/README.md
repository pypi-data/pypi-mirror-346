# 🐚 shell-prompt

**shell-prompt** is a command-line tool that translates natural language instructions into executable shell commands using an LLM. It supports multiple LLM providers (like OpenAI, Anthropic, Google Gemini, etc.) and adapts to the user's operating system.

#### Usage example:

- USER INPUT: 
```bash
shell-prompt "list all files in my Desktop directory"
```
- OUTPUT:
```bash
Command to run:  
dir "%UserProfile%\Desktop"  
Execute this command? [y/N]: y  
Running command: dir "%UserProfile%\Desktop"  
*Command output here*
```

---

## 🚀 Features

- Converts natural language into shell commands
- Supports execution and preview mode
- Compatible with Windows, Linux, and macOS
- Extensible to multiple LLM providers via `langchain`
- Lightweight and configurable

---

## 📦 Installation

You can install it from your local build or via PyPI.

### Installation should be done with a specific LLM provider, such as:
```bash
pip install shell-prompt[google-genai]
```

### List of supported providers:

- openai
- anthropic
- google-genai
- groq
- cohere
- langchain-nvidia-ai-endpoints
- fireworks
- mistralai
- together
- langchain-xai
- langchain-perplexity

## 🛠 Usage

Once installed, you should first configure the tool. Available options are:

| Option                                  | Description                                                                   |
| --------------------------------------- | ------------------------------------------------------------------------------|
| `-h`, `--help`                          | Show the help message and exit                                                |
| `--version`                             | Show the program's version number and exit                                    |
| `--config`                              | Show the current configuration                                                |
| `--set-provider PROVIDER_NAME`          | Set the LLM provider                                                          |
| `--set-model MODEL_NAME`                | Set the specific model to use                                                 |
| `--set-api-key API_KEY`                 | Set the API key for the currently selected provider                           |
| `--preview`, `--no-preview`             | Enable or disable preview mode (avoid instant execution - enabled by deafult) |

---

Example:
```bash
shell-prompt --set-provider google-genai --set-model "gemini-2.0-flash" --set-api-key APIKEY --no-preview
```
Print out the configuration:
```bash
shell-prompt --config
```
Run the tool:
```bash
shell-prompt "show current time, but only the seconds"
```
```bash
Running command: powershell Get-Date -Format ss
39
```
