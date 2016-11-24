"""Makes a form window for those who prefer using a GUI to set their settings."""
# Remove this bit when publishing.
import os
os.chdir(os.path.dirname(__file__))

import tkinter as tk
import selene
from modulescripts import FANCY_LANGS
# Too many ancestors. That's external wrapper libraries for you. pylint: disable-msg=R0901

class TestForm(tk.Frame):
    """A Frame containing a bunch of controls, used to customise test runs."""
    def __init__(self, props, master=None):
        super().__init__(master)
        self.pack(side='left')
        self.create_widgets(props)

    def create_widgets(self, props):
        """Create all of the widgets representing the various options."""
        # First group, the locales. Label it, and make a checkbox for each locale.
        self.locales = tk.Frame(self)
        self.locales.grid(column=0, row=0, rowspan=5)
        tk.Label(self.locales, text='Locales').grid(column=0, row=1)
        self.locales.choices = {FANCY_LANGS[l]: tk.IntVar() for l in FANCY_LANGS}
        for l in FANCY_LANGS:
            lbox = tk.Checkbutton(
                self.locales, text=l, variable=self.locales.choices[FANCY_LANGS[l]])
            lbox.grid(column=0, sticky='w', columnspan=2)
        # If the locale is selected in the config file, preselect it here.
        for l in props['locales']:
            self.locales.choices[l].set(1)
        # Some buttons for Select All and Select None.
        tk.Button(self.locales, text='Select All',
                  command=set_all(self.locales.choices, 1)).grid(column=0, row=50)
        # There are not actualy 50 rows. It's just a hack to have them show up at the end.
        tk.Button(self.locales, text='Select None',
                  command=set_all(self.locales.choices, 0)).grid(column=1, row=50)

        # Two fields for the Environment domains.
        self.environs = tk.Frame(self, padx=5)
        self.environs.grid(column=1, row=0, sticky='n')
        self.environs.environment, self.environs.chenvironment = tk.StringVar(), tk.StringVar()
        tk.Label(self.environs, text='Environment').grid(sticky='w')
        tk.Entry(self.environs, textvariable=self.environs.environment, width=50).grid()
        self.environs.environment.set(props['environment'])
        tk.Label(self.environs, text='China Environment').grid(sticky='w')
        tk.Entry(self.environs, textvariable=self.environs.chenvironment, width=50).grid()
        self.environs.chenvironment.set(props['chenvironment'])

        # The Author Credentials.
        self.auth = tk.Frame(self)
        self.auth.grid(column=1, row=1, sticky='n')
        self.auth.username, self.auth.password = tk.StringVar(), tk.StringVar()

class ResultsForm(tk.Frame):
    """A Frame containing a bunch of Frames containing a bunch of Frames"""
    def __init__(self, results, master=None):
        super().__init__(master)
        self.pack(side='right')
        self.create_widgets(results)

    def create_widgets(self, results):
        """Creates all of the frames containing the results of each test."""
        pass

def set_all(tosel, x):
    """Given a dict of tkinter variables, returns a function that can be called to set all to x."""
    def selectem():
        """Sets all of the things in the given list to 1"""
        for t in tosel:
            tosel[t].set(x)
    return selectem

def incipe(props):
    """Begin Form Test Mode, should allow iterated testing, conveniences minor changes?
    Is prepopulated with the .properties file the first time, does not write to it."""
    TestForm(props, master=root)

def fenestrate(results):
    """Display a TextTestResult as a Tk application thing. Results should be a list.
    A list of TextTestResult objects or Exceptions. Try not to mishandle them."""
    ResultsForm(results, master=root)

if __name__ == '__main__':
    root = tk.Tk()
    incipe(selene.read_properties())
    root.mainloop()
