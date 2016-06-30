"""Test execution goes in here, but no browser interaction implementation details."""

import re
import random
import hashlib
import unittest
from tap import TAPTestRunner
import drivery as DR
import components as CP

class REGR(unittest.TestCase):
	"""The main test suite, a regression run of ASP Global"""
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
		about = CP.About()
		about.point()
		# The About section should have: About, Why Register,
		# Program FAQ, Site Usage, Contact Us
		about.about()
		about.benefits()
		about.how_to_use_the_site()
		about.program_faq()
		about.contact_us()

		# Click on 'Sales Resources' in the Mega Menu.
		sales = CP.SalesResources()
		sales.point()
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
		train = CP.Training()
		train.point()
		# The Training section should have: *Training (Landing page only)
		train.training()

		# Click on 'News & Products' in the Mega Menu.
		news = CP.NewsAndProducts()
		news.point()
		# The News section should have: *News and Product Updates (Landing page only)
		news.news_and_product_updates()

		# Click on 'Aussie Specialist Club' in the Mega Menu.
		club = CP.AussieSpecialistClub()
		club.point()
		# The Club section should have: *Aussie Specialist Club (Landing page only)
		club.aussie_specialist_club()

	def test_Footer(self) -> None:
		"""Checks the content of the Footer."""
		DR.open_home_page()
		footer = CP.Footer()
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
		self.assertIn('/splash.html', DR.current_url)

	def test_Sitemap(self) -> None:
		"""Checks the Sitemap page links."""
		DR.open_home_page()
		# Click the Sitemap link in the Footer.
		CP.Footer().sitemap().click()
		# Should link to the Sitemap page."
		DR.wait_for_page()
		self.assertIn('/sitemap.html', DR.current_url())
		# Sitemap page should have links to each of the pages in the Nav Menu
		nav_links = CP.NavMenu().get_all_links()
		sitemap_links = CP.Sitemap().get_all_links()
		self.assertTrue(nav_links.issubset(sitemap_links))
		# And should also have Change Password, Unsubscribe, and Coming Soon links.
		sitemap.change()
		sitemap.newsletter_unsubscribe()
		sitemap.coming_soon()

	def test_Filtered_Search__Itineraries(self) -> None:
		"""Checks the Itineraries Search."""
		DR.open_home_page()
		# Navigate to Sales Resources > Itinerary Suggestions.
		sales = SalesResources()
		sales.point()
		sales.itineraries_search_and_feature().click()
		# Do a random search and validate the results.
		search = CP.FilteredSearch()
		search.random_search()
		self.look_at_search_results(search)

	def test_Filtered_Search__Fact_Sheets(self) -> None:
		"""Tests the Fact Sheet Search."""
		DR.open_home_page()
		# Navigate to Sales Resources > Fact Sheets.
		sales = CP.SalesResources()
		sales.point()
		sales.fact_sheets_overview().click()
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
		# Examine the Map Menu, Should be four sections:
		# Cities, Iconic Destinaions, Itineraries, and Flight Times.
		controls = imap.Controls()
		cities = controls.Cities()
		icons = controls.IconicDestinations()
		itineraries = controls.Itineraries()
		flights = controls.FlyingTimes()
		# Open the Cities menu.
		cities.open_menu()
		# The Cities list should be shown, and the Map should be populated with Map Pins.
		DR.flashy_find_elements('#cities #city-children li[data-type="Cities"]')
		cipi = DR.flashy_find_elements('div.bulb.Cities')
		# Click a listed or pinned City. First make sure it's not behind another pin.
		cip = random.choice(cipi)
		jeva('$(arguments[0]).style($(this).style() + " z-index: 1002;");', cip)
		cip.click()
		# That City's Info Panel should be shown. Go examine it.
		self.map_info_panel(cip.text)
		# Open the Iconic Destinations menu
		DR.flashy_find_element('#map-menu > #icons').click()
		# The Icons list should be shown, and the Map should be populated with Destination Pins.
		DR.flashy_find_elements('#icons #icon-children li[data-type="Icons"]')
		icpi = DR.flashy_find_elements('div.bulb.Icons')
		# Click a listed or pinned Destination after bringing it to the front.
		icp = random.choice(icpi)
		jeva('$(arguments[0]).style($(this).style() + " z-index: 1002;");', icp)
		icp.click()
		# That Icon's Info Panel should be shown.
		self.map_info_panel(icp.text)
		# Open the Flying Times section.
		DR.flashy_find_element('#map-menu > #flights').click()
		# The Flying Times device appears.
		DR.quietly_find_element('.flight-children .flight-info')
		# Select a city in each of the From and To drop menus.
		flf = DR.flashy_find_element('#flightFrom')
		# Because it's a fancy custom select, can't just assign a value normally.
		jeva('$(arguments[0]).val(arguments[1]).change();', flf,\
			 random.choice(flf.find_elements_by_css_selector(\
			 'option:not([disabled]):not([value="0"])')).get_attribute('value'))
		# Have to do them separately, as the To menu is not initially populated.
		DR.quietly_find_element('#flightTo option:not([value="0"])')
		flt = DR.flashy_find_element('#flightTo')
		jeva('$(arguments[0]).val(arguments[1]).change();', flt,\
			 random.choice(flt.find_elements_by_css_selector(\
			 'option:not([disabled]):not([value="0"])')).get_attribute('value'))
		# The selected cities' Pins appear on the map,
		#   connected by a flight path, traversed by a plane icon.
		self.assertEqual(len(DR.flashy_find_elements('.bulb.FlyingTimes')), 2)
		# The flying Times panel shows the approximate flight time and distance.
		DR.quietly_find_element('.flight-time')
		DR.quietly_find_element('.flight-distance')

		def map_info_panel(self, name: str) -> None:
			"""Look at a Map Location Info Pane. Checks the various links and images."""
			# The right Info panel should be open.
			self.assertEqual(name, DR.flashy_find_element('#info-title').text)
			# The Find Out More and View Highlights buttons should link
			#   to a relevant Fact Sheet/Itinerary Plan.
			ili = DR.flashy_find_element('#info-moreUrl').get_attribute('href')
			self.assertIn(self.locale, ili)
			self.assertEqual(ili, DR.flashy_find_element('#info-optionalLink').get_attribute('href'))
			# Click the Photos
			DR.flashy_find_element('#info-carousel img').click()
			# The Photo Viewer should appear, can be scrolled through, displays different images.
			ims = DR.flashy_find_element('#carousel-lightbox img').get_attribute('src')
			DR.flashy_find_element('#next.lightbox-link').click()
			imsI = DR.flashy_find_element('#carousel-lightbox img').get_attribute('src')
			self.assertNotEqual(ims, imsI)
			DR.flashy_find_element('#next.lightbox-link').click()
			ims = DR.flashy_find_element('#carousel-lightbox img').get_attribute('src')
			self.assertNotEqual(ims, imsI)
			# Close the Photo Viewer
			DR.flashy_find_element('#close-lightbox').click()
			# Hold up a bit.
			time.sleep(blinkTime)
			# Now, it should be closed.
			self.assertFalse(DR.check_visible_quick('#carousel-lightbox'))
			# Click on one of the Itinerary Suggestion links
			iti = random.choice(DR.flashy_find_elements('#suggested-itineraries a[data-type="Itinerary"]'))
			itin = iti.text
			iti.click()
			# The selected Itinerary should open.
			DR.flashy_find_element('.bulb.ItinerarySteps')
			self.assertEqual(itin, DR.flashy_find_element('#info-title').text)
			# The Find Out More link should link to the relevant Itinerary Page.
			iliII = DR.flashy_find_element('#info-moreUrl').get_attribute('href')
			self.assertIn(self.locale, iliII)
			# Its route shoud appear and gain focus on the map.
			rop = random.choice(DR.flashy_find_elements('.itinerary-step a'))
			# Zoom out a bit first, the pins will sometimes pop up behind the menu panel.
			DR.flashy_find_element('#zoomout').click()
			# Click on one of the Route Pins
			rop.click()
			# An info box should appear at the pin.
			DR.flashy_find_element('.infoWindow.itinerarysteps')
			# Click the Back To Menu Button
			DR.flashy_find_element('#back-to-filter').click()
			# The panel should spin back to the Main Map Menu
			self.assertTrue(DR.flashy_find_element('#map-menu').is_displayed())

	def test_Contact_Us(self) -> None:
		"""Checks the Contact Us page."""
		DR.open_home_page()
		# Navigate to About > Contact Us.
		point(DR.flashy_find_element('#nav-main-panel-1'))
		DR.flashy_find_element('a[href*="contact-us.html"]').click()
		# Click the Contact Us link, Default email client should open, with the To field populated
		#   with the relevant contact. But can't actually test that. The mailto: should suffice.
		DR.quietly_find_element('a[href^="mailto:"]')

	def test_Registration(self) -> None:
		"""Checks the Registration process. Slight use of witchcraft."""
		DR.open_home_page()
		# Navigate to the Registration Page
		DR.flashy_find_element('#loginCompButton a[href*="registration-form.html"]').click()
		# Random letters to make a unique username.
		raid = ''.join([chr(random.randrange(65, 91)) for i in range(4)])
		# The Country Code
		lcod = self.locale.split('-')[1]
		# Username stuff, add the Environment prefix to identify and relocate the user.
		env = self.base_url.split('/')[2].split('.')[0][0:3]
		# Different zip codes in different countries.
		zipc = dict([('gb', 'A12BC'), ('us', '12345'), ('ca', '12345'), ('my', '12345'), \
					 ('id', '12345'), ('it', '12345'), ('fr', '12345')]).get(lcod, '123456')
		# Fill out the Registration Form with dummy information.
		# Ensure the Name fields are/contain TEST.
		DR.flashy_find_element('[name="lname"]').send_keys('TEST')
		DR.flashy_find_element('[name="fname"]').send_keys('TEST ' + lcod + env)
		DR.flashy_find_element('#birthday-day').send_keys('12')
		DR.flashy_find_element('#birthday-month').send_keys('12')
		DR.flashy_find_element('#birthday-year').send_keys('1212')
		DR.flashy_find_element('[name="companyname"]').send_keys('TEST')
		DR.flashy_find_element('[name="jobtitle"]').send_keys('TEST')
		Select(DR.flashy_find_element('[name="busprofile"]')).select_by_value('1')
		DR.flashy_find_element('[name="address1"]').send_keys('TEST')
		DR.flashy_find_element('[name="town"]').send_keys('TEST')
		DR.flashy_find_element('[name="zip"]').send_keys(zipc)
		Select(DR.flashy_find_element('#country_id')).select_by_value(lcod.upper())
		# Wait for the Country selection to load the State/Lang info.
		lan = DR.flashy_find_element('[name="language"] :not([value=""])')
		Select(DR.flashy_find_element('#language_id')).select_by_value(lan.get_attribute('value'))
		Select(DR.flashy_find_element('#state_list')).select_by_value(\
			DR.flashy_find_element('#state_list :not([value=""])').get_attribute('value'))
		DR.flashy_find_element("[name='web']").send_keys("www.TEST.com")
		DR.flashy_find_element('[name="mobile"]').send_keys('TEST')
		# Use an overloaded email.
		DR.flashy_find_element('#email').send_keys(self.email.replace('@', '+' + raid + '@'))
		DR.flashy_find_element('#verifyemail').send_keys(self.email.replace('@', '+' + raid + '@'))
		DR.flashy_find_element('#howmany').send_keys("1")
		DR.flashy_find_element('#how-many-times').send_keys("1")
		DR.flashy_find_element('#number-of-bookings').send_keys("1")
		for tra in DR.flashy_find_elements("[name='travelstandard']"): tra.click()
		for cus in DR.flashy_find_elements("[name='custexp']"): cus.click()
		DR.flashy_find_element("[name='username']").send_keys(lcod + env + raid)
		DR.flashy_find_element('#pwd').send_keys(self.passw)
		DR.flashy_find_element("[name='pwd1']").send_keys(self.passw)
		DR.flashy_find_element('#agreement').click()
		# Here, try something quite possibly illegal.
		def h() -> int: return(round(time.time() * 1000)) // (60 * 1000)
		def ha(bits: bytes) -> str: return hashlib.md5(bits + str(h()).encode()).hexdigest()[1:6]
		# It's time sensitive, so refresh the captcha immediately beforehand.
		DR.flashy_find_element('fieldset:nth-child(7) > div:nth-child(2) a').click()
		# It does have an #ID, but it's wierd and breaks the selector function. So use this.
		DR.flashy_find_element('[name="captcha"]').send_keys(\
			ha(DR.flashy_find_element('#cq_captchakey').get_attribute('value').encode()))
		# Click the Create Account button.
		DR.flashy_find_element("#register-submit").click()
		# Popup should appear confirming account creation.
		DR.quietly_find_element('#fancybox-thanks')
		# Email should be sent confirming this.
		# In the Registration Confirmation email, click the Activate Account link.
		# Should open the Registration Acknowledgement page, confirming the account is set up.

	def login_no(self):
		DR.open_home_page()
		# In the header, click the Sign In link.
		DR.flashy_find_element('.link-signin-text').click()
		# The Sign In panel should appear.
		# DR.quietly_find_element('#fancybox-login-form')
		# Enter the username and password of the User.
		DR.flashy_find_element('#j_username').send_keys(self.usern)
		DR.flashy_find_element('[name="j_password"]').send_keys(self.passw)
		# Click the Sign In button.
		DR.flashy_find_element('#usersignin').click()
		self.driver.find_element_by_id('link-logout')

	def test_Login(self):
		# Log in.
		self.login()
		# Should proceed to the Secure welcome page.
		DR.quietly_find_element('.hero-user-name')
		self.assertIn(self.base_url + self.locale + '/secure.html', DR.current_url())
		# Check the Nav Menu
		# The Sales section should now have the My Sales Tools link
		DR.flashy_find_element('#nav-main-panel-2').click()
		DR.quietly_find_element('#nav-main-panel-2 a[href*="my-sales-tools.html"]')
		# The Training Section should now have the Training Summary link.
		# The Training section should now have the Webinars link.
		DR.flashy_find_element('#nav-main-panel-3').click()
		DR.quietly_find_element('#nav-main-panel-3 a[href*="webinars.html"]')
		DR.quietly_find_element('#nav-main-panel-3 a[href*="training-summary.html"]')
		# The News & Updates section should have the Latest News Link
		# The News section should now  have the Product Updates link.
		DR.flashy_find_element('#nav-main-panel-4').click()
		DR.quietly_find_element('#nav-main-panel-4 a[href*="latest-news.html"]')
		DR.quietly_find_element('#nav-main-panel-4 a[href*="product-videos.html"]')
		# The Club section should not be present.
		self.assertFalse(DR.check_visible_quick('#nav-main-panel-5'))

	def test_Forgotten_Username(self):
		DR.open_home_page()
		# Click the Sign In link
		DR.flashy_find_element('.link-signin-text').click()
		# In the Sign In panel, click the Forgotten Username link.
		DR.flashy_find_element('a[href*="forgotten-username.html"]').click()
		# Enter the user's email address into the Forgot Username form.
		DR.flashy_find_element('#forgotemail').send_keys(self.email)
		# Click the Submit button.
		DR.flashy_find_element('#forgotUser-submit').click()
		# A panel should appear confirming submission.
		DR.quietly_find_element('.fancybox-skin')
		# An email should be received at the given address containing the Username.

	def test_Forgotten_Password(self):
		DR.open_home_page()
		# Click the Sign In link
		DR.flashy_find_element('.link-signin-text').click()
		# In the Sign In panel, click the Forgotten Password link.
		DR.flashy_find_element('a[href*="forgotten-password.html"]').click()
		# Enter the user's email address into the Forgot Password form.
		DR.flashy_find_element('#forgotemail').send_keys(self.email)
		# Click the Submit button.
		DR.flashy_find_element('#forgotUser-submit').click()
		# A panel should appear confirming submission.
		DR.quietly_find_element('.fancybox-skin')
		# An email should be received at the given address containing the Username and new Password
		# Read that email and sign in with the new password.

	def test_Change_Password(self):
		def double():
			self.login()
			# In the Nav Menu, click the My Profile link.
			DR.flashy_find_element('#link-profile').click()
			# Click the Change Password button, below the Profile Data fields.
			DR.flashy_find_element('a[href*="change.html"]').click()
			# Fill out the Change Password Form with the Current Password, and a New Password.
			DR.flashy_find_element('input[name="current"]').send_keys(self.passw)
			DR.flashy_find_element('input[name="newpwd"]').send_keys(self.passw[::-1])
			DR.flashy_find_element('input[name="confirmnew"]').send_keys(self.passw[::-1])
			# Click the Submit button.
			DR.flashy_find_element('#changepwd-submit').click()
			# A panel should appear confirming the password change.
			DR.quietly_find_element('.fancybox-skin')
			# The page should redirect back to the Profile page.
			DR.quietly_find_element('#profile-form')
			# Click the Sign Out link in the header.
			DR.flashy_find_element('#link-logout').click()

		double()
		# Sign back in with the New Password. The system should accept the new password.
		self.passw = self.passw[::-1]
		double()
		# Then change it back for the rest of the tests.
		self.passw = self.passw[::-1]

	def test_Favourites(self):
		mtl = set()
		def mosaicad(num):
			nonlocal mtc, mtl
			# Click on some of the Mosaic panels.
			inp = DR.flashy_find_elements('.flipper')
			random.shuffle(inp)
			for fli in inp[0:num]:
				scrl(fli)
				fli.click()
				# The Panels should unfold, showing a description, More Info link, and heart button.
				# They aren't too well labelled though, so be sure to actually watch the playback.
				opa = [x for x in DR.flashy_find_elements('.mosaic-item-detail-container.active')\
					   if x.is_displayed()][0]
				fop = blipper(opa.find_element_by_css_selector)
				self.assertTrue(fop('.l-padding-tb-30-lr-15 p').is_displayed())
				self.assertTrue(fop('a:not(.btn-bubble):not([href="#"])').is_displayed())
				# Click on the Heart buttons of those mosaics.
				fop('.btn-bubble').click()
				# The Heart Icon in the header should pulse and have a number incremented.
				self.assertEqual(mtc + 1, int(DR.flashy_find_element('.my-trip-count').text))
				mtc += 1
				mtl.add(fop('.line-through-container-biline').text)

		# Pre-condition: Should be signed in.
		self.login()
		# Navigate to the About page.
		DR.flashy_find_element('#nav-main-panel-1').click()
		DR.flashy_find_element('#nav-main-panel-1 a[href*="about.html"]').click()
		mtc = int(DR.flashy_find_element('.my-trip-count').text) or 0
		# Add some of the mosaics to Sales Tools
		mosaicad(3)
		# Navigate to Sales Resources > Australian Events.
		DR.flashy_find_element('#nav-main-panel-2').click()
		DR.flashy_find_element('#nav-main-panel-2 a[href*="events.html"]').click()
		# Click the Add To Sales Tools buttons of some of the Event Mosaics.
		mosaicad(6)
		# Navigate to Sales Resources > Fact Sheets.
		DR.flashy_find_element('#nav-main-panel-2').click()
		DR.flashy_find_element('#nav-main-panel-2 a[href*="fact-sheets-overview.html"]').click()
		# Click the Add To Sales Tools buttons on a few of the results.
		for b in DR.flashy_find_elements('a.btn-bubble'):
			scrl(b)
			b.click()
			self.assertEqual(mtc + 1, int(DR.flashy_find_element('.my-trip-count').text))
			mtc += 1
			# element.parent does not, in fact, return the parent element.
			mtl.add(blipper(b.find_element_by_xpath('../..').find_element_by_css_selector)\
					('.line-through-container').text)
		# Click the Heart Icon in the header.
		DR.flashy_find_element('.favourite-summary').click()
		# The My Sales Tools page should be displayed.
		DR.quietly_find_element('.dreamTrip')
		# The My Sales Tools page should have an entry for each of the pages added previously.
		mts = [x.text for x in DR.flashy_find_elements('.search-results-title')]
		for l in mtl:
			self.assertIn(l, mts)
		# Entries should have an X button, a Title, a Description, and a More Info link.
		for ls in DR.flashy_find_elements('.search-result-row-spacing'):
			fls = blipper(ls.find_element_by_css_selector)
			self.assertTrue(fls('.icon-close').is_displayed())
			self.assertTrue(fls('.search-results-title').is_displayed())
			self.assertTrue(fls('.mloverflow-text').is_displayed())
			self.assertTrue(fls('p > a').is_displayed())
		# Click several of the listed items' X buttons.
		for ls in DR.flashy_find_elements('.search-result-row-spacing'):
			blipper(ls.find_element_by_css_selector)('.icon-close').click()
		# The entries should be removed from the list.
		self.assertFalse(DR.check_visible_quick('.search-result-row-spacing'))

	def test_My_Profile(self):
		# Pre-condition: Should be signed in.
		self.login()
		# Navigate to the Profile page.
		DR.flashy_find_element('#link-profile').click()
		# Modify the values of several of the fields, but leave TEST in the names.
		wor = DR.flashy_find_element('html').get_attribute('class').split()
		def wos():
			return [random.choice(wor) for x in range(5)]
		bio = ' '.join(wos())
		lno = ' TEST '.join(wos())
		spc = random.choice(DR.flashy_find_elements('[name="state"] \
			option:not([value=""])')).get_attribute('value')
		obi = DR.flashy_find_element('[name="bio"]')
		obi.clear()
		obi.send_keys(bio)
		oln = DR.flashy_find_element('[name="lname"]')
		oln.clear()
		oln.send_keys(lno)
		# Again with this.
		csp = DR.flashy_find_element('[name="state"]')
		jeva('$(arguments[0]).val(arguments[1]).change();', csp, spc)
		# Click the Save Changes button.
		DR.flashy_find_element('#updateProfileSubmit').click()
		# A panel confirming changes saved should appear.
		DR.quietly_find_element('.fancybox-skin')
		# Refresh the page.
		self.driver.refresh()
		# The changed field values should remain.
		self.assertEqual(DR.flashy_find_element('[name="bio"]').text, bio)
		self.assertEqual(DR.flashy_find_element('[name="state"]').get_attribute('value'), spc)
		self.assertEqual(DR.flashy_find_element('[name="lname"]').get_attribute('value'), lno)
		self.assertIn(lno, DR.flashy_find_element('.link-signin-text').text)

		#### TODO ####
		# Navigate to Training > Training Summary.
		# Open a Module as yet incomplete.
		# Complete the Module.
		# Go back to the Profile page.
		# The Module's Completion Badge should be at the top of the Recent Achievements list.
		raise NotImplementedError("But that's fine, this bit isn't finished.")

	def test_Training_Summary(self):
		# Pre-condition: Should be signed in.
		self.login()
		# Navigate to Training > Training Summary.
		DR.flashy_find_element('#nav-main-panel-3').click()
		DR.flashy_find_element('a[href*="training-summary.html"]').click()
		# Change the value of the Optional Modules Filter Form.
		olm = '__'.join([x.text for x in DR.flashy_find_elements('.line-through-container-biline')])
		# A Special Select.
		jeva('$(arguments[0]).val(arguments[1]).change();',\
			 DR.flashy_find_element('[name="Optional"]'), 'TrainingModule:Optional/Niche')
		# Click Refresh Results.
		DR.flashy_find_element('#btn-id').click()
		time.sleep(showa)
		# The Optional Modules should be filtered.
		nlm = '__'.join([x.text for x in DR.flashy_find_elements('.line-through-container-biline')])
		self.assertNotEqual(olm, nlm)
		# Click the View More Modules button.
		omc = len(DR.flashy_find_elements('.line-through-container-biline'))
		DR.flashy_find_element('.load-more').click()
		time.sleep(showa)
		# Three more modules should be displayed, up to the total amount available.
		nmc = len(DR.flashy_find_elements('.line-through-container-biline'))
		self.assertEqual(omc + 3, nmc)
		omc = nmc
		DR.flashy_find_element('.load-more').click()
		time.sleep(showa)
		nmc = len(DR.flashy_find_elements('.line-through-container-biline'))
		self.assertEqual(omc + 1, nmc)
		omc = nmc
		DR.flashy_find_element('.load-more').click()
		time.sleep(showa)
		nmc = len(DR.flashy_find_elements('.line-through-container-biline'))
		self.assertEqual(omc, nmc)
		# Unstarted Modules should have a Let's Start button, and an (X) Incomplete label.
		blipper(DR.flashy_find_element('a[data-ta-data-layer*="trainingModuleFilterRefreshStart-ASP"]')\
			.find_element_by_xpath('../..').find_element_by_css_selector)\
			('.search-favourite img[src*="icon-incomplete.png"]')
		# Started-Not-Finished Modules should have an In Progress button and the Incomplete label.
		blipper(DR.flashy_find_element('a[data-ta-data-layer*="trainingModuleFilterRefreshResume-ASP"]')\
			.find_element_by_xpath('../..').find_element_by_css_selector)\
			('.search-favourite img[src*="icon-incomplete.png"]')
		# Completed Modules should have a Complete button and a (v/) Complete label.
		blipper(DR.flashy_find_element('a[data-ta-data-layer=""]').find_element_by_xpath('../..')\
			.find_element_by_css_selector)('.search-favourite img[src*="icon-complete.png"]')

	def test_Aussie_Specialist_Club(self):
		# Pre-condition: Logged in as a Qualified User.
		self.login()
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
		# Pre-condition: Logged in as a Qualified User.
		self.login()
		# Navigate to ASC > Travel Club
		club = CP.AussieSpecialistClub()
		club.click()
		club.travel_club().click()
		# Search for results, changing the terms if none.
		travelsearch = CP.FilteredSearch()
		travelsearch.random_search()
		# Look at the search results.
		self.look_at_search_results(travelsearch)

	def test_Famils(self):
		# pre-condition: Logged in as a Qualified User.
		self.login()
		# Navigate to ASC > Famils
		DR.flashy_find_element('#nav-main-panel-5').click()
		DR.flashy_find_element('#nav-main-panel-5 a[href*="aussie-specialist-club/famils.html"]').click()
		# Maybe not available in all locales?
		# Should Display Famils page content.
		for fam in DR.flashy_find_elements('.type-body'):
			self.assertTrue(fam.is_displayed())

	def test_Aussie_Specialist_Photos(self):
		# pre-condition: Logged in as a Qualified User.
		self.login()
		# Navigate to ASC > AS Photos
		DR.flashy_find_element('#nav-main-panel-5').click()
		DR.flashy_find_element('#nav-main-panel-5 a[href*="aussie-specialist-photos.html"]').click()
		# Should display Instagram Image Tiles, with links and descriptions
		for pic in random.sample(DR.flashy_find_elements('.mosaic-item .flipper'), 10):
			def picl(el, sel):
				# In case the virtual mouse flips into the image
				self.assertTrue(el.find_element_by_css_selector(sel).is_enabled())
			picl(pic, 'img[src*="image.adapt"]')
			pic.click()
			pio = [x for x in DR.flashy_find_elements('.mosaic-item-detail-container.active') if x.is_displayed()][0]
			picl(pio, 'p')
			picl(pio, 'a[href="http://www.instagram.com/australia"]')
			pic.click()

	def test_Download_Qualification_Badge(self):
		# Pre-condition: Logged in as a Qualified User.
		self.login()
		# Navigate to ASC > Download Qualification Badge
		DR.flashy_find_element('#nav-main-panel-5').click()
		DR.flashy_find_element('#nav-main-panel-5 a[href*="aussie-specialist-club/asp-logo.html"]').click()
		# Click the Download Qualification Badge link.
		DR.flashy_find_element('a[href*="asp-badge.png"]').click()
		# Badge image should be downloaded/opened in a new tab.
		DR.switch_to_window(DR.window_handles[1])
		DR.quietly_find_element('img[src*="asp-badge.png"]')

#### TODO: Get the website thing to check the email thing? ####
	def test_Campaign(self):
		# TODO: Implement action: "pre-condition: User has registered, forgotten Username and
		# Password, and has Qualified, and received emails for each of these five events."
		# TODO: Implement action: "Check the wording and links of each of the five emails:"
		# TODO: Implement action: "Registration Acknowledgement"
		# TODO: Implement action: "Forgotten Username"
		# TODO: Implement action: "Forgotten Password"
		# TODO: Implement action: "Half Way Through Course"
		# TODO: Implement action: "Course Complete"
		# TODO: Implement result: "Link should point ot the correct pages in the correct locale."
		# TODO: Implement result: "Email and subject line is fully translated, if applicable."
		raise NotImplementedError("For now, go check it yourself?")

	def verlere(self):
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
		# Just gotta put this here.
		def examine_products(cat):
			nonlocal pco, prl
			cal = '.nav-store-categories-menu li a[href="' + cat + '"]'
			# Click on the Category link.
			DR.flashy_find_element(cal).click()
			# Choose a few of the Products present, and for each of them {
			prs = [x.get_attribute('href').replace(self.base_url, '')\
				   for x in DR.flashy_find_elements('.store-products-item')]
			kay = min([len(prs), max([len(prs)//3, 5])])
			for pr in random.sample(prs, kay):
				# Click on the Product Image
				pri = DR.flashy_find_element('a[href="' + pr + '"]')
				prn = pri.find_element_by_css_selector('.store-products-item-title').text.casefold()
				pri.click()
				# Should link to the Product's Page
				self.assertEqual(prn, DR.flashy_find_element('.home-hero-title').text.casefold())
				# Product Page should have a unique Code, which also should not be N/A or null.
				self.assertNotIn('N/A', DR.flashy_find_element('.product-code').text)
				self.assertNotIn('null', DR.flashy_find_element('.product-code').text)
				# Select a Quantity.
				qua = DR.flashy_find_element('[name="product-quantity"]')
				qua.send_keys(qua.find_elements_by_tag_name('option')[-1].get_attribute('value'))
				# Click the Add To Cart button.
				DR.flashy_find_element('#cart').click()
				# However, If The Cart Is Full: (Once 10-12 or so Products have been added)
				time.sleep(showa)
				if DR.check_visible_quick('#fancybox-cookieoverflow'):
					# Leave this bit out for now.
					return True
					# Other Things.
					#self.verlere()
					pco = 0
					prl.clear()
					continue
				# Otherwise or afterwards, continue as normal.
				pco += 1
				prl.add(prn)
				# Should redirect to the Cart page.
				DR.quietly_find_element('.store-my-cart')
				self.assertIn('cart.html', DR.current_url())
				# Cart page should show a list of all of the products added thus far.
				self.assertEqual(prl, {x.text.casefold() for x in DR.flashy_find_elements('.cell-title')})
				# (do not do for all) Click the X beside one of the products.
				if random.random() < 0.2:
					rei = random.randint(0, len(prl)-1)
					rem = DR.flashy_find_elements('.cell-title')[rei].text.casefold()
					reb = DR.flashy_find_elements('.product-remove')[rei]
					scrl(reb)
					reb.click()
					prl.remove(rem)
					pco -= 1
					# That product should be removed from the Cart.
					self.assertEqual(prl, {x.text.casefold() for x in DR.flashy_find_elements('.cell-title')})
				else: # If this one was removed, it's not going to be overbooked.
					# Go back to the Product Page,
					self.driver.back()
					time.sleep(showa)
					# and attempt to add more of it to the Cart, beyond the Quantity permitted.
					qua = DR.flashy_find_element('[name="product-quantity"]')
					qua.send_keys(qua.find_elements_by_tag_name('option')[-1]\
								  .get_attribute('value'))
					DR.flashy_find_element('#cart').click()
					# A panel should pop up, notifying that Maximum Quantity was exceeded.
					DR.quietly_find_element('#fancybox-maxerror')
					DR.flashy_find_element('.fancybox-close').click()
				# Back to Category Page, try the next one.
				DR.flashy_find_element(cal).click()
			return False

		# Pre-condition: Logged in as a Qualified User.
		self.login()
		# Preamblic mess.
		DR.flashy_find_element('#link-profile').click()
		def adn(s):
			return s + ', ' if s else ''
		# Some sort of conditional prepension.
		phone = DR.flashy_find_element('[name="countrycode"]').get_attribute('value') +\
				DR.flashy_find_element('[name="phone"]').get_attribute('value')
		phone = phone + '\n' if phone else phone
		contactBlob = (DR.flashy_find_element('[name="fname"]').get_attribute('value') + ' ' +\
					   DR.flashy_find_element('[name="lname"]').get_attribute('value') + '\n' +\
					   adn(DR.flashy_find_element('[name="address1"]').get_attribute('value')) +\
					   adn(DR.flashy_find_element('[name="address2"]').get_attribute('value')) +\
					   # Trim one extra space from here, apparently.
					   adn(DR.flashy_find_element('[name="address3"]').get_attribute('value'))[0:-1] + '\n' +\
					   DR.flashy_find_element('[name="town"]').get_attribute('value') + '\n' +\
					   DR.flashy_find_element('[name="state"] option[value="' +\
					   # And add one extra one here.
					   DR.flashy_find_element('[name="state"]').get_attribute('value') + '"]').text + ',  ' +\
			DR.flashy_find_element('[name="zip"]').get_attribute('value') + '\n' +\
			DR.flashy_find_element('[name="country"]').get_attribute('value') + phone)
		# Navigate to ASC > Aussie Store
		DR.flashy_find_element('#nav-main-panel-5').click()
		DR.flashy_find_element('#nav-main-panel-5 a[href*="aussie-specialist-club/aussie-store.html"]').click()
		# Click the Cart button
		DR.flashy_find_element('#myCartIcon').click()
		# Should get a popup message about the Cart being Empty.
		DR.quietly_find_element('.fancybox-skin')
		DR.flashy_find_element('.fancybox-close').click()
		# Click on one of the Product Images
		pri = random.choice(DR.flashy_find_elements('.store-products-item'))
		prn = pri.find_element_by_xpath('..')\
			  .find_element_by_css_selector('.store-products-item-title').text.casefold()
		pri.click()
		# Should redirect to that Product's page
		self.assertEqual(prn, DR.flashy_find_element('.home-hero-title').text.casefold())
		# Click the Add To Cart button
		DR.flashy_find_element('#cart').click()
		# Should go to the Cart Page
		DR.quietly_find_element('.store-my-cart')
		# The User's Name and Contact Details should be displayed with the same values
		# as displayed in the Profile. Any Blank Profile fields should not show up as 'null'.
		blobContact = DR.flashy_find_element('.store-order-box-left > p:nth-child(2)').text
		self.assertTrue(re.match(blobContact.replace(' ', r'\s+').replace('\n', '\\s+'),\
								 contactBlob))
		self.assertNotIn('null', blobContact)
		# Tidy up first
		DR.flashy_find_element('.product-remove').click()
		time.sleep(showa)
		# For each of the categories, (except All Products), go through it,
		pco = 0
		prl = set()
		cats = [x.get_attribute('href').replace(self.base_url, '') for x in \
				DR.flashy_find_elements('.nav-store-categories-menu li a:not([href*="all-products"])')]
		for cat in cats:
			# And do the stuff. And stop doing the stuff if the cart tops out.
			if examine_products(cat): break

		# The Downloads section isn't actually there, so never mind this bit?
		# TODO: Click on the Downloads Category link.
		# TODO: Navigates to the Downloads page.

	def test_Premier_Badge(self):
		# Pre-condition: Logged in as a Premier User
		self.login()
		# Navigate to the Profile Page.
		DR.flashy_find_element('#link-profile').click()
		# The Status Badge area shows the Premier Aussie Specialist Icon.
		DR.quietly_find_element('#profile-form > div:nth-child(2) a > img[src*="achievements/3.png"]')

if __name__ == '__main__':
	tests = unittest.TestSuite()
	tests.addTests(unittest.makeSuite(REGR))

	runner = TAPTestRunner()
	runner.set_outdir('./')
	runner.set_format('Result of: {method_name} - {short_description}')
	runner.run(tests)
