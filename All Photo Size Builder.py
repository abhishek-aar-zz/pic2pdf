from PIL import Image, ImageDraw
import os
import tkinter as tk
from tkinter.ttk import *
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
import enum
# from PyQt5 import QtGui
'''
Online References
1> To calculate the pixels
    https://www.pixelcalculator.com/index.php?round=&FORM=1&DP=1&FA=&lang=en&mm1=35&mm2=45&dpi1=300&sub1=+calculate+#a1
2> 
'''


class C4U:
    # sizes (w*h) are in mm
    paper_sizes = {
        "A4": (210, 297), "A5": (148, 210)}
    grid_offsets = {
        "xscreen": 465, "yscreen": 550,
        "x1": 20, "y1": 10,
        "x2": 2, "y2": 2}
    photo_sizes = {
        'Indian Passport Size': (35, 45),
        'Indian Stamp Size': (20, 25),
        "Indian SSLC Size": (25, 25),
        "Indian Normal Stamp size": (25, 30),
        "Indian Pan Card Size": (25, 35),
        "Indian Passport Form Size": (35, 35)
    }
    photo_borders = {
        "passport": (12, 12)
    }


class PPSPB:
    PATHS = []
    dirPATH = ""
    pw = 0
    w = 0
    ph = 0
    h = 0
    filename = ""
    validity = 0
    DPI = 300
    imgchk = 0
    pdfchk = 0
    built = 0
    versionX = "1.0"
    updatedonX = "07-01-2020"

    def __init__(self):
        self.GUI()
    # def centerwindow(self,window):
    #     window.update_idletasks()
    #     app = QtGui.QGuiApplication([])
    #
    #     size = tuple(int(_) for _ in window.geometry().split('+')[0].split('x'))
    #     x = (C4U.grid_offsets['xscreen'] / 2) - (size[0] / 2)
    #     y = (C4U.grid_offsets['yscreen'] / 2) - (size[1] / 2)
    #     window.geometry("+%d+%d" % (x, y))

    def putBorder(self, pic):
        w, h = pic.size
        image_with_border = Image.new('RGB', (
            (w + 2 * C4U.photo_borders['passport'][0]), (h + 2 * C4U.photo_borders['passport'][1])),
                                      (255, 255, 255, 255))
        position = (C4U.photo_borders['passport'][0], C4U.photo_borders['passport'][1])
        image_with_border.paste(pic, position)
        w, h = image_with_border.size
        drawlplus = ImageDraw.Draw(image_with_border)
        # draw corner lines on the image tile
        drawlplus.line((0, 0, 0, 10), fill=0, width=1)
        drawlplus.line((0, 0, 10, 0), fill=0, width=1)
        drawlplus.line((0, h - 1, 0, h - 10 - 1), fill=0, width=1)
        drawlplus.line((0, h - 1, 10, h - 1), fill=0, width=1)
        drawlplus.line((w - 1, 0, w - 1, 10), fill=0, width=1)
        drawlplus.line((w - 1, 0, w - 10 - 1, 0), fill=0, width=1)
        drawlplus.line((w - 1, h - 1, w - 10 - 1, h - 1), fill=0, width=1)
        drawlplus.line((w - 1, h - 1, w - 1, h - 10 - 1), fill=0, width=1)
        return image_with_border

    def makefullcopies(self):
        paths = self.PATHS
        pw, ph = (int(self.pw * self.DPI / 25.4), int(self.ph * self.DPI / 25.4))
        pw, ph = ((pw + 2 * C4U.photo_borders['passport'][0]), (ph + 2 * C4U.photo_borders['passport'][1]))
        w, h = (int(self.w * self.DPI / 25.4), int(self.h * self.DPI / 25.4))
        # print("(w,h):" + str(w) + " " + str(h))
        # print("(pw,ph):" + str(pw) + " " + str(ph))
        xpics = int((w - 40) / pw)
        ypics = int((h - 40) / ph)
        totpaths = len(paths)
        totpix = xpics * ypics

        if xpics * ypics < (int(h - 40) / pw * int(w - 40)):
            w, h = h, w
            xpics = int((w - 40) / pw)
            ypics = int((h - 40) / ph)
            totpix = xpics * ypics

        a4 = Image.new('RGB', (w, h), (255, 255, 255, 255))
        positions = [(i, j) for i in range(int(0.5 * (w - pw * xpics)), w, pw) for j in
                     range(int(0.5 * (h - ph * ypics)), h, ph) if
                     (w - 0.5 * (w - pw * xpics)) - i >= pw and (h - 0.5 * (h - ph * ypics)) - j >= ph]
        # print("positions: " + str(positions))
        li = [int(totpix / totpaths) + totpix % totpaths]
        for j in range(1, totpaths):
            li.append(int(totpix / totpaths))
        # print(li)
        i = 0
        kkk = 0
        for j in li:
            pic = Image.open(paths[kkk])
            pic = pic.resize((int(self.pw * self.DPI / 25.4), int(self.ph * self.DPI / 25.4)))
            pic = self.putBorder(pic)
            kkk += 1
            for k in range(j):
                a4.paste(pic, positions[i])
                i += 1
        if self.imgchk:
            a4.save(self.filename + "APSB.jpg")
        if self.pdfchk:
            a4.save(self.filename + "APSB.pdf")
        self.built = 1

    def builder(self, window, validat, sub):
        createit = Frame(window)
        createit.grid(column=0, row=7,pady=2, padx=C4U.grid_offsets['x1'])
        lab0 = Label(createit, text="Building...")
        lab0.grid(columnspan=10,ipadx=5, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])
        self.makefullcopies()
        if self.built == 0:
            messagebox.showerror("S0RTA Bug","There was an error\nPlease contact the dev @ github.com/arg-z")
        else:
            self.built = 0
            messagebox.showinfo("Job is done","Succesfully saved at the location :)")
        validat['state'] = 'normal'
        sub['state'] = 'disabled'
        lab0.grid_remove()
        createit.destroy()

    def GUI(self):
        window = tk.Tk()
        window.title("All Size Photo Builder v{}".format(self.versionX))
        window.geometry('{}x{}'.format(C4U.grid_offsets["xscreen"], C4U.grid_offsets["yscreen"]))
        window.resizable(0, 0)
        # ----------------------------------------------------------------------------
        # Frames - level 1
        select_images = Frame(window)
        select_images.grid(column=0, row=0, columnspan=2, pady=C4U.grid_offsets['y1'], padx=C4U.grid_offsets['x1'])
        Separator(window).grid(column=0, row=1, sticky="ew")
        select_size = Frame(window)
        select_size.grid(column=0, row=2, pady=C4U.grid_offsets['y1'], padx=C4U.grid_offsets['x1'])
        Separator(window).grid(column=0, row=3, sticky="ew")
        saveit = Frame(window)
        saveit.grid(column=0, row=4, pady=C4U.grid_offsets['y1'], padx=C4U.grid_offsets['x1'])
        Separator(window).grid(column=0, row=5, sticky="ew")
        createit = Frame(window)
        createit.grid(column=0, row=6, pady=C4U.grid_offsets['y1'], padx=C4U.grid_offsets['x1'])
        Separator(window).grid(column=0, row=9, sticky="ew")
        noteit = Frame(window)
        noteit.grid(column=0, row=10, pady=C4U.grid_offsets['y1'], padx=C4U.grid_offsets['x1'])
        # ---------------------------------------------------------------------------
        # Select images [frame]
        # ---------
        Label(select_images, text='Please select the image(s): ').grid(column=0, row=1, pady=C4U.grid_offsets['y2'],
                                                                       padx=C4U.grid_offsets['x2'])
        btn3 = Button(select_images, text="Select...", command=self.selImgBtn)
        btn3.grid(column=1, row=1, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])
        btn4 = Button(select_images, text="See selected images", command=self.seeSelImg)
        btn4.grid(columnspan=2, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])
        # ---------
        # ---------------------------------------------------------------------------
        # Select size [frame]
        # ---------
        # --------- photo size
        Label(select_size, text="Given photo type[ratio]: ").grid(column=0, row=0, pady=C4U.grid_offsets['y2'],
                                                                  padx=C4U.grid_offsets['x2'])
        btn2 = Combobox(select_size, width=40)
        val2 = [i + ": " + str(C4U.photo_sizes[i]) + "[in mm]" for i in
                [i for i in C4U.photo_sizes.keys()]]
        btn2['values'] = val2
        btn2.grid(column=1, row=0, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])
        # ---------
        # -------- custom photo size
        cusFra2 = Frame(select_size)
        cusFra2.grid(column=0, row=1, columnspan=2, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])
        btncstm = Button(cusFra2, text="Custom", command=lambda: self.customsize(cusFra2, 1, btn2))
        btncstm.grid(column=0, row=0, columnspan=2, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])
        # ---------
        # --------O/p size
        Label(select_size, text="Required output paper size: ").grid(column=0, row=3, pady=C4U.grid_offsets['y2'],
                                                                     padx=C4U.grid_offsets['x2'])
        btn1 = Combobox(select_size, width=40)
        val1 = [i + ": " + str(C4U.paper_sizes[i]) + "[in mm]" for i in
                [i for i in C4U.paper_sizes.keys()]]
        btn1['values'] = val1
        btn1.grid(column=1, row=3, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])
        # ---------
        # --------custom o/p size
        cusFra = Frame(select_size)
        cusFra.grid(column=0, row=4, columnspan=2, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])
        btncstm2 = Button(cusFra, text="Custom", command=lambda: self.customsize2(cusFra, 0, btn1))
        btncstm2.grid(column=0, row=0, columnspan=2, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])
        # ---------
        # ---------DPI
        dpifra = Frame(select_size)
        dpifra.grid(row=6, columnspan=2, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])
        Label(dpifra, text="Output DPI: ").grid()
        dpi = Entry(dpifra, width=8)
        dpi.insert(0, "300")
        dpi.grid(column=1, row=0, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])
        # ---------
        # ---------------------------------------------------------------------------
        # Save it [frame]
        # --------- filename input
        Label(saveit, text="Choose a filename to save: ").grid(column=0, row=0, pady=C4U.grid_offsets['y2'],
                                                               padx=C4U.grid_offsets['x2'])
        inp1 = Entry(saveit, width=40)
        inp1.grid(column=1, row=0, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])
        # --------- checkbox :image or/and pdf
        Label(saveit, text="What do you want: ").grid(column=0, row=1, pady=C4U.grid_offsets['y2'],
                                                      padx=C4U.grid_offsets['x2'])
        checkFrame = Frame(saveit)
        checkFrame.grid(column=1, row=1, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])
        c1 = tk.IntVar()
        c2 = tk.IntVar()
        self.imgchk = c1
        self.pdfchk = c2
        ch1 = Checkbutton(checkFrame, text="Image", variable=c1)
        ch1.grid(column=0, row=0, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])
        ch2 = Checkbutton(checkFrame, text="Pdf", variable=c2)
        ch2.grid(column=1, row=0, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])
        # --------- where to save
        Label(saveit, text="Choose a directory to save: ").grid(column=0, row=2, pady=C4U.grid_offsets['y2'],
                                                                padx=C4U.grid_offsets['x2'])
        btn5 = Button(saveit, text="Choose...", command=lambda: self.chooseopdir(saveit))
        btn5.grid(column=1, row=2, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])
        # ---------
        # ---------------------------------------------------------------------------
        # Validate - build - refresh
        # --------- validate button
        validat = Button(createit, text="Validate",
                         command=lambda: self.validate(window, btn2, btn1, inp1, c1, c2, sub, validat, dpi))
        validat.grid(ipady=5, ipadx=10, column=0, row=0, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])
        # --------- submit button
        sub = Button(createit, text="Build", state="disabled", command=lambda: self.builder(window, validat, sub))
        sub.grid(column=1, ipady=5, row=0, ipadx=30, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])
        # --------- refresh
        refr = Button(createit, text="Refresh",
                      command=lambda: (self.refreshwindow(btn1, btn2, inp1, c1, c2, validat, sub, dpi)))
        refr.grid(column=2, ipady=5, row=0, ipadx=10, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])
        # ---------
        # ---------------------------------------------------------------------------
        # Note
        # --------- notes
        note1 = "All measurements are in mm"
        Label(noteit, text=note1).grid(column=0, row=0, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])
        note2 = "Made by ARG-Z"
        Label(noteit, text=note2).grid(column=0, row=1, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])
        note2 = "Updated on {} [version {}]".format(self.updatedonX,self.versionX)
        Label(noteit, text=note2).grid(column=0, row=3, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])
        # ---------
        # ---------------------------------------------------------------------------
        # Loop
        # ---------
        # self.centerwindow(window)
        window.mainloop()
        # ---------

    def selImgBtn(self):
        PATHs = list(filedialog.askopenfilenames(initialdir=os.getcwd(), title="Select image(s)",
                                                 filetypes=[("Images", ['.png', '.jpg', '.jpeg'])]))
        if len(PATHs) != 0:
            self.PATHS = PATHs
        # print(self.PATHS)

    def seeSelImg(self):
        # Screen / Window
        screen = tk.Tk()
        # screen size
        screen.geometry("900x300")
        # Making it non resizable
        screen.resizable(width=0, height=0)
        # left frame for table/treeview and (horizontal scroll bar[r8 now -n/a])
        leftie = Frame(screen)
        leftie.pack(side="left")
        # Treeview instance
        treetime = Treeview(leftie)
        treetime.pack(side=tk.TOP, fill=tk.X)
        # vertical scrollbar
        vbar = Scrollbar(screen, orient="vertical", command=treetime.yview)
        vbar.pack(side='right', fill='y')
        treetime.configure(yscrollcommand=vbar.set)
        # Columns
        treetime["columns"] = ("1", "2")
        treetime.column("1", width=50, minwidth=40, anchor=tk.W)
        treetime.column("2", width=800, minwidth=400, anchor=tk.W)
        treetime['show'] = 'headings'
        treetime.heading("1", text="Sl. No.")
        treetime.heading("2", text="Path")
        for i in range(1, len(self.PATHS) + 1):
            treetime.insert("", "end", values=(str(i), self.PATHS[i - 1]))
        screen.mainloop()

    def chooseopdir(self, saveit):
        diPATH = filedialog.askdirectory(initialdir=os.getcwd(), title="Select image(s)")
        self.dirPATH = diPATH
        if self.dirPATH == "":
            messagebox.showwarning(title="Warning @ choosing", message="Output directory path cannot be empty")

        else:
            self.lab_ch_op = tk.Entry(saveit, width=60)
            self.lab_ch_op.grid(column=0, row=3, columnspan=2, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])
            self.lab_ch_op.insert(0, self.dirPATH)

        # print(self.dirPATH)

    def customsize(self, cusfra, i, comboB):
        self.pw_w_switch = i
        self.xxx = Entry(cusfra, width=10)
        self.yyy = Entry(cusfra, width=10)
        if (self.pw == 0):
            self.xxx.insert(0, "w")
        else:
            if i:
                self.xxx.insert(0, self.pw)
            else:
                self.xxx.insert(0, self.w)
        if self.pw == 0:
            self.yyy.insert(0, "h")
        else:
            if i:
                self.yyy.insert(0, self.ph)
            else:
                self.yyy.insert(0, self.h)
        self.bu = Button(cusfra, text="X", width=2, command=lambda: (self.bu.grid_remove(),
                                                                     self.xxx.grid_remove(),
                                                                     self.yyy.grid_remove(),
                                                                     self.su.grid_remove(),
                                                                     self.clearwh(i)))
        self.bu.grid(column=5, row=0, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])

        self.xxx.grid(column=2, row=0, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])
        self.yyy.grid(column=3, row=0, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])
        self.su = Button(cusfra, text="Save", width=5,
                         command=lambda: self.savecuslen(i, self.xxx, self.yyy, self.su, comboB))
        self.su.grid(column=4, row=0, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])

    def customsize2(self, cusfra, i, comboB):
        self.pw_w_switch = i
        self.xxx2 = Entry(cusfra, width=10)
        self.yyy2 = Entry(cusfra, width=10)
        if (self.pw == 0):
            self.xxx2.insert(0, "w")
        else:
            if i:
                self.xxx2.insert(0, self.pw)
            else:
                self.xxx2.insert(0, self.w)
        if self.pw == 0:
            self.yyy2.insert(0, "h")
        else:
            if i:
                self.yyy2.insert(0, self.ph)
            else:
                self.yyy2.insert(0, self.h)
        self.bu2 = Button(cusfra, text="X", width=2, command=lambda: (self.bu2.grid_remove(),
                                                                      self.xxx2.grid_remove(),
                                                                      self.yyy2.grid_remove(),
                                                                      self.su2.grid_remove(),
                                                                      self.clearwh(i)))
        self.bu2.grid(column=5, row=0, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])

        self.xxx2.grid(column=2, row=0, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])
        self.yyy2.grid(column=3, row=0, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])
        self.su2 = Button(cusfra, text="Save", width=5,
                          command=lambda: self.savecuslen(i, self.xxx2, self.yyy2, self.su2, comboB))
        self.su2.grid(column=4, row=0, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])

    def savecuslen(self, i, x, y, su, comboB):
        try:
            if i:
                self.pw = int(x.get())
                self.ph = int(y.get())
            else:
                self.w = int(x.get())
                self.h = int(x.get())
            if int(x.get()) <= 0 or int(y.get()) <= 0:
                messagebox.showwarning("Zero is unacceptable", "Enter the numbers(integers/decimals)")
            else:
                su['text'] = "Saved: {}x{} mm^2".format(x.get(), y.get())
                su['width'] = 35
                su['state'] = tk.DISABLED
                x.grid_remove()
                y.grid_remove()
                comboB.set('')
        except:
            messagebox.showwarning("Not a number", "Enter the numbers(integers/decimals)")

    def clearwh(self, i):
        if i:
            self.pw = 0
            self.ph = 0
        else:
            self.w = 0
            self.h = 0

    def validate(self, window, btn2, btn1, inp1, c1, c2, sub, validat, dpi):
        msg = []
        stateit = Frame(window)
        stateit.grid(column=0, row=8, pady=2, padx=C4U.grid_offsets['x1'])
        lab0 = Label(stateit)
        lab0['text'] = "Processing..."
        lab0.grid(ipadx=5, pady=C4U.grid_offsets['y2'], padx=C4U.grid_offsets['x2'])
        # ----------------------------
        # image selection
        if len(self.PATHS) == 0:
            msg.append("Select at least one image")
        # ----------------------------
        # both size selection
        if (self.pw == 0) and (self.ph == 0):
            try:
                self.pw = C4U.photo_sizes[btn2.get().split(":")[0]][0]
                self.ph = C4U.photo_sizes[btn2.get().split(":")[0]][1]
            except:
                msg.append("Select the photo size")
        if (self.w == 0) and (self.h == 0):
            try:
                self.w = C4U.paper_sizes[btn1.get().split(":")[0]][0]
                self.h = C4U.paper_sizes[btn1.get().split(":")[0]][1]
            except:
                msg.append("Select the output paper size")
        # ----------------------------
        # dpi
        try:
            self.DPI = int(dpi.get())
        except:
            msg.append("Output DPI must be an integer")
        if self.DPI == 0:
            self.DPI = 300
            dpi.delete(0, "end")
            dpi.insert(0, "300")
            msg.append("Output DPI cannot be zero")
        # ----------------------------
        # filename
        filename = str(inp1.get())
        if filename == "":
            msg.append("Choose the destination path")
        self.filename = filename.replace("/", "\\")
        # ----------------------------
        # checkbox
        self.imgchk = c1.get()
        self.pdfchk = c2.get()
        if (self.imgchk == 0) and (self.pdfchk == 0):
            msg.append("Select at least one format")
        # ----------------------------
        # destination path
        if self.dirPATH == "":
            msg.append("Select destination path")
        if len(msg) == 0:
            self.validity = 1
            lab0['text'] = "Good to go..."
            messagebox.showinfo("Great", "Good to go...")
            validat['state'] = tk.DISABLED
            sub['state'] = tk.NORMAL
        else:
            lab0['text'] = 'Check again and validate'
            messagebox.showwarning("Warnings", "\n".join(["{}> {}".format(i + 1, msg[i]) for i in range(len(msg))]))
        lab0.grid_remove()
        stateit.destroy()

    def refreshwindow(self, btn1, btn2, inp1, c1, c2, validat, sub, dpi):
        self.PATHS = []
        self.dirPATH = ""
        self.pw = 0
        self.w = 0
        self.ph = 0
        self.h = 0
        self.filename = ""
        self.validity = 0
        self.built = 0
        btn1.set('')
        btn2.set('')
        inp1.delete(0, 'end')
        c1.set(0)
        c2.set(0)
        validat['state'] = 'normal'
        sub['state'] = 'disabled'
        self.DPI = 300
        dpi.delete(0, "end")
        dpi.insert(0, "300")
        try:
            self.bu.grid_remove()
            self.xxx.grid_remove()
            self.yyy.grid_remove()
            self.su.grid_remove()
            self.clearwh(self.pw_w_switch)
        except:
            pass
        try:
            self.bu2.grid_remove()
            self.xxx2.grid_remove()
            self.yyy2.grid_remove()
            self.su2.grid_remove()
            self.clearwh(self.pw_w_switch)
        except:
            pass
        try:
            self.lab_ch_op.grid_remove()
        except:
            pass


PPSPB()
