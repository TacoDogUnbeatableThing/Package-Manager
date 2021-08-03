from typing import final
import PySimpleGUI as sg
import json
import os
import zipfile as zp


ROOT = ""
def sendRoot(root):
    global ROOT
    ROOT = root


title = "TacoDog MC" #MC stands for "mod creator"
sg.theme("Topanga")


size = (10, 1)



#Action to pick if you want to create a mod or edit one
def actPick():
    #Window to pick between creating a mod or editing one
    firstWin = sg.Window(title, [

        [sg.B("Create mod", size=size) ],
        [sg.B("Edit mod", size=size)   ]

    ], element_justification="c", resizable=True)

    while True:
        e1, v1 = firstWin.read()


        if e1 == "Create mod":
            #Window to put in details about the new mod being created
            createWin = sg.Window(title, [

                [sg.T("Mod name:", size=size),  sg.Input(key="name") ],
                [sg.B("Create", size=size)                           ]

            ], element_justification="c", modal=True, resizable=True)

            while True:
                e2, v2 = createWin.read()


                if e2 == "Create":
                    createWin.close()
                    firstWin.close()

                    return zp.ZipFile(f"modfiles/{v2['name']}.bmap", "w", compression=zp.ZIP_LZMA)

                elif e2 == sg.WINDOW_CLOSED:
                    createWin.close()
                    break

        elif e1 == "Edit mod":
            #Window to put in details about the mod to be edited
            for _, _, files in os.walk("modfiles"):
                modConfigs = files
                break

            editWin = sg.Window(title, [

                [sg.T("Please select a mod")                                                                ],
                [sg.LB(modConfigs, size=size, key="modSelected", select_mode="LISTBOX_SELECT_MODE_SINGLE")  ],
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
                        zip = zp.ZipFile(f"modfiles/{v2['modSelected'][0]}", "w")
                        
                        editWin.close()
                        firstWin.close()

                        return zip
                    except:
                        pass

                elif e2 == sg.WINDOW_CLOSED:
                    editWin.close()
                    break

        elif e1 == sg.WINDOW_CLOSED: 
            firstWin.close()

            return


#Select beatmap window
def selBeatmap(OSUPATH):
    #Select beatmap window
    for _, dirs, _ in os.walk(OSUPATH):
        songs = dirs
        break

    beatWin = sg.Window(title, [

        [sg.T("Please select a song")                                                           ],
        [sg.LB(songs, size=size, key="songSelected", select_mode="LISTBOX_SELECT_MODE_SINGLE")  ],
        [sg.I(key="folderInput", size=size), sg.FolderBrowse("Browse", size=size)               ],
        [sg.B("Convert", size=size)                                                             ]
        

    ], element_justification="c", resizable=True, finalize=True)
    beatWin.bind('<Configure>', "Configure")

    while True:
        e1, v1 = beatWin.read()
        try:
            beatWin["songSelected"].expand(expand_x=True, expand_y=True)
            beatWin["folderInput"].expand(expand_x=True)
        except:
            pass


        if e1 == "Convert":
            try:
                beatWin.close()

                if v1["folderInput"] == "":
                    return os.path.join(OSUPATH, v1['songSelected'][0])
                else:
                    return v1["folderInput"]
            except:
                pass

        elif e1 == sg.WINDOW_CLOSED:
            beatWin.close()
            return