import os
from tkinter import filedialog as fd
from tkinter import *
from PIL import Image,ImageTk


main = Tk()
class Crop:
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
            if len(arr) <= 3 or arr[0]=="#": # emty line
                pass
            elif len(arr) == 5: # 
                Crop.saveCrop(img, arr[0], Crop.getBox(arr))
            elif len(arr) == 6:
                numOfFrames = int(arr[5])
                for frameIndex in range(0, numOfFrames):
                    Crop.saveCrop(img, arr[0] + '_f' + str(frameIndex), Crop.getBox(arr, frameIndex))
            elif len(arr) == 7:
                numOfFrames = int(arr[5])
                numOFHFrames = int(arr[6])
                for frameHIndex in range(0, numOFHFrames):
                    for frameIndex in range(0, numOfFrames):
                        Crop.saveCrop(img, arr[0] + '_f' + str(frameIndex)+str(frameHIndex), Crop.getBox(arr, frameIndex, frameHIndex))
        a.close()

class Text:
    def __init__(self, canvas, text, x, y, location):
        self.textvar = StringVar()

        self.location = location
        self.canvas = canvas
        self.x = int(x)
        self.y = int(y)
        self.text = str(text)
        
        self.a=canvas.create_text(self.x,self.y,fill="black",font="Times 10 bold",text=self.text,tag = self.text+"x")
        self.r = self.canvas.create_rectangle(self.canvas.bbox(self.a),fill="white", tag = self.text+"b") # crate background
        self.canvas.tag_lower(self.r,self.a) # set layout
        
        self.bind(self.text+"x")
        
        #self.canvas.tag_bind(str(self.name)+"x","<Enter>", self.tooltip_show)
        #self.canvas.tag_bind(str(self.name)+"x","<Leave>", self.tooltip_hide)

    def bind(self,key):
        self.binding = self.canvas.tag_bind(key,"<Button-1>", self.edit_begin)
        
    def unbind(self):
        self.canvas.unbind("<Button 1>", self.binding)
        
    def edit_begin(self,args=None):
        self.textvar.set(self.text) 
        e = Entry(main, width=10, textvariable=self.textvar, bd=0,highlightthickness=1, bg="white") 
        e.selection_range(0, "end")
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
            
            self.unbind()
            self.text = text #edit self.name
            self.bind(text+"x")

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
        self.data =  fd.askopenfilename(initialdir=os.getcwd(), filetypes =[('Data files', '*.dat')],
                                        title='Open dat')
        self.show_crop()
        
    def open_image(self):
        self.image = Image.open(fd.askopenfilename(initialdir=os.getcwd(), filetypes =[('Image Files', '*.png')],
                                        title='Open image'))
        self.width, self.height = self.image.size
        
        self.edit_crop()
        
    def crop(self):
        try:
            self.image
            self.dat
        except:
            print("There is not such file")
        Crop.run(self.image,self.data,self.width,self.height)
        
    def save_data(self):##
        pass
    
    def help(self):
        print("Shortcuts:")
        print("scroll vertical"," - scroll_wheel")
        print("scroll hortical"," - shift + scroll_wheel")
        print("move"," - scroll_wheel_click")
        print("zoom"," - ctrl + scroll_wheel")

    # copied
    


        

    
    def show_crop(self):
        a = open(self.data, 'r')
        for line in a.readlines():
            arr = line.split()
            if len(arr) == 0 or "#" in arr[0]: # emty line
                pass
            if len(arr) == 5: # if array is only one block ()
                array = Crop.getBox(arr)
                self.canvas.create_rectangle(array)
                Text(self.canvas, arr[0], arr[1], arr[2], self.data) #canvas, name, x, y, text
                #print(arr[0],getBox(arr))
                
            if len(arr) == 6: # if array is repeated in lines |||
                numOfFrames = int(arr[5])
                for frameIndex in range(0, numOfFrames):
                    array = Crop.getBox(arr, frameIndex)
                    self.canvas.create_rectangle(array)
                    Text(self.canvas, arr[0], arr[1], arr[2], self.data) #canvas, name, x, y, text
                    #print(arr[0] + '_f' + str(frameIndex),Crop.getBox(arr, frameIndex))
                    
            if len(arr) == 7: # if array is repeated in lines and rows -_
                numOfFrames = int(arr[5])
                numOFHFrames = int(arr[6])
                for frameHIndex in range(0, numOFHFrames):
                    for frameIndex in range(0, numOfFrames):
                        array = Crop.getBox(arr, frameIndex, frameHIndex)
                        self.canvas.create_rectangle(array)# crate croping
                        Text(self.canvas, arr[0], arr[1], arr[2], self.data) #canvas, name, x, y, text
                        #print(arr[0] + '_f' + str(frameIndex)+str(frameHIndex),Crop.getBox(arr, frameIndex, frameHIndex))
        a.close()

    def show_image(self):
        self.canvas.delete("all")
        self.canvas.configure(scrollregion=(-50,-50,self.width+50,self.height+50))
        img = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0,anchor = "nw",image=img)
        self.canvas.image = img
    def edit_crop(self):##
        self.show_image()
        try:
            self.show_crop()
        except:
            print("Load or generate crop data!###")
        

f = Functions()

#menu
upMenu = Menu(main)

menuFile = Menu(upMenu, tearoff=0)
menuFile.add_command(label="Open dat", command=f.open_data)
menuFile.add_command(label="Open image", command=f.open_image)
menuFile.add_command(label="Crop", command=f.crop)
upMenu.add_cascade(label="File", menu=menuFile)

menuEdit = Menu(upMenu, tearoff=0)
menuEdit.add_command(label="Show croping", command=f.edit_crop)
upMenu.add_cascade(label="Edit", menu=menuEdit)

menuHelp = Menu(upMenu, tearoff=0)
menuHelp.add_command(label="Help shorcuts", command=f.help)
upMenu.add_cascade(label="Help", menu=menuHelp)

main.config(menu=upMenu)



mainloop()
