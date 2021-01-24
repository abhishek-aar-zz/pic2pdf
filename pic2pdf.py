import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import *

from PIL import Image, ImageDraw

"""
Online References
1> To calculate the pixels
    https://www.pixelcalculator.com/index.php?round=&FORM=1&DP=1&FA=&lang=en&mm1=35&mm2=45&dpi1=300&sub1=+calculate+#a1
2>
"""


class C4U:
    """Constants for You: A class of constants"""

    # sizes (w*h) are in mm
    paper_sizes = {"A4": (210, 297), "A5": (148, 210)}
    grid_offsets = {
        "xscreen": 465,
        "yscreen": 580,
        "x1": 20,
        "y1": 10,
        "x2": 2,
        "y2": 2,
    }
    photo_sizes = {
        "Indian Passport Size": (35, 45),
        "Indian Stamp Size": (20, 25),
        "Indian SSLC Size": (25, 25),
        "Indian Normal Stamp size": (25, 30),
        "Indian Pan Card Size": (25, 35),
        "Indian Passport Form Size": (35, 35),
    }
    # photo_borders dimensions are in pixels and not in mm
    photo_borders = {
        "Indian Passport Size": (25, 25),
        "Indian Stamp Size": (20, 20),
        "Indian SSLC Size": (15, 15),
        "Indian Normal Stamp size": (20, 20),
        "Indian Pan Card Size": (20, 20),
        "Indian Passport Form Size": (25, 25),
    }


class State:
    def __init__(self) -> None:
        self.PATHS = []
        self.dirPATH = ""
        self.pw = 0  # pic width
        self.w = 0  # window screen width
        self.ph = 0  # pic height
        self.h = 0  # window screen height
        self.filename = ""
        self.validity = 0
        self.DPI_value = 300  # default DPI
        self.built_flag = 0
        self.photo_type = ""
        self.selective_paste_flag = False
        self.versionList = [
            ["21.1.7", "Initial Version"],
            ["21.1.16", "Code reformat"],
            ["21.1.18", "Code reformat"],
            ["21.1.20", "Code reformat"],
            ["21.1.23", "Code reformat"],
            ["21.1.24", "Added Selective Paste"],
        ]
        self.copies = []
        self.customCopies = 0


class BackEnd:
    def setState(self, given_state: State) -> None:
        self.state = given_state

    def tryExcept(self, fun):
        try:
            fun()
        except:
            pass

    def selImgBtn(self):
        PATHs = list(
            filedialog.askopenfilenames(
                initialdir=os.getcwd(),
                title="Select image(s)",
                filetypes=[("Images", [".png", ".jpg", ".jpeg"])],
            )
        )
        if len(PATHs) != 0:
            self.state.PATHS = sorted(list(set(self.state.PATHS + PATHs)))

    def enablePart(self):
        if self.enable_part_button["text"] == "Enable":
            self.enable_part_button["text"] = "Disable"
            entry = self.select_images.children["part_print"].children["part_reg_entry"]
            entry["state"] = "enable"
        else:
            self.enable_part_button["text"] = "Enable"
            entry = self.select_images.children["part_print"].children["part_reg_entry"]
            entry.delete(0, "end")
            entry["state"] = "disable"
            self.state.selective_paste_flag = False

    def getBorderSize(self):
        try:
            pic_border = C4U.photo_borders[self.state.photo_type]
        except:
            pic_border = C4U.photo_borders["Indian Passport Size"]
            print(f"\t[i] Border size if defaulted to '{pic_border}'")
        return pic_border

    def putBorder(self, pic):
        print(f"\t[i] Putting borders for the pictures")
        w, h = pic.size  # width, height
        pic_border = self.getBorderSize()

        image_with_border = Image.new(
            "RGB",
            (w + 2 * pic_border[0], h + 2 * pic_border[1]),
            (255, 255, 255, 255),
        )
        position = (pic_border[0], pic_border[1])
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

    def parseReg(self):
        part_print_children = self.select_images.children["part_print"].children
        reg = part_print_children["part_reg_entry"].get()
        l = [i.split(":") for i in reg.split(";")]
        for i in l:
            if len(i) != 2:
                print(f"[!] Reg-Parse Error: There are more number of ':'")
                raise Exception("Reg-Parse Error")
            i[0] = int(i[0].strip())
            els = i[1].split(",")
            nums = []
            for k in els:
                try:
                    nums.append(int(k.strip()))
                except:
                    if "-" in k:
                        a, b = map(int, k.split("-"))
                        nums += list(range(a, b + 1))
            i[1] = list(set(nums))
        return l

    def makeFullCopies(self):
        def getPicNum(pw, ph, w, h):
            """Return the xpics, ypics and total number of pics in a page"""
            return (
                int((w - 40) / pw),  # xpics
                int((h - 40) / ph),  # ypics
                int((w - 40) / pw) * int((h - 40) / ph),  # total
            )

        def getPixel(side):
            return int(side * DPI_value / 25.4)

        paths = self.state.PATHS
        DPI_value = self.state.dpi_entry_value
        pw = getPixel(self.state.pw)
        ph = getPixel(self.state.ph)
        pic_border = self.getBorderSize()
        # Adding gutter pixels
        pw, ph = (pw + 2 * pic_border[0], ph + 2 * pic_border[1])
        w = getPixel(self.state.w)
        h = getPixel(self.state.h)
        xpics, ypics, totpix = getPicNum(pw, ph, w, h)
        if totpix < getPicNum(pw, ph, h, w)[2]:
            w, h = h, w  # swap dimensions
            print(
                f"\t[i] Change in page orientation to accommodate pics from '{totpix}' to '{getPicNum(pw, ph, w, h)[2]}'"
            )
            xpics, ypics, totpix = getPicNum(pw, ph, w, h)

        a4 = Image.new("RGB", (w, h), (255, 255, 255, 255))
        positions = [
            (i, j)
            for i in range(int(0.5 * (w - pw * xpics)), w, pw)
            for j in range(int(0.5 * (h - ph * ypics)), h, ph)
            if (w - 0.5 * (w - pw * xpics)) - i >= pw
            and (h - 0.5 * (h - ph * ypics)) - j >= ph
        ]
        totpaths = len(paths)
        # print("positions: " + str(positions))
        li = [int(totpix / totpaths) + totpix % totpaths]
        for j in range(1, totpaths):
            li.append(int(totpix / totpaths))
        # Mention number of copies if not equal
        # li = [8,8,3,3,3,3]
        def full():
            print(f"\t[i] Entering into Full Copy mode since no regex is given")
            i = 0
            kkk = 0
            for j in li:
                pic = Image.open(paths[kkk])
                pic = pic.resize(
                    (
                        int(self.state.pw * DPI_value / 25.4),
                        int(self.state.ph * DPI_value / 25.4),
                    )
                )
                pic = self.putBorder(pic)
                kkk += 1
                for k in range(j):
                    a4.paste(pic, positions[i])
                    i += 1

        def partial():
            print(f"\t[i] Entering into Selective Paste Mode.")
            li = self.parseReg()
            dikt = {i: -1 for i in range(totpix)}
            for i in li:
                a, b = i
                for c in b:
                    dikt[c - 1] = a - 1
            i = 0
            for i, j in dikt.items():
                # i: pic position in paper
                # j: image path index
                if j != -1 and j >= 0 and j < len(paths):
                    if i >= 0 and i < len(positions):
                        pic = Image.open(paths[j])
                        pic = pic.resize(
                            (
                                int(self.state.pw * DPI_value / 25.4),
                                int(self.state.ph * DPI_value / 25.4),
                            )
                        )
                        pic = self.putBorder(pic)
                        a4.paste(pic, positions[i])

        def save(extension):
            a4.save(self.state.filename + extension)
            print(f"\t[i] Output file save as: {self.state.filename + extension}")

        partial() if self.state.selective_paste_flag else full()
        save(".jpg") if self.state.imgchk.get() else None
        save(".pdf") if self.state.pdfchk.get() else None
        self.state.built_flag = 1

    def closeCustomSize(self, custom_frame):
        children = custom_frame.children
        children["custom_button"]["state"] = "enabled"
        try:
            children["width_entry"].grid_remove()
            children["height_entry"].grid_remove()
        except:
            pass
        children["save_button"].grid_remove()
        children["cancel_button"].grid_remove()
        self.clearWH(custom_frame)
        print(
            f"\t[i] Cleared: pw: '{self.state.pw}', ph: '{self.state.ph}',"
            f"w: '{self.state.w}', h: '{self.state.h}'"
        )

    def saveCustomDim(self, custom_frame):
        warnings = [
            [
                "Non-Positive is unacceptable",
                "Enter a positive number(integer/decimal)",
            ],
            ["Out of range", "Range: 1-999 mm"],
            ["Not a number", "Enter a positive number(integer/decimal)"],
        ]
        save_button = custom_frame.children["save_button"]
        width_entry = custom_frame.children["width_entry"]
        height_entry = custom_frame.children["height_entry"]
        try:
            width = int(width_entry.get())
            height = int(height_entry.get())
            if width <= 0 or height <= 0:
                messagebox.showwarning(*warnings[0])
                return
            if width >= 1000 or height >= 1000:
                messagebox.showwarning(*warnings[1])
                return
        except:
            messagebox.showwarning(*warnings[2])
            return
        if custom_frame._name == "f_sel_pic_size":
            self.state.pw, self.state.ph = width, height
        else:
            self.state.w, self.state.h = width, height
        width_entry.grid_remove()
        height_entry.grid_remove()
        save_button["text"] = f"Saved: {width}x{height} mm^2"
        save_button["width"] = 35
        save_button["state"] = tk.DISABLED
        siblings = custom_frame.master.children
        combobox = (
            siblings["!combobox"]
            if custom_frame._name == "f_sel_pic_size"
            else siblings["!combobox2"]
        )
        combobox.set("")
        print(
            f"\t[i] Saved: pw: '{self.state.pw}', ph: '{self.state.ph}',"
            f"w: '{self.state.w}', h: '{self.state.h}'"
        )

    def clearWH(self, custom_frame):
        flag = 1 if custom_frame._name == "f_sel_pic_size" else 0
        if flag:
            self.state.pw = 0
            self.state.ph = 0
        else:
            self.state.w = 0
            self.state.h = 0

    def validation(self):
        state_it = self.crtFrm()
        state_it.grid(column=0, row=8, pady=2, padx=C4U.grid_offsets["x1"])
        lab0 = Label(state_it, text="Processing...")
        lab0.grid(ipadx=5, pady=C4U.grid_offsets["y2"], padx=C4U.grid_offsets["x2"])
        msg = []

        def v_selectImage():
            if len(self.state.PATHS) == 0:
                msg.append("Select at least one image")
            warning = "One of the given paths does not exist. Check cmd-line"
            for i in self.state.PATHS:
                if not os.path.exists(i):
                    msg.append(warning) if warning not in msg else None
                    print(f"[!] The following media path does not exist: '{i}'")
            print(f"\t[i] Media Paths: {self.state.PATHS}")

        def v_selective():
            part_print_children = self.select_images.children["part_print"].children
            if part_print_children["ena_part"]["text"] == "Disable":
                reg = part_print_children["part_reg_entry"].get()
                if reg == "":
                    msg.append("Selective Paste has Empty string")
                    self.enablePart()
                else:
                    try:
                        l = self.parseReg()
                        self.state.selective_paste_flag = True
                        print(f"\t[i] Parsed regex: {l}")
                    except:
                        msg.append("Regex Parsing Error")

        def v_photoSize():
            if (self.state.pw == 0) and (self.state.ph == 0):
                try:
                    self.state.photo_type = (
                        self.select_size.children["!combobox"].get().split(":")[0]
                    )
                    photo_size = C4U.photo_sizes[self.state.photo_type]
                    self.state.pw, self.state.ph = photo_size
                    print(
                        f"\t[i] Photo_type: {self.state.photo_type}, Photo_size: {photo_size}"
                    )
                except:
                    msg.append("Select the photo type/size")
            else:
                print(f"\t[i] Custom photo_size: {(self.state.pw, self.state.ph)}")

        def v_paperSize():
            if (self.state.w == 0) and (self.state.h == 0):
                try:
                    btn1_value = (
                        self.select_size.children["!combobox2"].get().split(":")[0]
                    )
                    paper_size = C4U.paper_sizes[btn1_value]
                    self.state.w = paper_size[0]
                    self.state.h = paper_size[1]
                    print(f"\t[i] Paper_type: {btn1_value}, Paper_size: {paper_size}")
                    del paper_size, btn1_value
                except:
                    msg.append("Select the output paper size")
            else:
                print(f"\t[i] Custom paper_size: {(self.state.w, self.state.h)}")
            # --------- pic < paper
            if self.state.pw * self.state.ph > self.state.w * self.state.h:
                msg.append("Paper size must be greater than pic size")

        def v_dpiEntry():
            try:
                self.state.dpi_entry_value = int(self.state.dpi_entry.get())
            except:
                msg.append("Output DPI must be an integer")
            if self.state.dpi_entry_value <= 0:
                self.state.dpi_entry_value = 300
                self.state.dpi_entry.delete(0, "end")
                self.state.dpi_entry.insert(0, "300")
                msg.append("Output DPI must be greater than 0")
            print(f"\t[i] Current DPI: {self.state.dpi_entry_value}")

        def v_filename():
            filename = str(self.state.op_filename_entry.get())
            if filename == "":
                msg.append("Provide the output filename")
            else:
                self.state.filename = filename.replace("/", "\\")
            print(f"\t[i] Filename: '{self.state.filename}'")

        def v_checkbox():
            try:
                if (self.state.imgchk.get() == 0) and (self.state.pdfchk.get() == 0):
                    msg.append("Select at least one output format")
                print(
                    f"\t[i] ImageFlag: {self.state.imgchk.get()}, PdfFlag: {self.state.pdfchk.get()}"
                )
            except:
                msg.append("Select at least one output format")

        def v_destinationPath():
            if self.state.dirPATH == "":
                msg.append("Select destination path")
            elif not os.path.exists(self.state.dirPATH):
                self.state.dirPATH = ""
                msg.append("Destination path does not exist")
            print(f"\t[i] O/P Directory: '{self.state.dirPATH}'")

        print("--------------- Validation ---------------")
        v_selectImage()
        v_selective()
        v_photoSize()
        v_paperSize()
        v_dpiEntry()
        v_filename()
        v_checkbox()
        v_destinationPath()
        print("------------------------------------------")
        if len(msg) == 0:
            self.state.validity = True
            lab0["text"] = "Good to go..."
            messagebox.showinfo("Great", "Good to go...")
            self.state.validate_button["state"] = tk.DISABLED
            self.state.build_button["state"] = tk.NORMAL
        else:
            lab0["text"] = "Check again and validate"
            messagebox.showwarning(
                "Warnings",
                "\n".join(["{}> {}".format(i + 1, msg[i]) for i in range(len(msg))]),
            )
        lab0.grid_remove()
        state_it.destroy()

    def builder(self):
        print("---------------- Building ----------------")
        build_it = self.crtFrm()
        build_it.grid(column=0, row=7, pady=2, padx=C4U.grid_offsets["x1"])
        lab0 = Label(build_it, text="Building...")
        lab0.grid(
            columnspan=10,
            ipadx=5,
            pady=C4U.grid_offsets["y2"],
            padx=C4U.grid_offsets["x2"],
        )
        self.makeFullCopies()
        lab0.grid_remove()
        if self.state.built_flag == 0:
            messagebox.showerror(
                "S0RTA Bug", "There was an error\nPlease contact the dev"
            )
        else:
            self.state.built_flag = 0
            messagebox.showinfo("Job is done", "Successfully saved at the location :)")
        self.state.validate_button["state"] = "normal"
        self.state.build_button["state"] = "disabled"
        build_it.destroy()
        print("------------------------------------------")

    def refreshwindow(self):
        print("--------------- Refreshing ---------------")
        self.state.PATHS = []
        self.state.dirPATH = ""
        self.state.pw = 0
        self.state.w = 0
        self.state.ph = 0
        self.state.h = 0
        self.state.filename = ""
        self.state.validity = 0
        self.state.built_flag = 0
        self.state.dpi_entry_value = 300
        self.state.selective_paste_flag = False
        self.select_size.children["!combobox"].set("")
        self.select_size.children["!combobox2"].set("")
        self.state.imgchk.set(0)
        self.state.pdfchk.set(0)
        self.state.validate_button["state"] = "normal"
        self.state.build_button["state"] = "disabled"
        self.state.dpi_entry.delete(0, "end")
        self.state.dpi_entry.insert(0, "300")
        if self.enable_part_button["text"] == "Disable":
            self.enablePart()
        self.state.op_filename_entry.delete(0, "end")
        for i, j in self.select_size.children.items():
            if "f_sel_" in i and "cancel_button" in j.children:
                j.children["cancel_button"].invoke()

        def fun4():
            self.state.lab_ch_op.grid_remove()

        self.tryExcept(fun4)
        print("------------------------------------------")


class GUI(BackEnd):
    def __init__(self):
        self.state = State()
        self.setState(self.state)
        self.display()

    def display(self):
        self.window_init()
        self.layer1Frame()

    def window_init(self):
        self.window = tk.Tk()
        self.window.title("ArgZ Pic2Pdf v{}".format(self.state.versionList[-1][0]))
        self.window.geometry(
            "{}x{}".format(C4U.grid_offsets["xscreen"], C4U.grid_offsets["yscreen"])
        )
        self.window.resizable(0, 0)

    def mySep(self, column: int, row: int):
        Separator(self.window).grid(column=column, row=row, sticky="ew")

    def crtFrm(self):
        return Frame(self.window)

    def crtBtn(self, name, frame, text: str, command, state="enabled", width=None):
        button = Button(frame, text=text, command=command, state=state, name=name)
        if width:
            button["width"] = width
        return button

    def crtLbl(self, given_frame, text, column: int, row: int, padx: str, pady: str):
        Label(given_frame, text=text).grid(
            column=column,
            row=row,
            padx=C4U.grid_offsets[padx],
            pady=C4U.grid_offsets[pady],
        )

    def gridConfig(self, given_frame, column, row, padx, pady, columnspan=None):
        given_frame.grid(
            column=column,
            row=row,
            padx=C4U.grid_offsets[padx],
            pady=C4U.grid_offsets[pady],
            columnspan=columnspan,
        )

    def layer1Frame(self):
        self.select_images = self.crtFrm()
        self.gridConfig(self.select_images, 0, 0, "x1", "y1", columnspan=2)
        self.callSelectImagesF()
        self.mySep(0, 1)  # -----------------------------------------------
        self.select_size = self.crtFrm()
        self.gridConfig(self.select_size, 0, 2, "x1", "y1")
        self.callSelectSizeF()
        self.callSelectOpSizeF()
        self.mySep(0, 3)  # -----------------------------------------------
        self.save_it = self.crtFrm()
        self.gridConfig(self.save_it, 0, 4, "x1", "y1")
        self.callSaveItF()
        self.mySep(0, 5)  # -----------------------------------------------
        self.create_it = self.crtFrm()
        self.gridConfig(self.create_it, 0, 6, "x1", "y1")
        self.callValidateF()
        self.mySep(0, 9)  # -----------------------------------------------
        self.note_it = self.crtFrm()
        self.gridConfig(self.note_it, 0, 10, "x1", "y1")
        self.callNotesF()
        self.window.mainloop()  # Loop ------------------------------------

    def callSelectImagesF(self):
        labels = [
            "Please select the image(s): ",
            "See selected images",
            "Selective Paste: ",
        ]
        self.crtLbl(self.select_images, labels[0], 0, 1, "x2", "y2")
        btn3 = self.crtBtn("btn3", self.select_images, "Select...", self.selImgBtn)
        btn3 = Button(self.select_images, text="Select...", command=self.selImgBtn)
        self.gridConfig(btn3, 1, 1, "x2", "y2")
        btn4 = self.crtBtn("btn4", self.select_images, labels[1], self.seeSelImgW)
        self.gridConfig(btn4, None, None, "x2", "y2", columnspan=2)
        part_print = Frame(self.select_images, name="part_print")
        self.gridConfig(part_print, 0, 3, "x2", "y2", columnspan=2)
        self.crtLbl(part_print, labels[2], 0, 0, "x2", "y2")
        part_regex = Entry(part_print, width=25, name="part_reg_entry")
        self.gridConfig(part_regex, 1, 0, "x2", "y2", columnspan=3)
        part_regex["state"] = "disable"
        self.enable_part_button = self.crtBtn(
            "ena_part", part_print, "Enable", self.enablePart
        )
        self.gridConfig(self.enable_part_button, 4, 0, "x2", "y2")

    def seeSelImgW(self):
        screen = tk.Tk()  # Screen / Window
        screen.geometry("900x300")  # screen size
        screen.resizable(width=0, height=0)  # Making it non resizable
        # left frame for table/treeview and (horizontal scroll bar[r8 now -n/a])
        lefty = Frame(screen)
        self.gridConfig(lefty, 0, 0, "x1", "y1")
        lefty.pack(side="left")
        # Treeview instance
        treetime = Treeview(lefty)
        treetime.pack(side=tk.TOP, fill=tk.X)
        # vertical scrollbar
        vbar = Scrollbar(screen, orient="vertical", command=treetime.yview)
        vbar.pack(side="right", fill="y")
        treetime.configure(yscrollcommand=vbar.set)
        # Columns
        treetime["columns"] = ("1", "2")
        treetime.column("1", width=50, minwidth=40, anchor=tk.W)
        treetime.column("2", width=800, minwidth=400, anchor=tk.W)
        treetime["show"] = "headings"
        treetime.heading("1", text="Sl. No.")
        treetime.heading("2", text="Path")
        for i in range(1, len(self.state.PATHS) + 1):
            treetime.insert("", "end", values=(str(i), self.state.PATHS[i - 1]))
        screen.mainloop()

    def callSelectSizeF(self):
        labels = ["Given photo type[ratio]: "]
        # --------- photo size
        self.crtLbl(self.select_size, labels[0], 0, 0, "x2", "y2")
        combo_photo = Combobox(self.select_size, width=40)
        combo_photo["values"] = [
            i + ": " + str(C4U.photo_sizes[i]) + "[in mm]"
            for i in [i for i in C4U.photo_sizes.keys()]
        ]
        self.gridConfig(combo_photo, 1, 0, "x2", "y2")
        # -------- custom photo size
        custom_frame = Frame(self.select_size, name="f_sel_pic_size")
        self.gridConfig(custom_frame, 0, 1, "x2", "y2", columnspan=2)
        custom_button = self.crtBtn(
            "custom_button",
            custom_frame,
            "Custom",
            lambda: self.callCustomSizeF(custom_frame),
        )
        self.gridConfig(custom_button, 0, 0, "x2", "y2", columnspan=2)

    def callSelectOpSizeF(self):
        labels = ["Required output paper size: "]
        # --------O/p size
        self.crtLbl(self.select_size, labels[0], 0, 3, "x2", "y2")
        combo_paper = Combobox(self.select_size, width=40)
        combo_paper["values"] = [
            i + ": " + str(C4U.paper_sizes[i]) + "[in mm]"
            for i in [i for i in C4U.paper_sizes.keys()]
        ]
        self.gridConfig(combo_paper, 1, 3, "x2", "y2")
        # --------custom o/p size
        custom_frame = Frame(self.select_size, name="f_sel_pap_size")
        self.gridConfig(custom_frame, 0, 4, "x2", "y2", columnspan=2)
        custom_button = self.crtBtn(
            "custom_button",
            custom_frame,
            "Custom",
            lambda: self.callCustomSizeF(custom_frame),
        )
        self.gridConfig(custom_button, 0, 0, "x2", "y2", columnspan=2)
        # ---------DPI
        dpi_frame = Frame(self.select_size, name="f_dpi")
        self.gridConfig(dpi_frame, None, 6, "x2", "y2", columnspan=2)
        Label(dpi_frame, text="Output DPI: ").grid()
        self.state.dpi_entry = Entry(dpi_frame, width=8)
        self.state.dpi_entry.insert(0, "300")
        self.gridConfig(self.state.dpi_entry, 1, 0, "x2", "y2")

    def callCustomSizeF(self, custom_frame):
        cus_button = custom_frame.children["custom_button"]
        cus_button["state"] = "disabled"

        width_entry = Entry(custom_frame, width=10, name="width_entry")
        self.gridConfig(width_entry, 2, 0, "x2", "y2")
        height_entry = Entry(custom_frame, width=10, name="height_entry")
        self.gridConfig(height_entry, 3, 0, "x2", "y2")

        prev_width = (
            self.state.pw if custom_frame._name == "f_sel_pic_size" else self.state.w
        )
        prev_height = (
            self.state.ph if custom_frame._name == "f_sel_pic_size" else self.state.h
        )
        show_width = prev_width if prev_width else "w"
        show_height = prev_height if prev_height else "h"
        width_entry.insert(0, show_width)
        height_entry.insert(0, show_height)
        save_button = self.crtBtn(
            "save_button",
            custom_frame,
            "Save",
            lambda: self.saveCustomDim(custom_frame),
            width=5,
        )
        self.gridConfig(save_button, 4, 0, "x2", "y2")
        cancel_button = self.crtBtn(
            "cancel_button",
            custom_frame,
            "X",
            lambda: self.closeCustomSize(custom_frame),
            width=2,
        )
        self.gridConfig(cancel_button, 5, 0, "x2", "y2")

    def callSaveItF(self):
        # --------- filename input
        self.crtLbl(self.save_it, "Choose a filename to save: ", 0, 0, "x2", "y2")
        self.state.op_filename_entry = Entry(self.save_it, width=40)
        self.gridConfig(self.state.op_filename_entry, 1, 0, "x2", "y2")
        # --------- checkbox :image or/and pdf
        self.crtLbl(self.save_it, "What do you want: ", 0, 1, "x2", "y2")
        checkFrame = Frame(self.save_it)
        self.gridConfig(checkFrame, 1, 1, "x2", "y2")
        self.state.imgchk, self.state.pdfchk = tk.IntVar(), tk.IntVar()

        ch1 = Checkbutton(checkFrame, text="Image", variable=self.state.imgchk)
        self.gridConfig(ch1, 0, 0, "x2", "y2")
        ch2 = Checkbutton(checkFrame, text="Pdf", variable=self.state.pdfchk)
        self.gridConfig(ch2, 1, 0, "x2", "y2")
        # --------- where to save
        self.crtLbl(self.save_it, "Choose a directory to save: ", 0, 2, "x2", "y2")
        btn5 = self.crtBtn("dir_button", self.save_it, "Choose...", self.chooseOPDirF)
        self.gridConfig(btn5, 1, 2, "x2", "y2")

    def chooseOPDirF(self):
        warnings = [["Warning while choosing", "Output directory path cannot be empty"]]
        dir_path = filedialog.askdirectory(
            initialdir=os.getcwd(), title="Select image(s)"
        )
        self.state.dirPATH = dir_path
        if self.state.dirPATH == "":
            messagebox.showwarning(*warnings[0])
        else:
            self.state.lab_ch_op = tk.Entry(self.save_it, width=60)
            self.gridConfig(self.state.lab_ch_op, 0, 3, "x2", "y2", 2)
            self.state.lab_ch_op.insert(0, self.state.dirPATH)
            self.state.lab_ch_op["state"] = "disabled"

    def callValidateF(self):
        def localGridConfig(given_frame, row, col, ipadx, ipady, padx, pady):
            given_frame.grid(
                ipady=ipady,
                ipadx=ipadx,
                row=row,
                column=col,
                pady=C4U.grid_offsets[pady],
                padx=C4U.grid_offsets[padx],
            )

        # --------- Validate button
        self.state.validate_button = self.crtBtn(
            "validate_button", self.create_it, "Validate", self.validation
        )
        localGridConfig(self.state.validate_button, 0, 0, 10, 5, "x2", "y2")
        # --------- Build button
        self.state.build_button = self.crtBtn(
            "build_button", self.create_it, "Build", self.builder, "disabled"
        )
        localGridConfig(self.state.build_button, 0, 1, 30, 5, "x2", "y2")
        # --------- Refresh
        refresh_button = self.crtBtn(
            "refresh_button", self.create_it, "Refresh", self.refreshwindow
        )
        localGridConfig(refresh_button, 0, 2, 10, 5, "x2", "y2")

    def callNotesF(self):
        """Displays the notes"""
        note1 = "All measurements are in mm"
        note2 = "Built by: ARG-Z"
        note3 = f"Version: {self.state.versionList[-1][0]}"
        self.crtLbl(self.note_it, note1, 0, 0, "x2", "y2")
        self.crtLbl(self.note_it, note2, 0, 1, "x2", "y2")
        self.crtLbl(self.note_it, note3, 0, 3, "x2", "y2")


GUI()
