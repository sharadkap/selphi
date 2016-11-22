import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi = tk.Button(self)
        self.hi['text'] = "Hello World\n(click)"
        self.hi['command'] = self.say_hi
        self.hi.pack(side='top', expand=1)

        self.quit = tk.Button(self, text='QUIT', fg='red', bg='blue', command=root.destroy)
        self.quit.pack(side='bottom', expand=1)

    def say_hi(self):
        print('Hello.')

root = tk.Tk()
app = Application(master=root)
app.mainloop()

def fenestrate(results):
    """Display a TextTestResult as a Tk application thing. Results should be a list.
    A list of TextTestResult objects or Exceptions. Try not to mishandle them."""
    pass
