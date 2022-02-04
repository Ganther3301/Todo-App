import tkinter as tk
from login import *
from home import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class App(ttk.Window):
	def __init__(self):
		super().__init__(themename = "darkly")

		self.resizable(0,0)
		self.attributes('-toolwindow',True)

		self.container = ttk.Frame(self)
		self.canvas = ttk.Canvas(self.container)
		self.scrollbar = ttk.Scrollbar(self.container, orient = 'vertical', command = self.canvas.yview)

		self.scrollbar.pack(side = 'left', fill = 'y')
		self.canvas.pack(side = 'right', fill = 'both')
		self.canvas.configure(yscrollcommand = self.scrollbar.set)
		self.container.pack( fill = 'both', expand = True)
		self.canvas.pack(side = 'right', fill = 'both', expand = True)

		self.frames = {
			Login : 'Login',
			Create : 'Create',
			Home : 'Home',
			List: '',
		}

		self.showFrame(Login)

	def showFrame(self,cont):
		self.frame = cont(self, self.canvas)
		self.frames[List] = db.title
		if self.frames[cont] in ['Home', db.title]:
			self.attributes('-toolwindow', False)
			self.geometry('500x700')
			self.canvas.configure(height = 700, width = 500)
		else:
			self.frame.pack(fill = 'both', expand = True)
			self.frame.update()
			self.canvas.configure(height = self.frame.winfo_reqheight(), width = self.frame.winfo_reqwidth())   

		self.frame.pack(fill = 'both', expand = True)
		self.frame.update()
		
		self.frame.bind(
		  '<Configure>',
		  lambda e: self.canvas.configure(
		      scrollregion = self.canvas.bbox('all')
		      )
		  )

		self.canvas.create_window((0,0), window = self.frame, anchor = 'nw',)
		self.title(self.frames[cont])

	def delFrame(self,cont):
		self.frame.pack_forget()
		self.canvas.delete('all')
		self.showFrame(cont)

if __name__ == '__main__':
	app = App()
	app.eval('tk::PlaceWindow . center')
	app.mainloop()