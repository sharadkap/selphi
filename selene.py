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

from ASP import ASP, aspnames
from AUS import AUS, ausnames

def main():
    """Read the arguments, run the tests."""
    args = read_properties()
    # Set the settings from the given arguments
    if args.username:
        args.userid = args.username[-4:]    # The mail ID is the last four characters.
        args.email = args.email.format(args.userid)

    # Get the output settings, the chosen test methods from the ASP suite.
    outdir = os.path.split(__file__)[0]

    # Run them in each locale.
    pool = Pool(cpu_count() * 2)  # It's mostly waiting; we can afford to overload the cores, right?
    # KeyboardInterrupts don't actually break out of blocking-waits, so do this the hard way.
    try:
        asy = pool.map_async(
            launch_test, [(loc, bro, outdir, args.copy())
                          for loc in args.locales for bro in args.browser])
        while True:
            if asy.ready():
                return
            time.sleep(1)   # Alright! Busy-Waiting! That can't possibly go awry!

    except KeyboardInterrupt:
        pool.terminate()
        raise

def launch_test(args) -> None:
    """Do all the things needed to run a test suite. Put this as the target call of a process."""
    signal.signal(signal.SIGINT, signal.SIG_IGN)    # Set the workers to ignore KeyboardInterrupts.
    locale, browser, outdir, globs = args   # Unpack arguments.
    # Instantiate the test suites, and give them their process-unique globals
    if globs.site == 'ASP':
        names = [ASP(aspnames[x], globs) for x in globs.tests or aspnames]
    elif globs.site == 'AUS':
        names = [AUS(ausnames[x], globs) for x in globs.tests or ausnames]

    # Do a bunch of method overrides to get it to work properly.
    perform_hacks()
    # Set up the run settings.
    DR.BROWSER_TYPE = DR.BROWSERS[browser]
    # If China Mode, do it in China, otherwise set the locale
    if locale == globs.cn_locale:
        globs.cn_mode = True
        globs.base_url = globs.chenvironment
    else:
        # If a url was given, make that the default.
        globs.base_url = globs.environment

    # Create the test runner, choose the output path: right next to the test script file.
    buf = io.StringIO()
    tap.runner._tracker = tap.tracker.Tracker()  # Reboot the test runner. pylint: disable-msg=W0212
    runner = tap.TAPTestRunner()
    runner.set_format('Result of: {method_name} - {short_description}')
    runner.set_stream(True)
    tap.runner._tracker.stream = buf    # bit of a hack, but how else? pylint: disable-msg=W0212
    runner.stream.stream = sys.stdout    # why.
    tests = unittest.TestSuite(names)
    suite = unittest.TestSuite()
    suite.addTests(tests)
    runner.run(suite)

    # Give a unique name to the output file so you don't overwrite it every time!
    with open(os.path.join(outdir, 'REGR_{0}_{1}_{2}.tap'
                           .format(locale, browser, time.strftime('%Y%m%d_%H%M'))),
              mode='w', encoding='UTF-8') as newfil:
        newfil.write(buf.getvalue())
    print(buf.getvalue() or 'It was blank')
    buf.close()

def perform_hacks():
    """Because not everything works the way it SHOULD, have to override a few methods."""
    # Another one, that menu sure does get in the way sometimes.
    oldclick = DR.WebElement.click
    def newclick(*args, **kwargs):
        """Overwrite the WebElement.click method to make sure that it isn't behind the nav menu."""
        try:
            oldclick(*args, **kwargs)
        except MOD.WebDriverException:
            DR.Drivery.scroll_element(args[0])
            oldclick(*args, **kwargs)
    DR.WebElement.click = newclick

    # This one really is a mess. Had to copy the method verbatim and make the required changes.
    # The original method contains this unused argument, and yes, it isn't used there either.
    def newex(self, err, test):     # pylint: disable-msg=W0613
        """Converts a sys.exc_info()-style tuple of values into a string."""
        import traceback
        exctype, value, tb = err
        # Strip the traceback down to the innermost call.
        tb_e = traceback.TracebackException(exctype, value, tb, limit=0,
                                            capture_locals=self.tb_locals)
        msgLines = list(tb_e.format())

        if self.buffer:
            output = sys.stdout.getvalue()
            error = sys.stderr.getvalue()
            if output:
                if not output.endswith('\n'):
                    output += '\n'
                msgLines.append('\nStdout:\n%s' % output)
            if error:
                if not error.endswith('\n'):
                    error += '\n'
                msgLines.append('\nStderr:\n%s' % error)
        return ''.join(msgLines)
    # And, override the existing method.
    # I do need to access this private property to correctly HAX it into working.
    # pylint: disable-msg=W0212
    unittest.result.TestResult._exc_info_to_string = newex
    # Also, tap has its own renderer as well, so have to overwrite that too.
    def newf(exc):
        """Rewrite this method so as to remove the traceback."""
        import traceback
        # Changed this bit, added the limit.
        exception_lines = traceback.format_exception(*exc, limit=0)
        lines = ''.join(exception_lines).splitlines(True)
        return tap.formatter.format_as_diagnostics(lines)
    tap.formatter.format_exception = newf

class Nict(dict):
    """Makes the dict a little more namespacey."""
    def __setattr__(self, name, value):
        self['name'] = value
    def __getattr__(self, name):
        try:
            return self['name']
        except KeyError:
            return None
    def copy(self):
        return Nict(dict.copy(self))

def read_properties() -> Nict:
    """Read the run options from the properties file and tidy them up a little."""
    conf = configparser.ConfigParser()
    conf.read(filenames='test.properties')
    result = Nict(conf['Main Section'])
    result.locales = result.locales.split(',')
    result.browser = result.browsers.split(',')
    result.tests = result.tests.split(',') if result.tests else []
    return result

if __name__ == '__main__':
    main()
