import tkinter as tk

rootTitle = "Flashcards"
rootX = 400
rootY = 400
rootSize = f"{rootX}x{rootY}"
rootBGColor = "#333"
rootFGColor = "#BBB"
font = ("Times New Roman", 21, "bold")
smallFont = ("Times New Roman", 11, "bold")

global currentFrame
currentFrame = 0

def IntroFrame():
    global currentFrame
    currentFrame = 0

    frame = tk.Frame(root, bg=rootBGColor, height=rootY)
    frame.pack()

    introLabel = tk.Label(frame, text="Welcome!", bg=rootBGColor, fg=rootFGColor, font=font)
    introLabel.pack(pady=100, padx=78)

    introButton = tk.Button(frame, text="Next", bg=rootBGColor, fg=rootFGColor, command=ChangeFrame)
    introButton.pack()

def FlashcardFrame():
    frame = tk.Frame(root, bg=rootBGColor, height=rootY)
    frame.pack()

    settingsButton = tk.Button(frame, text="Settings", bg=rootBGColor, fg=rootFGColor, command=ChangeFrame)
    settingsButton.pack()

    introLabel = tk.Label(frame, text="---", bg=rootBGColor, fg=rootFGColor, font=font)
    introLabel.pack(pady=100, padx=78)

    answerLabel = tk.Label(frame, text=" ", bg=rootBGColor, fg=rootFGColor, font=font)
    answerLabel.pack(pady=50, padx=78)

    instructionLabel = tk.Label(frame, text="Press LEFT if correct, or RIGHT if incorrect", bg=rootBGColor, fg=rootFGColor, font=smallFont)
    instructionLabel.pack(pady=3)

    root.bind("<Return>", lambda event: ShowAnswer(answerLabel))

def SettingsFrame():
    frame = tk.Frame(root, bg=rootBGColor)
    frame.pack()

    introLabel = tk.Label(frame, text="Settings page", bg=rootBGColor, fg=rootFGColor)
    introLabel.pack()

    introButton = tk.Button(frame, text="Next", bg=rootBGColor, fg=rootFGColor, command=ChangeFrame)
    introButton.pack()

def ChangeFrame():
    global currentFrame
    
    if currentFrame == 0:
        currentFrame += 1
        ClearFrame()
        FlashcardFrame()
    elif currentFrame == 1:
        currentFrame += 1
        ClearFrame()
        SettingsFrame()
    elif currentFrame == 2:
        currentFrame = 0
        ClearFrame()
        IntroFrame()

# Clear the screen, allowing new widgets to be created.
def ClearFrame():
    for child in root.winfo_children():
        child.destroy()

def ShowAnswer(labelToFill, event=None):
    labelToFill.config(text="Success!")
        


root = tk.Tk()
root.title(rootTitle)
root.geometry(rootSize)
root.config(bg=rootBGColor)
root.resizable(False, False)

IntroFrame()

root.mainloop()