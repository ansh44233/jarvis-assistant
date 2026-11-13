# J.A.R.V.I.S. — Personal Productivity Assistant

I built J.A.R.V.I.S. as a Python project to make everyday tasks easier to manage from one place. It has a terminal interface and a browser dashboard for notes, tasks, reminders, and a daily brief. I also added optional local AI chat using Ollama.

The app runs on your computer and stores your data in SQLite.

[Open the demo](https://ansh44233.github.io/jarvis-assistant/) · [View source code](https://github.com/ansh44233/jarvis-assistant)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![MIT License](https://img.shields.io/badge/License-MIT-green)

## Features

- Notes: add, search, list, and delete
- Tasks: create tasks, set due dates, and mark them complete
- Reminders: create one-time and recurring reminders
- Daily brief: see upcoming and overdue work
- Browser dashboard and terminal interface
- Optional AI chat with a local Ollama model
- Voice input and spoken replies in supported browsers
- Local SQLite storage and JSON export

## Demo

[Try the J.A.R.V.I.S. demo](https://ansh44233.github.io/jarvis-assistant/)

The public demo uses sample data in your browser. It is separate from the Python app and does not connect to your local database or Ollama.

## Tech stack

- Python 3.10+
- SQLite
- HTML, CSS, JavaScript
- Ollama (optional)

The core app uses Python's standard library and has no required third-party runtime dependencies.

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/ansh44233/jarvis-assistant.git
cd jarvis-assistant
```

**2. Create a virtual environment**

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**3. Install and run**

```bash
python -m pip install -e .
jarvis
```

To open the browser dashboard instead:

```bash
jarvis --web
```

Then open http://127.0.0.1:8765.

## Commands

| Command | Description |
|---|---|
| `note <text>` | Save a note |
| `notes` | List notes |
| `find <word>` | Search notes |
| `task <text> [when]` | Create a task |
| `tasks` | List tasks |
| `done <id>` | Complete a task |
| `remind me <text> <when>` | Create a reminder |
| `reminders` | List reminders |
| `brief` | Show the daily brief |
| `chat <message>` | Chat with the local AI model |
| `delete note <id>` | Delete a note |
| `delete task <id>` | Delete a task |
| `delete reminder <id>` | Delete a reminder |
| `help` | Show help |

Example:

```text
note Learn Python decorators
task Finish my assignment tomorrow
remind me to take a break in 30 minutes
brief
```

## Optional AI setup

To use AI chat, install [Ollama](https://ollama.com/), start it, and download a model such as `qwen2.5:3b`. Then run J.A.R.V.I.S. and use the `chat` command.

AI is optional. Notes, tasks, reminders, and the dashboard work without it.

## Project structure

```text
jarvis-assistant/
├── demo/
├── jarvis/
│   ├── ai.py
│   ├── assistant.py
│   ├── cli.py
│   ├── store.py
│   ├── timeparse.py
│   └── web.py
├── tests/
├── .github/
├── LICENSE
└── pyproject.toml
```

## Tests

Run the tests with:

```bash
python -m unittest discover -s tests -t . -v
```

## A few things to know

- Data is stored locally in `~/.jarvis/jarvis.db` by default.
- AI prompts go to the Ollama server configured on your computer.
- The browser dashboard is intended for local use; don't expose it directly to the public internet.
- The public demo is separate and uses sample data.

## License

MIT — see [LICENSE](LICENSE).

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=ansh44233/jarvis-assistant&type=Date)](https://star-history.com/#ansh44233/jarvis-assistant&Date)

---

Made by **Ansh**.
