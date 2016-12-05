"""Test execution goes in here, but no browser interaction implementation details.
Nonfatal Assertions are a bit of a mess, but whatever, can't really refactor control flow."""

import os
import io
import sys
import time
import signal
import unittest
import configparser
from multiprocessing import cpu_count
from multiprocessing.pool import Pool
import tap
import drivery as DR
import modules as MOD

import fenester
from ASP import ASP, aspnames
from AUS import AUS, ausnames

DEBUG = False

def main() -> None:
    """If selene.py is the entrypoint, read the settings from the config file and run the tests."""
    # Get the test run settings from the config file.
    args = read_properties()
    # And run the test with the config file settings.
    launch_test_suite(args)

def launch_test_suite(args: dict) -> None:
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
                # fenester.fenestrate(asy.get())  # If so, cool, let's go.
                return
            time.sleep(1) # If not, wait a second and check again. This doesn't block the interrupt.

    except:   # If there is an interrupt, shut down everything, that was the Cancel Run signal.
        pool.terminate()
        raise

def launch_test(args) -> None:
    """Do all the things needed to run a test suite. Put this as the target call of a process."""
    signal.signal(signal.SIGINT, signal.SIG_IGN)    # Set the workers to ignore KeyboardInterrupts.
    locale, browser, outdir, globs = args   # Unpack arguments.
    # Turn on debug logging mode, maybe.
    if globs['debug']:
        global DEBUG
        DEBUG = True
    # Instantiate the test suites, and give them their process-unique globals
    site = globs['site']
    if site == 'ASP':
        names = [ASP(aspnames[x], globs) for x in globs['tests'] or aspnames]
    elif site == 'AUS':
        names = [AUS(ausnames[x], globs) for x in globs['tests'] or ausnames]
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
        # TAP uses Module State, have to reset it for each test.
        tap.runner._tracker = tap.tracker.Tracker()     #pylint: disable-msg=W0212
        runner = tap.TAPTestRunner()
        runner.set_format('Result of: {method_name} - {short_description}')
        runner.set_stream(True)
        # Bit of a hack, but it doesn't support A Proper Way to reassign output, so.
        tap.runner._tracker.stream = buf    # pylint: disable-msg=W0212
        # For whatever reason, there are two output streams. Ignore this one, I guess.
        runner.stream.stream = sys.stdout
        tests = unittest.TestSuite(names)
        suite = unittest.TestSuite()
        suite.addTests(tests)
        result = runner.run(suite)

        # Give a unique name to the output file so you don't overwrite it every time!
        try:
            with open(os.path.join( # Bleh.
                outdir, 'REGR_{0}_{1}_{2}_{3}.tap'.format(
                    locale.replace('/', ''), site, browser, time.strftime('%Y%m%d_%H%M'))),
                      mode='w', encoding='UTF-8') as newfil:
                newfil.write(buf.getvalue())
            # return result
        except Exception as ex:
            print(ex)
            # return ex

def tidy_error(ex=None) -> str:
    """Reads exception info from sys.exc_info and only shows the lines that are from SELPHI
    Unless DEBUG is True, in which case, it prints the enrirety of the trace."""
    from os.path import join, abspath, dirname
    from traceback import extract_tb, format_list, format_exception_only

    show = join(dirname(abspath(__file__)), '')

    def _check_file(name):
        return name and name.startswith(show)

    def _print(typ, value, tb):
        show = extract_tb(tb) if DEBUG else (fs for fs in extract_tb(tb, limit=3) if _check_file(fs.filename))
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

    # By default, it will print out the full list of test failures at the end of the test.
    # This is a terrible idea, as that list tends to be longer than the cmd window buffer.
    # Especially when multiple test runs are underway. Here, set to skip that step.
    def newprinterrors(self):
        """Print a newline to the stream if in dot-drawing mode. Do not print the error report."""
        if self.dots or self.showAll:
            self.stream.writeln()
    unittest.TextTestResult.printErrors = newprinterrors

    # Striiped this entire method right out.
    # The original method contains this unused argument, and yes, it isn't used there either.
    def newex(self, err, test):     # pylint: disable-msg=W0613
        """Converts a sys.exc_info()-style tuple of values into a string."""
        return tidy_error(err)
    # And, override the existing method.
    # I do need to access this private property to correctly HAX it into working.
    # pylint: disable-msg=W0212
    unittest.result.TestResult._exc_info_to_string = newex
    # Also, tap has its own renderer as well, so have to overwrite that too.
    def newf(exc):
        """Rewrite this method so as to remove the traceback."""
        lines = tidy_error(exc).splitlines(True)
        return tap.formatter.format_as_diagnostics(lines)
    tap.formatter.format_exception = newf

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
    if 'username' in result.keys():
        result['userid'] = result['username'][-4:]    # The mail ID is the last four characters.
        result['email'] = result['email'].format(result['userid'])
    return result

if __name__ == '__main__':
    main()
