################################################################################
##  Repository: clipboard-manager
##  Author:     Jake Berreth
##  Sources:    https://github.com/prashantgupta24/clipboard-manager
################################################################################
from tkinter import Tk, Label, RAISED
import pyperclip

################################################################################
################################################################################
def updateClipboard():
    clippingText = pyperclip.paste() # get the text to be pasted
    processClipping(clippingText=clippingText) # process the clipping
    root.after(ms=100, func=updateClipboard) # check for new clippings after 100 ms

################################################################################
################################################################################
def processClipping(clippingText):
    cleanedClippingText = cleanClippingText(clippingText=clippingText) # clean clipping text
    label["text"] = cleanedClippingText # set label text to cleaned clipping text

################################################################################
################################################################################
def cleanClippingText(clippingText):
    cleanedClippingText = ""
    for character in clippingText: # only keep characters less than 65535 in Unicode (range for Tool Command Language (TCL))
        if (ord(character) <= 65535):
            cleanedClippingText = cleanedClippingText + character
             
    return cleanedClippingText

################################################################################
################################################################################
def onClick(labelElem):
    labelText = labelElem["text"] # get text of clicked label
    print(labelText) # print text to the screen
    pyperclip.copy(labelText) # copy label text

################################################################################
################################################################################
if __name__ == '__main__':
    root = Tk() # root element
    
    label = Label(root, text="", cursor="arrow", relief=RAISED, pady=5,  wraplength=500) # create label
    label.bind("<Button-1>", lambda event, labelElem=label: onClick(labelElem)) # bind label to click event
    label.pack() # display label in pack format
    
    updateClipboard() # updates clipboard infinitely until windows closes
    
    root.mainloop() # main application loop
    
    