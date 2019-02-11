from tkinter import *
import cv2
from PIL import ImageTk, Image
trace = 0 
class CanvasEventsDemo: 
    def __init__(self, parent=None):
        root = Tk()
        image = Image.open("max.jpg")
        width,height =image.size
        photo = ImageTk.PhotoImage(image)  
        canvas = Canvas(width=width, height=height)
        background_label = Label(root, image=photo)
        background_label.image=photo
        canvas.pack()
        
        canvas.create_image(0, 0, image=photo, anchor=NW)
        canvas.bind('<ButtonPress-1>', self.onStart)  
        canvas.bind('<B1-Motion>',     self.onGrow)   
        canvas.bind('<Double-1>',      self.onClear)  
        canvas.bind('<ButtonPress-3>', self.onMove)   
        self.canvas = canvas
        self.drawn  = None
        

    def onStart(self, event):
        self.start = event
        self.drawn = None

    def onGrow(self, event):                          
        canvas = event.widget
        if self.drawn: canvas.delete(self.drawn)
        objectId = canvas.create_rectangle(self.start.x, self.start.y, event.x, event.y,outline='red',width=2)
        if trace: print( objectId)
        self.drawn = objectId

    def onClear(self, event):
        event.widget.delete('all')

    def onMove(self, event):
        if self.drawn:            
            if trace: print (self.drawn)
            canvas = event.widget
            diffX, diffY = (event.x - self.start.x), (event.y - self.start.y)
            canvas.move(self.drawn, diffX, diffY)
            self.start = event
     
CanvasEventsDemo()
mainloop()

