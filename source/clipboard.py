################################################################################
##  Repository: clipboard-manager
##  Author:     Jake Berreth
##  Sources:    https://github.com/prashantgupta24/clipboard-manager
################################################################################
from tkinter import Tk, Label, Button, Menu
import pyperclip

class ClipboardManager():
    ################################################################################
    ################################################################################
    def __init__(self, root):
        self.root          = root
        self.root.title('Clipboard Manager')
        self.root['bg'] = '#638889'
        self.root.minsize(290, 400)
        self.root.maxsize(290, 400)
        root.wm_attributes("-topmost", 1)
        root.resizable(False, False)
        
        self.labelList     = []
        self.labelTextList = []
        
        self.createMenu()
        
        self.forgottenLabel   = None
        self.clearedClippings = False
        
        self.shortenedTextToTrueText = {}
        self.maxDisplayTextLength    = 100
        
        
    ################################################################################
    ################################################################################
    def appendLabelToLabelList(self, textValue):
        label = Button(
                    root, 
                    text=textValue, 
                    cursor="arrow", 
                    relief="raised", 
                    padx=20, 
                    pady=10, 
                    wraplength=300,
                    width=38,
                    font=("Helvetica", 8),
                    background='#ECE3CE'
                )
        label.bind("<Button-1>", lambda event, labelElem=label: self.onLeftClick(labelElem)) # bind label to left click event
        label.bind("<Button-3>", lambda event, labelElem=label: self.onRightClick(labelElem)) # bind label to right click event
        
        self.labelList.append(label)
        
        if (label == self.labelList[len(self.labelList) - 1]):
            label.pack(pady=(10, 0)) # display label in pack format
        else:
            label.pack(pady=(10, 10))
        
        
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
                
        shortenedClippingText = ""
        if (len(cleanedClippingText) > 0):
            shortenedClippingText = cleanedClippingText
            self.shortenedTextToTrueText[shortenedClippingText] = cleanedClippingText
            
            if (len(cleanedClippingText) > self.maxDisplayTextLength):
                tempCleanedClipping = cleanedClippingText
                shortenedClippingText = cleanedClippingText[:self.maxDisplayTextLength] + "..."
                self.shortenedTextToTrueText[shortenedClippingText] = tempCleanedClipping
                
            for label in self.labelList:
                if (label):
                    if (label["text"] == shortenedClippingText):
                        return
            
            self.appendLabelToLabelList(shortenedClippingText)
            

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
    def onLeftClick(self, labelElem):
        labelText = self.shortenedTextToTrueText[labelElem["text"]] # get text of clicked label
        print(labelText) # print text to the screen
        pyperclip.copy(labelText) # copy label text
 
    ################################################################################
    ################################################################################
    def onRightClick(self, labelElem):
        labelText = labelElem["text"] # get text of clicked label
        
        for label in self.labelList:
            if (label["text"] == labelText):
                label.pack_forget()
                self.forgottenLabel = label
 
 
    ################################################################################
    ################################################################################     
    def clearAllClippings(self):
        for label in self.labelList:
            label.pack_forget()
            self.clearedClippings = True
            
            
    ################################################################################
    ################################################################################     
    def undo(self):
        if (self.forgottenLabel is not None):
            self.forgottenLabel.pack(pady=(10, 0))
            self.forgottenLabel = None
            self.clearedClippings = False
            return
        
        if (self.clearedClippings):
            for label in self.labelList:
                label.pack(pady=(10, 0))
                self.clearedClippings = False
                self.forgottenLabel = None
                        
            
    ################################################################################
    ################################################################################      
    def createMenu(self):
        self.menubar = Menu(root)
        self.root.config(menu=self.menubar)
        self.menubar.add_command(label="Clear All", command=self.clearAllClippings)
        self.menubar.add_command(label="Undo", command=self.undo)


################################################################################
################################################################################
if __name__ == '__main__':
    root = Tk() # root element
    
    clipboardManager = ClipboardManager(root)
    
    clipboardManager.updateClipboard() # updates clipboard infinitely until windows closes
    
    clipboardManager.root.mainloop() # main application loop
    
    