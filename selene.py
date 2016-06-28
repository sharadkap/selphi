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
		about.about().point()
		aufi('[href*="about/benefits.html"]')
		aufi('[href*="about/program-faq.html"]')
		aufi('[href*="about/how-to-use-the-site.html"]')
		aufi('[href*="about/contact-us.html"]')

		# Click on 'Sales Resources' in the Mega Menu.
		sales = elec('#nav-main-panel-2')
		point(sales)
		# The Sales section should have: Sales Resources (Landing), Interactive Map,
		# Fact Sheets, Useful Websites, Image and video galleries, My sales tools,
		# Itinerary Search, Australian Events, Destination FAQ
		safi = blipper(sales.find_element_by_css_selector)
		safi('[href*="sales-resources.html"]')
		safi('[href*="sales-resources/interactive-map.html"]')
		safi('[href*="sales-resources/itineraries-search-and-feature.html"]')
		safi('[href*="sales-resources/fact-sheets-overview.html"]')
		safi('[href*="sales-resources/events.html"]')
		safi('[href*="sales-resources/useful-sites.html"]')
		safi('[href*="sales-resources/destination-faq.html"]')
		safi('[href*="sales-resources/image-and-video-galleries.html"]')

		# Click on 'Training' in the Mega Menu.
		train = elec('#nav-main-panel-3')
		point(train)
		# The Training section should have: *Training (Landing page only)
		blipper(train.find_element_by_css_selector)('[href*="training.html"]')

		# Click on 'News & Products' in the Mega Menu.
		news = elec('#nav-main-panel-4')
		point(news)
		# The News section should have: *News and Product Updates (Landing page only)
		blipper(news.find_element_by_css_selector)('[href*="news-and-product-updates.html"]')

		# Click on 'Aussie Specialist Club' in the Mega Menu.
		club = elec('#nav-main-panel-5')
		point(club)
		# The Club section should have: *Aussie Specialist Club (Landing page only)
		blipper(club.find_element_by_css_selector)('[href*="aussie-specialist-club.html"]')

	def test_Footer(self) -> None:
		"""Checks the content of the Footer."""
		self.homepage()
		# The Footer should have: Find us on: Social icons and links.
		sofi = blipper(elec('.default-social-list').find_element_by_css_selector)
		sofi('a[href="https://www.facebook.com/SeeAustralia"]')
		sofi('a[href="https://twitter.com/australia"]')
		sofi('a[href="https://plus.google.com/+australia"]')
		sofi('a[href="http://instagram.com/australia"]')
		sofi('a[href="http://www.youtube.com/user/australia"]')
		# About this site: links through to relevant pages
		fiau = blipper(elec('.footer-type-light').find_element_by_css_selector)
		fiau('a[href*="sitemap.html"]')
		fiau('a[href*="privacy-policy.html"]')
		fiau('a[href*="terms-and-conditions.html"]')
		fiau('a[href*="terms-of-use.html"]')
		fiau('a[href*="about/contact-us.html"]')
		# Other sites: Links through to Aus.com, Corporate site and Business Events.
		fios = blipper(elec('.l-list-clean:not(.footer-type-light)').find_element_by_css_selector)
		fios('a[href*="www.australia.com"]')
		fios('a[href*="www.tourism.australia.com"]')
		fios('a[href*="businessevents.australia.com/businessevents"]')
		# Click the Change Your Country link.
		elec('a[href="/splash.html"]').click()
		# Should link back to the Splash page.
		verf('.splash-screen')
		self.assertEqual(self.driver.current_url, self.base_url + '/splash.html')

	def test_Sitemap(self) -> None:
		"""Checks the Sitemap page links."""
		self.homepage()
		# Click the Sitemap link in the Footer.
		elec('a[href*="sitemap.html"]').click()
		# Should link to the Sitemap page."
		self.assertEqual(self.driver.current_url, self.base_url + self.locale + '/sitemap.html')
		# Sitemap page should have links to each of the pages in the Nav Menu
		navas = {x.get_attribute('href') for x in \
 			elecs('.main-nav-panel .nav-bar-nav.nav-bar-left a:not([href^="#"])')}
		simas = {x.get_attribute('href') for x in elecs('.sitemap a')}
		self.assertTrue(navas.issubset(simas))
		# And should also have Change Password, Unsubscribe, and Coming Soon links.
		moras = {self.base_url + self.locale + x for x in \
			 ['/change.html', '/newsletter-unsubscribe.html', '/coming-soon.html']}
		self.assertTrue(moras.issubset(simas))

	def search_for_results(self, FactMode: bool=False) -> None:
		"""Randomly searches with a Filtered Search Component until it finds some results.

		As the Fact Sheet one is different, includes a switch for whether it should
		also check for the presence of a PDF Download link."""
		# Enter Search Criteria into the Search Form dropdowns, Click Refresh Results,
		for x in elecs('.atdw-refresh-results-wrapper select'):
			x.send_keys(random.choice([y.get_attribute('value') \
				for y in x.find_elements_by_tag_name('option')]))
		elec('.btn-primary.transparent').click()
		# Wait twice as long for loading, it is much slower than loading a page.
		for i in range(impwa * 2):
			# If the Loading Bubbles are still present, keep waiting.
			if nelec('.preload-no-transition-support-image.is-show-preload-animation'):
				time.sleep(1)
			else: break
		else: self.fail("Loading Results Timed Out.")
		# If no results are returned, try again, hopefully with different Search Terms.
		if not nelec('.mosaic-item'): self.search_for_results()
		# Factsheets test wants at least one PDF though
		if FactMode and not nelec('.download-pdf'): self.search_for_results()

	def look_at_search_results(self) -> None:
		"""Validates the search results and the View More button."""
		# If the counter is present on this page, count the number of results.
		# Otherwise, never mind.
		if nelec('.search-result-count-copy'):
			# Get a list of all of the numbers that appear in the counter.
			def shor():
				return [int(x) for x in re.findall(r'\d+', elec('.search-result-count-copy').text)]
			# Count the number of results.
			co = len(elecs('.mosaic-item'))
			# Different languages display the counter in different orders, so just make sure the
			# right number is in there somewhere.
			self.assertIn(co, shor())
			# Click the View More button.
			elec('.load-more').click()
			# Wait for them to load.
			for i in range(impwa * 2):
				if nelec('.preload-no-transition-support-image.is-show-preload-animation'):
					time.sleep(1)
				else: break
			else: self.fail("Loading More Timed Out.")
			# At least five more results should be displayed, up to the maximum matching amount.
			con = len(elecs('.mosaic-item'))
			self.assertIn(con, shor())
			self.assertTrue(con == co + 5 or con == max(shor()))
		# Check the first result's title.
		frst = elec('.mosaic-item')
		firf = blipper(frst.find_element_by_css_selector)
		nem = firf('.line-through-container-biline').text.casefold()
		# Click on the first result's More Info link.
		firf('a[data-ta-data-key]').click()
		# Should link to that result's More Info page.
		self.assertEqual(elec('.tabreadcrumb li:nth-child(4)').text.casefold(), nem)

	def test_Filtered_Search__Itineraries(self) -> None:
		"""Checks the Itineraries Search."""
		self.homepage()
		# Navigate to Sales Resources > Itinerary Suggestions.
		point(elec('#nav-main-panel-2 > a'))
		elec('#nav-main-panel-2 a[href*="itineraries-search-and-feature.html"]').click()
		# First, wait until the initial results are loaded, or they'll interrupt later.
		verf('.mosaic-item')
		# Get some search results.
		self.search_for_results()
		# Check the search results
		self.look_at_search_results()

	def test_Filtered_Search__Fact_Sheets(self) -> None:
		"""Tests the Fact Sheet Search."""
		self.homepage()
		# Navigate to Sales Resources > Fact Sheets.
		point(elec('#nav-main-panel-2 > a'))
		elec('#nav-main-panel-2 a[href*="fact-sheets-overview.html"]').click()
		# First, wait until the initial results are loaded, or they'll interrupt later.
		verf('.mosaic-item')
		# Get Some Results. With a PDF download handy.
		self.search_for_results(FactMode=True)
		# Check the View More, look at one, should go to the right page.
		self.look_at_search_results()
		# Click on a result's Download PDF link.
		self.driver.back()
		# Note the pdf source.
		pdl = elec('.download-pdf')
		pdh = pdl.get_attribute('href')
		pdl.click()
		# The relevant PDF should open in a new window.
		self.driver.switch_to_window(self.driver.window_handles[1])
		verf('embed[type="application/pdf"],.pdfViewer')
		self.assertEqual(pdh, self.driver.current_url)

	def map_info_panel(self, name: str) -> None:
		"""Look at a Map Location Info Pane. Checks the various links and images."""
		# The right Info panel should be open.
		self.assertEqual(name, elec('#info-title').text)
		# The Find Out More and View Highlights buttons should link
		#   to a relevant Fact Sheet/Itinerary Plan.
		ili = elec('#info-moreUrl').get_attribute('href')
		self.assertIn(self.locale, ili)
		self.assertEqual(ili, elec('#info-optionalLink').get_attribute('href'))
		# Click the Photos
		elec('#info-carousel img').click()
		# The Photo Viewer should appear, can be scrolled through, displays different images.
		ims = elec('#carousel-lightbox img').get_attribute('src')
		elec('#next.lightbox-link').click()
		imsI = elec('#carousel-lightbox img').get_attribute('src')
		self.assertNotEqual(ims, imsI)
		elec('#next.lightbox-link').click()
		ims = elec('#carousel-lightbox img').get_attribute('src')
		self.assertNotEqual(ims, imsI)
		# Close the Photo Viewer
		elec('#close-lightbox').click()
		# Hold up a bit.
		time.sleep(blinkTime)
		# Now, it should be closed.
		self.assertFalse(nelec('#carousel-lightbox'))
		# Click on one of the Itinerary Suggestion links
		iti = random.choice(elecs('#suggested-itineraries a[data-type="Itinerary"]'))
		itin = iti.text
		iti.click()
		# The selected Itinerary should open.
		elec('.bulb.ItinerarySteps')
		self.assertEqual(itin, elec('#info-title').text)
		# The Find Out More link should link to the relevant Itinerary Page.
		iliII = elec('#info-moreUrl').get_attribute('href')
		self.assertIn(self.locale, iliII)
		# Its route shoud appear and gain focus on the map.
		rop = random.choice(elecs('.itinerary-step a'))
		# Zoom out a bit first, the pins will sometimes pop up behind the menu panel.
		elec('#zoomout').click()
		# Click on one of the Route Pins
		rop.click()
		# An info box should appear at the pin.
		elec('.infoWindow.itinerarysteps')
		# Click the Back To Menu Button
		elec('#back-to-filter').click()
		# The panel should spin back to the Main Map Menu
		self.assertTrue(elec('#map-menu').is_displayed())

	def test_Interactive_Map(self) -> None:
		"""Checks the Interactive Map page."""
		# Navigate to Sales Resources > Interactive Map
		self.homepage()
		elec('.icon-map').click()
		# Swith into the Map Iframe.
		self.driver.switch_to_frame('interactiveMapId')
		# Examine the Map Menu, Should be four sections:
		# Cities, Iconic Destinaions, Itineraries, and Flight Times.
		verf('#map-menu > #cities')
		verf('#map-menu > #icons')
		verf('#map-menu > #itinerarytypes')
		verf('#map-menu > #flights')
		# Open the Cities menu.
		elec('#map-menu > #cities').click()
		# The Cities list should be shown, and the Map should be populated with Map Pins.
		elecs('#cities #city-children li[data-type="Cities"]')
		cipi = elecs('div.bulb.Cities')
		# Click a listed or pinned City. First make sure it's not behind another pin.
		cip = random.choice(cipi)
		jeva('$(arguments[0]).style($(this).style() + " z-index: 1002;");', cip)
		cip.click()
		# That City's Info Panel should be shown. Go examine it.
		self.map_info_panel(cip.text)
		# Open the Iconic Destinations menu
		elec('#map-menu > #icons').click()
		# The Icons list should be shown, and the Map should be populated with Destination Pins.
		elecs('#icons #icon-children li[data-type="Icons"]')
		icpi = elecs('div.bulb.Icons')
		# Click a listed or pinned Destination after bringing it to the front.
		icp = random.choice(icpi)
		jeva('$(arguments[0]).style($(this).style() + " z-index: 1002;");', icp)
		icp.click()
		# That Icon's Info Panel should be shown.
		self.map_info_panel(icp.text)
		# Open the Flying Times section.
		elec('#map-menu > #flights').click()
		# The Flying Times device appears.
		verf('.flight-children .flight-info')
		# Select a city in each of the From and To drop menus.
		flf = elec('#flightFrom')
		# Because it's a fancy custom select, can't just assign a value normally.
		jeva('$(arguments[0]).val(arguments[1]).change();', flf,
			 random.choice(flf.find_elements_by_css_selector(\
				 'option:not([disabled]):not([value="0"])')).get_attribute('value'))
		# Have to do them separately, as the To menu is not initially populated.
		verf('#flightTo option:not([value="0"])')
		flt = elec('#flightTo')
		jeva('$(arguments[0]).val(arguments[1]).change();', flt,
			 random.choice(flt.find_elements_by_css_selector(
				 'option:not([disabled]):not([value="0"])')).get_attribute('value'))
		# The selected cities' Pins appear on the map,
		#   connected by a flight path, traversed by a plane icon.
		self.assertEqual(len(elecs('.bulb.FlyingTimes')), 2)
		# The flying Times panel shows the approximate flight time and distance.
		verf('.flight-time')
		verf('.flight-distance')

	def test_Contact_Us(self) -> None:
		"""Checks the Contact Us page."""
		self.homepage()
		# Navigate to About > Contact Us.
		point(elec('#nav-main-panel-1'))
		elec('a[href*="contact-us.html"]').click()
		# Click the Contact Us link, Default email client should open, with the To field populated
		#   with the relevant contact. But can't actually test that. The mailto: should suffice.
		verf('a[href^="mailto:"]')

	def test_Registration(self) -> None:
		"""Checks the Registration process. Slight use of witchcraft."""
		self.homepage()
		# Navigate to the Registration Page
		elec('#loginCompButton a[href*="registration-form.html"]').click()
		# Random letters to make a unique username.
		raid = ''.join([chr(random.randrange(65, 91)) for i in range(4)])
		# The Country Code
		lcod = self.locale.split('-')[1]
		# Username stuff, add the Environment prefix to identify and relocate the user.
		env = self.base_url.split('/')[2].split('.')[0][0:3]
		# Different zip codes in different countries.
		zipc = dict([('gb', 'A12BC'), ('us', '12345'), ('ca', '12345'), ('my', '12345'),
					 ('id', '12345'), ('it', '12345'), ('fr', '12345')]).get(lcod, '123456')
		# Fill out the Registration Form with dummy information.
		# Ensure the Name fields are/contain TEST.
		elec('[name="lname"]').send_keys('TEST')
		elec('[name="fname"]').send_keys('TEST ' + lcod + env)
		elec('#birthday-day').send_keys('12')
		elec('#birthday-month').send_keys('12')
		elec('#birthday-year').send_keys('1212')
		elec('[name="companyname"]').send_keys('TEST')
		elec('[name="jobtitle"]').send_keys('TEST')
		Select(elec('[name="busprofile"]')).select_by_value('1')
		elec('[name="address1"]').send_keys('TEST')
		elec('[name="town"]').send_keys('TEST')
		elec('[name="zip"]').send_keys(zipc)
		Select(elec('#country_id')).select_by_value(lcod.upper())
		# Wait for the Country selection to load the State/Lang info.
		lan = elec('[name="language"] :not([value=""])')
		Select(elec('#language_id')).select_by_value(lan.get_attribute('value'))
		Select(elec('#state_list')).select_by_value(
			elec('#state_list :not([value=""])').get_attribute('value'))
		elec("[name='web']").send_keys("www.TEST.com")
		elec('[name="mobile"]').send_keys('TEST')
		# Use an overloaded email.
		elec('#email').send_keys(self.email.replace('@', '+' + raid + '@'))
		elec('#verifyemail').send_keys(self.email.replace('@', '+' + raid + '@'))
		elec('#howmany').send_keys("1")
		elec('#how-many-times').send_keys("1")
		elec('#number-of-bookings').send_keys("1")
		for tra in elecs("[name='travelstandard']"): tra.click()
		for cus in elecs("[name='custexp']"): cus.click()
		elec("[name='username']").send_keys(lcod + env + raid)
		elec('#pwd').send_keys(self.passw)
		elec("[name='pwd1']").send_keys(self.passw)
		elec('#agreement').click()
		# Here, try something quite possibly illegal.
		def h()-> int: return(round(time.time() * 1000 )) // (60 * 1000)
		def ha(bits: bytes)-> str: return hashlib.md5(bits + str(h()).encode()).hexdigest()[1:6]
		# It's time sensitive, so refresh the captcha immediately beforehand.
		elec('fieldset:nth-child(7) > div:nth-child(2) a').click()
		# It does have an #ID, but it's wierd and breaks the selector function. So use this.
		elec('[name="captcha"]').send_keys(
			ha(elec('#cq_captchakey').get_attribute('value').encode()))
		# Click the Create Account button.
		elec("#register-submit").click()
		# Popup should appear confirming account creation.
		verf('#fancybox-thanks')
		# Email should be sent confirming this.
		# In the Registration Confirmation email, click the Activate Account link.
		# Should open the Registration Acknowledgement page, confirming the account is set up.

	def login(self):
		self.homepage()
		# In the header, click the Sign In link.
		elec('.link-signin-text').click()
		# The Sign In panel should appear.
		# verf('#fancybox-login-form')
		# Enter the username and password of the User.
		elec('#j_username').send_keys(self.usern)
		elec('[name="j_password"]').send_keys(self.passw)
		# Click the Sign In button.
		elec('#usersignin').click()
		self.driver.find_element_by_id('link-logout')

	def test_Login(self):
		# Log in.
		self.login()
		# Should proceed to the Secure welcome page.
		verf('.hero-user-name')
		self.assertIn(self.base_url + self.locale + '/secure.html', self.driver.current_url)
		# Check the Nav Menu
		# The Sales section should now have the My Sales Tools link
		elec('#nav-main-panel-2').click()
		verf('#nav-main-panel-2 a[href*="my-sales-tools.html"]')
		# The Training Section should now have the Training Summary link.
		# The Training section should now have the Webinars link.
		elec('#nav-main-panel-3').click()
		verf('#nav-main-panel-3 a[href*="webinars.html"]')
		verf('#nav-main-panel-3 a[href*="training-summary.html"]')
		# The News & Updates section should have the Latest News Link
		# The News section should now  have the Product Updates link.
		elec('#nav-main-panel-4').click()
		verf('#nav-main-panel-4 a[href*="latest-news.html"]')
		verf('#nav-main-panel-4 a[href*="product-videos.html"]')
		# The Club section should not be present.
		self.assertFalse(nelec('#nav-main-panel-5'))

	def test_Forgotten_Username(self):
		self.homepage()
		# Click the Sign In link
		elec('.link-signin-text').click()
		# In the Sign In panel, click the Forgotten Username link.
		elec('a[href*="forgotten-username.html"]').click()
		# Enter the user's email address into the Forgot Username form.
		elec('#forgotemail').send_keys(self.email)
		# Click the Submit button.
		elec('#forgotUser-submit').click()
		# A panel should appear confirming submission.
		verf('.fancybox-skin')
		# An email should be received at the given address containing the Username.

	def test_Forgotten_Password(self):
		self.homepage()
		# Click the Sign In link
		elec('.link-signin-text').click()
		# In the Sign In panel, click the Forgotten Password link.
		elec('a[href*="forgotten-password.html"]').click()
		# Enter the user's email address into the Forgot Password form.
		elec('#forgotemail').send_keys(self.email)
		# Click the Submit button.
		elec('#forgotUser-submit').click()
		# A panel should appear confirming submission.
		verf('.fancybox-skin')
		# An email should be received at the given address containing the Username and new Password
		# Read that email and sign in with the new password.

	def test_Change_Password(self):
		def double():
			self.login()
			# In the Nav Menu, click the My Profile link.
			elec('#link-profile').click()
			# Click the Change Password button, below the Profile Data fields.
			elec('a[href*="change.html"]').click()
			# Fill out the Change Password Form with the Current Password, and a New Password.
			elec('input[name="current"]').send_keys(self.passw)
			elec('input[name="newpwd"]').send_keys(self.passw[::-1])
			elec('input[name="confirmnew"]').send_keys(self.passw[::-1])
			# Click the Submit button.
			elec('#changepwd-submit').click()
			# A panel should appear confirming the password change.
			verf('.fancybox-skin')
			# The page should redirect back to the Profile page.
			verf('#profile-form')
			# Click the Sign Out link in the header.
			elec('#link-logout').click()

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
			inp = elecs('.flipper')
			random.shuffle(inp)
			for fli in inp[0:num]:
				scrl(fli)
				fli.click()
				# The Panels should unfold, showing a description, More Info link, and heart button.
				# They aren't too well labelled though, so be sure to actually watch the playback.
				opa = [x for x in elecs('.mosaic-item-detail-container.active')
					   if x.is_displayed()][0]
				fop = blipper(opa.find_element_by_css_selector)
				self.assertTrue(fop('.l-padding-tb-30-lr-15 p').is_displayed())
				self.assertTrue(fop('a:not(.btn-bubble):not([href="#"])').is_displayed())
				# Click on the Heart buttons of those mosaics.
				fop('.btn-bubble').click()
				# The Heart Icon in the header should pulse and have a number incremented.
				self.assertEqual(mtc + 1, int(elec('.my-trip-count').text))
				mtc += 1
				mtl.add(fop('.line-through-container-biline').text)

		# Pre-condition: Should be signed in.
		self.login()
		# Navigate to the About page.
		elec('#nav-main-panel-1').click()
		elec('#nav-main-panel-1 a[href*="about.html"]').click()
		mtc = int(elec('.my-trip-count').text) or 0
		# Add some of the mosaics to Sales Tools
		mosaicad(3)
		# Navigate to Sales Resources > Australian Events.
		elec('#nav-main-panel-2').click()
		elec('#nav-main-panel-2 a[href*="events.html"]').click()
		# Click the Add To Sales Tools buttons of some of the Event Mosaics.
		mosaicad(6)
		# Navigate to Sales Resources > Fact Sheets.
		elec('#nav-main-panel-2').click()
		elec('#nav-main-panel-2 a[href*="fact-sheets-overview.html"]').click()
		# Click the Add To Sales Tools buttons on a few of the results.
		for b in elecs('a.btn-bubble'):
			scrl(b)
			b.click()
			self.assertEqual(mtc + 1, int(elec('.my-trip-count').text))
			mtc += 1
			# element.parent does not, in fact, return the parent element.
			mtl.add(blipper(b.find_element_by_xpath('../..').find_element_by_css_selector)\
					('.line-through-container').text)
		# Click the Heart Icon in the header.
		elec('.favourite-summary').click()
		# The My Sales Tools page should be displayed.
		verf('.dreamTrip')
		# The My Sales Tools page should have an entry for each of the pages added previously.
		mts = [x.text for x in elecs('.search-results-title')]
		for l in mtl:
			self.assertIn(l, mts)
		# Entries should have an X button, a Title, a Description, and a More Info link.
		for ls in elecs('.search-result-row-spacing'):
			fls = blipper(ls.find_element_by_css_selector)
			self.assertTrue(fls('.icon-close').is_displayed())
			self.assertTrue(fls('.search-results-title').is_displayed())
			self.assertTrue(fls('.mloverflow-text').is_displayed())
			self.assertTrue(fls('p > a').is_displayed())
		# Click several of the listed items' X buttons.
		for ls in elecs('.search-result-row-spacing'):
			blipper(ls.find_element_by_css_selector)('.icon-close').click()
		# The entries should be removed from the list.
		self.assertFalse(nelec('.search-result-row-spacing'))

	def test_My_Profile(self):
		# Pre-condition: Should be signed in.
		self.login()
		# Navigate to the Profile page.
		elec('#link-profile').click()
		# Modify the values of several of the fields, but leave TEST in the names.
		wor = elec('html').get_attribute('class').split()
		def wos():
			return [random.choice(wor) for x in range(5)]
		bio = ' '.join(wos())
		lno = ' TEST '.join(wos())
		spc = random.choice(elecs('[name="state"] option:not([value=""])')).get_attribute('value')
		obi = elec('[name="bio"]')
		obi.clear()
		obi.send_keys(bio)
		oln = elec('[name="lname"]')
		oln.clear()
		oln.send_keys(lno)
		# Again with this.
		csp = elec('[name="state"]')
		jeva('$(arguments[0]).val(arguments[1]).change();', csp, spc)
		# Click the Save Changes button.
		elec('#updateProfileSubmit').click()
		# A panel confirming changes saved should appear.
		verf('.fancybox-skin')
		# Refresh the page.
		self.driver.refresh()
		# The changed field values should remain.
		self.assertEqual(elec('[name="bio"]').text, bio)
		self.assertEqual(elec('[name="state"]').get_attribute('value'), spc)
		self.assertEqual(elec('[name="lname"]').get_attribute('value'), lno)
		self.assertIn(lno, elec('.link-signin-text').text)

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
		elec('#nav-main-panel-3').click()
		elec('a[href*="training-summary.html"]').click()
		# Change the value of the Optional Modules Filter Form.
		olm = '__'.join([x.text for x in elecs('.line-through-container-biline')])
		# A Special Select.
		jeva('$(arguments[0]).val(arguments[1]).change();',
			 elec('[name="Optional"]'), 'TrainingModule:Optional/Niche')
		# Click Refresh Results.
		elec('#btn-id').click()
		time.sleep(showa)
		# The Optional Modules should be filtered.
		nlm = '__'.join([x.text for x in elecs('.line-through-container-biline')])
		self.assertNotEqual(olm, nlm)
		# Click the View More Modules button.
		omc = len(elecs('.line-through-container-biline'))
		elec('.load-more').click()
		time.sleep(showa)
		# Three more modules should be displayed, up to the total amount available.
		nmc = len(elecs('.line-through-container-biline'))
		self.assertEqual(omc + 3, nmc)
		omc = nmc
		elec('.load-more').click()
		time.sleep(showa)
		nmc = len(elecs('.line-through-container-biline'))
		self.assertEqual(omc + 1, nmc)
		omc = nmc
		elec('.load-more').click()
		time.sleep(showa)
		nmc = len(elecs('.line-through-container-biline'))
		self.assertEqual(omc, nmc)
		# Unstarted Modules should have a Let's Start button, and an (X) Incomplete label.
		blipper(elec('a[data-ta-data-layer*="trainingModuleFilterRefreshStart-ASP"]')\
			.find_element_by_xpath('../..').find_element_by_css_selector)\
			('.search-favourite img[src*="icon-incomplete.png"]')
		# Started-Not-Finished Modules should have an In Progress button and the Incomplete label.
		blipper(elec('a[data-ta-data-layer*="trainingModuleFilterRefreshResume-ASP"]')\
			.find_element_by_xpath('../..').find_element_by_css_selector)\
			('.search-favourite img[src*="icon-incomplete.png"]')
		# Completed Modules should have a Complete button and a (v/) Complete label.
		blipper(elec('a[data-ta-data-layer=""]').find_element_by_xpath('../..')\
			.find_element_by_css_selector)('.search-favourite img[src*="icon-complete.png"]')

	def test_Aussie_Specialist_Club(self):
		# Pre-condition: Logged in as a Qualified User.
		self.login()
		# Open the Aussie Specialist Club section in the Nav menu
		elec('#nav-main-panel-5').click()
		# Should now be populated with the full set of links:
		# Aussie Specialist Club (Landing Page), Travel Club, Aussie Specialist Photos
		# Download Qualification Badge, Aussie Store (May not be available in all locales)
		verf('#nav-main-panel-5 a[href*="aussie-specialist-club.html"]')
		verf('#nav-main-panel-5 a[href*="aussie-specialist-club/travel-club.html"]')
		verf('#nav-main-panel-5 a[href*="aussie-specialist-club/famils.html"]')
		verf('#nav-main-panel-5 a[href*="aussie-specialist-club/aussie-specialist-photos.html"]')
		verf('#nav-main-panel-5 a[href*="aussie-specialist-club/asp-logo.html"]')
		verf('#nav-main-panel-5 a[href*="aussie-specialist-club/aussie-store.html"]')

	def test_Travel_Club(self):
		# Pre-condition: Logged in as a Qualified User.
		self.login()
		# Navigate to ASC > Travel Club
		elec('#nav-main-panel-5').click()
		elec('#nav-main-panel-5 a[href*="aussie-specialist-club/travel-club.html"]').click()
		# Search for results, changing the terms if none.
		self.search_for_results()
		# Look at the search results.
		self.look_at_search_results()

	def test_Famils(self):
		# pre-condition: Logged in as a Qualified User.
		self.login()
		# Navigate to ASC > Famils
		elec('#nav-main-panel-5').click()
		elec('#nav-main-panel-5 a[href*="aussie-specialist-club/famils.html"]').click()
		# Maybe not available in all locales?
		# Should Display Famils page content.
		for fam in elecs('.type-body'):
			self.assertTrue(fam.is_displayed())

	def test_Aussie_Specialist_Photos(self):
		# pre-condition: Logged in as a Qualified User.
		self.login()
		# Navigate to ASC > AS Photos
		elec('#nav-main-panel-5').click()
		elec('#nav-main-panel-5 a[href*="aussie-specialist-photos.html"]').click()
		# Should display Instagram Image Tiles, with links and descriptions
		for pic in random.sample(elecs('.mosaic-item .flipper'), 10):
			def picl(el, sel):
				# In case the virtual mouse flips into the image
				self.assertTrue(blipper(el.find_element_by_css_selector)(sel).is_enabled())
			picl(pic, 'img[src*="image.adapt"]')
			pic.click()
			pio = [x for x in elecs('.mosaic-item-detail-container.active') if x.is_displayed()][0]
			picl(pio, 'p')
			picl(pio, 'a[href="http://www.instagram.com/australia"]')
			scrl(pic)
			pic.click()

	def test_Download_Qualification_Badge(self):
		# Pre-condition: Logged in as a Qualified User.
		self.login()
		# Navigate to ASC > Download Qualification Badge
		elec('#nav-main-panel-5').click()
		elec('#nav-main-panel-5 a[href*="aussie-specialist-club/asp-logo.html"]').click()
		# Click the Download Qualification Badge link.
		elec('a[href*="asp-badge.png"]').click()
		# Badge image should be downloaded/opened in a new tab.
		self.driver.switch_to_window(self.driver.window_handles[1])
		verf('img[src*="asp-badge.png"]')

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
		elec('.fancybox-close').click()
		elec('#myCartIcon').click()
		# Click the Place Order button
		elec('.store-order-box-right a input').click()
		# Should redirect to the Order Confirmation page
		verf('.orderconfirmation')
		self.assertIn('confirmation.html', self.driver.current_url)
		# Confirmation Page should have notices of Order Placed,
		verf('.store-order-confirmed-text')
		# Should Receive Email (with the user's email address),
		verf('.confirmation-page p:nth-child(2)')
		# and Contact Us (which links to the Contact Us page).
		verf('.confirmation-page p:nth-child(3) a[href*="about/contact-us.html"]')

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
			elec(cal).click()
			# Choose a few of the Products present, and for each of them {
			prs = [x.get_attribute('href').replace(self.base_url, '')
				   for x in elecs('.store-products-item')]
			kay = min([len(prs), max([len(prs)//3, 5])])
			for pr in random.sample(prs, kay):
				# Click on the Product Image
				pri = elec('a[href="' + pr + '"]')
				prn = pri.find_element_by_css_selector('.store-products-item-title').text.casefold()
				pri.click()
				# Should link to the Product's Page
				self.assertEqual(prn, elec('.home-hero-title').text.casefold())
				# Product Page should have a unique Code, which also should not be N/A or null.
				self.assertNotIn('N/A', elec('.product-code').text)
				self.assertNotIn('null', elec('.product-code').text)
				# Select a Quantity.
				qua = elec('[name="product-quantity"]')
				qua.send_keys(qua.find_elements_by_tag_name('option')[-1].get_attribute('value'))
				# Click the Add To Cart button.
				elec('#cart').click()
				# However, If The Cart Is Full: (Once 10-12 or so Products have been added)
				time.sleep(showa)
				if nelec('#fancybox-cookieoverflow'):
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
				verf('.store-my-cart')
				self.assertIn('cart.html', self.driver.current_url)
				# Cart page should show a list of all of the products added thus far.
				self.assertEqual(prl, {x.text.casefold() for x in elecs('.cell-title')})
				# (do not do for all) Click the X beside one of the products.
				if random.random() < 0.2:
					rei = random.randint(0, len(prl)-1)
					rem = elecs('.cell-title')[rei].text.casefold()
					reb = elecs('.product-remove')[rei]
					scrl(reb)
					reb.click()
					prl.remove(rem)
					pco -= 1
					# That product should be removed from the Cart.
					self.assertEqual(prl, {x.text.casefold() for x in elecs('.cell-title')})
				else: # If this one was removed, it's not going to be overbooked.
					# Go back to the Product Page,
					self.driver.back()
					time.sleep(showa)
					# and attempt to add more of it to the Cart, beyond the Quantity permitted.
					qua = elec('[name="product-quantity"]')
					qua.send_keys(qua.find_elements_by_tag_name('option')[-1]\
								  .get_attribute('value'))
					elec('#cart').click()
					# A panel should pop up, notifying that Maximum Quantity was exceeded.
					verf('#fancybox-maxerror')
					elec('.fancybox-close').click()
				# Back to Category Page, try the next one.
				elec(cal).click()
			return False

		# Pre-condition: Logged in as a Qualified User.
		self.login()
		# Preamblic mess.
		elec('#link-profile').click()
		def adn(s):
			return s + ', ' if s else ''
		# Some sort of conditional prepension.
		phone = elec('[name="countrycode"]').get_attribute('value') +\
				elec('[name="phone"]').get_attribute('value')
		phone = phone + '\n' if phone else phone
		contactBlob = (elec('[name="fname"]').get_attribute('value') + ' ' +
					   elec('[name="lname"]').get_attribute('value') + '\n' +
					   adn(elec('[name="address1"]').get_attribute('value')) +
					   adn(elec('[name="address2"]').get_attribute('value')) +
					   # Trim one extra space from here, apparently.
					   adn(elec('[name="address3"]').get_attribute('value'))[0:-1] + '\n' +
					   elec('[name="town"]').get_attribute('value') + '\n' +
					   elec('[name="state"] option[value="' +
					   # And add one extra one here.
					   elec('[name="state"]').get_attribute('value') + '"]').text + ',  ' +
			elec('[name="zip"]').get_attribute('value') + '\n' +
			elec('[name="country"]').get_attribute('value') + phone)
		# Navigate to ASC > Aussie Store
		elec('#nav-main-panel-5').click()
		elec('#nav-main-panel-5 a[href*="aussie-specialist-club/aussie-store.html"]').click()
		# Click the Cart button
		elec('#myCartIcon').click()
		# Should get a popup message about the Cart being Empty.
		verf('.fancybox-skin')
		elec('.fancybox-close').click()
		# Click on one of the Product Images
		pri = random.choice(elecs('.store-products-item'))
		prn = pri.find_element_by_xpath('..')\
			  .find_element_by_css_selector('.store-products-item-title').text.casefold()
		pri.click()
		# Should redirect to that Product's page
		self.assertEqual(prn, elec('.home-hero-title').text.casefold())
		# Click the Add To Cart button
		elec('#cart').click()
		# Should go to the Cart Page
		verf('.store-my-cart')
		# The User's Name and Contact Details should be displayed with the same values
		# as displayed in the Profile. Any Blank Profile fields should not show up as 'null'.
		blobContact = elec('.store-order-box-left > p:nth-child(2)').text
		self.assertTrue(re.match(blobContact.replace(' ', r'\s+').replace('\n', '\\s+'),
								 contactBlob))
		self.assertNotIn('null', blobContact)
		# Tidy up first
		elec('.product-remove').click()
		time.sleep(showa)
		# For each of the categories, (except All Products), go through it,
		pco = 0
		prl = set()
		cats = [x.get_attribute('href').replace(self.base_url, '') for x in
				elecs('.nav-store-categories-menu li a:not([href*="all-products"])')]
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
		elec('#link-profile').click()
		# The Status Badge area shows the Premier Aussie Specialist Icon.
		verf('#profile-form > div:nth-child(2) a > img[src*="achievements/3.png"]')

if __name__ == '__main__':
	tests = unittest.TestSuite()
	tests.addTests(unittest.makeSuite(REGR))

	runner = TAPTestRunner()
	runner.set_outdir('./')
	runner.set_format('Result of: {method_name} - {short_description}')
	runner.run(tests)
