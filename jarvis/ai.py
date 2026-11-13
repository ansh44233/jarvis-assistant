"""Optional local AI chat powered by Ollama; core JARVIS stays dependency-free."""
from __future__ import annotations

import json
import os
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen


class OllamaError(RuntimeError):
    pass


def chat(prompt: str, history: list[dict[str, str]] | None = None) -> str:
    """Send a chat turn to a locally running Ollama instance."""
    base = os.environ.get("JARVIS_OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
    model = os.environ.get("JARVIS_MODEL", "qwen2.5:3b")
    messages = [{"role": "system", "content": "You are JARVIS, a natural, friendly, capable personal assistant. Speak like a real conversational assistant, not a command parser. Reply directly to greetings and casual messages; if the user says hi, greet them and ask how you can help. Understand informal English, common Hinglish, typos, and short messages when possible. Keep simple replies brief and clear. For complex requests, explain in useful steps. Use conversation history for context. Do not say you did not catch a message unless it is genuinely unintelligible. Never claim to have performed actions you did not perform. You can manage notes, tasks, and reminders only through available JARVIS commands; if asked to do something outside those capabilities, explain the limitation honestly."}]
    messages.extend(history or [])
    messages.append({"role": "user", "content": prompt})
    payload = json.dumps({"model": model, "messages": messages, "stream": False}).encode()
    req = Request(f"{base}/api/chat", data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urlopen(req, timeout=90) as response:
            data = json.loads(response.read().decode("utf-8"))
        return str(data["message"]["content"]).strip()
    except (URLError, HTTPError, TimeoutError, KeyError, ValueError) as exc:
        raise OllamaError("Local AI is unavailable. Start Ollama and pull the configured model.") from exc
