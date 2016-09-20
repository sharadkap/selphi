"""Test execution goes in here, but no browser interaction implementation details.
Nonfatal Assertions are a bit of a mess, but whatever, can't really refactor control flow."""

import os
import io
import sys
import time
import argparse
import unittest
from multiprocessing import cpu_count
from multiprocessing.pool import Pool
import tap
import drivery as DR
import modules as MOD

from ASP import ASP, aspnames

def main():
    """Read the arguments, run the tests."""
    global USERNAME, USERID        # I'm sure it's fine. pylint: disable-msg=W0601

    parser = argparse.ArgumentParser()
    m = parser.add_mutually_exclusive_group()
    m.add_argument('--asp', help='Set this flag to run with the ASP regression test suite.',
                        action='store_true')
    parser.add_argument('-e', '--environment', help='The Domain of the environment to test. \
                        Remember to include http(s). Default is %(default)s.', nargs=1, type=str,
                        default=[DR.BASE_URL], metavar='')
    parser.add_argument('-ce', '--chenvironment', help='The Domain of the China environment to \
                        test (if applicable). Remember to include http(s). Default is %(default)s.',
                        nargs=1, type=str, default=[DR.CN_BASE_URL], metavar='')
    parser.add_argument('-l', '--locales', help='Which locales to test. \
                        One or more of [%(choices)s]. Default is %(default)s.',
                        nargs='+', type=str, choices=DR.LOCALES.keys(), default=['gb'], metavar='')
    parser.add_argument('-b', '--browser', help='Which browser to use. One or more of \
                        [%(choices)s]. Default is %(default)s', nargs='+', default=['chrome'],
                        choices=DR.BROWSERS.keys(), metavar='')
    parser.add_argument('-u', '--username', help='The Username to use in testing. \
        Due to the way the tests are structured, it will have to be a Test Account formatted user: \
        last four characters the email subaddress code (testeratta+xxxx@gmail.com), \
        password Welcome1. Only do this if your custom suite does not include Registration. \
        Likely won\'t work if you have multiple locales.', default=[None], nargs=1, metavar='')
    parser.add_argument('-t', '--tests', help='Which tests to run. Will be run in the order \
                    supplied. Default is all, in the default testing order. Choices are [{}]'
                        .format(', '.join(["'{}' for {}"
                                           .format(x, aspnames[x]) for x in aspnames])),
                        nargs='+', choices=aspnames.keys(), default=aspnames.keys(),
                        type=str, metavar='')
    args = parser.parse_args()

    # Set the settings from the given arguments
    if args.username[0]:
        USERNAME = args.username[0]
        USERID = USERNAME[-4:]    # The mail ID is the last four characters.
        DR.EMAIL = DR.EMAIL.format(USERID)
    else:
        USERNAME, USERID = None, None

    # Get the output settings, the chosen test methods from the ASP suite.
    outdir = os.path.split(__file__)[0]
    names = [ASP(aspnames[x]) for x in args.tests]

    # Run them in each locale.
    pool = Pool(cpu_count() * 2)  # It's mostly waiting; we can afford to overload the cores, right?
    pool.map(launch_test, [(loc, bro, outdir, names, USERNAME, USERID,
                            [args.environment[0], args.chenvironment[0]])
                           for loc in args.locales for bro in args.browser])

def launch_test(args) -> None:
    """Do all the things needed to run a test suite. Put this as the target call of a process.
    It looks like this is messing with things on a Global level, but it's actually totally fine."""
    # These have t obe here, otherwise the processes won't have access to it.
    # pylint: disable-msg=E1126, W0601
    global USERNAME, USERID
    locale, browser, outdir, names, USERNAME, USERID, env = args
    # Processes don't share global state, but the processes get reused, so have to clean up anyway.
    DR.reset_globals()
    # Do a bunch of method overrides to get it to work properly.
    perform_hacks()
    # If a url was given, make that the default.
    DR.BASE_URL = env[0]
    DR.CN_BASE_URL = env[1]
    # Set up the run settings.
    DR.BROWSER_TYPE = DR.BROWSERS[browser]
    # If China Mode, do it in China, otherwise set the locale
    if locale == 'cn':
        DR.CN_MODE = True
        DR.LOCALE = DR.CN_LOCALE
        DR.BASE_URL = DR.CN_BASE_URL
    else:
        DR.LOCALE = DR.LOCALES[locale]

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
            DR.scroll_element(args[0])
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
    # Also, tap has its own renderer as well, so have to overwrite that as well.
    def newf(exc):
        """Rewrite this method so as to remove the traceback."""
        import traceback
        # Changed this bit, added the limit.
        exception_lines = traceback.format_exception(*exc, limit=0)
        lines = ''.join(exception_lines).splitlines(True)
        return tap.formatter.format_as_diagnostics(lines)
    tap.formatter.format_exception = newf


if __name__ == '__main__':
    main()
