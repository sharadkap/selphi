# encoding: UTF-8
import unittest
from actionwords import Actionwords

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
        driver.find_element_by_link_text(u"必游胜地").click()
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
        driver.find_element_by_link_text(u"探索及计划行程").click()
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
        driver.find_element_by_link_text(u"探索及计划行程").click()
        driver.find_element_by_xpath("//li[@id='nav-main-panel-3']/ul/li/div/div/div[3]/div/div/div/div/a/span[2]/span/span").click()
        # Count results, assert all buttons lit.
        # TODO: Implement action: "Scroll to the KDP ( travel package ) section that under the heading Explore Trip (搜索行程)"
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
        driver.find_element_by_link_text(u"旅游度假").click()
        # Should link to homepage.

        # Click the Business Events link in the header
        driver.find_element_by_link_text(u"商务会奖").click()
        # Should link to businessevents.australia.cn in new tab

        # Open the Explore section in the header
        driver.find_element_by_link_text(u"探索及计划行程").click()
        # Verify existence of the three Explore+Planning sections.

        # Open the Destinations section in the header
        driver.find_element_by_link_text(u"必游胜地").click()
        # Confirm existence of Cities and Destinations sections and map thing.
        # Click the States section switcher
        driver.find_element_by_xpath("//div[@id='sites']/ul/li[2]/a/span").click()
        # Confirm the States section appeared.

    def test_Verify_Australiacn_Logo_Link(self):
        self.actionwords.env_up__home_page()
        self.actionwords.click_on_australiacn_logo()
        self.actionwords.home_page_should_be_displayed()
        self.actionwords.no_page_distortions()

    def test_Verify_Holiday_link_in_Australiacn(self):
        self.actionwords.env_up__home_page()
        self.actionwords.click_on_holiday_link()
        self.actionwords.home_page_should_be_displayed()
        self.actionwords.no_page_distortions()

    def test_Verify_Plan_a_Business_Event_link(self):
        self.actionwords.env_up__home_page()
        self.actionwords.click_on_p1_link(p1 = "'Plan a Business Event'(商务会奖)")
        self.actionwords.australia_business_event_page_should_be_displayed_in_a_new_tab()

    def test_Verify_Explore__Trip_Planning_link(self):
        self.actionwords.click_explore__trip_planning_menu_link_available_in_header()
        self.actionwords.explore__trip_planning_navigation_will_be_expanded()
        self.actionwords.unique_features_popular_itineries_and_campaigns_submenu_will_be_displayed()
        self.actionwords.no_styling_issues()

    def test_Verify_all_submenus_under_Activities(self):
        self.actionwords.env_up__home_page()
        self.actionwords.open_the_explore__trip_planning__menu_in_the_header()
        self.actionwords.in_the_unique_features__category_click_on_submenu_links_one_by_one()
        self.actionwords.the_page_for_the_selected_submenu_will_be_displayed()
        self.actionwords.ensure_general_correctness()

    def test_Verify_Favorite_functionality(self):
        self.actionwords.env_up__homepage()
        self.actionwords.navigate_to_p1_availble_under_p2_section(p1 = "'Animals'(动物)", p2 = "'Official Information'(澳大利亚简介)")
        self.actionwords.click_on_the_p1_icon_symbol_below_the_add_label(p1 = "favourite")
        self.actionwords.favourites_icon_present_in_header_counter_should_be_incremented()

    def test_Verify_All_Itineraries_page(self):
        self.actionwords.env_up__home_page()
        self.actionwords.click_on_general_information()
        self.actionwords.in_official_information_section_click_on_p1(p1 = "'See More(查看更多)'")
        self.actionwords.facts_of_australia_page_will_be_displayed()
        self.actionwords.ensure_general_correctness()

    def test_Verify_Whitsundays_Sailing(self):
        self.actionwords.start_up_at_whitsundays_sailinghttpwwwaustraliacnzhcnitinerariesqldwhitsundayssailinghtml()
        self.actionwords.whitsundays_sailing_page_will_be_displayed()
        self.actionwords.ensure_general_correctness()

    def test_Verify_day_Link(self):
        self.actionwords.start_up_at_whitsundays_sailing_httpwwwaustraliacnzhcnitinerariesqldwhitsundayssailinghtml()
        self.actionwords.scroll_the_page_so_that_you_can_see_all_the_day_links()
        self.actionwords.click_on_any_of_the_day_link_eg_p1(p1 = "Day 7 （第七日）")
        self.actionwords.the_page_should_get_scrolled_to_the_selected_day_datails()

    def test_Click_on_Destination__from_header(self):
        self.actionwords.precondition_site_should_be_loaded_properly()
        self.actionwords.open_the_home_page()
        self.actionwords.home_page_should_be_loaded()
        self.actionwords.click_destination_()
        self.actionwords.navigation_will_be_expanded_no_styling_issues_the_following_submenu_will_be_displayed()
        self.actionwords.1_cities_section()
        self.actionwords.2_state__territories_map()
        self.actionwords.3_explore_australia_by_map_link()
        self.actionwords.4_attractions_section()

    def test_Verify_Cities_link(self):
        self.actionwords.start_with_destination___cities_()
        self.actionwords.check_the_links_present_on_cities_page()
        self.actionwords.all_links_if_any_should_work()

    def test_Verify_Iconic_Attractions__link(self):
        self.actionwords.site_loaded__home()
        self.actionwords.click_destination_()
        self.actionwords.destination__navigation_should_be_expanded()
        self.actionwords.click_on_an_iconic_attractions__link()
        self.actionwords.selected_attractions_page_should_be_displayed_no_missing_images()
        self.actionwords.check_the_links_present_on_page()
        self.actionwords.all_links_if_any_should_work()

    def test_Verify_States__Territories__link(self):
        self.actionwords.site_loaded__home()
        self.actionwords.click_destination_()
        self.actionwords.destination__navigation_should_be_expanded()
        self.actionwords.click_on_states__territories__link__select_any_link_from_the_list()
        self.actionwords.selected_states__territories__page_should_be_displayed_no_missing_images()
        self.actionwords.check_the_links_present_on_page()
        self.actionwords.all_links_if_any_should_work()

    def test_Verify_Add_To_Your_Dream_Trip(self):
        self.actionwords.start_with_destination___cities_()
        self.actionwords.click_on_the_heart_icon_present_on_the_page()
        self.actionwords.favourites_icon_counter_should_be_incremented()

    def test_Verify_Explore_Australia_in_360_360_(self):
        self.actionwords.site_loaded__home()
        self.actionwords.click_explore__trip_planning_()
        self.actionwords.explore__trip_planning__navigation_should_be_expanded()
        self.actionwords.unique_features__popular_itineraries__and_campaigns__submenus_will_be_displayed()
        self.actionwords.navigate_explore__trip_planning___unique_features___explore_australia_in_360_360()
        self.actionwords.explore_australia_in_360_360_page_should_be_loaded()
        self.actionwords.no_missing_images_all_links_correct_if_any()

    def test_Click_on__Explore__Trip_Planning__from_header(self):
        self.actionwords.site_loaded__home()
        self.actionwords.click_explore__trip_planning_()
        self.actionwords.explore__trip_planning__navigation_should_be_expanded()
        self.actionwords.unique_features__popular_itineraries__and_campaigns__submenus_will_be_displayed()

    def test_Verify_General_Search_functionality(self):
        self.actionwords.site_loaded__home()
        self.actionwords.click_search_icon_in_the_header()
        self.actionwords.search_bar_should_appear()
        self.actionwords.click_on_a_few_of_the_popular_searches_links()
        self.actionwords.should_redirect_to_the_search_results_page_and_five_relevant_search_results_appear()
        self.actionwords.the_results_should_switch_between_displaying_as_a_list_and_as_mosaic_tiles()
        self.actionwords.click_the_lines_grid_icons_above_the_search_results()
        self.actionwords.click_the_view_more_button()
        self.actionwords.five_more_search_results_should_be_loaded_up_to_the_maximum_shown_in_the_results_count()

    def test_Click_on_the_Favourites_Icon_from_the_header(self):
        self.actionwords.precondition_site_should_be_loaded_properly()
        self.actionwords.precondition_add_few_page_to_favourites_for_example_select_heart_icon_from_enplacessydneyhtml()
        self.actionwords.click_favourites_icon_from_home_page()
        self.actionwords.favourites_page_should_be_displayed_the_count_in_the_list_should_be_the_same_number_as_the_number_in_the_counter()
        self.actionwords.in_the_current_page_select_an_item_on_the_list_and_click_the_remove_x_button()
        self.actionwords.the_item_should_be_removed_from_the_list()
        self.actionwords.refresh_the_current_page()
        self.actionwords.removed_item_should_not_be_present_on_page()

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
