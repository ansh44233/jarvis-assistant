import json
import unittest
from unittest.mock import patch
from jarvis.ai import chat
class FakeResponse:
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def read(self): return json.dumps({"message":{"content":"Hello from local JARVIS"}}).encode()
class AITests(unittest.TestCase):
    @patch("jarvis.ai.urlopen", return_value=FakeResponse())
    def test_chat_uses_local_ollama_api(self, mocked):
        self.assertEqual(chat("hello",[{"role":"user","content":"previous"}]),"Hello from local JARVIS")
        request=mocked.call_args.args[0]
        self.assertTrue(request.full_url.endswith("/api/chat"))
        self.assertEqual(json.loads(request.data)["messages"][-1]["content"],"hello")
if __name__ == "__main__": unittest.main()
