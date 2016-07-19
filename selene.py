"""Test execution goes in here, but no browser interaction implementation details."""

import os
import random
import unittest
from tap import TAPTestRunner
import drivery as DR
import modules as MOD
import components as CP

class REGR(unittest.TestCase): # pylint: disable-msg=R0904
	"""The main test suite, a regression run of ASP Global"""
	# No, the naming scheme is necessary.
	# pylint: disable-msg=C0103
	# They can't be functions, that would defeat the entire purpose of the test suite.
	# pylint: disable-msg=R0201
	def setUp(self) -> None:
		"""Called just before each test is run, sets up the browser and test records."""
		# Initialise the browser connection.
		self.verificationErrors = []
		self.accept_next_alert = True
		DR.begin()

	def tearDown(self) -> None:
		"""Called after finishing each test, closes the browser and counts up the errors."""
		DR.close()
		self.assertEqual([], self.verificationErrors)

	# Tests start here.
	def test_Splash_Page(self) -> None:
		"""Tests the Splash Page."""
		# Open the splash page.
		DR.splash_page()
		# Concerning the Languages Selector
		langsel = CP.SplashSelect()
		# The list should contain all locales.
		self.assertSetEqual(DR.LOCALE_SET, langsel.get_values())
		# Select the country from the dropdown.
		langsel.choose_locale()
		# Page should redirect to its respective locale.
		DR.wait_for_page()
		self.assertIn(DR.LOCALE, DR.current_url())

	def test_Homepage(self) -> None:
		"""Tests the Welcome Page content."""
		DR.open_home_page()
		# Video should be present.
		video = CP.WelcomeVideo()
		# Login and Register buttons should be present in the body content.
		CP.BodyLoginButton()
		CP.BodyRegisterButton()
		# The What You Can See Mosaic is displayed, contains five tiles.
		mosaic = CP.WhatYouCanSeeMosaic()
		self.assertEqual(mosaic.tile_count(), 5)
		# Play the video.
		video.play()
		# Video loads and plays.
		self.assertTrue(video.is_playing())

	def test_Navigation(self) -> None:
		"""Checks that the contents of the Signed Out Nav Menu are correct."""
		DR.open_home_page()
		# Click on 'About' in the Mega Menu.
		about = CP.About().point()
		# The About section should have: About, Why Register,
		# Program FAQ, Site Usage, Contact Us
		about.about()
		about.benefits()
		about.how_to_use_the_site()
		about.program_faq()
		about.contact_us()

		# Click on 'Sales Resources' in the Mega Menu.
		sales = CP.SalesResources().point()
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

		# Click on 'Training' in the Mega Menu.
		train = CP.Training().point()
		# The Training section should have: *Training (Landing page only)
		train.training()

		# Click on 'News & Products' in the Mega Menu.
		news = CP.NewsAndProducts().point()
		# The News section should have: *News and Product Updates (Landing page only)
		news.news_and_product_updates()

		# Click on 'Aussie Specialist Club' in the Mega Menu.
		club = CP.AussieSpecialistClub().point()
		# The Club section should have: *Aussie Specialist Club (Landing page only)
		club.aussie_specialist_club()

	def test_Footer(self) -> None:
		"""Checks the content of the Footer."""
		DR.open_home_page()
		footer = CP.Footer()
		if DR.CN_MODE:
			# China is different, of course.
			footer.wechat()
		else:
			# The Footer should have: Find us on: Social icons and links.
			footer.facebook()
			footer.twitter()
			footer.plus_google()
			footer.instagram()
			footer.youtube()
		# About this site: links through to relevant pages
		footer.sitemap()
		footer.privacy_policy()
		footer.terms_and_conditions()
		footer.terms_of_use()
		footer.contact_us()
		# Other sites: Links through to Aus.com, Corporate site and Business Events.
		footer.australia()
		footer.tourism_australia()
		footer.businessevents_australia()
		# Click the Change Your Country link.
		footer.splash().click()
		# Should link back to the Splash page.
		DR.wait_for_page()
		self.assertIn('/splash.html', DR.current_url())

	def test_Sitemap(self) -> None:
		"""Checks the Sitemap page links."""
		DR.open_home_page()
		# Click the Sitemap link in the Footer.
		CP.Footer().sitemap().click()
		# Should link to the Sitemap page."
		DR.wait_for_page()
		self.assertIn('/sitemap.html', DR.current_url())
		# Sitemap page should have links to each of the pages in the Nav Menu
		sitemap = CP.Sitemap()
		nav_links = CP.NavMenu().get_all_links()
		sitemap_links = sitemap.get_all_links()
		self.assertTrue(nav_links.issubset(sitemap_links))
		# And should also have Change Password, Unsubscribe, and Coming Soon links.
		sitemap.change()
		sitemap.newsletter_unsubscribe()
		sitemap.coming_soon()

	def test_Filtered_Search__Itineraries(self) -> None:
		"""Checks the Itineraries Search."""
		DR.open_home_page()
		# Navigate to Sales Resources > Itinerary Suggestions.
		CP.SalesResources().point().itineraries_search_and_feature().click()
		# Do a random search and validate the results.
		search = CP.FilteredSearch()
		search.random_search()
		self.look_at_search_results(search)

	def test_Filtered_Search__Fact_Sheets(self) -> None:
		"""Tests the Fact Sheet Search."""
		DR.open_home_page()
		# Navigate to Sales Resources > Fact Sheets.
		CP.SalesResources().point().fact_sheets_overview().click()
		# Do a random search. (In Fact Sheet +PDFs Mode) Then validate the results.
		search = CP.FilteredSearch(fact_sheet_mode=True)
		search.random_search()
		self.look_at_search_results(search)
		# Alright, done there back up.
		DR.back()
		# Because the page was reloaded, have to refresh the references.
		search = CP.FilteredSearch(fact_sheet_mode=True)
		result = search.get_random_result()
		# Click on a result's Download PDF link.
		result.download_pdf()
		# The relevant PDF should open in a new (second) (so number 1) window.
		DR.switch_to_window(1)
		CP.PDFPage()

	def look_at_search_results(self, searcher: CP.FilteredSearch) -> None:
		"""Validates the search results and the View More button."""
		# If the counter is present on this page, validate it against the number of results.
		count = searcher.read_results_counter()
		if count is not None:
			firstcount = searcher.count_results()
			self.assertEqual(count[0], firstcount)
			# Now see if it updates upon Loading More Results.
			searcher.load_more()
			secondcount = searcher.count_results()
			count = searcher.read_results_counter()
			# At most five more results should be displayed, up to the maximum matching amount.
			self.assertEqual(secondcount, min(firstcount + 5, count[1]))
			# Check a random result, make sure it links to the right page.
			result = searcher.get_random_result()
			name = result.get_title().casefold()
			# Click on the result's More Info link.
			result.view_more_information()
			# Should link to that result's More Info page.
			self.assertEqual(result.SearchResultPage().get_title().casefold(), name)

	def test_Interactive_Map(self) -> None:
		"""Checks the Interactive Map page."""
		# Navigate to Sales Resources > Interactive Map
		DR.open_home_page()
		CP.HeaderMapIcon().click()
		# (Switches into the Map Iframe.)
		imap = CP.InteractiveMap()
		# Map Menu should have: Cities, Iconic Destinaions, Itineraries, and Flight Times.
		controls = imap.Controls()
		cities = controls.Cities()
		icons = controls.IconicDestinations()
		controls.Itineraries()
		flights = controls.FlyingTimes()
		# Open the Cities menu, the Cities list should be shown.
		cities.open_menu()
		# The Map should be populated with Map Pins.
		# Click a pinned City, remember which one it was.
		pin = imap.MapArea.MapPins().pick_random()
		# That City's Info Panel should be shown. Go examine it.
		self.map_info_panel(pin)
		# Open the Iconic Destinations menu
		icons.open_menu()
		# The Icons list should be shown, and the Map should be populated with Destination Pins.
		# Click a random pinned Destination.
		pin = imap.MapArea.MapPins().pick_random()
		# That Icon's Info Panel should be shown, verify all that.
		self.map_info_panel(pin)
		# Open the Flying Times section, the Flying Times device appears.
		flights.open_menu()
		# Select a city in each of the From and To drop menus.
		ffrom = flights.choose_from()
		fto = flights.choose_to()
		# The selected cities' Pins appear on the map,
		#   connected by a flight path, traversed by a plane icon.
		pins = imap.MapArea.MapPins()
		self.assertEqual(pins.count(), 2)
		names = pins.get_names()
		self.assertIn(ffrom, names)
		self.assertIn(fto, names)
		# The flying Times panel shows the approximate flight time and distance.
		flights.flight_time()
		flights.flight_distance()

	def map_info_panel(self, name: str) -> None:
		"""Look at a Map Location Info Pane. Checks the various links and images."""
		# The right Info panel should be open.
		panel = CP.InteractiveMap.Controls.InfoPanel()
		self.assertEqual(name, panel.get_title())
		# The Find Out More and View Highlights buttons should link
		#   to a relevant Fact Sheet/Itinerary Plan.
		fomlink = panel.find_out_more()
		self.assertIn(DR.LOCALE, fomlink)
		self.assertEqual(fomlink, panel.view_highlights())
		# Click the Photos
		imgnum = panel.count_photos()
		photos = panel.open_photos()
		# The Photo Viewer should appear, can be scrolled through, displays different images.
		# But if there was only one image available, skip this scrolling bit.
		if not imgnum == 1:
			imgone = photos.current_image_source()
			photos.next()
			imgtwo = photos.current_image_source()
			self.assertNotEqual(imgone, imgtwo)
			photos.next()
			imgone = photos.current_image_source()
			self.assertNotEqual(imgtwo, imgone)
		# Close the Photo Viewer
		photos.close()
		# Click on one of the Itinerary Suggestion links
		itiname = panel.random_itinerary()
		# If there were no Itinerary links, skip this bit.
		if itiname != '':
			# New panel, renew the selector.
			panel = CP.InteractiveMap.Controls.InfoPanel()
			# The selected Itinerary should open.
			self.assertEqual(itiname, panel.get_title())
			# Its route should appear and gain focus on the map, but zoom out a bit first,
			# the pins will sometimes pop up behind the menu panel.
			CP.InteractiveMap.ZoomTools().zoom_out()
			pins = CP.InteractiveMap.MapArea.MapPins()
			# The Find Out More link should link to the relevant Itinerary Page.
			self.assertIn(DR.LOCALE, panel.find_out_more())
			# Click on one of the Route Pins
			pins.pick_random()
			# An info box should appear at the pin.
			CP.InteractiveMap.MapArea.InfoPopup()
		# Click the Back To Menu Button, the panel should spin back to the Main Map Menu
		panel.back_to_menu()

	def test_Contact_Us(self) -> None:
		"""Checks the Contact Us page."""
		DR.open_home_page()
		# Navigate to About > Contact Us.
		CP.About().point().contact_us().click()
		# "Click the Contact Us link, Default email client should open, with the To field populated
		#   with the relevant contact." Can't actually test that, so a 'mailto:' will have to do.
		CP.ContactUs()

	def test_Registration(self) -> None:
		"""Checks the Registration process."""
		global USERID, USERNAME
		DR.open_home_page()
		# Navigate to the Registration Page
		CP.BodyRegisterButton().click()
		# Random letters to make a unique username.
		USERID = ''.join([chr(random.randrange(65, 91)) for i in range(4)])
		# The Country Code
		langcode, localecode = DR.LOCALE.split('-')
		# Username stuff, add the Environment prefix to identify the user.
		environ = DR.BASE_URL.split('/')[2].split('.')[0][0:3]
		# Different zip codes in different countries.
		zipcode = {'gb': 'A12BC', 'us': '12345', 'ca': '12345', 'my': '12345', 'id': '12345', \
			'it': '12345', 'fr': '12345', 'de': '12345'}.get(localecode, '123456')
		# Fill out the Registration Form with dummy information.
		# Ensure the Name fields are/contain TEST.
		form = CP.RegistrationForm()
		form.plain_text_fields('TEST')
		form.web = 'www.TEST.com'
		form.lname = 'TEST ' + localecode + environ
		form.date_of_birth('12/12/1212')
		form.pick_business_profile()
		form.zip = zipcode
		form.pick_country(localecode.upper())
		form.pick_state()
		form.pick_language(langcode)
		# Use an overloaded email.
		form.email_address(DR.EMAIL.format(USERID))
		form.how_many_years()
		form.how_many_times()
		form.how_many_bookings()
		form.standard_categories()
		form.experiences()
		# Better hope this test comes before the other ones!
		USERNAME = localecode + environ + USERID
		form.username = USERNAME
		form.password(DR.PASSWORD)
		form.terms_and_conditions()
		form.decaptcha()
		# Click the Create Account button, popup should appear confirming account creation.
		form.submit()
		# Email should be sent confirming this.
		regemail = DR.Email.RegistrationEmail(USERID)
		self.assertEqual({DR.LOCALE[1:]}, regemail.get_locale())
		# In the Registration Confirmation email, click the Activate Account link.
		# Should open the Registration Acknowledgement page, confirming the account is set up.
		DR.get(regemail.activation_link())

	def test_Login(self):
		"""Tests the Login-related functionality."""
		# Log in.
		DR.open_home_page()
		CP.SignIn().sign_in(USERNAME, DR.PASSWORD)
		# Should proceed to the Secure welcome page.
		self.assertIn(DR.LOCALE + '/secure.html', DR.current_url())
		# Check the Nav Menu
		# The Sales section should now have the My Sales Tools link
		CP.SalesResources().click().my_sales_tools()
		# The Training Section should now have the Training Summary and Webinars links.
		train = CP.Training().click()
		train.webinars()
		train.training_summary()
		# The News & Updates section should have the Latest News Link
		# The News section should now  have the Product Updates link.
		news = CP.NewsAndProducts().click()
		news.latest_news()
		news.product_videos()
		# The Club section should not be present. (Don't instantiate it, it isn't there)
		self.assertTrue(CP.AussieSpecialistClub.not_present())

	def test_Forgotten_Username(self):
		"""Tests the Forgotten Username feature."""
		DR.open_home_page()
		# Click the Sign In link
		# In the Sign In panel, click the Forgotten Username link.
		CP.SignIn().forgotten_username().click()
		# Enter the user's email address into the Forgot Username form.
		forgus = CP.ForgottenForm()
		forgus.email(DR.EMAIL.format(USERID))
		# Click the Submit button, a panel should appear confirming submission.
		forgus.submit()
		# An email should be received at the given address containing the Username.
		usnaema = DR.Email.ForgottenUsernameEmail(USERID)
		self.assertEqual(USERNAME, usnaema.get_username())

	def test_Forgotten_Password(self):
		"""Tests the Forgotten Password feature."""
		global TEMP_PASS
		DR.open_home_page()
		# Click the Sign In link
		# In the Sign In panel, click the Forgotten Password link.
		CP.SignIn().forgotten_password().click()
		# Enter the user's email address into the Forgot Password form.
		forgpa = CP.ForgottenForm()
		forgpa.email(DR.EMAIL.format(USERID))
		# Click the Submit button, a panel should appear confirming submission.
		forgpa.submit()
		# An email should be received at the given address containing the Username and new Password
		uspaema = DR.Email.ForgottenPasswordEmail(USERID)
		self.assertEqual(USERNAME, uspaema.get_username())
		# Read that email and sign in with the new password.
		TEMP_PASS = uspaema.get_password()

	def test_Change_Password(self):
		"""Tests the Change Password feature."""
		DR.open_home_page()
		# Sign in with the new password, because these tests are being executed in order, right?
		CP.SignIn().sign_in(USERNAME, TEMP_PASS)
		# In the Nav Menu, click the My Profile link.
		CP.NavMenu().profile().click()
		# Click the Change Password button, below the Profile Data fields.
		CP.Profile().change().click()
		# Fill out the Change Password Form with the Current Password and a New Password.
		change = CP.ChangePassword()
		change.current_password(TEMP_PASS)
		change.new_password(DR.PASSWORD)	# Use the regular password, of course.
		# Click the Submit button, a panel should appear confirming the password change, and
		# The page should redirect back to the Profile page.
		change.submit()

	def test_Favourites(self):
		"""Tests the Sales Tools functionality."""
		favtitles = set()
		def mosaicad(num):
			"""Opens a mosaic, checks it, and adds it to sales tools"""
			nonlocal favcount, favtitles
			# Click on some of the Mosaic panels.
			for tile in CP.WhatYouCanSeeMosaic().random_selection(num):
				tile.open()
				# The Panels should unfold, showing a description, More Info link, and heart button.
				# They aren't too well labelled though, so be sure to actually watch the playback.
				self.assertTrue(tile.get_description().is_displayed())
				self.assertTrue(tile.get_link().is_displayed())
				# Click on the Heart buttons of those mosaics.
				tile.add_to_favourites()
				# The Heart Icon in the header should pulse and have a number incremented.
				favcount += 1
				self.assertEqual(favcount, CP.HeaderHeartIcon().favourites_count())
				favtitles.add(tile.get_title())

		# Pre-condition: Should be signed in.
		DR.open_home_page()
		CP.SignIn().sign_in(USERNAME, DR.PASSWORD)
		favcount = CP.HeaderHeartIcon().favourites_count()
		# If there are already favourites, that's a problem, remove them. Messes with the count.
		if favcount > 0:
			favcount = 0
			CP.SalesResources().click().my_sales_tools().click()
			for x in CP.MySalesTools().get_favourites():
				x.close()
		# Navigate to the About page.
		CP.About().click().about().click()
		# Add some of the mosaics to Sales Tools
		mosaicad(3)
		# Navigate to Sales Resources > Australian Events.
		CP.SalesResources().click().events().click()
		# Click the Add To Sales Tools buttons of some of the Event Mosaics.
		mosaicad(6)
		# Navigate to Sales Resources > Fact Sheets.
		CP.SalesResources().click().fact_sheets_overview().click()
		# Click the Add To Sales Tools buttons on a few of the results.
		search = CP.FilteredSearch(fact_sheet_mode=True)
		for result in search.get_all_results():
			result.add_to_favourites()
			favcount += 1
			self.assertEqual(favcount, CP.HeaderHeartIcon().favourites_count())
			favtitles.add(result.get_title())
		# Click the Heart Icon in the header, the My Sales Tools page should be displayed.
		CP.HeaderHeartIcon().click()
		# The My Sales Tools page should have an entry for each of the pages added previously.
		faves = CP.MySalesTools().get_favourites()
		favpagetitles = {x.get_title() for x in faves}
		self.assertTrue(favtitles.issubset(favpagetitles))
		# Entries should have an X button, a Title, a Description, and a More Info link.
		for fave in faves:
			fave.get_title()
			fave.get_description()
			fave.get_link()
			# Click several of the listed items' X buttons.
			fave.close()
		# The entries should be removed from the list.
		self.assertEqual(0, len(CP.MySalesTools().get_favourites()))

	def test_My_Profile(self):
		"""Tests the Profile page."""
		# Pre-condition: Should be signed in.
		DR.open_home_page()
		CP.SignIn().sign_in(USERNAME, DR.PASSWORD)
		# Navigate to the Profile page.
		CP.NavMenu().profile().click()
		profile = CP.Profile()
		# Modify the values of several of the fields, but leave TEST in the names.
		words = "A Series Of Random Words To Use For Sampling Or Some Such Thing".split()
		def pick_words(num: int):
			"""Gets random words."""
			return [random.choice(words) for x in range(num)]
		bio = ' '.join(pick_words(10))
		lastname = ' TEST '.join(pick_words(2))
		state = profile.set_state()
		profile.bio = bio
		profile.lname = lastname
		# Click the Save Changes button, a panel confirming changes saved should appear.
		profile.save_changes()
		# Refresh the page.
		DR.refresh()
		# The changed field values should remain.
		profile = CP.Profile()
		self.assertEqual(profile.bio, bio)
		self.assertEqual(profile.state, state)
		self.assertEqual(profile.lname, lastname)
		self.assertIn(lastname.strip(), CP.NavMenu().user_names())

	def test_Training_Summary(self):
		"""Checks the Training Summary page."""
		# Pre-condition: Should be signed in.
		DR.open_home_page()
		CP.SignIn().sign_in(USERNAME, DR.PASSWORD)
		# Navigate to Training > Training Summary.
		CP.Training().click().training_summary().click()
		modules = CP.TrainingSummary()
		# Change the value of the Optional Modules Filter Form.
		oldlist = modules.get_optional_titles()
		modules.filter_optional_niche()
		# The Optional Modules should be filtered.
		newlist = modules.get_optional_titles()
		self.assertNotEqual(oldlist, newlist)
		modules.filter_optional_sto()
		# Click the View More Modules button.
		oldcount = modules.count_modules()
		modules.load_more()
		# Three more modules should be displayed, up to the total amount available.
		newcount = modules.count_modules()
		self.assertEqual(oldcount + 3, newcount)
		oldcount = newcount
		modules.load_more()
		newcount = modules.count_modules()
		self.assertEqual(oldcount + 2, newcount)
		oldcount = newcount
		modules.load_more()
		newcount = modules.count_modules()
		self.assertEqual(oldcount, newcount)

		# Go do a few of the modules.
		modules.module_one()
		MOD.do_module(DR.DRIVER, '1')
		DR.back();DR.back()	# The module clicks the Back To Training.
		modules = CP.TrainingSummary()
		modules.module_two()
		MOD.do_module(DR.DRIVER, '2')
		DR.back();DR.back()	# That button links to the LIVE page.
		modules = CP.TrainingSummary()
		modules.module_three()
		MOD.do_module(DR.DRIVER, '3')
		DR.back();DR.back()	# No guarantee that we are testing LIVE, though.
		modules = CP.TrainingSummary()

		# Should receive a halfway email here.
		halfway = DR.Email.LocalizedEmail(USERID)
		# Open this one, but don't finish it.
		modules.module_vic()
		DR.back()
		modules = CP.TrainingSummary()
		# Unstarted Modules should have a Let's Start button, and an (X) Incomplete label.
		# Started-Not-Finished Modules should have an In Progress button and the Incomplete label.
		# Completed Modules should have a Complete button and a (v/) Complete label.
		modules.completion_types()

		modules.module_nsw()
		MOD.do_module(DR.DRIVER, 'nsw')
		DR.back();DR.back()
		modules = CP.TrainingSummary()
		modules.module_qld()
		MOD.do_module(DR.DRIVER, 'qld')
		DR.back()

		# Should receive the qualification email here.
		qualified = DR.Email.LocalizedEmail(USERID)

		# Go back to the Profile page.
		CP.NavMenu().profile().click()
		# The Modules' Completion Badges should be in the Recent Achievements list.
		profile = CP.Profile()
		self.assertSetEqual({'mod1', 'mod2', 'mod3', 'nsw', 'qld'}, profile.module_badges())

	def test_Aussie_Specialist_Club(self):
		"""Checks the Aussie Specialist Club nav menu links."""
		# Pre-condition: Logged in as a Qualified User.
		DR.open_home_page()
		CP.SignIn().sign_in(USERNAME, DR.PASSWORD)
		# Open the Aussie Specialist Club section in the Nav menu
		club = CP.AussieSpecialistClub()
		club.click()
		# Should now be populated with the full set of links:
		# Aussie Specialist Club (Landing Page), Travel Club, Aussie Specialist Photos
		# Download Qualification Badge, Aussie Store (May not be available in all locales)
		club.aussie_specialist_club()
		club.travel_club()
		club.aussie_specialist_photos()
		club.asp_logo()
		club.aussie_store()

	def test_Travel_Club(self):
		"""Tests the Travel Club search."""
		# Pre-condition: Logged in as a Qualified User.
		DR.open_home_page()
		CP.SignIn().sign_in(USERNAME, DR.PASSWORD)
		# Navigate to ASC > Travel Club
		CP.AussieSpecialistClub().click().travel_club().click()
		# Search for results, changing the terms if none.
		travelsearch = CP.FilteredSearch()
		travelsearch.random_search()
		# Look at the search results.
		self.look_at_search_results(travelsearch)

	def test_Famils(self):
		"""Checks the Famils page."""
		# pre-condition: Logged in as a Qualified User.
		DR.open_home_page()
		CP.SignIn().sign_in(USERNAME, DR.PASSWORD)
		# Navigate to ASC > Famils
		CP.AussieSpecialistClub().click().aussie_specialist_club().click()
		# Maybe not available in all locales?
		# Should Display Famils page content.
		CP.Famils()

	def test_Aussie_Specialist_Photos(self):
		"""Checks the Aussie Specialist Photos page."""
		# pre-condition: Logged in as a Qualified User.
		DR.open_home_page()
		CP.SignIn().sign_in(USERNAME, DR.PASSWORD)
		# Navigate to ASC > AS Photos
		CP.AussieSpecialistClub().click().aussie_specialist_photos().click()
		# Should display Instagram Image Tiles, with links and descriptions
		for pic in CP.AussieSpecialistPhotos().random_images(10):
			pic.open()
			pic.get_description()
			pic.get_link()
			pic.close()

	def test_Download_Qualification_Badge(self):
		"""Checks the Download Qualification Badge page."""
		# Pre-condition: Logged in as a Qualified User.
		DR.open_home_page()
		CP.SignIn().sign_in(USERNAME, DR.PASSWORD)
		# Navigate to ASC > Download Qualification Badge
		CP.AussieSpecialistClub().click().asp_logo().click()
		# Click the Download Qualification Badge link.
		# Badge image should be downloaded/opened in a new tab.
		CP.SpecialistBadge()

	def test_Campaign(self):
		"""Ensures that all emails received are in the correct locale."""
		# Pre-condition: User has registered, forgotten Username and
		# Password, and has Qualified, and received emails for each of these five events.
		# Links should point ot the correct pages in the correct locale.
		self.assertEqual({DR.LOCALE[1:]}, DR.Email(USERID).get_all_locales())

	def submit_store_order(self):
		"""When in the Aussie Store, submit an order.
		Except don't actually ever do this. That form is hooked up to real delivery agents,
		most of whom would rather not be bombarded with Test Emails."""
		# Go to the Cart Page.
		DR.flashy_find_element('.fancybox-close').click()
		DR.flashy_find_element('#myCartIcon').click()
		# Click the Place Order button
		DR.flashy_find_element('.store-order-box-right a input').click()
		# Should redirect to the Order Confirmation page
		DR.quietly_find_element('.orderconfirmation')
		self.assertIn('confirmation.html', DR.current_url())
		# Confirmation Page should have notices of Order Placed,
		DR.quietly_find_element('.store-order-confirmed-text')
		# Should Receive Email (with the user's email address),
		DR.quietly_find_element('.confirmation-page p:nth-child(2)')
		# and Contact Us (which links to the Contact Us page).
		DR.quietly_find_element('.confirmation-page p:nth-child(3) a[href*="about/contact-us.html"]')

		#### TODO: Email valdation? ####
		# Check your email client under the user's email address.
		# Should have received an email detailing the contents of the order
		# and the correct delivery address.
		# If the testing was done in PROD or LIVE environments, forward this email
		# to Nadine Christiansen <nchristiansen@tourism.australia.com>, flagging it
		# as a Test Order, so as to prevent the STO from trying to
		# deliver materials to the test address.

	def test_Aussie_Store(self):
		"""Checks all of the Aussie Store functionality, except for actually placing an order."""
		# Just gotta put this here.
		def examine_products(category):
			"""Given a category, check a bunch of randomly selected items."""
			nonlocal productcount, productnames
			# Click on the Category link.
			CP.AussieStore.CategoriesMenu().goto_iteree(category)
			# Choose a few of the Products present, and for each of them {
			grid = CP.AussieStore.ProductGrid()
			gridcount = grid.count()
			howmany = min([gridcount, max([gridcount//3, 5])])
			for prodnum in random.sample(range(gridcount), howmany):
				# Click on the Product Image
				prodname = grid.goto_iteree(prodnum)
				# Should link to the Product's Page
				product = CP.AussieStore.ProductPage()
				self.assertEqual(prodname, product.name())
				# Product Page should have a unique Code, which also should not be N/A or null.
				code = product.unique_code()
				self.assertNotIn('N/A', code)
				self.assertNotIn('null', code)
				# Select a Quantity.
				product.select_max_quantity()
				# Click the Add To Cart button.
				# However, If The Cart Is Full: (Once 10-12 or so Products have been added)
				if not product.add_to_cart():
					# Currently, do not attempt to actually submit an order,
					# this magnitude of unattended orders would upset someone at the STOs.
					# do not self.submit_store_order(), just dump them.
					CP.AussieStore().my_cart()
					CP.AussieStore.CartPage().remove_all()
					productcount = 0
					productnames.clear()
					CP.AussieStore.CategoriesMenu().goto_iteree(category)
					grid = CP.AussieStore.ProductGrid()
					continue
				# Otherwise, continue as normal.
				productcount += 1
				productnames.add(prodname.casefold())
				# Should redirect to the Cart page.
				cart = CP.AussieStore.CartPage()
				# Cart page should show a list of all of the products added thus far.
				self.assertEqual(productnames, {x.casefold() for x in cart.get_product_names()})
				# (do not do for all) Click the X beside one of the products.
				if random.random() < 0.2:
					productnames.remove(cart.remove_random())
					productcount -= 1
					# That product should be removed from the Cart.
					self.assertEqual(productnames, {x.casefold() for x in cart.get_product_names()})
				else: # If one was removed, it's not going to be overbooked.
					# Go back to the Product Page,
					DR.back()
					# and attempt to add more of it to the Cart, beyond the Quantity permitted.
					product = CP.AussieStore.ProductPage()
					product.select_max_quantity()
					# A panel should pop up, notifying that Maximum Quantity was exceeded.
					self.assertFalse(product.add_to_cart())
				# Back to Category Page, try the next one.
				CP.AussieStore.CategoriesMenu().goto_iteree(category)
				grid = CP.AussieStore.ProductGrid()

		# Pre-condition: Logged in as a Qualified User.
		DR.open_home_page()
		CP.SignIn().sign_in(USERNAME, DR.PASSWORD)
		# Preamblic mess.
		CP.NavMenu().profile().click()
		def xandxplusy(x: str, y: str=', '):
			"""Basically, if X is not blank, append Y to it."""
			return x and x + y
		# First, create a set of profile data that matches the formatting given in the Store.
		profile = CP.Profile()
		# No space between the comma and newline on the address there.
		contactBlob = profile.fname + ' ' + profile.lname + '\n' + \
			(xandxplusy(profile.address1) + xandxplusy(profile.address2) + \
				xandxplusy(profile.address3)).strip() + '\n' + \
			profile.town + '\n' + \
			profile.get_state() + ', ' + profile.zip + '\n' + \
			profile.country + '\n' + \
			profile.countrycode + profile.phone
		# Navigate to ASC > Aussie Store
		CP.AussieSpecialistClub().click().aussie_store().click()
		# Click the Cart button
		store = CP.AussieStore()
		store.my_cart()
		# Should get a popup message about the Cart being Empty.
		store.empty_cart_notice()
		# Click on one of the Product Images
		productname = CP.AussieStore.ProductGrid().random_product()
		# Should redirect to that Product's page
		product = CP.AussieStore.ProductPage()
		self.assertEqual(product.name(), productname)
		# Click the Add To Cart button, should go to the Cart Page
		product.add_to_cart()
		cart = CP.AussieStore.CartPage()
		# The User's Name and Contact Details should be displayed with the same values
		# as displayed in the Profile. Any Blank Profile fields should not show up as 'null'.
		cartcontact = cart.contact_details()
		self.assertEqual(cartcontact, contactBlob)
		self.assertNotIn('null', cartcontact)
		# Tidy up the cart before going into the large test.
		cart.remove_all()
		# For each of the categories, (except All Products), go through it,
		productcount = 0
		productnames = set()
		catnum = CP.AussieStore.CategoriesMenu().count()
		for cat in range(catnum)[1:]:
			# And do the stuff. And stop doing the stuff if the cart tops out.
			examine_products(cat)

	def test_Premier_Badge(self):
		"""Checks that the Profile PPage has a Premier Badge. Expect this one to fail."""
		# Pre-condition: Logged in as a Premier User
		DR.open_home_page()
		CP.SignIn().sign_in(USERNAME, DR.PASSWORD)
		# Navigate to the Profile Page.
		CP.NavMenu().profile().click()
		# The Status Badge area shows the Premier Aussie Specialist Icon.
		profile = CP.Profile()
		self.assertEqual(profile.user_level(), CP.Profile.PREMIER)

if __name__ == '__main__':
	# Not really constants, no. 	pylint: disable-msg=C0103
	tests = unittest.TestSuite()
	loader = unittest.TestLoader()
	# INTROSPECTIVE ANALYSIS!
	# Sort the tests by declaration order, not alphabetical order.
	ln = lambda f: getattr(REGR, f).__code__.co_firstlineno
	lncmp = lambda a, b: ln(a) - ln(b)
	loader.sortTestMethodsUsing = lncmp
	tests.addTests(loader.loadTestsFromTestCase(REGR))

	runner = TAPTestRunner()
	runner.set_outdir(os.path.join(os.path.split(__file__)[0]))
	runner.set_format('Result of: {method_name} - {short_description}')
	runner.run(tests)
