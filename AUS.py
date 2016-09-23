"""Contains the Test Suite for the AUS.com regression and basically nothing else."""

import os
import unittest
from selenium import webdriver
import tap
import drivery as DR
import components as CP

class AUS(unittest.TestCase):
    """The Test Suite for the AUS.com regression."""
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://www.australia.cn"
        self.verificationErrors = []
        self.driver.get(self.base_url + "/zh-cn")

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

    def test_social(self):
        # Navigate to any page (e.g. http://www.australia.cn/zh-cn/planning/getting-around.html)
        CP.PlanYourTrip().open().getting_around().click()
        # Click the Share icon
        share = CP.ShareThis().share()
        share.open()
        # Two icons should slide out from under it
        # Click the icon for WeChat (two chat balloon faces)
        share.wechat()
        qur = CP.QRCode()
        # A QR code should appear
        # TODO: Implement action: "Scan the QR code using the WeChat app on your phone"
        # TODO: Implement result: "The corresponding page opens in WeChat"
        # Close the QR code.
        qur.close()

        # Click the icon for Weibo (eyeball thing)
        share.weibo()
        # TODO: Implement result: "A window should pop up linking to service.weibo.com"
        # TODO: Implement result: "The page should contain copy related to the page and images pulled from the page"
        # TODO: Implement result: "This data should be correct"
        # Verify the Weibo page?

        # Click on the WeChat QR code/link in the footer
        footer = CP.Footer()
        footer.wechat().click()
        # A QR code should appear in an overlay
        qur = CP.QRCode()
        # TODO: Implement action: "Scan the QR code using your WeChat app"
        # TODO: Implement result: "The WeChat account belonging to TA China shows up"
        qur.close()

        # Click on the Sina Weibo image link
        footer.weibo().click()
        # TODO: Implement result: "A new tab/window opens to TA's Sina Weibo account (login to Sina Weibo required)"

        # Navigate to the Aquatics page
        CP.ThingsToDo().open().aquatic().click()
        # TODO: Implement action: "Click the watch video button"
        pan = CP.PanoramicCarousel()
        pan.watch_video()
        # Click the other start video button
        pan.once_off_start_video()
        # Open the Menu, might not need to do this if you are fast enough
        pan.open_video_menu()
        # Click the WeChat icon
        pan.wechat()
        # A QR code appears
        qur = CP.QRCode()
        # TODO: Implement action: "Scan the QR code using the WeChat app on your phone"
        # TODO: Implement result: "The corresponding page opens in WeChat"
        qur.close()

        # Click the Weibo icon
        pan.weibo()
        # TODO: Implement result: "A window should pop up linking to service.weibo.com"
        # TODO: Implement result: "The page should contain copy related to the page and images pulled from the page"
        # TODO: Implement result: "This data should be correct"

    def test_kdp(self):
        # Navigate to the KDP page
        CP.PlanYourTrip().open().kdp().click()
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
        driver = self.driver
        # Click the Australia.com logo in the header
        driver.find_element_by_css_selector("div.header-masthead > a.logo-masthead").click()
        # Should link to homepage

        # Click the Holiday In Australia link in the header
        driver.find_element_by_link_text("旅游度均").click()
        # Should link to homepage.

        # Click the Business Events link in the header
        driver.find_element_by_link_text("商务会奖").click()
        # Should link to businessevents.australia.cn in new tab

        # Open the Explore section in the header
        driver.find_element_by_link_text("探索坊计划行程").click()
        # Verify existence of the three Explore+Planning sections.

        # Open the Destinations section in the header
        driver.find_element_by_link_text("必游胜地").click()
        # Confirm existence of Cities and Destinations sections and map thing.
        # Click the States section switcher
        driver.find_element_by_xpath("//div[@id='sites']/ul/li[2]/a/span").click()
        # Confirm the States section appeared.

    def test_favourites(self):
        driver = self.driver
        # Go to the Australia's Animals page
        driver.find_element_by_link_text("实用信杯").click()
        driver.find_element_by_xpath("//li[@id='nav-main-panel-2']/ul/li/div/div/div/ul/li[3]/a/p").click()
        # Click the Add To Favourites button
        driver.find_element_by_css_selector("img.btn-bubble-active").click()
        # Wait for the animation to finish
        # confirm incremention

        # Do that again with the Regional Cities page.

        # Go to favourites page
        driver.find_element_by_xpath("//li[@id='nav-heart-this-widget']/a/span/span[2]").click()
        # Remove a favourite
        driver.find_element_by_xpath("//div[@id='main-content']/div/div/div[5]/div[2]/div/div/div[2]/div/div[2]/div/div[3]/a/span").click()
        # Confirm it was removed

    def test_whitsundays(self):
        driver = self.driver
        # Navigate to Whitsundays Sailing
        driver.find_element_by_link_text("探索坊计划行程").click()
        driver.find_element_by_xpath("//li[@id='nav-main-panel-3']/ul/li/div/div/div[2]/ul/li[2]/a/p").click()
        driver.find_element_by_xpath("//div[@id='main-content']/div/div/div[5]/div/div[2]/div/div[2]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/p").click()

        # Click a few of the Itinerary Day links
        driver.find_element_by_link_text(u"第七日").click()
        # Confirm scrolling has taken place?

    def test_360(self):
        driver = self.driver
        # Navigate to Acquatic And Coastal
        driver.find_element_by_link_text("探索坊计划行程").click()
        driver.find_element_by_xpath("//li[@id='nav-main-panel-3']/ul/li/div/div/div/div/div/div/div/a/span[2]/span/span").click()

        # Go do a bunch of stuff with the video maybe.

    def test_search(self):
        driver = self.driver
        # Do this a couple of times, different buttons:
        # Open the Search bar
        driver.find_element_by_xpath("//li[@id='nav-main-panel-search']/a/span").click()
        # Click a Common Search Term
        driver.find_element_by_link_text("签话信杯").click()
        # Change the view?
        driver.find_element_by_xpath("//div[@id='main-content']/div/div/div/div/div[3]/div/div/div/div/div/div/div[2]/a[2]/img[2]").click()
        # Change back ?
        driver.find_element_by_css_selector("img.btn-bubble-active").click()
        # Click Load more
        driver.find_element_by_css_selector("a.btn-primary.load-more").click()
        # Confirm the count is incremented?

    def test_wycs(self):
        driver = self.driver
        # Navigate to the Three Days Itineraries page
        driver.find_element_by_link_text("探索坊计划行程").click()
        driver.find_element_by_xpath("//li[@id='nav-main-panel-3']/ul/li/div/div/div[2]/div/div/div/div/a/span[2]/span/span").click()
        # Click on a tile
        driver.find_element_by_xpath("//div[@id='main-content']/div/div/div[6]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div").click()
        # Should direct to the correct page while the other tiles grey out

        # Go to the Great Barrier Reef page
        driver.find_element_by_link_text("必游胜地").click()
        driver.find_element_by_xpath("//div[@id='attractions']/div[2]/div/div/div/a/span[2]/span/span").click()
        # Click on a tile
        driver.find_element_by_xpath("//div[@id='main-content']/div[3]/div/div/div/div[2]/div/div[2]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/p").click()
        # Should direct to the correct page, other tiles faded

    def test_special_offers(self):
        driver = self.driver
        # Navigate to the Special Offers page
        driver.find_element_by_link_text("探索及计划行程").click()
        driver.find_element_by_xpath("//li[@id='nav-main-panel-3']/ul/li/div/div/div[3]/ul/li/a/p").click()
        # Click on a Special Offers link
        driver.find_element_by_css_selector("div.specialoffer-links > a").click()

    def test_brightcove(self):
        driver = self.driver
        # Go to the Tasmania page
        driver.find_element_by_link_text(u"必游胜地").click()
        driver.find_element_by_xpath("//div[@id='sites']/ul/li[2]/a/span").click()
        driver.find_element_by_xpath("//div[@id='states']/div[2]/ul/li[2]/a/p").click()
        # Play the video somehow, check that it worked?

    def test_banner_video(self):
        driver = self.driver
        # Navigate to the Australia's Animals page
        driver.find_element_by_link_text(u"实用信息").click()
        driver.find_element_by_xpath("//li[@id='nav-main-panel-2']/ul/li/div/div/div/ul/li[3]/a/p").click()
        # Verify that the hero banner is animated. Somehow.

    def test_explore(self):
        driver = self.driver
        # Navigate to the Sydney page
        driver.find_element_by_link_text(u"必游胜地").click()
        driver.find_element_by_xpath("//div[@id='cities']/div[3]/div/div/div/a/span[2]/span/span").click()
        # Click the Location Pin button on a the Explore component
        driver.find_element_by_css_selector("#explore-flip-btn > span.btn-bubble-button > img.btn-bubble-active").click()
        driver.find_element_by_xpath("(//a[@id='explore-flip-btn']/span[2]/img[2])[2]").click()
        driver.find_element_by_xpath("(//a[@id='explore-flip-btn']/span[2]/img[2])[3]").click()
        # Confirm that the card flipped?
        # Click the back to overview button
        driver.find_element_by_id("explore-flip-back-btn").click()
        driver.find_element_by_xpath("(//a[contains(text(),'Back to overview')])[2]").click()
        driver.find_element_by_xpath("(//a[contains(text(),'Back to overview')])[3]").click()
        # Add some to favourites
        driver.find_element_by_css_selector("span.btn-bubble.is-touched > span.btn-bubble-button > img.btn-bubble-active").click()
        driver.find_element_by_css_selector("span.btn-bubble.is-touched > span.btn-bubble-button > img.btn-bubble-active").click()
        driver.find_element_by_css_selector("span.btn-bubble.is-touched > span.btn-bubble-button > img.btn-bubble-active").click()
        # Confirm favourites incremented

if __name__ == "__main__":
    oldopen = open
    def open8(*args, **kwargs):
        if len(args) > 1 and 'b' not in args[1]:
            kwargs['encoding'] = 'utf-8'
        return oldopen(*args, **kwargs)

    __builtins__.open = open8
    # Create the test runner, choose the output path: right next to the test script file.]
    runner = tap.TAPTestRunner()
    runner.set_format('Result of: {method_name} - {short_description}')
    runner.set_outdir(os.path.join(os.path.split(__file__)[0], 'REGR_{0}_{1}_{2}.tap')) #.format(locale, browser, time.strftime('%Y%m%d_%H%M'))))
    # tests = unittest.TestSuite([AUS('test_360')])
    # suite = unittest.TestSuite()
    suite = unittest.makeSuite(AUS)
    # suite.addTests(tests)
    runner.run(suite)


    # Give a unique name to the output file so you don't overwrite it every time!
    # with open(os.path.join(outdir, 'REGR_{0}_{1}_{2}.tap'
    #                        .format(locale, browser, time.strftime('%Y%m%d_%H%M'))),
    #           mode='w', encoding='UTF-8') as newfil:
    #     newfil.write(buf.getvalue())
    # print(buf.getvalue() or 'It was blank')
    # buf.close()

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
