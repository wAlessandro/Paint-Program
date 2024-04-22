from tkinter import *
from tkinter import colorchooser,filedialog,messagebox
from PIL import ImageGrab
def savefile():
    path = filedialog.asksaveasfilename(title='Select a directory',defaultextension='.jpg',initialfile='Untitled',
                                        filetypes=[('JPEG','*.jpg')])
    if path:
        print('saved in: '+path)
        x = canvas.winfo_rootx()+6
        y = canvas.winfo_rooty()+6
        img = ImageGrab.grab(bbox=(x,y,x+canvas.winfo_width()-8,y+canvas.winfo_height()-8))
        img.save(path)
        img.show()
def setcolor():
    color = colorchooser.askcolor()
    if color[1] is None:
        brushcolor.append(brushcolor[-1])
    else:
        brushcolor.append(color[1])
def brush(event):
    brush = canvas.create_oval(event.x,event.y,
                               event.x,event.y,
                              fill=brushcolor[-1],outline=brushcolor[-1],width=scale.get(),tag='ball')
    motioncordinates.config(text=f'x:{event.x}\ny:{event.y}')
    if brushcolor[-1] == brushcolor[0]:
        previouscolor.set(brushcolor[0])
    else:
        previouscolor.set(brushcolor[-2])
        pbtn.config(bg=previouscolor.get())
def eraser(event):
    canvas.create_rectangle(event.x,event.y,
                            event.x,event.y,fill=CANVASCOLOR,width=scale.get()*2,outline=CANVASCOLOR,tag='eraser')
def get_cordinates(event):
    motioncordinates.config(text=f"x:{event.x}\ny:{event.y}")
WINDOWWIDHT = 850
WINDOWHEIGHT = 510
WINDOWBACKGROUND = "#B3B3AC"
CANVASCOLOR = "#E8E8E8"
brushcolor = ['black']

window = Tk()
window.title('Paint')
window.geometry(f'{WINDOWWIDHT}x{WINDOWHEIGHT}')
window.resizable(False,False)
window['bg'] = WINDOWBACKGROUND

motioncordinates = Label(window,text='x:\ny:',font=('consolas',12),bd=2,relief='sunken')
motioncordinates.pack(anchor='w',side='bottom')

scroolbarY = Scrollbar(window,orient=VERTICAL,width=15)
scroolbarY.pack(side=RIGHT,fill=Y,anchor='se')
scroolbarX = Scrollbar(window,orient=HORIZONTAL,width=15)
scroolbarX.pack(side=BOTTOM,anchor='n',fill=X)

#BUTTONS----
buttonframe = Frame(window,bg=WINDOWBACKGROUND,bd=3,relief='sunken')
buttonframe.pack(side=LEFT,anchor='se',expand=True)
colors = ['yellow','red',
             'blue','brown',
             'brown','green',
             'pink','orange',
             'purple','black',
             'grey','white',]
colorindex = 0
for row in range(6):
    for column in range(2):
        btn = Button(buttonframe,width=2,height=1,bg=colors[colorindex],relief='sunken',bd=2,command=lambda colorcmd=colors[colorindex]: brushcolor.append(colorcmd))
        btn.grid(row=row,column=column)

        if colorindex < len(colors):
            colorindex+=1
previouscolor = StringVar()
previouscolor.set(brushcolor[0])
pbtn = Button(buttonframe,bg=previouscolor.get(),width=2,height=1,text='↺',font=('System',1),fg='white',command=lambda:brushcolor.append(previouscolor.get()))
pbtn.grid(row=4,column=3)

pickimage = PhotoImage(file='assets/pickcolor.png',width=106,height=50)
coloredit = Button(buttonframe,image=pickimage,width=20,height=18,relief='sunken',command=setcolor)
coloredit.grid(row=5,column=3)

#BRUSHSIZE---
bushsizeframe = Frame(window,bg=WINDOWBACKGROUND)
bushsizeframe.pack(side=LEFT,anchor='s')
scale = Scale(bushsizeframe,from_=10,to=0,bg="#A8A7A3",relief='sunken')
scale.pack()
#CANVASFUNCTIONS---
canvas = Canvas(window,width=WINDOWWIDHT,height=WINDOWHEIGHT,bg=CANVASCOLOR,relief='sunken',bd=4)
canvas.pack(anchor='s',expand=True)

canvas.bind('<Motion>',get_cordinates)
canvas.bind('<B1-Motion>',brush)
canvas.bind('<B3-Motion>',eraser)

canvas.config(yscrollcommand=scroolbarY.set)
canvas.config(xscrollcommand=scroolbarX.set)

#MENUBAR
menubar = Menu(window,)
window.config(menu=menubar)

file = Menu(menubar,tearoff=0)
menubar.add_cascade(label='File',menu=file)
file.add_command(label='New',command=lambda:canvas.delete(ALL))
file.add_command(label='Save',command=savefile)
menubar.add_command(label='Help',command=lambda:messagebox.showinfo(title='help',message='This is a beta version.It may have some bugs.\n\nLeft mouse click to draw\nRight mouse click to erase\n\nIn the bottom left side, you have some buttons which contains basic colors, previous color and the colorpicker.You can adjust the brush width in the size scale box'))

window.mainloop()