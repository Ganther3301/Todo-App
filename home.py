import tkinter as tk
import datetime
import subprocess
from ttkbootstrap.dialogs import Messagebox as show
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import database as db


class Home(ttk.Frame):
    def __init__(self, controller, parent): 
        super().__init__(parent, width = 500, height = 700) 
        self.create_widgets(controller)

    def create_widgets(self, controller):

        def display(event):
            if type(event.widget) == ttk.Labelframe:
                db.title = event.widget['text']
                controller.delFrame(List)
            else:    
                db.title = icns[event.widget]['text']
                controller.delFrame(List)

        def delete():
            db.deleteTitle(self.widgetName)
            controller.delFrame(Home)

        icns = dict() 
        style = tk.ttk.Style(controller)
        ttk.Label(self,text = "Hello " + db.get('name').strip() + '!', anchor = 'w', font = ('Roboto', 20,),).grid(row = 0, padx = 22, pady = (25,25), sticky = tk.EW) 
        btm = ttk.Frame(self)

        icon = ttk.PhotoImage(file = 'add.png')
        add_btn = ttk.Button(btm, text = 'Add New Title', image = icon, compound = 'left',width = 50, bootstyle = 'secondary', command = lambda: self.newEntry(controller))
        add_btn.image = icon
        self.names = db.get('todo')
        i = 0
        for j in self.names:
            if  j!= ' ':
                lb = ttk.Labelframe(btm, text = j, height = 200, bootstyle = 'default') 
                inside = ttk.Frame(lb, height = 15, width = 450,bootstyle = 'secondary')
                icns[inside] = lb
                lb.grid(row = i, column = 1, padx =10, pady = 10, sticky = 'ew')
                inside.grid(row = 0, column = 0, sticky = 'nsew')
                i += 1

        add_btn.grid(row = i, column = 1, padx = 10, pady = 10, sticky = 'ew')

        menu = ttk.Menu(self, tearoff = 0)
        menu.add_command(label = 'Delete', command = delete)

        def do_popup(event):
            try:
                menu.tk_popup(event.x_root, event.y_root)
                if type(event.widget) == ttk.Labelframe:
                    self.widgetName = event.widget['text']
                else:    
                    self.widgetName = icns[event.widget]['text']
            finally:
                menu.grab_release()

        for i in icns:
            i.bind('<Button-1>',display)
            i.bind('<Button-3>',do_popup)
            icns[i].bind('<Button-1>',display)
            icns[i].bind('<Button-3>',do_popup)

        btm.grid(row = 2)
        style.configure('TLabelframe',borderwidth = 0.5)
        style.configure('TLabelframe.Label',font = ('Comforta',10,),)

    def newEntry(self,controller):

        def checkEntry():
            if not title.get().strip():
                show.show_error('Enter Title', title = 'Error')
                top.lift()
                top.focus()
            elif len(title.get().strip()) > 20:
                show.show_error('Maximum 20 characters', title = 'Error')
                top.lift()
                top.focus()
            elif title.get().strip() in self.names:
                show.show_error('Title already exists!', title = "Error")
                top.lift()
                top.focus()
            else:
                db.addTitle(title.get().strip())
                top.destroy()
                self.create_widgets(controller)

        top = ttk.Toplevel(self) 
        top.title('Enter')
        top.attributes('-toolwindow',True)

        ttk.Label(top, text = "Enter Title:",).grid(row = 0, column = 0, padx = 10, pady = (10,0), sticky = tk.EW)
        title = ttk.Entry(top) 
        title.focus()
        title.grid(row = 1, column = 0, sticky = tk.EW, padx = 10, pady = (0,10))

        ttk.Button(top, text = 'Create', bootstyle = LIGHT, command = checkEntry).grid(row = 2, column = 0, padx = 10, pady = 10, sticky = 'nsew')


class List(ttk.Frame):
    def __init__(self, controller, parent):
        super().__init__()
        self.create_widgets(controller)
        self.controller = controller
        self.reminder = tk.BooleanVar()

    def create_widgets(self, controller): 

        def delete():
            db.deleteItem(self.widgetName)
            controller.delFrame(List)

        def clicked(event):
            value = ['True', 'incomplete']
            if db.user['todo'][db.title][event.widget['text']]['value'] in value:
                self.newEntry(controller, title = event.widget['text'], arg = False)

            else:
                 db.user['todo'][db.title][event.widget['text']]['value'] = 'True'
            controller.delFrame(List)


        style = tk.ttk.Style(controller)

        icon = ttk.PhotoImage(file = 'left.png')
        back = tk.Label(self, text = 'Back', font = ('Roboto', 10), image = icon, compound = 'left')
        back.image = icon
        back.bind('<Button-1>', lambda e: controller.delFrame(Home))
        back.grid(row = 0, padx = 5, pady = (15,10), sticky = tk.W)

        ttk.Label(self,text = db.title , anchor = 'w', font = ('Roboto', 20,),).grid(row = 1, padx = 22, pady = (0,5), sticky = tk.EW) 
        ttk.Separator(self, orient = 'horizontal', bootstyle = 'light').grid(row = 2, padx = 20, pady = (0, 25), sticky = 'ew')
        btm = ttk.Frame(self)

        icon = ttk.PhotoImage(file = 'add.png')
        add_btn = ttk.Button(btm, text = 'Add New Task', image = icon, compound = 'left',width = 50, bootstyle = 'secondary', command = lambda: self.newEntry(controller))
        add_btn.image = icon

        completed = ttk.Labelframe(self, text = 'Completed', height = 25, bootstyle = 'secondary', width = 450)
        incomplete = ttk.Labelframe(self, text = 'Incomplete', height = 25, bootstyle = 'secondary', width = 450)

        i = 0
        task_boxes = []
        self.tasks = db.get('todo', todo = True)
        now = datetime.datetime.now()
        for j in self.tasks:
            if  j!= ' ':
                if db.user['todo'][db.title][j]['remind'] == 'True':
                    dateTime = datetime.datetime.strptime(db.user['todo'][db.title][j]['datetime'], '%Y-%m-%d %X')

                    if db.user['todo'][db.title][j]['value'] == 'False':
                        if now > dateTime:
                            db.user['todo'][db.title][j]['value'] = 'incomplete'


                lb = ttk.Checkbutton(btm, text = j, bootstyle = 'dark', ) 
                if db.user['todo'][db.title][j]['value'] == 'True':
                    lb = ttk.Checkbutton(completed, text = j, bootstyle = 'dark', ) 
                    lb.state(['selected'])

                elif db.user['todo'][db.title][j]['value'] == 'incomplete':
                    lb = ttk.Checkbutton(incomplete, text = j, bootstyle = 'dark', ) 
                    lb.state(['readonly'])

                task_boxes.append(lb)
                lb.grid(row = i, column = 0, padx =15, pady = 10, sticky = 'ew')
                i += 1

                
        add_btn.grid(row = i, column = 0, padx = 15, pady = 10, sticky = 'ew')
        btm.grid(row = 3)
        completed.grid(row = 4, padx = 15, sticky = 'w')
        incomplete.grid(row = 5, padx = 15, sticky = 'w')

        menu = ttk.Menu(self, tearoff = 0)
        menu.add_command(label = 'Edit', command = lambda:self.newEntry(controller, title = self.widgetName, arg = False) )
        menu.add_command(label = 'Delete', command = delete)

        def do_popup(event):
            try:
                menu.tk_popup(event.x_root, event.y_root)
                self.widgetName = event.widget['text']
            finally:
                menu.grab_release()


        for i in task_boxes:
            i.bind('<Button-1>', clicked)
            i.bind('<Button-3>', do_popup)


        style.configure('TCheckbutton', font = ('Arial', 10))
        db.updateItem()

    def newEntry(self,controller, title = '', arg = True,):

        self.top = ttk.Toplevel(self) 
        self.top.title('Enter')
        self.top.attributes('-toolwindow',True)

        if arg:
            ttk.Label(self.top, text = "Enter Task:",).grid(row = 0, column = 0, padx = 10, pady = (10,0), sticky = tk.EW)
            self.title = ttk.Entry(self.top) 
            self.title.focus()
            self.title.grid(row = 1, column = 0, sticky = tk.EW, padx = 10, pady = (0,10))
        else:
            self.title = tk.StringVar(value = title)

        today = datetime.date.today()
        now = datetime.datetime.now()
        frame = tk.Frame(self.top)
        date = tk.Frame(frame)

        def refresh():
            self.top.destroy()
            if arg:
                self.newEntry(self.controller, arg = arg)
            else:
                self.newEntry(self.controller, title = self.title.get(), arg = arg)
        reminderButton = ttk.Checkbutton(frame, text = 'Add reminder', command = refresh, bootstyle = 'dark',variable = self.reminder, onvalue = True, offvalue = False) 
        reminderButton.grid(row = 0, padx = 5, pady = 5, sticky = 'w')
         
        self.day_cb = ttk.Combobox(date, values = list(range(1,32)), state = 'readonly', width = 3)
        self.day_cb.current(int(today.day) - 1)

        self.month_cb = ttk.Combobox(date, state = 'readonly',  width = 3)

        self.months = [
            'Jan',
            'Feb',
            'Mar',
            'Apr',
            'May',
            'Jun',
            'Jul',
            'Aug',
            'Sep',
            'Oct',
            'Nov',
            'Dec'
        ]
        self.month_cb['values'] = self.months

        self.month_cb.current(int(today.month) - 1)

        years =  list(range(int(today.year),int(today.year)+11))
        self.year_cb = ttk.Combobox(date, values = years, state = 'readonly', width = 5)
        self.year_cb.current(years.index(int(today.year)))

        self.day_cb.grid(row = 0, column = 0, padx = 2)
        self.month_cb.grid(row = 0, column = 1, padx = 2)
        self.year_cb.grid(row = 0, column = 2, padx = 2)

        time = ttk.Frame(frame)
        self.hours_cb = ttk.Combobox(time, values = list(range(0,24)), state = 'readonly', width = 5)
        self.min_cb = ttk.Combobox(time, values = list(range(0,60)), state = 'readonly', width = 5)

        if int(now.hour) == 23 and int(now.minute) == 59:
            hour = 0
            minute = 0
        if int(now.minute) == 59:
            hour = int(now.hour)
            minute = 0 
        else:
            hour = int(now.hour)
            minute = int(now.minute) + 1

        self.hours_cb.current(hour)
        self.min_cb.current(minute)

        self.hours_cb.grid(row = 0, column = 0, padx = 5, sticky = 'nsew')
        ttk.Label(time, text = ':', width = 1).grid(row = 0, column = 1, padx = 5, sticky = 'nsew')
        self.min_cb.grid(row = 0, column = 2, padx = 5, sticky = 'nsew')

        if(self.reminder.get()):
            date.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = 'nsew')
            time.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = 'nsew')

        frame.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = 'nsew')

        ttk.Button(self.top, text = 'Create', bootstyle = LIGHT, command = lambda:self.checkEntry(controller, title = self.title.get().strip(), arg = arg)).grid(row = 3, column = 0, padx = 10, pady = 10, sticky = 'nsew')


    def checkEntry(self,controller, arg = True, title = ''):
        now = datetime.datetime.now()
        today = datetime.date.today()
        try:
            dateTime = datetime.datetime(int(self.year_cb.get()), int(self.months.index(self.month_cb.get())+1),
             int(self.day_cb.get()), int(self.hours_cb.get()), int(self.min_cb.get()))
            valid = True
            if arg:
                if not title:
                    show.show_error('Enter task', title = 'Error')
                    valid = False
                    self.top.lift()
                    self.top.focus()
                elif len(title) > 20:
                    show.show_error('Maximum 20 characters', title = 'Error')
                    valid = False
                    self.top.lift()
                    self.top.focus()
                elif title in self.tasks:
                    show.show_error('Task already exists!', title = "Error")
                    valid = False
                    self.top.lift()
                    self.top.focus()
            if self.reminder.get():
                if dateTime <= now:
                    show.show_error('Invalid date and time!', title = "Error")
                    valid = False
                    self.top.lift()
                    self.top.focus()

            if valid:
                if self.reminder.get():
                    db.addItem(title, dateTime)
                else:
                    db.addItem(title)
                self.top.destroy()
                controller.delFrame(List)
        except:
                show.show_error('Invalid date!', title = "Error")
                self.top.lift()
                self.top.focus()

