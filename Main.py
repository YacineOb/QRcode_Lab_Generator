""" Idea for future updates:
- add pref based on external file? e.g. default values, pdf, excel, color..."""

import os
import threading
import time
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Label, StringVar, messagebox, Menu, Frame, RAISED, \
    Checkbutton, IntVar, FLAT, Listbox, ttk, filedialog, END, Toplevel, X
from tkinter.ttk import Panedwindow
from PIL import ImageTk, Image
import math
from LabelMaker import generateQR, InputCheckpoint
from Tool import ToolTip, CreateToolTip

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def Input_format(entry):
    try:
        int(entry.get())
    except:
        if entry.get().replace(' ', '') == '':
            pass
        else:
            labelerror = Label(window, text='Number of slides is not a number. Please only use integers.',
                               bg='#fff', fg='#f00')
            canvas.create_window(895, 412, window=labelerror, tag='integersonly')
    else:
        if int(entry.get()) == 0:
            labelnull = Label(window, text='0 is not a correct value for "Number of slide".', bg='#fff', fg='#f00')
            canvas.create_window(895, 412, window=labelnull, tag='nullerror')
        else:
            pass


def Processing():
    global image_X, label2

    canvas.delete('integers only')
    canvas.delete("Success")
    canvas.delete("QR")
    image_X = PhotoImage(file=relative_to_assets("image_1p.png"))
    canvas.create_image(258.0, 262.0, image=image_X, tags="Processing")
    window.update()


sequencememory = 0


def Insert_image(entry_list, col, path):
    global entry_image_X, label1, QR, timestr, sequence, sequencememory

    canvas.delete('integersonly')
    canvas.delete('nullerror')
    Input_format(entry_list[9])
    timestr = Get_time()

    entry_len = [len(x.get()) for x in entry_list]
    input_raw = [str(x.get()) for x in entry_list]
    input_overview = [input_raw[x].replace(" ", "") for x in range(0, len(input_raw))]
    element = all(element == input_overview[0] for element in input_overview)

    if sum(entry_len) != 0 and element == False:
        info = InputCheckpoint(entry_12.get(), entry_3.get(), entry_2.get(), entry_13.get(), entry_5.get(),
                               entry_6.get(), entry_4.get(), entry_9.get(), entry_7.get(), entry_8.get(),
                               entry_11.get(),
                               entry_10.get(), entry_14.get(), entry_15.get(), entry_16.get(), entry_17.get(),
                               entry_18.get(), entry_19.get(), entry_20.get())  # The order is wrong

        canvas.delete("warning")

        # Path manipulation
        if cb_var2.get() == 1:
            path = path + '/Label_individual/'
        else:
            path = path + '/Labels/' + timestr

        # individual mode memory features
        if cb_var2.get() == 0:
            sequence = ''
        elif cb_var2.get() == 1:
            sequence = 1
            sequencememory += sequence

        # generate QR codes
        QR, data = generateQR(info, timestr, Version, str(col), path,
                              excel_activate.get(), sequencememory, cb_var2.get())

        # Display the last QR-Code
        entry_image_X = ImageTk.PhotoImage(QR)
        canvas.create_image(258.0, 262.0, image=entry_image_X, tags="QR")

        # message to confirm generation of labels
        label_2 = Label(window, text='Labels generated with success. View labels.', bg='#fff', fg='#18b576',
                        cursor="hand2")
        label_2.bind("<Button-1>", lambda e: os.startfile(path + '\\'))
        canvas.create_window(895, 412, window=label_2, tag='Success')


    elif element:
        canvas.delete("QR")
        canvas.delete("Success")
        canvas.delete("Processing")
        label_1 = Label(window, text='Fill at least one entry to generate a QR-Code', bg='#fff', fg='#f00')
        canvas.create_window(895, 412, window=label_1, tag='warning')
        pass


def makepdf(path, activate=0, individual_mode=0):
    if individual_mode == 1:
        path = path + '/Label_individual/'
    else:
        path = path + '/Labels/' + timestr

    if activate == 1:
        imgs = []
        path_pdf = path
        valid_images = [".jpg", ".gif", ".png", ".tga"]
        for f in sorted(os.listdir(path_pdf), key=lambda x: x[9:]):
            ext = os.path.splitext(f)[1]
            if ext.lower() not in valid_images:
                continue
            imgs.append(Image.open(os.path.join(path_pdf, f)))

        height_page = 3508 * 2
        width_page = 2480 * 2
        h = 130 * 2
        w = 270 * 2
        n = 0
        position = 0
        max_label_page = 243

        pdffile = 0
        page_total = int(math.ceil(len(imgs) / max_label_page))
        total_pages = range(0, page_total, 1)
        flyer = [0] * page_total

        for pages in total_pages:
            flyer[pages] = Image.new('RGB', (width_page, height_page), color='#FFFFFF')

        pages = 0
        for pic in imgs:
            pic = pic.resize((w, h), Image.ANTIALIAS)
            flyer[pages].paste(pic, (n, position))
            position += h

            if position >= height_page:
                position = 0
                n += w
            if n > (8 * w):
                pages += 1
                n = 0

        flyer[0].save(path_pdf + '/' + 'PDFCompositeLabel_' + '.pdf',
                      save_all=True, append_images=flyer[1:], dpi=(300, 300))
    else:
        pass


def TempText(entry, default):
    def on_entry_click(event):
        if entry.cget('fg') == '#CBCACA':
            entry.delete(0, "end")  # delete all the text in the entry
            entry.insert(0, '')  # Insert blank for user input
            entry.config(fg='black')

    def on_focusout(event):
        if entry.get() == '':
            entry.config(fg='#CBCACA')
            entry.insert(0, default)

    entry.insert(0, default)
    entry.bind('<FocusIn>', on_entry_click)
    entry.bind('<FocusOut>', on_focusout)
    entry.config(fg='#CBCACA')


def Get_time():
    timestring = time.strftime("%H-%M-%S_%d.%m.%y")
    return timestring


# Version and time definition
Version = 'v0.590422'
date = Get_time()

# Main window built
window = Tk()
window.geometry("1263x525")
window.iconbitmap(relative_to_assets("logoQR.ico"))
window.title('QR-Code Lab Generator by Yacine B.' + Version)
window.configure(bg="#FFFFFF")

style = ttk.Style()
style.configure("BW.TLabel", background="#FFFFFF")
frame1 = Panedwindow(window, height=200, width=1263, style='BW.TLabel')
frame1.pack(fill='both', expand=True)
separator = ttk.Separator(window, orient='horizontal')
separator.place(x=0, y=527, width=1263)

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=525,
    width=1263,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    786.5,
    126.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#F0F5FA",
    highlightthickness=0,
    font=('calibri', 25, 'normal'),
    textvariable=StringVar()
)

entry_1.place(
    x=583.0,
    y=106.0 + 20,
    width=407.0,
    height=19.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    676.0,
    209.5,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#F0F5FA",
    highlightthickness=0,
    font=('calibri', 16, 'normal'),
    textvariable=StringVar()
)
entry_2.place(
    x=583.0,
    y=182.0 + 20,
    width=186.0,
    height=33.0
)

TempText(entry_2, "Immunohistochemistry")

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    1120.0,
    134.5,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#F0F5FA",
    highlightthickness=0,
    font=('calibri', 16, 'normal'),
    textvariable=StringVar()
)
entry_3.place(
    x=1029.0,
    y=108.0 + 20,
    width=182.0,
    height=31.0
)
TempText(entry_3, date[9:])
threading.Thread(target=CreateToolTip(entry_3, text="Default value is today's date.")).start()

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    676.0,
    285.5,
    image=entry_image_4
)
entry_4 = Entry(
    bd=0,
    bg="#F0F5FA",
    highlightthickness=0,
    font=('calibri', 16, 'normal'),
    textvariable=StringVar()
)
entry_4.place(  # This entry is not responding correclty when this is the only value entered
    x=583.0,
    y=258.0 + 20,
    width=186.0,
    height=33.0
)
TempText(entry_4, "C57BL/6jCrl")

entry_image_5 = PhotoImage(
    file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(
    1067.5,
    209.5,
    image=entry_image_5
)
entry_5 = Entry(
    bd=0,
    bg="#F0F5FA",
    highlightthickness=0,
    font=('calibri', 16, 'normal'),
    textvariable=StringVar()
)
entry_5.place(
    x=1029.0,
    y=182.0 + 20,
    width=77.0,
    height=33.0
)

threading.Thread(target=CreateToolTip(entry_5, text="Leave empty if you don't use. "
                                                    "\nTips: Add the wavelenght for each target"
                                                    "\ne.g. Calbindin (647 nm)")).start()

entry_image_6 = PhotoImage(
    file=relative_to_assets("entry_6.png"))
entry_bg_6 = canvas.create_image(
    1172.5,
    209.5,
    image=entry_image_6
)
entry_6 = Entry(
    bd=0,
    bg="#F0F5FA",
    highlightthickness=0,
    font=('calibri', 16, 'normal'),
    textvariable=StringVar()
)
entry_6.place(
    x=1134.0,
    y=182.0 + 20,
    width=77.0,
    height=33.0
)

threading.Thread(target=CreateToolTip(entry_6, text="Leave empty if you don't use. "
                                                    "\nTips: Add the wavelenght for each target"
                                                    "\ne.g. Calbindin (647 nm)")).start()

entry_image_7 = PhotoImage(
    file=relative_to_assets("entry_7.png"))
entry_bg_7 = canvas.create_image(
    1067.5,
    285.5,
    image=entry_image_7
)
entry_7 = Entry(
    bd=0,
    bg="#F0F5FA",
    highlightthickness=0,
    font=('calibri', 16, 'normal'),
    textvariable=StringVar()
)
entry_7.place(
    x=1029.0,
    y=258.0 + 20,
    width=77.0,
    height=33.0
)
threading.Thread(target=CreateToolTip(entry_7, text="Leave empty if you don't use. "
                                                    "\nTips: Add the wavelenght for each target"
                                                    "\ne.g. Calbindin (647 nm)")).start()
entry_image_8 = PhotoImage(
    file=relative_to_assets("entry_8.png"))
entry_bg_8 = canvas.create_image(
    1170.5,
    285.5,
    image=entry_image_8
)
entry_8 = Entry(
    bd=0,
    bg="#F0F5FA",
    highlightthickness=0,
    font=('calibri', 16, 'normal'),
    textvariable=StringVar()
)
entry_8.place(
    x=1132.0,
    y=258.0 + 20,
    width=77.0,
    height=33.0
)
threading.Thread(target=CreateToolTip(entry_8, text="Leave empty if you don't use. "
                                                    "\nTips: Add the wavelenght for each target"
                                                    "\ne.g. Calbindin (647 nm)")).start()

entry_image_9 = PhotoImage(
    file=relative_to_assets("entry_9.png"))
entry_bg_9 = canvas.create_image(
    897.5,
    285.5,
    image=entry_image_9
)
entry_9 = Entry(
    bd=0,
    bg="#F0F5FA",
    highlightthickness=0,
    font=('calibri', 16, 'normal'),
    textvariable=StringVar()
)
entry_9.place(
    x=805.0,
    y=258.0 + 20,
    width=185.0,
    height=33.0
)
TempText(entry_9, "Wild-Type")

entry_image_10 = PhotoImage(
    file=relative_to_assets("entry_10.png"))
entry_bg_10 = canvas.create_image(
    1119.0,
    365.5,
    image=entry_image_10
)
entry_10 = Entry(
    bd=0,
    bg="#F0F5FA",
    highlightthickness=0,
    font=('calibri', 16, 'normal'),
    textvariable=StringVar()
)
entry_10.place(
    x=1029.0,
    y=334.0 + 20,
    width=180.0,
    height=41.0
)
threading.Thread(target=CreateToolTip(entry_10, text="Enter the number of label you need."
                                                     "\nAll parameters will be the same for all labels except "
                                                     "for the Internal ID")).start()

entry_image_11 = PhotoImage(
    file=relative_to_assets("entry_11.png"))
entry_bg_11 = canvas.create_image(
    897.5,
    365.5,
    image=entry_image_11
)
entry_11 = Entry(
    bd=0,
    bg="#F0F5FA",
    highlightthickness=0,
    font=('calibri', 16, 'normal'),
    textvariable=StringVar()
)
entry_11.place(
    x=805.0,
    y=334.0 + 20,
    width=185.0,
    height=41.0
)

threading.Thread(target=CreateToolTip(entry_11, text="Enter Cell ID if you have one. "
                                                     "\nBest use for individual cells (see individual mode)"
                                                     "\nIf you don't have any, leave blank and "
                                                     "refer to auto-generated internal ID")).start()

entry_image_12 = PhotoImage(
    file=relative_to_assets("entry_12.png"))
entry_bg_12 = canvas.create_image(
    786.5,
    133.5,
    image=entry_image_12
)
entry_12 = Entry(
    bd=0,
    bg="#F0F5FA",
    highlightthickness=0,
    font=('calibri', 16, 'normal'),
    textvariable=StringVar()
)
entry_12.place(
    x=583.0,
    y=106.0 + 20,
    width=407.0,
    height=33.0
)
TempText(entry_12, "Yacine B.")
threading.Thread(target=CreateToolTip(entry_12, text="Please enter the name of the experimenter.")).start()

entry_image_13 = PhotoImage(
    file=relative_to_assets("entry_13.png"))
entry_bg_13 = canvas.create_image(
    897.5,
    209.5,
    image=entry_image_13
)
entry_13 = Entry(
    bd=0,
    bg="#F0F5FA",
    highlightthickness=0,
    font=('calibri', 16, 'normal')
)
entry_13.place(
    x=805.0,
    y=182.0 + 20,
    width=185.0,
    height=33.0
)
threading.Thread(target=CreateToolTip(entry_13, text="50 micrometers is the default value. "
                                                     "default unit is micrometer")).start()
canvas.create_text(
    805.0,
    182.0,
    anchor="nw",
    text="Thickness (\u03BCm)",
    fill="#143B69",
    font=("Arial Bold", 15 * -1)
)

TempText(entry_13, "50")

# advanced mode entries #####################################################

entry_image_14 = PhotoImage(
    file=relative_to_assets("entry_14.png"))

entry_bg_14 = Label(frame1, image=entry_image_14, borderwidth=0, bg="White")
entry_bg_14.place(x=580, y=33)

entry_14 = Entry(
    bd="0",
    bg="#F0F5FA",
    highlightthickness=0,
    font=('calibri', 16, 'normal'),
    textvariable=StringVar(),
)

entry_14.place(
    x=585.0,
    y=580,
    width=186.0,
    height=33.0
)

label14 = Label(
    frame1,
    font="Arial 11",
    foreground="#143B69", bg="#F0F5FA", text="Birthday (dd.mm.yy)")
label14.place(x=585, y=35)

# entry 15 #####################################################

entry_image_15 = PhotoImage(
    file=relative_to_assets("entry_15.png"))

entry_bg_15 = Label(frame1, image=entry_image_15, borderwidth=0, bg="White")
entry_bg_15.place(x=802, y=33)

entry_15 = Entry(
    bd=0,
    bg="#F0F5FA",
    highlightthickness=0,
    font=('calibri', 16, 'normal'),
    textvariable=StringVar()
)
entry_15.place(
    x=809,
    y=580,
    width=186.0,
    height=33.0
)

label15 = Label(
    frame1,
    font="Arial 11",
    foreground="#143B69", bg="#F0F5FA", text="Slice type")
label15.place(x=809, y=35)

TempText(entry_15, "Horizontal")

# entry 16 #####################################################

entry_image_16 = PhotoImage(
    file=relative_to_assets("entry_16.png"))

entry_bg_16 = Label(frame1, image=entry_image_16, borderwidth=0, bg="White")
entry_bg_16.place(x=1026, y=33)

entry_16 = Entry(
    bd=0,
    bg="#F0F5FA",
    highlightthickness=0,
    font=('calibri', 16, 'normal'),
    textvariable=StringVar()
)
entry_16.place(
    x=1033.0,
    y=580,
    width=186.0,
    height=33.0
)

label16 = Label(
    frame1,
    font="Arial 11",
    foreground="#143B69", bg="#F0F5FA", text="Mounting medium")
label16.place(x=1033, y=35)

TempText(entry_16, "Mowiol")

# entry 17 #####################################################

entry_image_17 = PhotoImage(
    file=relative_to_assets("entry_17.png"))

entry_bg_17 = Label(frame1, image=entry_image_17, borderwidth=0, bg="White")
entry_bg_17.place(x=1026, y=113)

entry_17 = Entry(
    bd=0,
    bg="#F0F5FA",
    highlightthickness=0,
    font=('calibri', 16, 'normal'),
    textvariable=StringVar()
)
entry_17.place(
    x=1033.0,
    y=660,
    width=66.0,
    height=33.0
)

label17 = Label(
    frame1,
    font="Arial 11",
    foreground="#143B69", bg="#F0F5FA", text="Target 5")
label17.place(x=1031, y=115)

threading.Thread(target=CreateToolTip(entry_17, text="Leave empty if you don't use. "
                                                     "\nTips: Add the wavelenght for each target"
                                                     "\ne.g. Calbindin (647 nm)")).start()

# entry 18 #####################################################

entry_image_18 = PhotoImage(
    file=relative_to_assets("entry_18.png"))

entry_bg_18 = Label(frame1, image=entry_image_18, borderwidth=0, bg="White")
entry_bg_18.place(x=1133, y=113)

entry_18 = Entry(
    bd=0,
    bg="#F0F5FA",
    highlightthickness=0,
    font=('calibri', 16, 'normal'),
    textvariable=StringVar()
)
entry_18.place(
    x=1135.0,
    y=660,
    width=66.0,
    height=33.0
)

label18 = Label(
    frame1,
    font="Arial 11",
    foreground="#143B69", bg="#F0F5FA", text="Target 6")
label18.place(x=1135, y=115)

threading.Thread(target=CreateToolTip(entry_18, text="Leave empty if you don't use. "
                                                     "\nTips: Add the wavelenght for each target"
                                                     "\ne.g. Calbindin (647 nm)")).start()
# entry 19   #####################################################

entry_image_19 = PhotoImage(
    file=relative_to_assets("entry_19.png"))

entry_bg_19 = Label(frame1, image=entry_image_19, borderwidth=0, bg="White")
entry_bg_19.place(x=580, y=113)

entry_19 = Entry(
    bd=0,
    bg="#F0F5FA",
    highlightthickness=0,
    font=('calibri', 16, 'normal'),
    textvariable=StringVar()
)
entry_19.place(
    x=582.0,
    y=660,
    width=400.0,
    height=33.0
)

label19 = Label(
    frame1,
    font="Arial 11",
    foreground="#143B69", bg="#F0F5FA", text="Comment")
label19.place(x=582, y=115)

threading.Thread(target=CreateToolTip(entry_19, text="Feel free to add any information you might consider useful. "
                                                     "\nEverything written there will be available in the QR-code")
                 ).start()

# entry 20: Animal ID #####################################################

entry_image_20 = PhotoImage(
    file=relative_to_assets("entry_20.png"))

entry_bg_20 = Label(window, image=entry_image_20, borderwidth=0, bg="White")
entry_bg_20.place(x=580, y=335)

entry_20 = Entry(
    bd=0,
    bg="#F0F5FA",
    highlightthickness=0,
    font=('calibri', 16, 'normal'),
    textvariable=StringVar()
)
entry_20.place(
    x=583.0,
    y=334 + 20,
    width=185.0,
    height=33.0
)

label20 = Label(
    window,
    font="Arial 11",
    foreground="#143B69", bg="#F0F5FA", text="Animal ID")
label20.place(x=584, y=336)

# Entries summary ######################

entry_list = [entry_1, entry_2, entry_3, entry_4, entry_5, entry_6,
              entry_7, entry_8, entry_9, entry_10, entry_11, entry_12,
              entry_13, entry_14, entry_15, entry_16, entry_17, entry_18, entry_19
              ]

background = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    262.0 + 73,
    262.0,
    image=background,
    tag="defaultskinbase"
)

canvas.create_text(
    585.0,
    105.0,
    anchor="nw",
    text="Experimenter",
    fill="#143B69",
    font=("Arial Bold", 15 * -1)
)

canvas.create_text(
    808.0,
    336.0,
    anchor="nw",
    text="Cell ID",
    fill="#143B69",
    font=("Arial Bold", 15 * -1)
)

canvas.create_text(
    584.0,
    336.0,
    anchor="nw",
    text="Animal ID",
    fill="#143B69",
    font=("Arial Bold", 15 * -1)
)

canvas.create_text(
    1030.0,
    106.0,
    anchor="nw",
    text="Date",
    fill="#143B69",
    font=("Arial Bold", 15 * -1)
)

canvas.create_text(
    585.0,
    182.0,
    anchor="nw",
    text="Experiment",
    fill="#143B69",
    font=("Arial Bold", 15 * -1)
)

canvas.create_text(
    1031.0,
    334.0,
    anchor="nw",
    text="No Slides",
    fill="#143B69",
    font=("Arial Bold", 15 * -1)
)

canvas.create_text(
    585.0,
    260.0,
    anchor="nw",
    text="Animal",
    fill="#143B69",
    font=("Arial Bold", 15 * -1)
)

canvas.create_text(
    808.0,
    260.0,
    anchor="nw",
    text="Model",
    fill="#143B69",
    font=("Arial Bold", 15 * -1)
)

canvas.create_text(
    1031.0,
    185.0,
    anchor="nw",
    text="Target 1",
    fill="#143B69",
    font=("Arial Bold", 15 * -1)
)

canvas.create_text(
    1135.0,
    185.0,
    anchor="nw",
    text="Target 2",
    fill="#143B69",
    font=("Arial Bold", 15 * -1)
)

canvas.create_text(
    1030.0,
    261.0,
    anchor="nw",
    text="Target 3",
    fill="#143B69",
    font=("Arial Bold", 15 * -1)
)

canvas.create_text(
    1132.0,
    261.0,
    anchor="nw",
    text="Target 4",
    fill="#143B69",
    font=("Arial Bold", 15 * -1)
)

canvas.create_text(
    687.0,
    26.0,
    anchor="nw",
    text="QR-Code LAB Generator",
    fill="#000000",
    font=("Arial Bold", 45 * -1)
)

canvas.create_text(
    687.0,
    26.0 + 45,
    anchor="nw",
    text="                                                                                             "
         "by Yacine B.   " + Version,
    fill="#000000",
    font=("Arial Italic", 13 * -1)
)

canvas.create_rectangle(
    779.0,
    471.0,
    1011.0,
    515.0,
    fill="#000000",
    outline="")


def change(e):
    button_image_1 = PhotoImage(file=relative_to_assets("button_1ov.png"))
    button_1.config(image=button_image_1)
    button_1.image = button_image_1


def changeback(e):
    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1.config(image=button_image_1)
    button_1.image = button_image_1


button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))

button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: [Processing(), Insert_image(entry_list, selected_color.get(), entry_output_path.get()),
                     makepdf(entry_output_path.get(), pdf_activate.get(), cb_var2.get())],
    relief="flat",
    highlightcolor="#ffffff"
)

button_1.bind("<Enter>", change)
button_1.bind("<Leave>", changeback)

button_1.place(
    x=779.0,
    y=470.95184326171875,
    width=232.0296630859375,
    height=44.04815673828125
)

canvas.create_text(
    604.0 + 85,
    412.0,
    anchor="nw",
    text="\nThis code is meant to help you organize your slides during and after your experiments.\n"
         "          an ID will be automatically attributed to each slide for inventory purposes.\n"
         "                       Your labels will be created in a 'labels' file on your Desktop",
    fill="#000000",
    font=("Inter ExtraLight", 10 * -1)
)


# Additional labels on second frame

def frame1_disp():
    if cb_var1.get():
        frame1.place(x=0, y=525)
        window.geometry("1263x725")
    else:
        frame1.place_forget()
        window.geometry("1263x525")


on_image = PhotoImage(file=relative_to_assets("on1.png"))
off_image = PhotoImage(file=relative_to_assets("off1.png"))
cb_var1 = IntVar()
c1 = Checkbutton(window, image=off_image, selectimage=on_image, text="Advanced mode", indicatoron=False,
                 variable=cb_var1, command=frame1_disp, bg="white", selectcolor="#ffffff", offrelief=FLAT,
                 highlightthickness=0, bd=0)
c1.pack()
c1.place(
    x=580,
    y=485,
)

canvas.create_text(
    640,
    492,
    anchor="nw",
    text="Advanced mode",
    fill="#143B69",
    font=("Arial Bold", 11 * -1)
)

option_image = PhotoImage(file=relative_to_assets("option.png"))
option_frame = Label(frame1, image=option_image, borderwidth=0, bg="White")
option_frame.place(x=0, y=5)

# Option menu ##################################################################

entry_output_path = Entry(
    bd=0,
    bg="#F0F5FA",
    highlightthickness=0,
    font=('calibri', 12, 'normal'),
    textvariable=StringVar()
)

entry_output_path.place(
    x=23.0,
    y=601,
    width=350.0,
    height=25.0
)

TempText(entry_output_path, os.path.expanduser("~\\Desktop"))


def browse_func():
    entry_output_path.delete(0, END)
    filename = filedialog.askdirectory()
    entry_output_path.config(fg='black')
    entry_output_path.insert(END, filename)


path_button = Button(window, text="Browse", font=10, borderwidth=0, relief="flat", bg='#DDDDDD',
                     activebackground='#2d6de9', activeforeground='white', command=browse_func)
path_button.place(x=385.0, y=601, width=100.0, height=25.0)

# excel sheet
excel_activate = IntVar()
c2 = Checkbutton(frame1, text="Create excel workbook", indicatoron=True,
                 bg='#3e94f9', activebackground='#2d6de9', offrelief=FLAT, bd=0, variable=excel_activate)
c2.pack()
c2.place(
    x=23,
    y=150,
)

# Create PDF to print
pdf_activate = IntVar()
c3 = Checkbutton(frame1, text="Create PDF file", indicatoron=True, bg='#3e94f9',
                 activebackground='#2d6de9', offrelief=FLAT, highlightthickness=0, bd=0, variable=pdf_activate)
c3.pack()
c3.place(
    x=200,
    y=150)

# Choose color of QR-code via a combobox
selected_color = StringVar()
color_cb = ttk.Combobox(frame1, textvariable=selected_color)

color_cb['values'] = ['black', 'gray', 'blue', 'cyan', 'purple', 'green',
                      'yellow', 'red', 'orange', 'magenta']
color_cb.current(0)

# prevent typing a value
color_cb['state'] = 'readonly'

# place the widget
color_cb.place(x=340, y=150, )
color_cb.bind('<<ComboboxSelected>>')

color_set = Label(
    frame1,
    font="Arial 8",
    foreground="#143B69", bg="#3e94f9", text="Choose QR-code color")
color_set.place(x=340, y=130)


# Ind and Group mode
def change2(e):
    group_image = PhotoImage(file=relative_to_assets("ind.png"))
    c2.config(image=group_image)
    c2.image = group_image


def changeback2(e):
    bgroup_image = PhotoImage(file=relative_to_assets("Group.png"))
    c2.config(image=bgroup_image)
    c2.image = bgroup_image


def individual():
    global entry_10
    if cb_var2.get() == 1:
        entry_10.delete(0, END)
        TempText(entry_10, '1')
        entry_10.config(state="disabled")
        window.update()
    elif cb_var2.get() == 0:
        entry_10.config(state="normal")
        entry_10.delete(0, END)
        entry_10.update()


group_image = PhotoImage(file=relative_to_assets("Group.png"))
ind_image = PhotoImage(file=relative_to_assets("over.png"))
cb_var2 = IntVar()
c2 = Checkbutton(frame1, image=group_image, selectimage=ind_image, indicatoron=False,
                 variable=cb_var2, command=individual, highlightthickness=0, bd=0, bg="#3e94f9", selectcolor="#3e94f9",
                 activebackground="#3e94f9", overrelief="flat")
c2.pack()
c2.place(
    x=385,
    y=15,
)

c2.bind("<Enter>", change2)
c2.bind("<Leave>", changeback2)

# Bottom comment about more place #####################
final_comment = Label(
    frame1,
    font="Arial 8",
    foreground="#143B69", bg="white", text="More space is available in the comment entry. "
                                           "Future updates might include new entries.                "
                                           "Yacine B. Soft 2022")
final_comment.place(x=680, y=180)


# Menu ###############################################################################################
def about():
    messagebox.showinfo('About', 'QR-code Lab generator - Ya-soft 2022 - Version: ' + Version
                        + '\nFor updates please visit: https://github.com/YacineOb')


def howto():
    howto_window = Toplevel(window)  # Toplevel object which will be treated as a new window
    howto_window.title("QR-code Lab Generator: How to use")  # sets the title of the
    howto_window.geometry("1000x500")  # sets the geometry of toplevel
    howto_window.resizable(False, False)

    howto_image = PhotoImage(file=relative_to_assets("Howto.png"))
    howto_frame = Label(howto_window, image=howto_image)
    howto_frame.image = howto_image
    howto_frame.pack()


menubar = Menu(window, background='#ff8000', foreground='black', activebackground='white', activeforeground='black')
file = Menu(menubar, tearoff=0)
file.add_command(label="New")
file.add_command(label="Open")
file.add_command(label="Save")
file.add_command(label="Save as")
file.add_separator()
file.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=file)

edit = Menu(menubar, tearoff=0)
edit.add_command(label="Undo")
edit.add_command(label="Cut")
edit.add_command(label="Copy")
edit.add_command(label="Paste")
menubar.add_cascade(label="Edit", menu=edit)

help_tab = Menu(menubar, tearoff=0)
help_tab.add_command(label="About", command=about)
help_tab.add_command(label="How to use", command=howto)
menubar.add_cascade(label="Help", menu=help_tab)

#################################################################################

window.config(menu=menubar)
window.resizable(False, False)
window.mainloop()
