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

def _rename_markers_sports_markerset():
    marker_mapping = {
        "HeadFront": "Q_HeadFront",
        "HeadR": "Q_HeadR",
        "HeadL": "Q_HeadL",
        "RShoulderTop": "Q_RShoulderTop",
        "LShoulderTop": "Q_LShoulderTop",
        "Chest": "Q_Chest",
        "LElbowIn": "Q_LElbowIn",
        "RElbowIn": "Q_RElbowIn",
        "LElbowOut": "Q_LElbowOut",
        "RElbowOut": "Q_RElbowOut",
        "LWristOut": "Q_LWristOut",
        "RWristOut": "Q_RWristOut",
        "LWristIn": "Q_LWristIn",
        "RWristIn": "Q_RWristIn",
        "WaistRFront": "Q_WaistRFront",
        "WaistLFront": "Q_WaistLFront",
        "RThighFrontLow": "Q_RThighFrontLow",
        "LThighFrontLow": "Q_LThighFrontLow",
        "LTightFrontLow": "Q_LThighFrontLow", # there was a typo for this in source data
        "LKneeIn": "Q_LKneeIn",
        "RKneeIn": "Q_RKneeIn",
        "LKneeOut": "Q_LKneeOut",
        "RKneeOut": "Q_RKneeOut",
        "LShinFrontHigh": "Q_LShinFrontHigh",
        "RShinFrontHigh": "Q_RShinFrontHigh",
        "LAnkleOut": "Q_LAnkleOut",
        "RAnkleOut": "Q_RAnkleOut",
        "LForefoot5": "Q_LForefoot5",
        "RForefoot5": "Q_RForefoot5",
        "LForefoot2": "Q_LForefoot2",
        "RForefoot2": "Q_RForefoot2",
        "SpineThoracic2": "Q_SpineThoracic2",
        "SpineThoracic12": "Q_SpineThoracic12",
        "RArm": "Q_RArm",
        "LArm": "Q_LArm",
        "WaistR": "Q_WaistR",
        "WaistL": "Q_WaistL",
        "IOR_LV5": "Q_WaistBack",
        "RHand2": "Q_RHand2",
        "LHand2": "Q_LHand2",
        "RHeelBack": "Q_RHeelBack",
        "LHeelBack": "Q_LHeelBack",
        
    }
    _rename_markers(marker_mapping)

def _rename_markers_CGM2():
    marker_mapping = {
        "head_front_right__CGM_RFHD": "RFHD",
        "head_back_right__CGM_RFHD": "RBHD",
        "head_back_left__CGM_LBHD": "LBHD",
        "head_front_left__CGM_LFHD": "LFHD",
        "C_7__IOR_CV7__CGM_C7__CAST_CV7": "C7",
        "B_10__CGM_T10__CAST_TV10": "T10",
        "Chest": "CLAV",
        "sternum__IOR_SXS__CGM_STRN": "STRN",
        "CGM_RBAK": "RBAK",
        "LShoulderTop": "LSHO",
        "LElbowOut": "LELB",
        "LWristOut": "LWRB",
        "LWristIn": "LWRA",
        "LHand2": "LFIN",
        "RShoulderTop": "RSHO",
        "RElbowOut": "RELB",
        "RWristOut": "RWRB",
        "RWristIn": "RWRA",
        "RHand2": "RFIN",
        "SIPS_right__IOR_R_IPS__CGM_RPSI__CAST_R_IPS": "RPSI",
        "WaistRFront": "RASI",
        "WaistLFront": "LASI",
        "SIPS_left__IOR_L_IPS__CGM_LPSI__CAST_L_IPS": "LPSI",
        "CGM_RTHAP": "RTHAP",
        "CGM_RTHAD": "RTHAD",
        "CGM_RTHI": "RTHI",
        "RKneeOut": "RKNE",
        "RKneeIn": "RKNM",
        "CGM_RTIAD": "RTIAD",
        "CGM_RTIB": "RTIB",
        "CGM_LTHAP": "LTHAP",
        "CGM_LTHAD": "LTHAD",
        "CGM_LTHI": "LTHI",
        "LKneeOut": "LKNE",
        "LKneeIn": "LKNM",
        "CGM_LTIAD": "LTIAD",
        "CGM_LTIB": "LTIB",
        "mal_med_left__IOR_L_TAM_CGM_LMED__CAST_L_TAM": "LMED",
        "LAnkleOut": "LANK",
        "LHeelBack": "LHEE",
        "LForefoot5": "LVMH",
        "forefoot_med_left__IOR_L_FM1__CGM_LFMH__CAST_FM1": "LFMH",
        "LForefoot2": "LSMH",
        "CGM_LTOE": "LTOE",
        "mal_med_right__IOR_R_TAM__CGM_RMED__CAST_R_TAM": "RMED",
        "RAnkleOut": "RANK",
        "RHeelBack": "RHEE",
        "RForefoot5": "RVMH",
        "forfoot_med_right__IOR_R_FM1__CGM_RFMH__CAST_R_FM1": "RFMH",
        "RForefoot2": "RSMH",
        "CGM_RTOE": "RTOE",

    }
    _rename_markers(marker_mapping)

def _rename_markers_IOR():
    marker_mapping = {
        "HeadFront": "SGL",
        "HeadR": "R_HEAD",
        "HeadL": "L_HEAD",
        "C_7__IOR_CV7__CGM_C7__CAST_CV7": "CV7",
        "SpineThoracic2": "TV2",
        "IOR_MAI": "MAI",
        "IOR_LV1": "LV1",
        "IOR_LV3": "LV3",
        "IOR_LV5": "LV5",
        "Chest": "SJN",
        "sternum__IOR_SXS__CGM_STRN": "SXS",
        "LShoulderTop": "L_SAE",
        "LArm": "L_HUM",
        "LElbowOut": "L_HLE",
        "LWristOut": "L_USP",
        "LWristIn": "L_RSP",
        "LHand2": "L_HM2",
        "RShoulderTop": "R_SAE",
        "RArm": "R_HUM",
        "RElbowOut": "R_HLE",
        "RWristOut": "R_USP",
        "RWristIn": "R_RSP",
        "RHand2": "R_HM2",
        "SIPS_right__IOR_R_IPS__CGM_RPSI__CAST_R_IPS": "R_IPS",
        "WaistRFront": "R_IAS",
        "WaistLFront": "L_IAS",
        "SIPS_left__IOR_L_IPS__CGM_LPSI__CAST_L_IPS": "L_IPS",
        "IOR_R_FTC": "R_FTC",
        "RKneeOut": "R_FLE",
        "RKneeIn": "R_FME",
        "IOR_R_FAX": "R_FAX",
        "RShinFrontHigh": "R_TTC",
        "IOR_L_FTC": "L_FTC",
        "LKneeOut": "L_FLE",
        "LKneeIn": "L_FME",
        "IOR_L_FAX": "L_FAX",
        "LShinFrontHigh": "L_TTC",
        "mal_med_left__IOR_L_TAM_CGM_LMED__CAST_L_TAM": "L_TAM",
        "LAnkleOut": "L_FAL",
        "IOR_L_FCC2__CAST_L_FCC2": "L_FCC2",
        "calc_med_left__IOR_L_MCAL__CAST_L_MCAL": "L_MCAL",
        "LHeelBack": "L_FCC",
        "calc_lat_left__IOR_L_LCAL__CAST_L_LCAL": "L_LCAL",
        "IOR_L_FMT__CAST_L_FMT": "L_FMT",
        "LForefoot5": "L_FM5",
        "toe_left__IOR_L_PM6__CAST_L_PM6": "L_PM6",
        "forefoot_med_left__IOR_L_FM1__CGM_LFMH__CAST_FM1": "L_FM1",
        "LForefoot2": "L_FM2",
        "IOR_L_P1MT__CAST_L_P1MT": "L_P1MT",
        "mal_med_right__IOR_R_TAM__CGM_RMED__CAST_R_TAM": "R_TAM",
        "RAnkleOut": "R_FAL",
        "IOR_R_FCC2__CAST_R_FCC": "R_FCC2",
        "calc_med_right__IOR_R_MCAL__CAST_R_MCAL": "R_MCAL",
        "RHeelBack": "R_FCC",
        "calc_lat_right__IOR_R_LCAL__CAST_R_LCAL": "R_LCAL",
        "IOR_R_FMT__CAST_R_FMT": "R_FMT",
        "RForefoot5": "R_FM5",
        "toe_right__IOR_R_PM6__CAST_R_PM6": "R_PM6",
        "forfoot_med_right__IOR_R_FM1__CGM_RFMH__CAST_R_FM1": "R_FM1",
        "RForefoot2": "R_FM2",
        "IOR_R_P1MT__CAST_R_P1MT": "R_P1MT",

    }
    _rename_markers(marker_mapping)

def _rename_markers_CAST():
    marker_mapping = {
        "HeadFront": "SGL",
        "HeadR": "R_HEAD",
        "HeadL": "L_HEAD",
        "C_7__IOR_CV7__CGM_C7__CAST_CV7": "CV7",
        "B_10__CGM_T10__CAST_TV10": "TH10",
        "CAST_L_SIA": "L_SIA",
        "CGM_RBAK": "R_SIA",
        "LShoulderTop": "L_SAE",
        "LArm": "L_HUM",
        "LElbowOut": "L_HLE",
        "LWristOut": "L_USP",
        "LWristIn": "L_RSP",
        "LHand2": "L_HM2",
        "RShoulderTop": "R_SAE",
        "RArm": "R_HUM",
        "RElbowOut": "R_HLE",
        "RWristOut": "R_USP",
        "RWristIn": "R_RSP",
        "RHand2": "R_HM2",
        "SIPS_right__IOR_R_IPS__CGM_RPSI__CAST_R_IPS": "R_IPS",
        "WaistRFront": "R_IAS",
        "WaistLFront": "L_IAS",
        "SIPS_left__IOR_L_IPS__CGM_LPSI__CAST_L_IPS": "L_IPS",
        "cluster_femur_right_1__CAST_R_TH2": "R_TH2",
        "cluster_femur_right_2__CAST_R_TH1": "R_TH1",
        "cluster_femur_right_3__CAST_R_TH3": "R_TH3",
        "cluster_femur_right_4__CAST_R_TH4": "R_TH4",
        "RKneeOut": "R_FLE",
        "RKneeIn": "R_FME",
        "cluster_tibia_right_1__CAST_R_SK2": "R_SK2",
        "cluster_tibia_right_2__CAST_R_SK1": "R_SK1",
        "cluster_tibia_right_3__CAST_R_SK3": "R_SK3",
        "cluster_tibia_right_4__CAST_R_SK_4": "R_SK4",
        "cluster_femur_left_1__CAST_L_TH1": "L_TH1",
        "cluster_femur_left_2__CAST_L_TH2": "L_TH2",
        "cluster_femur_left_3__CAST_L_TH_4": "L_TH3",
        "cluster_femur_left_4__CAST_L_TH_3": "L_TH4",
        "LKneeOut": "L_FLE",
        "LKneeIn": "L_FME",
        "cluster_tibia_left_1__CAST_L_SK1": "L_SK1",
        "cluster_tibia_left_2__CAST_L_SK2": "L_SK2",
        "cluster_tibia_left_3__CAST_L_SK4": "L_SK3",
        "cluster_tibia_left_4__CAST_L_SK3": "L_SK4",
        "mal_med_left__IOR_L_TAM_CGM_LMED__CAST_L_TAM": "L_TAM",
        "LAnkleOut": "L_FAL",
        "IOR_L_FCC2__CAST_L_FCC2": "L_FCC2",
        "calc_med_left__IOR_L_MCAL__CAST_L_MCAL": "L_MCAL",
        "LHeelBack": "L_FCC",
        "calc_lat_left__IOR_L_LCAL__CAST_L_LCAL": "L_LCAL",
        "IOR_L_FMT__CAST_L_FMT": "L_FMT",
        "LForefoot5": "L_FM5",
        "toe_left__IOR_L_PM6__CAST_L_PM6": "L_PM6",
        "forefoot_med_left__IOR_L_FM1__CGM_LFMH__CAST_FM1": "L_FM1",
        "LForefoot2": "L_FM2",
        "IOR_L_P1MT__CAST_L_P1MT": "L_P1MT",
        "mal_med_right__IOR_R_TAM__CGM_RMED__CAST_R_TAM": "R_TAM",
        "RAnkleOut": "R_FAL",
        "IOR_R_FCC2__CAST_R_FCC": "R_FCC2",
        "calc_med_right__IOR_R_MCAL__CAST_R_MCAL": "R_MCAL",
        "RHeelBack": "R_FCC",
        "calc_lat_right__IOR_R_LCAL__CAST_R_LCAL": "R_LCAL",
        "IOR_R_FMT__CAST_R_FMT": "R_FMT",
        "RForefoot5": "R_FM5",
        "toe_right__IOR_R_PM6__CAST_R_PM6": "R_PM6",
        "forfoot_med_right__IOR_R_FM1__CGM_RFMH__CAST_R_FM1": "R_FM1",
        "RForefoot2": "R_FM2",
        "IOR_R_P1MT__CAST_R_P1MT": "R_P1MT",

    }
    _rename_markers(marker_mapping)

def _rename_markers_MoTrack():
    marker_mapping = {
        "head_front_right__CGM_RFHD": "head_front_right",
        "HeadR": "ear_right",
        "head_back_right__CGM_RFHD": "head_back_right",
        "head_back_left__CGM_LBHD": "head_back_left",
        "HeadL": "ear_left",
        "head_front_left__CGM_LFHD": "head_front_left",
        "C_7__IOR_CV7__CGM_C7__CAST_CV7": "C_7",
        "B_10__CGM_T10__CAST_TV10": "B10",
        "Chest": "clav",
        "sternum__IOR_SXS__CGM_STRN": "sternum",
        "LShoulderTop": "acrom_left",
        "shoulder_left": "shoulder_left",
        "LArm": "cluster_upperarm_left_1",
        "cluster_upperarm_left_2": "cluster_upperarm_left_2",
        "cluster_upperarm_left_3": "cluster_upperarm_left_3",
        "LElbowIn": "elbow_med_left",
        "elbow_top_left": "elbow_top_left",
        "LElbowOut": "elbow_lat_left",
        "cluster_lowerarm_left_1": "cluster_lowerarm_left_1",
        "cluster_lowerarm_left_2": "cluster_lowerarm_left_2",
        "cluster_lowerarm_left_3": "cluster_lowerarm_left_3",
        "LWristOut": "hand_lat_left",
        "LWristIn": "hand_med_left",
        "LHand2": "hand_top_left",
        "RShoulderTop": "acrom_right",
        "shoulder_right": "shoulder_right",
        "RArm": "cluster_upperarm_right_1",
        "cluster_upperarm_right_2": "cluster_upperarm_right_2",
        "cluster_upperarm_right_3": "cluster_upperarm_right_3",
        "RElbowIn": "elbow_med_right",
        "elbow_top_right": "elbow_top_right",
        "RElbowOut": "elbow_lat_right",
        "cluster_lowerarm_right_1": "cluster_lowerarm_right_1",
        "cluster_lowerarm_right_2": "cluster_lowerarm_right_2",
        "cluster_lowerarm_right_3": "cluster_lowerarm_right_3",
        "RWristOut": "hand_lat_right",
        "RWristIn": "hand_med_right",
        "RHand2": "hand_top_right",
        "SIPS_right__IOR_R_IPS__CGM_RPSI__CAST_R_IPS": "SIPS_right",
        "WaistR": "becken_top_right",
        "WaistRFront": "SIAS_right",
        "WaistLFront": "SIAS_left",
        "WaistL": "becken_top_left",
        "SIPS_left__IOR_L_IPS__CGM_LPSI__CAST_L_IPS": "SIPS_left",
        "cluster_femur_right_1__CAST_R_TH2": "cluster_femur_right_1",
        "cluster_femur_right_2__CAST_R_TH1": "cluster_femur_right_2",
        "cluster_femur_right_3__CAST_R_TH3": "cluster_femur_right_3",
        "cluster_femur_right_4__CAST_R_TH4": "cluster_femur_right_4",
        "RKneeOut": "epi_lat_right",
        "RKneeIn": "epi_med_right",
        "cluster_tibia_right_1__CAST_R_SK2": "cluster_tibia_right_1",
        "cluster_tibia_right_2__CAST_R_SK1": "cluster_tibia_right_2",
        "cluster_tibia_right_3__CAST_R_SK3": "cluster_tibia_right_3",
        "cluster_tibia_right_4__CAST_R_SK_4": "cluster_tibia_right_4",
        "cluster_femur_left_1__CAST_L_TH1": "cluster_femur_left_1",
        "cluster_femur_left_2__CAST_L_TH2": "cluster_femur_left_2",
        "cluster_femur_left_3__CAST_L_TH_4": "cluster_femur_left_3",
        "cluster_femur_left_4__CAST_L_TH_3": "cluster_femur_left_4",
        "LKneeOut": "epi_lat_left",
        "LKneeIn": "epi_med_left",
        "cluster_tibia_left_1__CAST_L_SK1": "cluster_tibia_left_1",
        "cluster_tibia_left_2__CAST_L_SK2": "cluster_tibia_left_2",
        "cluster_tibia_left_3__CAST_L_SK4": "cluster_tibia_left_3",
        "cluster_tibia_left_4__CAST_L_SK3": "cluster_tibia_left_4",
        "mal_med_left__IOR_L_TAM_CGM_LMED__CAST_L_TAM": "mal_med_left",
        "LAnkleOut": "mal_lat_left",
        "calc_med_left__IOR_L_MCAL__CAST_L_MCAL": "calc_med_left",
        "LHeelBack": "calc_back_left",
        "calc_lat_left__IOR_L_LCAL__CAST_L_LCAL": "calc_lat_left",
        "LForefoot5": "forefoot_lat_left",
        "toe_left__IOR_L_PM6__CAST_L_PM6": "toe_left",
        "forefoot_med_left__IOR_L_FM1__CGM_LFMH__CAST_FM1": "forefoot_med_left",
        "mal_med_right__IOR_R_TAM__CGM_RMED__CAST_R_TAM": "mal_med_right",
        "RAnkleOut": "mal_lat_right",
        "calc_med_right__IOR_R_MCAL__CAST_R_MCAL": "calc_med_right",
        "RHeelBack": "calc_back_right",
        "calc_lat_right__IOR_R_LCAL__CAST_R_LCAL": "calc_lat_right",
        "RForefoot5": "forfoot_lat_right",
        "toe_right__IOR_R_PM6__CAST_R_PM6": "toe_right",
        "forfoot_med_right__IOR_R_FM1__CGM_RFMH__CAST_R_FM1": "forfoot_med_right",

    }
    _rename_markers(marker_mapping)




def _setup_commands():
    add_command("rename_markers_sports_markerset", _rename_markers_sports_markerset)
    add_command("rename_markers_CGM2", _rename_markers_CGM2)
    add_command("rename_markers_IOR", _rename_markers_IOR)
    add_command("rename_markers_CAST", _rename_markers_CAST)
    add_command("rename_markers_MoTrack", _rename_markers_MoTrack)


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
        add_menu_item(menu_id, "Rename markers (sports markerset)", "rename_markers_sports_markerset")
        add_menu_item(menu_id, "Rename markers (CGM2)", "rename_markers_CGM2")
        add_menu_item(menu_id, "Rename markers (IOR)", "rename_markers_IOR") # we can add a button, but if we call the commands from the script, we don't really need to
        add_menu_item(menu_id, "Rename markers (CAST)", "rename_markers_CAST")
        add_menu_item(menu_id, "Rename markers (MoTrack)", "rename_markers_MoTrack") 
    except Exception as e:
        try_print_except(str(e), "Press 'Reload scripts' to try again.")


if __name__ == "__main__":
    add_menu_and_commands()
