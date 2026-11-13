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
    messages = [{"role": "system", "content": "You are JARVIS, a concise and helpful personal assistant. Never claim to have performed actions you did not perform."}]
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
