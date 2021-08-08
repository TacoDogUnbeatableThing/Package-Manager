from PySimpleGUI.PySimpleGUI import G
import gui

import os
import zipfile as zp
import json
import re
import requests


#Code for getting all IDs, don't leave this in final build
'''
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

#UB Maps file ID: 1kmDCpmWQTIZRqhcvKsqzm4oZf2z6-mp5
fileList = drive.ListFile({'q': "'1kmDCpmWQTIZRqhcvKsqzm4oZf2z6-mp5' in parents and trashed=false"}).GetList()
IDs = {}

for file in fileList:
    IDs[file["title"]] = file["id"]

with open("IDs.json", "wt") as file:
    json.dump(IDs, file, indent=4)

quit()
'''

#IDs id: 1mdqjkS2JKSpTmDMC-qp6wpuFgvMAvh1N

ROOT = os.path.dirname(os.path.realpath(__file__))
STRIPPIDCHARS = "_- .[]()"
OSUPATH = os.path.join(os.path.dirname(os.getenv("APPDATA")), "Local\\osu!\\Songs")

if not os.path.exists(os.path.join(ROOT, "modfiles")):
    os.makedirs(os.path.join("modfiles"))


config = {

    "OSU_path": OSUPATH,
    "game_data_path": ""

}

try:
    config = json.load(open(os.path.join(ROOT, "config.json"), "rt"))
except:
    with open(os.path.join(ROOT, "config.json"), "wt") as file:
        json.dump(config, file, indent=4)


OSUPATH = config["OSU_path"]
GAMEDATAPATH = config["game_data_path"]





def extractAll():
    for path, _, files in os.walk(os.path.join(ROOT, "modfiles")):
        for file in files:
            with zp.ZipFile(os.path.join(path, file), "r") as zip:
                zip.extractall(os.path.join(GAMEDATAPATH, "UNBEATABLE [white label]_Data", "StreamingAssets", "USER_BEATMAPS", os.path.splitext(file)[0]))





gui.sendInfo(ROOT, STRIPPIDCHARS, OSUPATH)

data = gui.actPick()
if data == None: quit()
elif data == "downloaded":
    extractAll()
    quit()



#Select map pack GUI goes here
try:
    if type(data[1]) == list:
        pass
except:
    data.append(gui.selBeatmap())
    if data[1] == None: quit()

#Get the files and put them into their zip
i = 0
for zip in data[0]:
    bmFinalPath = f"USER_BEATMAPS/{os.path.splitext(os.path.basename(zip.filename))[0]}"

    foundAudio = False
    for fileName in os.listdir(data[1][i]):
        with open(os.path.join(OSUPATH, data[1][i], fileName), "rb") as inFile:
            rawContents = inFile.read()

            if ".osu" in fileName:
                contentsList = rawContents.decode("utf-8").split("\r\n")
                contentsList = [line for line in contentsList if line != ""]

                for index, line in enumerate(contentsList):
                    if "AudioFilename:" in line:
                        contentsList[index] = f"AudioFilename: {bmFinalPath}/audio.mp3"
                        break

                rawContents = "".join([string + "\r\n" for string in contentsList]).encode("utf-8")

                fileName = gui.ourStrip(fileName.removesuffix(".osu")) + ".osu"

            elif ".mp3" in fileName or ".flac" in fileName or ".wav" in fileName or ".ogg" in fileName:
                if foundAudio: continue
                
                fileName = "audio.mp3"
                foundAudio = True

            else:
                continue

            zip.writestr(fileName, rawContents)


    print("Converted!")
    zip.close()

    i += 1

extractAll()