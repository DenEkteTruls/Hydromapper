import serial
from tkinter import *
  
root = Tk()
root.geometry("320x350")
root.title("Uploader")

def check_seral(a):
    try:
        global s
        s = serial.Serial(a.split(":")[0], int(a.split(":")[1]))
    except:
        Output.insert(INSERT, "\nCould not find MPU device!")
        return False
    Output.insert(INSERT, "\nMPU device found!")
    return True
  
def do_input():
    a = inputtxt.get("1.0", "end-1c")
    if check_seral(a):
        try:
            s.write(inputtxt.get("1.0", "end-1c"))
        except:
            Output.insert(INSERT, "Error during navigation upload\n\n")
            return False
        Output.insert(INSERT, "Successfully uploadere navigation data\n\n")
    else:
        return False

      
l = Label(text="Navigation data here ...")

comtxt = Text(root, height = 1, 
              width = 35, 
              bg = "light cyan")

inputtxt = Text(root, height = 10,
                width = 35,
                bg = "light yellow")
  
Output = Text(root, height = 5, 
              width = 35, 
              bg = "light cyan")
  
Display = Button(root, height = 2,
                 width = 30, 
                 text ="Upload",
                 command = lambda:do_input())
  
l.pack()
comtxt.pack()
inputtxt.pack()
Display.pack()
Output.pack()

mainloop()