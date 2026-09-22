from pynput.keyboard import Controller, Key
from pynput.mouse import Button
from pathlib import Path
from typos import Typos
from delays import Delay
from mouse import RealisticMouse
import numpy as np
from numpy.random import uniform as rand
import time
import subprocess
import argparse
import psutil
import win32con, win32gui
import base64


def getargs():
    parser = argparse.ArgumentParser(
        description="MS-Word Agent"
    )

    parser.add_argument(
        "filename",
        help="TXT file containing the text you want to write"
    )

    parser.add_argument(
        "-o", "--output",
        help="Output file: *.docx"
    )

    parser.add_argument(
        "-c", "--close_word",
        action="store_true",
        help="Close Word's window after task if set to true"
    )

    args = parser.parse_args()
    return args.filename, args.output, args.close_word

SCRIPT_DIR = Path(__file__).resolve().parent
SPOOFING_LOCATION = SCRIPT_DIR / "createWithFakePPID.exe"

def getExplorerPID():
    explorer_pids = [
        proc.info["pid"]
        for proc in psutil.process_iter(["pid", "name"])
        if proc.info["name"] and proc.info["name"].lower() == "explorer.exe"
    ]
    print("PID of explorer.exe is:", explorer_pids[0])
    return explorer_pids[0]


def openDocument(filename: str):
    filename = filename.lstrip(".\\")
    docxfile = Path(filename)
    if not docxfile.exists():
        print(f"{filename} does not exist. Creating a new one...")
        docxfile.touch()

    explorer_pid = getExplorerPID()

    fuzz_num = 10
    command = [
        "cmd.exe",
        "/C",
        str(SPOOFING_LOCATION),
        "/n",
        str(fuzz_num)
    ] + [
        "-" + base64.b64encode(str(np.random.randint(100000, 999999)).encode()).decode()[:-2]
        for _ in range(fuzz_num)
    ] + [
        str(explorer_pid),
        str(docxfile.absolute())
    ]
    subprocess.run(" ".join(command), timeout=5)
    time.sleep(3)

    hwnd = win32gui.FindWindow(None, f"{filename} - Word")

    is_foreground = lambda hwnd: win32gui.GetForegroundWindow() == hwnd
    if hwnd:
        print("found")
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        for _ in range(10):
            time.sleep(0.2)
            win32gui.SetForegroundWindow(hwnd)
            if is_foreground(hwnd):
                break
        else:
            raise "cannot put foreground"


def writeDocument(text: str):
    keyboardController = Controller()
    delayController = Delay()
    mouseController = RealisticMouse()
    typoController = Typos(keyboardController, delayController)
    next_scroll = np.random.exponential(90)
    last_scroll = time.time()

    # zoom in
    time.sleep(0.5)
    with keyboardController.pressed(Key.ctrl):
        mouseController.real_scroll(3)
    time.sleep(1)

    for index, c in enumerate(text):
        thres = 0.1 if delayController.status != 2 else 0.2

        # Typo
        if c == "\n":
            keyboardController.press(Key.enter)
            keyboardController.release(Key.enter)
        elif rand() < thres and c.isupper():
            typoController.capitalization_error(text[index: min(index + 8, len(text))])
        elif rand() < thres and c.isalpha():
            typoController.random(c)
        else:
            keyboardController.press(c)
            keyboardController.release(c)

        # Delay
        if c == ".":
            if rand() < 0.9:
                delayController.fullstop()
            else:
                delayController.thinking()
        elif c == " " and rand() < 0.2:
            delayController.thinking()
        elif c == "\n":
            delayController.thinking()
        elif c == ",":
            delayController.comma()
        else:
            if delayController.status == 1:
                if rand() < 0.2: # fast mode
                    keepStatusFor = np.random.randint(8, 15)
                    delayController.setStatus(2, keepStatusFor)
                elif rand() < 0.1: # slow mode
                    keepStatusFor = np.random.randint(2, 5)
                    delayController.setStatus(3, keepStatusFor)

            delayController.next()
            delayController.wait()

        # scrolling
        if time.time() > last_scroll + next_scroll:
            mouseController.real_scroll(-2)
            mouseController.real_scroll(1)
            last_scroll = time.time()
            next_scroll = np.random.exponential(90)

    # save file after typing
    with keyboardController.pressed(Key.ctrl):
        keyboardController.press("s")
        keyboardController.release("s")

    time.sleep(0.5)
    with keyboardController.pressed(Key.ctrl):
        mouseController.real_scroll(-3)
    time.sleep(1)

def main():
    filename, output, close_word = getargs()
    if not filename.endswith(".txt"):
        raise ValueError("Provide a txt file as source")

    if not output.endswith(".docx"):
        output += ".docx"

    with open(filename, "r") as f:
        content = f.read()

    openDocument(output)
    time.sleep(2)
    writeDocument(content)

    if close_word:
        time.sleep(3)
        mouse = RealisticMouse()
        mouse.real_move(1600, 33)
        mouse.click(Button.left)

if __name__ == "__main__":
    main()