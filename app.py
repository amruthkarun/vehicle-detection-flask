from tkinter import *
import cv2
from PIL import ImageTk, Image
import os
trace = 0 
root = Tk()
class CanvasEventsDemo: 
    def __init__(self, parent=None):
        self.objectId=0
        self.rectangles=[]
        image = Image.open("max.jpg")
        width,height =image.size
        photo = ImageTk.PhotoImage(image)  
        canvas = Canvas(width=width, height=height)
        background_label = Label(root, image=photo)
        background_label.image=photo

        b1 = Button(root,text="Reset",width=10,height=10, command=self.reset)
        b1.pack(side=LEFT,fill='both')
        canvas.pack()
        
        canvas.create_image(0, 0, image=photo, anchor=NW)
        canvas.bind('<ButtonPress-1>', self.onStart)  
        canvas.bind('<B1-Motion>',     self.onGrow)   
        canvas.bind('<ButtonRelease-1>', self.onMove)   
        self.canvas = canvas
        self.drawn  = None
       

    def onStart(self, event):
        self.start = event
        self.drawn = None
           

    def onGrow(self, event):                          
        canvas = event.widget
        if self.drawn: canvas.delete(self.drawn)
        self.objectId = canvas.create_rectangle(self.start.x, self.start.y, event.x, event.y,outline='red',width=2)
        if trace: print(self.objectId)
        self.drawn = self.objectId
        self.rectangles.append(self.drawn)  
          
    def reset(self):
         for item in self.rectangles:
           self.canvas.delete(item)
         if os.path.exists("out.txt"):
           os.remove("out.txt")         
    def onMove(self, event):
        if self.drawn:
            if trace: print (self.drawn)
            f=open("out.txt","a")
            f.write(str(self.start.x)+" "+str(self.start.y)+" "+str(event.x)+" "+str(event.y)+"\n")
            self.start = event
     
CanvasEventsDemo()
mainloop()

