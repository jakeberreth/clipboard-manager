################################################################################
##  Repository: clipboard-manager
##  Author:     Jake Berreth
##  Sources:    https://github.com/prashantgupta24/clipboard-manager
################################################################################
from tkinter import Tk, Label, RAISED
import pyperclip

class ClipboardManager():
    ################################################################################
    ################################################################################
    def __init__(self, root):
        self.root          = root
        self.labelList     = []
        self.labelTextList = []
        
    ################################################################################
    ################################################################################
    def appendLabelTextToLabelTextList(self, textValue):
        label = Label(
                    root, 
                    text=textValue, 
                    cursor="arrow", 
                    relief="raised", 
                    padx=20, 
                    pady=10, 
                    wraplength=500,
                    font=("Helvetica", 14),
                    background="#f5f5f5"
                )
        label.bind("<Button-1>", lambda event, labelElem=label: self.onClick(labelElem)) # bind label to click event
        label.pack(padx=20, pady=20) # display label in pack format
        
        self.labelTextList.append(label['text'])
        
        return label
        
    ################################################################################
    ################################################################################
    def updateClipboard(self):
        clippingText = pyperclip.paste() # get the text to be pasted
        self.processClipping(clippingText=clippingText) # process the clipping
        root.after(ms=100, func=self.updateClipboard) # check for new clippings after 100 ms


    ################################################################################
    ################################################################################
    def processClipping(self, clippingText):
        cleanedClippingText = self.cleanClippingText(clippingText=clippingText) # clean clipping text
        
        if cleanedClippingText not in self.labelTextList:
            self.appendLabelTextToLabelTextList(cleanedClippingText)

    ################################################################################
    ################################################################################
    def cleanClippingText(self, clippingText):
        cleanedClippingText = ""
        for character in clippingText: # only keep characters less than 65535 in Unicode (range for Tool Command Language (TCL))
            if (ord(character) <= 65535):
                cleanedClippingText = cleanedClippingText + character
                
        return cleanedClippingText
        
    ################################################################################
    ################################################################################
    def onClick(self, labelElem):
        labelText = labelElem["text"] # get text of clicked label
        print(labelText) # print text to the screen
        pyperclip.copy(labelText) # copy label text

################################################################################
################################################################################
if __name__ == '__main__':
    root = Tk() # root element
    root['bg'] = '#a9a9a9'
    
    clipboardManager = ClipboardManager(root)
    
    clipboardManager.updateClipboard() # updates clipboard infinitely until windows closes
    
    clipboardManager.root.mainloop() # main application loop
    
    