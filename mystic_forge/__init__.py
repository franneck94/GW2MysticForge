import argparse
import random
import threading
import time
from typing import Callable

import pyautogui
from pynput import keyboard


MOVE_WIDTH = 150
ACTIONS = [
    {"move": (-MOVE_WIDTH, 0), "click": True},
    {"move": (MOVE_WIDTH, 0), "click": True},
]
MOVE_OFFSET_X = 20
MOVE_OFFSET_Y = 10

time.sleep(3)


def _create_stop_listener(stop_event: threading.Event) -> keyboard.Listener:
    ctrl_pressed = False

    def on_press(key: keyboard.Key | keyboard.KeyCode | None) -> bool:
        nonlocal ctrl_pressed
        if key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
            ctrl_pressed = True
            return True
        if key == keyboard.KeyCode.from_char("c") and ctrl_pressed:
            stop_event.set()
            return False
        return True

    def on_release(key: keyboard.Key | keyboard.KeyCode | None) -> bool:
        nonlocal ctrl_pressed
        if key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
            ctrl_pressed = False
        return True

    return keyboard.Listener(on_press=on_press, on_release=on_release)


def run_iterations(
    num_iterations: int,
    stop_event: threading.Event | None = None,
    pyautogui_module=pyautogui,
    sleep_func: Callable[[float], None] = time.sleep,
) -> None:
    if stop_event is None:
        stop_event = threading.Event()

    forge_btn_x, forge_btn_y = pyautogui_module.position()

    try:
        for i in range(num_iterations):
            if stop_event.is_set():
                break
            print(f"Iteration {i + 1}/{num_iterations}")
            x, y = forge_btn_x, forge_btn_y
            for action in ACTIONS:
                dx, dy = action["move"]
                dx += random.randint(-MOVE_OFFSET_X, MOVE_OFFSET_X)  # noqa: S311
                dy += random.randint(-MOVE_OFFSET_Y, MOVE_OFFSET_Y)  # noqa: S311
                x += dx
                y += dy
                pyautogui_module.moveTo(
                    x,
                    y,
                    duration=random.uniform(0.15, 0.35),  # noqa: S311
                    tween=pyautogui_module.easeInOutQuad,
                )
                sleep_func(random.uniform(0.5, 0.7))  # noqa: S311
                if stop_event.is_set():
                    break
                if action["click"]:
                    pyautogui_module.doubleClick()
                    sleep_func(random.uniform(0.5, 0.7))  # noqa: S311
                if stop_event.is_set():
                    break
            if stop_event.is_set():
                break
            sleep_func(random.uniform(0.9, 1.1))  # noqa: S311
    except KeyboardInterrupt:
        stop_event.set()
        print("Stopped by user.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Automated clicker script.")
    parser.add_argument(
        "-n",
        "--num_iterations",
        type=int,
        help="Number of iterations to run",
        required=True,
    )
    args = parser.parse_args()
    num_iterations = args.num_iterations

    stop_event = threading.Event()
    listener = _create_stop_listener(stop_event)
    listener.start()

    try:
        run_iterations(num_iterations, stop_event=stop_event)
    except KeyboardInterrupt:
        stop_event.set()
        print("Stopped by user.")
    finally:
        listener.stop()
        listener.join(timeout=1.0)


if __name__ == "__main__":
    main()
