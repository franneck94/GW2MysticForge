import threading

import mystic_forge


def test_run_iterations_stops_when_requested(monkeypatch):
    stop_requested = threading.Event()

    class FakePyAutoGUI:
        def position(self):
            return 100, 100

        def moveTo(self, x, y, duration, tween):
            self.last_move = (x, y, duration, tween)

        def doubleClick(self):
            self.double_clicks += 1

        @staticmethod
        def easeInOutQuad(x):
            return x

    fake_gui = FakePyAutoGUI()
    fake_gui.last_move = None
    fake_gui.double_clicks = 0

    sleep_calls = []

    def fake_sleep(seconds):
        sleep_calls.append(seconds)
        if not stop_requested.is_set() and len(sleep_calls) >= 1:
            stop_requested.set()

    mystic_forge.run_iterations(3, stop_requested, fake_gui, fake_sleep)

    assert stop_requested.is_set()
    assert fake_gui.double_clicks == 0
