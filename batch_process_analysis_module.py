import glob
import os
import threading
import time
from typing import List, Union
from winreg import *

import psutil
import requests

# It is assumed that PAF project is opened in QTM before starting this script.
# Do not use Visual3D while running this script as they are going to be repeatedly automaticaly closed.

# --- Edit these line to adjust to specific PAF module
analysisNames: Union[List, str] = "V3D Processing" #Use it for Visual3D analysis. Case sensitive substring unique to analysis name to run. It can be a list of substrings, e.g. ["Visual3D", "V3D"]. In case of list each session is tested for existances of each analysis name.
desiredSubjectIds = [] # List of desired subject Ids Must match names exactly. Eg ["P002","P003"] If empty, all subjects are used.
# ---

def getSubjectIdField(itemMetadata):
    return itemMetadata["Fields"]["ID"]

def getDesiredSubjectIdFields(myJson):
    if desiredSubjectIds:
        return desiredSubjectIds
    else:
        result = list()
        for itemId in myJson["ChildIDs"]:
            itemMetadata = requests.get('http://localhost:7979/api/v1/paf/instance/' + itemId).json()
            subjectIdField = getSubjectIdField(itemMetadata)
            result.append(subjectIdField)
        return result

def testCmzExists(cmzFile):
    cmzExists = False

    while not cmzExists:
        if glob.glob(cmzFile):
            cmzExists = True
        else:
            cmzExists = False
    return cmzExists



# Find if any item in the list is a substring of any item in other list
def isSubstringPresent(analisysNames, processNames):
    if len(analisysNames) and len(processNames): 
        if isinstance(analisysNames, str) and isinstance(processNames, str):  # Both are strings
            return analisysNames in processNames
        elif isinstance(analisysNames, list) and isinstance(processNames, str):  # list1 is a list and list2 is a string
            for item1 in analisysNames:
                if item1 in processNames:
                    return True
        elif isinstance(analisysNames, str) and isinstance(processNames, list):  # list1 is a string and list2 is a list
            for item2 in processNames:
                if analisysNames in item2:
                    return True
        elif isinstance(analisysNames, list) and isinstance(processNames, list):  # Both are lists
            for item1 in analisysNames:
                for item2 in processNames:
                    if item1 in item2:
                        return True
        return False
    return False

def v3dProcess(id, analysisNames, cmzFile, analysesList):
    for process in analysesList:
        if isSubstringPresent(analysisNames, process):
            analysisNameBody = {"Process": process}

            #delete cmz if it exists
            cmzFiles = glob.glob(cmzFile)
            for file in cmzFiles:
                try:
                    os.remove(file)
                except:
                    print("Error while deleting file: ", file)

            requests.post('http://localhost:7979/api/v1/paf/instance/' + id + '/start_processing', json = analysisNameBody)	
            print ("Processing: " + process)

            # close Visual3D
            if testCmzExists(cmzFile):
                for proc in psutil.process_iter():
                    if "Visual3D.exe" in proc.name():
                            time.sleep(8) #allow time to save cmz before terminating Visual3D
                            proc.terminate()                    
                            print ("Visual3D closed.")


# Process 'Static and Functional session' first if it exists, do not change order of subsessions if 'Static and Functional session' not found
def reorderedDictionary(session, key):
    subsessionDict = dict()

    for subSessionId in session["ChildIDs"]:
        subSession = requests.get('http://localhost:7979/api/v1/paf/instance/' + subSessionId).json()
        #create dictionary of subsession ids and subsession names
        subsessionDict[subSession["Name"]] = subSessionId

    if key not in subsessionDict:
        return subsessionDict

    reordered_dict = {key: subsessionDict[key]}
    for k, v in subsessionDict.items():
        if k != key:
            reordered_dict[k] = v

    return reordered_dict

def v3dBatch():
    myJson = requests.get('http://localhost:7979/api/v1/paf/instance').json()
    for itemId in myJson["ChildIDs"]:
        itemMetadata = requests.get('http://localhost:7979/api/v1/paf/instance/' + itemId).json()
        subjectId = getSubjectIdField(itemMetadata)
        subjectIds = getDesiredSubjectIdFields(myJson)

        if subjectId in subjectIds:
            for sessionId in itemMetadata["ChildIDs"]:
                session = requests.get('http://localhost:7979/api/v1/paf/instance/' + sessionId).json()
                sessionName = session["Name"]
                sessionProcesses = session["Processes"]
                cmzFilePath = session["Fields"]["Path"]
                cmzFile = cmzFilePath + '*.cmz' 

                if len(analysisNames):
                    if len(sessionProcesses) and isSubstringPresent(analysisNames, sessionProcesses):
                        print("Subject: " + subjectId)
                        print("Session: " + sessionName)
                        v3dProcess(sessionId, analysisNames, cmzFile, sessionProcesses)
                    else:
                        subsessionDictReordered = reorderedDictionary(session,"Static and functional session")

                        for subName in subsessionDictReordered:
                            subSessionName = subName
                            subSessionId = subsessionDictReordered[subName]
                            subSession = requests.get('http://localhost:7979/api/v1/paf/instance/' + subSessionId).json()
                            subSessionProcesses = subSession["Processes"]
                            cmzFilePath = subSession["Fields"]["Path"]
                            cmzFile = cmzFilePath + '*.cmz' 

                            print("Subject: " + subjectId)
                            print("Session: " + sessionName)
                            print("Subsession: " + subSessionName)

                            if len(subSessionProcesses) and isSubstringPresent(analysisNames, subSessionProcesses):
                                v3dProcess(subSessionId,analysisNames,cmzFile,subSessionProcesses)
                            else:
                                print("Analysis '" + analysisNames + "' not found")



# --- Start actual batch ---
def runProcessing():
    v3dBatch()

def run():
    t1 = threading.Thread(target=runProcessing)
    t1.start()

if __name__ == "__main__":
    run()

