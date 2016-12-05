"""The test suite for the ASP website regression."""

import random
import unittest
from collections import OrderedDict
from drivery import Drivery, Email
import modules as MOD
import components as CP

# A mapping of the test names to their abbreviations
aspnames = OrderedDict(
    [('SPL', 'test_01_Splash_Page'), ('HPG', 'test_02_Homepage'), ('NAV', 'test_03_Navigation'),
     ('FTR', 'test_04_Footer'), ('SMP', 'test_05_Sitemap'),
     ('ITN', 'test_06_Filtered_Search_Itineraries'), ('FCT', 'test_07_Filtered_Search_Fact_Sheets'),
     ('MAP', 'test_08_Interactive_Map'), ('CTC', 'test_09_Contact_Us'),
     ('REG', 'test_10_Registration'), ('LOG', 'test_11_Login'), ('FAV', 'test_12_Favourites'),
     ('PRF', 'test_13_My_Profile'), ('TRN', 'test_14_Training_Summary'),
     ('ASC', 'test_15_Aussie_Specialist_Club'), ('TVL', 'test_16_Travel_Club'),
     ('FML', 'test_17_Famils'), ('PHT', 'test_18_Aussie_Specialist_Photos'),
     ('DLB', 'test_19_Download_Qualification_Badge'), ('STR', 'test_20_Aussie_Store'),
     ('PRM', 'test_21_Premier_Badge'), ('FUN', 'test_22_Forgotten_Username'),
     ('FPW', 'test_23_Forgotten_Password'), ('CPW', 'test_24_Change_Password'),
     ('CMP', 'test_25_Campaign')])

class ASP(unittest.TestCase): # pylint: disable-msg=R0904
    """The Test Suite for the ASP regresseion. Test methods are numbered because HipTest."""
    def __init__(self, name: str, glob: dict):
        # super(ASP, self, name).__init__()
        super().__init__(methodName=name)
        self.globs = glob

    def setUp(self) -> None:
        """Called just before each test is run, sets up the browser and test records."""
        # Initialise the browser connection.
        self.verificationErrors = []    # Keep a list of everything that went wrong.
        self.accept_next_alert = True
        self.dr = Drivery(self.globs)

    def tearDown(self) -> None:
        """Called after finishing each test, closes the browser and counts up the errors."""
        self.dr.close()
        self.maxDiff = None
        self.assertEqual([], self.verificationErrors, 'This will fail if there were any nonlethal'
                         ' assertions. Hopefully the custom messages are helpful enough.')

    def add_error(self) -> None:
        """Adds an error to the errors list. Shortcut."""
        from selene import tidy_error
        self.verificationErrors.append(tidy_error())

    # Tests start here.
    def test_01_Splash_Page(self) -> None:
        """Tests the Splash Page."""
        # Open the splash page.
        self.dr.splash_page()
        # Concerning the Languages Selector
        langsel = CP.SplashSelect(self.dr)
        try:
            self.assertSetEqual(langsel.locale_set, langsel.get_values(),
                                'The language selector should contain all locales.')
        except Exception:
            self.add_error()
        # Select the country from the dropdown.
        langsel.choose_locale()
        # Page should redirect to its respective locale.
        self.dr.wait_for_page()
        self.assertIn(self.globs['locale'], self.dr.fix_url(self.dr.current_url()),
                      'The selected locale should link to that locale.')

    def test_02_Homepage(self) -> None:
        """Tests the Welcome Page content."""
        self.dr.open_home_page()
        # Video should be present. But its absence isn't worth aborting the test over.
        try:
            video = CP.WelcomeVideo(self.dr)
        except Exception:
            self.add_error()
        else:
            # Play the video.
            video.play()
            # Video loads and plays. Again, there are still other things to test.
            try:
                self.dr.wait_until(video.is_playing, 'After clicking Play, the video should play.')
            except Exception:
                self.add_error()
        # Login and Register buttons should be present in the body content.
        try:
            CP.BodyLoginButton(self.dr)
            CP.BodyRegisterButton(self.dr)
        except Exception:
            self.add_error()
        # The What You Can See Mosaic is displayed, contains five tiles.
        mosaic = CP.WhatYouCanSeeMosaic(self.dr)
        self.assertEqual(mosaic.tile_count(), 5,
                         'There should be five mosaic tiles on the homepage.')

    def test_03_Navigation(self) -> None:
        """Checks that the contents of the Signed Out Nav Menu are correct."""
        self.dr.open_home_page()
        # Click on 'About' in the Mega Menu.
        try:
            about = CP.NavMenu.About(self.dr).open()
            # The About section should have: About, Why Register,
            # Program FAQ, Site Usage, Contact Us
            about.about()
            about.benefits()
            about.how_to_use_the_site()
            about.program_faq()
            about.contact_us()
        except Exception:
            self.add_error()

        # Click on 'Sales Resources' in the Mega Menu.
        try:
            sales = CP.NavMenu.SalesResources(self.dr).open()
            # The Sales section should have: Sales Resources (Landing), Interactive Map,
            # Fact Sheets, Useful Websites, Image and video galleries, My sales tools,
            # Itinerary Search, Australian Events, Destination FAQ
            sales.sales_resources()
            sales.interactive_map()
            sales.itineraries_search_and_feature()
            sales.fact_sheets_overview()
            sales.events()
            sales.useful_sites()
            sales.destination_faq()
            sales.image_and_video_galleries()
        except Exception:
            self.add_error()

        # Click on 'Training' in the Mega Menu.
        try:
            train = CP.NavMenu.Training(self.dr).open()
            # The Training section should have: *Training (Landing page only)
            train.training()
        except Exception:
            self.add_error()

        # Click on 'News & Products' in the Mega Menu.
        try:
            news = CP.NavMenu.NewsAndProducts(self.dr).open()
            # The News section should have: *News and Product Updates (Landing page only)
            news.news_and_product_updates()
        except Exception:
            self.add_error()

        # Click on 'Aussie Specialist Club' in the Mega Menu.
        try:
            club = CP.NavMenu.AussieSpecialistClub(self.dr).open()
            # The Club section should have: *Aussie Specialist Club (Landing page only)
            club.aussie_specialist_club()
        except Exception:
            self.add_error()

    def test_04_Footer(self) -> None:
        """Checks the content of the Footer."""
        self.dr.open_home_page()
        footer = CP.Footer(self.dr)
        if self.globs['cn_mode']:
            # China is different, of course.
            try:
                footer.wechat()
            except Exception:
                self.add_error()
        else:
            # The Footer should have: Find us on: Social icons and links.
            try:
                footer.facebook()
                footer.twitter()
                footer.plus_google()
                footer.instagram()
                footer.youtube()
            except Exception:
                self.add_error()
        # About this site: links through to relevant pages
        try:
            footer.sitemap()
            footer.privacy_policy()
            footer.terms_and_conditions()
            footer.terms_of_use()
            footer.contact_us()
        except Exception:
            self.add_error()
        # Other sites: Links through to Aus.com, Corporate site and Business Events.
        try:
            footer.australia()
            footer.businessevents_australia()
            if not self.globs['cn_mode']:    # China doesn't have this one.
                footer.tourism_australia()
        except Exception:
            self.add_error()
        # Click the Change Your Country link.
        footer.splash().click()
        # Should link back to the Splash page.
        self.dr.wait_for_page()
        self.assertIn('/splash.html', self.dr.current_url(), 'The Splash link should lead to the '
                      'Splash page, of course.')

    def test_05_Sitemap(self) -> None:
        """Checks the Sitemap page links."""
        self.dr.open_home_page()
        # Click the Sitemap link in the Footer.
        try:
            CP.Footer(self.dr).sitemap().click()
            # Should link to the Sitemap page."
            self.dr.wait_for_page()
            self.assertIn('/sitemap.html', self.dr.current_url(), 'The Sitemap link should link '
                          'to the Sitemap page.')
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).sitemap()
        # Sitemap page should have links to each of the pages in the Nav Menu
        sitemap = CP.Sitemap(self.dr)
        try:
            nav_links = CP.NavMenu(self.dr).get_all_links()
            sitemap_links = sitemap.get_all_links()
            self.assertTrue(nav_links.issubset(sitemap_links),
                            'The sitemap should contain each of the links in the Nav Menu.')
        except Exception:
            self.add_error()
        try:
            # And should also have Change Password, Unsubscribe, and Coming Soon links.
            # But China doesn't.
            if not self.globs['cn_mode']:
                sitemap.change()
                sitemap.newsletter_unsubscribe()
                sitemap.coming_soon()
        except Exception:
            self.add_error()

    def test_06_Filtered_Search_Itineraries(self) -> None:
        """Checks the Itineraries Search."""
        self.dr.open_home_page()
        # Navigate to Sales Resources > Itinerary Suggestions.
        try:
            CP.NavMenu.SalesResources(self.dr).open().itineraries_search_and_feature().click()
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).itineraries()
        # Do a random search and validate the results.
        search = CP.FilteredSearch(self.dr)
        search.random_search()
        self.look_at_search_results(search)

    def test_07_Filtered_Search_Fact_Sheets(self) -> None:
        """Tests the Fact Sheet Search."""
        self.dr.open_home_page()
        # Navigate to Sales Resources > Fact Sheets.
        try:
            CP.NavMenu.SalesResources(self.dr).open().fact_sheets_overview().click()
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).factsheets()
        # Do a random search. (In Fact Sheet +PDFs Mode) Then validate the results.
        search = CP.FilteredSearch(self.dr, fact_sheet_mode=True)
        search.random_search()
        try:
            self.look_at_search_results(search)
        except Exception:
            self.add_error()
        # Alright, done there back up.
        self.dr.back()
        # Because the page was reloaded, have to refresh the references.
        search = CP.FilteredSearch(self.dr, fact_sheet_mode=True)
        result = search.get_random_result()
        # Click on a result's Download PDF link.
        result.download_pdf()
        # The relevant PDF should open in a new (second) (so number 1) window.
        self.dr.switch_to_window(1)
        CP.PDFPage(self.dr)

    def look_at_search_results(self, searcher: CP.FilteredSearch) -> None:
        """Validates the search results and the View More button."""
        # If the counter is present on this page, validate it against the number of results.
        count = searcher.read_results_counter()
        if count is not None:
            firstcount = searcher.count_results()
            self.assertEqual(count[0], firstcount,
                             'The counter should initially show the number of results visible.')
            # Now see if it updates upon Loading More Results.
            searcher.load_more()
            secondcount = searcher.count_results()
            count = searcher.read_results_counter()
            # At most five more results should be displayed, up to the maximum matching amount.
            self.assertEqual(secondcount, min(firstcount + 5, count[1]),
                             'The counter should show the new number of results visible.')
            # Check a random result, make sure it links to the right page.
            result = searcher.get_random_result()
            name = result.get_title().casefold()
            # Click on the result's More Info link.
            result.view_more_information()
            # Should link to that result's More Info page.
            self.assertEqual(result.SearchResultPage(self.dr).get_title().casefold(), name,
                             "The result's link should go to the relevant page.")

    def test_08_Interactive_Map(self) -> None:
        """Checks the Interactive Map page."""
        # Navigate to Sales Resources > Interactive Map
        self.dr.open_home_page()
        try:
            CP.HeaderMapIcon(self.dr).click()
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).map()
        # (Switches into the Map Iframe.)
        imap = CP.InteractiveMap(self.dr)
        # Map Menu should have: Cities, Iconic Destinaions, Itineraries, and Flight Times.
        controls = imap.Controls(self.dr)
        try:
            cities = controls.Cities(self.dr)
        except Exception:
            self.add_error()
        else:
            try:
                # Open the Cities menu, the Cities list should be shown.
                cities.open_menu()
                # The Map should be populated with Map Pins.
                # Click a pinned City, remember which one it was.
                pin = imap.MapArea.MapPins(self.dr).pick_random()
                # That City's Info Panel should be shown. Go examine it.
                self.map_info_panel(pin)
            except Exception:
                self.add_error()
        try:
            icons = controls.IconicDestinations(self.dr)
        except Exception:
            self.add_error()
        else:
            try:
                # Open the Iconic Destinations menu
                icons.open_menu()
                # The Icons list should be shown, the Map should be populated with Destination Pins.
                # Click a random pinned Destination.
                pin = imap.MapArea.MapPins(self.dr).pick_random()
                # That Icon's Info Panel should be shown, verify all that.
                self.map_info_panel(pin)
            except Exception:
                self.add_error()
        try:
            controls.Itineraries(self.dr)
        except Exception:
            self.add_error()
        try:
            flights = controls.FlyingTimes(self.dr)
        except Exception:
            self.add_error()
        else:
            # Open the Flying Times section, the Flying Times device appears.
            flights.open_menu()
            # Select a city in each of the From and To drop menus.
            ffrom = flights.choose_from()
            fto = flights.choose_to()
            # The selected cities' Pins appear on the map,
            #   connected by a flight path, traversed by a plane icon.
            pins = imap.MapArea.MapPins(self.dr)
            self.assertEqual(pins.count(), 2, 'A flight path should have two pins.')
            names = pins.get_names()
            self.assertIn(ffrom, names, 'The flight path should have the From pin.')
            self.assertIn(fto, names, 'The flight path should have the To pin.')
            # The flying Times panel shows the approximate flight time and distance.
            flights.flight_time()
            flights.flight_distance()

    def map_info_panel(self, name: str) -> None:
        """Look at a Map Location Info Pane. Checks the various links and images."""
        # The right Info panel should be open.
        panel = CP.InteractiveMap.Controls.InfoPanel(self.dr)
        try:
            self.assertEqual(name, panel.get_title(),
                             'The link should open the City of the same name.')
            # The Find Out More and View Highlights buttons should link
            #   to a relevant Fact Sheet/Itinerary Plan.
            fomlink = panel.find_out_more()
            self.assertIn(self.globs['locale'], fomlink,
                          'The More Info link should remain within the same locale.')
            self.assertEqual(fomlink, panel.view_highlights(),
                             'Both of the More Info Links should go to the same page.')
        except Exception:
            self.add_error()
        # Click the Photos
        try:
            imgnum = panel.count_photos()
            # Open the Photo viewer.
            photos = panel.open_photos()
            # The Photo Viewer should appear, can be scrolled through, displays different images.
            # But if there was only one image available, skip this scrolling bit.
            if not imgnum == 1:
                imgone = photos.current_image_source()
                photos.next()
                imgtwo = photos.current_image_source()
                self.assertNotEqual(imgone, imgtwo,
                                    'One image should be distinct from the next.')
                photos.next()
                imgone = photos.current_image_source()
                self.assertNotEqual(imgtwo, imgone,
                                    'Two image should also be distinct from the nexter.')
            # Close the Photo Viewer
            photos.close()
        except Exception:
            self.add_error()
        # Click on one of the Itinerary Suggestion links
        try:
            itiname = panel.random_itinerary()
            # If there were no Itinerary links, skip this bit.
            if itiname != '':
                # New panel, renew the selector.
                panel = CP.InteractiveMap.Controls.InfoPanel(self.dr)
                # The selected Itinerary should open.
                self.assertEqual(itiname, panel.get_title(),
                                 'The link should open the Itinerary of the same name.')
                # Its route should appear and gain focus on the map, but zoom out a bit first,
                # the pins will sometimes pop up behind the menu panel.
                CP.InteractiveMap.ZoomTools(self.dr).zoom_out()
                pins = CP.InteractiveMap.MapArea.MapPins(self.dr)
                # The Find Out More link should link to the relevant Itinerary Page.
                self.assertIn(self.globs['locale'], panel.find_out_more(),
                              'The More Info link should remain within the same locale.')
                # Click on one of the Route Pins
                pins.pick_random()
                # An info box should appear at the pin.
                CP.InteractiveMap.MapArea.InfoPopup(self.dr)
            # Click the Back To Menu Button, the panel should spin back to the Main Map Menu
        except Exception:
            self.add_error()
        finally:
            panel.back_to_menu()

    def test_09_Contact_Us(self) -> None:
        """Checks the Contact Us page."""
        self.dr.open_home_page()
        # Navigate to About > Contact Us.
        try:
            CP.NavMenu.About(self.dr).open().contact_us().click()
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).contact()
        # "Click the Contact Us link, Default email client should open, with the To field populated
        #   with the relevant contact." Can't actually test that, so a 'mailto:' will have to do.
        CP.ContactUs(self.dr)

    def test_10_Registration(self) -> None:
        """Checks the Registration process."""
        self.dr.open_home_page()
        # Navigate to the Registration Page
        try:
            CP.BodyRegisterButton(self.dr).click()
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).register()
        # Random letters to make a unique username.
        self.globs['userid'] = ''.join([chr(random.randrange(65, 91)) for i in range(4)])
        self.globs['email'] = self.globs['email'].format(self.globs['userid'])
        # The Country Code
        langcode, localecode = self.globs['locale'].replace('/', '').split('-')
        environ = self.globs['base_url'].split('/')[2].split('.')[0][0:3] #pylint: disable-msg=E1101
        # Username stuff, add the Environment prefix to identify the user.
        # Different zip codes in different countries.
        zipcode = {'gb': 'A12BC', 'us': '12345', 'ca': '12345', 'my': '12345', 'id': '12345',
                   'it': '12345', 'fr': '12345', 'de': '12345'}.get(localecode, '123456')
        # Fill out the Registration Form with dummy information.
        # Ensure the Name fields are/contain TEST.
        form = CP.RegistrationForm(self.dr)
        form.plain_text_fields('TEST')
        form.web = 'www.TEST.com'
        form.fname = 'TEST ' + localecode + environ
        form.date_of_birth('12/12/1212')
        form.pick_business_profile()
        form.zip = zipcode
        # If in China, pick an Official Preferred Travel Partner
        if self.globs['cn_mode']: form.pick_partner()
        # If in China, it is already China.
        if not self.globs['cn_mode']: form.pick_country(localecode.upper())
        form.pick_state()
        # If in China, it is already Chinese.
        if not self.globs['cn_mode']: form.pick_language(langcode)
        # Use an overloaded email.
        form.email_address(self.globs['email'].format(self.globs['userid']))
        form.how_many_years()
        form.how_many_times()
        form.how_many_bookings()
        form.standard_categories()
        form.experiences()
        # Better hope this test comes before the other ones!
        self.globs['username'] = localecode + environ + self.globs['userid']
        form.username = self.globs['username']
        form.password(self.globs['password'])
        form.terms_and_conditions()
        form.decaptcha()
        # Click the Create Account button, popup should appear confirming account creation.
        form.submit()
        # Email should be sent confirming this.
        regemail = Email.RegistrationEmail(self.globs, self.dr, self.globs['userid'])
        # In the Registration Confirmation email, click the Activate Account link.
        # Should open the Registration Acknowledgement page, confirming the account is set up.
        self.dr.get(regemail.activation_link())

    def test_11_Login(self):
        """Tests the Login-related functionality."""
        # Log in.
        self.dr.open_home_page()
        CP.SignIn(self).sign_in(self.globs['username'], self.globs['password'])
        # Should proceed to the Secure welcome page.
        try:
            self.assertIn(self.globs['locale'] + '/secure.html', self.dr.current_url(),
                          'After logging in, should redirect to a/the secure page.')
        except Exception:
            self.add_error()
        # Check the Nav Menu
        # The Sales section should now have the My Sales Tools link
        try:
            CP.NavMenu.SalesResources(self.dr).open().my_sales_tools()
        except Exception:
            self.add_error()
        # The Training Section should now have the Training Summary and Webinars links.
        try:
            train = CP.NavMenu.Training(self.dr).open()
            train.webinars()
            train.training_summary()
        except Exception:
            self.add_error()
        # The News & Updates section should have the Latest News Link
        # The News section should now  have the Product Updates link.
        try:
            news = CP.NavMenu.NewsAndProducts(self.dr).open()
            news.latest_news()
            news.product_videos()
        except Exception:
            self.add_error()
        # China shows most of its ASC stuff to unqualified users, yes.
        if self.globs['cn_mode']:
            club = CP.NavMenu.AussieSpecialistClub(self.dr).open()
            club.famils()
            club.aussie_specialist_photos()
        else:
            # The Club section should not be present. (Don't instantiate it, it isn't there)
            self.assertTrue(CP.NavMenu.AussieSpecialistClub.not_present(self.dr),
                            'A trainee should not have access to the Aussie Specialist Club.')

    def test_12_Favourites(self):
        """Tests the Sales Tools functionality."""
        favtitles = set()
        def mosaicad(num: int):
            """Opens a mosaic, checks it, and adds it to sales tools"""
            nonlocal favtitles
            # Click on some of the Mosaic panels.
            try:
                # Bleh. Can't just use the tile list, pages change, StaleElementExceptions.
                # pick a bunch of random numbers from zero to the number of tiles.
                for i in random.sample(range(len(CP.WhatYouCanSeeMosaic(self.dr))), num):
                    tile = CP.WhatYouCanSeeMosaic(self.dr)[i]
                    # The Panels direct to their page when clicked.
                    tile.go()
                    # Click on the Heart buttons of those mosaics.
                    hero = CP.Hero(self.dr)
                    hero.add()
                    favtitles.add(hero.get_title())
                    # The Heart Icon in the header should pulse and have a number incremented.
                    self.dr.wait_until(
                        lambda: len(favtitles) == CP.HeaderHeartIcon(self.dr).favourites_count(),
                        'Added page to faves to increment favourites count.')
                    self.dr.back()
            except Exception:
                self.add_error()

        # Pre-condition: Should be signed in.
        self.dr.open_home_page()
        CP.SignIn(self).sign_in(self.globs['username'], self.globs['password'])
        # If there are already favourites, that's a problem, remove them. Messes with the count.
        if CP.HeaderHeartIcon(self.dr).favourites_count() != 0:
            CP.NavMenu.SalesResources(self.dr).open().my_sales_tools().click()
            for x in CP.MySalesTools(self.dr).get_favourites():
                x.close()
        # Navigate to the About page.
        try:
            CP.NavMenu.About(self.dr).open().about().click()
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).about()
        # Add some of the mosaics to Sales Tools
        mosaicad(3)
        # Navigate to Sales Resources > Australian Events.
        try:
            CP.NavMenu.SalesResources(self.dr).open().events().click()
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).events()
        # Click the Add To Sales Tools buttons of some of the Event Mosaics.
        mosaicad(3)
        # Navigate to Sales Resources > Fact Sheets.
        try:
            CP.NavMenu.SalesResources(self.dr).open().fact_sheets_overview().click()
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).factsheets()
        # Click the Add To Sales Tools buttons on a few of the results.
        try:
            search = CP.FilteredSearch(self.dr, fact_sheet_mode=True)
            for result in search.get_all_results():
                result.add_to_favourites()
                favtitles.add(result.get_title())
                self.dr.wait_until( # Use a wait instead of an assert, it takes a second to add.
                    lambda: len(favtitles) == CP.HeaderHeartIcon(self.dr).favourites_count(),
                    'Checking equality of my favourites count and favourites count display.')
        except Exception:
            self.add_error()
        # Click the Heart Icon in the header, the My Sales Tools page should be displayed.
        try:
            CP.HeaderHeartIcon(self.dr).click()
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).favourites()
        # The My Sales Tools page should have an entry for each of the pages added previously.
        tools = CP.MySalesTools(self.dr)
        faves = tools.get_favourites()
        favpagetitles = {x.get_title() for x in faves}
        try:
            self.assertSetEqual(favtitles, favpagetitles,
                                'The Sales Tools should contain every item previously added.')
        except Exception:
            self.add_error()
        # Entries should have an X button, a Title, a Description, and a More Info link.
        try:
            for fave in faves:
                fave.get_title()
                fave.get_description()
                fave.get_link()
                # Click several of the listed items' X buttons.
                fave.close()
        except Exception:
            self.add_error()
        # There will now be a set of buttons present instead of the favourites list.
        tools.home_search()
        # The entries should be removed from the list.
        self.assertEqual(0, len(tools.get_favourites()),
                         'Favourites list should be empty after removing all of them.')

    def test_13_My_Profile(self):
        """Tests the Profile page."""
        # Pre-condition: Should be signed in.
        self.dr.open_home_page()
        CP.SignIn(self).sign_in(self.globs['username'], self.globs['password'])
        # Navigate to the Profile page.
        try:
            CP.NavMenu(self.dr).profile().click()
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).profile()
        profile = CP.Profile(self.dr)
        # Modify the values of several of the fields, but leave TEST in the names.
        words = "A Series Of Random Words To Use For Sampling Or Some Such Thing".split()
        def pick_words(num: int):
            """Gets random words."""
            return [random.choice(words) for x in range(num)]
        bio = ' '.join(pick_words(10))
        lastname = ' TEST '.join(pick_words(2))
        try:
            state = profile.set_state()
            if self.globs['cn_mode']: partner = profile.set_partner()
            profile.bio = bio
            profile.lname = lastname
        except Exception:
            self.add_error()
        # Click the Save Changes button, a panel confirming changes saved should appear.
        profile.save_changes()
        # Refresh the page.
        self.dr.refresh()
        # The changed field values should remain.
        profile = CP.Profile(self.dr)
        self.assertEqual(profile.bio, bio, 'Biography should reflect changes made.')
        self.assertEqual(profile.state, state, 'State should reflect changes made.')
        if self.globs['cn_mode']: self.assertEqual(partner, profile.get_partner(),
                                                   'Partner should reflect changes made.')
        self.assertEqual(profile.lname, lastname, 'Name should reflect changes made.')
        self.assertIn(lastname.strip(), CP.NavMenu(self.dr).user_names(),
                      'Header Name Display should reflect changes made.')

    def test_14_Training_Summary(self):
        """Checks the Training Summary page."""
        # Tells the site that the user has completed five modules.
        dofimo = ('var o=["_core_mod1","_core_mod2","_core_mod3","_sto_vic","_sto_nsw"],e="{0}";'
            'for(m in o)if(o.hasOwnProperty(m))$.ajax({{url:"/bin/asp/trainingModule",type:"POST",cache:!1,dataType:"json"'
            ',data:{{isComplete:true,moduleId:e+o[m]}}}})').format(
                '_'.join(self.dr.locale[1:].split('.')[::-1]).replace('gb', 'uk'))

        def do_mod_then_back(mod: str) -> None:
            """Doing the Module clicks the Back To Training button, which leads to LIVE
            No guarantee that the testing is going on in LIVE, so go back manually."""
            nonlocal modules
            try:
                MOD.do_module(self.dr.driver, mod)  # Cheating a little, but w/e
            except Exception:
                self.add_error()
                # There are a lot of things that can go wrong here, just nuke the site from orbit.
                self.dr.execute_script(dofimo)
                    # It's the only way to be certain.
            self.dr.back()
            try:
                CP.NavMenu.Training(self.dr).open().training_summary().click()
            except Exception:
                self.add_error()
                CP.BackupHrefs(self.dr).training()
            modules = CP.TrainingSummary(self.dr)
        # Pre-condition: Should be signed in.
        self.dr.open_home_page()
        CP.SignIn(self).sign_in(self.globs['username'], self.globs['password'])
        # Navigate to Training > Training Summary.
        try:
            CP.NavMenu.Training(self.dr).open().training_summary().click()
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).training()

        # Wrap this whole test in an Oops, It's Not Working? Just Cheat! layer.
        try:
            modules = CP.TrainingSummary(self.dr)
            # Go do a few of the modules.
            # I did say that implementation details are to be done elsewhere.
            # But error handling is to be done here, and that takes priority.
            modules.module_one()
            do_mod_then_back('mod1')
            modules.module_two()
            do_mod_then_back('mod2')
            modules.module_three()
            do_mod_then_back('mod3')

            # Should receive a halfway email here.
            try:
                Email.LocalizedEmail(self.globs, self.dr, self.globs['userid'])
            except Exception:
                self.add_error()

            modn = modules.module_nsw()
            do_mod_then_back(modn)

            # Open this one, but don't finish it.
            try:
                modules.module_vic()
                modules.wait_for_module()
                # Get back out of the module before you try to access the menu.
                self.dr.switch_to_frame(None)
                CP.NavMenu.Training(self.dr).open().training_summary().click()
            except Exception:
                self.add_error()
                CP.BackupHrefs(self.dr).training()
            # Unstarted Modules and Paths should have a New label
            # Started-Not-Finished Modules and Paths should have an Incomplete label
            # Completed Modules and Paths should have the Complete label.
            modules = CP.TrainingSummary(self.dr)
            try:
                modules.completion_types()
            except Exception:
                self.add_error()

            modq = modules.module_qld()
            do_mod_then_back(modq)
        except Exception:   # Anything goes wrong with the modules, hack the badges and cugs in.
            self.add_error()
            self.dr.execute_script(dofimo)

        # Should receive the qualification email here.
        try:
            Email.LocalizedEmail(self.globs, self.dr, self.globs['userid'])
        except Exception:
            self.add_error()

        # Go back to the Profile page.
        try:
            CP.NavMenu(self.dr).profile().click()
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).profile()
        # The Modules' Completion Badges should be in the Recent Achievements list.
        profile = CP.Profile(self.dr)
        self.assertSetEqual({'mod1', 'mod2', 'mod3', modn, modq}, profile.module_badges(),
                            'The Profile should contain the badges of the modules just completed.')

    def test_15_Aussie_Specialist_Club(self):
        """Checks the Aussie Specialist Club nav menu links."""
        # Pre-condition: Logged in as a Qualified User.
        self.dr.open_home_page()
        CP.SignIn(self).sign_in(self.globs['username'], self.globs['password'])
        # Open the Aussie Specialist Club section in the Nav menu
        club = CP.NavMenu.AussieSpecialistClub(self.dr)
        club.click()
        # Should now be populated with the full set of links:
        # Aussie Specialist Club (Landing Page), Travel Club, Aussie Specialist Photos
        # Download Qualification Badge, Aussie Store (May not be available in all locales)
        club.aussie_specialist_club()
        club.aussie_specialist_photos()
        club.famils()
        club.travel_club()
        # But china doesn't have these two.
        if not self.globs['cn_mode']:
            club.asp_logo()
            club.aussie_store()

    def test_16_Travel_Club(self):
        """Tests the Travel Club search."""
        # Pre-condition: Logged in as a Qualified User.
        self.dr.open_home_page()
        CP.SignIn(self).sign_in(self.globs['username'], self.globs['password'])
        # Navigate to ASC > Travel Club
        try:
            CP.NavMenu.AussieSpecialistClub(self.dr).open().travel_club().click()
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).travel()
        # Search for results, changing the terms if none.
        travelsearch = CP.FilteredSearch(self.dr)
        travelsearch.random_search()
        # Look at the search results.
        self.look_at_search_results(travelsearch)

    def test_17_Famils(self):
        """Checks the Famils page."""
        # pre-condition: Logged in as a Qualified User.
        self.dr.open_home_page()
        CP.SignIn(self).sign_in(self.globs['username'], self.globs['password'])
        # Navigate to ASC > Famils
        try:
            CP.NavMenu.AussieSpecialistClub(self.dr).open().famils().click()
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).famils()
        # Maybe not available in all locales?
        # Should Display Famils page content.
        CP.Famils(self.dr)

    def test_18_Aussie_Specialist_Photos(self):
        """Checks the Aussie Specialist Photos page."""
        # pre-condition: Logged in as a Qualified User.
        self.dr.open_home_page()
        CP.SignIn(self).sign_in(self.globs['username'], self.globs['password'])
        # Navigate to ASC > AS Photos
        try:
            CP.NavMenu.AussieSpecialistClub(self.dr).open().aussie_specialist_photos().click()
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).photos()
        # Should display Instagram Image Tiles, with links and descriptions
        for pic in CP.AussieSpecialistPhotos(self.dr).random_images(10):
            pic.open()
            pic.get_description()
            if not self.globs['cn_mode']: # China does not have Instagram.
                pic.get_link()
            pic.close()

    def test_19_Download_Qualification_Badge(self):
        """Checks the Download Qualification Badge page."""
        # China doesn't have this?
        if self.globs['cn_mode']:
            self.skipTest("China doesn't have the Qualification Badge Download.")
        # Pre-condition: Logged in as a Qualified User.
        self.dr.open_home_page()
        CP.SignIn(self).sign_in(self.globs['username'], self.globs['password'])
        # Navigate to ASC > Download Qualification Badge
        CP.NavMenu.AussieSpecialistClub(self.dr).open().asp_logo().click()
        # Click the Download Qualification Badge link.
        # Badge image should be downloaded/opened in a new tab.
        CP.SpecialistBadge(self.dr)

    def submit_store_order(self):
        """When in the Aussie Store, submit an order.
        Except don't actually ever do this. That form is hooked up to real delivery agents,
        most of whom would rather not be bombarded with Test Emails."""
        raise NotImplementedError('Do Not.')    # Do Not.
        # pylint: disable-msg=W0101
        # Go to the Cart Page.
        self.dr.flashy_find_element('.fancybox-close').click()
        self.dr.flashy_find_element('#myCartIcon').click()
        # Click the Place Order button
        self.dr.flashy_find_element('.store-order-box-right a input').click()
        # Should redirect to the Order Confirmation page
        self.dr.quietly_find_element('.orderconfirmation')
        self.assertIn('confirmation.html', self.dr.current_url(),
                      'Ordering should have redirected to the Confirmation page.')
        # Confirmation Page should have notices of Order Placed,
        self.dr.quietly_find_element('.store-order-confirmed-text')
        # Should Receive Email (with the user's email address),
        self.dr.quietly_find_element('.confirmation-page p:nth-child(2)')
        # and Contact Us (which links to the Contact Us page).
        self.dr.quietly_find_element(
            '.confirmation-page p:nth-child(3) a[href*="about/contact-us.htm"]')

        #### Email validation to be done? Probably not, this is still verboten ####
        # Check your email client under the user's email address.
        # Should have received an email detailing the contents of the order
        # and the correct delivery address.
        # If the testing was done in PROD or LIVE environments, forward this email
        # to Nadine Christiansen <nchristiansen@tourism.australia.com>, flagging it
        # as a Test Order, so as to prevent the STO from trying to
        # deliver materials to the test address.

    def test_20_Aussie_Store(self):
        """Checks all of the Aussie Store functionality, except for actually placing an order."""
        # yes its a big method i know    pylint: disable-msg=R0914
        # China doesn't have the store.
        if self.globs['cn_mode']:
            self.skipTest("China doesn't have the Aussie Store.")
        # Just gotta put this here.
        def examine_products(category):
            """Given a category, check a bunch of randomly selected items."""
            nonlocal productcount, productnames
            # Click on the Category link.
            CP.AussieStore.CategoriesMenu(self.dr).goto_iteree(category)
            # Choose a few of the Products present, and for each of them {
            grid = CP.AussieStore.ProductGrid(self.dr)
            gridcount = grid.count()
            howmany = min([gridcount, max([gridcount//3, 5])])
            for prodnum in random.sample(range(gridcount), howmany):
                # Click on the Product Image
                prodname = grid.goto_iteree(prodnum)
                print(prodname)
                # Should link to the Product's Page
                product = CP.AussieStore.ProductPage(self.dr)
                self.assertEqual(prodname, product.name(),
                                 "A Product link should link to the same Product's page.")
                # Product Page should have a unique Code, which also should not be N/A or null.
                code = product.unique_code()
                self.assertNotIn('N/A', code,
                                 "It's important that the code not be 'N/A'. That isn't unique.")
                self.assertNotIn('null', code,
                                 "It's important that the code not be 'null'. That isn't unique.")
                # Select a Quantity.
                product.select_max_quantity()
                # Click the Add To Cart button.
                # However, If The Cart Is Full: (Once 10-12 or so Products have been added)
                if not product.add_to_cart():
                    # Currently, do not attempt to actually submit an order,
                    # this magnitude of unattended orders would upset someone at the STOs.
                    # do not self.submit_store_order(), just dump them.
                    CP.AussieStore(self.dr).my_cart()
                    CP.AussieStore.CartPage(self.dr).remove_all()
                    productcount = 0
                    productnames.clear()
                    CP.AussieStore.CategoriesMenu(self.dr).goto_iteree(category)
                    grid = CP.AussieStore.ProductGrid(self.dr)
                    continue
                # Otherwise, continue as normal.
                productcount += 1
                print(productnames)
                productnames.append(prodname.casefold())
                print(productnames)
                # Should redirect to the Cart page.
                cart = CP.AussieStore.CartPage(self.dr)
                # Cart page should show a list of all of the products added thus far.
                self.assertEqual(productnames, cart.get_product_names(),
                                 'The Cart page should list all of the products previously added.')
                # (do not do for all) Click the X beside one of the products.
                if random.random() < 0.2:
                    productnames.remove(cart.remove_random())
                    productcount -= 1
                    # That product should be removed from the Cart.
                    self.assertEqual(productnames, cart.get_product_names(),
                                     'The cart should no longer show a removed item.')
                else: # If one was removed, it's not going to be overbooked.
                    # Go back to the Product Page,
                    self.dr.back()
                    # and attempt to add more of it to the Cart, beyond the Quantity permitted.
                    product = CP.AussieStore.ProductPage(self.dr)
                    product.select_max_quantity()
                    # A panel should pop up, notifying that Maximum Quantity was exceeded.
                    self.assertFalse(product.add_to_cart(),
                                     "Shouldn't be able to add beyond max quantity, shows a popup.")
                # Back to Category Page, try the next one.
                CP.AussieStore.CategoriesMenu(self.dr).goto_iteree(category)
                grid = CP.AussieStore.ProductGrid(self.dr)

        # Pre-condition: Logged in as a Qualified User.
        self.dr.open_home_page()
        CP.SignIn(self).sign_in(self.globs['username'], self.globs['password'])
        # Preamblic mess.
        try:
            CP.NavMenu(self.dr).profile().click()
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).profile()
        def xandxplusy(x: str, y: str=', '):
            """Basically, if X is not blank, append Y to it."""
            return x and x + y
        # First, create a set of profile data that matches the formatting given in the Store.
        try:
            profile = CP.Profile(self.dr)
            # No space between the comma and newline on the address there.
            contactBlob = (profile.fname + ' ' + profile.lname + '\n' +
                           (xandxplusy(profile.address1) + xandxplusy(profile.address2) +
                            xandxplusy(profile.address3)).strip() + '\n' + profile.town +
                           '\n' + profile.get_state() + ', ' + profile.zip + '\n' +
                           profile.country + '\n' + profile.countrycode + profile.phone)
        except Exception:
            self.add_error()
            gotprof = False
        else:
            gotprof = True
        # Navigate to ASC > Aussie Store
        try:
            CP.NavMenu.AussieSpecialistClub(self.dr).open().aussie_store().click()
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).store()
        # Click the Cart button
        try:
            store = CP.AussieStore(self.dr)
            store.my_cart()
            # Should get a popup message about the Cart being Empty.
            store.empty_cart_notice()
        except Exception:
            self.add_error()
        # Click on one of the Product Images
        try:
            productname = CP.AussieStore.ProductGrid(self.dr).random_product()
            # Should redirect to that Product's page
            product = CP.AussieStore.ProductPage(self.dr)
            self.assertEqual(product.name(), productname,
                             "A Product link should link to that Product's page.")
            # Click the Add To Cart button, should go to the Cart Page
            product.add_to_cart()
            cart = CP.AussieStore.CartPage(self.dr)
            # The User's Name and Contact Details should be displayed with the same values
            # as displayed in the Profile. Any Blank Profile fields should not show up as 'null'.
            if gotprof:
                cartcontact = cart.contact_details()
                self.assertEqual(cartcontact, contactBlob,
                                 "The Cart contact details should match the user's Profile data.")
                self.assertNotIn('null', cartcontact,
                                 "The Cart contact details should contain no 'null' values.")
            # Tidy up the cart before going into the large test.
            cart.remove_all()
        except Exception:
            self.add_error()
        # For each of the categories, (except All Products), go through it,
        productcount = 0
        productnames = []
        try:
            catnum = CP.AussieStore.CategoriesMenu(self.dr).count()
            for cat in range(catnum)[1:]:
                # And do the stuff. And stop doing the stuff if the cart tops out.
                examine_products(cat)
        except Exception:
            self.add_error()

    def test_21_Premier_Badge(self):
        """Checks that the Profile Page has a Premier Badge. Expect this one to fail."""
        # Pre-condition: Logged in as a Premier User
        self.dr.open_home_page()
        CP.SignIn(self).sign_in(self.globs['username'], self.globs['password'])
        # Navigate to the Profile Page.
        try:
            CP.NavMenu(self.dr).profile().click()
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).profile()
        # The Status Badge area shows the Premier Aussie Specialist Icon.
        profile = CP.Profile(self.dr)
        self.assertEqual(profile.user_level(), CP.Profile.PREMIER,
                         'The Profile page should show a Premier badge for a Premier. But this '
                         'test usually fails when included in a Full Run.')

    def test_22_Forgotten_Username(self):
        """Tests the Forgotten Username feature."""
        self.dr.open_home_page()
        # Click the Sign In link
        # In the Sign In panel, click the Forgotten Username link.
        try:
            CP.SignIn(self).forgotten_username().click()
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).username()
        # Enter the user's email address into the Forgot Username form.
        forgus = CP.ForgottenForm(self.dr)
        forgus.email(self.globs['email'])
        # Click the Submit button, a panel should appear confirming submission.
        forgus.submit()
        # An email should be received at the given address containing the Username.
        usnaema = Email.ForgottenUsernameEmail(self.globs, self.dr, self.globs['userid'])
        self.assertEqual(self.globs['username'], usnaema.get_username(),
                         "The Username provided in the email should match the user's username.")

    def test_23_Forgotten_Password(self):
        """Tests the Forgotten Password feature."""
        self.dr.open_home_page()
        # Click the Sign In link
        # In the Sign In panel, click the Forgotten Password link.
        try:
            CP.SignIn(self).forgotten_password().click()
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).password()
        # Enter the user's email address into the Forgot Password form.
        forgpa = CP.ForgottenForm(self.dr)
        forgpa.email(self.globs['email'])
        # Click the Submit button, a panel should appear confirming submission.
        forgpa.submit()
        # An email should be received at the given address containing the Username and new Password
        uspaema = Email.ForgottenPasswordEmail(self.globs, self.dr, self.globs['userid'])
        self.assertEqual(self.globs['username'], uspaema.get_username(),
                         "The Username provided in the email should match the user's username.")
        # Read that email and sign in with the new password.
        self.globs['temp_pass'] = uspaema.get_password()

    def test_24_Change_Password(self):
        """Tests the Change Password feature."""
        self.dr.open_home_page()
        # Sign in with the new password, because these tests *are* being executed in order, right?
        try:
            # Signing in with a temp password should redirect to the Change page, catch it if not.
            CP.SignIn(self).sign_in(
                self.globs['username'], self.globs['temp_pass'], new_password=True)
            change = CP.ChangePassword(self.dr)
        except Exception:
            self.add_error()
            CP.BackupHrefs(self.dr).change()
            change = CP.ChangePassword(self.dr)
        # Fill out the Change Password Form with the Current Password and a New Password.
        change.current_password(self.globs['temp_pass'])
        change.new_password(self.globs['password'])    # Use the regular password, of course.
        # Click the Submit button, a panel should appear confirming the password change, and
        # The page should redirect back to the Profile page.
        change.submit()

    def test_25_Campaign(self):
        """Ensures that all emails received are in the correct locale."""
        # Pre-condition: User has registered, forgotten Username and
        # Password, and has Qualified, and received emails for each of these five events.
        # Links should point ot the correct pages in the correct locale.
        self.assertEqual(
            {self.globs['locale'][1:]},
            Email(self.globs, self.dr, self.globs['userid']).get_all_locales(),
            "The emails received should all link to the user's locale.")
