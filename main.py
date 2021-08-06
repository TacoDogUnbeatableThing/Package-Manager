import gui

import os
import zipfile as zp
import json


ROOT = os.path.dirname(os.path.realpath(__file__))
STRIPPIDCHARS = "_- .[]()"
gui.sendInfo(ROOT, STRIPPIDCHARS)

OSUPATH = os.path.join(os.path.dirname(os.getenv("APPDATA")), "Local\\osu!\\Songs")

if not os.path.exists(os.path.join(ROOT, "modfiles")):
    os.makedirs(os.path.join("modfiles"))



zips = gui.actPick(OSUPATH)
if zips == None: quit()




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



#Select map pack GUI goes here
bulk = False
packs = []
try:
    if type(zips[1]) == list:
        bulk = True

        packs = zips[1]
        zips = zips[0]
except:
    packs[0] = gui.selBeatmap(OSUPATH)
    if packs[0] == None: quit()

#Get the files and put them into their zip
i = 0
for zip in zips:
    bmFinalPath = f"USER_BEATMAPS/{os.path.splitext(os.path.basename(zip.filename))[0]}"

    foundAudio = False
    for fileName in os.listdir(packs[i]):
        with open(os.path.join(OSUPATH, packs[i], fileName), "rb") as inFile:
            rawContents = inFile.read()

            if ".osu" in fileName:
                contentsList = rawContents.decode("utf-8").split("\r\n")

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

    zip.extractall(os.path.join(GAMEDATAPATH, "UNBEATABLE [white label]_Data", "StreamingAssets", bmFinalPath))
    zip.close()

    i += 1