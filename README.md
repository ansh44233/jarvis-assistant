<div align="center">

# J.A.R.V.I.S.

### Your personal command center — private, lightweight, and local-first.

A Python productivity assistant for notes, tasks, reminders, and optional local AI conversations. Use it from your terminal or a browser dashboard, with your workspace stored in SQLite on your own machine.

<p>
  <a href="https://ansh44233.github.io/jarvis-assistant/"><strong>▶ Try the interactive demo</strong></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/ansh44233/jarvis-assistant">View source</a>
  &nbsp;·&nbsp;
  <a href="#-quick-start">Get started</a>
</p>

<p>
  <a href="https://github.com/ansh44233/jarvis-assistant/actions/workflows/ci.yml"><img src="https://github.com/ansh44233/jarvis-assistant/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/ansh44233/jarvis-assistant/actions/workflows/pages.yml"><img src="https://github.com/ansh44233/jarvis-assistant/actions/workflows/pages.yml/badge.svg" alt="GitHub Pages deployment"></a>
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/Core%20dependencies-None-16a34a" alt="No core dependencies">
  <img src="https://img.shields.io/badge/Storage-SQLite-003B57?logo=sqlite&logoColor=white" alt="SQLite">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-64748b" alt="MIT License"></a>
  <a href="https://github.com/ansh44233/jarvis-assistant/stargazers"><img src="https://img.shields.io/github/stars/ansh44233/jarvis-assistant?style=social" alt="GitHub stars"></a>
</p>

</div>

---

## ✨ What is J.A.R.V.I.S.?

J.A.R.V.I.S. is a lightweight personal productivity assistant built around one principle: **your everyday workspace should stay useful, understandable, and under your control.**

It combines a command-line interface with a browser dashboard. Save notes, organize tasks, schedule reminders, review a daily brief, and optionally chat with a model running locally through [Ollama](https://ollama.com/).

The core application uses Python's standard library and SQLite. No hosted AI account is required for its core productivity features.

> **Try before installing:** [Open the interactive browser demo](https://ansh44233.github.io/jarvis-assistant/). It runs with sample data in your browser and does not connect to your personal JARVIS database.

## 🚀 Highlights

| Feature | What it offers |
|---|---|
| 📝 Notes | Save, list, search, and delete notes |
| ✅ Tasks | Create tasks, add due dates, list open work, and mark tasks complete |
| ⏰ Reminders | Schedule one-time, daily, and weekly reminders |
| ☀️ Daily brief | Review overdue and upcoming work at a glance |
| 🖥️ Browser dashboard | Responsive dark dashboard with quick actions and workspace counters |
| 🤖 Optional local AI | Chat through an Ollama model running on your machine |
| 🎙️ Browser voice input | Speech recognition where supported by the browser |
| 🔊 Spoken replies | Optional browser speech synthesis |
| 💾 Local persistence | Store notes, tasks, reminders, and recent chat history in SQLite |
| 📦 JSON export | Export your workspace to a portable JSON file |
| 🧪 Automated tests | Run the test suite locally and through GitHub Actions |

### Why local-first?

- **Your data stays yours:** the database is stored on your device.
- **No mandatory AI service:** AI chat is optional; the core organizer works without it.
- **Small runtime footprint:** no third-party Python runtime dependencies for core features.
- **Understandable code:** a compact Python codebase with separate modules for routing, storage, date parsing, AI, and the dashboard.

## 🧭 Live demo

**[Launch the J.A.R.V.I.S. interactive demo →](https://ansh44233.github.io/jarvis-assistant/)**

The public demo is intentionally separate from the real application. It uses temporary sample data and simulates notes, tasks, reminders, and the daily brief entirely in the browser. It does not access a user's local database, connect to Ollama, or send commands to a hosted Python server.

To try it, enter `help`, then test commands such as:

```text
note Explore Python automation
task Finish portfolio tomorrow
remind me to take a break in 30 minutes
brief
notes
tasks
```

The full Python dashboard is different: it runs on your own machine at `http://127.0.0.1:8765`.

## 🧰 Tech stack

- **Language:** Python 3.10+
- **Persistence:** SQLite
- **Web interface:** HTML, CSS, vanilla JavaScript, Python standard-library HTTP server
- **Optional AI:** Ollama local HTTP API
- **Automation:** GitHub Actions
- **Public demo hosting:** GitHub Pages

## ⚡ Quick start

### Requirements

- Python **3.10 or newer**
- Git
- Ollama only if you want optional local AI chat

### 1. Clone the project

```bash
git clone https://github.com/ansh44233/jarvis-assistant.git
cd jarvis-assistant
```

### 2. Create a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

The core application has no third-party runtime dependencies.

### 4. Run J.A.R.V.I.S.

Start the interactive terminal assistant:

```bash
jarvis
```

Run a single command:

```bash
jarvis "note Explore Python automation"
jarvis tasks
```

Launch the browser dashboard:

```bash
jarvis --web
```

Then open **http://127.0.0.1:8765** in your browser.

## 🖥️ Browser dashboard

The built-in dashboard provides:

- A command console for interacting with J.A.R.V.I.S.
- Workspace counters for notes, open tasks, reminders, and chat history
- Quick actions for common commands
- Browser speech input where supported
- Optional spoken replies using browser speech synthesis

The dashboard is served by the local Python application. By default, it binds to `127.0.0.1`, so it is reachable only from your own computer.

## 🤖 Optional local AI with Ollama

AI chat is optional. J.A.R.V.I.S. can send prompts to an Ollama server that you run and configure locally.

1. Install [Ollama](https://ollama.com/).
2. Start Ollama and download a model that your computer can run.
3. For example, pull `qwen2.5:3b`.
4. Start J.A.R.V.I.S. and enter a command such as:

```text
chat Explain recursion with a simple example
```

If Ollama is unavailable, notes, tasks, reminders, the daily brief, export, and the browser dashboard remain usable.

## ⌨️ Command reference

| Command | Description | Example |
|---|---|---|
| `note <text>` | Save a note | `note Read about Python decorators` |
| `notes` | List saved notes | `notes` |
| `find <word>` | Search notes | `find Python` |
| `task <text> [when]` | Create a task with an optional due date | `task Finish assignment tomorrow` |
| `tasks` | List open tasks | `tasks` |
| `done <id>` | Mark a task complete | `done 2` |
| `remind me <text> <when>` | Create a reminder | `remind me to stretch in 30 minutes` |
| `reminders` | List pending reminders | `reminders` |
| `brief` | Show your daily brief | `brief` |
| `chat <message>` | Ask the local AI model | `chat Summarize this idea` |
| `delete note <id>` | Delete a note | `delete note 1` |
| `delete task <id>` | Delete a task | `delete task 2` |
| `delete reminder <id>` | Delete a reminder | `delete reminder 3` |
| `help` | Show command help | `help` |
| `quit` | Exit interactive mode | `quit` |

Commands are handled by J.A.R.V.I.S.'s intent router. It does not execute arbitrary shell commands from chat.

## 📅 Dates and recurring reminders

The date parser supports relative days, weekdays, explicit dates, 12/24-hour times, relative durations, and daily or weekly repeats.

```text
task Submit the project tomorrow
task Prepare presentation friday at 6pm
remind me to take a break in 45 minutes
remind me to review my notes every day at 9pm
remind me to call home every sunday at 8pm
```

Date-only reminders are scheduled for **9:00 AM**. Invalid calendar dates and out-of-range clock times are rejected.

## ⚙️ Configuration

| Environment variable | Default | Purpose |
|---|---|---|
| `JARVIS_DB` | `~/.jarvis/jarvis.db` | SQLite database path |
| `JARVIS_NAME` | `boss` | Name shown in the daily brief |
| `JARVIS_OLLAMA_URL` | `http://127.0.0.1:11434` | Ollama server endpoint |
| `JARVIS_MODEL` | `qwen2.5:3b` | Model used for AI chat |

You can also choose a database path with the CLI's `--db` option.

## 🏗️ Architecture

The application keeps its main responsibilities separated:

```mermaid
flowchart TD
    U[User] --> CLI[Command Line Interface]
    U --> WEB[Browser Dashboard]
    CLI --> CORE[Assistant Router]
    WEB --> CORE
    CORE --> TIME[Date and Time Parser]
    CORE --> STORE[SQLite Store]
    CORE --> AI[Optional Ollama Client]
    STORE --> DB[(Local SQLite Database)]
    AI --> MODEL[Local Ollama Model]
```

| Module | Responsibility |
|---|---|
| `assistant.py` | Routes commands and coordinates features |
| `cli.py` | CLI entry point and dashboard launcher |
| `timeparse.py` | Parses dates, times, and recurring reminders |
| `store.py` | SQLite persistence and data export |
| `ai.py` | Optional Ollama integration |
| `web.py` | Local browser dashboard and HTTP endpoints |

### Repository layout

```text
jarvis-assistant/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── pages.yml
├── demo/
│   └── index.html
├── jarvis/
│   ├── __init__.py
│   ├── __main__.py
│   ├── ai.py
│   ├── assistant.py
│   ├── cli.py
│   ├── store.py
│   ├── timeparse.py
│   └── web.py
├── tests/
├── LICENSE
├── pyproject.toml
└── README.md
```

## 🔐 Privacy and security

- Notes, tasks, reminders, and conversation history are stored in a local SQLite database.
- On POSIX systems, J.A.R.V.I.S. restricts the database file to owner-only read/write permissions when created or opened.
- Core productivity features do not need an internet connection after installation.
- Optional AI prompts are sent to the Ollama endpoint you configure.
- The local dashboard binds to localhost by default and does **not** include authentication.
- Database files and JSON exports may contain personal information; do not commit them to a public repository.

**Do not expose the local Python dashboard directly to the public internet.** It is designed for personal localhost use, not as a multi-user hosted service. The public GitHub Pages demo is a separate simulation with sample data.

## 🧪 Development and testing

Run the test suite from the repository root:

```bash
python -m unittest discover -s tests -t . -v
```

Compile the application and tests:

```bash
python -m compileall -q jarvis tests
```

The tests cover command handling, task and reminder behavior, date parsing, SQLite persistence, and the Ollama client. AI client tests use mocked HTTP responses, so Ollama is not required to run the test suite.

GitHub Actions runs the test suite across Python 3.10, 3.11, 3.12, and 3.13.

## 🌐 Hosting the demo

The public demo is a static site in `demo/`. The workflow at `.github/workflows/pages.yml` deploys it to GitHub Pages whenever the demo or workflow changes on `main`.

If Pages has not been enabled for the repository yet:

1. Open **Settings → Pages** in this GitHub repository.
2. Under **Build and deployment**, choose **GitHub Actions** as the source.
3. Open the **Actions** tab and run **Deploy public demo to GitHub Pages** (or push a change to `demo/`).
4. When the deployment workflow succeeds, the demo is available at:

   **https://ansh44233.github.io/jarvis-assistant/**

## ⭐ Star History

If you find the project useful, consider giving it a star. It helps others discover the repository.

[![Star History Chart](https://api.star-history.com/svg?repos=ansh44233/jarvis-assistant&type=Date)](https://star-history.com/#ansh44233/jarvis-assistant&Date)

## 🗺️ Roadmap

- [ ] More flexible natural-language command parsing.
- [ ] Richer dashboard views and task organization.
- [ ] Additional export and backup options.
- [ ] More configurable assistant preferences.
- [ ] Expanded end-to-end and dashboard test coverage.
- [ ] Optional authenticated remote access, designed separately from the local-first core.

These are future ideas, not claims about current functionality.

## 🤝 Contributing

Contributions, bug reports, and thoughtful suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make a focused change and add or update tests.
4. Run `python -m unittest discover -s tests -t .`.
5. Open a pull request describing the change and how you tested it.

## 📄 License

J.A.R.V.I.S. is released under the [MIT License](LICENSE).

---

<div align="center">

**Built to keep everyday productivity simple, understandable, and local-first.**

[Interactive demo](https://ansh44233.github.io/jarvis-assistant/) · [GitHub repository](https://github.com/ansh44233/jarvis-assistant) · [Star history](https://star-history.com/#ansh44233/jarvis-assistant&Date)

</div>
