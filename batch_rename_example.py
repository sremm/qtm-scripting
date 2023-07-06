"""Automation script example renaming many files"""

import argparse
from pathlib import Path
import requests
import time
import shutil

LOCALHOST = "127.0.0.1"
QTM = f"http://{LOCALHOST}:7979"
LOAD_FILE = "/api/experimental/command/load_file"
WORKERSTATE = "/api/experimental/workerstate"
SEND_COMMAND = "/api/scripting/qtm/gui/send_command"
# Stolen from qtm rest tools



def qtm_is_busy(verbose=False):
    result = requests.get(QTM + WORKERSTATE)
    result_json = result.json()
    result_status_code = result.status_code
    if verbose:
        print(f"QTM STATUS: {result_json} status_code: {result_status_code}")
    return result_status_code == 200 and result_json != "Idle"


def wait(initial_sleep_time=0.2, sleep_increment=0.05, max_sleep_time=10):
    time_slept = initial_sleep_time
    time.sleep(initial_sleep_time)  # To make sure qtm has started processing
    while qtm_is_busy():
        time_slept += sleep_increment
        time.sleep(sleep_increment)
        assert time_slept < max_sleep_time


def qtm_load_file(filename):
    result = requests.post(QTM + LOAD_FILE, json={"FileName": str(filename)})
    wait()
    if result.status_code != 200:
        return False
    return True


def send_command(command):
    result = requests.post(QTM + SEND_COMMAND, json=[command])
    wait()
    if result.status_code != 200:
        return False
    return True

def rename_qtm_files(session_root: Path, file_suffix: str):
    qtm_files = list(session_root.glob(pattern="*.qtm"))
    print(f"Found {len(qtm_files)} qtm files")
    for file in qtm_files:
        print(f"Processing file: {file}")

        # copy file with new name to avoid overwriting
        # this could also be another folder with the same name or whatever you desire
        new_file = file.parent / (file.stem + file_suffix + file.suffix)
        shutil.copyfile(file, new_file)

        qtm_load_file(new_file)
        send_command("rename_markers")
        send_command("save_file")
        send_command("close_file")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""Rename qtm files in a folder""")
    parser.add_argument("session_root", type=Path, help="Diretory where qtm files are located")
    parser.add_argument("--file_suffix", type=str, default= "_renamed", help="Suffix to add to qtm files")
    args = parser.parse_args()

    session_root = args.session_root.absolute()
    file_suffix = args.file_suffix

    rename_qtm_files(session_root, file_suffix)
