"""The test suite for the Investment website regression."""

import random
from collections import OrderedDict
import components as CP
import miklase

# A mapping of the test names to their abbreviations
invnames = OrderedDict(
    [('SPL', 'test_01_Splash_Page'),])

class INV(miklase.MyTestCase):
    """The Test Suite for the Investment regression"""
    def test_01_Navigation(self) -> None:
        """Checks the various logos and links in the header"""
        self.dr.open_home_page()
        # Click the logo link
        with self.restraint('Logo link missing', AssertionError='Logo link did not go to homepage'):
            CP.NavMenu(self.dr).logo().click()
            self.assertEqual(self.globs['locale_url'], self.dr.current_url())

        # Click the Invest In Australia site link
        with self.restraint('Invest In Australia link is missing',
                            AssertionError='Invest In Australia link did not link to homepage'):
            CP.NavMenu(self.dr).current().click()
            self.assertEqual(self.globs['locale_url'], self.dr.current_url())

        # Click the 中国大陆 (简体中文) link        I assume you're testing the /en site, i guess??
        with self.restraint('INV CN Link missing', IndexError='INV CN Link did not open in new tab',
                            AssertionError='INV CN Link did not link to the CN Investment Site'):
            CP.NavMenu(self.dr).invcn().click()
            self.dr.switch_to_window(1)
            self.assertEqual(self.globs['base_url'] + '/zh', self.dr.current_url())
        # Back to the main window.
        self.dr.close_other_windows()

        # Check every link in the header nav, make sure they are correct
        # Assuming of course, that the PROD content is correct, and never changes
        with self.destruction('Header Nav is missing'):
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

    def test_02_Hero(self) -> None:
        """Tests the Hero Banner's Pin It button, mostly"""
        self.dr.open_home_page()
        # Open a page with a Hero Banner
        with self.restraint('Why Australia link missing from nav',
                            CP.BackupHrefs(self.dr).why_australia):
            CP.NavMenu.WhyAustralia(self.dr).open().why_australia().click()
        # Find the banner and click the Pin It button
        with self.destruction('Hero banner Pin It button is missing'):
            CP.Hero(self.dr).pin_it()
        # Confirm the Pinterest window opens in a new window
        with self.restraint(IndexError='Pinterest link did not open in new window',
                            TimeoutException='Pin It button did not open Pinterest site.'):
            self.dr.switch_to_window(1)
            self.dr.wait_for_page('pinterest.com')

    def test_03_Share(self) -> None:
        """Tests the ShareThis functionality"""
        self.dr.open_home_page()
        # Open a page with a Share component and click the Share button
        with self.restraint('Why Australia link missing from nav',
                            CP.BackupHrefs(self.dr).why_australia):
            CP.NavMenu.WhyAustralia(self.dr).open().why_australia().click()
        # Confirm the AddThis window appears, and is populated with the page title
        with self.destruction('Share button missing from the page',
                              AssertionError='Page title is not shown in the share popup'):
            self.assertIn(CP.ShareThis(self.dr).open_share(), self.dr.page_title())

    def test_04_Search(self) -> None:
        """Tests the Site Search funtionality"""
        self.dr.open_home_page()
        search_term = 'Investment'
        # Enter a search term, there are no popular suggestions listed here
        with self.restraint('Search section is missing from the header'):
            CP.HeaderSearch(self.dr).open().search(search_term)
        # Should go to the Search page, and have the Results listed
        with self.destruction('Search Results component is missing',
                              TimeoutException='Search form did not redirect to the Search page'):
            self.dr.wait_for_page('search.html')
            search = CP.SiteSearch(self.dr)
        # Flip the view mode back and forth
        with self.restraint('Mode switching not working'):
            search.grid_mode()
            search.list_mode()
        # Click the View More results button, should load more results
        with self.restraint('Search Results\' View More button missing',
                            AssertionError='Viewing More did not increase result count'):
            fico = search.count_results()
            search.load_more()
            self.assertGreater(search.count_results(), fico)
        # The search results should actually contain the search term
        with self.restraint('Search Results did not all match the search term'):
            for res in search.get_all_results():
                self.assertIn(search_term, res.get_title() + res.get_summary())

    def test_05_Footer(self) -> None:
        """Tests the Footer functionality"""
        self.dr.open_home_page()
        # Find the footer
        with self.destruction('The Footer is missing'):
            fot = CP.Footer(self.dr)
        # About Us, About This Site, and External Sites links
        with self.restraint('Footer is missing a link'):
            fot.about_us()
            fot.contact_us()
            fot.sitemap()
            fot.terms_conditions()
            fot.austrade()
            fot.tourism_australia()
            fot.businessevents_australia()
            fot.australia()
        # Language Selector, the CN option should be present
        with self.restraint('Footer locales list is incorrect'):
            self.assertListEqual(['/en.html', '/zh.html'], fot.get_locales())
        with self.restraint('The CN locale link is not working'):
            fot.pick_locale('/zh.html')
            self.assertIn(self.globs['base_url'] + '/zh', self.dr.current_url())

    def test_06_Brightcove(self) -> None:
        """Tests the Brightcove Video functionality"""
        self.dr.open_home_page()
        # Find a video
        with self.restraint('World Class Tourism link is missing',
                            CP.BackupHrefs(self.dr).world_class_tourism_offering):
            CP.NavMenu.WhyAustralia(self.dr).open().world_class_tourism_offering().click()
        with self.destruction('Video is missing from the page',
                              TimeoutException='Video does not play when clicked'):
            vide = CP.Video(self.dr)
            vide.play()
            self.dr.wait_until(vide.is_playing, 'Waiting for video to be in the Playing state')

    def test_07_Mosaic(self) -> None:
        """Tests the Mosaic functionality, and that the PDFs are hosted correctly."""
        self.dr.open_home_page()
        # Go to a page with a Mosaic
        with self.restraint('Why Australia link is missing from the nav',
                            CP.BackupHrefs(self.dr).why_australia):
            CP.NavMenu.WhyAustralia(self.dr).open().why_australia().click()
        # Find the mosaic
        with self.restraint('Mosaic comonent missing from the page',
                            TimeoutException='Tile did not link to its page'):
            mos = CP.WhatYouCanSeeMosaic(self.dr)
            mos.random_selection(1)[0].go()
        # In case it was an external link
        self.dr.close_other_windows()
        # Find a page with PDFs Included
        with self.restraint('Data Room link is missing from the nav',
                            CP.BackupHrefs(self.dr).data_room):
            CP.NavMenu.DataRoom(self.dr).open().data_room().click()
        with self.restraint('Second Mosaic component is missing',
                            AssertionError='A PDF link did not go to the right environment'):
            mos = CP.WhatYouCanSeeMosaic(self.dr, 1)
            for tile in mos:
                self.assertIn(self.globs['base_url'], tile.get_link().get_attribute('href'))

    def test_08_Livefyre(self) -> None:
        """Tests the Livefyre functionality."""
        self.dr.open_home_page()
        # Find the Livefyre carousel
        with self.destruction('Livefyre component is missing'):
            liv = CP.Livefyre(self.dr)
        # Should have a description text
        with self.restraint('Livefyre missing the description paragraph'):
            self.assertGreater(liv.get_description(), '')
        with self.destruction('Livefyre component has no images'):
            til = random.choice(liv.tiles)
