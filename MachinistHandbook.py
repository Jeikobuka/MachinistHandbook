import customtkinter as ctk
import tkinter as tk

import json, os, requests

SFM_CONSTANT = 3.819
GEN_FONT = ("Roboto", 16, "bold")
CUTTING_PROCESSES = ["Drilling", "Milling"]
TOOL_MATERIALS = ["HSS", "Carbide"]
THEME = ["blue", "green", "dark-blue", "themes/FireAtDusk.json", "themes/Redline.json"][1] # <-- Change this index to whatever theme you want to use, or, put the path to your own custom theme here and use that index

if os.path.exists("data/MATERIALS.json"):
    with open("data/MATERIALS.json", "r") as f:
        MATERIALS = json.load(f)
else:
    MATERIALS = requests.get("https://raw.githubusercontent.com/Jeikobuka/MachinistHandbook/main/data/MATERIALS.json").json()

try:
    ctk.set_default_color_theme(THEME)
except Exception as e:
    print(e)
    print("No such theme in themes directory, defaulting to blue theme")
    ctk.set_default_color_theme("blue")
def getMaterialSFM():
    sfm = MATERIALS[genMatVar.get()][matAlloyVar.get()][toolMatVar.get()][cuttingProcessVar.get()]
    sfmEntry.delete(0, tk.END)
    sfmEntry.insert(0, sfm)

def getRPM(toolDiameter, sfm):
    rpm = round((float(sfm) * 3.819) / float(toolDiameter))
    rpmEntry.delete(0, tk.END)
    rpmEntry.insert(0, rpm)

def getFeedrate(rpm, ipt, fluteCount):
    feed = round((float(rpm) * float(ipt) * int(fluteCount)), 2)
    feedEntry.delete(0, tk.END)
    feedEntry.insert(0, feed)

def clearEntryBoxes():
    sfmEntryVar.set(value="")
    toolDiaEntryVar.set(value="")
    rpmEntryVar.set(value="")
    iptEntryVar.set(value="")
    fluteCountEntryVar.set(value="")
    feedEntryVar.set(value="")

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

tabs = ctk.CTkTabview(root)
tabs.add("Calculator")
tabs.add("Conversions")
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
# ----- CONVERSION FRAMES -----
conversionFrame = ctk.CTkFrame(tabs.tab("Conversions"))
conversionFrame.pack(padx=10, pady=10, anchor="center", expand=True, fill=tk.BOTH)
conversionButtonFrame = ctk.CTkFrame(tabs.tab("Conversions"))
conversionButtonFrame.pack(padx=10, pady=10, side=tk.BOTTOM, fill=tk.X)
# ----- CALCULATOR FRAMES -----
calcFrame = ctk.CTkFrame(tabs.tab("Calculator"))
calcFrame.pack(padx=10, pady=10, side=tk.TOP, fill=tk.X)
entryFrame = ctk.CTkFrame(tabs.tab("Calculator"))
entryFrame.pack(padx=10, pady=10, anchor="center", expand=True, fill=tk.BOTH)
buttonFrame = ctk.CTkFrame(tabs.tab("Calculator"))
buttonFrame.pack(padx=10, pady=10, side=tk.BOTTOM, fill=tk.X)
# ----- MATERIAL -----
genMatLabel = ctk.CTkLabel(calcFrame, text="Material", font=("Roboto", 12, "bold"))
genMatLabel.grid(row=0, column=1, padx=10)
genMatCombobox = ctk.CTkComboBox(calcFrame, values=list(MATERIALS.keys()), command=_genMatCallback, variable=genMatVar, width=120)
genMatCombobox.grid(row=1, column=1, padx=8, pady=10, sticky="w")
# ----- ALLOY -----
matAlloyLabel = ctk.CTkLabel(calcFrame, text="Alloy", font=("Roboto", 12, "bold"))
matAlloyLabel.grid(row=0, column=2, padx=10)
matAlloyCombobox = ctk.CTkComboBox(calcFrame, values=list(MATERIALS["Aluminum"].keys()), command=_matAlloyCallback, variable=matAlloyVar, width=120)
matAlloyCombobox.grid(row=1, column=2, padx=8, pady=10, sticky="e")
# ----- CUTTING PROCESS -----
cutProcessLabel = ctk.CTkLabel(calcFrame, text="Cutting Process", font=("Roboto", 12, "bold"))
cutProcessLabel.grid(row=2, column=1, padx=10)
cuttingProcessCombobox = ctk.CTkComboBox(calcFrame, values=CUTTING_PROCESSES, command=_matAlloyCallback, variable=cuttingProcessVar, width=120)
cuttingProcessCombobox.grid(row=3, column=1, padx=8, pady=10, sticky="w")
# ----- TOOL MATERIAL -----
toolMatLabel = ctk.CTkLabel(calcFrame, text="Tool Material", font=("Roboto", 12, "bold"))
toolMatLabel.grid(row=2, column=2, padx=10)
toolMatCombobox = ctk.CTkComboBox(calcFrame, values=TOOL_MATERIALS, command=_matAlloyCallback, variable=toolMatVar, width=120)
toolMatCombobox.grid(row=3, column=2, padx=8, pady=10, sticky="e")
# ----- IPT -----
iptLabel = ctk.CTkLabel(calcFrame, text="IPT", font=("Roboto", 12, "bold"))
iptLabel.grid(row=0, column=3, padx=10)
iptEntry = ctk.CTkEntry(calcFrame, placeholder_text="IPT", textvariable=iptEntryVar, width=80)
iptEntry.grid(row=1, column=3)
# ----- FLUTE COUNT -----
fluteCountLabel = ctk.CTkLabel(calcFrame, text="Flute Count", font=("Roboto", 12, "bold"))
fluteCountLabel.grid(row=2, column=3, padx=10)
fluteCountEntry = ctk.CTkEntry(calcFrame, placeholder_text="Flute Count", textvariable=fluteCountEntryVar, width=80)
fluteCountEntry.grid(row=3, column=3)
# ----- SFM -----
sfmLabel = ctk.CTkLabel(entryFrame, text="SFM: ", font=GEN_FONT)
sfmLabel.grid(row=0, column=0, padx=10, pady=10, sticky="w")
sfmEntry = ctk.CTkEntry(entryFrame, placeholder_text="SFM", textvariable=sfmEntryVar)
sfmEntry.grid(row=0, column=1, pady=10, sticky="w")
sfmButton = ctk.CTkButton(entryFrame, text="Get SFM", command=getMaterialSFM, width=60)
sfmButton.grid(row=0, column=2, padx=10, pady=10, sticky="w")
# ----- TOOL DIAMETER -----
toolDiaLabel = ctk.CTkLabel(entryFrame, text="Tool Diameter: ", font=GEN_FONT)
toolDiaLabel.grid(row=1, column=0, padx=10, pady=10, sticky="w")
toolDiaEntry = ctk.CTkEntry(entryFrame, placeholder_text="Tool Diameter", textvariable=toolDiaEntryVar)
toolDiaEntry.grid(row=1, column=1, pady=10, sticky="w")
# ----- RPM -----
rpmLabel = ctk.CTkLabel(entryFrame, text="RPM: ", font=GEN_FONT)
rpmLabel.grid(row=2, column=0, padx=10, pady=10, sticky="w")
rpmEntry = ctk.CTkEntry(entryFrame, placeholder_text="RPM", textvariable=rpmEntryVar)
rpmEntry.grid(row=2, column=1, pady=10, sticky="w")
rpmButton = ctk.CTkButton(entryFrame, text="Get RPM", command=lambda: getRPM(toolDiaEntryVar.get(), sfmEntryVar.get()), width=60)
rpmButton.grid(row=2, column=2, padx=10, pady=10, sticky="w")
# ----- FEEDRATE -----
feedLabel = ctk.CTkLabel(entryFrame, text="Feedrate: ", font=GEN_FONT)
feedLabel.grid(row=3, column=0, padx=10, pady=10, sticky="w")
feedEntry = ctk.CTkEntry(entryFrame, placeholder_text="Feedrate", textvariable=feedEntryVar)
feedEntry.grid(row=3, column=1, pady=10, sticky="w")
feedButton = ctk.CTkButton(entryFrame, text="Get Feedrate", command=lambda:getFeedrate(rpmEntryVar.get(), iptEntryVar.get(), fluteCountEntryVar.get()), width=60)
feedButton.grid(row=3, column=2, padx=10, pady=10, sticky="w")
# ----- CALCULATOR CONTROL ------
exitButton = ctk.CTkButton(buttonFrame, text="Exit", command=root.destroy, width=60)
exitButton.pack(padx=10, pady=10, side=tk.RIGHT, anchor="se")
clearButton = ctk.CTkButton(buttonFrame, text="Clear Entry Boxes", command=clearEntryBoxes, width=60)
clearButton.pack(padx=10, pady=10, side=tk.RIGHT, anchor="se")
# -------------------------------------------------------------------------------------------------------

CONVERSIONS = {
    "MM2IN":"/25.4", 
    "IN2MM":"*25.4",
    "KM2MI": "/1.609",
    "MI2KM": "*1.609"
}

def getMM2IN():
    res = eval(conversionEntryVar.get()+CONVERSIONS[conversionComboboxVar.get()])
    print(res)
    return res

# ----- CALCULATOR VARIABLES -----
conversionEntryVar = tk.StringVar()
conversionComboboxVar = tk.StringVar(value="MM2IN")

# ----- CONVERT ------
conversionCombobox = ctk.CTkComboBox(conversionFrame, values=CONVERSIONS.keys(), variable=conversionComboboxVar, width=140)
conversionCombobox.grid(row=0, column=0, padx=10, pady=10, sticky="w")
conversionEntry = ctk.CTkEntry(conversionFrame, placeholder_text="Type your value here...", textvariable=conversionEntryVar)
conversionEntry.grid(row=0, column=1, pady=10, sticky="w")
conversionButton = ctk.CTkButton(conversionFrame, text="Convert!", command=getMM2IN, width=60)
conversionButton.grid(row=0, column=2, padx=10, pady=10, sticky="w")

# ----- CONVERSION CONTROL ------
conversionExitButton = ctk.CTkButton(conversionButtonFrame, text="Exit", command=root.destroy, width=60)
conversionExitButton.pack(padx=10, pady=10, side=tk.RIGHT, anchor="se")


root.mainloop()