import unittest
from datetime import datetime, timedelta
from jarvis.assistant import Assistant
from jarvis.store import Store
class AssistantTests(unittest.TestCase):
    def setUp(self):
        self.now=datetime(2026,11,13,22,0); self.store=Store()
        self.jarvis=Assistant(self.store,clock=lambda:self.now,name="Ansh")
    def tearDown(self): self.store.close()
    def test_notes_roundtrip(self):
        self.assertEqual(self.jarvis.handle("note learn dp"),"Noted (#1).")
        self.assertIn("learn dp",self.jarvis.handle("notes"))
        self.assertIn("learn dp",self.jarvis.handle("find dp"))
        self.assertEqual(self.jarvis.handle("find xyz"),"Nothing matches.")
    def test_task_lifecycle(self):
        self.assertIn("due tomorrow",self.jarvis.handle("task finish DSA sheet tomorrow"))
        self.assertIn("finish DSA sheet",self.jarvis.handle("tasks"))
        self.assertEqual(self.jarvis.handle("done 1"),"Task #1 done.")
        self.assertEqual(self.jarvis.handle("done 1"),"No open task #1.")
        self.assertEqual(self.jarvis.handle("tasks"),"Nothing to do. Enjoy it.")
    def test_tasks_sorted_by_due_date(self):
        self.jarvis.handle("task later friday"); self.jarvis.handle("task sooner tomorrow"); self.jarvis.handle("task whenever")
        titles=[line.split("]")[1].split("(")[0].strip() for line in self.jarvis.handle("tasks").splitlines()]
        self.assertEqual(titles,["sooner","later","whenever"])
    def test_reminder_fires_once(self):
        self.jarvis.handle("remind me to stretch in 30 minutes"); self.assertEqual(self.jarvis.alerts(),[])
        self.now+=timedelta(minutes=31); self.assertEqual(self.jarvis.alerts(),["Reminder: stretch"])
        self.assertEqual(self.jarvis.alerts(),[])
    def test_recurring_reminder_comes_back(self):
        self.assertIn("repeating daily",self.jarvis.handle("remind me to revise every day at 11pm"))
        self.now=datetime(2026,11,13,23,5); self.assertEqual(self.jarvis.alerts(),["Reminder: revise"])
        self.now=datetime(2026,11,14,23,5); self.assertEqual(self.jarvis.alerts(),["Reminder: revise"])
        self.assertEqual(len(self.store.reminders()),1)
    def test_weekly_reminder_anchors_to_weekday(self):
        self.jarvis.handle("remind me to call home every sunday at 8pm"); row=self.store.reminders()[0]
        self.assertEqual((row["at"],row["repeat"]),("2026-11-15T20:00","weekly"))
    def test_reminder_needs_a_time(self):
        self.assertTrue(self.jarvis.handle("remind me to sleep").startswith("When?"))
    def test_delete_and_unknown(self):
        self.jarvis.handle("note temp"); self.assertEqual(self.jarvis.handle("delete note 1"),"Deleted note #1.")
        self.assertEqual(self.jarvis.handle("delete note 1"),"No note #1.")
        self.assertIn("didn't catch",self.jarvis.handle("sing a song"))
    def test_brief_lists_overdue_work(self):
        self.jarvis.handle("task submit lab today"); text=self.jarvis.handle("brief")
        self.assertIn("Good evening, Ansh.",text); self.assertIn("submit lab",text); self.assertIn("1 open task.",text)
    def test_invalid_task_date_returns_a_helpful_message(self):
        self.assertIn("date is not valid",self.jarvis.handle("task submit report 2026-02-30"))
    def test_invalid_reminder_time_returns_a_helpful_message(self):
        self.assertIn("hour",self.jarvis.handle("remind me to call home at 25:30"))
if __name__ == "__main__": unittest.main()
