import requests
import uuid
import sys
import argparse

URL = "https://talkai.info/chat/send/"
HEADERS = {
    "Host": "talkai.info",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "application/json, text/event-stream",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Referer": "https://talkai.info/chat/",
    "Content-Type": "application/json",
    "Origin": "https://talkai.info",
    "Connection": "close",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=0",
}

MODELS = {
    "deepseek": "deepseek-chat",
    "google": "gemini-2.0-flash-lite",
    "claude": "claude-3-haiku-20240307",
    "gpt": "gpt-4.1-nano"
}

def generate_message_id():
    return str(uuid.uuid4())

def get_limited_history(messages_history, limit):
    if limit <= 0:
        return messages_history
    max_messages = limit * 2
    return messages_history[-max_messages:] if len(messages_history) > max_messages else messages_history

def chat(model_name, history_limit):
    messages_history = []
    print(f"Chat started with model: {model_name}")
    print(f"History limit: {history_limit if history_limit > 0 else 'unlimited'} conversation pairs")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        if not user_input:
            continue

        messages_history.append({"id": generate_message_id(), "from": "you", "content": user_input, "model": ""})
        limited_history = get_limited_history(messages_history, history_limit)

        payload = {
            "type": "chat",
            "messagesHistory": limited_history,
            "settings": {"model": model_name, "temperature": 0.7}
        }

        try:
            response = requests.post(URL, headers=HEADERS, json=payload, stream=True, timeout=60)
            if response.status_code != 200:
                print(f"Error: HTTP {response.status_code}\n{response.text}")
                messages_history.pop()
                continue

            full_response = ""
            first_chunk = True

            for line in response.iter_lines(decode_unicode=True):
                if not line:
                    continue
                line = line.strip()
                if not line.startswith("data: "):
                    continue

                data = line[6:].strip()
                if not data:
                    continue

                # Skip model name in first chunk
                if first_chunk:
                    skip_prefixes = ["GPT", "DeepSeek", "Gemini", "Claude"]
                    if any(prefix in data for prefix in skip_prefixes):
                        parts = data.split(None, 3)
                        if len(parts) > 3:
                            data = parts[3]
                        else:
                            data = ""
                    first_chunk = False

                if data.isdigit():
                    continue

                # Fix \n and smart spacing
                data = data.replace("\\n", "\n")

                # Smart space insertion
                if full_response and full_response[-1] not in " \n\t.!?,:;，。！？；：”)]}" and \
                   data[0] not in " \n\t.!?,:;，。！？；：“([{":
                    full_response += " " + data
                else:
                    full_response += data

            # Print clean response
            if full_response.strip():
                print(f"Bot:\n{full_response.strip()}\n")
                messages_history.append({
                    "id": generate_message_id(),
                    "from": "chatGPT",
                    "content": full_response.strip(),
                    "model": model_name
                })
            else:
                print("[No response received]\n")
                messages_history.pop()

        except requests.exceptions.RequestException as e:
            print(f"\nRequest failed: {e}")
            messages_history.pop()
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            messages_history.pop()

def main():
    parser = argparse.ArgumentParser(description="TalkAI Unlimited - Fixed spacing & newlines",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog="""
Models: deepseek | google | claude | gpt (default)
Example: python talkai.py --model deepseek --limit 10
""")
    parser.add_argument("--model", choices=MODELS.keys(), default="gpt", help="Model (default: gpt)")
    parser.add_argument("--limit", type=int, default=0, help="Conversation pairs to remember (0 = unlimited)")
    args = parser.parse_args()

    chat(MODELS[args.model], args.limit)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
