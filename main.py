import gui

import os
import zipfile as zp


ROOT = os.path.dirname(os.path.realpath(__file__))
gui.sendRoot(ROOT)

OSUPATH = os.path.join(os.path.dirname(os.getenv("APPDATA")), "Local/osu!/Songs")

zip = gui.actPick()
if zip == None: quit()

#gui.mainWin()

'''
zip = zp.ZipFile(f"modfiles/{v2['name']}.bmap", "w", compression=zp.ZIP_LZMA)
with zip.open("config.json", "w") as file:
    file.write(json.dumps(mod, indent=4).encode("utf-8"))


with zp.ZipFile(f"modfiles/{v2['modSelected'][0]}", "r") as zip:
    with zip.open("config.json") as file:
        mod = json.load(file)

'''




osuMapPacks = []
selPack = 0

for path, _, _ in os.walk(OSUPATH):
    if path == OSUPATH: continue
    osuMapPacks.append(path)


#Select map pack GUI goes here
selectedPack = osuMapPacks[len(osuMapPacks) - 1]

for fileName in os.listdir(selectedPack):
    if ".osu" not in fileName and "audio.mp3" not in fileName:
        continue

    with open(os.path.join(OSUPATH, selectedPack, fileName), "rb") as inFile:
        zip.writestr(fileName, inFile.read())




zip.close()
#test