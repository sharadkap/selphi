"""Test execution goes in here, but no browser interaction implementation details.
Nonfatal Assertions are a bit of a mess, but whatever, can't really refactor control flow."""

import os
import io
import sys
import time
import signal
import unittest
import configparser
from typing import Tuple
from multiprocessing import cpu_count, Pool
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementNotVisibleException, ElementNotInteractableException
import drivery as DR
import modules as MOD
import miklase

def main() -> None:
    """If selene.py is the entrypoint, read the settings from the config file and run the tests."""
    # Get the test run settings from the config file.
    args = read_properties()
    # And run the test with the config file settings.
    launch_test_suite(args)

def test_dr() -> Tuple[dict, DR.Drivery]:
    """When the module is loaded, call this one to get a prepopulated gdict and Drivery object."""
    d = read_properties()
    d['browser'] = 'chrome'
    d['locale'] = '/en'
    d['cn_mode'] = False
    d['base_url'] = d['environment']
    d['locale_url'] = d['base_url'] + d['locale']
    return d, DR.Drivery(d)

def launch_test_suite(args: dict) -> list:
    """Set up the multiprocessing constructure, and kick off all of the tests."""
    outdir = os.path.split(__file__)[0]
    # Each locale and browser combination is to be run in parallel, break out the MultiProcessing.
    # Up to 3xcores, but only as many as needed.
    count = min(cpu_count() * 3, len(args['locales']) * len(args['browsers']))
    pool = Pool(count)
    # KeyboardInterrupts don't actually break out of blocking-waits, so a bit of a workaround:
    try:    # Do the things as normal,
        asy = pool.map_async(launch_test, [(loc, bro, outdir, args.copy())
                                           for loc in args['locales'] for bro in args['browsers']])
        while True:     # But check every so often if they are all done.
            if asy.ready():
                return asy.get()  # If so, cool, let's go.
            time.sleep(1) # If not, wait a second and check again. This doesn't block the interrupt.
    except KeyboardInterrupt:
        # If there is an interrupt, shut down everything, that was the Cancel Run signal.
        pool.terminate()
        sys.exit()

def launch_test(args) -> Tuple[str, str, dict]:
    """Do all the things needed to run a test suite. Put this as the target call of a process."""
    # Put these in this method here to avoid circular importing.
    import ASP, AUS, INV

    signal.signal(signal.SIGINT, signal.SIG_IGN)    # Set the workers to ignore KeyboardInterrupts.
    locale, browser, outdir, globs = args   # Unpack arguments.
    # Do a bunch of method overrides to get it to work properly.
    perform_hacks()
    # Set up the run settings.
    globs['locale'] = locale
    globs['browser'] = browser
    # If China Mode, do it in China, otherwise, don't do it in China
    if locale == globs['cn_locale']:
        globs['cn_mode'] = True
        globs['base_url'] = globs['chenvironment']
    else:
        # If a url was given, make that the default.
        globs['cn_mode'] = False
        globs['base_url'] = globs['environment']
    globs['locale_url'] = globs['base_url'] + locale

    # Create the test runner, choose the output path: right next to the test script file.
    with io.StringIO() as buf:
        # A custom hack to enable multiple-test-failues
        runner = miklase.MyTestRunner(stream=buf, resultclass=miklase.MyTestResult)
        # Instantiate the test suites, and give them their process-unique globals and accesses
        site = globs['site']
        if site == 'ASP':
            names = [ASP.ASP(ASP.aspnames[x], globs, runner.result)
                     for x in globs['tests'] or ASP.aspnames]
        elif site == 'AUS':
            names = [AUS.AUS(AUS.ausnames[x], globs, runner.result)
                     for x in globs['tests'] or AUS.ausnames]
        elif site == 'INV':
            names = [INV.INV(INV.invnames[x], globs, runner.result)
                     for x in globs['tests'] or INV.invnames]
        suite = unittest.TestSuite()
        suite.addTests(unittest.TestSuite(names))
        result = runner.run(suite)

        # Give a unique name to the output file so you don't overwrite it every time!
        filna = 'REGR_{0}_{1}_{2}_{3}.txt'.format(locale[1:], site, browser,
                                                  time.strftime('%Y%m%d_%H%M'))
        try:
            with open(os.path.join(outdir, filna), mode='w', encoding='UTF-8') as newfil:
                newfil.write(globs.get('username'))
                newfil.write(buf.getvalue())
        except Exception as ex:
            print("Failed to save the output file:", ex)
        return (browser, locale, result.resultsList)

def perform_hacks() -> None:
    """Because not everything works the way it SHOULD, have to override a few methods."""
    # Another one, that menu sure does get in the way sometimes.
    oldclick = DR.WebElement.click
    def newclick(*args, **kwargs):
        """Overwrite the WebElement.click method to make sure that it isn't behind the nav menu."""
        try:
            oldclick(*args, **kwargs)
        except ElementNotVisibleException:
            time.sleep(1)   # Just wait till it's finished animating or whatever
            oldclick(*args, **kwargs)
        except ElementNotInteractableException:  # args[0] will be the 'self': the WebElement
            args[0].parent.execute_script(DR.SCROLL_SCRIPT, args[0])
            oldclick(*args, **kwargs)
    DR.WebElement.click = newclick

    def newctrlclick(self):
        """Create a new method, for control-clicking"""
        dr = self.parent
        try:
            ActionChains(dr).key_down(Keys.CONTROL).click(self).key_up(Keys.CONTROL).perform()
        except MOD.WebDriverException:
            dr.execute_script(DR.SCROLL_SCRIPT, self)
            ActionChains(dr).key_down(Keys.CONTROL).click(self).key_up(Keys.CONTROL).perform()
    DR.WebElement.ctrl_click = newctrlclick

def read_properties() -> dict:
    """Read the run options from the properties file and tidy them up a little."""
    conf = configparser.ConfigParser()
    conf.read(os.path.join(os.path.dirname(__file__), 'test.properties'))
    result = dict(conf['Main Section'])
    result['auth'] = result['auth'].split(',') if result['auth'] else []
    result['locales'] = result['locales'].split(',')
    result['browsers'] = result['browsers'].split(',')
    result['tests'] = result['tests'].split(',') if result['tests'] else []
    result['asp_from_emails'] = result['asp_from_emails'].split(',')
    # Fill out the user details if username is included.
    if result['username']:
        result['userid'] = result['username'][-4:]    # The mail ID is the last four characters.
        result['email'] = result['email'].format(result['userid'])
    return result

if __name__ == '__main__':
    main()
