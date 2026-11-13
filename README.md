<div align="center">

# J.A.R.V.I.S.

### Your personal command center.

A local-first productivity assistant built with Python. Organize notes, tasks and reminders, get a daily brief, and chat with an optional local AI model.

[**🚀 Launch Live Demo**](https://ansh44233.github.io/jarvis-assistant/) · [**Browse Source**](https://github.com/ansh44233/jarvis-assistant) · [**Report an Issue**](https://github.com/ansh44233/jarvis-assistant/issues)

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/Storage-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Beta-f59e0b?style=for-the-badge)

</div>

---

## ✦ About

J.A.R.V.I.S. brings everyday productivity into one focused workspace. Use the terminal or browser dashboard to capture ideas, track tasks, manage reminders and review what's next.

The core app runs on your computer and stores its data in SQLite. Optional AI chat can connect to [Ollama](https://ollama.com/) for local model inference.

> **Two experiences, clearly separated:** the public website is an interactive demo with sample data. The Python app is the local application that stores your own workspace on your computer.

## ✦ Live demo

<div align="center">

### [Open J.A.R.V.I.S. Command Center →](https://ansh44233.github.io/jarvis-assistant/)

</div>

The public demo runs in your browser and requires no installation. Its notes, tasks and reminders are sample workspace data saved in browser storage. Optional AI chat uses a separate Cloudflare Worker backend. The hosted demo cannot access your computer, files, local SQLite database or local Ollama instance. Microphone features depend on browser support and permission.

## ✦ Features

| Feature | Description |
|---|---|
| **Notes** | Create, list, search and delete notes |
| **Tasks** | Add tasks, set due dates and mark work complete |
| **Reminders** | Create one-time and recurring reminders |
| **Daily brief** | Review upcoming and overdue work |
| **Browser dashboard** | Manage your workspace in a browser |
| **Terminal interface** | Use quick commands from your shell |
| **Optional AI chat** | Connect a local Ollama model |
| **Voice interaction** | Voice input and spoken replies in supported browsers |
| **Local persistence** | SQLite storage and JSON export |

## ✦ Quick start

### Requirements

- Python 3.10+
- Windows, macOS or Linux
- Ollama only if you want local AI chat

### 1. Clone

```bash
git clone https://github.com/ansh44233/jarvis-assistant.git
cd jarvis-assistant
```

### 2. Create a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install

```bash
python -m pip install -e .
```

### 4. Run

Start the terminal assistant:

```bash
jarvis
```

Start the browser dashboard instead:

```bash
jarvis --web
```

Then open **http://127.0.0.1:8765**.

## ✦ Command guide

| Command | What it does |
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
| `help` | Show all commands |

Example:

```text
note Explore Python automation
task Finish my portfolio tomorrow
remind me to take a break in 30 minutes
brief
```

## ✦ Optional local AI setup

AI is optional — notes, tasks, reminders and the dashboard work without it.

1. Install [Ollama](https://ollama.com/).
2. Download a model:

   ```bash
   ollama pull qwen2.5:3b
   ```

3. Start J.A.R.V.I.S. and use `chat <message>`.

For the separate AI backend used by the public demo, see the [Worker setup guide](worker/README.md).

## ✦ Tech stack

- **Python** — core assistant and CLI
- **SQLite** — local database
- **HTML, CSS, JavaScript** — browser dashboard and public demo
- **Ollama** — optional local AI
- **Cloudflare Workers AI** — optional public-demo chat backend
- **GitHub Actions + Pages** — checks and demo deployment

The core Python app uses the standard library and has no required third-party runtime dependencies.

## ✦ Project structure

```text
jarvis-assistant/
├── demo/                  # Public browser demo
├── jarvis/                # Python application
│   ├── ai.py              # Optional AI integration
│   ├── assistant.py       # Assistant logic
│   ├── cli.py             # Terminal commands
│   ├── store.py            # SQLite persistence
│   ├── timeparse.py        # Date/time parsing
│   └── web.py              # Local browser dashboard
├── worker/                # Public demo AI backend
├── tests/                 # Automated tests
├── .github/workflows/     # CI and deployment
├── LICENSE
├── README.md
└── pyproject.toml
```

## ✦ Tests

Run the test suite from the project root:

```bash
python -m unittest discover -s tests -t . -v
```

## ✦ Privacy & security

- Local app data is stored at `~/.jarvis/jarvis.db` by default.
- Prompts for local AI chat are sent to the Ollama server configured on your computer.
- Do not expose the local dashboard directly to the public internet without suitable security controls.
- The public demo is separate and uses sample workspace data in browser storage.
- The public AI endpoint may consume your Cloudflare Workers AI quota.
- Never commit API tokens, credentials or other secrets to the repository.

## ✦ Roadmap

- [ ] More dashboard customisation
- [ ] Better task filtering and organisation
- [ ] Expanded voice interaction
- [ ] More automated tests and accessibility improvements

Ideas and contributions are welcome — open an [issue](https://github.com/ansh44233/jarvis-assistant/issues).

## ✦ Star history

If you like the project, consider giving it a ⭐.

[![Star History Chart](https://api.star-history.com/svg?repos=ansh44233/jarvis-assistant&type=Date)](https://star-history.com/#ansh44233/jarvis-assistant&Date)

---

<div align="center">

**Built with focus by Ansh.**

[Live Demo](https://ansh44233.github.io/jarvis-assistant/) · [GitHub](https://github.com/ansh44233/jarvis-assistant) · [MIT License](LICENSE)

</div>
