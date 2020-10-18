from tkinter import *
from tkinter import ttk
from tkinter import font,filedialog,messagebox,colorchooser
from tkinter.filedialog import askopenfilename,asksaveasfilename
import os
root=Tk()
root.title("Notepad")
root.geometry("600x400")
root.wm_iconbitmap("icon.ico")

menubar=Menu(root)
#filemenu
def NewFile():
    global file
    root.title("Untitled-Notepad")
    file=None
    text_editor.delete(1.0,END)

def OpenFile():
    #a filedialouge should be open
    file=askopenfilename(defaultextension=".txt",filetype=[("Allfiles","*.*"),("Text Document","*.*")])
    if file==" ":
        file=None
    else:
        root.title(os.path.basename(file)+" - Notepad")
        text_editor.delete(1.0,END)
        f=open(file,"r")
        text_editor.insert(1.0,f.read())
        f.close()

def SaveasFile():
    global file
    if file==None:
        file=asksaveasfilename(initialfile="Untitled.txt",defaultextension=".txt",filetype=[("Allfiles","*.*"),("Text Document","*.*")])
        if file=="":
            file=None
        else:
            f=open(file,"w")
            f.write(text_editor.get(1.0,END))
            f.close()
            root.title(os.path.basename(file)+" - Notepad")
    else:
        f=open(file,"w")
        f.write(text_editor.get(1.0,END))
        f.close()
filemenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="File",menu=filemenu)
filemenu.add_command(label="New",compound=LEFT,accelerator="Ctrl+N",command=NewFile)
filemenu.add_command(label="Open",compound=LEFT,accelerator="Ctrl+O",command=OpenFile)
filemenu.add_command(label="Save",compound=LEFT,accelerator="Ctrl+S")
filemenu.add_command(label="Save As",compound=LEFT,accelerator="Ctrl+Sfift+S",command=SaveasFile)
filemenu.add_command(label="Close",compound=LEFT,accelerator="Alt+F4")
filemenu.add_command(label="Exit",compound=LEFT,accelerator="Ctrl+Q",command=root.destroy)

#editmenu
editmenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="Edit",menu=editmenu)
editmenu.add_command(label="Undo",compound=LEFT,accelerator="Ctrl+Z",command=lambda:text_editor.event_generate("<<Undo>>"))
editmenu.add_command(label="Redo",compound=LEFT,accelerator="Ctrl+Shift+Z",command=lambda:text_editor.event_generate("<<Reo>>"))
editmenu.add_command(label="Cut",compound=LEFT,accelerator="Ctrl+X",command=lambda:text_editor.event_generate("<<Cut>>"))
editmenu.add_command(label="Copy",compound=LEFT,accelerator="Ctrl+C",command=lambda:text_editor.event_generate("<<Copy>>"))
editmenu.add_command(label="Paste",compound=LEFT,accelerator="Ctrl+V",command=lambda:text_editor.event_generate("<<Paste>>"))
editmenu.add_command(label="Select All",compound=LEFT,accelerator="Ctrl+A",command=lambda:text_editor.event_generate("<<Select>>"))
editmenu.add_command(label="Clear All",compound=LEFT,accelerator="Ctrl+Alt+Shift",command=lambda:text_editor.delete(1.0,END))

def find_fun():
    def find():
        word=find_input.get()
        text_editor.tag_remove("match",1.0,END)
        matches=0
        if word:
            start_pos="1.0"
            while True:
                start_pos=text_editor.search(word,start_pos,stopindex=END)
                if not start_pos:
                    break
                end_pos=f"{start_pos}+{len(word)}c"
                text_editor.tag_add("match",start_pos,end_pos)
                matches+=1
                start_pos=end_pos
                text_editor.tag_config('match',foreground='red',background='yellow')
                
    def replace():
        word=find_input.get()
        replace_text=replace_input.get()
        content=text_editor.get(1.0,END)
        new_content=content.replace(word,replace_text)
        text_editor.delete(1.0,END)
        text_editor.insert(1.0,new_content)
        
    find_popup=Toplevel()
    find_popup.geometry("450x200")
    find_popup.title("Find Word")
    find_popup.resizable(0,0)

    find_frame=ttk.LabelFrame(find_popup,text="Find and Replace Words")
    find_frame.pack(pady=20)

    text_find=ttk.Label(find_frame,text="Find")
    text_replace=ttk.Label(find_frame,text="Replace")

    find_input=ttk.Entry(find_frame,width=30)
    replace_input=ttk.Entry(find_frame,width=30)

    find_button=ttk.Button(find_frame,text="Find",command=find)
    replace_button=ttk.Button(find_frame,text="Replace",command=replace)

    text_find.grid(row=0,column=0,padx=4,pady=4)
    text_replace.grid(row=1,column=0,padx=4,pady=4)

    find_input.grid(row=0,column=1,padx=4,pady=4)
    replace_input.grid(row=1,column=1,padx=4,pady=4)
    
    find_button.grid(row=2,column=0,padx=8,pady=4)
    replace_button.grid(row=2,column=1,padx=8,pady=4)

    
editmenu.add_command(label="Find",compound=LEFT,accelerator="Ctrl+F",command=find_fun)

#<----------viewmenu-------------------------------------------------->
show_toolbar=BooleanVar()
show_toolbar.set(True)
show_status_bar=BooleanVar()
show_status_bar.set(True)
def hide_toolbar():
    global show_toolbar
    if show_toolbar:
        toolbar.pack_forget()
        show_toolbar=False
    else:
        text_editor.pack_forget()
        status_bar.pack_forget()
        toolbar.pack(side=TOP,fill=X)
        text_editor.pack(fill=BOTH,expand=YES)
        status_bar.pack(side=BOTTOM)
        show_toolbar=True
    
def hide_statusbar():
    global show_status_bar
    if show_status_bar:
        status_bar.pack_forget()
        show_status_bar=False
    else:
        status_bar.pack(side=BOTTOM)
        show_status_bar=True

viewmenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="View",menu=viewmenu)
viewmenu.add_checkbutton(label="Tool Bar",onvalue=True,offvalue=0,compound=LEFT,command=hide_toolbar)
viewmenu.add_checkbutton(label="Status Bar",onvalue=True,offvalue=0,compound=LEFT,command=hide_statusbar)


#<-----------------------------colormenu------------------------------>
colormenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="Color",menu=colormenu)
theme_choose=StringVar()

def change_theme():
    get_theme=theme_choose.get()
    color_tuple=color_dict.get(get_theme)
    fg_color,bg_color=color_tuple[0],color_tuple[1]
    text_editor.config(bg=bg_color,fg=fg_color)
color_dict={'Light Default':('#000000','#ffffff'),'Light Plus':('#474747','#e0e0e0'),'Dark':('#c4c4c4','#2d2d2d'),
            'Night Blue':('#ededed','#6b9dc2'),'Red':('#2d2d2d','#ffe8e8')}
for i in color_dict:
    colormenu.add_radiobutton(label=i,compound=LEFT,variable=theme_choose,command=change_theme)

toolbar=Label(root)
toolbar.pack(side=TOP,fill=X)

font_tuple=font.families()
font_family=StringVar()
font_box=ttk.Combobox(toolbar,width=30,textvariable=font_family,state="readonly")
font_box['values']=font_tuple
font_box.grid(row=0,column=0,padx=5,pady=5)
font_box.current(font_tuple.index("Arial"))

size_variable=IntVar()
font_size=ttk.Combobox(toolbar,width=30,textvariable=size_variable,state="readonly")
font_size['values']=tuple(range(8,101,2))
font_size.current(4)
font_size.grid(row=0,column=1,padx=5,pady=5)

bold_btn=ttk.Button(toolbar,text="B")
bold_btn.grid(row=0,column=2,padx=5,pady=5)

italic_btn=ttk.Button(toolbar,text="I")
italic_btn.grid(row=0,column=3,padx=5,pady=5)

underline_btn=ttk.Button(toolbar,text="U")
underline_btn.grid(row=0,column=4,padx=5,pady=5)

font_color_btn=ttk.Button(toolbar,text="FC")
font_color_btn.grid(row=0,column=5,padx=5,pady=5)

align_left_btn=ttk.Button(toolbar,text="AL")
align_left_btn.grid(row=0,column=6,padx=5,pady=5)

align_center_btn=ttk.Button(toolbar,text="AC")
align_center_btn.grid(row=0,column=7,padx=5,pady=5)

align_right_btn=ttk.Button(toolbar,text="AR")
align_right_btn.grid(row=0,column=8,padx=5,pady=5)

#TEXTEDITOR
text_editor=Text(root)
text_editor.config(wrap="word",relief=FLAT)
text_editor.focus_set()
scroll_bar=Scrollbar(root)
scroll_bar.pack(side=RIGHT,fill=Y)
text_editor.pack(fill=BOTH,expand=YES)
scroll_bar.config(command=text_editor.yview)
text_editor.config(yscrollcommand=scroll_bar.set)

status_bar=ttk.Label(root,text="Status Bar")
status_bar.pack(side=BOTTOM)

text_change=False

def change_word(event):
    global text_change
    if text_editor.edit_modified():
        text_change=True
        word=len(text_editor.get(1.0,END).split())
        character=len(text_editor.get(1.0,END).replace(" ",""))-1
        status_bar.config(text=f"Word: {word} Character: {character}")
    text_editor.edit_modified(False)
text_editor.bind("<<Modified>>",change_word)

font_now="Arial"
font_size_now=16

def change_font(event):
    global font_now
    font_now=font_family.get()
    text_editor.configure(font=(font_now,font_size_now))

def change_size(event):
    global font_size_now
    font_size_now=font_size.get()
    text_editor.configure(font=(font_now,font_size_now))
    
font_box.bind("<<ComboboxSelected>>",change_font)
font_size.bind("<<ComboboxSelected>>",change_size)


#print(font.Font(font=text_editor['font']).actual())
def bold_fun():
    text_get=font.Font(font=text_editor['font'])
    if text_get.actual()['weight']=='normal':
        text_editor.configure(font=(font_now,font_size_now,"bold"))
    if text_get.actual()['weight']=='bold':
        text_editor.configure(font=(font_now,font_size_now,"normal"))
bold_btn.configure(command=bold_fun)

def italic_fun():
    text_get=font.Font(font=text_editor['font'])
    if text_get.actual()['slant']=='roman':
        text_editor.configure(font=(font_now,font_size_now,"italic"))
    if text_get.actual()['slant']=='italic':
        text_editor.configure(font=(font_now,font_size_now,"roman"))
italic_btn.configure(command=italic_fun)

def underline_fun():
    text_get=font.Font(font=text_editor['font'])
    if text_get.actual()['underline']==0:
        text_editor.configure(font=(font_now,font_size_now,"underline"))
    if text_get.actual()['underline']==1:
        text_editor.configure(font=(font_now,font_size_now,"normal"))
underline_btn.configure(command=underline_fun)

def color_choose():
    color_var=colorchooser.askcolor()
    text_editor.configure(fg=color_var[1])
font_color_btn.configure(command=color_choose)    

def align_left():
    text_get_all=text_editor.get(1.0,END)
    text_editor.tag_config("left",justify=LEFT)
    text_editor.delete(1.0,END)
    text_editor.insert(INSERT,text_get_all,'left')
align_left_btn.configure(command=align_left)

def align_right():
    text_get_all=text_editor.get(1.0,END)
    text_editor.tag_config("right",justify=RIGHT)
    text_editor.delete(1.0,END)
    text_editor.insert(INSERT,text_get_all,'right')
align_right_btn.configure(command=align_right)

def align_center():
    text_get_all=text_editor.get(1.0,END)
    text_editor.tag_config("center",justify=CENTER)
    text_editor.delete(1.0,END)
    text_editor.insert(INSERT,text_get_all,'center')
align_center_btn.configure(command=align_center)

root.config(menu=menubar)
root.mainloop()
