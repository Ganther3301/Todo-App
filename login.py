import tkinter as tk
from ttkbootstrap.dialogs import Messagebox as show
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import database as db
from home import *

class Login(ttk.Frame):
    def __init__(self, controller, parent):
        super().__init__(parent)

        def checkUsername():
            uname = username.get().strip()
            pword = password.get().strip()
            if uname:
                if not pword:
                    show.show_error('Enter password',title = 'Error',)
                else:
                    valid = db.login(uname,pword)
                    if valid:
                        controller.delFrame(Home)

                    else:
                        show.show_error('Incorrect credentials', title = 'Error')

        self.columnconfigure(0, weight = 1)

        ttk.Label(self, text = "Username",).grid(row = 0, column = 0, padx = 10, pady = (10,0), sticky = tk.EW)
        username = ttk.Entry(self) 
        username.focus()
        username.grid(row = 1, column = 0, sticky = tk.EW, padx = 10, pady = (0,10))

        ttk.Label(self, text = "Password").grid(row = 2, column = 0, padx = 10, pady = (10,0), sticky = tk.NW)
        password = ttk.Entry(self, show = '*')
        password.grid(row = 3, column = 0, sticky = tk.EW, padx = 10, pady = (0,10))

        ttk.Button(self, text = 'Login', bootstyle = LIGHT,command = checkUsername).grid(row = 4, column = 0, padx = 10, pady = 10, sticky = 'nsew')
        ttk.Button(self, text = 'Create New Account', bootstyle = LIGHT,command = lambda: controller.delFrame(Create)).grid(row = 5, column = 0, padx = 10, pady = 10, sticky = 'nsew')

class Create(ttk.Frame):
    def __init__(self, controller, parent):
        super().__init__(parent)

        def createAccount():
            if name.get().strip() and username.get().strip() and password.get().strip() and email.get().strip():
                valid = db.create(name.get().strip(), username.get().strip(), password.get().strip(), email.get().strip())
                if len(password.get().strip()) < 8:
                    show.show_error('Password must have minimum 8 characters!', title = 'Error')
                elif valid:
                    show.ok('Account created successfully!', title = 'Success')
                    controller.delFrame(Login)
                else:
                    show.show_error('Username already exists!', title = 'Error')
            else:
                show.show_error('Fill all the fields!', title = 'Error')

        self.columnconfigure(0, weight = 1)

        ttk.Label(self, text = "Name",).grid(row = 0, column = 0, padx = 10, pady = (10,0), sticky = tk.EW)
        name = ttk.Entry(self) 
        name.focus()
        name.grid(row = 1, column = 0, sticky = tk.EW, padx = 10, pady = (0,10))

        ttk.Label(self, text = "Username",).grid(row = 2, column = 0, padx = 10, pady = (10,0), sticky = tk.EW)
        username = ttk.Entry(self) 
        username.focus()
        username.grid(row = 3, column = 0, sticky = tk.EW, padx = 10, pady = (0,10))

        ttk.Label(self, text = "Email-ID",).grid(row = 4, column = 0, padx = 10, pady = (10,0), sticky = tk.EW)
        email = ttk.Entry(self) 
        email.focus()
        email.grid(row = 5, column = 0, sticky = tk.EW, padx = 10, pady = (0,10))

        ttk.Label(self, text = "Password").grid(row = 6, column = 0, padx = 10, pady = (10,0), sticky = tk.NW)
        password = ttk.Entry(self, show = '*')
        password.grid(row = 7, column = 0, sticky = tk.EW, padx = 10, pady = (0,10))

        ttk.Button(self, text = 'Create Account', bootstyle = LIGHT, command = createAccount).grid(row = 8, column = 0, padx = 10, pady = (2,10), sticky = 'nsew')
        ttk.Button(self, text = 'Back to Login', bootstyle = LIGHT,command = lambda: controller.delFrame(Login)).grid(row = 9, column = 0, padx = 10, pady = (2,10), sticky = 'nsew')
  