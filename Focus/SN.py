import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog as sd

def do_askstring():
    str_input=sd.askstring("8L_num", "請輸SN")
    print(str_input)
    print("VCResult:{0}".format(str_input))

root=tk.Tk()
root.title("simpledialog")
do_askstring()
#ttk.Button(root, text="8L_num", command=do_askstring).pack()
#root.mainloop()
