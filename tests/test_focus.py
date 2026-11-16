import unittest
from datetime import datetime, timedelta

import focus

T0 = datetime(2026, 11, 16, 9, 0, 0)


def m(n):
    return T0 + timedelta(minutes=n)


def new_data():
    return {"focus": {"accumulated_seconds": 0, "is_running": False, "started_at": None}}


class TestFocus(unittest.TestCase):
    def test_start_twice_does_not_reset(self):
        d = focus.start_focus(new_data(), m(0))
        d = focus.start_focus(d, m(5))
        self.assertEqual(focus.get_focus_seconds(d, m(10)), 600)

    def test_end_adds_duration(self):
        d = focus.start_focus(new_data(), m(0))
        d = focus.end_focus(d, m(10))
        self.assertEqual(d["focus"]["accumulated_seconds"], 600)
        self.assertFalse(d["focus"]["is_running"])

    def test_end_without_session_changes_nothing(self):
        d = focus.end_focus(new_data(), m(5))
        self.assertEqual(d["focus"]["accumulated_seconds"], 0)

    def test_threshold_boundary(self):
        d = focus.start_focus(new_data(), m(0))
        just_before = m(50) - timedelta(seconds=1)
        self.assertFalse(focus.is_rest_required(d, just_before, 50))
        self.assertTrue(focus.is_rest_required(d, m(50), 50))

    def test_record_break_while_running(self):
        d = focus.start_focus(new_data(), m(0))
        d = focus.record_break(d, m(60))
        self.assertEqual(d["focus"]["accumulated_seconds"], 0)
        self.assertEqual(focus.get_focus_seconds(d, m(61)), 60)

    def test_reset_on_launch_clears_running_session(self):
        d = focus.start_focus(new_data(), m(0))
        d = focus.reset_focus_on_launch(d)
        self.assertFalse(d["focus"]["is_running"])
        self.assertEqual(d["focus"]["accumulated_seconds"], 0)

    def test_corrupt_started_at_does_not_crash(self):
        d = new_data()
        d["focus"]["is_running"] = True
        d["focus"]["started_at"] = "bukan-tanggal"
        self.assertEqual(focus.get_focus_seconds(d, m(10)), 0)


if __name__ == "__main__":
    unittest.main()