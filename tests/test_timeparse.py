import unittest
from datetime import datetime
from jarvis.timeparse import extract_when
NOW=datetime(2026,11,13,22,0)
class ExtractWhenTests(unittest.TestCase):
    def test_no_time_phrase(self):
        p=extract_when("buy milk",NOW); self.assertEqual((p.text,p.when),("buy milk",None))
    def test_tomorrow_with_time(self):
        p=extract_when("call mom tomorrow at 6pm",NOW); self.assertEqual(p.text,"call mom")
        self.assertEqual(p.when,datetime(2026,11,14,18,0)); self.assertTrue(p.has_time)
    def test_weekday_is_strictly_in_the_future(self):
        p=extract_when("gym friday",NOW); self.assertEqual(p.when.date(),datetime(2026,11,20).date()); self.assertFalse(p.has_time)
    def test_relative_hours(self):
        p=extract_when("stretch in 2 hours",NOW); self.assertEqual(p.text,"stretch"); self.assertEqual(p.when,datetime(2026,11,14,0,0))
    def test_time_already_passed_rolls_to_tomorrow(self):
        p=extract_when("water plants at 8am",NOW); self.assertEqual(p.when,datetime(2026,11,14,8,0))
    def test_iso_date(self):
        p=extract_when("submit form 2026-12-01",NOW); self.assertEqual(p.text,"submit form"); self.assertEqual(p.when,datetime(2026,12,1))
    def test_noon_and_midnight(self):
        self.assertEqual(extract_when("x tomorrow 12pm",NOW).when.hour,12); self.assertEqual(extract_when("x tomorrow 12am",NOW).when.hour,0)
    def test_invalid_clock_time_is_rejected(self):
        with self.assertRaises(ValueError): extract_when("call at 25:10",NOW)
        with self.assertRaises(ValueError): extract_when("call at 6:75pm",NOW)
    def test_invalid_calendar_date_is_rejected(self):
        with self.assertRaises(ValueError): extract_when("submit 2026-02-30",NOW)
if __name__ == "__main__": unittest.main()
