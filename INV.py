"""The test suite for the Investment website regression."""

import unittest
from collections import OrderedDict
from drivery import Drivery
import selene
import components as CP

# A mapping of the test names to their abbreviations
invnames = OrderedDict(
    [('SPL', 'test_01_Splash_Page'),])

class INV(selene.MyTestCase): # pylint: disable=R0904
    """The Test Suite for the Investment regression"""
    def test_01_Navigation(self) -> None:
        """Checks the various logos and links in the header"""
        self.dr.open_home_page()
        # Click the logo link
        CP.NavMenu(self.dr).logo().click()
        with self.restraint('Logo link did not go to homepage'):
            self.assertEqual(self.globs['locale_url'], self.dr.current_url())

        # Click the Invest In Australia site link
        CP.NavMenu(self.dr).current().click()
        with self.restraint('Invest In Australia link did not link to Investment Site'):
            self.assertEqual(self.globs['locale_url'], self.dr.current_url())

        # Click the 中国大陆 (简体中文) link
        CP.NavMenu(self.dr).invcn().click()
        with self.restraint('INV CN Link did not open in new tab',
                            AssertionError='INV CN Link did not link to the CN Investment Site'):
            self.dr.switch_to_window(1)
            self.assertEqual(self.globs['base_url'] + '/zh.html', self.dr.current_url())   # uh

        self.dr.switch_to_window(0)
