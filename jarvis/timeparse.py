"""Pull a date/time phrase out of free text."""
from __future__ import annotations
import re
from dataclasses import dataclass
from datetime import datetime, time, timedelta

DAY_NAMES=["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
_REL=re.compile(r"\bin\s+(\d+)\s*(minutes?|mins?|hours?|hrs?|days?|m|h|d)\b",re.I)
_ISO=re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")
_DAY=re.compile(r"\b(?:on\s+|next\s+)?(today|tonight|tomorrow|"+ "|".join(DAY_NAMES)+"|"+"|".join(d[:3] for d in DAY_NAMES)+r")\b",re.I)
_TIME_AMPM=re.compile(r"\b(?:at\s+)?(\d{1,2})(?::(\d{2}))?\s*(am|pm)\b",re.I)
_TIME_AT=re.compile(r"\bat\s+(\d{1,2})(?::(\d{2}))?\b",re.I)
_DANGLING=re.compile(r"\s+(?:on|at|by|due|for)\s*$",re.I)
_EVERY=re.compile(r"\b(?:every\s+(day|"+"|".join(DAY_NAMES)+r")|(daily))\b",re.I)

def extract_repeat(text: str) -> tuple[str,str | None]:
    m=_EVERY.search(text)
    if not m: return text,None
    word=(m.group(1) or "daily").lower()
    if word in ("day","daily"): return _cut(text,m.span()),"daily"
    return text[:m.start()]+word+text[m.end():],"weekly"

@dataclass
class Parsed:
    text: str
    when: datetime | None
    has_time: bool

def _cut(s: str,span: tuple[int,int]) -> str: return (s[:span[0]]+" "+s[span[1]:]).strip()

def _clock(m: re.Match) -> time:
    hour,minute=int(m.group(1)),int(m.group(2) or 0)
    meridiem=(m.group(3) or "").lower() if m.lastindex and m.lastindex>=3 else ""
    if minute>59: raise ValueError("Minutes must be between 0 and 59.")
    if meridiem:
        if not 1<=hour<=12: raise ValueError("Use an hour between 1 and 12 with am/pm.")
        if meridiem=="pm" and hour<12: hour+=12
        elif meridiem=="am" and hour==12: hour=0
    elif not 0<=hour<=23: raise ValueError("Use a 24-hour time between 00:00 and 23:59.")
    return time(hour,minute)

def extract_when(text: str,now: datetime) -> Parsed:
    s=text.strip()
    m=_REL.search(s)
    if m:
        n,unit=int(m.group(1)),m.group(2).lower()
        if unit.startswith("d"):
            when=(now+timedelta(days=n)).replace(hour=0,minute=0,second=0,microsecond=0)
            return Parsed(_clean(_cut(s,m.span())),when,False)
        delta=timedelta(minutes=n) if unit.startswith("m") else timedelta(hours=n)
        return Parsed(_clean(_cut(s,m.span())),(now+delta).replace(second=0,microsecond=0),True)
    day=None
    m=_ISO.search(s)
    if m:
        try: day=datetime(int(m.group(1)),int(m.group(2)),int(m.group(3)))
        except ValueError as exc: raise ValueError("That date is not valid. Use YYYY-MM-DD.") from exc
        s=_cut(s,m.span())
    else:
        m=_DAY.search(s)
        if m:
            word=m.group(1).lower(); base=now.replace(hour=0,minute=0,second=0,microsecond=0)
            if word in ("today","tonight"): day=base
            elif word=="tomorrow": day=base+timedelta(days=1)
            else:
                target=[d[:3] for d in DAY_NAMES].index(word[:3])
                day=base+timedelta(days=(target-now.weekday())%7 or 7)
            s=_cut(s,m.span())
    clock=None
    for pattern in (_TIME_AMPM,_TIME_AT):
        m=pattern.search(s)
        if m: clock=_clock(m); s=_cut(s,m.span()); break
    if day is None and clock is None: return Parsed(text.strip(),None,False)
    if day is None:
        day=now.replace(hour=0,minute=0,second=0,microsecond=0)
        if datetime.combine(day.date(),clock)<=now: day+=timedelta(days=1)
    when=datetime.combine(day.date(),clock) if clock else day
    return Parsed(_clean(s),when,clock is not None)

def _clean(s: str) -> str:
    s=re.sub(r"\s{2,}"," ",s).strip()
    return _DANGLING.sub("",s).strip(" ,.")

def describe(when: datetime,now: datetime,has_time: bool=True) -> str:
    days=(when.date()-now.date()).days
    if days==0: label="today"
    elif days==1: label="tomorrow"
    elif days==-1: label="yesterday"
    elif 1<days<7: label=when.strftime("%A")
    else: label=when.strftime("%a %d %b")
    return f"{label} {when:%H:%M}" if has_time else label
