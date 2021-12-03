import os
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter import *
from PIL import Image,ImageTk





class Crop:
    def create_rectangle(canvas, arr, **kwargs):
        x1,y1,x2,y2 = arr[0],arr[1],arr[2],arr[3]
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            fill = main.winfo_rgb(fill) + (alpha,)
            image = Image.new('RGBA', (x2-x1, y2-y1), fill)
            images = ImageTk.PhotoImage(image)
            cimage =canvas.create_image(x1, y1, image=images, anchor='nw')
        canvas.create_rectangle(x1, y1, x2, y2, **kwargs)
        return cimage
    
    def getBox(arr, frameIndex = 0, frameHIndex = 0):
        w, h = int(arr[3]), int(arr[4])
        x, y = int(arr[1]) + w*frameIndex, int(arr[2])+h*frameHIndex
        return (x, y, x+w, y+h)

    def saveCrop(img, title, box):
        path = os.path.join('./frames/' + title + '.png')
        try:
            croppedImg = img.crop(box)
            croppedImg.save(path)
            print('ok: ' + title)
        except Exception as e:
            print('fail: ' + title + ' -- ' + str(e))
    
    def run(img,dat,w,h):
        try:
            path = os.path.join(os.getcwd(), "frames")
            os.mkdir(path)
        except:
            pass
        a = open(dat, 'r')
        for line in a.readlines():
            arr = line.split()
            if len(arr) <= 3 or "#" in arr[0]: # emty line
                pass
            elif len(arr) <= 7:
                numOfFrames = int(arr[5])
                numOFHFrames = int(arr[6])
                for frameHIndex in range(0, numOFHFrames):
                    for frameIndex in range(0, numOfFrames):
                        Crop.saveCrop(img, arr[0] + '_f' + str(frameIndex)+str(frameHIndex), Crop.getBox(arr, frameIndex, frameHIndex))
        a.close()

class Area:
    def __init__(self, canvas, location, arr):
        #main and editing
        self.location = location
        self.canvas = canvas
        
        #for both
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
        
        self.text = str(self.arr[0])
        self.x = int(self.arr[1])
        self.y = int(self.arr[2])
        
        #for cropping area
        self.xvar = StringVar() #cords x
        self.yvar = StringVar() #cords y
        self.wvar = StringVar() #width
        self.hvar = StringVar() #height
        self.rwvar = StringVar() #repeats w
        self.rhvar = StringVar() #repeats h
        
        
        self.x_click = None
        self.y_click = None
        self.cropping_area_create() #initialize areas
        
        #for text
        self.textvar = StringVar()
        self.text_create() #initialize text
        
        #self.canvas.tag_bind(str(self.name)+"x","<Enter>", self.tooltip_show)
        #self.canvas.tag_bind(str(self.name)+"x","<Leave>", self.tooltip_hide)

    def cropping_area_create(self):
        numOfFrames = int(self.arr[5])
        numOFHFrames = int(self.arr[6])
        for frameHIndex in range(0, numOFHFrames):
            for frameIndex in range(0, numOfFrames):
                array = Crop.getBox(self.arr, frameIndex, frameHIndex)
                #rect = self.canvas.create_rectangle(array)
                rect = Crop.create_rectangle(self.canvas, array, tag = self.text+"rect",fill="green", alpha=.1)
                self.rectangle_bind(rect)# crate croping

    def rectangle_bind(self, rect):
        self.m = Menu(main, tearoff = 0)
        self.m.add_command(label = self.text, state=DISABLED)
        self.m.add_separator()
        self.m.add_command(label ="Edit tile", command = self.edit_cropping_area)
        self.m.add_command(label ="Create new [Ctrl+n]")
        self.m.add_separator()
        self.m.add_command(label ="Delete", command = self.delete)
        
        self.canvas.tag_bind(rect, '<Button-3>', self.right_click_menu)
        
    def right_click_menu(self,args):
        try:
            self.m.tk_popup(args.x_root, args.y_root)
        finally:
            self.m.grab_release()
    def delete(self):
        self.edit_crop_cancel()
        self.save_edits_crop("","","","","","")

        
    def edit_cropping_area(self):
        self.xvar.set(self.x)
        self.yvar.set(self.y)
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
            
        x0 = self.x+30#self.x_click
        y0 = self.y+30#self.y_click - 15
        y1 = self.y+40#self.y_click
        x_change = 85
        data = [[ex, "x0"],[ey, "tile_y0"],[ew, "width"],[eh, "height"],[erw, "repeat_width"],[erh, "repeat_height"]]
        
        self.canvas.create_rectangle([x0-10,y0-10,x0+10+x_change*6,y0+10+25],fill="blue", tag = self.text+"an"+str(6)) #rect around
        for n in range (6):
            this_x = x0+x_change*n
            a = self.canvas.create_text(this_x+25,y0,fill="black",font="Times 10 bold",text = data[n][1],tag = self.text+"an"+str(n))
            r = self.canvas.create_rectangle(self.canvas.bbox(a),fill="white", tag = self.text+"an"+str(n)) # crate background
            self.canvas.tag_lower(r,a) # set layout
            
            w = self.canvas.create_window(this_x, y1, window=data[n][0], tags=self.text+"an"+str(n), anchor="nw")
            
            data[n][0].bind("<Escape>", self.edit_crop_cancel) ###new###
            data[n][0].bind("<Button-3>", self.edit_crop_end)
            data[n][0].bind("<Return>", self.edit_crop_end)
        
        
        data[0][0].selection_range(0, "end")
        data[0][0].focus_set()
    
    def edit_crop_cancel(self, args=None):
        for n in range(7):
            self.canvas.delete(self.text+"an"+str(n))
        self.canvas.delete(self.text+"rect")
        self.canvas.delete(self.text+"b")
        self.canvas.delete(self.text+"x")
        try:
            args.widget.destroy()
        except:
            pass
    
    def edit_crop_end(self, args):
        self.edit_crop_cancel(args)
        
        x=self.xvar.get() or self.x
        y=self.yvar.get() or self.y
        w=self.wvar.get() or self.arr[3]
        h=self.hvar.get() or self.arr[4]
        rw=self.rwvar.get() or self.arr[5]
        rh=self.rhvar.get() or self.arr[6]
        
        self.save_edits_crop(x,y,w,h,rw,rh)
    
    def save_edits_crop(self,x,y,w,h,rw,rh):
    
        a = open(self.location, 'r')
        list_of_lines = a.readlines() #/n split

        n = 0
        new_line = None
        for line in list_of_lines: #/find the last name
            arr = line.split()
            if len(arr)>3:
                    
                if self.text == arr[0]:
                    if x=="":
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
                        new_line = ' '.join(map(str,arr))
                    continue
            n+=1
        if new_line==None:
            del list_of_lines[x_row]
            self.rewrite_lines(list_of_lines)
            del self   
            
        else:
            list_of_lines[x_row] = new_line+"\n" #set new line name
            self.rewrite_lines(list_of_lines)
            self.x=int(x)
            self.y=int(y)
            self.arr= arr_n
            self.cropping_area_create()
            self.text_create()
              
    def rewrite_lines(self,list_of_lines):   
        a = open(self.location, 'w')
        a.writelines(list_of_lines) #save file with new name
        a.close()  
        
        
    def text_create(self):
        self.a = self.canvas.create_text(self.x,self.y,fill="black",font="Times 10 bold",text=self.text,tag = self.text+"x")
        self.r = self.canvas.create_rectangle(self.canvas.bbox(self.a),fill="white", tag = self.text+"b") # crate background
        self.canvas.tag_lower(self.r,self.a) # set layout

        self.text_bind(self.text+"x")
        
    def text_bind(self,key):
        self.binding = self.canvas.tag_bind(key,"<Button-1>", self.edit_begin)
        
    def text_unbind(self):
        self.canvas.unbind("<Button 1>", self.binding)
        
    def edit_begin(self,args=None):
        self.textvar.set(self.text) 
        e = Entry(main, width=10, textvariable=self.textvar, bd=0,highlightthickness=1, bg="white") 
        e.selection_range(0, "end")
        
        #a = self.canvas.create_text(self.x,self.y-25,fill="black",font="Times 10 bold",text = self.text,tag = self.text+"a")
        #r = self.canvas.create_rectangle(self.canvas.bbox(self.a),fill="white", tag = self.text+"a") # crate background
        #self.canvas.tag_lower(r,a) # set layout
        
        w = self.canvas.create_window(self.x, self.y, window=e, tags=self.text+"a", anchor="nw")
        e.focus_set()
        e.bind("<Return>", self.edit_end)
        e.bind("<Escape>", self.edit_cancel)
        e.bind("<Button-3>", self.edit_end)
        
    def edit_color(): #next versions
        self.other = colorchooser.askcolor(title ="Choose color")
        #button.configure(bg=color_code[-1])
        print(color_code[-1])
        
    def edit_cancel(self,args):
        self.canvas.delete(self.text+"a")
        args.widget.destroy()
        
    def edit_end(self,args):
        self.edit_cancel(args)
        text = self.textvar.get()
        self.save_edits(text,args)
        
    def save_edits(self,text,args):
        a = open(self.location, 'r')
        list_of_lines = a.readlines() #/n slit

        x = 0
        err = 0
        for line in list_of_lines: #/find the last name
            arr = line.split()
            if len(arr)>3:
                if text == arr[0]: #if the same value was setted
                    self.edit_cancel(args)
                    err = 1
                    print("name has already used!")
                    
                if self.text == arr[0]:
                    arr[0] = text
                    x_row = x
                    new_line = ' '.join(map(str,arr))
            x+=1
            
        if err == 0:
            list_of_lines[x_row] = new_line+"\n" #set new line name
            
            a = open(self.location, 'w')
            a.writelines(list_of_lines) #save file with new name
            a.close()

            self.canvas.itemconfigure(self.text+"x", text = text, tags=text+"x" )# upravit num na pořadí ve dnu - listu + editovat list
            self.canvas.delete(self.text+"b")
            self.r = self.canvas.create_rectangle(self.canvas.bbox(self.a),fill="white", tag = text+"b") # crate background
            self.canvas.tag_lower(self.r,self.a) # set layout
            
            self.text_unbind()
            self.text = text #edit self.name
            self.text_bind(text+"x")

class Functions:
    def __init__(self):
        self.canvas = Canvas(main)

        vbar1=Scrollbar(main,orient="vertical")
        vbar1.pack(side="right",fill=BOTH)
        vbar1.config(command=self.canvas.yview)
        hbar1=Scrollbar(main,orient="horizontal")
        hbar1.pack(side="bottom",fill=BOTH)
        hbar1.config(command=self.canvas.xview)

        self.canvas.config(width = 300, height = 300)
        self.canvas.config(xscrollcommand=hbar1.set,yscrollcommand=vbar1.set)
        self.canvas.bind("<ButtonPress-2>", self.scroll_start)
        self.canvas.bind("<B2-Motion>", self.scroll_move)
        self.canvas.bind_all("<MouseWheel>", self.scrollbar_move_y)
        self.canvas.bind_all("<Shift-MouseWheel>", self.scrollbar_move_x)
        self.canvas.bind_all("<Control-c>", self.crop)
        self.canvas.pack(side="right",expand=True,fill="both")
    
    def scroll_start(self,args):
        self.canvas.scan_mark(args.x, args.y)

    def scroll_move(self,args):
        self.canvas.scan_dragto(args.x, args.y, gain=1)
        
    def scrollbar_move_y(self,args):
        self.canvas.yview_scroll(int(-2*(args.delta/120)), "units")
        
    def scrollbar_move_x(self,args):
        self.canvas.xview_scroll(int(-2*(args.delta/120)), "units")
        
    def open_data(self):
        self.data =  fd.askopenfilename(initialdir=os.getcwd(), filetypes =[('Data files', '*.dat')], title='Open dat')
        self.show_crop()
        
    def open_image(self):
        self.image = Image.open(fd.askopenfilename(initialdir=os.getcwd(), filetypes =[('Image Files', '*.png')], title='Open image'))
        self.width, self.height = self.image.size
        
        self.edit_crop()
        
    def crop(self,args=None):
        try:
            self.image
            self.data
        except:
            print("There is not such file")
            return

        
        Crop.run(self.image,self.data,self.width,self.height)
        self.end_crop()
        
    def end_crop(self):
        messagebox.showinfo("info", "Cropping Done")
        print("Done")
        
    def loading(self):
        from time import sleep
        from tkinter import ttk
        teams = range(100)
        popup = Toplevel()
        Label(popup, text="Files being downloaded").grid(row=0,column=0)

        progress = 0
        progress_var = DoubleVar()
        progress_bar = ttk.Progressbar(popup, variable=progress_var, maximum=100)
        progress_bar.grid(row=1, column=0)#.pack(fill=tk.X, expand=1, side=tk.BOTTOM)
        popup.pack_slaves()

        progress_step = float(100.0/len(teams))
        for team in teams:
            popup.update()
            sleep(0.1) # lauch task
            progress += progress_step
            progress_var.set(progress)

        return 0
    
    def help(self):
        print("Shortcuts:")
        print("scroll vertical"," - scroll_wheel")
        print("scroll hortical"," - shift + scroll_wheel")
        print("move"," - scroll_wheel_click")
        print("crop"," - ctrl + c")        

    def show_crop(self):
        a = open(self.data, 'r')
        for line in a.readlines():
            arr = line.split()
            if len(arr) >= 5 and not "#" in arr[0] and not "\n" in arr[0] :# emty line
                Area(self.canvas, self.data, arr) #canvas, file direction, 
        a.close()

    def show_image(self):
        self.canvas.delete("all")
        self.canvas.configure(scrollregion=(-50,-50,self.width+50,self.height+50))
        img = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0,anchor = "nw",image=img)
        self.canvas.image = img
        
    def edit_crop(self):
        try:
            self.show_image()
        except:
            pass
            
        try:
            self.show_crop()
        except:
            pass

main = Tk()
main.title('Image cropper')
main.iconbitmap('Icon.ico')

f = Functions()

#menu
upMenu = Menu(main)

menuFile = Menu(upMenu, tearoff=0)
menuFile.add_command(label="Open dat", command=f.open_data)
menuFile.add_command(label="Open image", command=f.open_image)
menuFile.add_command(label="Crop", command=f.crop)
upMenu.add_cascade(label="File", menu=menuFile)

menuEdit = Menu(upMenu, tearoff=0)
menuEdit.add_command(label="Refresh layers", command=f.edit_crop)
upMenu.add_cascade(label="Edit", menu=menuEdit)

menuHelp = Menu(upMenu, tearoff=0)
menuHelp.add_command(label="Help shorcuts", command=f.help)
upMenu.add_cascade(label="Help", menu=menuHelp)

main.config(menu=upMenu)

mainloop()
