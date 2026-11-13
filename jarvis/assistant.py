"""Intent routing. Plain regexes, no network, no model calls."""
from __future__ import annotations

import re
from datetime import datetime, time
from typing import Callable

from .store import Store
from .ai import chat as ai_chat, OllamaError
from .timeparse import describe, extract_repeat, extract_when

HELP = """\\
note <text>               save a note            notes | find <word>
task <text> [when]        add a task             tasks | done <id>
remind me <text> <when>   set a reminder         reminders
                          add 'every day' / 'every monday' to repeat
brief                     what needs attention today
delete note|task|reminder <id>
chat <message>       ask local AI (Ollama)
export               export your data as JSON
help | quit

<when> understands: tomorrow, fri, 2026-12-01, at 6pm, in 2 hours"""


class Assistant:
    def __init__(self, store: Store, clock: Callable[[], datetime] = datetime.now, name: str = "boss"):
        self.store = store
        self.clock = clock
        self.name = name
        self.routes: list[tuple[re.Pattern, Callable[[re.Match], str]]] = [
            (re.compile(r"^(?:add\\s+)?(?:note|remember)\\s*[:\\-]?\\s+(.+)$", re.I), self.add_note),
            (re.compile(r"^(?:show\\s+|list\\s+)?notes$", re.I), lambda m: self.list_notes()),
            (re.compile(r"^(?:find|search)\\s+(?:notes?\\s+)?(.+)$", re.I), self.find_notes),
            (re.compile(r"^(?:add\\s+)?(?:task|todo)\\s*[:\\-]?\\s+(.+)$", re.I), self.add_task),
            (re.compile(r"^(?:show\\s+|list\\s+)?(?:tasks|todos?)$", re.I), lambda m: self.list_tasks()),
            (re.compile(r"^(?:done|finish|complete)\\s+#?(\\d+)$", re.I), self.finish_task),
            (re.compile(r"^remind\\s+me\\s+(?:to\\s+)?(.+)$", re.I), self.add_reminder),
            (re.compile(r"^(?:show\\s+|list\\s+)?reminders$", re.I), lambda m: self.list_reminders()),
            (re.compile(r"^(?:delete|remove)\\s+(note|task|reminder)\\s+#?(\\d+)$", re.I), self.delete),
            (re.compile(r"^(?:brief|agenda|today|status)$", re.I), lambda m: self.brief()),
            (re.compile(r"^(?:chat|ask)\\s+(.+)$", re.I), self.chat),
            (re.compile(r"^(?:help|\\?)$", re.I), lambda m: HELP),
        ]

    def handle(self, text: str) -> str:
        text = text.strip()
        if not text:
            return ""
        for pattern, handler in self.routes:
            match = pattern.match(text)
            if match:
                return handler(match)
        return "I didn't catch that. Type 'help' to see what I can do."

    def alerts(self) -> list[str]:
        """Reminders that have come due since the last call."""
        return [f"Reminder: {r['body']}" for r in self.store.due_reminders(self.clock())]

    def add_note(self, m: re.Match) -> str:
        nid = self.store.add_note(m.group(1).strip(), self.clock())
        return f"Noted (#{nid})."

    def list_notes(self) -> str:
        rows = self.store.notes()
        return "\\n".join(f"{r['id']:>3}. {r['body']}" for r in rows) or "No notes yet."

    def find_notes(self, m: re.Match) -> str:
        rows = self.store.notes(m.group(1).strip())
        return "\\n".join(f"{r['id']:>3}. {r['body']}" for r in rows) or "Nothing matches."

    def add_task(self, m: re.Match) -> str:
        now = self.clock()
        try:
            parsed = extract_when(m.group(1), now)
        except ValueError as exc:
            return str(exc)
        if not parsed.text:
            return "A task needs a title."
        tid = self.store.add_task(parsed.text, parsed.when, parsed.has_time, now)
        suffix = f", due {describe(parsed.when, now, parsed.has_time)}" if parsed.when else ""
        return f"Task #{tid} added{suffix}."

    def list_tasks(self) -> str:
        now = self.clock()
        lines = []
        for r in self.store.tasks():
            due = ""
            if r["due"]:
                due = f"  ({describe(datetime.fromisoformat(r['due']), now, bool(r['has_time']))})"
            lines.append(f"{r['id']:>3}. [ ] {r['title']}{due}")
        return "\\n".join(lines) or "Nothing to do. Enjoy it."

    def finish_task(self, m: re.Match) -> str:
        tid = int(m.group(1))
        return f"Task #{tid} done." if self.store.complete_task(tid) else f"No open task #{tid}."

    def add_reminder(self, m: re.Match) -> str:
        now = self.clock()
        text, repeat = extract_repeat(m.group(1))
        try:
            parsed = extract_when(text, now)
        except ValueError as exc:
            return str(exc)
        if parsed.when is None:
            return "When? Try 'remind me to call mom at 6pm' or 'in 30 minutes'."
        when = parsed.when
        if not parsed.has_time:
            when = datetime.combine(when.date(), time(9, 0))
        if not parsed.text:
            return "Remind you about what?"
        rid = self.store.add_reminder(parsed.text, when, repeat)
        every = {"daily": ", repeating daily", "weekly": ", repeating weekly"}.get(repeat, "")
        return f"Reminder #{rid} set for {describe(when, now)}{every}."

    def list_reminders(self) -> str:
        now = self.clock()
        rows = self.store.reminders()
        return (
            "\\n".join(
                f"{r['id']:>3}. {r['body']}  ({describe(datetime.fromisoformat(r['at']), now)}"
                f"{', ' + r['repeat'] if r['repeat'] else ''})"
                for r in rows
            )
            or "No pending reminders."
        )

    def delete(self, m: re.Match) -> str:
        kind, item_id = m.group(1).lower(), int(m.group(2))
        return (
            f"Deleted {kind} #{item_id}."
            if self.store.delete(kind, item_id)
            else f"No {kind} #{item_id}."
        )

    def chat(self, m: re.Match) -> str:
        prompt = m.group(1).strip()
        try:
            answer = ai_chat(prompt, self.store.conversation())
        except OllamaError as exc:
            return str(exc)
        now = self.clock()
        self.store.add_message("user", prompt, now)
        self.store.add_message("assistant", answer, now)
        return answer

    def brief(self) -> str:
        now = self.clock()
        greeting = "morning" if now.hour < 12 else "afternoon" if now.hour < 18 else "evening"
        lines = [f"Good {greeting}, {self.name}."]
        end_of_today = datetime.combine(now.date(), time(23, 59))
        due = [
            r for r in self.store.tasks()
            if r["due"] and datetime.fromisoformat(r["due"]) <= end_of_today
        ]
        if due:
            lines.append("Due today or overdue:")
            lines += [
                f"  - {r['title']} ({describe(datetime.fromisoformat(r['due']), now, bool(r['has_time']))})"
                for r in due
            ]
        upcoming = [r for r in self.store.reminders() if datetime.fromisoformat(r["at"]) <= end_of_today]
        if upcoming:
            lines.append("Reminders today:")
            lines += [f"  - {r['body']} ({datetime.fromisoformat(r['at']):%H:%M})" for r in upcoming]
        open_count = len(self.store.tasks())
        lines.append(f"{open_count} open task{'s' * (open_count != 1)}.")
        return "\\n".join(lines)
