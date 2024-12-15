import tkinter as tk
from tkinter import filedialog as fd
import main
import os
from PIL import ImageTk, Image
from pathlib import Path

root = tk.Tk()
root.title('Automated Batch Editor')
root.geometry('800x300')

y_padding = 12
x_padding = 20

# ABE function selector
function_variable = tk.StringVar()

values = {'Compress Image' : 'compression',
          'Gaussian Blur' : 'gaussian_blur',
          'Add Watermark' : 'watermark'}

for (button_text, button_value) in values.items():
    tk.Radiobutton(root,
                   command = button_value,
                   text = button_text,
                   variable = function_variable,
                   value = button_value,
                   indicator = 0,
                   font = ('Arial', 10),
                   height = 2,
                   width = 14).grid(column = 0,
                   row = list(values).index(button_text) + 1,
                   padx = x_padding,
                   pady = y_padding)

# value entry
value_entry = {'compression' : 'COMPRESSION_VARIABLE',
               'gaussian_blur' : 'GAUSSIAN_BLUR_VARIABLE',
               'watermark' : 'WATERMARK_VARIABLE'}

for (entry, entry_variable) in value_entry.items():
    tk.Entry(root,
             textvariable = entry_variable).grid(row = list(value_entry).index(entry) + 1,
             column = 1,
             pady = y_padding,
             padx = x_padding)

# render or delete button
render_button = tk.Button(text = 'Render', command = fd.askopenfilename)
render_button.grid(row = 4, column = 0, pady = y_padding, padx = x_padding)
delete_button = tk.Button(text = 'Delete')
delete_button.grid(row = 4, column = 1, pady = y_padding, padx = x_padding)

execute_button = tk.Button(text = 'Execute')
execute_button.grid(row = 5, column = 0, columnspan = 2, sticky = 'EW', pady = y_padding, padx = x_padding)

# select and display image
select_image_variable = tk.StringVar()
imageee = tk.StringVar()
def update_select_image_variable():
    test = fd.askopenfilename()
    imageee.set(Path(test))
    processed_test = os.path.basename(test)
    select_image_variable.set(processed_test)
    
select_image_button = tk.Button(text = 'Select Image', command = update_select_image_variable)
select_image_button.grid(row = 0, column = 0)

select_image_label = tk.Label(root, textvariable = select_image_variable)
select_image_label.grid(row = 0, column = 1)

imagee = Image.open(imageee)
test = ImageTk.PhotoImage(imagee.resize((300,250)))
image_label = tk.Label(image = test).grid(row = 0, column = 2, rowspan = 5)



root.resizable(0, 0)
root.mainloop()

