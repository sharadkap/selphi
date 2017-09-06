"""A few custom classes, slight modifications to the basic unittest functionality.
Principally, to enable a different style of result output and recording."""
import sys
import time
import enum
import warnings
import unittest
from typing import Callable
from contextlib import contextmanager
from collections import OrderedDict
from drivery import Drivery

STATES = enum.Enum('STATES', 'PASS SKIP FAIL ERROR')

class JustStopError(unittest.TestCase.failureException):
    """Use this one if you want to crash a test, without logging another untreated exception."""

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
        self.dr = Drivery(self.globs)

    def tearDown(self) -> None:
        """Called after finishing each test, closes the browser and counts up the errors."""
        self.dr.close()
        self.maxDiff = None
        for err in self.verificationErrors:
            self.result.addFailure(self, err)

    @contextmanager
    def restraint(self, msg=None, backuphref: Callable = None, **errors):
        """Shortcut for logging: Used in a with statement, it'll log any errors that may appear.
        msg is the default message, used if none of the specific exception types in errors occur.
        Provide alternate messages with the kwargs like ZeroDivisionError="Can't divide by zero"
        backuphref should be a BackupHrefs' method reference. Mind you don't invoke it instead."""
        try:
            yield
        except:
            erty = sys.exc_info()[0].__name__
            if errors.get(erty):
                self.add_error(errors[erty])
            else:
                self.add_error(msg)
            if backuphref:
                backuphref()

    @contextmanager
    def destruction(self, msg=None, **errors):
        """Shortcut for error handling, but this one is for errors that warrant aborting the test.
        msg is the default message, or pass kwarged messages for specific exception types."""
        try:
            yield
        except:
            erty = sys.exc_info()[0].__name__
            if errors.get(erty):
                self.add_error(errors[erty])
            else:
                self.add_error(msg)
            raise JustStopError()

    def add_error(self, message=None) -> None:
        """Adds an error to the errors list. Shortcut.
        message is a more readable Error message"""
        self.verificationErrors.append(('' + message +':\n' if message else '') + self.tidy_error())

    def tidy_error(self, ex=None) -> str:
        """Reads exception info from sys.exc_info and only shows the lines that are from SELPHI
        Unless the DEBUG flag is True, in which case, it prints the entirety of the trace."""
        from os.path import join, abspath, dirname
        from traceback import extract_tb, format_list, format_exception_only
        # If the exception is already pasted into a string, just return that.
        if isinstance(ex, str):
            return ex

        show = join(dirname(abspath(__file__)), '')

        def _check_file(name):
            return name and name.startswith(show)

        def _print(typ, value, tb):  # If not debug, generator expression: filter trace to my files.
            show = extract_tb(tb) if self.globs['debug'] else (
                fs for fs in extract_tb(tb, limit=3) if _check_file(fs.filename))
            fmt = format_list(show) + format_exception_only(typ, value)
            return ''.join((f.strip('"\'').replace('\\n', '') for f in fmt))

        args = ex or sys.exc_info()
        return _print(*args)

class MyTestRunner(unittest.TextTestRunner):
    """Custom runner for this increasingly elabourate actually-readable-results-output hack"""
    def __init__(self, *args, **kwargs):
        super(MyTestRunner, self).__init__(*args, **kwargs)
        self.result = self._makeResult()

    def run(self, test):
        "Run the given test case or test suite. All this overload for one measly line."
        # result = self._makeResult()   Move this line into the init so I can mess with it interim.
        unittest.signals.registerResult(self.result)
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
        return test.tidy_error(err)

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
        # The JustStopError is raised by me, right after I have already logged the error in question
        if not isinstance(err, JustStopError):      # You can ignore it
            super(MyTestResult, self).addFailure(test, err)
            self.addResult(test, STATES.FAIL, test.tidy_error(err))

    def addError(self, test, err):
        """If a test crashed, make a note of that"""
        # The JustStopError is raised by me, right after I have already logged the error in question
        if not isinstance(err, JustStopError):      # You can ignore it
            super(MyTestResult, self).addError(test, err)
            self.addResult(test, STATES.ERROR, test.tidy_error(err))

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
