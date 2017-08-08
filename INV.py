"""The test suite for the Investment website regression."""

import unittest
from collections import OrderedDict
from drivery import Drivery
from selene import tidy_error
import components as CP

# A mapping of the test names to their abbreviations
invnames = OrderedDict(
    [('SPL', 'test_01_Splash_Page'),])

class INV(unittest.TestCase): # pylint: disable=R0904
    """The Test Suite for the Investment regression"""
    def __init__(self, name: str, glob: dict, result: 'MyTestResult'):
        super().__init__(methodName=name)
        self.globs = glob
        self.result = result

    def setUp(self) -> None:
        """Called just before each test is run, sets up the browser and test records"""
        # Initialise the browser connection.
        self.verificationErrors = []    # Keep a list of everything that went wrong.
        self.accept_next_alert = True
        self.dr = Drivery(self.globs)
        self.dr.open_home_page()

    def tearDown(self) -> None:
        """Called after finishing each test, closes the browser and counts up the errors"""
        self.dr.close()
        self.maxDiff = None
        for err in self.verificationErrors:
            self.result.addFailure(self, err)

    def add_error(self) -> None:
        """Adds an error to the errors list. Shortcut"""
        # from selene import tidy_error
        self.verificationErrors.append(tidy_error())

    # Tests start here.
    def test_01_TA_Logo_Link(self) -> None:
        """Checks the TA logo in the header"""
