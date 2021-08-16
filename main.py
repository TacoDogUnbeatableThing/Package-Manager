import gui

import os
import zipfile as zp
import json

from pymongo import MongoClient











#Get IDs
#response = requests.get("https://api.github.com/gists/12d74aacfc4eee259216284c78117ca0")
#IDS = json.loads(response.json()["files"]["IDs.json"]["content"])
CONNECTION_STRING = f"mongodb+srv://user:dURWwuARJFZ8tO7F@ub-package-index.vpkkp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

dbClient = MongoClient(CONNECTION_STRING)
DBINDEX = dbClient["UB-Database"]["Index"]



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









def extractAll(inLoc, outLoc):
    for path, _, files in os.walk(inLoc):
        for file in files:
            if zp.is_zipfile(os.path.join(path, file)):
                with zp.ZipFile(os.path.join(path, file), "r") as zip:
                    zip.extractall(os.path.join(outLoc, os.path.splitext(file)[0]))





def convertFileForPackage(inFile, fileName, zip, zipFileName):
    rawContents = inFile.read()

    if ".osu" in fileName:
        contentsList = rawContents.decode("utf-8").split("\r\n")
        contentsList = [line for line in contentsList if line != ""]

        for index, line in enumerate(contentsList):
            if "AudioFilename:" in line:
                contentsList[index] = f"AudioFilename: USER_BEATMAPS/{os.path.splitext(os.path.basename(zipFileName))[0]}/audio.mp3"
                break

        rawContents = "".join([string + "\r\n" for string in contentsList]).encode("utf-8")

        fileName = gui.ourStrip(fileName.removesuffix(".osu")) + ".osu"

    elif ".mp3" in fileName or ".flac" in fileName or ".wav" in fileName or ".ogg" in fileName:
        fileName = "audio.mp3"

    else:
        return False

    zip.writestr(fileName, rawContents)



def main():
    gui.sendInfo(ROOT, STRIPPIDCHARS, OSUPATH, DBINDEX, GAMEDATAPATH)

    data = gui.actPick()
    if data == None: quit()
    elif data == "downloaded":
        extractAll(os.path.join(ROOT, "modfiles"), os.path.join(GAMEDATAPATH, "UNBEATABLE [white label]_Data", "StreamingAssets", "USER_BEATMAPS"))
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
        for fileName in os.listdir(data[1][i]):
            with open(os.path.join(OSUPATH, data[1][i], fileName), "rb") as inFile:
                convertFileForPackage(inFile, fileName, zip, zip.filename)

        print("Converted!")
        zip.close()

        i += 1

    extractAll(os.path.join(ROOT, "modfiles"), os.path.join(GAMEDATAPATH, "UNBEATABLE [white label]_Data", "StreamingAssets", "USER_BEATMAPS"))






if __name__ == "__main__":
    main()