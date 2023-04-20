import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

import json, os, requests

SFM_CONSTANT = 3.819
LABEL_FONT = ("Roboto", 16, "bold")
BUTTON_FONT = ("Roboto", 13, "bold")
ENTRY_FONT = ("Roboto", 16)
CUTTING_PROCESSES = ["Drilling", "Milling"]
TOOL_MATERIALS = ["HSS", "Carbide"]
THEME = ["blue", "green", "dark-blue", "themes/FireAtDusk.json", "themes/Redline.json"][-1] # <-- Change this index to whatever theme you want to use, or, put the path to your own custom theme here and use that index


# INIT GITHUB DATA
def initData():
    global MATERIALS, TAPS
    if os.path.exists("data/MATERIALS.json"):
        with open("data/MATERIALS.json", "r") as f:
            MATERIALS = json.load(f)
    else:
        MATERIALS = requests.get("https://raw.githubusercontent.com/Jeikobuka/MachinistHandbook/main/data/MATERIALS.json").json()
    if os.path.exists("data/TAPS.json"):
        with open("data/TAPS.json", "r") as f:
            TAPS = json.load(f)
    else:
        TAPS = requests.get("https://raw.githubusercontent.com/Jeikobuka/MachinistHandbook/main/data/TAPS.json").json()
initData()
try:
    ctk.set_default_color_theme(THEME)
except Exception as e:
    print(e)
    print("No such theme in themes directory, defaulting to blue theme")
    ctk.set_default_color_theme("blue")
def getMaterialSFM():
    if isEntryBlank([genMatVar, matAlloyVar, toolMatVar, cuttingProcessVar]):
        sfm = MATERIALS[genMatVar.get()][matAlloyVar.get()][toolMatVar.get()][cuttingProcessVar.get()]
        sfmEntry.delete(0, tk.END)
        sfmEntry.insert(0, sfm)
    else:
        print("Missing parameters required for calculation")

def getRPM(toolDiameter, sfm):
    if isEntryBlank([sfmEntryVar, toolDiaEntryVar]):
        rpm = round((float(sfm) * 3.819) / float(toolDiameter))
        rpmEntry.delete(0, tk.END)
        rpmEntry.insert(0, rpm)
    else:
        print("Missing parameters required for calculation")

def getFeedrate(rpm, ipt, fluteCount):
    if isEntryBlank([rpmEntryVar, iptEntryVar, fluteCountEntryVar]):
        feed = round((float(rpm) * float(ipt) * int(fluteCount)), 2)
        feedEntry.delete(0, tk.END)
        feedEntry.insert(0, feed)
    else:
        print("Missing parameters required for calculation")

def clearEntryBoxes():
    sfmEntryVar.set(value="")
    toolDiaEntryVar.set(value="")
    rpmEntryVar.set(value="")
    iptEntryVar.set(value="")
    fluteCountEntryVar.set(value="")
    feedEntryVar.set(value="")

def isEntryBlank(varVals):
    for varVal in varVals:
        if varVal.get().strip() == "":
            print(varVal)
            tk.messagebox.showwarning(title="Invalid Parameters", message="Missing parameters required for calculation")
            return False
    return True
def _genMatCallback(choice):
    matAlloyCombobox.configure(values=list(MATERIALS[choice].keys()))
    matAlloyCombobox.set(list(MATERIALS[choice].keys())[0])
    _matAlloyCallback(list(MATERIALS[choice].keys())[0])
def _matAlloyCallback(choice):
    print(choice)

ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.geometry("475x550")
root.title("Machinist's Handbook")
root.attributes("-topmost", True)
root.resizable(False, False)
# ----- TABS -----
tabs = ctk.CTkTabview(root)
tabs.add("Speeds & Feeds Calculator")
tabs.add("Conversions")
tabs.add("Thread Info")
tabs.pack(padx=20, pady=20, expand=True, fill=tk.BOTH)
# ----- CALCULATOR VARIABLES -----
genMatVar = tk.StringVar(value="Aluminum")
matAlloyVar = tk.StringVar(value="6061")
cuttingProcessVar = tk.StringVar(value="Milling")
toolMatVar = tk.StringVar(value="Carbide")
sfmEntryVar = tk.StringVar()#value="500")
toolDiaEntryVar = tk.StringVar()#value=".5")
rpmEntryVar = tk.StringVar()#value="3819")
iptEntryVar = tk.StringVar()#value=".001")
fluteCountEntryVar = tk.StringVar()#value="3")
feedEntryVar = tk.StringVar()#value="11.46")
# ----- CALCULATOR FRAMES -----
calcFrame = ctk.CTkFrame(tabs.tab("Speeds & Feeds Calculator"))
calcFrame.pack(padx=10, pady=10, side=tk.TOP, fill=tk.X)
entryFrame = ctk.CTkFrame(tabs.tab("Speeds & Feeds Calculator"))
entryFrame.pack(padx=10, pady=10, anchor="center", expand=True, fill=tk.BOTH)
buttonFrame = ctk.CTkFrame(tabs.tab("Speeds & Feeds Calculator"))
buttonFrame.pack(padx=10, pady=10, side=tk.BOTTOM, fill=tk.X)
# ----- MATERIAL -----
genMatLabel = ctk.CTkLabel(calcFrame, text="Material", font=LABEL_FONT)
genMatLabel.grid(row=0, column=1, padx=10)
genMatCombobox = ctk.CTkComboBox(calcFrame, values=list(MATERIALS.keys()), command=_genMatCallback, variable=genMatVar, width=120, font=BUTTON_FONT)
genMatCombobox.grid(row=1, column=1, padx=8, pady=10, sticky="w")
# ----- ALLOY -----
matAlloyLabel = ctk.CTkLabel(calcFrame, text="Alloy", font=LABEL_FONT)
matAlloyLabel.grid(row=0, column=2, padx=10)
matAlloyCombobox = ctk.CTkComboBox(calcFrame, values=list(MATERIALS["Aluminum"].keys()), command=_matAlloyCallback, variable=matAlloyVar, width=120, font=BUTTON_FONT)
matAlloyCombobox.grid(row=1, column=2, padx=8, pady=10, sticky="e")
# ----- CUTTING PROCESS -----
cutProcessLabel = ctk.CTkLabel(calcFrame, text="Cutting Process", font=LABEL_FONT)
cutProcessLabel.grid(row=2, column=1, padx=10)
cuttingProcessCombobox = ctk.CTkComboBox(calcFrame, values=CUTTING_PROCESSES, command=_matAlloyCallback, variable=cuttingProcessVar, width=120, font=BUTTON_FONT)
cuttingProcessCombobox.grid(row=3, column=1, padx=8, pady=10, sticky="w")
# ----- TOOL MATERIAL -----
toolMatLabel = ctk.CTkLabel(calcFrame, text="Tool Material", font=LABEL_FONT)
toolMatLabel.grid(row=2, column=2, padx=10)
toolMatCombobox = ctk.CTkComboBox(calcFrame, values=TOOL_MATERIALS, command=_matAlloyCallback, variable=toolMatVar, width=120, font=BUTTON_FONT)
toolMatCombobox.grid(row=3, column=2, padx=8, pady=10, sticky="e")
# ----- IPT -----
iptLabel = ctk.CTkLabel(calcFrame, text="IPT", font=LABEL_FONT)
iptLabel.grid(row=0, column=3, padx=10)
iptEntry = ctk.CTkEntry(calcFrame, placeholder_text="IPT", textvariable=iptEntryVar, width=80, font=ENTRY_FONT)
iptEntry.grid(row=1, column=3)
# ----- FLUTE COUNT -----
fluteCountLabel = ctk.CTkLabel(calcFrame, text="Flute Count", font=LABEL_FONT)
fluteCountLabel.grid(row=2, column=3, padx=10)
fluteCountEntry = ctk.CTkEntry(calcFrame, placeholder_text="Flute Count", textvariable=fluteCountEntryVar, width=80, font=ENTRY_FONT)
fluteCountEntry.grid(row=3, column=3)
# ----- SFM -----
sfmLabel = ctk.CTkLabel(entryFrame, text="SFM: ", font=LABEL_FONT)
sfmLabel.grid(row=0, column=0, padx=10, pady=10, sticky="w")
sfmEntry = ctk.CTkEntry(entryFrame, placeholder_text="SFM", textvariable=sfmEntryVar, font=ENTRY_FONT)
sfmEntry.grid(row=0, column=1, pady=10, sticky="w")
sfmButton = ctk.CTkButton(entryFrame, text="Get SFM", command=getMaterialSFM, width=60, font=BUTTON_FONT)
sfmButton.grid(row=0, column=2, padx=10, pady=10, sticky="w")
# ----- TOOL DIAMETER -----
toolDiaLabel = ctk.CTkLabel(entryFrame, text="Tool Diameter: ", font=LABEL_FONT)
toolDiaLabel.grid(row=1, column=0, padx=10, pady=10, sticky="w")
toolDiaEntry = ctk.CTkEntry(entryFrame, placeholder_text="Tool Diameter", textvariable=toolDiaEntryVar, font=ENTRY_FONT)
toolDiaEntry.grid(row=1, column=1, pady=10, sticky="w")
# ----- RPM -----
rpmLabel = ctk.CTkLabel(entryFrame, text="RPM: ", font=LABEL_FONT)
rpmLabel.grid(row=2, column=0, padx=10, pady=10, sticky="w")
rpmEntry = ctk.CTkEntry(entryFrame, placeholder_text="RPM", textvariable=rpmEntryVar, font=ENTRY_FONT)
rpmEntry.grid(row=2, column=1, pady=10, sticky="w")
rpmButton = ctk.CTkButton(entryFrame, text="Get RPM", command=lambda: getRPM(toolDiaEntryVar.get(), sfmEntryVar.get()), width=60, font=BUTTON_FONT)
rpmButton.grid(row=2, column=2, padx=10, pady=10, sticky="w")
# ----- FEEDRATE -----
feedLabel = ctk.CTkLabel(entryFrame, text="Feedrate: ", font=LABEL_FONT)
feedLabel.grid(row=3, column=0, padx=10, pady=10, sticky="w")
feedEntry = ctk.CTkEntry(entryFrame, placeholder_text="Feedrate", textvariable=feedEntryVar, font=ENTRY_FONT)
feedEntry.grid(row=3, column=1, pady=10, sticky="w")
feedButton = ctk.CTkButton(entryFrame, text="Get Feedrate", command=lambda:getFeedrate(rpmEntryVar.get(), iptEntryVar.get(), fluteCountEntryVar.get()), width=60, font=BUTTON_FONT)
feedButton.grid(row=3, column=2, padx=10, pady=10, sticky="w")
# ----- CALCULATOR CONTROL ------
exitButton = ctk.CTkButton(buttonFrame, text="Exit", command=root.destroy, width=60, font=BUTTON_FONT)
exitButton.pack(padx=10, pady=10, side=tk.RIGHT, anchor="se")
clearButton = ctk.CTkButton(buttonFrame, text="Clear Entry Boxes", command=clearEntryBoxes, width=60, font=BUTTON_FONT)
clearButton.pack(padx=10, pady=10, side=tk.RIGHT, anchor="se")
# -------------------------------------------------------------------------------------------------------
# ----- CONVERSION FRAMES -----
conversionFrame = ctk.CTkFrame(tabs.tab("Conversions"))
conversionFrame.pack(padx=10, pady=10, anchor="center", expand=True, fill=tk.BOTH)
conversionButtonFrame = ctk.CTkFrame(tabs.tab("Conversions"))
conversionButtonFrame.pack(padx=10, pady=10, side=tk.BOTTOM, fill=tk.X)
CONVERSIONS = {
    "MM2IN":"/25.4", 
    "IN2MM":"*25.4",
    "KM2MI": "/1.609",
    "MI2KM": "*1.609",
    "GAL2L": "/3.785",
    "L2GAL": "*3.785"
}

def getConversion():
    res = eval(conversionEntryVar.get()+CONVERSIONS[conversionComboboxVar.get()])
    print(res)
    conversionEntryVar.set(str(res))
    return res

# ----- CONVERSION VARIABLES -----
conversionEntryVar = tk.StringVar()
conversionComboboxVar = tk.StringVar(value="MM2IN")

# ----- CONVERT ------
conversionCombobox = ctk.CTkComboBox(conversionFrame, values=CONVERSIONS.keys(), variable=conversionComboboxVar, width=140, font=BUTTON_FONT)
conversionCombobox.grid(row=0, column=0, padx=10, pady=10, sticky="w")
conversionEntry = ctk.CTkEntry(conversionFrame, placeholder_text="Type your value here...", textvariable=conversionEntryVar, font=ENTRY_FONT)
conversionEntry.grid(row=0, column=1, pady=10, sticky="w")
conversionButton = ctk.CTkButton(conversionFrame, text="Convert!", command=getConversion, width=60, font=BUTTON_FONT)
conversionButton.grid(row=0, column=2, padx=10, pady=10, sticky="w")
'''
# ----- POST-POST-PROCESSORS -----
pPostProcessorButton = ctk.CTkButton(conversionFrame, text="Open File to Convert!", width=60)
pPostProcessorButton.grid(row=1, column=1, padx=10, pady=10, sticky="w")
pPostProcessorButton.bind("<<Drop>>", on_drop)
'''
# ----- CONVERSION CONTROL ------
conversionExitButton = ctk.CTkButton(conversionButtonFrame, text="Exit", command=root.destroy, width=60, font=BUTTON_FONT)
conversionExitButton.pack(padx=10, pady=10, side=tk.RIGHT, anchor="se")
# -------------------------------------------------------------------------------------------------------
# ----- THREAD INFO VARIABLES -----
standardOrMetricComboboxVar = tk.StringVar(value="Standard")
threadInfoComboboxVar = tk.StringVar(value="1/4-20")

def _standardOrMetricCallback(choice):
    threadInfoCombobox.configure(values=list(TAPS[choice].keys()))
    threadInfoCombobox.set(list(TAPS[choice].keys())[0])

# ----- THREAD INFO FRAMES -----
threadInfoFrame = ctk.CTkFrame(tabs.tab("Thread Info"))
threadInfoFrame.pack(padx=10, pady=10, anchor="center", expand=True, fill=tk.BOTH)
threadInfoButtonFrame = ctk.CTkFrame(tabs.tab("Thread Info"))
threadInfoButtonFrame.pack(padx=10, pady=10, side=tk.BOTTOM, fill=tk.X)

# ----- THREAD INFO ------
standardOrMetricCombobox = ctk.CTkOptionMenu(threadInfoFrame, values=list(TAPS.keys()), variable=standardOrMetricComboboxVar, command=_standardOrMetricCallback, width=110, font=BUTTON_FONT)
standardOrMetricCombobox.grid(row=0, column=0, padx=10, pady=10, sticky="w")
threadInfoCombobox = ctk.CTkOptionMenu(threadInfoFrame, values=list(TAPS[standardOrMetricComboboxVar.get()].keys()), variable=threadInfoComboboxVar, width=140, font=BUTTON_FONT)
threadInfoCombobox.grid(row=0, column=1, padx=10, pady=10, sticky="w")
threadInfoButton = ctk.CTkButton(threadInfoFrame, text="Thread Info", command=getConversion, width=60, font=BUTTON_FONT)
threadInfoButton.grid(row=0, column=2, padx=10, pady=10, sticky="w")

# ----- THREAD INFO CONTROL ------
threadInfoExitButton = ctk.CTkButton(threadInfoButtonFrame, text="Exit", command=root.destroy, width=60, font=BUTTON_FONT)
threadInfoExitButton.pack(padx=10, pady=10, side=tk.RIGHT, anchor="se")

root.mainloop()
