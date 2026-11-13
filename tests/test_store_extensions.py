import os, tempfile, unittest
from datetime import datetime
from pathlib import Path
from jarvis.store import Store
class StoreExtensionTests(unittest.TestCase):
    def setUp(self): self.store=Store(); self.now=datetime(2026,11,13,12,0)
    def tearDown(self): self.store.close()
    def test_conversation_memory_is_chronological_and_bounded(self):
        self.store.add_message("user","first",self.now); self.store.add_message("assistant","second",self.now); self.store.add_message("user","third",self.now)
        self.assertEqual([m["content"] for m in self.store.conversation(2)],["second","third"])
    def test_export_contains_all_user_data_groups(self):
        self.store.add_note("remember this",self.now); exported=self.store.export_data()
        self.assertEqual(set(exported),{"notes","tasks","reminders","conversation"})
        self.assertEqual(exported["notes"][0]["body"],"remember this")
    def test_message_role_is_validated(self):
        with self.assertRaises(ValueError): self.store.add_message("system","not allowed",self.now)
    def test_delete_rejects_unknown_item_types(self):
        with self.assertRaises(ValueError): self.store.delete("users",1)
    @unittest.skipUnless(os.name=="posix","POSIX file permissions are not available")
    def test_database_file_is_created_with_private_permissions(self):
        with tempfile.TemporaryDirectory() as directory:
            database=Path(directory)/"private"/"jarvis.db"; store=Store(database)
            try: self.assertEqual(database.stat().st_mode & 0o777,0o600)
            finally: store.close()
if __name__ == "__main__": unittest.main()
