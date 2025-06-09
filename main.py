import time
import re

import pygetwindow as gw

from utils import set_square_edges, set_window_pos, set_window_size

SCREEN_DIMENSIONS = (1920, 1080)
GBA_DIMENSIONS = (240, 160)
GC_DIMENSIONS = (640, 480)
GBA_SCALE = 1.63
GC_SCALE = 1.8


def get_game_window():
    # Dolphin <version> | <recompiler> | <graphic_api> | <HLE/LLE> | <game_title> (<game_code>)
    regex = r"Dolphin .+ \| .+ \| .+ \| .+ \| .+ \(.+\)"

    all_windows = gw.getAllWindows()
    window: gw.Win32Window = None

    for window in all_windows:
        if re.match(regex, window.title):
            return window


def get_gba_window():
    # GBA<controller_port> | <volume>
    regex = r"GBA\d \| .+"

    all_windows = gw.getAllWindows()
    window: gw.Win32Window = None

    for window in all_windows:
        if re.match(regex, window.title):
            return window


def main():
    # try to get game and gba windows for 5 seconds
    print("Trying to find GC and GBA windows... (timeout in 5 seconds)")
    timeout_time = 5
    timeout_timer = time.perf_counter()
    curr_timeout_time = time.perf_counter() - timeout_timer
    while curr_timeout_time < timeout_time:
        curr_timeout_time = time.perf_counter() - timeout_timer
        game = get_game_window()
        gba = get_gba_window()
        if game is not None and gba is not None:
            break
        time.sleep(1 / 5)

    if game is None or gba is None:
        exit("Could not find GC and GBA windows.")
    else:
        print("GC and GBA windows found!")

    print("Running...")

    # position and resize game window
    set_square_edges(game)
    set_window_pos(game, 1, 0)
    set_window_size(game, *(int(x * GC_SCALE) for x in GC_DIMENSIONS))

    # position and resize gba window
    set_square_edges(gba)
    gba_x_pos = (
        int(GC_DIMENSIONS[0] * GC_SCALE) - 2
    )  # set gba x position to right after the game window
    gba_y_pos = (
        SCREEN_DIMENSIONS[1] - int(GBA_DIMENSIONS[1] * GBA_SCALE) - 215
    )  # set gba y position to the bottom edge (why the 215 offset???)
    set_window_pos(gba, gba_x_pos, gba_y_pos)
    set_window_size(gba, *(int(x * GBA_SCALE) for x in GBA_DIMENSIONS))

    # bring screens up front
    time.sleep(1 / 5)
    gba.activate()
    time.sleep(1 / 5)
    game.activate()
    time.sleep(1 / 5)

    # activate both windows if any of them comes up front
    on_top = True
    while True:
        active_window = gw.getActiveWindow()
        if active_window is not None:
            if on_top and active_window.title not in (game.title, gba.title):
                on_top = False

            if not on_top and active_window.title == gba.title:
                on_top = True
                game.activate()
                time.sleep(1 / 20)

            elif not on_top and active_window.title == game.title:
                on_top = True
                gba.activate()
                time.sleep(1 / 20)
                game.activate()
                time.sleep(1 / 20)

        # check if either the game or gba screen has been closed
        if not (game.title and gba.title):
            exit("One or both of the game windows have been closed.")

        time.sleep(1 / 5)


if __name__ == "__main__":
    main()
