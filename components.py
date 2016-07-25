"""Implements classes wrapping the behaviour for finding and manipulating web elements."""

import re
import time
import random
import hashlib
from types import MethodType
from typing import Set, List
from selenium.webdriver.remote.webelement import WebElement
import drivery as DR

class WrappedElement:
	"""Superclass for the various helper classes here."""
	# This is a placeholder, don't actually try this.
	element = WebElement(parent=None, id_=None)

	def click(self) -> 'WrappedElement':
		"""Clicks on the element."""
		DR.LAST_LINK = DR.fix_url(self.element.get_attribute('href'))
		self.element.click()
		return self

	def point(self) -> 'WrappedElement':
		"""Moves the mouse cursor over the element."""
		DR.execute_mouse_over(self.element)
		return self

	def is_displayed(self) -> bool:
		"""Again, a bit of a formality. Checks whether the element is displayed"""
		return self.element.is_displayed()

	def __getattr__(self, name):
		"""Basically just to stop pylint from complaining about dynamic attributes."""
		raise AttributeError('No, the {0} attribute does not exist on {1}.'.format(name, type(self)))

class MinorElement(WrappedElement):
	"""Superclass for all the internally used minor elements; with no unique
	properties, initialised with a css selector instead of self-founding."""
	def __init__(self, selector: str, within: WrappedElement) -> None:
		self.element = DR.flashy_find_element(selector, within)

class SplashSelect(WrappedElement):
	"""Represents the Language Selector on the Splash Page."""
	def __init__(self):
		self.element = DR.flashy_find_element('.dropdown-select-language1')

	def get_values(self) -> Set[str]:
		"""Gets a set containing the URLs of all the Language Options."""
		return {DR.fix_url(x.get_attribute('value')) \
			for x in DR.quietly_find_elements('option:not([value="#"])', self.element)}

	def choose_locale(self) -> None:
		"""Selects the Language Option representing the current locale."""
		option = DR.quietly_find_element('option[value*="{}"]'.format(DR.LOCALE), self.element)
		DR.LAST_LINK = option.get_attribute('value')
		option.click()

class WelcomeVideo(WrappedElement):
	"""Represents the main Video on the home page."""
	def __init__(self):
		self.element = DR.flashy_find_element('.hero')

	def play(self) -> None:
		"""Clicks the video's Play button."""
		DR.flashy_find_element('.cts-icon-play', self.element).click()
		if DR.CN_MODE:	# In China, you have to click it twice.
			DR.flashy_find_element('.vjs-poster', self.element).click()

	def is_playing(self) -> bool:
		"""Checks whether the video is playing."""
		return DR.quietly_find_element('.vjs-play-control', self.element).is_displayed()

class BodyLoginButton(WrappedElement):
	"""Represents the Sign In button that appears in a page's body content when signed out."""
	def __init__(self):
		self.element = DR.flashy_find_element('#loginCompButton > div > a.btn-primary.fancybox')

class BodyRegisterButton(WrappedElement):
	"""Represents the Join The Program button that appears in a page's body content when signed out."""
	def __init__(self):
		self.element = DR.flashy_find_element('#loginCompButton > div > a:nth-child(2)')

class WhatYouCanSeeMosaic(WrappedElement):
	"""Represents the What You Can See Mosaic, however many tiles may appear."""
	def __init__(self):
		self.element = DR.flashy_find_element('div.whatYouCanSee div.mosaic')
		self.tiles = DR.quietly_find_elements('.flipper')

	def tile_count(self) -> int:
		"""Returns the number of tiles in the mosaic."""
		return len(self.tiles)

	class MosaicTile(WrappedElement):
		"""Represents a single Mosaic Tile, including its internal elements.
		Don't instantiate this from the test script directly, it needs a WebElement"""
		def __init__(self, element: WebElement):
			self.element = DR.blip_element(element)
			self.contentpane = None

		def open(self) -> None:
			"""Clicks on the mosaic tile, opening it.
			Panel contents is a bit of a mess though, have to account for responsive design."""
			DR.blip_element(self.element)
			DR.execute_script('scrollBy(0,-400);return 0')	# That header does insist on being in the way.
			self.element.click()
			self.contentpane = [x for x in DR.flashy_find_elements(\
				'.mosaic-item-detail-container.active') if x.is_displayed()][0]

		def get_title(self) -> str:
			"""Returns the title text of a tile's content pane. Has to be open first."""
			return DR.flashy_find_element('.line-through-container-biline', self.contentpane).text

		def get_description(self) -> MinorElement:
			"""Returns the description text in a tile's pane. Has to be open."""
			return MinorElement('.l-padding-tb-30-lr-15 p', self.contentpane)

		def get_link(self) -> MinorElement:
			"""Returns the More Info link from a tiles pane. Has to be open."""
			return MinorElement('a:not(.btn-bubble):not([href="#"])', self.contentpane)

		def add_to_favourites(self) -> None:
			"""Clicks the Heart button in the tiles content. Has to be open first."""
			DR.flashy_find_element('.btn-bubble', self.contentpane).click()

	def random_selection(self, num: int) -> List[WrappedElement]: # pylint: disable-msg=E1126
		"""Given a number, gets that many randomly selected tiles from the mosaic."""
		return [self.MosaicTile(tile) for tile in random.sample(self.tiles, num)]

def attach_link(section: WrappedElement, name: str, selector: str='[href*="{}.html"]') -> None:
	"""A function that attaches an attribute that can be called to create a simple link.
	The 'name' argument should be the bit that .formats into the selector"""
	def link_maker():
		"""A function that can be called to create a simple link"""
		return MinorElement(selector.format(name), section.element)
	link_maker.__doc__ = 'Creates the {0}/{1} link representation'\
		.format(type(section), name.replace('-', ' ').replace('.', ' ').title())
	section.__setattr__(name.replace('-', '_').replace('.', '_'), link_maker)

class NavSection(WrappedElement):
	"""Methods common to the five Nav Menu sections."""
	def open(self) -> WrappedElement:
		"""Opens the menu, whether that be by clicking or by pointing."""
		self.point()
		if self.element.get_attribute('class').find('is-open') == -1:
			self.click()
		return self

class About(NavSection):
	"""Represents the About menu in the main nav menu."""
	def __init__(self):
		self.element = DR.flashy_find_element('#nav-main-panel-1')
		attach_link(self, 'about')
		attach_link(self, 'benefits')
		attach_link(self, 'how-to-use-the-site')
		attach_link(self, 'program-faq')
		attach_link(self, 'contact-us')

class SalesResources(NavSection):
	"""Represents the Sales Resources menu in the main nav menu."""
	def __init__(self):
		self.element = DR.flashy_find_element('#nav-main-panel-2')
		attach_link(self, 'sales-resources')
		attach_link(self, 'my-sales-tools')
		attach_link(self, 'interactive-map')
		attach_link(self, 'itineraries-search-and-feature')
		attach_link(self, 'fact-sheets-overview')
		attach_link(self, 'events')
		attach_link(self, 'useful-sites')
		attach_link(self, 'destination-faq')
		attach_link(self, 'image-and-video-galleries')

class Training(NavSection):
	"""Represents the Training menu in the main nav menu."""
	def __init__(self):
		self.element = DR.flashy_find_element('#nav-main-panel-3')
		attach_link(self, 'training')
		attach_link(self, 'training-summary')
		attach_link(self, 'webinars')

class NewsAndProducts(NavSection):
	"""Represents the News And Products menu in the main nav menu."""
	def __init__(self):
		self.element = DR.flashy_find_element('#nav-main-panel-4')
		attach_link(self, 'news-and-product-updates')
		attach_link(self, 'latest-news')
		attach_link(self, 'product-videos')

class AussieSpecialistClub(NavSection):
	"""Represents the Aussie Specialist Club menu in the main nav menu."""
	def __init__(self):
		self.element = DR.flashy_find_element('#nav-main-panel-5')
		attach_link(self, 'aussie-specialist-club')
		attach_link(self, 'travel-club')
		attach_link(self, 'famils')
		attach_link(self, 'aussie-specialist-photos')
		attach_link(self, 'asp-logo')
		attach_link(self, 'aussie-store')

	@staticmethod
	def not_present() -> bool:
		"""Checks that the Aussie Specialist Club menu is not present.
		As such, does not attempt to locate it, and is a static method."""
		return not DR.check_visible_quick('#nav-main-panel-5')

class NavMenu(WrappedElement):
	"""In case you need to refer to all of the nav menu elements collectively."""
	about = About
	sales_resources = SalesResources
	training = Training
	news_and_products = NewsAndProducts
	aussie_specialist_club = AussieSpecialistClub
	def __init__(self):
		self.element = DR.flashy_find_element('.main-nav-wrap')
		attach_link(self, 'profile', selector='#link-{}')
		attach_link(self, 'logout', selector='#link-{}')

	def get_all_links(self) -> Set[str]:
		"""Gets a set containing the href of each link in the nav menu.
		The Five/Four section panels, that is, not the Icons, or the Sign In thing."""
		return {x.get_attribute('href') for x in DR.flashy_find_elements(\
			'#nav-bar-top .nav-bar-left a:not([href^="#"])', self.element)}

	def user_names(self) -> str:
		"""Gets the text displayed in the corner that shows the user names.
		Totally unformatted, so just use the in() function rather than parsing."""
		return DR.flashy_find_element('.link-signin-text', self.element).text

class Footer(WrappedElement):
	"""Represents the global Footer."""
	def __init__(self):
		self.element = DR.flashy_find_element('#main-footer')
		attach_link(self, 'splash')
		attach_link(self, 'facebook', selector='[href*="www.{}.com"]')
		attach_link(self, 'plus.google', selector='[href*="{}.com"]')
		attach_link(self, 'youtube', selector='[href*="www.{}.com"]')
		attach_link(self, 'twitter', selector='[href*="{}.com"]')
		attach_link(self, 'instagram', selector='[href*="{}.com"]')
		attach_link(self, 'wechat', selector='[href*="#qr_image"]')
		attach_link(self, 'sitemap')
		attach_link(self, 'privacy-policy')
		attach_link(self, 'terms-and-conditions')
		attach_link(self, 'terms-of-use')
		attach_link(self, 'contact-us')
		if DR.CN_MODE:
			attach_link(self, 'australia', selector='[href*="www.{}.cn"]')
			attach_link(self, 'businessevents.australia', selector='[href*="{}.cn"]')
		else:
			attach_link(self, 'australia', selector='[href*="www.{}.com"]')
			attach_link(self, 'tourism.australia', selector='[href*="www.{}.com"]')
			attach_link(self, 'businessevents.australia', selector='[href*="{}.com"]')

class Sitemap(WrappedElement):
	"""Represents the Sitemap link cloud."""
	def __init__(self):
		self.element = DR.flashy_find_element('.sitemap')
		attach_link(self, 'change')
		attach_link(self, 'newsletter-unsubscribe')
		attach_link(self, 'coming-soon')

	def get_all_links(self) -> Set[str]:
		"""Gets a set containing the href of each link in the Sitemap link section."""
		return {x.get_attribute('href') for x in DR.flashy_find_elements('a', self.element)}

class FilteredSearch(WrappedElement):
	"""Represents the Itinerary or Fact Sheet Search Components."""
	def __init__(self, fact_sheet_mode: bool=False) -> None:
		self.element = DR.flashy_find_element('.filteredSearch')
		self.fact_sheet_mode = fact_sheet_mode
		# Hold up, have to wait for the initial results to come in first,
		# they'll interrupt if they appear halfway through something else.
		DR.quietly_find_element('.mosaic-item')

	class SearchResult(WrappedElement):
		"""Represents a Result of a Filtered Search."""
		def __init__(self, which: WebElement):
			self.element = which

		def get_title(self) -> str:
			"""Gets the page Title/Name of the result."""
			return DR.flashy_find_element('.line-through-container', self.element).text

		def view_more_information(self) -> None:
			"""Navigates to the result's main page, clicks the View More Info link."""
			link = DR.flashy_find_element('.search-results-copy-container a', self.element)
			DR.LAST_LINK = DR.fix_url(link.get_attribute('href'))
			link.click()
			DR.wait_for_page()

		def add_to_favourites(self) -> None:
			"""Clicks the result's Heart Icon: Add To My Sales Tool Kit."""
			DR.flashy_find_element('a.btn-bubble', self.element).click()

		def download_pdf(self) -> None:
			"""Clicks the Download PDF link."""
			link = DR.flashy_find_element('a.download-pdf', self.element)
			link.click()

		class SearchResultPage(WrappedElement):
			"""Represents the full More Info page pointed to by a Filtered Search's result."""
			def __init__(self):
				self.element = DR.flashy_find_element('.home-hero-title')

			def get_title(self) -> None:
				"""Returns the title of the page the result was pointing to."""
				return self.element.text.replace('\n', ' ')

	def load_more(self) -> None:
		"""Clicks the Search Component's Load More button."""
		DR.flashy_find_element('.load-more', self.element).click()
		DR.wait_until_gone('.filteredSearch .preload-image-wrapper img')

	def random_search(self) -> None:
		"""Picks random values in each of the search category droplists,
		then clicks the Refresh Results button. Repeats this until results are found."""
		while True:
			for select in DR.quietly_find_elements('select', self.element):
				DR.blip_element(select)
				random.choice(DR.quietly_find_elements('option', select)).click()
			DR.flashy_find_element('#btn-id', self.element).click()
			DR.wait_until_gone('.filteredSearch .preload-image-wrapper img')
			# Check if any results are returned, and, if in Fact Sheet Mode, if any PDF links are present.
			if DR.check_visible_quick('.mosaic-item', self.element):
				# If not in Fact mode, don't need pdf, so done. If in Fact, do need pdf.
				if not self.fact_sheet_mode or (DR.check_visible_quick(\
					'.mosaic-item-detail-container .search-favourite a[href$="pdf"]', self.element)):
					break

	def count_results(self) -> int:
		"""Returns the number of search results currently displayed."""
		return len(DR.flashy_find_elements('.mosaic-item', self.element))

	def read_results_counter(self) -> (int, int) or None:
		"""Returns the number of results the 'Showing X-Y of Z results' thing says there are:
		A tuple as (shown, total), or a None if it's not shown, such as with Travel Club"""
		counter = DR.flashy_find_element('.search-result-count-copy', self.element).text
		counter = [int(x) for x in re.findall(r'\d+', counter)]
		if counter == []:
			 return None
		# Different languages can show the numbers in different orders.
		counter.sort()
		# The largest number has to be the total results, with the other two being 'this many shown'.
		return (1 + counter[1] - counter[0], counter[2])

	def get_all_results(self) -> List[WrappedElement]: # pylint: disable-msg=E1126
		"""Gets all of the search results."""
		return [self.SearchResult(e) for e in DR.flashy_find_elements('.mosaic-item')]

	def get_random_result(self) -> WrappedElement:
		"""Picks a random one from the search results."""
		result = self.SearchResult(DR.blip_element(\
			random.choice(DR.quietly_find_elements('.mosaic-item'))))
		return result

class PDFPage(WrappedElement):
	"""Represents a PDF file viewed within the browser.
	As a PDF embed is not a web page, this class doesn't do much."""
	def __init__(self):
		self.element = DR.quietly_find_element('embed[type="application/pdf"],.pdfViewer')

class HeaderMapIcon(WrappedElement):
	"""Represents the Icon in the Header linking to the Interactive Map."""
	def __init__(self):
		self.element = DR.flashy_find_element('.link-map a')

class HeaderHeartIcon(WrappedElement):
	"""Represents the Heart Icon in the Header. Complete with favourites count."""
	def __init__(self):
		self.element = DR.flashy_find_element('.favourite-summary')

	def favourites_count(self) -> int:
		"""Returns the number of favourites as indicated by the icon subtitle."""
		anim = DR.quietly_find_element('.icon-heart-animate', self.element)
		DR.wait_until(lambda _: anim.get_attribute('style') == '' or \
			anim.get_attribute('style').find('opacity: 0;') != -1)
		try:
			return int(DR.flashy_find_element('.my-trip-count', self.element).text)
		except ValueError:
			return 0

class InteractiveMap(WrappedElement):
	"""Represents the Interactive Map.
	Note that instantiating this class will also switch WebDriver focus into the map's iframe."""
	def __init__(self):
		DR.switch_to_frame('#interactiveMapId')

	class Controls(WrappedElement):
		"""Represents the menu to the left of the map area."""
		def __init__(self):
			self.element = DR.flashy_find_element('.controls-wrapper')

		def open_menu(self) -> None:
			"""Opens a menu, and waits until it is open, too."""
			DR.blip_element(self.element).click()
			DR.wait_until(lambda _: self.element.get_attribute('class') == 'active')

		def pick_random(self) -> None:
			"""Picks a random entry from the menu."""
			city = random.choice(DR.quietly_find_element('li a', self.element))
			DR.blip_element(city).click()

		class Cities(WrappedElement):
			"""Represents the Cities Menu."""
			def __init__(self):
				self.element = DR.flashy_find_element('#cities')
				self.open_menu = MethodType(InteractiveMap.Controls.open_menu, self)
				self.pick_random = MethodType(InteractiveMap.Controls.pick_random, self)

		class IconicDestinations(WrappedElement):
			"""Represents the Iconic Destinations Menu."""
			def __init__(self):
				self.element = DR.flashy_find_element('#icons')
				self.open_menu = MethodType(InteractiveMap.Controls.open_menu, self)
				self.pick_random = MethodType(InteractiveMap.Controls.pick_random, self)

		class Itineraries(WrappedElement):
			"""Represents the Itineraries Menu."""
			def __init__(self):
				self.element = DR.flashy_find_element('#itinerarytypes')
				self.open_menu = MethodType(InteractiveMap.Controls.open_menu, self)
				self.pick_random = MethodType(InteractiveMap.Controls.pick_random, self)

		class FlyingTimes(WrappedElement):
			"""Represents the Flying Times Menu."""
			def __init__(self):
				self.element = DR.flashy_find_element('#flights')
				self.open_menu = MethodType(InteractiveMap.Controls.open_menu, self)

			def choose_from(self) -> str:
				"""Randomly chooses a city from the From field."""
				select = DR.flashy_find_element('#flightFrom', self.element)
				opt = random.choice(DR.quietly_find_elements('option[id]', select))
				opt.click()
				return opt.text

			def choose_to(self) -> str:
				"""Randomly sets a city to the To field."""
				select = DR.flashy_find_element('#flightTo', self.element)
				opt = random.choice(DR.quietly_find_elements('option[id]', select))
				opt.click()
				return opt.text

			def flight_time(self) -> WrappedElement:
				"""Gets a representation of the Flight Time display."""
				return MinorElement('.flight-time', self.element)

			def flight_distance(self) -> WrappedElement:
				"""Gets a representation of the Flight Distance display."""
				return MinorElement('.flight-distance', self.element)

		class InfoPanel(WrappedElement):
			"""Represents the information panel about a City/Icon/Itinerary."""
			def __init__(self):
				self.element = DR.flashy_find_element('#info-middle')

			def get_title(self) -> str:
				"""Returns the name of the location that the panel describes"""
				return DR.flashy_find_element('#info-title', self.element).text

			def back_to_menu(self) -> None:
				"""Clicks the BACK TO MENU button at the top there, then waits until it finishes spinning"""
				DR.flashy_find_element('#back-to-filter', self.element).click()
				panel = DR.get_parent_element(DR.get_parent_element(DR.quietly_find_element('#map-menu')))
				DR.wait_until(lambda _: panel.get_attribute('style').find('rotateY(0deg)') != -1)

			def find_out_more(self) -> str:
				"""Returns the url of the Find Out More link."""
				return DR.get_parent_element(\
					DR.flashy_find_element('#info-mainLink', self.element)\
					).get_attribute('href')

			def view_highlights(self) -> str:
				"""Returns the url of the VIEW HIGHLIGHTS button."""
				return DR.flashy_find_element('#info-optionalLink', self.element).get_attribute('href')

			def count_photos(self) -> int:
				"""Counts the number of photographs shown for this location."""
				return len(DR.quietly_find_elements('#info-carousel img', self.element))

			def open_photos(self) -> WrappedElement:
				"""Clicks on one of the photos, opening the image carousel."""
				DR.flashy_find_element('#info-carousel img', self.element).click()
				DR.wait_until_present("#carousel-lightbox")
				return InteractiveMap.ImageCarousel()

			def random_itinerary(self) -> str:
				"""Clicks on one of the Itinerary Suggestions links, and returns its title."""
				suges = DR.quietly_find_elements('#suggested-itineraries a', self.element)
				try:
					suge = random.choice(suges)
					sug = suge.text
					suge.click()
					DR.wait_until(lambda _: DR.quietly_find_element('#info-title').text == sug)
					return sug
				except IndexError:	# There can apparently be no suggested itineraries.
					return ''

	class MapArea(WrappedElement):
		"""Just a precaution, preventing searches from overlapping too much?"""
		def __init__(self):
			self.element = DR.flashy_find_element('#map_canvas')

		class MapPins(WrappedElement):
			"""Represents the collection of pins that appear on the map when a menu is opened."""
			def __init__(self):
				self.pins = DR.flashy_find_elements('{} div.bulb:not(.Itineraries)'\
					.format('.MapPushpinBase' if DR.CN_MODE else '.marker'))
				self.element = DR.get_parent_element(DR.get_parent_element(self.pins[0]))

			def pick_random(self) -> str:
				"""Picks a random pin and clicks it. Returns the name of its destination.
				Also manipulates the CSS to bring it to the front, in case it's behind another one."""
				pin = random.choice(self.pins)
				DR.bring_to_front(pin)
				DR.blip_element(pin)
				name = pin.text
				pin.click()
				panel = DR.quietly_find_element('#info-box')
				DR.wait_until(lambda _: panel.is_displayed() and \
					panel.get_attribute('style').find('rotateY(0deg)') != -1)
				return name

			def count(self) -> int:
				"""Returns the number of map pins visible."""
				DR.blip_element(self.pins)
				return len(self.pins)

			def get_names(self) -> List[str]: # pylint: disable-msg=E1126
				"""Returns a list of the labels on all of the pins"""
				DR.blip_element(self.pins)
				return [x.text for x in self.pins]

		class InfoPopup(WrappedElement):
			"""Represents the popup window thing that appears from an Itinerary Step Pin."""
			def __init__(self):
				self.element = DR.flashy_find_element('.gm-style-iw')

	class ImageCarousel(WrappedElement):
		"""Represents the Photo Carousel that pops out from a Location Information panel"""
		def __init__(self):
			self.element = DR.flashy_find_element('#lightbox-inner')

		def current_image_source(self) -> str:
			"""Returns the image source of the image currently shown."""
			return DR.flashy_find_element('#lightbox-inner-image', self.element).get_attribute('src')

		def next(self) -> None:
			"""Clicks the > next button to show the next photo."""
			DR.flashy_find_element('#next', self.element).click()

		def close(self) -> None:
			"""Clicks the X close button to hide the carousel"""
			DR.flashy_find_element('#close-lightbox', self.element).click()
			DR.wait_until_gone('#lightbox-inner')

	class ZoomTools(WrappedElement):
		"""Represents the Zoom In/Zoom Out button set."""
		def __init__(self):
			self.element = DR.flashy_find_element('.zoom-wrapper')

		def zoom_in(self) -> None:
			"""Clicks the Zoom In button."""
			DR.flashy_find_element('#zoomin', self.element).click()
			time.sleep(DR.SHORT_WAIT)

		def zoom_out(self) -> None:
			"""Clicks the Zoom Out button."""
			DR.flashy_find_element('#zoomout', self.element).click()
			time.sleep(DR.SHORT_WAIT)	# Otherwise it tries to click where the pin *was*.

class ContactUs(WrappedElement):
	"""Represents the Contact Us page, which isn't a lot."""
	def __init__(self):
		self.element = DR.flashy_find_element('a[href*="mailto:"]')

class RegistrationForm(WrappedElement): # They aren't instance variables. pylint: disable-msg=R0902
	"""Represents the Registration Form"""
	def __init__(self):
		self.element = DR.flashy_find_element('#registration-form')

	def __getattr__(self, name):
		"""If an unknown GET message is received, see if there's a field with that name."""
		return DR.flashy_find_element('[name*="{}"]'.format(\
			name.replace('_', '-')), self.element).get_attribute('value')

	def __setattr__(self, name, value):
		"""If an unknown SET message is received, see if there's a field with that name."""
		# Really should have seen this coming.
		if name == 'element':
			object.__setattr__(self, name, value)
			return
		elem = DR.flashy_find_element('[name="{}"]'.format(name.replace('_', '-')), self.element)
		elem.clear()
		elem.send_keys(value)

	def plain_text_fields(self, value: str=''):
		"""Sets the value of all of the text fields that are mandatory,
		but which don't need any particular value or format."""
		elements = DR.quietly_find_elements('[type="text"]', self.element)
		for element in elements:
			DR.blip_element(element)
			element.send_keys(value)
	# Deliberately uses the __setattr__, ignore the attribute define warning.
	# pylint: disable-msg=W0201
	def date_of_birth(self, value: str='//') -> None:
		"""Overwrites the Date Of Birth Name field to have the given D/M/Y value. Blank default."""
		value = value.split('/')
		self.birthdayday = value[0]
		self.birthdaymonth = value[1]
		self.birthdayyear = value[2]

	def pick_business_profile(self) -> None:
		"""Picks a random option in the Business Profile list."""
		sel = DR.flashy_find_element('[name="busprofile"]', self.element)
		random.choice(DR.quietly_find_elements('option:not([value=""])', sel)).click()

	def pick_partner(self) -> None:
		"""Picks a random option in the PReferred Travel Partners list."""
		sel = DR.flashy_find_element('[name="affiliationtype"]', self.element)
		random.choice(DR.quietly_find_elements('option:not([value=""])', sel)).click()

	def pick_country(self, value: str='') -> None:
		"""Picks the country with the given abbreviation from the Country list."""
		sel = DR.flashy_find_element('#country_id', self.element)
		DR.quietly_find_element('option[value="{0}"]'.format(value), sel).click()
		# Wait for the Country selection to load the State/Lang info.
		DR.wait_until_present('[name="language"] :not([value=""])')

	def pick_state(self) -> None:
		"""Picks a random option from the State/Province/County field."""
		sel = DR.flashy_find_element('#state_list', self.element)
		random.choice(DR.quietly_find_elements('option:not([value=""])', sel)).click()

	def pick_language(self, lang: str='') -> None:
		"""Picks a language from the Language field. If in Hong Kong, choose carefully."""
		sel = DR.flashy_find_element('#language_id', self.element)
		if lang == 'zh':
			DR.quietly_find_element('option[value="8"])', sel).click()
		else:
			DR.quietly_find_element('option:not([value=""])', sel).click()

	def email_address(self, value: str='') -> None:
		"""Overwrites the Email Address and Verify Email fields to have the given value. Blank default."""
		self.email = value
		# China does not have this email verification.
		if not DR.CN_MODE: self.verifyemail = value

	def how_many_years(self) -> None:
		"""Sets the value of the How Many Years Selling field."""
		sel = DR.flashy_find_element('#howmany', self.element)
		DR.quietly_find_element('option:not([value=""])', sel).click()

	def how_many_times(self) -> None:
		"""Sets the value of the How Many Times Been field."""
		sel = DR.flashy_find_element('#how-many-times', self.element)
		DR.quietly_find_element('option:not([value=""])', sel).click()

	def how_many_bookings(self) -> None:
		"""Sets the value of the How Many Bookings Personally Made field."""
		sel = DR.flashy_find_element('#number-of-bookings', self.element)
		DR.quietly_find_element('option:not([value=""])', sel).click()

	def standard_categories(self) -> None:
		"""Picks a random selection of Categories Of Standard Of Travel"""
		sel = DR.quietly_find_elements('[name=travelstandard]', self.element)
		for box in random.sample(sel, len(sel) // 2):
			DR.blip_element(box).click()

	def experiences(self) -> None:
		"""Picks a random selection of Experiences Asked For"""
		sel = DR.quietly_find_elements('[name=custexp]', self.element)
		for box in random.sample(sel, len(sel) // 2):
			DR.blip_element(box).click()

	def password(self, value: str='') -> None:
		"""Sets the value of the Create A Password and Re-Enter Password fields. Blank default."""
		self.pwd = value
		self.pwd1 = value

	def terms_and_conditions(self) -> None:
		"""Agrees to the Terms And Conditions, without reading them."""
		DR.flashy_find_element('#agreement', self.element).click()

	def decaptcha(self) -> None:
		"""Calculates the value of the 'captcha' code."""
		def get_time() -> int:
			"""Calculates the current time."""
			return (round(time.time() * 1000)) // (60 * 1000)
		def do_it(bits: bytes) -> str:
			"""Calculates the MD5 hex of something, in addition to the current time."""
			return hashlib.md5(bits + str(get_time()).encode()).hexdigest()[1:6]
		# It's time sensitive, so refresh the captcha immediately beforehand.
		DR.flashy_find_element('a[onclick="captchaRefresh()"]', self.element).click()
		self.captcha = do_it(DR.flashy_find_element('#cq_captchakey').get_attribute('value').encode())

	def submit(self) -> None:
		"""Clicks the Create My Account Button, and awaits confirmation."""
		DR.flashy_find_element("#register-submit", self.element).click()
		DR.wait_until_present('#fancybox-thanks')

class SignIn(WrappedElement):
	"""Represents the Sign In panel. Instantiating this class will open said panel."""
	def __init__(self):
		DR.flashy_find_element('.link-signin-text').click()
		self.element = DR.flashy_find_element('.fancybox-wrap')
		attach_link(self, 'forgotten-username')
		attach_link(self, 'forgotten-password')

	def sign_in(self, user: str, passw: str, new_password=False) -> None:
		"""Logs in using the given Username and Password."""
		DR.flashy_find_element('#j_username', self.element).send_keys(user)
		DR.flashy_find_element('[name="j_password"]', self.element).send_keys(passw)
		DR.flashy_find_element('#usersignin', self.element).click()
		DR.LAST_LINK = '/change.html' if new_password else '/secure'
		DR.wait_for_page()

class ForgottenForm(WrappedElement):
	"""Represents the Forgotten Username/Password form. They are the same component."""
	def __init__(self):
		self.element = DR.flashy_find_element('#forgotform')

	def email(self, email: str) -> None:
		"""Enters the given email address into the email address field."""
		DR.flashy_find_element('#forgotemail', self.element).send_keys(email)

	def submit(self) -> None:
		"""Clicks the Submit button and waits for the confirmation message."""
		DR.flashy_find_element('#forgotUser-submit', self.element).click()
		DR.wait_until_present('.fancybox-skin')

class ChangePassword(WrappedElement):
	"""Represents the Change Password form."""
	def __init__(self):
		self.element = DR.flashy_find_element('#changepwdform')

	def current_password(self, password: str) -> None:
		"""Inputs the given password to the Current Password field."""
		DR.flashy_find_element('[name="current"]', self.element).send_keys(password)

	def new_password(self, password: str) -> None:
		"""Inputs the given password to the New and Repeat Password fields."""
		DR.flashy_find_element('#newpwd', self.element).send_keys(password)
		DR.flashy_find_element('[name="confirmnew"]', self.element).send_keys(password)

	def submit(self) -> None:
		"""Clicks the Update Password button, and then waits for the redirect."""
		DR.flashy_find_element('#changepwd-submit', self.element).click()
		DR.wait_until_present('.fancybox-wrap')
		DR.LAST_LINK = 'profile.html'
		DR.wait_for_page()

class MySalesTools(WrappedElement):
	"""Represents the My Sales Tools page."""
	def __init__(self):
		self.element = DR.flashy_find_element('.dreamTrip')

	class SalesTool(WrappedElement):
		"""Represents a single favourite entry."""
		def __init__(self, element):
			self.element = element

		def get_link(self) -> WrappedElement:
			"""Returns the entry's More Info link."""
			return MinorElement('p > a', self.element)

		def get_title(self) -> str:
			"""Returns the title of the entry."""
			return DR.flashy_find_element('.search-results-title', self.element).text

		def get_description(self) -> str:
			"""Returns the Page Summary of the entry."""
			return DR.flashy_find_element('.mloverflow-text', self.element).text

		def close(self) -> None:
			"""Clicks the X button, closing the entry."""
			DR.flashy_find_element('.icon-close', self.element).click()

	def get_favourites(self) -> List[WrappedElement]: # pylint: disable-msg=E1126
		"""Gets all of the saved sales tools entries."""
		return [self.SalesTool(x) for x in \
			DR.flashy_find_elements('.search-result-row-spacing', self.element)]

	def home_search(self) -> WrappedElement:
		"""Gets that Home button Search button pair that appears when the list is empty."""
		return DR.wait_until_present('.dreamtrip-cta')

class Profile(WrappedElement):
	"""Represents the Profile page form."""
	def __init__(self):
		self.element = DR.flashy_find_element('#profile-form')
		attach_link(self, 'change')

	def __getattr__(self, name):
		"""If an unknown GET message is received, see if there's a field with that name."""
		return DR.flashy_find_element('[name*="{}"]'.format(\
			name.replace('_', '-')), self.element).get_attribute('value')

	def __setattr__(self, name, value):
		"""If an unknown SET message is received, see if there's a field with that name."""
		# Really should have seen this coming.
		if name in {'element', 'change'}:
			object.__setattr__(self, name, value)
			return
		elem = DR.flashy_find_element('[name*="{}"]'.format(name.replace('_', '-')), self.element)
		elem.clear()
		elem.send_keys(value)

	def get_state(self) -> str:
		"""Gets the text of the selected state option."""
		sel = DR.flashy_find_element('[name="state"]', self.element)
		return DR.quietly_find_element('[value="{0}"]'.format(sel.get_attribute('value')), sel).text

	def set_state(self) -> None:
		"""Randomly sets the value of the State field. Returns the chosen value."""
		opt = random.choice(DR.flashy_find_element('[name="state"]', self.element)\
			.find_elements_by_css_selector('option:not([value=""])'))
		opt.click()
		return opt.get_attribute('value')

	def save_changes(self) -> None:
		"""Clicks the Save Changes button."""
		DR.flashy_find_element('#updateProfileSubmit', self.element).click()
		DR.wait_until_present('.fancybox-skin')

	# Enum Hack:
	TRAINEE, QUALIFIED, PREMIER = 'trainee', 'qualified', 'premier'
	def user_level(self) -> str:
		"""Checks the Status Badge area, returns a string of the User Level."""
		if DR.check_visible_quick('.profile-status img', self.element):
			 img = DR.flashy_find_element('.profile-status img', self.element)
			 return {'2.png': self.QUALIFIED, '3.png': self.PREMIER}\
			 	.get(img.get_attribute('src')[-5:], self.TRAINEE)
		else:
			return self.TRAINEE

	def module_badges(self) -> Set[str]:
		"""Checks the Recent Achievements section, returns a set of the badges attained."""
		return {x.get_attribute('alt').split('_')[-1] \
			for x in DR.flashy_find_elements('.Achievements .profile-status img', self.element)}

class TrainingSummary(WrappedElement):
	"""Represents the two Training Summary modules list things."""
	def __init__(self):
		lis = DR.flashy_find_elements('.trainingModuleStatus')
		self.core = lis[0]
		self.optional = lis[1]

	def filter_optional_niche(self) -> None:
		"""Changes the filter on the Optional Modules, then clicks Refresh Results."""
		sel = DR.flashy_find_element('[name="Optional"]', self.optional)
		DR.quietly_find_element('[value="TrainingModule:Optional/Niche"]', sel).click()
		DR.execute_script('for(a of arguments[0])a.remove();', \
			DR.quietly_find_elements('.mosaic-grid-1', self.optional))
		DR.flashy_find_element('#btn-id', self.optional).click()

	def filter_optional_sto(self) -> None:
		"""Changes the filter on the Optional Modules, then clicks Refresh Results."""
		sel = DR.flashy_find_element('[name="Optional"]', self.optional)
		DR.quietly_find_element('[value="TrainingModule:Optional/StateandTerritories"]', sel).click()
		DR.execute_script('for(a of arguments[0])a.remove();', \
			DR.quietly_find_elements('.mosaic-grid-1', self.optional))
		DR.flashy_find_element('#btn-id', self.optional).click()

	def count_modules(self) -> int:
		"""Returns the number of Optional Modules displayed."""
		return len(DR.flashy_find_elements('.mosaic-item', self.optional))

	def get_optional_titles(self) -> List[str]: # pylint: disable-msg=E1126
		"""Returns a list of the titles of the currently displayed Optional Modules"""
		return [t.text for t in DR.flashy_find_elements('.line-through-container', self.optional)]

	def load_more(self) -> None:
		"""Clicks the View More Modules button."""
		count = self.count_modules()
		DR.flashy_find_element('.load-more', self.optional).click()
		DR.wait_until(lambda _: self.count_modules() != count or \
			DR.quietly_find_element('.load-more', self.optional).get_attribute('disabled') == 'true')

	def wait_for_module(self) -> None:
		"""Iframes don't integrate into the DOM ReadyState, so have to check this one explicitly."""
		# Switch into the iframe,
		DR.switch_to_frame('iframe[src^="/content/"]')
		# Then, wait until something is actually present
		DR.wait_until_present('[id^="Text_Caption_"]')
		# Then, wait until the loading overlay is gone.
		DR.wait_until_gone('#preloaderImage')
		# And then, set the module to slide one, just in case.
		DR.execute_script('cpCmndGotoSlide=0')

	def module_one(self) -> None:
		"""Opens the First Core Module."""
		MinorElement('.mosaic-grid-1:nth-child(1) .btn-primary', self.core).click()
		DR.wait_for_page()
		self.wait_for_module()

	def module_two(self) -> None:
		"""Opens the Second Core Module."""
		MinorElement('.mosaic-grid-1:nth-child(2) .btn-primary', self.core).click()
		DR.wait_for_page()
		self.wait_for_module()

	def module_three(self) -> None:
		"""Opens the First Core Module."""
		MinorElement('.mosaic-grid-1:nth-child(3) .btn-primary', self.core).click()
		DR.wait_for_page()
		self.wait_for_module()

	def module_nsw(self) -> None:
		"""Opens the First Optional Module."""
		MinorElement('.mosaic-grid-1:nth-child(1) .btn-primary', self.optional).click()
		DR.wait_for_page()
		self.wait_for_module()

	def module_qld(self) -> None:
		"""Opens the Second Optional Module."""
		MinorElement('.mosaic-grid-1:nth-child(2) .btn-primary', self.optional).click()
		DR.wait_for_page()
		self.wait_for_module()

	def module_vic(self) -> None:
		"""Opens the Third Optional Module."""
		MinorElement('.mosaic-grid-1:nth-child(3) .btn-primary', self.optional).click()
		DR.wait_for_page()
		self.wait_for_module()

	def completion_types(self) -> None:
		"""Gets all of the Module entries, then checks how complete they are,
		then matches that with a Progress Icon type. Kind of a mess."""
		mods = DR.flashy_find_elements('.mosaic-item', self.core) + \
			DR.flashy_find_elements('.mosaic-item', self.optional)
		for mod in mods:
			button = DR.flashy_find_element('.training-continue', mod)
			if re.search('Resume-ASP|Start-ASP', button.get_attribute('data-ta-data-layer')):
				DR.flashy_find_element('img[src*="icon-incomplete.png"]', mod)
			else:
				DR.flashy_find_element('img[src*="icon-complete.png"]', mod)

class Famils(WrappedElement):
	"""Represents the content of the Famils page."""
	def __init__(self):
		self.element = DR.flashy_find_elements('.type-body')[0]

class AussieSpecialistPhotos(WrappedElement):
	"""Represents the image mosaics on the Aussie Specialist Photos page."""
	def __init__(self):
		self.photos = DR.flashy_find_elements('.mosaic-item')

	def random_images(self, num: int) -> List[WrappedElement]: # pylint: disable-msg=E1126
		"""Randomly selects num photos."""
		return [self.Photo(x) for x in random.sample(self.photos, num)]

	class Photo(WrappedElement):
		"""Represents an individual Aussie Specialist Photo.
		Don't instantiate this from the test script directly, it needs a WebElement"""
		def __init__(self, element: WebElement):
			self.element = DR.get_parent_element(DR.get_parent_element(DR.blip_element(element)))
			self.contentpane = None

		def open(self) -> None:
			"""Clicks on the mosaic tile, opening it."""
			MinorElement('.flipper img[src*="image.adapt"]', self.element).point()
			DR.flashy_find_element('.flipper a', self.element).click()
			self.contentpane = [x for x in DR.flashy_find_elements(\
				'.mosaic-item-detail-container.active') if x.is_displayed()][0]

		def get_description(self) -> MinorElement:
			"""Returns the description text in a tile's pane. Has to be open."""
			return MinorElement('p', self.contentpane)

		def get_link(self) -> MinorElement:
			"""Returns the Instagram link from a tiles pane. Has to be open."""
			return MinorElement('a[href*="instagram.com/australia"]', self.contentpane)

		def close(self) -> None:
			"""Clicks the X button in the tiles content. Has to be open first."""
			close = DR.flashy_find_element('.icon-close', self.contentpane)
			close.click()

class SpecialistBadge(WrappedElement):
	"""Represents the Aussie Specialist Badge Download page and image. Kinda minimal."""
	def __init__(self):
		DR.flashy_find_element('a[href*="asp-badge.png"]').click()
		DR.switch_to_window(1)
		# There's no jQuery on a bare image, so can't highlight.
		DR.quietly_find_element('img[src*="asp-badge.png"]')

class AussieStore(WrappedElement):
	"""Contains representations the various pages of the Aussie Store area.
	Don't bother instantiating this one every time, it doesn't do a lot."""
	def __init__(self):
		self.element = DR.quietly_find_element('.contentwrapper')

	def my_cart(self) -> None:
		"""Clicks on the My Cart icon."""
		DR.flashy_find_element('#myCartIcon', self.element).click()

	def empty_cart_notice(self) -> None:
		"""Closes the Your Cart Is Empty message. If it's open."""
		DR.flashy_find_element('.fancybox-skin')
		DR.flashy_find_element('.fancybox-close').click()
		DR.wait_until_gone('.fancybox-skin')

	class CategoriesMenu(WrappedElement):
		"""Represents the list of store Categories to the left."""
		def __init__(self):
			cats = DR.flashy_find_elements('.store-categories>div')
			self.element = cats[0] if cats[0].is_displayed() else cats[1]
			self.categories = DR.quietly_find_elements('li a', self.element)

		def all_products(self) -> None:
			"""Clicks on the All Products link."""
			DR.flashy_find_element('li:first', self.element).click()

		def count(self) -> int:
			"""Gets the number of categories."""
			return len(self.categories)

		def goto_iteree(self, num: int) -> None:
			"""Given an number, clicks on the that-number-th link."""
			DR.blip_element(self.categories[num]).click()

	class ProductGrid(WrappedElement):
		"""Represents the grid of Products that appears on any Category Page."""
		def __init__(self):
			self.element = DR.quietly_find_element('.store-products')
			self.products = DR.flashy_find_elements('.store-products-item')

		def count(self) -> int:
			"""Gets the number of products in this category."""
			return len(self.products)

		def goto_iteree(self, num: int) -> str:
			"""Given a number, clicks on the that-number-th link."""
			prod = DR.blip_element(self.products[num])
			name = prod.text.casefold()
			prod.click()
			return name

		def random_product(self) -> str:
			"""Clicks on a random Product link and returns the product's name."""
			return self.goto_iteree(random.randint(0, len(self.products) - 1))

	class ProductPage(WrappedElement):
		"""Represents a Product's Page."""
		def __init__(self):
			self.element = DR.quietly_find_element('.product')
			DR.flashy_find_element('.col-sm-9.col-xs-12')

		def name(self) -> str:
			"""Gets the Product name displayed in the product info."""
			return DR.flashy_find_element('.product-title', self.element).text.casefold()

		def unique_code(self) -> str:
			"""Gets the Product's Unique Code, as displayed in the product info."""
			return DR.flashy_find_element('.product-code', self.element).text

		def select_max_quantity(self) -> None:
			"""Selects the largest available amount in the quantity selector."""
			sel = DR.flashy_find_element('[name="product-quantity"]', self.element)
			DR.quietly_find_elements('option', sel)[-1].click()

		def add_to_cart(self) -> bool:
			"""Clicks the Add To Cart button.
			Retuns true if successfully added, false if cart was full."""
			DR.flashy_find_element('#cart', self.element).click()
			if DR.check_visible_quick('.fancybox-skin'):
				DR.flashy_find_element('.fancybox-close').click()
				DR.wait_until_gone('.fancybox-skin')
				return False
			DR.LAST_LINK = 'cart.html'
			DR.wait_for_page()
			return True

	class CartPage(WrappedElement):
		"""Represents the My Cart Page."""
		def __init__(self):
			self.element = DR.flashy_find_element('.shoppingcart')

		def place_order(self, cartempty: bool=False) -> None:
			"""Clicks the Place Order button, and waits until it's finished loading/messaging."""
			DR.flashy_find_element('.submit', self.element)
			if not cartempty:
				DR.LAST_LINK = 'confirmation.html'
				DR.wait_for_page()
			else:
				DR.flashy_find_element('.fancybox-skin')
				DR.flashy_find_element('.fancybox-close').click()
				DR.wait_until_gone('.fancybox-skin')

		def contact_details(self) -> str:
			"""Gets the contact details shown at the bottom of the Cart page. Tidy up a bit, too."""
			text = DR.flashy_find_element('.store-order-box-left p:nth-child(2)', self.element).text
			return '\n'.join([x.strip() for x in text.replace('  ', ' ').split('\n')])

		def get_product_names(self) -> List[str]: # pylint: disable-msg=E1126
			"""Gets a list of the names of all of the Products in the Cart."""
			return [x.text for x in DR.flashy_find_elements('.cell-title', self.element)]

		def count(self) -> int:
			"""Counts the number of Products in the Cart."""
			return len(DR.quietly_find_elements('.shoppingcart tr', self.element))

		def remove_random(self) -> str:
			"""Clicks the Remove Product button on a random Product. Returns the ex-product's name."""
			count = self.count() - 1
			rei = random.randint(0, self.count() - 1)
			rem = DR.blip_element(DR.quietly_find_elements('.cell-title', self.element)[rei])
			ren = rem.text.casefold()
			DR.blip_element(DR.quietly_find_elements('.product-remove')[rei]).click()
			self.element = DR.quietly_find_element('.shoppingcart')
			DR.wait_until(lambda _: count == self.count())
			return ren

		def remove_all(self) -> None:
			"""Removes all of the Products from the Cart. This may take a minute if there are a lot."""
			count = self.count()
			while count > 0:
				DR.flashy_find_element('.product-remove').click()
				count -= 1
				self.element = DR.quietly_find_element('.shoppingcart')
				DR.wait_until(lambda _: self.count() == count)
