"""Makes a form window for those who prefer using a GUI to set their settings."""
import os
os.chdir(os.path.dirname(__file__))

import sys
import tkinter as tk
import tkinter.ttk as ttk
from math import ceil
from multiprocessing import Pool, cpu_count
import selene
from miklase import STATES
from ASP import aspnames
from drivery import BROWSERS
from modulescripts import FANCY_LANGS
# Too many ancestors. That's external wrapper libraries for you. pylint: disable=R0901

relcol = {STATES.PASS.name: 'green', STATES.SKIP.name: 'grey',
          STATES.FAIL.name: 'yellow', STATES.ERROR.name: 'red'}

class TestForm(tk.Frame):
    """A Frame containing a bunch of controls, used to customise test runs."""
    def __init__(self, props, master=None):
        super().__init__(master)
        self.grid(column=0, row=0)
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
        postreg = ('LOG', 'FAV', 'PRF', 'TRN', 'ASC', 'TVL', 'FML', 'PHT',
                   'DLB', 'STR', 'PRM', 'FUN', 'FPW', 'CPW', 'CMP')
        tk.Button(self.tests, text='Signed-In Tests', command=set_some(
            self.tests.choices, 0, postreg, 1)).grid(column=1, row=51, sticky='nsew')
        postqual = ('ASC', 'TVL', 'FML', 'PHT', 'DLB', 'STR', 'PRM', 'FUN', 'FPW', 'CPW', 'CMP')
        tk.Button(self.tests, text='Specialist Tests', command=set_some(
            self.tests.choices, 0, postqual, 1)).grid(column=2, row=50, sticky='nsew')
        modow = ('SPL', 'HPG', 'NAV', 'FTR', 'SMP', 'ITN', 'FCT', 'MAP', 'CTC',
                 'REG', 'LOG', 'FAV', 'PRF', 'FUN', 'FPW', 'CPW', 'CMP')
        tk.Button(self.tests, text='Full Run If Modules Is Down', command=set_some(
            self.tests.choices, 0, modow, 1)).grid(column=2, row=50, sticky='nsew')
        remodow = ('SPL', 'HPG', 'NAV', 'FTR', 'SMP', 'ITN', 'FCT', 'MAP', 'CTC',
                   'LOG', 'FAV', 'PRF', 'FUN', 'FPW', 'CPW', 'CMP')
        tk.Button(self.tests, command=set_some(self.tests.choices, 0, remodow, 1),
                  text='Full Run If Registration And Modules Are Down\n(Provide A Username)').grid(
                      column=2, row=51, sticky='nsew')

        # Finally, the Go Button.
        tk.Button(self, command=self.go, text='GO').grid(column=1, row=2, sticky='nsew')

    def go(self):
        """Arranges all of the options into an argsdict, and kicks off the test."""
        args = selene.read_properties()
        args['locales'] = [
            FANCY_LANGS[l] for l in FANCY_LANGS if self.locales.choices[FANCY_LANGS[l]].get() == 1]
        args['browsers'] = [b for b in BROWSERS if self.browsers.choices[b].get() == 1]
        args['tests'] = [t for t in aspnames if self.tests.choices[t].get() == 1]
        if self.user.name.get():
            args['username'] = self.user.name.get()
            args['userid'] = args['username'][-4:]    # The mail ID is the last four characters.
            args['email'] = args['email'].format(args['userid'])
        args['environment'] = self.environs.environment.get()
        args['chenvironment'] = self.environs.chenvironment.get()
        prev = self.master.children.get('!resultsform')
        if prev:
            prev.grid_forget()
        # fenestrate(self.launch_fake_test())
        self.launch_test_suite(args)

    def launch_test_suite(self, args) -> None:
        """Set up the multiprocessing constructure, and kick off all of the tests.
        It's supposed to be asynchronous, so don't worry about all those extra handles"""
        outdir = os.path.split(__file__)[0]
        locs, bros = args['locales'], args['browsers']
        count = min(cpu_count() * 3, len(locs) * len(bros))   # Make up to 3xcores processes
        largs = [(loc, bro, outdir, args.copy()) for loc in locs for bro in bros] # Args to pass
        Pool(count).map_async(selene.launch_test, largs, callback=fenestrate, error_callback=print)

    def launch_fake_test(self) -> list:
        """Just so I don't have to do an actual test run each time I test this thing."""
        return [('Chrome', '/it-it', {'Test_01_Something': [(STATES.PASS, 'Test Passed')], 'Test_02_Elsething': [(STATES.FAIL, 'Assertion: should not fail'), (STATES.ERROR, 'Could not find element')]}),
                ('Chrome', '/en-gb', {'Test_01_Something': [(STATES.PASS, 'Test Passed')], 'Test_02_Elsething': [(STATES.FAIL, 'Assertion: should not fail'), (STATES.ERROR, 'Could not find element')]}),
                ('Firefox', '/it-it', {'Test_01_Something': [(STATES.PASS, 'Test Passed')], 'Test_02_Elsething': [(STATES.FAIL, 'Assertion: should not fail'), (STATES.ERROR, 'Could not find element')]}),
                ('Firefox', '/en-gb', {'Test_01_Something': [(STATES.PASS, 'Test Passed')], 'Test_02_Elsething': [(STATES.FAIL, 'Assertion: should not fail'), (STATES.ERROR, '\nFile "C:\\Users\\bzalakos\\Documents\\GitHub\\selphi\\ASP.py", line 799, in test_15_Aussie_Specialist_Club\nclub.click()\nselenium.common.exceptions.WebDriverException: Message: unknown error: Element <li id="nav-main-panel-5" class="has-children" style="animation-duration: 0.5s; animation-name:\nselhian;">...</li> is not clickable at point (1131, 108). Other element would receive the click: <div class="fancybox-overlay fancybox-overlay-fixed" style="width: auto; height: auto; display: block;"></div>\n(Session info: chrome=59.0.3071.115)\n(Driver info: chromedriver=2.30.477700 (0057494ad8732195794a7b32078424f92a5fce41),platform=Windows NT 6.3.9600 x86_64)\n')]})]

class ResultsForm(tk.Frame):
    """A Frame containing a bunch of Frames containing a bunch of Frames"""
    def __init__(self, results, master=None):
        if master:
            master.columnconfigure(0, weight=1)
            master.columnconfigure(1, weight=1)
        super().__init__(master, borderwidth=2, relief='solid')
        self.grid(column=1, row=0, sticky="nsew")

        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.vsb.grid(row=0, column=1, sticky='nse')
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw", tags="self.frame")
        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.create_widgets(results)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.canvas.config(width=event.width, height=event.height)

    def create_widgets(self, results):
        """Creates all of the frames containing the results of each test."""
        colls = []
        topl = tk.Frame(self.frame)
        topl.grid(sticky='nsew')
        tk.Button(topl, command=lambda: [x.show() for x in colls], text="Show All").grid(column=0, row=0)
        tk.Button(topl, command=lambda: [x.hide() for x in colls], text="Hide All").grid(column=1, row=0)
        for browser, locale, result in results:
            pane = Collapser(self.frame, text=browser + ' - ' + locale)
            pane.grid(sticky='nsew')
            pane.sub_frame.columnconfigure(0, weight=1)
            colls.append(pane)
            for name in result:
                panelet = Collapser(pane.sub_frame, text=name)
                panelet.grid(sticky='nsew')
                colls.append(panelet)
                for i, (status, info) in enumerate(result[name]):
                    status = status.name
                    tk.Label(panelet.sub_frame, text=status, width=6,
                             background=relcol[status]).grid(row=i, column=0, sticky='nsew')
                    tk.Label(panelet.sub_frame, text=info, anchor='w', justify='left',
                             wraplength=500).grid(row=i, column=1, sticky='nsew')

class Collapser(tk.Frame):
    """A tk Frame that can be collapsed and expanded"""
    def __init__(self, parent, text="", *args, **options):
        tk.Frame.__init__(self, parent, *args, **options)

        self.showv = tk.IntVar()
        self.showv.set(0)
        self.columnconfigure(0, weight=1)
        self.title_frame = tk.Frame(self)
        self.title_frame.bind('<Button-1>', self.toggle)
        self.title_frame.grid(row=0, column=0, sticky='nsew')
        self.title_frame.columnconfigure(0, weight=1)
        label = tk.Label(self.title_frame, text=text)
        label.bind('<Button-1>', self.toggle)
        self.toggle_button = ttk.Label(self.title_frame, width=2, text='>')
        self.toggle_button.pack(side='left')
        label.pack(side='left')
        self.sub_frame = tk.Frame(self, relief='sunken', borderwidth=1, padx=10)

    def show(self):
        """Show the panel"""
        self.sub_frame.grid(row=1, column=0, sticky='nsew')
        self.toggle_button.configure(text='v')
        self.showv.set(1)

    def hide(self):
        """Hide the panel"""
        self.sub_frame.grid_remove()
        self.toggle_button.configure(text='>')
        self.showv.set(0)

    def toggle(self, _=None):
        """Show or hide the panel"""
        if bool(self.showv.get()):
            self.hide()
        else:
            self.show()

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
    """Given a dict of tkinter variables, returns a function that can be called to set all to x"""
    def selectem():
        """Sets all of the things to something"""
        for t in tosel:
            tosel[t].set(x)
    return selectem

def incipe(props):
    """Begin Form Test Mode, should allow iterated testing, conveniences minor changes?
    Is prepopulated with the .properties file the first time, does not write to it."""
    TestForm(props, master=root)

def fenestrate(results):
    """Display a TextTestResult as a Tk application thing. Results should be a list:
    A list of tuples (browser name, locale, results dict)"""
    ResultsForm(results)

if __name__ == '__main__':
    root = tk.Tk()
    root.title('SELPHI')
    if len(sys.argv) == 1:
        incipe(selene.read_properties())
    else:
        fenestrate(sys.argv[1])
    root.mainloop()
