import importlib

import qtm

from helpers.menu_tools import add_command, add_menu_item
from helpers.printing import try_print_except
from helpers.traj import get_labeled_marker_ids

# try:
#     import CUSTOM_LIBRARY_NAME
#     import CUSTOM_SCRIPT_NAME
# except ModuleNotFoundError as e:
#     try_print_except(str(e), "Press 'Reload scripts' to try again.")


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ////////   P R I V A T E   F U N C T I O N S   ////////
# - - - - - - - - - - - - - - - - - - - - - - - - - - -
# region [ COLLAPSE / EXPAND ]
def _reload_script_modules():
    # Python's default behaviour is to cache imported scripts. This
    # means that changes you make to these scripts will not show up in
    # QTM despite pressing the "Reload scripts" button. However, running
    # "importlib.reload()" on these scripts will force Python to reload them.
    # importlib.reload(CUSTOM_SCRIPT_NAME)
    # importlib.reload(CUSTOM_LIBRARY_NAME)
    pass


def _rename_markers(marker_mapping):
    print("Rename markers called with the following mapping:")
    print(marker_mapping)
    for original_label, new_label in marker_mapping.items():
        trajectory_id = qtm.data.object.trajectory.find_trajectory(original_label)
        if trajectory_id is None:
            print(f"Did not find trajectory with label {original_label}")
            continue

        cur_label = qtm.data.object.trajectory.get_label(trajectory_id)
        qtm.data.object.trajectory.set_label(trajectory_id, new_label)
        changed_label = qtm.data.object.trajectory.get_label(trajectory_id)

        if changed_label != new_label:
            print(f"Could not change label from {cur_label} to {new_label}")
            continue

def _rename_markers_markerset_name_X():
    marker_mapping = {
        "HeadFront": "NewHeadFront",
        "HeadR": "NewHeadR",
    }
    _rename_markers(marker_mapping)

def _rename_markers_markerset_name_Y():
    marker_mapping = {
        "forfoot_med_right": "forefoot_med_right",
        "toe_right": "toe_right3",
    }
    _rename_markers(marker_mapping)

def _rename_markers_markerset_name_Z():
    marker_mapping = {
        "original_name": "new_name",
        "original_name_2": "new_name_2",
    }
    _rename_markers(marker_mapping)




def _setup_commands():
    add_command("rename_markers_X", _rename_markers_markerset_name_X)
    add_command("rename_markers_Y", _rename_markers_markerset_name_Y)
    add_command("rename_markers_Z", _rename_markers_markerset_name_Z)


# endregion


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ////////   E X P O R T E D   F U N C T I O N S   ////////
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# region [ COLLAPSE / EXPAND ]
# NOTE: ADD FUNCTIONS THAT WILL BE ACCESSED OUTSIDE OF THIS FILE HERE


# endregion


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ////////   E N T R Y   P O I N T (local 'main')   ////////
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def add_menu_and_commands():
    try:
        _reload_script_modules()
        print("Modules loaded.")

        # Setup menu commands
        _setup_commands()

        # setup menu
        menu_id = qtm.gui.insert_menu_submenu(None, "Rename markers menu")
        add_menu_item(menu_id, "Rename markers (markerset X)", "rename_markers_X") # we can add a button, but if we call the commands from the script, we don't really need to
        add_menu_item(menu_id, "Rename markers (markerset Y)", "rename_markers_Y") 
    except Exception as e:
        try_print_except(str(e), "Press 'Reload scripts' to try again.")


if __name__ == "__main__":
    add_menu_and_commands()
