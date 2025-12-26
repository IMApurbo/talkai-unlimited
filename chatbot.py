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

# Available models
MODELS = {
    "deepseek": "deepseek-chat",
    "google": "gemini-2.0-flash-lite",
    "claude": "claude-3-haiku-20240307",
    "gpt": "gpt-4.1-nano"
}

def generate_message_id():
    return str(uuid.uuid4())

def get_limited_history(messages_history, limit):
    """Return only the last 'limit' pairs of messages (user + bot)"""
    if limit <= 0:
        return messages_history
    
    # Keep only the last (limit * 2) messages to preserve conversation pairs
    max_messages = limit * 2
    if len(messages_history) > max_messages:
        return messages_history[-max_messages:]
    return messages_history

def chat(model_name, history_limit):
    messages_history = []
    print(f"Chat started with model: {model_name}")
    if history_limit > 0:
        print(f"History limit: {history_limit} conversation pairs")
    else:
        print("History limit: unlimited")
    print("Type 'exit' or 'quit' to stop.\n")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        if not user_input:
            continue
        
        # Add user message to history
        messages_history.append({
            "id": generate_message_id(),
            "from": "you",
            "content": user_input,
            "model": ""
        })
        
        # Get limited history if specified
        limited_history = get_limited_history(messages_history, history_limit)
        
        payload = {
            "type": "chat",
            "messagesHistory": limited_history,
            "settings": {
                "model": model_name,
                "temperature": 0.7
            }
        }
        
        try:
            response = requests.post(
                URL,
                headers=HEADERS,
                json=payload,
                stream=True,
                timeout=60
            )
            
            if response.status_code != 200:
                print(f"Error: HTTP {response.status_code}")
                print(response.text)
                messages_history.pop()
                continue
            
            full_response = ""
            first_chunk = True
            
            for line in response.iter_lines(decode_unicode=True):
                if not line:
                    continue
                line = line.strip()
                if line.startswith("data: "):
                    data = line[6:].strip()
                    if data:
                        # Skip the first chunk if it contains the model name
                        if first_chunk:
                            # Check for various model name prefixes
                            skip_prefixes = ["GPT", "DeepSeek", "Gemini", "Claude"]
                            should_skip = False
                            for prefix in skip_prefixes:
                                if prefix in data:
                                    parts = data.split(None, 3)
                                    if len(parts) > 3:
                                        data = parts[3]
                                    else:
                                        should_skip = True
                                    break
                            first_chunk = False
                            if should_skip:
                                continue
                        
                        # Skip numerical chunks (token count)
                        if data.isdigit():
                            continue
                        
                        full_response += data + " "
            
            # Display complete response at once
            if full_response.strip():
                print(f"Bot: {full_response.strip()}\n")
                messages_history.append({
                    "id": generate_message_id(),
                    "from": "chatGPT",
                    "content": full_response.strip(),
                    "model": model_name
                })
            else:
                print("[No response content received]\n")
                messages_history.pop()
                
        except requests.exceptions.RequestException as e:
            print(f"\nRequest failed: {e}")
            messages_history.pop()
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            messages_history.pop()

def main():
    parser = argparse.ArgumentParser(
        description="Chat with AI models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available models:
  deepseek  - DeepSeek Chat
  google    - Gemini 2.0 Flash Lite
  claude    - Claude 3 Haiku
  gpt       - GPT 4.1 Nano (default)

Examples:
  python script.py --model deepseek
  python script.py --model google --limit 5
  python script.py --limit 10
        """
    )
    
    parser.add_argument(
        "--model",
        type=str,
        choices=MODELS.keys(),
        default="gpt",
        help="Select AI model (default: gpt)"
    )
    
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Number of conversation pairs to remember (0 = unlimited, default: 0)"
    )
    
    args = parser.parse_args()
    
    model_name = MODELS[args.model]
    history_limit = args.limit
    
    try:
        chat(model_name, history_limit)
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()
