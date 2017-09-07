"""The test suite for the Investment website regression."""

import random
from collections import OrderedDict
import components as CP
import miklase

# A mapping of the test names to their abbreviations
invnames = OrderedDict(
    [('NAV', 'test_01_Navigation'), ('HER', 'test_02_Hero'), ('SHR', 'test_03_Share'),
     ('SER', 'test_04_Search'), ('FOO', 'test_05_Footer'), ('VID', 'test_06_Brightcove'),
     ('MOS', 'test_07_Mosaic'), ('LFR', 'test_08_Livefyre'), ('FIL', 'test_09_FilteredSearch'),
     ('MAP', 'test_10_Sitemap'), ])

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
            oppo.beaches_and_islands()
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
        search_term = random.choice('Aviation Hotel Data National Market Strategy Business'.split())
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
        with self.restraint('Search Results\' View More button missing (' + search_term + ')',
                            AssertionError='Viewing More did not increase result count (' + search_term + ')'):
            fico = search.count_results()
            search.load_more()
            self.assertGreater(search.count_results(), fico)
        # The search results should actually contain the search term
        with self.restraint('Could not get a result\'s text (' + search_term + ')',
                            AssertionError='Search Results did not all match the search term (' + search_term + ')'):
            for res in search.get_all_results():
                if not search_term.casefold() in (res.get_title() + res.get_summary()).casefold():
                    res.view_more_information(True)
                    self.assertIn(search_term.casefold(), CP.Page(self.dr).text())
                    self.dr.close_other_windows()

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
        with self.restraint('Tourism Demand Strategy link is missing',
                            CP.BackupHrefs(self.dr).tourism_demand_strategy):
            CP.NavMenu.WhyAustralia(self.dr).open().tourism_demand_strategy().click()
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
            for tile in mos:    # Eeh, the AUTH throws it off a bit. Trim https bit to compensate
                self.assertIn(self.globs['base_url'][8:], tile.get_link())

    def test_08_Livefyre(self) -> None:
        """Tests the Livefyre functionality."""
        self.dr.open_home_page()
        # Find the Livefyre carousel
        with self.destruction('Livefyre component is missing or has no tile content'):
            liv = CP.Livefyre(self.dr)
            til = random.choice([x for x in liv.tiles if x.is_displayed()])
        # Should have a description text
        with self.restraint('Livefyre missing the description paragraph'):
            self.assertGreater(liv.get_description(), '')
        with til:
            # Open a link
            with self.restraint('No links are present in the photo description'):
                lin = random.choice(til.get_links())
                te = lin.text
                lin.click()
                with self.restraint(IndexError='Link did not open in a new tab', AssertionError=
                                    'Link did not go to the relevant Instagram page'):
                    self.dr.switch_to_window(1)
                    self.assertIn('instagram', self.dr.current_url())
                    self.assertIn(te[1:], self.dr.current_url())
            self.dr.close_other_windows()
            # Check the Share button
            with self.restraint('Could not open the Share interface'):
                til.share()
                til.close_share()
        # If the livefyre is in Mosaic mode, try clicking the Load More
        with self.restraint('Could not view more on the Livefyre Mosaic', AssertionError=
                            'Clicking Load More on the Livefyre Mosaic did not load more tiles'):
            fir = len(liv.tiles)
            liv.view_more()
            self.assertGreater(len(liv.tiles), fir)
        # # If the Livefyre is in Carousel mode, try scrolling across it
        # with self.restraint('Could not scroll the Livefyre Carousel', AssertionError=
        #                     'Scrolling the Livefyre Carousel did not change the tiles visible'):
        #     fir = [x for x, y in enumerate(liv.tiles) if y.is_displayed()]
        #     liv.scroll()
        #     sec = [x for x, y in enumerate(liv.tiles) if y.is_displayed()]
        #     self.assertNotEqual(fir, sec)

    def test_09_FilteredSearch(self) -> None:
        """Tests the Filtered Search functionality."""
        self.dr.open_home_page()
        # Go to the Contact Us page
        with self.restraint('Cannot get to the Contact Us page via the footer link',
                            CP.BackupHrefs(self.dr).contact_inv):
            CP.Footer(self.dr).contact_us().click()
        # Get the contact Search
        with self.destruction('The Contact Us page is missing the Filtered Search component'):
            fil = CP.FilteredSearch(self.dr)
        with self.destruction('No contact search results are present'):
            ress = fil.get_all_results()
        # Check each of the results has a name, an email address, and a phone link
        with self.restraint('Results are missing fields'):
            for res in ress:
                self.assertGreater(res.name(), ''), res.email(), res.phone()
        # Add some filters, and confirm that filtering did, in fact, occur
        with self.restraint('Unable to apply a search filter', AssertionError=
                            'Filtering the search did not change the results present'):
            fil.random_search()
            self.assertNotEqual(ress, fil.get_all_results())

    def test_10_Sitemap(self) -> None:
        """Tests the Sitemap functionality."""
        self.dr.open_home_page()
        # Go to the sitemap page, and get the Sitemap
        with self.restraint('Cannot get to sitemap page via footer nav',
                            CP.BackupHrefs(self.dr).sitemap):
            CP.Footer(self.dr).sitemap().click()
        with self.destruction('Sitemap is missing from the sitemap page'):
            sma = CP.Sitemap(self.dr)
        # Sitemap should have links to each of the pages in the Nav Menu
        with self.restraint('Could not collect list of nav/sitemap links',
                            AssertionError='The sitemap/nav menu link sets do not match'):
            nav_links = CP.NavMenu(self.dr).get_all_links()
            sitemap_links = sma.get_all_links()
            self.assertTrue(nav_links.issubset(sitemap_links))
        # And should also links corresponding to the footer links
        with self.restraint('Could not collect the list of footer links',
                            AssertionError='The sitemap/footer link sets do not match'):
            fo = CP.Footer(self.dr)
            fo_li = fo.get_all_links()
            self.assertTrue(fo_li.issubset(sitemap_links))
        # And, a bit for the languages
        with self.restraint('Could not collect the list of locales',
                            AssertionError='The sitemap/footer locales sets do not match'):
            loc = {self.dr.base_url + f.replace('.html', '/sitemap.html') for f in fo.get_locales()}
            self.assertTrue(loc.issubset(sitemap_links))
