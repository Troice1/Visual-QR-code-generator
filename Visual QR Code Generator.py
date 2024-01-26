from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap import Variable
from ttkbootstrap.dialogs import Messagebox
import time
import qrcode
import threading
from PIL import Image

import img

with open("./wz.png", 'wb') as f:
    f.write(img.ystp)

MainWindow = ttk.Window()
MainWindow.geometry('550x400')
MainWindow.title("Visual QR code generator")
MainWindow.resizable(False, False)
MainWindow.update()

style = ttk.Style(theme="darkly")

URLLabel = ttk.Label(MainWindow, text="URL:")
URLLabel.place(x=0, y=0)
URLLabel.update()
# URLLabel.place(x=MainWindow.winfo_width() / 2 - URLLabel.winfo_width(), y=10)
URLLabel.place(x=70, y=13)

UrlEntry_Context = Variable()
URLEntry = ttk.Entry(MainWindow, textvariable=UrlEntry_Context, width=45)
URLEntry.place(x=0, y=0)
URLEntry.update()
URLEntry.place(x=MainWindow.winfo_width() / 2 - URLEntry.winfo_width() / 2, y=10)

Image_Main = ttk.PhotoImage(file="./wz.png")
print(Image_Main)
Image_Main_Label = ttk.Label(MainWindow, image=Image_Main, width=10)
Image_Main_Label.place(x=0, y=0)
Image_Main_Label.update()
Image_Main_Label.place(x=MainWindow.winfo_width() / 2 - Image_Main_Label.winfo_width() / 2, y=50)

lock = threading.RLock()


def func():
    global Image_Main_Label, MainWindow
    while True:
        lock.acquire()
        time.sleep(1)
        print("update")
        Image_Main_ = ttk.PhotoImage(file="./wz.png")
        Image_Main_Label['image'] = Image_Main_
        lock.release()

detection = False
image_ = None
def Generate_Function():
    global detection, image_
    global UrlEntry_Context, MainWindow
    if str(UrlEntry_Context.get()).replace(' ', '') == "":
        Messagebox.show_info(title="title", message="Prohibit input of blank content")
        return None
    image_file = qrcode.make(str(UrlEntry_Context.get()))
    image_ = image_file
    with open("./wz.png", "wb") as filepath:
        image_file.save(filepath)
        f_in = './wz.png'
        img = Image.open(f_in)
        print(img.size)
        out = img.resize((300, 300))
        fout = './wz.png'
        out.save(fout, 'png')
    detection = True


Button_Get = ttk.Button(MainWindow, text="Generate", bootstyle=("INFO", "OUTLINE"), command=Generate_Function)
Button_Get.place(x=0, y=0)
Button_Get.update()
Button_Get.place(x=MainWindow.winfo_width() / 2 - Button_Get.winfo_width() / 2 + URLEntry.winfo_width() / 2 + 50, y=10)

threading.Thread(target=func).start()


def Save_func():
    global detection, image_
    if detection:
        filepath_save = filedialog.askdirectory()
        print(filepath_save)
        with open(str(filepath_save) + "\image.png", 'wb') as fp:
            image_.save(fp)
        Messagebox.show_info(title="title", message=f"Path:{str(filepath_save)}/image.png")
    else:
        Messagebox.show_info(title="title", message="Please generate a QR code")



Save_Button = ttk.Button(MainWindow, text="Save", command=Save_func, bootstyle=("INFO", "OUTLINE"), width=10)
Save_Button.place(x=0, y=0)
Save_Button.update()
Save_Button.place(x=MainWindow.winfo_width() / 2 - Save_Button.winfo_width() / 2, y=360)

MainWindow.mainloop()
