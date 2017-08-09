"""The test suite for the Investment website regression."""

from collections import OrderedDict
import components as CP
import selene

# A mapping of the test names to their abbreviations
invnames = OrderedDict(
    [('SPL', 'test_01_Splash_Page'),])

class INV(selene.MyTestCase):
    """The Test Suite for the Investment regression"""
    def test_01_Navigation(self) -> None:
        """Checks the various logos and links in the header"""
        self.dr.open_home_page()
        # Click the logo link
        with self.restraint('Logo link is missing',
                            AssertionError='Logo link did not go to homepage'):
            CP.NavMenu(self.dr).logo().click()
            self.assertEqual(self.globs['locale_url'], self.dr.current_url())

        # Click the Invest In Australia site link
        with self.restraint('Invest In Australia link is missing',
                            AssertionError='Invest In Australia link did not link to homepage'):
            CP.NavMenu(self.dr).current().click()
            self.assertEqual(self.globs['locale_url'], self.dr.current_url())

        # Click the 中国大陆 (简体中文) link        I assume you're testing the /en site, i guess??
        with self.restraint('INV CN Link is missing or did not open in new tab',
                            AssertionError='INV CN Link did not link to the CN Investment Site'):
            CP.NavMenu(self.dr).invcn().click()
            self.dr.switch_to_window(1)
            self.assertEqual(self.globs['base_url'] + '/zh.html', self.dr.current_url())   # hm
        # Back to the main window.
        self.dr.switch_to_window(0)

        # Check every link in the header nav, make sure they are correct
        # Assuming of course, that the PROD content is correct, and never changes
        nav = CP.NavMenu(self.dr)
        with self.restraint('Why Australia section was missing an option'):
            why = nav.WhyAustralia(self.dr).open()
            why.why_australia()
            why.resilient_growth_economy()
            why.easy_place_to_do_business()
            why.globally_significant_tourism_industry()
            why.strong_performing_accommodation_sector()
            why.aviation_access()
            why.world_class_tourism_offering()
            why.strong_events_calendar()
            why.tourism_demand_strategy()

        with self.restraint('Investment Opportunities section was missing an option'):
            oppo = nav.InvestmentOpportunities(self.dr).open()
            oppo.investment_opportunities()
            oppo.cities()
            oppo.beaches_and_island()
            oppo.nature_and_outback()
            oppo.food_and_wine()

        with self.restraint('Data Room section was missing an option'):
            dar = nav.DataRoom(self.dr).open()
            dar.data_room()
            dar.tourism_performance()
            dar.hotel_performance()
            dar.aviation()
            dar.the_markets()
            dar.success_stories()

        with self.restraint('About Us section was missing an option'):
            abu = nav.AboutUs(self.dr).open()
            abu.about_us()
            abu.how_we_can_help()
            abu.a_national_priority()
            abu.contact_us()
