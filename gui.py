from typing import final
import PySimpleGUI as sg
import json
import os
import zipfile as zp
import re
import requests
from pymongo import MongoClient

from PySimpleGUI.PySimpleGUI import LISTBOX_SELECT_MODE_EXTENDED, LISTBOX_SELECT_MODE_MULTIPLE, LISTBOX_SELECT_MODE_SINGLE


ROOT = ""
STRIPPIDCHARS = ""
OSUPATH = ""
DBINDEX = {}

def sendInfo(root, strippedChards, osuPath, dbIndex):
    global ROOT
    global STRIPPIDCHARS
    global OSUPATH
    global DBINDEX

    ROOT = root
    STRIPPIDCHARS = strippedChards
    OSUPATH = osuPath
    DBINDEX = dbIndex

title = "TacoDog MC" #MC stands for "mod creator"
sg.theme("Topanga")


size = (15, 1)



def ourStrip(strIn):
    return "".join(c for c in strIn if c not in STRIPPIDCHARS)



#Action to pick if you want to create a mod or edit one
def actPick():
    #Window to pick between creating a mod or editing one
    firstWin = sg.Window(title, [

        [sg.B("Create package", size=size)      ],
        [sg.B("Edit package", size=size)        ],
        [sg.T()                                 ],
        [sg.B("Bulk make package", size=size)   ],
        [sg.T()                                 ],
        [sg.B("Download packages", size=size)   ]

    ], element_justification="c", resizable=True)

    while True:
        e1, v1 = firstWin.read()


        if e1 == "Create package":
            #Window to put in details about the new package being created
            createWin = sg.Window(title, [

                [sg.T("Mod name:", size=size),  sg.Input(key="name") ],
                [sg.B("Create", size=size)                           ]

            ], element_justification="c", modal=True, resizable=True)

            while True:
                e2, v2 = createWin.read()


                if e2 == "Create":
                    createWin.close()
                    firstWin.close()

                    return [[zp.ZipFile(f"modfiles/{v2['name']}.bmap", "w", compression=zp.ZIP_LZMA)]]

                elif e2 == sg.WINDOW_CLOSED:
                    createWin.close()
                    break

        elif e1 == "Edit package":
            #Window to put in details about the package to be edited
            for _, _, files in os.walk("modfiles"):
                modConfigs = files
                break

            editWin = sg.Window(title, [

                [sg.T("Please select a mod")                                                                ],
                [sg.LB(modConfigs, size=size, key="modSelected", select_mode=LISTBOX_SELECT_MODE_SINGLE)    ],
                [sg.B("Edit", size=size)                                                                    ]

            ], element_justification="c", modal=True, resizable=True, finalize=True)
            editWin.bind('<Configure>', "Configure")

            while True:
                e2, v2 = editWin.read()
                try:
                    editWin["modSelected"].expand(expand_x=True, expand_y=True)
                except:
                    pass


                if e2 == "Edit":
                    try:
                        data = [zp.ZipFile(f"modfiles/{v2['modSelected'][0]}", "w", compression=zp.ZIP_LZMA)]
                        
                        editWin.close()
                        firstWin.close()

                        return [data]
                    except:
                        pass

                elif e2 == sg.WINDOW_CLOSED:
                    editWin.close()
                    break

        elif e1 == "Bulk make package":
            #Window to put in details about the packages to be made
            editWin = sg.Window(title, [

                [sg.T("Folder with unpackaged beatmaps:"), sg.I(key="folderInput", size=size), sg.FolderBrowse("Browse", size=size) ],
                [sg.B("Bulk make", size=size)                                                                                       ]

            ], element_justification="c", modal=True, resizable=True, finalize=True)
            editWin.bind('<Configure>', "Configure")

            while True:
                e2, v2 = editWin.read()
                try:
                    editWin["folderInput"].expand(expand_x=True, expand_y=True)
                except:
                    pass

                if e2 == "Bulk make":
                    try:
                        beatmapPaths = []
                        for path, _, _ in os.walk(v2['folderInput']):
                            if path == v2['folderInput']:
                                continue
                            beatmapPaths.append(path)

                        beatmaps = []
                        for _, dirs, _ in os.walk(v2['folderInput']):
                            beatmaps = dirs
                            break

                        editWin.close()
                        firstWin.close()

                        return [[zp.ZipFile(f"modfiles/{ourStrip(beatmap)}.bmap", "w", compression=zp.ZIP_LZMA) for beatmap in beatmaps], beatmapPaths]
                    except:
                        pass

                elif e2 == sg.WINDOW_CLOSED:
                    editWin.close()
                    break

        elif e1 == "Download packages":
            #Select package window
            packWin = sg.Window(title, [

                [sg.T("Please select a package")                                                                                        ],
                [sg.Input(key="input"), sg.Combo(["Name", "Artist"], default_value="Name", size=size, key="searchType")                 ],
                [sg.B("Search", bind_return_key=True, size=size)                                                                        ],
                [sg.LB([t["name"] for t in DBINDEX.find()], size=size, key="packageSelected", select_mode=LISTBOX_SELECT_MODE_EXTENDED) ],
                [sg.B("Download", size=size)                                                                                            ]
                

            ], element_justification="c", modal=True, resizable=True, finalize=True)
            packWin.bind('<Configure>', "Configure")

            while True:
                e2, v2 = packWin.read()
                try:
                    packWin["packageSelected"].expand(expand_x=True, expand_y=True)
                except:
                    pass


                if e2 == "Search":
                    if v2["input"] != "":
                        titles = [t["name"] for t in DBINDEX.aggregate([
                            {"$search": {"text": {"query": v2["input"],"path": v2["searchType"].lower()}}}])
                        ]
                    else:
                        titles = [t["name"] for t in DBINDEX.find()]

                    v2['packageSelected'] = []
                    packWin.FindElement("packageSelected").Update(values=titles)


                elif e2 == "Download":
                    packWin.close()

                    for t in v2['packageSelected']:
                        for bm in DBINDEX.find({"name": t}):
                            del bm["_id"]

                            response = requests.get(f"https://drive.google.com/uc?export=download&id={bm['file_id']}")

                            bmFilePath = os.path.join("modfiles", bm['file_id'] + ".bmap")
                            open(bmFilePath, "wb").write(response.content)

                            with zp.ZipFile(bmFilePath, "a", compression=zp.ZIP_LZMA) as zip:
                                with zip.open("info.json", "w") as infoFile:
                                    infoFile.write(json.dumps(bm, indent=4).encode("utf-8"))


                            print("Downloaded " + bm['file_id'])
                            break

                    return "downloaded"


                elif e2 == sg.WINDOW_CLOSED:
                    packWin.close()
                    return

        elif e1 == sg.WINDOW_CLOSED: 
            firstWin.close()

            return


#Select beatmap window
def selBeatmap():
    #Select beatmap window
    for _, dirs, _ in os.walk(OSUPATH):
        songs = dirs
        break

    beatWin = sg.Window(title, [

        [sg.T("Please select a song")                                                           ],
        [sg.LB(songs, size=size, key="songSelected", select_mode=LISTBOX_SELECT_MODE_SINGLE)    ],
        [sg.B("Convert", size=size)                                                             ]
        

    ], element_justification="c", resizable=True, finalize=True)
    beatWin.bind('<Configure>', "Configure")

    while True:
        e1, v1 = beatWin.read()
        try:
            beatWin["songSelected"].expand(expand_x=True, expand_y=True)
        except:
            pass


        if e1 == "Convert":
            try:
                beatWin.close()
                if v1['songSelected'] == []: return
                return [os.path.join(OSUPATH, beatmap) for beatmap in v1['songSelected']]
            except:
                pass

        elif e1 == sg.WINDOW_CLOSED:
            beatWin.close()
            return