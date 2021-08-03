import gui

import os
import zipfile as zp
from pydub import AudioSegment


ROOT = os.path.dirname(os.path.realpath(__file__))
gui.sendRoot(ROOT)

OSUPATH = os.path.join(os.path.dirname(os.getenv("APPDATA")), "Local/osu!/Songs")

zip = gui.actPick()
if zip == None: quit()

'''
zip = zp.ZipFile(f"modfiles/{v2['name']}.bmap", "w", compression=zp.ZIP_LZMA)
with zip.open("config.json", "w") as file:
    file.write(json.dumps(mod, indent=4).encode("utf-8"))


with zp.ZipFile(f"modfiles/{v2['modSelected'][0]}", "r") as zip:
    with zip.open("config.json") as file:
        mod = json.load(file)

'''




#Select map pack GUI goes here
selectedPack = gui.selBeatmap(OSUPATH)
if selectedPack == None: quit()



#Get the files and put them into their zip
for fileName in os.listdir(selectedPack):
    with open(os.path.join(OSUPATH, selectedPack, fileName), "rb") as inFile:
        rawContents = inFile.read()

        if ".osu" in fileName:
            contentsList = rawContents.decode("utf-8").split("\r\n")

            for index, line in enumerate(contentsList):
                if "AudioFilename:" in line:
                    contentsList[index] = f"AudioFilename: USER_BEATMAPS/{os.path.splitext(os.path.basename(zip.filename))[0]}/audio.mp3"
                    break

            rawContents = "".join([string + "\r\n" for string in contentsList]).encode("utf-8")

        elif ".mp3" in fileName or ".flac" in fileName or ".wav" in fileName or ".ogg" in fileName:
            fileName = "audio.mp3"

        zip.writestr(fileName, rawContents)




zip.close()