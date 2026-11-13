"""SQLite persistence. Everything lives in one small file."""
from __future__ import annotations
import os
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, body TEXT NOT NULL, created TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, due TEXT, has_time INTEGER NOT NULL DEFAULT 0, done INTEGER NOT NULL DEFAULT 0, created TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS conversation (id INTEGER PRIMARY KEY, role TEXT NOT NULL CHECK(role IN ('user', 'assistant')), content TEXT NOT NULL, created TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS reminders (id INTEGER PRIMARY KEY, body TEXT NOT NULL, at TEXT NOT NULL, fired INTEGER NOT NULL DEFAULT 0, repeat TEXT);
"""
_TABLES={"note":"notes","task":"tasks","reminder":"reminders"}

def default_path() -> Path:
    override=os.environ.get("JARVIS_DB")
    return Path(override) if override else Path.home()/".jarvis"/"jarvis.db"

def _iso(dt: datetime | None) -> str | None:
    return dt.isoformat(timespec="minutes") if dt else None

class Store:
    def __init__(self,path: str | Path=":memory:"):
        if str(path)!=":memory:":
            database_path=Path(path).expanduser()
            database_path.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
            path=database_path
        self.db=sqlite3.connect(str(path),timeout=10)
        if str(path)!=":memory:":
            try: os.chmod(path,0o600)
            except OSError: pass
        self.db.row_factory=sqlite3.Row
        self.db.executescript(SCHEMA)
        self._migrate()
    def _migrate(self):
        cols={r["name"] for r in self.db.execute("PRAGMA table_info(reminders)")}
        if "repeat" not in cols:
            self.db.execute("ALTER TABLE reminders ADD COLUMN repeat TEXT"); self.db.commit()
    def close(self): self.db.close()
    def add_note(self,body: str,now: datetime) -> int:
        cur=self.db.execute("INSERT INTO notes (body, created) VALUES (?, ?)",(body,_iso(now))); self.db.commit(); return cur.lastrowid
    def notes(self,query: str | None=None):
        if query:
            return self.db.execute("SELECT * FROM notes WHERE body LIKE ? ORDER BY id DESC",(f"%{query}%",)).fetchall()
        return self.db.execute("SELECT * FROM notes ORDER BY id DESC").fetchall()
    def add_task(self,title: str,due: datetime | None,has_time: bool,now: datetime) -> int:
        cur=self.db.execute("INSERT INTO tasks (title, due, has_time, created) VALUES (?, ?, ?, ?)",(title,_iso(due),int(has_time),_iso(now))); self.db.commit(); return cur.lastrowid
    def tasks(self,include_done: bool=False):
        where="" if include_done else "WHERE done = 0"
        return self.db.execute(f"SELECT * FROM tasks {where} ORDER BY due IS NULL, due, id").fetchall()
    def complete_task(self,task_id: int) -> bool:
        cur=self.db.execute("UPDATE tasks SET done = 1 WHERE id = ? AND done = 0",(task_id,)); self.db.commit(); return cur.rowcount>0
    def add_reminder(self,body: str,at: datetime,repeat: str | None=None) -> int:
        cur=self.db.execute("INSERT INTO reminders (body, at, repeat) VALUES (?, ?, ?)",(body,_iso(at),repeat)); self.db.commit(); return cur.lastrowid
    def reminders(self,pending_only: bool=True):
        where="WHERE fired = 0" if pending_only else ""
        return self.db.execute(f"SELECT * FROM reminders {where} ORDER BY at").fetchall()
    def due_reminders(self,now: datetime):
        rows=self.db.execute("SELECT * FROM reminders WHERE fired = 0 AND at <= ? ORDER BY at",(_iso(now),)).fetchall()
        for r in rows:
            if r["repeat"]:
                step=timedelta(days=1 if r["repeat"]=="daily" else 7)
                nxt=datetime.fromisoformat(r["at"])+step
                while nxt<=now: nxt+=step
                self.db.execute("UPDATE reminders SET at = ? WHERE id = ?",(_iso(nxt),r["id"]))
            else: self.db.execute("UPDATE reminders SET fired = 1 WHERE id = ?",(r["id"],))
        if rows: self.db.commit()
        return rows
    def add_message(self,role: str,content: str,now: datetime):
        if role not in {"user","assistant"}: raise ValueError("role must be user or assistant")
        self.db.execute("INSERT INTO conversation (role, content, created) VALUES (?, ?, ?)",(role,content,_iso(now))); self.db.commit()
    def conversation(self,limit: int=12):
        rows=self.db.execute("SELECT role, content FROM conversation ORDER BY id DESC LIMIT ?",(max(1,min(limit,100)),)).fetchall()
        return [dict(row) for row in reversed(rows)]
    def export_data(self) -> dict:
        return {table:[dict(row) for row in self.db.execute(f"SELECT * FROM {table} ORDER BY id")] for table in ("notes","tasks","reminders","conversation")}
    def delete(self,kind: str,item_id: int) -> bool:
        try: table=_TABLES[kind]
        except KeyError as exc: raise ValueError(f"Unsupported item type: {kind}") from exc
        cur=self.db.execute(f"DELETE FROM {table} WHERE id = ?",(item_id,)); self.db.commit(); return cur.rowcount>0
