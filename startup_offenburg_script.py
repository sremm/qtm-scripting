"""
Default startup for user examples.  Invoke the startup script
in demo_scripts.
"""
import importlib
import inspect
import os
import sys

# Set scripts 'path' to your repo location
# NOTE: This needs to be done before importing custom libraries
this_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
if this_dir not in sys.path:
    sys.path.append(os.path.join(this_dir))
    sys.path.append(os.path.join(this_dir, "offenburg_scripts"))


import offenburg_scripts.rename_markers

importlib.reload(offenburg_scripts.rename_markers)


def add_menu_and_commands():
    offenburg_scripts.rename_markers.add_menu_and_commands()


if __name__ == "__main__":
    add_menu_and_commands()
