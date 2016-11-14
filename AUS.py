"""Contains the Test Suite for the AUS.com regression and basically nothing else."""

import random
import unittest
from collections import OrderedDict
from drivery import Drivery
import components as CP

# A mapping of the test names to the abbreviations.
ausnames = OrderedDict(
    [('SOC', 'test_01_social'), ('KDP', 'test_02_kdp'), ('HDR', 'test_03_header'),
     ('FAV', 'test_04_favourites'), ('ITI', 'test_05_whitsundays'), ('SRC', 'test_06_search'),
     ('WYC', 'test_07_wycs'), ('OFF', 'test_08_special_offers'), ('BRT', 'test_09_brightcove'),
     ('BVD', 'test_10_banner_video'), ('XPL', 'test_11_explore')])

class AUS(unittest.TestCase):
    """The Test Suite for the AUS regression. Tests methods are numbered because HipTest."""
    def __init__(self, name, glob):
        super().__init__(methodName=name)
        self.globs = glob

    def setUp(self):
        """Called just before each test is run, sets up the browser and test records."""
        self.verificationErrors = []    # Keep a list of everything that went wrong.
        self.accept_next_alert = True
        self.dr = Drivery(self.globs)
        self.dr.open_home_page()

    def tearDown(self):
        """Called after finishing each test, closes the browser and counts up the errors."""
        self.dr.close()
        self.maxDiff = None
        self.assertEqual([], self.verificationErrors, 'This will fail if there were any nonlethal'
                         ' assertions. Hopefully the custom messages are helpful enough.')

    def add_error(self) -> None:
        """Adds an error to the errors list. Shortcut."""
        from selene import tidy_error    # Can I do this?
        self.verificationErrors.append(tidy_error())

    def test_01_social(self):   # Most of those branches are try/except. pylint: disable-msg=R0912
        """Tests the various Social Sharing components. WeChat/Weibo in CN, ShareThis elsewhere.
        Does not test the QR code links, can't seem to do that."""
        # Navigate to any page (e.g. http://www.australia.cn/zh-cn/planning/getting-around.html)
        try:
            if self.globs['cn_mode']:
                CP.NavMenu.PracticalInformation(self.dr).open().getting_around().click()
            else:
                CP.NavMenu.PlanYourTrip(self.dr).open().getting_around().click()
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).getting_around()
        # ShareThis compoent bit:
        try:
            # Click the Share icon
            share = CP.ShareThis(self.dr)
            share.open_share()
            if self.globs['cn_mode']:
                # Two icons should slide out from under it
                # Click the icon for WeChat (two chat balloon faces)
                share.open_wechat()
                qur = CP.QRCode(self.dr)
                # TODO: A QR code should appear, scan it.
                # self.dr.get(qur.decode())
                # TODO: Implement result: "The corresponding page opens in WeChat"
                # self.assertEqual(self.dr.current_url(), 'who even knows')
                # self.dr.back()
                # Close the QR code.
                qur.close()

                # Take some notes on the page for later comparison.
                desc = share.page_description()
                # img = share.page_image()
                url = self.dr.current_url()
                # Click the icon for Weibo (eyeball thing)
                share.open_weibo()
                # A window should pop up linking to service.weibo.com
                self.dr.switch_to_window(1)
                # It should contain the description of, images pulled from,
                # and a minified link to, the page
                weibo = CP.WeiboShare(self.dr)
                self.assertEqual(desc, weibo.page_description(), 'The Weibo message should default '
                                 'to the page description.')
                # The page image should be there, but the image filenames are all parameterized,
                # there's no way to confirm that it's the right image other than looking at it.
                # self.assertEqual(img, weibo.page_image(), "The page's image should be listed.")
                self.dr.get(weibo.miniurl())
                self.assertEqual(url, self.dr.current_url(), "The Weibo mini-url should resolve to "
                                 "the page's url.")
                self.dr.close_window()
            else:
                # TODO: Global Share Icon behaviour.
                self.skipTest("Haven't done global share component yet.")
        except Exception:
            self.add_error()
            self.dr.close_other_windows()

        # Footer bit:
        try:
            if self.globs['cn_mode']:
                # Click on the WeChat QR code/link in the footer
                footer = CP.Footer(self.dr)
                footer.wechat().click()
                # A QR code should appear in an overlay
                qur = CP.QRCode(self.dr)
                # TODO: Implement action: "Scan the QR code using your WeChat app"
                # self.dr.get(qur.decode())
                # TODO: Implement result: "The WeChat account belonging to TA China shows up"
                # self.assertEqual(self.dr.current_url(), 'who even knows')
                # self.dr.back()
                qur.close()

                # Click on the Sina Weibo image link
                footer.weibo().click()
                # A new tab/window opens to TA's Sina Weibo account (login to Sina Weibo required)
                self.dr.switch_to_window(1)
                # TODO: Maybe set up a weibo account and log in properly?
                self.assertRegex(self.dr.current_url(), 'weibo.com/(login.php|.+?seeaustralia)',
                                 'The link should go to the AUS.com Weibo page, '
                                 'or it may redirect to a login page.')
                self.dr.close_window()
            else:
                # TODO: Handle the global footer social media links
                self.skipTest("Haven't done global social links yet.")
        except Exception:
            self.add_error()
            self.dr.close_other_windows()

        # Navigate to the Aquatics page
        try:
            if self.globs['cn_mode']:
                CP.NavMenu.ExploreAndPlan(self.dr).open().aquatic().click()
            else:
                CP.NavMenu.ThingsToDo(self.dr).open().aquatic().click()
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).aquatic()
        pan = CP.PanoramicCarousel(self.dr)
        # Take some notes on the page for later comparison.
        # Click the watch video button
        desc, _ = pan.watch_video()
        # Click the other start video button
        pan.once_off_start_video()
        # Open the Menu, might not need to do this if you are fast enough
        # pan.open_video_menu()
        if self.globs['cn_mode']:
            # Click the WeChat icon
            pan.wechat()
            # A QR code appears
            qur = CP.QRCode(self.dr)
            # TODO: Implement action: "Scan the QR code using the WeChat app on your phone"
            # TODO: Implement result: "The corresponding page opens in WeChat"
            qur.close()

            # Click the Weibo icon
            pan.weibo()
            # A window should pop up linking to service.weibo.com
            self.dr.switch_to_window(1)
            # It should contain the description of, images pulled from,
            # and a minified link to, the video
            weibo = CP.WeiboShare(self.dr)
            self.assertEqual(desc, weibo.page_description(), 'The Weibo message should default'
                             ' to the video description.')
            # The page image should be there, but the image filenames are all parameterized,
            # there's no way to confirm that it's the right image other than looking at it.
            # self.assertEqual(img, weibo.page_image(), "The video preview image should be listed.")
            self.dr.get(weibo.miniurl())
            self.assertRegex(self.dr.current_url(), '(passport.)?weibo.com/(login.php)?',
                             "The Weibo mini-url should resolve to some Weibo page url.")
        else:
            # TODO: Do the global 360 share bit.
            pass

    def test_02_kdp(self):
        """Tests the KDP Partner Search functionality."""
        if not self.globs['cn_mode']:
            self.skipTest('Only China has the KDP thing.')
        # Navigate to the KDP page
        try:
            CP.NavMenu.ExploreAndPlan(self.dr).open().kdp().click()
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).kdp()
        # Count results, assert all buttons lit.
        kdp = CP.KDPSearch(self.dr)
        # North China, South China, East China and West China icons should all be active
        self.assertEqual(len(kdp.lit_icons()), 4)
        total = kdp.total_results()
        subtotal = 0
        # Click the South China button
        kdp.south()
        # The South China icon should remain cyan while the others turn white.
        self.assertEqual(kdp.lit_icons(), 's')
        self.assertLessEqual(kdp.total_results(), total)
        subtotal += kdp.total_results()
        # Do that for the remaining three regions (North China, East China and West China)
        kdp.east()
        self.assertEqual(kdp.lit_icons(), 'e')
        self.assertLessEqual(kdp.total_results(), total)
        subtotal += kdp.total_results()
        kdp.west()
        self.assertEqual(kdp.lit_icons(), 'w')
        self.assertLessEqual(kdp.total_results(), total)
        subtotal += kdp.total_results()
        kdp.north()
        self.assertEqual(kdp.lit_icons(), 'n')
        self.assertLessEqual(kdp.total_results(), total)
        subtotal += kdp.total_results()
        # And make sure that they all add to the total.
        self.assertEqual(total, subtotal)

    def test_03_header(self):
        """Tests the various menu sections in the header."""
        try:
            # Click the Australia.com logo in the header
            CP.NavMenu(self.dr).logo().click()
            # Should link to homepage
            self.assertEqual(self.dr.current_url(), self.globs['locale_url'])

            # Click the Holiday In Australia link in the header
            CP.NavMenu(self.dr).holiday().click()
            # Should link to homepage.
            self.assertEqual(self.dr.current_url(), self.globs['locale_url'])

            # Click the Business Events link in the header
            CP.NavMenu(self.dr).businessevents().click()
            # Should link to businessevents.australia.com/cn in new tab
            self.dr.switch_to_window(1)
            self.assertIn('businessevents.australia.c', self.dr.current_url())
            self.dr.close_window()
        except Exception:
            self.add_error()
            self.dr.close_other_windows()

        try:
            # Open the Explore section in the header
            if self.globs['cn_mode']:
                eap = CP.NavMenu.ExploreAndPlan(self.dr).open()
                # Verify existence of the three Explore+Planning sections.
                eap.aquatic()
                eap.city_journeys()
                eap.kdp()
            else:
                pass
                # TODO: Read the AUS.com test, replicate here.
        except Exception:
            self.add_error()

        # Open the Destinations section in the header
        ptg = CP.NavMenu.PlacesToGo(self.dr).open()
        # Confirm existence of Cities and Destinations sections and map thing.
        ptg.sydney()
        ptg.great_barrier_reef()
        # China does not have the AUS.com map.
        if not self.globs['cn_mode']:
            ptg.explore()

        # Click the States section switcher
        ptg.states().click()
        # Confirm the States section appeared.
        self.assertTrue(ptg.act().is_displayed())

    def test_04_favourites(self):
        """Tests the My Dream Trip functionality."""
        # Go to the Australia's Animals page
        try:
            if self.globs['cn_mode']:
                CP.NavMenu.PracticalInformation(self.dr).open().australias_animals().click()
            else:
                CP.NavMenu.PlanYourTrip(self.dr).open().facts().click()
                CP.WhatYouCanSeeMosaic(self.dr)["Australia's Animals"].click()
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).australias_animals()
        try:
            # Click the Add To Favourites button
            favcount = CP.HeaderHeartIcon(self.dr).favourites_count() + 1
            CP.ShareThis(self.dr).add_to_favourites()
            # Wait for the animation to finish and for confirmation of incremention
            self.dr.wait_until(lambda: CP.HeaderHeartIcon(self.dr).favourites_count() == favcount,
                               'Heart Icon count == favcount.')
            # Do that again with the Regional Cities page.
            try:
                CP.NavMenu.PlacesToGo(self.dr).open().regional_cities().click()
            except Exception:
                self.add_error()
                CP.BackupHrefs(self.dr).regional_cities()
            # Do this again, because the heart count doesn't load at the same time as the page.
            self.dr.wait_until(lambda: CP.HeaderHeartIcon(self.dr).favourites_count() == favcount,
                               'Heart Icon count == favcount.')
            favcount = CP.HeaderHeartIcon(self.dr).favourites_count() + 1
            CP.ShareThis(self.dr).add_to_favourites()
            self.dr.wait_until(lambda: CP.HeaderHeartIcon(self.dr).favourites_count() == favcount,
                               'Heart Icon count == favcount.')
        except Exception:
            self.add_error()

        # Go to favourites page. I would put a try-navigate here, but it's a dynamic url.
        CP.HeaderHeartIcon(self.dr).click()
        # Remove a favourite
        favs = CP.MySalesTools(self.dr).get_favourites()
        oldfavs = {f.get_title() for f in favs}
        rem = random.choice(favs)
        oldfavs.remove(rem.get_title())
        rem.close()
        # Confirm it was removed
        self.dr.refresh()
        favs = CP.MySalesTools(self.dr).get_favourites()
        self.assertSetEqual(oldfavs, {f.get_title() for f in favs})

    def test_05_whitsundays(self):
        """Tests various things pertaining to Itinerary pages."""
        # Navigate to Whitsundays Sailing
        try:
            if self.globs['cn_mode']:
                CP.NavMenu.ExploreAndPlan(self.dr).open().coastal_journeys().click()
                CP.WhatYouCanSeeMosaic(self.dr)['圣灵群岛航海游'].go()
            else:
                CP.NavMenu.ThingsToDo(self.dr).open().coastal_journeys().click()
                CP.WhatYouCanSeeMosaic(self.dr)['Whitsundays Sailing'].go()
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).whitsundays()

        # Click a few of the Itinerary Day links
        iti = CP.ItineraryDay(self.dr)
        # Get the scroll position of that bit.
        scr = self.dr.current_scroll()
        iti.random_link()
        # Confirm scrolling has taken place?
        self.assertNotEqual(scr, self.dr.current_scroll())
        iti.back_to_top()
        self.assertEqual(0, self.dr.current_scroll())

    def test_06_search(self):
        """Tests the Site and Header Search functionalities."""
        # Do this a couple of times, different buttons:
        # Opens the Search bar, clicks a Common Search Term
        for _ in CP.HeaderSearch.popular_searches(self.dr, 3):
            try:
                src = CP.SiteSearch(self.dr)
                # Change the view?
                src.grid_mode()
                # Change back ?
                src.list_mode()
                # Click Load more
                count = src.count_results()
                src.load_more()
                # Confirm the count is incremented?
                self.assertGreaterEqual(count, src.count_results())
            except Exception:
                self.add_error()

    def test_07_wycs(self):
        """Tests the What You-Can-See-Mosaic-related functionality."""
        # Navigate to the Three Days Itineraries page
        try:
            if self.globs['cn_mode']:
                CP.NavMenu.ExploreAndPlan(self.dr).open().city_journeys().click()
            else:
                CP.NavMenu.ThingsToDo(self.dr).open().city_journeys().click()
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).city_journeys()
        # Click on a tile, should direct to the correct page while the other tiles grey out
        try:
            CP.WhatYouCanSeeMosaic(self.dr).random_selection(1)[0].go()
            # Some of them go to external sites which open in a new tab.
            self.dr.close_other_windows()
        except Exception:
            self.add_error()
            self.dr.close_other_windows()

        # Go to the Great Barrier Reef page
        try:
            CP.NavMenu.PlacesToGo(self.dr).open().great_barrier_reef().click()
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).great_barrier_reef()
        # Click on a tile, should direct to the correct page, other tiles faded
        CP.WhatYouCanSeeMosaic(self.dr).random_selection(1)[0].go()

    def test_08_special_offers(self):
        """Tests the Special Offers page"""
        # Navigate to the Special Offers page
        try:
            if self.globs['cn_mode']:
                CP.NavMenu.ExploreAndPlan(self.dr).open().specialoffers().click()
            else:
                CP.NavMenu.ThingsToDo(self.dr).open().campaigns().click()
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).offers()
        # Click on a Special Offers link
        CP.SpecialOffer(self.dr).view_more_information()

    def test_09_brightcove(self):
        """Tests the Brightcove Video Player."""
        # Go to the Tasmania page
        try:
            pla = CP.NavMenu.PlacesToGo(self.dr).open()
            pla.states().click()
            pla.tas().click()
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).tas()
        # Play the video.
        vid = CP.Video(self.dr)
        vid.play()

    def test_10_banner_video(self):
        """Tests the Hero Banner With Video."""
        # Navigate to the Australia's Animals page
        if self.globs['cn_mode']:
            CP.NavMenu.PracticalInformation(self.dr).open().australias_animals().click()
        else:
            CP.NavMenu.PlanYourTrip(self.dr).open().facts().click()
            CP.WhatYouCanSeeMosaic(self.dr)["Australia's Animals"].go()
        # Verify that the hero banner is animated. This seems to count?
        self.assertTrue(CP.Video(self.dr).is_playing())

    def test_11_explore(self):
        """Tests the Explore component."""
        # Navigate to the Sydney page
        try:
            CP.NavMenu.PlacesToGo(self.dr).open().sydney().click()
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).sydney()
        # Click the Location Pin button on a the Explore component
        cards = CP.Explore(self.dr).cards
        for card in cards:
            card.flip()
        # Confirm that the card flipped
        for card in cards:
            self.assertTrue(card.is_flipped())
        # Click the back to overview button
        for card in cards:
            card.unflip()
        for card in cards:
            self.assertFalse(card.is_flipped())
        # Add some to favourites
        count = CP.HeaderHeartIcon(self.dr).favourites_count()
        for card in cards:
            card.add_to_favourites()
        # Confirm favourites incremented
        self.dr.wait_until(lambda: count + 3 == CP.HeaderHeartIcon(self.dr).favourites_count(),
                           'count + 3 equals favourites.count.')

if __name__ == '__main__':
    unittest.main()
