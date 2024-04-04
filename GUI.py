import tkinter
from tkinter import *
from PIL import Image, ImageTk
root = Tk()
# Create a photoimage object of the image in the path
image1 = Image.open('/Users/pico/Desktop/ABE/Originals/P001.JPG')
test = ImageTk.PhotoImage(image1)
label1 = tkinter.Label(image=test)
label1.image = test
# Position image
label1.place()
root.mainloop()

