################################################################################
##  Repository: clipboard-manager
##  Author:     Jake Berreth
##  Sources:    https://github.com/prashantgupta24/clipboard-manager
################################################################################
from tkinter import Tk, Label, Menu
import pyperclip

class ClipboardManager():
    ################################################################################
    ################################################################################
    def __init__(self, root):
        self.root          = root
        self.root.title('Clipboard Manager')
        self.root['bg'] = '#a9a9a9'
        self.root.minsize(300, 100)
        
        self.labelList     = []
        self.labelTextList = []
        
        self.createMenu()
        
        
    ################################################################################
    ################################################################################
    def appendLabelToLabelList(self, textValue):
        label = Label(
                    root, 
                    text=textValue, 
                    cursor="arrow", 
                    relief="raised", 
                    padx=20, 
                    pady=10, 
                    wraplength=500,
                    font=("Helvetica", 14),
                    background="#f5f5f5",
                    borderwidth=2
                )
        label.bind("<Button-1>", lambda event, labelElem=label: self.onClick(labelElem)) # bind label to click event
        label.pack(padx=20, pady=20) # display label in pack format
        
        self.labelList.insert(0, label)
        
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
        
        for label in self.labelList:
            if (label):
                if (label["text"] == cleanedClippingText):
                    return
                
        if (len(cleanedClippingText) > 0):
            self.appendLabelToLabelList(cleanedClippingText)


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
    def clearAllClippings(self):
        for label in self.labelList:
            label.pack_forget()
            
            
    ################################################################################
    ################################################################################      
    def createMenu(self):
        self.menubar = Menu(root)
        self.root.config(menu=self.menubar)
        self.menubar.add_command(label="Clear All", command=self.clearAllClippings)
        # menubar.add_cascade(label="Options", menu=optionsMenu)
        #self.parent.config(menu=menubar)


################################################################################
################################################################################
if __name__ == '__main__':
    root = Tk() # root element
    
    clipboardManager = ClipboardManager(root)
    
    clipboardManager.updateClipboard() # updates clipboard infinitely until windows closes
    
    clipboardManager.root.mainloop() # main application loop
    
    