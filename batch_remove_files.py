from pathlib import Path
import argparse
# remove files with _renamed.qtm suffix
def remove_qtm_files(session_root: Path, file_suffix: str):
    qtm_files = list(session_root.rglob(pattern=f"*{file_suffix}.qtm"))
    print(f"Found {len(qtm_files)} qtm files")
    for file in qtm_files:
        print(f"Removing file: {file}")
        file.unlink()

parser = argparse.ArgumentParser(description="""Remove qtm files in a folder and all its subfolders""")
parser.add_argument("session_root", type=Path, help="Diretory where qtm files are located")
args = parser.parse_args()

session_root = args.session_root.absolute()
file_suffix = "_renamed"

remove_qtm_files(session_root, file_suffix)