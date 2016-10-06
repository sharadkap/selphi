"""Contains the Test Suite for the AUS.com regression and basically nothing else."""

import random
import unittest
from collections import OrderedDict
import drivery as DR
import components as CP

ausnames = OrderedDict(
    [('SOC', 'test_social'), ('KDP', 'test_kdp'), ('HDR', 'test_header'),
     ('FAV', 'test_favourites'), ('ITI', 'test_whitsundays'), ('360', 'test_360'),
     ('SRC', 'test_search'), ('WYC', 'test_wycs'), ('OFF', 'test_special_offers'),
     ('BRT', 'test_brightcove'), ('BVD', 'test_banner_video'), ('XPL', 'test_explore'), ])

class AUS(unittest.TestCase):
    """The Test Suite for the AUS.com regression."""
    def setUp(self):
        """Called just before each test is run, sets up the browser and test records."""
        DR.verificationErrors = []    # This might work. Keep a list of everything that went wrong.
        self.accept_next_alert = True
        DR.begin()
        DR.CN_MODE = True
        DR.BASE_URL = "http://www.australia.cn"
        DR.LOCALE = '/zh-cn'
        DR.open_home_page()

    def tearDown(self):
        """Called after finishing each test, closes the browser and counts up the errors."""
        DR.close()
        self.maxDiff = None
        self.assertEqual([], DR.verificationErrors, '\nThis will fail if there were any nonlethal \
            assertions. Hopefully the custom messages are helpful enough.')

    def test_social(self):
        """Tests the various Social Sharing components. WeChat/Weibo in CN, ShareThis elsewhere.
        Does not test the QR code links, can't seem to do that."""
        # Navigate to any page (e.g. http://www.australia.cn/zh-cn/planning/getting-around.html)
        try:
            if DR.CN_MODE:
                CP.NavMenu.PracticalInformation().open().getting_around().click()
            else:
                CP.NavMenu.PlanYourTrip().open().getting_around().click()
        except Exception as ex:
            DR.add_error(ex)
            CP.BackupHrefs.getting_around()
        # ShareThis compoent bit:
        try:
            # Click the Share icon
            share = CP.ShareThis()
            share.open_share()
            if DR.CN_MODE:
                # Two icons should slide out from under it
                # Click the icon for WeChat (two chat balloon faces)
                share.open_wechat()
                qur = CP.QRCode()
                # TODO: A QR code should appear, scan it.
                # DR.get(qur.decode())
                # TODO: Implement result: "The corresponding page opens in WeChat"
                # self.assertEqual(DR.current_url(), 'who even knows')
                # DR.back()
                # Close the QR code.
                qur.close()

                # Take some notes on the page for later comparison.
                desc = share.page_description()
                img = share.page_image()
                url = DR.current_url()
                # Click the icon for Weibo (eyeball thing)
                share.open_weibo()
                # A window should pop up linking to service.weibo.com
                DR.switch_to_window(1)
                # It should contain the description of, images pulled from,
                # and a minified link to, the page
                weibo = CP.WeiboShare()
                self.assertEqual(desc, weibo.page_description(), 'The Weibo message should default'
                                 ' to the page description.')
                self.assertEqual(img, weibo.page_image(), "The page's Hero image should be listed.")
                DR.get(weibo.miniurl())
                self.assertEqual(url, DR.current_url(), "The Weibo mini-url should resolve to the "
                                 "page's url.")
                DR.close_window()
            else:
                # TODO: Global Share Icon behaviour.
                self.skipTest('Haven\'t done global share component yet.')
        except Exception as ex:
            DR.add_error(ex)
            DR.close_other_windows()

        # Footer bit:
        try:
            if DR.CN_MODE:
                # Click on the WeChat QR code/link in the footer
                footer = CP.Footer()
                footer.wechat().click()
                # A QR code should appear in an overlay
                qur = CP.QRCode()
                # TODO: Implement action: "Scan the QR code using your WeChat app"
                # DR.get(qur.decode())
                # TODO: Implement result: "The WeChat account belonging to TA China shows up"
                # self.assertEqual(DR.current_url(), 'who even knows')
                # DR.back()
                qur.close()

                # Click on the Sina Weibo image link
                footer.weibo().click()
                # A new tab/window opens to TA's Sina Weibo account (login to Sina Weibo required)
                DR.switch_to_window(1)
                # TODO: Maybe set up a weibo account and log in properly?
                self.assertRegex(DR.current_url(), '^weibo.com/(login.php|seeaustralia)',
                                 'The link should go to the AUS.com Weibo page, '
                                 'or it may redirect to the login page.')
                DR.close_window()
            else:
                # TODO: Handle the global footer social media links
                self.skipTest('Haven\'t done global social links yet.')
        except Exception as ex:
            DR.add_error(ex)
            DR.close_other_windows()

        # Navigate to the Aquatics page
        try:
            if DR.CN_MODE:
                CP.NavMenu.ExploreAndPlan().open().aquatic().click()
            else:
                CP.NavMenu.ThingsToDo().open().aquatic().click()
        except Exception as ex:
            DR.add_error(ex)
            CP.BackupHrefs.aquatic()
        pan = CP.PanoramicCarousel()
        # Take some notes on the page for later comparison.
        url = DR.current_url()
        # Click the watch video button
        desc, img = pan.watch_video()
        # Click the other start video button
        pan.once_off_start_video()
        # Open the Menu, might not need to do this if you are fast enough
        pan.open_video_menu()
        if DR.CN_MODE:
            # Click the WeChat icon
            pan.wechat()
            # A QR code appears
            qur = CP.QRCode()
            # TODO: Implement action: "Scan the QR code using the WeChat app on your phone"
            # TODO: Implement result: "The corresponding page opens in WeChat"
            qur.close()

            # Click the Weibo icon
            pan.weibo()
            # A window should pop up linking to service.weibo.com
            DR.switch_to_window(1)
            # It should contain the description of, images pulled from,
            # and a minified link to, the video
            weibo = CP.WeiboShare()
            self.assertEqual(desc, weibo.page_description(), 'The Weibo message should default'
                             ' to the video description.')
            self.assertEqual(img, weibo.page_image(), "The video's preview image should be listed.")
            DR.get(weibo.miniurl())
            self.assertEqual(url, DR.current_url(), "The Weibo mini-url should resolve to the "
                             "video's page url.")
        else:
            # TODO: Do the global 360 share bit.
            pass

    def test_kdp(self):
        """Tests the KDP Partner Search functionality."""
        if not DR.CN_MODE:
            self.skipTest('Only China has the KDP thing.')
        # Navigate to the KDP page
        CP.NavMenu.ExploreAndPlan().open().kdp().click()
        # Count results, assert all buttons lit.
        kdp = CP.KDPSearch()
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

    def test_header(self):
        """Tests the various men usections in the header."""
        # Click the Australia.com logo in the header
        CP.NavMenu().logo().click()
        # Should link to homepage
        self.assertEqual(DR.current_url(), DR.BASE_URL + DR.LOCALE)

        # Click the Holiday In Australia link in the header
        CP.NavMenu().holiday().click()
        # Should link to homepage.
        self.assertEqual(DR.current_url(), DR.BASE_URL + DR.LOCALE)

        # Click the Business Events link in the header
        CP.NavMenu().business_events().click()
        # Should link to businessevents.australia.com/cn in new tab
        DR.switch_to_window(1)
        self.assertIn('businessevents.australia.c', DR.current_url())
        DR.switch_to_window(0)

        # Open the Explore section in the header
        if DR.CN_MODE:
            eap = CP.NavMenu.ExploreAndPlan().open()
            # Verify existence of the three Explore+Planning sections.
            eap.aquatic()
            eap.city_journeys()
            eap.kpd()
        else:
            pass
            # TODO: Read the AUS.com test, replicate here.

        # Open the Destinations section in the header
        ptg = CP.NavMenu.PlacesToGo().open()
        # Confirm existence of Cities and Destinations sections and map thing.
        ptg.sydney()
        ptg.great_barrier_reef()
        ptg.explore()

        # Click the States section switcher
        ptg.states().click()
        # Confirm the States section appeared.
        self.assertTrue(ptg.act().is_displayed())


    def test_favourites(self):
        """Tests the My Dream Trip functionality."""
        # Go to the Australia's Animals page
        if DR.CN_MODE:
            CP.NavMenu.PracticalInformation().open().australias_animals().click()
        else:
            CP.NavMenu.PlanYourTrip().open().facts().click()
            CP.WhatYouCanSeeMosaic()['Australia\'s Animals'].click()
        # Click the Add To Favourites button
        favcount = CP.HeaderHeartIcon().favourites_count()
        CP.ShareThis().add_to_favourites()
        # Wait for the animation to finish
        # confirm incremention
        self.assertEqual(CP.HeaderHeartIcon().favourites_count(), favcount + 1)
        # Do that again with the Regional Cities page.
        CP.NavMenu.PlacesToGo().open().regional_cities().click()
        favcount = CP.HeaderHeartIcon().favourites_count()
        CP.ShareThis().add_to_favourites()
        self.assertEqual(CP.HeaderHeartIcon().favourites_count(), favcount + 1)

        # Go to favourites page
        CP.HeaderHeartIcon().click()
        # Remove a favourite
        favs = CP.MySalesTools().get_favourites()
        oldfavs = {f.get_title() for f in favs}
        rem = random.choice(favs)
        oldfavs.remove(rem.get_title())
        rem.close()
        # Confirm it was removed
        DR.refresh()
        favs = CP.MySalesTools().get_favourites()
        self.assertSetEqual(oldfavs, {f.get_title() for f in favs})

    def test_whitsundays(self):
        """Tests various things pertaining to Itinerary pages."""
        # Navigate to Whitsundays Sailing
        if DR.CN_MODE:
            CP.NavMenu.ExploreAndPlan().open().coastal_journeys().click()
        else:
            CP.NavMenu.ThingsToDo().open().coastal_journeys().click()
        CP.WhatYouCanSeeMosaic()['Whitsundays Sailing'].go()

        # Click a few of the Itinerary Day links
        iti = CP.ItineraryDay()
        # Get the scroll position of that bit.
        scr = DR.current_scroll()
        iti.random_link()
        # Confirm scrolling has taken place?
        self.assertNotEqual(scr, DR.current_scroll())
        iti.back_to_top()
        self.assertEqual(0, DR.current_scroll())

    def test_360(self):
        """Checks the Aquatic And Coastal page. Slightly."""
        # Navigate to Acquatic And Coastal
        if DR.CN_MODE:
            CP.NavMenu.ExploreAndPlan().open().aquatic().click()
        else:
            CP.NavMenu.ThingsToDo().open().aquatic().click()
        # Confirm the Panorama is there??
        CP.PanoramicCarousel()

        # Not part of the test, but go do a bunch of stuff with the video maybe?

    def test_search(self):
        """Tests the Site and Header Search functionalities."""
        # Do this a couple of times, different buttons:
        for term in CP.HeaderSearch().popular_searches():
            # Open the Search bar
            CP.HeaderSearch().open()
            # Click a Common Search Term
            term.click()
            src = CP.SiteSearch()
            # Change the view?
            src.grid_mode()
            # Change back ?
            src.list_mode()
            # Click Load more
            count = src.count_results()
            src.load_more()
            # Confirm the count is incremented?
            self.assertGreaterEqual(count, src.count_results())

    def test_wycs(self):
        """Tests the What You-Can-See-Mosaic-related functionality."""
        # Navigate to the Three Days Itineraries page
        if DR.CN_MODE:
            CP.NavMenu.ExploreAndPlan().open().city_journeys().click()
        else:
            CP.NavMenu.ThingsToDo().open().city_journeys().click()
        # Click on a tile, should direct to the correct page while the other tiles grey out
        CP.WhatYouCanSeeMosaic().random_selection(1)[0].go()

        # Go to the Great Barrier Reef page
        CP.NavMenu.PlacesToGo().open().great_barrier_reef().click()
        # Click on a tile, should direct to the correct page, other tiles faded
        CP.WhatYouCanSeeMosaic().random_selection(1)[0].go()

    def test_special_offers(self):
        """Tests the Special Offers page"""
        # Navigate to the Special Offers page
        if DR.CN_MODE:
            CP.NavMenu.ExploreAndPlan().open().specialoffers().click()
        else:
            CP.NavMenu.ThingsToDo().open().campaigns().click()
        # Click on a Special Offers link
        CP.SpecialOffer().view_more_information()

    def test_brightcove(self):
        """Tests the Brightcove Video Player."""
        # Go to the Tasmania page
        pla = CP.NavMenu.PlacesToGo().open()
        pla.states().click()
        pla.tas().click()
        # Play the video somehow, check that it worked?
        vid = CP.Video()
        vid.play()
        self.assertTrue(vid.is_playing())

    def test_banner_video(self):
        """Tests the Hero Banner With Video."""
        # Navigate to the Australia's Animals page
        if DR.CN_MODE:
            CP.NavMenu.PracticalInformation().open().australias_animals().click()
        else:
            CP.NavMenu.PlanYourTrip().open().facts().click()
            CP.WhatYouCanSeeMosaic()['Australia\'s Animals'].go()
        # Verify that the hero banner is animated. This seems to count?
        self.assertTrue(CP.Video().is_playing())

    def test_explore(self):
        """Tests the Explore component."""
        # Navigate to the Sydney page
        CP.NavMenu.PlacesToGo().open().sydney().click()
        # Click the Location Pin button on a the Explore component
        cards = CP.Explore().cards
        for card in cards:
            card.flip()
        # Confirm that the card flipped
        for card in cards:
            self.assertTrue(card.is_flipped())
        # Click the back to overview button
        for card in cards():
            card.unflip()
        for card in cards:
            self.assertFalse(card.is_flipped())
        # Add some to favourites
        count = CP.HeaderHeartIcon().favourites_count()
        for card in cards:
            card.add_to_favourites()
        # Confirm favourites incremented
        self.assertEqual(count + 3, CP.HeaderHeartIcon().favourites_count())
