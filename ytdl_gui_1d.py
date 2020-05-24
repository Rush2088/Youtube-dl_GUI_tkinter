''' 
YTDL-GUI Version      : 0.1d 
Date                  : 24/05/2020
Written By            : Rashmil Dahanayake
Info                  : GUI to download MP3's using youtube-dl 
Requirements          : Python 3.8 and youtube-dl, 
                        ffmpeg(for mp3 conversion) 

'''

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, ttk
from ytdl_backend import download,validate_urls
from multiprocessing import Process , Queue
import concurrent.futures
import os

window = tk.Tk()
window.title("Youtube MP3 Downloader ")
window.geometry("750x435")
window.minsize(550 ,450)


#global variables
downloadqueue = {}  
status_code=tk.IntVar()
default_dir=tk.StringVar()
status_bar_msg=tk.StringVar()
status_code.set(0)
default_dir.set(os.path.join(os.environ['UserProfile'],'downloads').replace(os.sep, '/'))
status_bar_msg.set('Enter URL to Download')


####### Helper Functions for GUI ############
def Process_execute(event=None):
    global downloadqueue, process, dwn_obj 
    while not downloadqueue == {} :
        _, dwn_obj = downloadqueue.popitem()
        process = Process(target=download, args=(dwn_obj.url, dwn_obj.fid  , dwn_obj.dir )) 
        process.start() 
        dwnld_btn['state'] = 'disabled'
        dwnld_btn['activebackground'] = 'SystemButtonFace'
        #status update - refer func def eloborating tree widget config##
        tree_status_update(dwn_obj, 'Downloading..')
        status_bar_msg.set('Downloading please wait')
        check_dl_procss(dwn_obj)

def check_dl_procss(dwn_obj_current):
    # global dwn_obj
    if not process.is_alive():
        dwnld_btn['state'] = 'normal'
        dwnld_btn['activebackground'] = '#f57476'

        if not (_:=status_code.get()):
            status_bar_msg.set('Download Completed!!!')
            tree_status_update(dwn_obj_current, 'Downloaded')


    else:
        window.after(200, check_dl_procss ,dwn_obj_current) 
        #with additional arguments to after()

def donothing():
    pass
# spare button event handler


def updatetree():
    pass


def process_terminate(event=None):
    process.terminate()
    status_code.set(1)
    dwnld_btn['state'] = 'normal'
    dwnld_btn['activebackground'] = '#f57476'
    # downloadqueue.append(dwn_obj )  # preserving the object
    downloadqueue[dwn_obj.fid ] =dwn_obj   # preserving the object
    status_bar_msg.set('Cancelled')

def dir_select(event=None):
    dir_name = filedialog.askdirectory()
    print("Selected:", dir_name)  # For debugging
    ent_dir_name.delete(0, tk.END)
    ent_dir_name.insert(0, dir_name)

def exit(event):
    window.destroy()


def add(event=None):
    global downloadqueue, process

    def check_procss():
        # global new_obj
        if not process.is_alive():
            # dl_btn['state'] = 'normal'
            print('json check completed')
            process.terminate()
            try:
                e_code, new_obj.name, new_obj.fid ,new_obj.size= queue.get()
            except:
                pass
            # error checking
            if e_code:
                err_msg= 'Invalid url or connection error'
                new_obj.status = 'offline'
                new_obj.dir = err_msg
                status_bar_msg.set(err_msg)
            
            else:
                new_obj.status = 'online'
                status_bar_msg.set('Press Download Button to Continue') 

            tree_status_update(new_obj, new_obj.status)  # either offline or online
            btn_add['state'] = 'normal'

        else:
            window.after(200, check_procss) 
            

    url_= txt_url_name.get()
    save_dir= ent_dir_name.get()
    if not save_dir:
        # save_dir= os.path.join(os.environ['UserProfile'],'downloads').replace(os.sep, '/')
        save_dir=default_dir.get()
    
    
    elif url_:
        print(f"{url_} Added to queue!")# debug
        # queue.insert(END,  url_)     # update tree
        new_obj= downobj(url_, save_dir)
        # downloadqueue.append(new_obj)  # update lsit variable

        x= tree.insert("", 'end', values = new_obj.mainfields()) #iid saved to x
        new_obj.tree_iid=x  # making function compatible
        downloadqueue[new_obj.Xid]= new_obj  # saving to queue dict data type
        print (f'xid {new_obj.Xid} added')

        print(f'x={x}')
        status_bar_msg.set('Verifying URL. Please Wait ..')  # update statusbar
        queue = Queue()
        queue.put(url_)
        process = Process(target=validate_urls, args=(queue,)) 
        process.start() 
        btn_add['state'] = 'disabled'
        # process.join()
        check_procss()
        txt_url_name.delete(0, tk.END)
        txt_url_name.focus()
    else:
        status_bar_msg.set('Enter a valid url')  # update statusbar
        txt_url_name.focus()

def remove_item(event = None):
    global downloadqueue
    selected_items = tree.selection()
    if selected_items:
        for selected_item in selected_items:  
            if  tree.item(selected_item)['values'][1] !="Downloaded"  :         
                xid1 = tree.item(selected_item)['values'][5] 
                print (f'{xid1} was deleted')
                del downloadqueue[xid1]
                
            tree.delete(selected_item)
    
    else:
        status_bar_msg.set('No items selected to delete')


def tree_status_update(dwn_obj1, msg):
    dwn_obj1.status = msg
    tree.delete(dwn_obj1.tree_iid)
    dwn_obj1.tree_iid=tree.insert("", 'end', values = dwn_obj1.mainfields())
    
        
def popup_about(event=None):
    win_popup = tk.Toplevel()
    win_popup.geometry("270x90")
    win_popup.resizable(False, False)
    win_popup.wm_title("About")
    lbl_about = tk.Label(master=win_popup, text="Youtube MP3 Downloader\nRushworks 2020")
    lbl_about.pack(expand=True)
    btn1=ttk.Button(master=win_popup, text='OK', command=win_popup.destroy)
    btn1.pack(expand=True)
    win_popup.grab_set()   # disable other windows
    win_popup.wait_window(window)   # wait till pop up modal close

############ Menubar #############
menubar = tk.Menu(master=window)
FileMenu = tk.Menu(master=menubar, tearoff=False)
menubar.add_cascade(label="File", underline=0, menu=FileMenu)
FileMenu.add_command(label="Save Log", command=donothing, accelerator="Ctrl+N")
FileMenu.add_command(label="Exit", command=donothing, accelerator="Ctrl+W")
FileMenu.add_separator()
FileMenu.add_command(label="Exit", command=window.quit)

EditMenu = tk.Menu(master=menubar, tearoff=False)
menubar.add_cascade(label="Settings", underline=0, menu=EditMenu)
EditMenu.add_command(label="Config",
                     underline=1,
                     command=lambda: print("Goodbye"),
                     accelerator="Ctrl+C")

AboutMenu = tk.Menu(master=menubar, tearoff=False)
menubar.add_cascade(label="Help", underline=0, menu=AboutMenu)
AboutMenu.add_cascade(label="Content Help", command=donothing)
AboutMenu.add_separator()
AboutMenu.add_cascade(label="About", command=popup_about)

# instead of packing using this command to add menubar
window.config(menu=menubar)


class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        # tk.Button.__init__(self,master=master,**kw)
        super().__init__(master=master,**kw)
        self.defaultBackground = self["background"]
        self['width']=70
        self['height']=70
        self['activebackground']='#f57476'
        self['compound'] = 'top'
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground


class downobj:
    ''' download object defineition '''
    Xid =0
    
    def __init__(self,url, savedir):
        self.url = url  # user input - raw url
        self.status='Checking..'  # treeview
        self.fid=''   #download file format
        self.name ='' #windows friendly title
        self.size=''  # in MB
        self.dir = savedir  # user ipout
        self.tree_iid=''  # tree IID reference
        self.Xid=downobj.Xid  #unique ID to indentifty 
        
        downobj.Xid+=1


    def __repr__(self):
        return f"{self.Xid} :{self.url}"
        
    def mainfields(self) :
        return self.url,self.status , self.name ,self.size ,self.dir,self.Xid

class RightClick:
    def __init__(self, master):
        '''if self.tree_item:
         create a popup menu '''
        self.tree_item = ''

        self.aMenu = tk.Menu(master, tearoff=0)
        # self.aMenu.add_command(label='Delete Entry', command=self.delete)
        self.aMenu.add_command(label='Delete Entry', command=remove_item)
        self.aMenu.add_command(label='Explore Folder', command=self.open_dir)

 
    def open_dir(self):
        if self.tree_item:
            path1= tree.item(self.tree_item)['values'][4]  # pathvariable
            print(f'opening folder {path1}')
            os.system(f'start {os.path.realpath(path1)}')


    def popup(self, event):
        # self.tree_item = tree.focus()
        selected = tree.selection()

        if  selected:
            print (f'{len(selected)} iems selected')
            if len(selected) <2 and tree.item(selected)['values'][1] !="Downloaded" :
                self.aMenu.entryconfig(1, state="disabled")  # disable child item
            self.aMenu.post(event.x_root, event.y_root)


#define main layout frames
frm_Main = tk.Frame(master=window, bg='#faeaea', relief=tk.FLAT, borderwidth=2)
frm_RIBBON = tk.Frame(master=frm_Main, relief=tk.GROOVE, borderwidth=2)
frm_TOP = tk.Frame(master=frm_Main,bg='#ffffff', relief=tk.GROOVE,borderwidth=2)
frm_MID = tk.Frame(master=frm_Main,bg='#ffffff',relief=tk.GROOVE, borderwidth=2)
statusbar = tk.Frame(master=frm_Main,bg='#ffffff',relief=tk.SUNKEN, borderwidth=2)
info_frm =  ttk.LabelFrame(master=frm_RIBBON,text = 'Instructions',
relief=tk.RAISED, borderwidth=2)


frm_Main.pack(expand=False)
frm_RIBBON.pack(side =tk.TOP, fill=tk.BOTH, expand=True)
frm_TOP.pack(side =tk.TOP, fill=tk.BOTH, )
frm_MID.pack(side =tk.TOP,  expand=True) 
info_frm.pack(side =tk.RIGHT,  expand=False, padx=5, pady=2) 
# statusbar.pack(side =tk.BOTTOM,  fill=tk.X, anchor='w',) 

frm_TOP.grid_columnconfigure(1, weight=1)

# using hover button class
download_b2 = tk.PhotoImage(file = r"images/download_b2.png") # preload images
stop_b2 = tk.PhotoImage(file = r"images/stop_b2.png") 
delete_b2 = tk.PhotoImage(file = r"images/delete_b2.png") 

dwnld_btn = HoverButton( master=frm_RIBBON,image=download_b2,text='DOWNLOAD',command=Process_execute)
stp_btn = HoverButton(master=frm_RIBBON,image=stop_b2,text='STOP',command=process_terminate)
del_btn= HoverButton(master=frm_RIBBON,image=delete_b2,text='DELETE', command=remove_item)


info_lbl = tk.Label(master=info_frm,
            text ='1. Paste URL  \n2. Select Folder  \n3. Press Add button \n4. Press Download Button    '
            ,justify='left', anchor='e')

info_lbl.configure(font="Arial 10")            

dwnld_btn.pack(side="left", fill="both", expand=False,)
stp_btn.pack(side="left", fill="both", expand=False, )
del_btn.pack(side="left", fill="both", expand=False,)
info_lbl.pack(side="right", fill="both", expand=True, pady=2, padx=2)
# temp_btn.pack(side="right", fill="both", expand=True)

#status bar
lbl_status_txt = tk.Label(master=window, textvariable=status_bar_msg, bd=2, relief=tk.SUNKEN, anchor=tk.W)
lbl_status_txt.pack( side=tk.BOTTOM,fill=tk.X)



#TOP Frame Widgets
lbl_url_name = ttk.Label(master=frm_TOP, text=f'{"Youtube Url":<14}:')
txt_url_name = ttk.Entry(master=frm_TOP)

btn_add = ttk.Button(master=frm_TOP, text="Add",width=10, command=add)
btn_add.grid(row=0, column=5, padx=8, pady=5, sticky='e')
lbl_dir_name = ttk.Label(master=frm_TOP,  text=f'{"Select Folder":<14}:')
ent_dir_name = ttk.Entry(master=frm_TOP)
btn_browse = ttk.Button(master=frm_TOP, text="Browse...", width=10,command=dir_select)

lbl_url_name.grid(row=0, column=0, padx=8, pady=5 , sticky='w')                      
txt_url_name.grid(row=0, column=1, columnspan=4, pady=5 , sticky='ew')
lbl_dir_name.grid(row=1, column=0, padx=8, pady=5 , sticky='w')
ent_dir_name.grid(row=1, column=1, columnspan=4, pady=5 , sticky='ew')
btn_browse.grid(row=1, column=5, padx=8, pady=5, sticky='e')

ent_dir_name.insert(tk.END, default_dir.get())


tree=ttk.Treeview(master=frm_MID)
tree.grid(column=0, row=0, sticky='nsew')
ysb = ttk.Scrollbar(master=frm_MID,  orient ="vertical",  command = tree.yview) 
ysb.grid(column=1, row=0, sticky='ns')
xsb = ttk.Scrollbar(master=frm_MID,  orient ="horizontal",  command = tree.xview) 
xsb.grid(column=0, row=1, sticky='ew')

frm_MID.grid_columnconfigure(0, weight=1)
frm_MID.grid_rowconfigure(0, weight=1)
tree["yscroll"] = ysb.set
tree["xscroll"] = xsb.set

tree["columns"] = ("1", "2", "3","4","5","6")
tree.column('#0', width =1,anchor ='se',stretch='no') #right align

tree.column("1", width = 250, anchor ='w',stretch='no') 
tree.column("2", width = 70, anchor ='w',stretch='no') 
tree.column("3", width = 250, anchor ='w',stretch='no') 
tree.column("4", width = 60, anchor ='c',stretch='no') 
tree.column("5", width = 150, anchor ='w',stretch='no') 
tree.column("6", width = 10, anchor ='w',stretch='no') 

# tree.heading("#0", text ="ID")
tree.heading("1", text ="URL") 
tree.heading("2", text ="Status") 
tree.heading("3", text ="Name") 
tree.heading("4", text ="Size") 
tree.heading("5", text ="Folder") 
tree.heading("6", text ="Xid") 

tree["displaycolumns"]= ("1","2","3","4","5")

def OnDoubleClick(event):
    item = tree.selection()[0]
    # print("you clicked on", tree.item(item,"text"))   # to get index
    print("you clicked on", tree.item(item,"values")[0])   # specific field
   
    

#key bindings
tree.bind("<Double-1>", OnDoubleClick)     # treeview specific
tree.bind("<Delete>", remove_item)
window.bind("<Return>", add)  # overall window
window.bind('<Control-q>', lambda e:window.destroy())   
rclick = RightClick(window)
tree.bind('<Button-3>', rclick.popup)


if __name__ == "__main__":
    window.mainloop()
    
