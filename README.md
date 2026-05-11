# 💬 TalkAI Unlimited

A lightweight command-line chatbot that connects to [talkai.info](https://talkai.info) and lets you chat with multiple AI models — with conversation history, streaming responses, and clean output formatting.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow)
![requests](https://img.shields.io/badge/requests-latest-lightgrey)

---

## 🤖 Supported Models

| Flag | Model |
|---|---|
| `gpt` *(default)* | GPT-4.1 Nano |
| `deepseek` | DeepSeek Chat |
| `google` | Gemini 2.0 Flash Lite |
| `claude` | Claude 3 Haiku |

---

## ✨ Features

- Chat with GPT, DeepSeek, Gemini, or Claude from the terminal
- Streaming responses — output appears as it arrives
- Conversation history with configurable memory limit
- Smart spacing and newline handling for clean, readable output
- Skips model-name prefixes injected into the first response chunk
- Graceful error handling for network failures and bad responses
- `Ctrl+C` exits cleanly

---

## 🚀 Installation

```bash
git clone https://github.com/IMApurbo/talkai-unlimited.git
cd talkai-unlimited
pip install requests
```

---

## ▶️ Usage

```bash
python main.py
```

**With options:**

```bash
python main.py --model deepseek --limit 10
```

### Arguments

| Argument | Description | Default |
|---|---|---|
| `--model` | Model to use: `gpt`, `deepseek`, `google`, `claude` | `gpt` |
| `--limit` | Number of conversation pairs to remember (`0` = unlimited) | `0` |

---

## 💡 Examples

**Chat with DeepSeek, remembering last 5 exchanges:**
```bash
python main.py --model deepseek --limit 5
```

**Chat with Gemini, unlimited history:**
```bash
python main.py --model google
```

**Chat with Claude:**
```bash
python main.py --model claude
```

**In-chat commands:**

| Input | Action |
|---|---|
| `exit` or `quit` | End the session |
| `Ctrl+C` | Force quit |

---

## 📋 Requirements

```
requests
```

```bash
pip install requests
```

---

## 📁 Project Structure

```
talkai-unlimited/
├── main.py       # Main script
└── README.md
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👤 Author

**IMApurbo**  
GitHub: [@IMApurbo](https://github.com/IMApurbo)

---

> No API key needed. Just run and chat.
