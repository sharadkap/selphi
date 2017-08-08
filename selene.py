"""Test execution goes in here, but no browser interaction implementation details.
Nonfatal Assertions are a bit of a mess, but whatever, can't really refactor control flow."""

import os
import io
import sys
import time
import enum
import signal
import unittest
import configparser
from typing import Tuple
from collections import OrderedDict
from contextlib import contextmanager
from multiprocessing import cpu_count, Pool
import drivery as DR
import modules as MOD

from ASP import ASP, aspnames
from AUS import AUS, ausnames

DEBUG = False
STATES = enum.Enum('STATES', 'PASS SKIP FAIL ERROR')

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
    d['locale'] = '/en-gb'
    d['cn_mode'] = False
    d['base_url'] = d['environment']
    d['locale_url'] = d['base_url'] + d['locale']
    return d, DR.Drivery(d)

def launch_test_suite(args: dict) -> list:
    """Set up the multiprocessing constructure, and kick off all of the tests."""
    outdir = os.path.split(__file__)[0]
    # Each locale and browser combination is to be run in parallel, break out the MultiProcessing.
    pool = Pool(cpu_count() * 3)  # It's mostly waiting; we can afford to overload the cores, right?
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

class MyTestCase(unittest.TestCase):
    """A customised test case, to use my custom error handling"""
    def __init__(self, name: str, glob: dict, result: 'MyTestResult'):
        super().__init__(methodName=name)
        self.globs = glob
        self.result = result

    def setUp(self) -> None:
        """Called just before each test is run, sets up the browser and test records."""
        # Initialise the browser connection.
        self.verificationErrors = []    # Keep a list of everything that went wrong.
        self.accept_next_alert = True
        self.dr = DR.Drivery(self.globs)

    def tearDown(self) -> None:
        """Called after finishing each test, closes the browser and counts up the errors."""
        self.dr.close()
        self.maxDiff = None
        for err in self.verificationErrors:
            self.result.addFailure(self, err)

    @contextmanager
    def restraint(self, msg, **errors):
        """Shortcut for the error handling. Put this in a with statement, it'll log any error.
        msg is the default message, provide alternate messages for specific errors with the kwargs.
        Something like ZeroDivisionError="Can't divide by zero" """
        try:
            yield
        except:
            erty = sys.exc_info()[0].__name__
            if errors.get(erty):
                self.add_error(errors[erty])
            else:
                self.add_error(msg)

    def add_error(self, message=None) -> None:
        """Adds an error to the errors list. Shortcut.
        message is a more readable Error message"""
        self.verificationErrors.append(('' + message +':\n' if message else '') + tidy_error())

class MyTestRunner(unittest.TextTestRunner):
    def __init__(self, *args, **kwargs):
        super(MyTestRunner, self).__init__(*args, **kwargs)
        self.result = self._makeResult()

    def run(self, test):
        "Run the given test case or test suite. All this overload for one measly line."
        import warnings
        from unittest.signals import registerResult
        # result = self._makeResult()   Move this line into the init so I can mess with it interim.
        registerResult(self.result)
        self.result.failfast = self.failfast
        self.result.buffer = self.buffer
        self.result.tb_locals = self.tb_locals
        with warnings.catch_warnings():
            if self.warnings:
                warnings.simplefilter(self.warnings)
                if self.warnings in ['default', 'always']:
                    warnings.filterwarnings('module',
                                            category=DeprecationWarning,
                                            message=r'Please use assert\w+ instead.')
            startTime = time.time()
            startTestRun = getattr(self.result, 'startTestRun', None)
            if startTestRun is not None:
                startTestRun()
            try:
                test(self.result)
            finally:
                stopTestRun = getattr(self.result, 'stopTestRun', None)
                if stopTestRun is not None:
                    stopTestRun()
            stopTime = time.time()
        timeTaken = stopTime - startTime
        self.result.printErrors()
        if hasattr(self.result, 'separator2'):
            self.stream.writeln(self.result.separator2)
        run = self.result.testsRun
        self.stream.writeln("Ran %d test%s in %.3fs" %
                            (run, run != 1 and "s" or "", timeTaken))
        self.stream.writeln()

        expectedFails = unexpectedSuccesses = skipped = 0
        try:
            results = map(len, (self.result.expectedFailures,
                                self.result.unexpectedSuccesses,
                                self.result.skipped))
        except AttributeError:
            pass
        else:
            expectedFails, unexpectedSuccesses, skipped = results

        infos = []
        if not self.result.wasSuccessful():
            self.stream.write("FAILED")
            failed, errored = len(self.result.failures), len(self.result.errors)
            if failed:
                infos.append("failures=%d" % failed)
            if errored:
                infos.append("errors=%d" % errored)
        else:
            self.stream.write("OK")
        if skipped:
            infos.append("skipped=%d" % skipped)
        if expectedFails:
            infos.append("expected failures=%d" % expectedFails)
        if unexpectedSuccesses:
            infos.append("unexpected successes=%d" % unexpectedSuccesses)
        if infos:
            self.stream.writeln(" (%s)" % (", ".join(infos),))
        else:
            self.stream.write("\n")
        return self.result

class MyTestResult(unittest.TextTestResult):
    """Like a TextTestResult, but it actually remembers how all the tests went"""
    def __init__(self, *args, **kwargs):
        self.resultsList = OrderedDict()
        super(MyTestResult, self).__init__(*args, **kwargs)

    def _exc_info_to_string(self, err, test):
        """Converts a sys.exc_info()-style tuple of values into a string."""
        return tidy_error(err)

    def addResult(self, test, status, info):
        """Add a test's result to the record.
        Ends up something like {name: [(status, info), (status, info)]}"""
        name = test.id()
        if self.resultsList.get(name):
            self.resultsList[name].append((status, info))
        else:
            self.resultsList[name] = [(status, info)]

    def addSuccess(self, test):
        """If a test passed, make a note of that"""
        super(MyTestResult, self).addSuccess(test)
        self.addResult(test, STATES.PASS, "Test Passed")

    def addSkip(self, test, reason):
        """If a test was skipped, make a note of that"""
        super(MyTestResult, self).addSkip(test, reason)
        self.addResult(test, STATES.SKIP, reason)

    def addFailure(self, test, err):
        """If a test failed, make a note of that"""
        super(MyTestResult, self).addFailure(test, err)
        self.addResult(test, STATES.FAIL, tidy_error(err))

    def addError(self, test, err):
        """If a test crashed, make a note of that"""
        super(MyTestResult, self).addError(test, err)
        self.addResult(test, STATES.ERROR, tidy_error(err))

    def printErrors(self):
        """After running the test, print out the full results"""
        self.stream.writeln()
        for name in self.resultsList:
            self.stream.writeln(self.separator1)
            self.stream.writeln(name)
            for status, info in self.resultsList[name]:
                self.stream.writeln(self.separator2)
                self.stream.writeln(status.name)
                self.stream.writeln(info)

def launch_test(args) -> Tuple[str, str, dict]:
    """Do all the things needed to run a test suite. Put this as the target call of a process."""
    signal.signal(signal.SIGINT, signal.SIG_IGN)    # Set the workers to ignore KeyboardInterrupts.
    locale, browser, outdir, globs = args   # Unpack arguments.
    # Turn on debug logging mode, maybe.
    if globs['debug']:
        global DEBUG
        DEBUG = True
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
        runner = MyTestRunner(stream=buf, resultclass=MyTestResult)
        # Instantiate the test suites, and give them their process-unique globals and access to things
        site = globs['site']
        if site == 'ASP':
            names = [ASP(aspnames[x], globs, runner.result) for x in globs['tests'] or aspnames]
        elif site == 'AUS':
            names = [AUS(ausnames[x], globs, runner.result) for x in globs['tests'] or ausnames]
        tests = unittest.TestSuite(names)
        suite = unittest.TestSuite()
        suite.addTests(tests)
        result = runner.run(suite)

        # Give a unique name to the output file so you don't overwrite it every time!
        filna = 'REGR_{0}_{1}_{2}_{3}.txt'.format(locale[1:], site, browser,
                                                  time.strftime('%Y%m%d_%H%M'))
        try:
            with open(os.path.join(outdir, filna), mode='w', encoding='UTF-8') as newfil:
                newfil.write(buf.getvalue())
        except Exception as ex:
            print("Failed to save the output file:", ex)
        return (browser, locale, result.resultsList)



def tidy_error(ex=None) -> str:
    """Reads exception info from sys.exc_info and only shows the lines that are from SELPHI
    Unless DEBUG is True, in which case, it prints the enrirety of the trace."""
    from os.path import join, abspath, dirname
    from traceback import extract_tb, format_list, format_exception_only
    # If the exception is already pasted into a string, just return that.
    if type(ex) is str:
        return ex

    show = join(dirname(abspath(__file__)), '')

    def _check_file(name):
        return name and name.startswith(show)

    def _print(typ, value, tb):     # If not debug, generator expression: filter trace to my files.
        show = extract_tb(tb) if DEBUG else (
            fs for fs in extract_tb(tb, limit=3) if _check_file(fs.filename))
        fmt = format_list(show) + format_exception_only(typ, value)
        return ''.join((f.strip('"\'').replace('\\n', '') for f in fmt))

    args = ex or sys.exc_info()
    return _print(*args)

def perform_hacks() -> None:
    """Because not everything works the way it SHOULD, have to override a few methods."""
    # Another one, that menu sure does get in the way sometimes.
    oldclick = DR.WebElement.click
    def newclick(*args, **kwargs):
        """Overwrite the WebElement.click method to make sure that it isn't behind the nav menu."""
        try:
            oldclick(*args, **kwargs)
        except MOD.WebDriverException:  # args[0] will be the 'self' argument, so, the WebElement.
            args[0].parent.execute_script(DR.SCROLL_SCRIPT, args[0])
            oldclick(*args, **kwargs)
    DR.WebElement.click = newclick

def read_properties() -> dict:
    """Read the run options from the properties file and tidy them up a little."""
    conf = configparser.ConfigParser()
    conf.read('test.properties')
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
