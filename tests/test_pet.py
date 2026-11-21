import unittest
from datetime import datetime, timedelta

import focus
import pet

T0 = datetime(2026, 11, 17, 9, 0, 0)


def at(minutes=0, seconds=0):
    return T0 + timedelta(minutes=minutes, seconds=seconds)


def new_data():
    return {"focus": {"accumulated_seconds": 0, "is_running": False, "started_at": None}}


class TestGetPetState(unittest.TestCase):
    def test_all_combinations(self):
        # (rest_required, is_journaling, task_just_completed) -> state
        expected = {
            (True, True, True): "rest",
            (True, True, False): "rest",
            (True, False, True): "rest",
            (True, False, False): "rest",
            (False, True, True): "listening",
            (False, True, False): "listening",
            (False, False, True): "happy",
            (False, False, False): "idle",
        }
        for args, state in expected.items():
            with self.subTest(args=args):
                self.assertEqual(pet.get_pet_state(*args), state)


class TestHappyActive(unittest.TestCase):
    def test_none_is_not_happy(self):
        self.assertFalse(pet.is_happy_active(None, T0))

    def test_happy_within_duration(self):
        self.assertTrue(pet.is_happy_active(T0, at(seconds=3)))

    def test_expires_at_duration(self):
        self.assertFalse(pet.is_happy_active(T0, at(seconds=4)))

    def test_future_completion_is_not_happy(self):
        self.assertFalse(pet.is_happy_active(at(seconds=10), T0))


class TestResolvePetState(unittest.TestCase):
    def test_idle_by_default(self):
        self.assertEqual(pet.resolve_pet_state(new_data(), {}, T0), "idle")

    def test_rest_when_focus_reaches_threshold(self):
        d = focus.start_focus(new_data(), T0)
        self.assertEqual(pet.resolve_pet_state(d, {}, at(minutes=50)), "rest")

    def test_listening_when_journaling(self):
        ui = {"is_journaling": True}
        self.assertEqual(pet.resolve_pet_state(new_data(), ui, T0), "listening")

    def test_happy_then_back_to_idle(self):
        ui = {"task_completed_at": T0}
        self.assertEqual(pet.resolve_pet_state(new_data(), ui, at(seconds=2)), "happy")
        self.assertEqual(pet.resolve_pet_state(new_data(), ui, at(seconds=5)), "idle")

    def test_rest_beats_listening(self):
        d = focus.start_focus(new_data(), T0)
        ui = {"is_journaling": True}
        self.assertEqual(pet.resolve_pet_state(d, ui, at(minutes=50)), "rest")

    def test_break_clears_rest(self):
        d = focus.start_focus(new_data(), T0)
        d = focus.record_break(d, at(minutes=50))
        ui = {"is_journaling": True}
        self.assertEqual(pet.resolve_pet_state(d, ui, at(minutes=51)), "listening")

class TestPetImage(unittest.TestCase):
    def test_each_state_has_its_image(self):
        for state in ("idle", "listening", "happy", "rest"):
            with self.subTest(state=state):
                self.assertEqual(pet.get_pet_image(state), "pet_%s.gif" % state)

    def test_unknown_state_falls_back_to_idle(self):
        self.assertEqual(pet.get_pet_image("apa-saja"), "pet_idle.gif")

if __name__ == "__main__":
    unittest.main()