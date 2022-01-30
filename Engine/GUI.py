import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.colorchooser import *

import time

from . import livereloader
from . import httpserver
#from Tkinter import *

import http.server
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import time


class Window:
	def __init__(self):

		self.icon_path = './Engine/Assets/icon.png'
		self.icon_height = int(108/2)
		self.icon_width = int(192/2)
		self.curr_frame = None
		#self.parent = self
		self.preview_frames = {}
		self.project = None
		self.ck_img = None
		self.videos = {}
		self.window_objs = {}
		self.selected = None
		self.curr_time = 0
		#Initialize main window
		self.root = Tk()
		self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.root.title("PyMVC")
		self.root.geometry("1366x768")
		self.root.minsize(1366,768)
		self.root.config(bg="#232323")

		#Initialize menubar
		self.menubar = Menu(self.root, bg='#303030', fg='white', activebackground='#202020', activeforeground='white', bd=0)
		self.file = Menu(self.menubar, bg='#303030', fg='white', activebackground='#202020', activeforeground='white', bd=0)
		self.file.add_command(label="New")
		self.file.add_command(label="Open")
		self.file.add_command(label="Save")
		self.file.add_separator()
		'''self.file.add_command(label="Import", command=self.import_video)
		self.file.add_command(label="Export/Render/Bake", command=self.export) #this will do the magic'''
		self.menubar.add_cascade(label="File", menu=self.file)

		self.edit = Menu(self.menubar, bg='#303030', fg='white', activebackground='#202020', activeforeground='white', bd=0)
		self.edit.add_command(label="Undo")
		self.edit.add_command(label="Redo")
		self.edit.add_command(label="Copy")
		self.edit.add_command(label="Paste")
		self.menubar.add_cascade(label="Edit", menu=self.edit)

		self.root.config(menu=self.menubar)

		#Arrange Window
		self.mainpanel = PanedWindow(orient='vertical', bg='black', bd=0, sashwidth=5)
		self.mainpanel.pack(fill= BOTH, expand=True)

		#Initialize tabs
		self.notebook = ttk.Notebook(self.mainpanel)
		self.notebook.pack(pady=100, expand=True, fill=BOTH)

		self.frame1 = PanedWindow(self.notebook, orient="vertical",bg="black", bd=0)
		self.frame2 = PanedWindow(self.notebook, orient="vertical",bg="black", bd=0)
		self.frame3 = PanedWindow(self.notebook, orient="vertical",bg="black", bd=0)
		self.frame4 = PanedWindow(self.notebook, orient="vertical",bg="black", bd=0)
		self.frame5 = PanedWindow(self.notebook, orient="vertical",bg="black", bd=0)

		Label(self.frame2, text="Coming soon!", fg="white", bg="black").grid(column=0,row=0,padx=30,pady=30)
		Label(self.frame3, text="Coming soon!", fg="white", bg="black").grid(column=0,row=0,padx=30,pady=30)
		Label(self.frame4, text="Coming soon!", fg="white", bg="black").grid(column=0,row=0,padx=30,pady=30)
		Label(self.frame5, text="Coming soon!", fg="white", bg="black").grid(column=0,row=0,padx=30,pady=30)
		#self.frame2 = PanedWindow(self.notebook, background="green")

		self.frame1.pack(fill="both", expand=True)
		self.frame2.pack(fill="both", expand=True)

		self.style = ttk.Style(self.root)
		self.style.theme_create( "testStyle", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [0, 0, 0, 0], "background":"black", "bd":"0","highlightthickness":"0" } },
        "TNotebook.Tab": {
            "configure": {"padding": [100, 10], "background": "#202020", "foreground":"white" },
            "map":       {"background": [("selected", "#303030")],
                          "expand": [("selected", [0, 0, 0, 0])] } } } )
		self.style.configure("testStyle", foreground="white", background="#303030", activebackground='#202020', activeforeground='white', font=('./Engine/Assets/Font/Roboto/Roboto-Regular',11))
		self.style.theme_use("testStyle")

		self.notebook.add(self.frame1, text="General")
		self.notebook.add(self.frame2, text="Styling")
		self.notebook.add(self.frame3, text="Models")
		self.notebook.add(self.frame4, text="Component Builder")
		self.notebook.add(self.frame5, text="Routes")

		self.top_panel = PanedWindow(self.frame1,orient='horizontal', bg='black', bd=0, sashwidth=5)
		self.mainpanel.add(self.notebook)
		self.frame1.add(self.top_panel, height=500)

		self.bot_panel = PanedWindow(self.frame1,orient='horizontal', bg='black', bd=0, sashwidth=5)
		self.frame1.add(self.bot_panel)

		self.effects_panel = Frame(bg='#232323')
		self.top_panel.add(self.effects_panel, width=550)

		self.preview_panel = Frame(bg='#232323')
		self.top_panel.add(self.preview_panel)

		self.left_bot = Frame(self.bot_panel, bg='#232323')
		self.bot_panel.add(self.left_bot, width=350)
		self.import_panel = Frame(self.left_bot, bg='#303030')
		self.import_panel.pack(padx=(10,10), pady=(10,10), anchor=NW)

		self.tracks_panel = Frame(bg='#232323')

		self.bot_panel.add(self.tracks_panel)
		self.project_panel = Canvas(self.tracks_panel, width=(1366-390), height=(768-520), bg='#303030', highlightthickness=0)
		self.proj_label = Label(self.project_panel, text="Project", font=("Roboto", 12), width=(1366-330), fg='#eeeeee', bg="#303030", anchor=NW)

		self.video_tracks_panel = Frame(self.project_panel, width=(1366-390), height=(768-568)/2, bg='#3A3A3A')
		self.audio_tracks_panel = Frame(self.project_panel, width=(1366-390), height=(768-568)/2, bg='#3A3A3A')
		b = Button(self.effects_panel, text="Do something", relief=GROOVE, bg='#3A3A3A', fg='white', padx=20, pady=10, activebackground='#202020', activeforeground='white', bd=0, command= lambda: (self.OpenTestModal()),highlightthickness=0, width=50)
		b.pack()
		self.serverButton = Button(self.effects_panel, text="Start Server", relief=GROOVE, bg='#3A3A3A', fg='white', padx=20, pady=10, activebackground='#202020', activeforeground='white', bd=0, command= lambda: (self.StartServer()),highlightthickness=0, width=50)
		self.serverButton.pack()

		self.root.iconphoto(False, PhotoImage(file=self.icon_path))

	def OpenTestModal(self):
		testModal = Toplevel(self.root, bg="#303030", pady=10)
		variable = StringVar(testModal)
		options_list = ["Option 1", "Option 2", "Option 3", "Option 4"]
		variable.set("one")
		w = OptionMenu(testModal, variable, *options_list)
		w.config(bg="#3A3A3A", fg="white", activebackground="#202020", activeforeground="white", highlightthickness=0, relief=GROOVE, bd=0, padx=10, pady=20)
		w.pack()
		cc = askcolor()
		print(cc)
		b = Button(testModal, text="Close", relief=GROOVE, bg='#3A3A3A', fg='white', padx=20, pady=10, activebackground='#202020', activeforeground='white', bd=0, command= lambda: (testModal.destroy()),highlightthickness=0, width=50)
		b.pack()

	def StartServer(self):
		self.webServer = httpserver.HttpServer()
		self.serverButton.pack_forget()
		self.serverButton = Button(self.effects_panel, text="Stop Server", relief=GROOVE, bg='#3A3A3A', fg='white', padx=20, pady=10, activebackground='#202020', activeforeground='white', bd=0, command= lambda: (self.StopServer()),highlightthickness=0, width=50)
		self.serverButton.pack()

	def StopServer(self):
		self.webServer.stop()
		self.serverButton.pack_forget()
		self.serverButton = Button(self.effects_panel, text="Start Server", relief=GROOVE, bg='#3A3A3A', fg='white', padx=20, pady=10, activebackground='#202020', activeforeground='white', bd=0, command= lambda: (self.StartServer()),highlightthickness=0, width=50)
		self.serverButton.pack()

	def on_closing(self):
		print("Exiting")
		livereloader.running = False
		time.sleep(1)
		#x.join()
		self.root.destroy()