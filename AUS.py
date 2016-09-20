# -*- coding: utf-8 -*-
# coding=utf-8

import unittest

class AUS(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://www.australia.cn/"
        self.verificationErrors = []
        driver.get(self.base_url + "/zh-cn")

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

    def test_social(self):
        driver = self.driver
        # Navigate to any page (e.g. http://www.australia.cn/zh-cn/planning/getting-around.html)
        driver.find_element_by_link_text("必游胜地").click()
        # Click the Share icon under the words '分享'
        driver.find_element_by_css_selector("p").click()
        driver.find_element_by_css_selector("span.i.i-ico4").click()
        # Two icons should slide out from under it
        # Click the icon for WeChat (two chat balloon faces)
        driver.find_element_by_css_selector("span.i.i-ico6").click()
        # TODO: Implement result: "A QR code should appear"
        # TODO: Implement action: "Scan the QR code using the WeChat app on your phone"
        # TODO: Implement result: "The corresponding page opens in WeChat"
        driver.find_element_by_css_selector("button.close").click()

        # TODO: Implement action: "Click the icon for Weibo (eyeball thing)"
        driver.find_element_by_css_selector("span.i.i-ico5").click()
        # TODO: Implement result: "A window should pop up linking to service.weibo.com"
        # TODO: Implement result: "The page should contain copy related to the page and images pulled from the page"
        # TODO: Implement result: "This data should be correct"
        # Verify the Weibo page?

        # TODO: Implement action: "Scroll to the footer"
        # TODO: Implement action: "Click on the WeChat QR code/link"
        driver.find_element_by_css_selector("#china_qr-footer-button > span").click()
        # TODO: Implement result: "A QR code should appear in an overlay"
        # TODO: Implement action: "Scan the QR code using your WeChat app"
        # TODO: Implement result: "The WeChat account belonging to TA China shows up"
        driver.find_element_by_css_selector("a.fancybox-item.fancybox-close").click()

        # TODO: Implement action: "Click on the Sina Weibo image/link (kangaroo picture)"
        driver.find_element_by_xpath("//footer[@id='main-footer']/div/div/div[2]/div/div/ul/li/a/span").click()
        # TODO: Implement result: "A new tab/window opens to TA's Sina Weibo account (login to Sina Weibo required)"

        # TODO: Implement action: "Navigate to the aquatic page (http://www.australia.cn/zh-cn/things-to-do/aquatic.html)"
        driver.find_element_by_link_text("探索坊计划行程").click()
        driver.find_element_by_xpath("//li[@id='nav-main-panel-3']/ul/li/div/div/div/div/div/div/div/a/span[2]/span/span").click()
        # TODO: Implement action: "Click the watch video button"
        driver.find_element_by_css_selector("button.button.carouselcoastal-explore-btn").click()
        # TODO: Implement action: "Click the start video button"
        driver.find_element_by_id("start360VideoButtonDesktop").click()
        # Open the Menu, might not need to do this if you are fast enough
        driver.find_element_by_css_selector("span.icon-font-pie").click()
        # TODO: Implement action: "Click the icon for WeChat (two chat balloon faces, third from the top in the sidebar)"
        driver.find_element_by_css_selector("span.i.i-ico3").click()
        # TODO: Implement result: "A QR code should appear"
        # TODO: Implement action: "Scan the QR code using the WeChat app on your phone"
        # TODO: Implement result: "The corresponding page opens in WeChat"
        driver.find_element_by_css_selector("#myModalForVideo > div.modal-dialog > div.modal-content > div.modal-body > button.close").click()

        # TODO: Implement action: "Click the icon for Weibo (eyeball thing, second from the top in the sidebar)"
        driver.find_element_by_css_selector("span.i.i-ico2").click()
        # TODO: Implement result: "A window should pop up linking to service.weibo.com"
        # TODO: Implement result: "The page should contain copy related to the page and images pulled from the page"
        # TODO: Implement result: "This data should be correct"
        # Log in to Weibo maybe, verify the page.

    def test_kdp(self):
        driver = self.driver
        # TODO: Implement action: "Navigate to the KDP page (http://www.australia.cn/zh-cn/plan/kdp.html)"
        driver.find_element_by_link_text("探索坊计划行程").click()
        driver.find_element_by_xpath("//li[@id='nav-main-panel-3']/ul/li/div/div/div[3]/div/div/div/div/a/span[2]/span/span").click()
        # Count results, assert all buttons lit.
        # TODO: Implement action: "Scroll to the KDP ( travel package ) section that under the heading Explore Trip (杜索行程)"
        # TODO: Implement result: "North China, South China, East China and West China icons should all be active (cyan with white lines) and all KDP products should appear."
        # TODO: Implement action: "Click the South China button (first button on the left)"
        driver.find_element_by_xpath("//div[@id='searchSectionValue']/div/div[2]/div[2]/div/div/div/div[2]/a/span/img[2]").click()
        # TODO: Implement result: "The South China icon should remain cyan while the others turn white. Check if all items displayed are from the South China region."
        # TODO: Implement action: "Perform steps 4 and 5 for the remaining three regions (North China, East China and West China)"
        # TODO: Implement result: "If all KDP ( travel packages ) show correctly on four regions , the test is passed."

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
        driver.find_element_by_link_text("探索坊计划行程").click()
        driver.find_element_by_xpath("//li[@id='nav-main-panel-3']/ul/li/div/div/div[2]/div/div/div/div/a/span[2]/span/span").click()
        driver.find_element_by_xpath("//div[@id='main-content']/div/div/div[6]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div").click()
        driver.find_element_by_link_text("必游胜地").click()
        driver.find_element_by_xpath("//div[@id='attractions']/div[2]/div/div/div/a/span[2]/span/span").click()
        driver.find_element_by_xpath("//div[@id='main-content']/div[3]/div/div/div/div[2]/div/div[2]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/p").click()

    def test_Verify_Three_day_itineraries__(self):
        self.actionwords.site_loaded__home()
        self.actionwords.click_explore__trip_planning_()
        self.actionwords.explore__trip_planning__navigation_should_be_opened()
        self.actionwords.unique_features__popular_itineraries__and_campaigns__submenu_will_be_displayed()
        self.actionwords.click_on_the_three_day_itineraries__image()
        self.actionwords.the_three_day_itineraries__page_should_be_loaded()
        self.actionwords.click_on_any_of_the_submenus()
        self.actionwords.the_page_for_the_selected_submenu_will_be_displayed_no_missing_images()

    def test_Verify_Special_Offers_page(self):
        self.actionwords.env_up__homepage()
        self.actionwords.navigate_to_cx_airline_campaign_page__httpwwwaustraliacnzhcncampaigncathayhtml()
        self.actionwords.cx_airline_campaign_page_will_be_displayed()
        self.actionwords.find_special_offers_section_below_the_first_passage()
        self.actionwords.ensure_general_correctness()

    def test_Verify_Brightcove_Video_functionality(self):
        self.actionwords.env_up__homepage()
        self.actionwords.navigate_to_p1_availble_under_p2_section(p1 = "Tasmania (塔斯马尼亚)", p2 = "Destination（必游胜地）> States & Territory (州和领地)")
        self.actionwords.click_on_the_video_play_icon_in_the_video_below_the_first_few_paragraphs()
        self.actionwords.the_video_should_begin_to_play_with_sound()

    def test_Verify_Hero_Banner_Video(self):
        self.actionwords.navigate_to_p1___animals__(p1 = "“Official Information （澳大利亚简介）”")
        self.actionwords.the_video_should_automatically_begin_to_play()
        self.actionwords.the_video_should_play_on_a_loop()

    def test_Verify_What_You_Can_See_component(self):
        self.actionwords.site_loaded__home()
        self.actionwords.navigate_to_destination___great_barrier_reef_()
        self.actionwords.scroll_down_to_the_wycs_mosaic_tiles_component()
        self.actionwords.click_one_of_the_tiles()
        self.actionwords.the_selected_tile_should_open_other_tiles_should_fadegrey_out()
        self.actionwords.automatically_links_to_the_relevant_page()

    def test_Verify_Explore_component(self):
        self.actionwords.site_loaded__home()
        self.actionwords.navigate_to_destination___sydney_()
        self.actionwords.scroll_down_to_the_what_you_can_see_near_sydney_section_not_the_wycs_mosaic_further_down()
        self.actionwords.click_the_nearby_places__and_itineraries__icons()
        self.actionwords.displayed_cards_should_change_to_each_category_as_selected()
        self.actionwords.click_the_location_pin_button_on_one_of_the_cards()
        self.actionwords.card_should_flip_to_reveal_a_map()
        self.actionwords.click_the_back_to_overview_link()
        self.actionwords.card_flips_back_to_reveal_main_overview()
        self.actionwords.click_the_favorite_icon_on_card()
        self.actionwords.dream_trip_icon_in_header_is_incremented()
