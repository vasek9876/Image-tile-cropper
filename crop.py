import os  # os
from tkinter import Tk, Canvas, Entry, Label, Scrollbar, Menu, IntVar  # GUI items
from tkinter import StringVar, Toplevel, DoubleVar  # GUI inside
from tkinter import colorchooser, messagebox, filedialog as fd, mainloop  # GUI popups
from tkinter import BOTH, DISABLED  # GUI constants
from PIL import Image, ImageTk  #


def create_rectangle(canvas, arr, **kwargs):
    x1, y1, x2, y2 = arr[0], arr[1], arr[2], arr[3]
    alpha = int(kwargs.pop('alpha') * 255)
    fill = kwargs.pop('fill')
    fill = main.winfo_rgb(fill) + (alpha,)
    image = Image.new('RGBA', (x2 - x1, y2 - y1), fill)
    images = ImageTk.PhotoImage(image)
    cimage = canvas.create_image(x1, y1, image=images, anchor='nw')
    canvas.create_rectangle(x1, y1, x2, y2, **kwargs)
    return cimage


def getBox(arr, frame_v_index=0, frame_h_index=0):
    w, h = int(arr[3]), int(arr[4])
    x, y = int(arr[1]) + w * frame_v_index, int(arr[2]) + h * frame_h_index
    return x, y, x + w, y + h


def saveCrop(img, title, box):
    path = os.path.join('./frames/' + title + '.png')
    try:
        cropped_img = img.crop(box)
        cropped_img.save(path)
        print('ok: ' + title)
    except Exception as e:
        print('fail: ' + title + ' -- ' + str(e))


def loading():  # not used
    from time import sleep
    from tkinter import ttk
    teams = range(100)
    popup = Toplevel()
    Label(popup, text="Files being downloaded").grid(row=0, column=0)

    progress = 0
    progress_var = DoubleVar()
    progress_bar = ttk.Progressbar(popup, variable=progress_var, maximum=100)
    progress_bar.grid(row=1, column=0)  # .pack(fill=tk.X, expand=1, side=tk.BOTTOM)
    popup.pack_slaves()

    progress_step = float(100.0 / len(teams))

    for _ in teams:
        popup.update()
        sleep(0.1)  # launch task
        progress += progress_step
        progress_var.set(progress)

    return 0


def run(img, dat):
    path = os.path.join(os.getcwd(), "frames")
    if not os.path.isdir(path):
        os.mkdir(path)

    a = open(dat, 'r')
    for line in a.readlines():
        arr = line.split()
        if len(arr) <= 3 or "#" in arr[0]:  # empty line
            pass
        elif len(arr) <= 7:
            num_of_frames = int(arr[5])
            num_ofh_frames = int(arr[6])
            for frameHIndex in range(0, num_ofh_frames):
                for frameIndex in range(0, num_of_frames):
                    saveCrop(img, arr[0] + '_f' + str(frameIndex) + str(frameHIndex),
                             getBox(arr, frameIndex, frameHIndex))
    a.close()
    messagebox.showinfo("info", "Cropping Done")
    print("Done")


class Area:
    def __init__(self, canvas, location, arr):
        # main and editing
        self.text_item = None
        self.binding = None
        self.other = None
        self.m = None
        self.location = location
        self.canvas = canvas

        # for both
        self.arr = arr
        self.arr_length = len(self.arr)
        if self.arr_length < 6:
            self.arr.append(1)
            self.arr.append(1)
        elif self.arr_length < 7:
            self.arr.append(1)
        else:
            pass
        self.arr_length = len(self.arr)

        self.arr[0] = str(self.arr[0])

        # for cropping area
        self.xvar = IntVar()  # cords x
        self.yvar = IntVar()  # cords y
        self.wvar = IntVar()  # width
        self.hvar = IntVar()  # height
        self.rwvar = IntVar()  # repeats w
        self.rhvar = IntVar()  # repeats h

        self.x_click = None
        self.y_click = None
        self.cropping_area_create()  # initialize areas

        # for text
        self.textvar = StringVar()
        self.text_create()  # initialize text

        # self.canvas.tag_bind(str(self.name)+"x","<Enter>", self.tooltip_show)
        # self.canvas.tag_bind(str(self.name)+"x","<Leave>", self.tooltip_hide)

    def cropping_area_create(self):
        num_of_frames = int(self.arr[5])
        num_ofh_frames = int(self.arr[6])
        for frameHIndex in range(0, num_ofh_frames):
            for frameIndex in range(0, num_of_frames):
                array = getBox(self.arr, frameIndex, frameHIndex)
                # rect = self.canvas.create_rectangle(array)
                rect = create_rectangle(self.canvas, array, tag=self.arr[0] + "rect", fill="green", alpha=.1)
                self.rectangle_bind(rect)  # crate cropping

    def rectangle_bind(self, rect):
        self.m = Menu(main, tearoff=0)
        self.m.add_command(label=self.arr[0], state=DISABLED)
        self.m.add_separator()
        self.m.add_command(label="Edit tile", command=self.edit_cropping_area)
        self.m.add_command(label="Create new [Ctrl+n]")
        self.m.add_separator()
        self.m.add_command(label="Delete", command=self.delete)

        self.canvas.tag_bind(rect, '<Button-3>', self.right_click_menu)

    def right_click_menu(self, args):
        try:
            self.m.tk_popup(args.x_root, args.y_root)
        finally:
            self.m.grab_release()

    def delete(self):
        self.edit_crop_cancel()
        self.save_edits_crop("", "", "", "", "", "")

    def default(self):
        self.edit_crop_cancel()
        self.save_edits_crop(self.arr[1], self.arr[2], self.arr[3], self.arr[4], self.arr[5], self.arr[6])

    def edit_cropping_area(self):
        self.xvar.set(self.arr[1])
        self.yvar.set(self.arr[2])
        self.wvar.set(self.arr[3])
        self.hvar.set(self.arr[4])
        self.rwvar.set(self.arr[5])
        self.rhvar.set(self.arr[6])

        ex = Entry(main, width=10, textvariable=self.xvar, bd=0, highlightthickness=1, bg="white")
        ey = Entry(main, width=10, textvariable=self.yvar, bd=0, highlightthickness=1, bg="white")
        ew = Entry(main, width=10, textvariable=self.wvar, bd=0, highlightthickness=1, bg="white")
        eh = Entry(main, width=10, textvariable=self.hvar, bd=0, highlightthickness=1, bg="white")
        erw = Entry(main, width=10, textvariable=self.rwvar, bd=0, highlightthickness=1, bg="white")
        erh = Entry(main, width=10, textvariable=self.rhvar, bd=0, highlightthickness=1, bg="white")

        x0 = int(self.arr[1]) + 30  # self.x_click
        y0 = int(self.arr[2]) + 30  # self.y_click - 15
        y1 = y0 + 10  # self.y_click
        x_change = 85
        data = [[ex, "x0"], [ey, "y0 "], [ew, "width"], [eh, "height"], [erw, "repeat_width"], [erh, "repeat_height"]]

        self.canvas.create_rectangle([x0 - 10, y0 - 10, x0 + 10 + x_change * 6, y0 + 10 + 25], fill="blue",
                                     tag=self.arr[0] + "an" + str(6))  # rect around
        for n in range(6):
            this_x = x0 + x_change * n
            a = self.canvas.create_text(this_x + 25, y0, fill="black", font="Times 10 bold", text=data[n][1],
                                        tag=self.arr[0] + "an" + str(n))
            r = self.canvas.create_rectangle(self.canvas.bbox(a), fill="white",
                                             tag=self.arr[0] + "an" + str(n))  # crate background
            self.canvas.tag_lower(r, a)  # set layout

            self.canvas.create_window(this_x, y1, window=data[n][0], tags=self.arr[0] + "an" + str(n), anchor="nw")

            data[n][0].bind("<Escape>", self.edit_crop_cancel)
            data[n][0].bind("<Button-3>", self.edit_crop_end)
            data[n][0].bind("<Return>", self.edit_crop_end)

        data[0][0].selection_range(0, "end")
        data[0][0].focus_set()

    def edit_crop_cancel(self, args=None):
        for n in range(7):
            self.canvas.delete(self.arr[0] + "an" + str(n))
        self.canvas.delete(self.arr[0] + "rect")
        self.canvas.delete(self.arr[0] + "b")
        self.canvas.delete(self.arr[0] + "x")
        if args is not None:
            args.widget.destroy()

    def edit_crop_end(self, args):
        self.edit_crop_cancel(args)

        try:
            x = self.xvar.get()
            y = self.yvar.get()
            w = self.wvar.get()
            h = self.hvar.get()
            rw = self.rwvar.get()
            rh = self.rhvar.get()
        except:
            self.default()
            print("Values has been set to default. The input value include empty entry.")
        else:
            self.save_edits_crop(x, y, w, h, rw, rh)

    def save_edits_crop(self, x, y, w, h, rw, rh):
        a = open(self.location, 'r')
        list_of_lines = a.readlines()  # /n split

        n = 0
        new_line = None
        x_row = None
        arr_n = self.arr

        for line in list_of_lines:  # /find the last name
            arr = line.split()
            if len(arr) > 3:

                if self.arr[0] == arr[0]:
                    if x == "":
                        x_row = n
                    else:
                        arr[1] = x
                        arr[2] = y
                        arr[3] = w
                        arr[4] = h
                        arr[5] = rw
                        arr[6] = rh
                        x_row = n
                        arr_n = arr
                        new_line = ' '.join(map(str, arr))
                    continue
            n += 1
        if new_line is None:
            del list_of_lines[x_row]
            self.rewrite_lines(list_of_lines)
            del self

        else:
            list_of_lines[x_row] = new_line + "\n"  # set new line name
            self.rewrite_lines(list_of_lines)
            self.arr = arr_n

            self.cropping_area_create()
            self.text_create()

    def rewrite_lines(self, list_of_lines):
        a = open(self.location, 'w')
        a.writelines(list_of_lines)  # save file with new name
        a.close()

    def text_create(self):
        self.text_item = self.canvas.create_text(self.arr[1], self.arr[2],
                                                 fill="black", font="Times 10 bold",
                                                 text=self.arr[0], tag=self.arr[0] + "x")

        r = self.canvas.create_rectangle(self.canvas.bbox(self.text_item), fill="white",
                                         tag=self.arr[0] + "b")  # crate background
        self.canvas.tag_lower(r, self.text_item)  # set layout

        self.text_bind(self.arr[0] + "x")

    def text_bind(self, key):
        self.binding = self.canvas.tag_bind(key, "<Button-1>", self.edit_text_begin)

    def text_unbind(self):
        self.canvas.unbind("<Button 1>", self.binding)

    def edit_text_begin(self, args=None):
        self.textvar.set(self.arr[0])
        e = Entry(main, width=10, textvariable=self.textvar, bd=0, highlightthickness=1, bg="white")
        e.selection_range(0, "end")

        # a = self.canvas.create_text(self.arr[1],self.arr[2]-25,
        # fill="black",font="Times 10 bold",text = self.arr[0],tag = self.arr[0]+"a")

        # r = self.canvas.create_rectangle(self.canvas.bbox(self.text_item),fill="white",
        # tag = self.arr[0]+"a") # crate background

        # self.canvas.tag_lower(r,a) # set layout

        self.canvas.create_window(self.arr[1], self.arr[2], window=e, tags=self.arr[0] + "a", anchor="nw")
        e.focus_set()
        e.bind("<Return>", self.edit_text_end)
        e.bind("<Escape>", self.edit_text_cancel)
        e.bind("<Button-3>", self.edit_text_end)

    def edit_text_cancel(self, args):
        self.canvas.delete(self.arr[0] + "a")
        args.widget.destroy()

    def edit_text_end(self, args):
        self.edit_text_cancel(args)
        text = self.textvar.get()
        self.save_edits_text(text, args)

    def save_edits_text(self, text, args):
        a = open(self.location, 'r')
        list_of_lines = a.readlines()  # /n slit

        x = 0
        err = 0
        x_row = None
        new_line = None
        for line in list_of_lines:  # /find the last name
            arr = line.split()
            if len(arr) > 3:
                if text == arr[0] or text == "":  # if the same value was set
                    self.edit_text_cancel(args)
                    err = 1
                    continue

                elif self.arr[0] == arr[0]:
                    arr[0] = text
                    x_row = x
                    new_line = ' '.join(map(str, arr))
            x += 1

        if err == 0:
            list_of_lines[x_row] = new_line + "\n"  # set new line name

            a = open(self.location, 'w')
            a.writelines(list_of_lines)  # save file with new name
            a.close()

            self.canvas.itemconfigure(self.arr[0] + "x", text=text,
                                      tags=text + "x")
            self.canvas.delete(self.arr[0] + "b")
            r = self.canvas.create_rectangle(self.canvas.bbox(self.text_item), fill="white",
                                             tag=text + "b")  # crate background
            self.canvas.tag_lower(r, self.text_item)  # set layout

            self.text_unbind()
            self.arr[0] = text  # edit self.name
            self.text_bind(text + "x")

        else:
            print("name has already used!")

    def edit_color(self):  # no usage
        self.other = colorchooser.askcolor(title="Choose color")
        # button.configure(bg=color_code[-1])
        # print(color_code[-1])


class Functions:
    def __init__(self):
        self.height = None
        self.width = None
        self.image = None
        self.data = None

        self.canvas = Canvas(main)

        vbar1 = Scrollbar(main, orient="vertical")
        vbar1.pack(side="right", fill=BOTH)
        vbar1.config(command=self.canvas.yview)

        hbar1 = Scrollbar(main, orient="horizontal")
        hbar1.pack(side="bottom", fill=BOTH)
        hbar1.config(command=self.canvas.xview)

        self.canvas.config(width=300, height=300)
        self.canvas.config(xscrollcommand=hbar1.set, yscrollcommand=vbar1.set)
        self.canvas.bind("<ButtonPress-2>", self.scroll_start)
        self.canvas.bind("<B2-Motion>", self.scroll_move)
        self.canvas.bind_all("<MouseWheel>", self.scrollbar_move_y)
        self.canvas.bind_all("<Shift-MouseWheel>", self.scrollbar_move_x)
        self.canvas.bind_all("<Control-c>", self.crop)
        self.canvas.pack(side="right", expand=True, fill="both")

    def scroll_start(self, args):
        self.canvas.scan_mark(args.x, args.y)

    def scroll_move(self, args):
        self.canvas.scan_dragto(args.x, args.y, gain=1)

    def scrollbar_move_y(self, args):
        self.canvas.yview_scroll(int(-2 * (args.delta / 120)), "units")

    def scrollbar_move_x(self, args):
        self.canvas.xview_scroll(int(-2 * (args.delta / 120)), "units")

    def open_data(self):
        self.data = fd.askopenfilename(initialdir=os.getcwd(), filetypes=[('Data files', '*.dat')], title='Open dat')
        self.show_crop()

    def open_image(self):
        self.image = Image.open(
            fd.askopenfilename(initialdir=os.getcwd(), filetypes=[('Image Files', '*.png')], title='Open image'))
        self.width, self.height = self.image.size

        self.pop_up_crop()

    def crop(self, args=None):

        if self.image and self.data:
            run(self.image, self.data)
        else:
            print("There is not such file")

    @staticmethod
    def help():
        print("Shortcuts:")
        print("scroll vertical", " - scroll_wheel")
        print("scroll horizontal", " - shift + scroll_wheel")
        print("move", " - scroll_wheel_click")
        print("crop", " - ctrl + c")

    def show_crop(self):
        a = open(self.data, 'r')
        for line in a.readlines():
            arr = line.split()
            if len(arr) >= 5 and '#' not in arr[0] and "\n" not in arr[0]:  # empty line
                Area(self.canvas, self.data, arr)  # canvas, file direction
        a.close()

    def show_image(self):
        self.canvas.delete("all")
        # self.canvas.configure(scrollregion=(-50, -50, self.width + 50, self.height + 50))
        img = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor="nw", image=img)
        self.canvas.image = img

    def pop_up_crop(self):
        if self.image is not None:
            self.show_image()
        else:
            print("There is no loaded image file")
        if self.data is not None:
            self.show_crop()
        else:
            print("There is no loaded data file")


if __name__ == '__main__':
    main = Tk()
    main.title('Image cropper')
    main.iconbitmap('Icon.ico')

    f = Functions()

    # menu
    upMenu = Menu(main)

    menuFile = Menu(upMenu, tearoff=0)
    menuFile.add_command(label="Open dat", command=f.open_data)
    menuFile.add_command(label="Open image", command=f.open_image)
    menuFile.add_command(label="Crop", command=f.crop)
    upMenu.add_cascade(label="File", menu=menuFile)

    menuEdit = Menu(upMenu, tearoff=0)
    menuEdit.add_command(label="Refresh layers", command=f.pop_up_crop)
    upMenu.add_cascade(label="Edit", menu=menuEdit)

    menuHelp = Menu(upMenu, tearoff=0)
    menuHelp.add_command(label="Help shortcuts", command=f.help)
    upMenu.add_cascade(label="Help", menu=menuHelp)

    main.config(menu=upMenu)

    mainloop()
