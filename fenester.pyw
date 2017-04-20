"""Makes a form window for those who prefer using a GUI to set their settings."""
# Remove this bit when publishing.
import os
os.chdir(os.path.dirname(__file__))

import re
import sys
import tkinter as tk
import selene
from math import ceil
from ASP import aspnames
from drivery import BROWSERS
from modulescripts import FANCY_LANGS
# Too many ancestors. That's external wrapper libraries for you. pylint: disable=R0901

class TestForm(tk.Frame):
    """A Frame containing a bunch of controls, used to customise test runs."""
    def __init__(self, props, master=None):
        super().__init__(master)
        self.pack(side='left')
        self.create_widgets(props)

    def create_widgets(self, props: dict):
        """Create all of the widgets representing the various options."""
        # Two fields for the Environment domains.
        self.environs = tk.Frame(self, padx=5, borderwidth=5, relief='groove')
        self.environs.grid(column=0, row=0, sticky='nsew', columnspan=2)
        self.environs.environment, self.environs.chenvironment = tk.StringVar(), tk.StringVar()
        tk.Label(self.environs, text='Environment').grid(sticky='w')
        tk.Entry(self.environs, textvariable=self.environs.environment, width=50).grid()
        self.environs.environment.set(props['environment'])
        tk.Label(self.environs, text='China Environment').grid(sticky='w')
        tk.Entry(self.environs, textvariable=self.environs.chenvironment, width=50).grid()
        self.environs.chenvironment.set(props['chenvironment'])

        # First group, the locales. Label it, and make a checkbox for each locale.
        self.locales = tk.Frame(self, borderwidth=5, relief='groove')
        self.locales.grid(column=0, row=1, rowspan=2, sticky='nsew')
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
                  command=set_all(self.locales.choices, 1)).grid(column=0, row=50, sticky='nsew')
        # There are not actualy 50 rows. It's just a hack to have them show up at the end.
        tk.Button(self.locales, text='Select None',
                  command=set_all(self.locales.choices, 0)).grid(column=1, row=50, sticky='nsew')

        # The Browser options.
        self.browsers = tk.Frame(self, borderwidth=5, relief='groove')
        self.browsers.grid(column=1, row=1, sticky='nsew')
        tk.Label(self.browsers, text='Browsers').grid(column=0, row=1)
        self.browsers.choices = {b: tk.IntVar() for b in BROWSERS}
        for b in BROWSERS:
            bbox = tk.Checkbutton(
                self.browsers, text=b, variable=self.browsers.choices[b])
            bbox.grid(column=0, sticky='w', columnspan=2)
        # If the browser is selected in the config file, preselect it here.
        for b in props['browsers']:
            self.browsers.choices[b].set(1)
        # Some buttons for Select All and Select None.
        tk.Button(self.browsers, text='Select All',
                  command=set_all(self.browsers.choices, 1)).grid(column=0, row=50, sticky='nsew')
        # There are not actualy 50 rows. It's just a hack to have them show up at the end.
        tk.Button(self.browsers, text='Select None',
                  command=set_all(self.browsers.choices, 0)).grid(column=1, row=50, sticky='nsew')

        # One for the Username field.
        self.user = tk.Frame(self, borderwidth=5, relief='groove')
        self.user.grid(column=2, row=0, sticky='nsew')
        self.user.name = tk.StringVar()
        tk.Label(self.user, text='Username (optional)').grid(sticky='e')
        tk.Entry(self.user, textvariable=self.user.name, width=15).grid()

        # The Test Options list.
        self.tests = tk.Frame(self, borderwidth=5, relief='groove')
        self.tests.grid(column=2, row=1, rowspan=2, sticky='nsew')
        self.tests.choices = {t: tk.IntVar() for t in aspnames}
        l = ceil(len(aspnames) / 2)
        for i, t in enumerate(aspnames):
            tbox = tk.Checkbutton(self.tests, text=' '.join(aspnames[t].split('_')[2:]),
                                  variable=self.tests.choices[t])
            tbox.grid(column=(0 if i < l else 2), row=(i % l), sticky='w', columnspan=2)
        # If no tests are specified, specify all of them.
        if props['tests'] == []:
            set_all(self.tests.choices, 1)()
        # If the test is selected in the config file, preselect it here.
        for t in props['tests']:
            self.tests.choices[t].set(1)
        # Some buttons for Select All and Select None.
        tk.Button(self.tests, text='Select All',
                  command=set_all(self.tests.choices, 1)).grid(column=0, row=50, sticky='nsew')
        # There are not actualy 50 rows. It's just a hack to have them show up at the end.
        tk.Button(self.tests, text='Select None',
                  command=set_all(self.tests.choices, 0)).grid(column=0, row=51, sticky='nsew')
        # Buttons for partial selections
        prereg = ('SPL', 'HPG', 'NAV', 'FTR', 'SMP', 'ITN', 'FCT', 'MAP', 'CTC')
        tk.Button(self.tests, text='Not-Signed-In Tests', command=set_some(
            self.tests.choices, 0, prereg, 1)).grid(column=1, row=50, sticky='nsew')
        postreg = ('LOG', 'FAV', 'PRF', 'TRN', 'ASC', 'TVL', 'FML', 'PHT', 'DLB', 'STR', 'PRM', 'FUN', 'FPW', 'CPW', 'CMP')
        tk.Button(self.tests, text='Signed-In Tests', command=set_some(
            self.tests.choices, 0, postreg, 1)).grid(column=1, row=51, sticky='nsew')
        postqual = ('ASC', 'TVL', 'FML', 'PHT', 'DLB', 'STR', 'PRM', 'FUN', 'FPW', 'CPW', 'CMP')
        tk.Button(self.tests, text='Specialist Tests', command=set_some(
            self.tests.choices, 0, postqual, 1)).grid(column=2, row=50, sticky='nsew')
        modow = ('SPL', 'HPG', 'NAV', 'FTR', 'SMP', 'ITN', 'FCT', 'MAP', 'CTC', 'REG', 'LOG', 'FAV', 'PRF', 'FUN', 'FPW', 'CPW', 'CMP')
        tk.Button(self.tests, text='Full Run If Modules Is Down', command=set_some(
            self.tests.choices, 0, modow, 1)).grid(column=2, row=50, sticky='nsew')
        remodow = ('SPL','HPG','NAV','FTR','SMP','ITN','FCT','MAP','CTC','LOG','FAV','PRF','FUN','FPW','CPW','CMP')
        tk.Button(self.tests, text='Full Run If Registration And Modules Are Down\n(Provide A Username)', command=set_some(
            self.tests.choices, 0, remodow, 1)).grid(column=2, row=51, sticky='nsew')

        # Finally, the Go Button.
        tk.Button(self, command=self.compile, text='GO').grid(column=1, row=2, sticky='nsew')

    def compile(self):
        pass

class ResultsForm(tk.Frame):
    """A Frame containing a bunch of Frames containing a bunch of Frames"""
    def __init__(self, results, master=None):
        super().__init__(master)
        self.pack(side='right')
        self.create_widgets(results)

    def create_widgets(self, results):
        """Creates all of the frames containing the results of each test."""

        with open(results) as tap:
            for line in tap.readlines:
                if re.match('(not )?ok', line):
                    pane = tk.Frame(self, bg='red' if line.startswith('not') else 'green')
                    tk.Label(pane, text=re.match(r'test_\d\d_(.+?) ').groups()[0]).grid(column=0)
                    fultex = tk.Label(pane).grid(columnspan=2)
                else:
                    fultex.text += line.strip('#')

def set_some(tosel, x, selection, y):
    """Given a dict of tkinter variables, and a tuple of keys returns a function
    that can be called to set the selected ones to y and the rest to x."""
    def selectem():
        """Sets some things to something, and others to other thing."""
        set_all(tosel, x)()
        for s in selection:
            tosel[s].set(y)
    return selectem

def set_all(tosel, x):
    """Given a dict of tkinter variables, returns a function that can be called to set all to x."""
    def selectem():
        """Sets all of the things to something."""
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
    if len(sys.argv) == 1:
        incipe(selene.read_properties())
    else:
        fenestrate(sys.argv[1])
    root.mainloop()
