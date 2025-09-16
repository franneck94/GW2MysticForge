import argparse
import random
import time

import pyautogui


MOVE_WIDTH = 150
ACTIONS = [
    {"move": (-MOVE_WIDTH, 0), "click": True},
    {"move": (MOVE_WIDTH, 0), "click": True},
]
MOVE_OFFSET_X = 20
MOVE_OFFSET_Y = 10
time.sleep(3)


def main():
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

    forge_btn_x, forge_btn_y = pyautogui.position()

    try:
        for i in range(num_iterations):
            print(f"Iteration {i + 1}/{num_iterations}")
            x, y = forge_btn_x, forge_btn_y
            for action in ACTIONS:
                dx, dy = action["move"]
                dx += random.randint(-MOVE_OFFSET_X, MOVE_OFFSET_X)
                dy += random.randint(-MOVE_OFFSET_Y, MOVE_OFFSET_Y)
                x += dx
                y += dy
                pyautogui.moveTo(
                    x,
                    y,
                    duration=random.uniform(0.15, 0.35),
                    tween=pyautogui.easeInOutQuad,
                )
                time.sleep(random.uniform(0.5, 0.7))
                if action["click"]:
                    pyautogui.doubleClick()
                    time.sleep(random.uniform(0.5, 0.7))
            time.sleep(random.uniform(0.9, 1.1))
    except KeyboardInterrupt:
        print("Stopped by user.")


if __name__ == "__main__":
    main()
