from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import os

FILES_PATH = os.path.join(Path(__file__).parent, "data", "")
SYSTEM_PATH = os.path.join(Path(__file__).parent, "system", "")

rootTitle = "Flashcards"
rootX = 400
rootY = 400
rootSize = f"{rootX}x{rootY}"
rootBGColor = "#333"
rootFGColor = "#BBB"
rootDimFGColor = "#555"
font = ("Times New Roman", 20, "bold")
smallFont = ("Times New Roman", 11, "bold")
tinyFont = ("Times New Roman", 8, "bold")

global testingData
testingData = []
global delimiter
delimiter = " : "
global savedPath
savedPath = ""
global columns
columns = [1, 2]
global correctAnswers
correctAnswers = 0
global incorrectAnswers
incorrectAnswers = 0


global currentFrame
currentFrame = 0

# Checks if data exists for continuing, and forces entry of a new target file and delimiter if it does not.
def IntroFrame():
    global currentFrame
    currentFrame = 0

    frame = tk.Frame(root, bg=rootBGColor, height=rootY)
    frame.pack()

    introLabel = tk.Label(frame, text="F L A S H C A R D S", bg=rootBGColor, fg=rootFGColor, font=font)
    introLabel.pack(pady=100, padx=78)

    introButton = tk.Button(frame, text="New", bg=rootBGColor, fg=rootFGColor, command=lambda: SetFrame(2))
    introButton.pack(pady=10)

    continueButton = tk.Button(frame, state=tk.DISABLED, text="Continue", bg=rootBGColor, fg=rootFGColor, highlightthickness=0, command=lambda: SetFrame(1)) 
    continueButton.pack()

    VerifyContinue(continueButton)

# Runs through existing flashcards until the end has been reached, at which point it will transfer to the end screen.
def FlashcardFrame():
    global testingData
    global columns

    frame = tk.Frame(root, bg=rootBGColor, height=rootY)
    frame.pack()

    titleButton = tk.Button(frame, text="Back", bg=rootBGColor, fg=rootFGColor, command=lambda: SetFrame(0))
    titleButton.pack()

    quizLabel = tk.Label(frame, text=testingData[0][columns[0]], bg=rootBGColor, fg=rootFGColor, font=font)
    quizLabel.pack(pady=80, padx=78)

    answerLabel = tk.Label(frame, text=" ", bg=rootBGColor, fg=rootFGColor, font=font)
    answerLabel.pack(pady=25, padx=78)

    instructionLabel = tk.Label(frame, text="Press LEFT if correct, or RIGHT if incorrect", bg=rootBGColor, fg=rootFGColor, font=smallFont)
    instructionLabel.pack(side="bottom", pady=3)

    # Show the correct answer and await the user's determination.
    def ShowAnswer(labelToFill, event=None):
        global testingData
        global columns
        labelToFill.config(text=testingData[0][columns[1]])
        root.bind("<Left>", lambda e: Next((1, 0)))
        root.bind("<Right>", lambda e: Next((0, 1)))

    def Next(rightWrong, event=None):
        global correctAnswers
        global incorrectAnswers
        
        correctAnswers += rightWrong[0]
        incorrectAnswers += rightWrong[1]

        global testingData
        if rightWrong[0] == 1:
            testingData.pop(0)
        else:
            testingData.append(testingData.pop(0))
        SaveSettings()


        if len(testingData) >= 1:
            SetFrame(1)
        else:
            SetFrame(0)
        root.unbind("<Right>")
        root.unbind("<Left>")

    root.bind("<Return>", lambda e: ShowAnswer(answerLabel))

# Runs through existing flashcards until the end has been reached, at which point it will transfer to the end screen.
def SetupFrame():
    frame = tk.Frame(root, bg=rootBGColor, height=rootY)
    frame.pack(fill="x")

    titleButton = tk.Button(frame, text="Back", bg=rootBGColor, fg=rootFGColor, command=lambda: SetFrame(0))
    titleButton.pack()

    tk.Label(frame, bg=rootBGColor, height=rootY, width=rootX).pack(fill="both") # Guarantee visibility of items being placed in the frame

    pathErrorLabel = tk.Label(frame, text="", bg=rootBGColor, fg="#FF0000", font=smallFont)
    pathErrorLabel.place(x=20, y=80)

    pathLabel = tk.Label(frame, text="File path: ", bg=rootBGColor, fg=rootFGColor, font=smallFont)
    pathLabel.place(x=20, y=40)

    def ValidateFile(value):
        if os.path.exists(value) and value.endswith(".txt"):
            with open(value) as file:
                data = file.readlines()
                if len(data) == 0:
                    pathErrorLabel.config(text="File is empty")
                    SetExampleLineText("---")
                    delimiterEntry.config(state=tk.DISABLED, highlightthickness=0)
                    delimiterLabel.config(fg=rootDimFGColor)
                else: # The file is usable
                    pathErrorLabel.config(text="")
                    SetExampleLineText(data[0].replace('\n', ''))
                    delimiterEntry.config(state=tk.NORMAL, highlightthickness=1)
                    delimiterLabel.config(fg=rootFGColor)
        else:
            if value != "": pathErrorLabel.config(text="Invalid file path")
            else: pathErrorLabel.config(text="")
            SetExampleLineText("---")
            delimiterEntry.config(state=tk.DISABLED, highlightthickness=0)
            delimiterLabel.config(fg=rootDimFGColor)
        return True
    
    vcmd = (frame.register(ValidateFile), '%P')

    pathEntry = tk.Entry(frame, bg=rootBGColor, fg=rootFGColor, font=smallFont, width=28)
    pathEntry.config(validate='key', validatecommand=vcmd)
    pathEntry.place(x=90, y=40)

    def BrowseForFile():
        path = filedialog.askopenfilename(title="Select a list:", filetypes=[("Text Files", "*.txt")])
        if path != None and path != '':
            pathEntry.delete(0, tk.END)
            pathEntry.insert(0, path)

    pathButton = tk.Button(frame, bg=rootBGColor, text="Browse", fg=rootFGColor, font=smallFont, pady=-2, command=BrowseForFile)
    pathButton.place(x=294, y=40)

    def SetExampleLineText(text):
        exampleLine.config(state=tk.NORMAL)
        exampleLine.delete("1.0", tk.END)
        exampleLine.insert("1.0", text)
        exampleLine.tag_configure("justify", justify="center")
        exampleLine.tag_add("justify", "1.0", "end")
        exampleLine.config(state=tk.DISABLED)

    exampleLineText = tk.Label(frame, text="Example data", width=35, justify="center", bg=rootBGColor, fg=rootFGColor)
    exampleLineText.place(y=100, x=60)

    exampleLine = tk.Text(frame, state=tk.NORMAL, width=54, height=1, wrap=None, font=tinyFont)
    SetExampleLineText("---")
    
    exampleLine.config(state=tk.DISABLED)
    exampleLine.place(y=130, x=60)

    delimiterLabel = tk.Label(frame, text="Delimiter/Separator: ", bg=rootBGColor, fg=rootDimFGColor, font=smallFont)
    delimiterLabel.place(x=20, y=200)

    def ColorDelimiter(input):
        exampleLine.tag_delete("colorTag")

        if input.upper() == "TAB": input = "	"

        string = exampleLine.get('1.0', 'end-1c')
        substring = input
        
        positions = [i for i in range(len(string)) if string.startswith(substring, i)]

        for position in positions:
            exampleLine.tag_add("colorTag", f"1.{position}", f"1.{position + len(substring)}")
        exampleLine.tag_config("colorTag", background="lightgreen")

        if (string == ""): exampleLine.tag_delete("colorTag")
        ValidateDelimiter(input)
        return True
    
    def ValidateDelimiter(currentDelimiter):
        if currentDelimiter == "": 
            delimiterErrorLabel.config(text="")
            quizOnSpinbox.config(state=tk.DISABLED, highlightthickness=0)
            quizOnLabel.config(fg=rootDimFGColor)
            answerSpinbox.config(state=tk.DISABLED, highlightthickness=0)
            answerLabel.config(fg=rootDimFGColor)
            submitButton.config(state=tk.DISABLED, highlightthickness=0)
            return
        data = OpenDataFile(pathEntry.get())
        splitData = SplitData(data, currentDelimiter)
        if VerifyColumnCount(splitData):
            delimiterErrorLabel.config(text="")
            quizOnSpinbox.config(state=tk.NORMAL, highlightthickness=1)
            quizOnLabel.config(fg=rootFGColor)
            answerSpinbox.config(state=tk.NORMAL, highlightthickness=1)
            answerLabel.config(fg=rootFGColor)
            quizOnSpinbox.config(from_=1, to=len(splitData[0]))
            answerSpinbox.config(from_=1, to=len(splitData[0]))
            submitButton.config(state=tk.NORMAL, highlightthickness=1)
        else:
            delimiterErrorLabel.config(text="Unequal number of columns in all rows")
            quizOnSpinbox.config(state=tk.DISABLED, highlightthickness=0)
            quizOnLabel.config(fg=rootDimFGColor)
            answerSpinbox.config(state=tk.DISABLED, highlightthickness=0)
            answerLabel.config(fg=rootDimFGColor)
            submitButton.config(state=tk.DISABLED, highlightthickness=0)
            exampleLine.tag_delete("quiz")
            exampleLine.tag_delete("answer")

    delimiterVal = (frame.register(ColorDelimiter), '%P')

    delimiterEntry = tk.Entry(frame, bg=rootBGColor, fg=rootFGColor, font=smallFont, width=8, disabledbackground=rootBGColor)
    delimiterEntry.config(validate='key', validatecommand=delimiterVal, state=tk.DISABLED, highlightthickness=0)
    delimiterEntry.place(x=170, y=200)

    delimiterErrorLabel = tk.Label(frame, text="", bg=rootBGColor, fg="#FF0000", font=smallFont)
    delimiterErrorLabel.place(x=20, y=220)

    quizOnLabel = tk.Label(frame, text="Column to quiz on: ", bg=rootBGColor, fg=rootDimFGColor, font=smallFont)
    quizOnLabel.place(x=20, y=240)

    def ColValidate(tagToModify, color, input):
        if not input.isdigit() or int(input) < 1 or int(input) > len(exampleLine.get("1.0", tk.END).split(delimiterEntry.get())): 
            return False
        
        inputNum = int(input) - 1
        exampleArray = exampleLine.get('1.0', 'end-1c').split(delimiterEntry.get())

        exampleLine.tag_delete(tagToModify)

        tempString = ""
        for i in range(0, inputNum):
            tempString += exampleArray[i] + delimiterEntry.get()

        exampleLine.tag_add(tagToModify, f"1.{len(tempString)}", f"1.{len(tempString) + len(exampleArray[inputNum])}")
        exampleLine.tag_config(tagToModify, background=color)

        return True

    quizOnVal = (frame.register(lambda P: ColValidate("quiz", "pink", P)), '%P')

    quizOnSpinbox = tk.Spinbox(frame, state=tk.DISABLED, bg=rootBGColor, fg=rootFGColor, font=smallFont, width=8, disabledbackground=rootBGColor, validate="key", validatecommand=quizOnVal)
    quizOnSpinbox.place(x=170, y=240)

    answerLabel = tk.Label(frame, text="Answer column: ", bg=rootBGColor, fg=rootDimFGColor, font=smallFont)
    answerLabel.place(x=20, y=280)

    answerVal = (frame.register(lambda P: ColValidate("answer", "lightblue", P)), '%P')

    answerSpinbox = tk.Spinbox(frame, state=tk.DISABLED, bg=rootBGColor, fg=rootFGColor, font=smallFont, width=8, disabledbackground=rootBGColor, validate="key", validatecommand=answerVal)
    answerSpinbox.place(x=170, y=280)

    def SaveData():
        with open(os.path.join(SYSTEM_PATH, "save.txt"), "w") as saveFile:
            global testingData
            global delimiter
            global savedPath
            global columns

            savedPath = pathEntry.get()

            targetData = OpenDataFile(pathEntry.get())
            saveFile.writelines(targetData)
            temp = delimiterEntry.get()
            if temp == "tab": temp = "\t"
            delimiter = temp
            testingData = SplitData(targetData, delimiter)
            columns = [int(quizOnSpinbox.get()) - 1, int(answerSpinbox.get()) - 1]

            SaveSettings()
            SetFrame(1)

    submitButton = tk.Button(frame, text="Start testing", state=tk.DISABLED, highlightthickness=0, bg=rootBGColor, fg=rootFGColor, font=smallFont, command=SaveData)
    submitButton.place(x=146, y=335)


def SetFrame(target):
    global currentFrame
    currentFrame = target

    # Intro/Title
    if target == 0:
        ClearFrame()
        IntroFrame()
        root.unbind("<Return>")
    # Flashcards
    elif target == 1:
        ClearFrame()
        FlashcardFrame()
    elif target == 2:
        ClearFrame()
        SetupFrame()
        root.unbind("<Return>")

# Clear the screen, allowing new widgets to be created.
def ClearFrame():
    for child in root.winfo_children():
        child.destroy()

# ------------------------------------------------------------------------------------------------------------------------

# Check upon open whether there is save data; if there is none, do not permit continuing.
def VerifyContinue(widget):
    global testingData
    global delimiter

    data = OpenDataFile(SYSTEM_PATH + "save.txt")
    if data != None:
        splitData = SplitData(data, delimiter)
        if (VerifyColumnCount(splitData)):
            testingData = splitData
            widget.config(state=tk.NORMAL, highlightthickness=1)

# Open the data file (if it exists) and return the lines of data as an array (if the data exists)
def OpenDataFile(path):
    file = open(path, 'r', encoding='utf-8')
    data = file.readlines()
    file.close()
    return data
        
def SplitData(array, delimiter):
    data = []
    for line in array:
        data.append(line.split(delimiter))
    return data

# Make certain that there is an equal number of columns in a text file.
def VerifyColumnCount(array):
    isValid = True
    try:
        targetLineCount = len(array[0])
        if targetLineCount < 2: isValid = False
        for line in array:
            if len(line) != targetLineCount:
                isValid = False
        return isValid
    except:
        return False
    
def CompileRow(dataToCompile, delimiter):
    newData = []
    for row in dataToCompile:
        wordCount = 0
        tempString = ""
        for data in row:
            wordCount += 1
            if wordCount != len(row):
                tempString += data + delimiter
            else:
                tempString += data
        newData.append(tempString)

    return newData
    
def SaveSettings():
    global delimiter
    global columns
    global correctAnswers
    global incorrectAnswers
    global testingData

    linesToWrite = [ delimiter, str(columns[0]), str(columns[1]), str(correctAnswers), str(incorrectAnswers) ]

    file = open(os.path.join(SYSTEM_PATH, "settings.txt"), 'w', encoding="utf-8")
    for line in linesToWrite:
        file.write(line + "\n")
    file.close()

    file = open(os.path.join(SYSTEM_PATH, "save.txt"), 'w', encoding="utf-8")
    for line in CompileRow(testingData, delimiter):
        file.write(line)
    file.close()

def LoadSettings():
    global delimiter
    global columns
    global correctAnswers
    global incorrectAnswers
    
# ------------------------------------------------------------------------------------------------------------------------

root = tk.Tk()
root.title(rootTitle)
root.geometry(rootSize)
root.config(bg=rootBGColor)
root.resizable(False, False)

IntroFrame()

root.mainloop()