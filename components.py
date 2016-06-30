"""Implements classes wrapping the behaviour for finding and manipulating web elements."""

import re
import random
from selenium.webdriver.remote.webelement import WebElement
import drivery as DR

class WrappedElement:
	"""Superclass for the various helper classes here."""
	# This is a placeholder, don't actually try this.
	element = WebElement(parent=None, id_=None)

	def click(self) -> None:
		"""Clicks on the element."""
		DR.LAST_LINK = self.element.get_attribute('href')
		self.element.click()

	def point(self) -> None:
		"""Moves the mouse cursor over the element."""
		DR.execute_mouse_over(self.element)

class SplashSelect(WrappedElement):
	"""Represents the Language Selector on the Splash Page."""
	def __init__(self) -> None:
		self.element = DR.flashy_find_element('.dropdown-select-language')

	def get_values(self) -> set(str):
		"""Gets a set containing the URLs of all the Language Options."""
		return {x.get_attribute('value') for x in DR.quietly_find_elements('option', self.element)}

	def choose_locale(self) -> None:
		"""Selects the Language Option representing the current locale."""
		option = DR.quietly_find_element('option[value*="{}"]'.format(DR.LOCALE), self.element)
		DR.LAST_LINK = option.get_attribute('value')
		option.click()

class WelcomeVideo(WrappedElement):
	"""Represents the main Video on the home page."""
	def __init__(self) -> None:
		self.element = DR.flashy_find_element('#hero-player')

	def play(self) -> None:
		"""Clicks the video's Play button."""
		DR.flashy_find_element('.cts-icon-play', self.element).click()

	def is_playing(self) -> bool:
		"""Checks whether the video is playing."""
		return DR.quietly_find_element('.vjs-play-control', self.element).is_displayed()

class BodyLoginButton(WrappedElement):
	"""Represents the Sign In button that appears in a page's body content when signed out."""
	def __init__(self) -> None:
		self.element = DR.flashy_find_element('#loginCompButton > div > a.btn-primary.fancybox')

class BodyRegisterButton(WrappedElement):
	"""Represents the Join The Program button that appears in a page's body content when signed out."""
	def __init__(self) -> None:
		self.element = DR.flashy_find_element('#loginCompButton > div > a:nth-child(2)')

class WhatYouCanSeeMosaic(WrappedElement):
	"""Represents the What You Can See Mosaic, however many tiles may appear."""
	def __init__(self) -> None:
		self.element = DR.flashy_find_element('div.whatYouCanSee div.mosaic')

	def tile_count(self) -> int:
		"""Returns the number of tiles in the mosaic."""
		return len(DR.quietly_find_elements('div.mosaic-item', self.element))

class NavLink(WrappedElement):
	"""Because creating fifty separate classes would be tiresome."""
	def __init__(self, selector: str, within: WrappedElement) -> None:
		self.element = DR.flashy_find_element(selector, within)

def attach_link(section: WrappedElement, name: str, selector: str='[href*={}.html]') -> None:
	"""A function that attaches an attribute that can be called to create a NavLink.
	The 'name' argument should be the bit that .formats into the selector"""
	def link_maker():
		"""A function that can be called to create a NavLink"""
		return NavLink(selector.format(name), section.element)
	link_maker.__doc__ = 'Creates the {0}/{1} link representation'\
		.format(type(section), name.replace('-', ' ').replace('.', ' ').title())
	section.__setattr__(name.replace('-', '_').replace('.', '_'), link_maker)

class About(WrappedElement):
	"""Represents the About menu in the main nav menu."""
	def __init__(self) -> None:
		self.element = DR.flashy_find_element('#nav-main-panel-1')
		attach_link(self, 'about')
		attach_link(self, 'benefits')
		attach_link(self, 'how-to-use-the-site')
		attach_link(self, 'program-faq')
		attach_link(self, 'contact-us')

class SalesResources(WrappedElement):
	"""Represents the Sales Resources menu in the main nav menu."""
	def __init__(self) -> None:
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

class Training(WrappedElement):
	"""Represents the Training menu in the main nav menu."""
	def __init__(self) -> None:
		self.element = DR.flashy_find_element('#nav-main-panel-3')
		attach_link(self, 'training')
		attach_link(self, 'training-summary')
		attach_link(self, 'webinars')

class NewsAndProducts(WrappedElement):
	"""Represents the News And Products menu in the main nav menu."""
	def __init__(self) -> None:
		self.element = DR.flashy_find_element('#nav-main-panel-4')
		attach_link(self, 'news-and-product-updates')
		attach_link(self, 'latest-news')
		attach_link(self, 'product-videos')

class AussieSpecialistClub(WrappedElement):
	"""Represents the Aussie Specialist Club menu in the main nav menu."""
	def __init__(self) -> None:
		self.element = DR.flashy_find_element('#nav-main-panel-5')
		attach_link(self, 'aussie-specialist-club')
		attach_link(self, 'travel-club')
		attach_link(self, 'aussie-specialist-photos')
		attach_link(self, 'asp-logo')
		attach_link(self, 'aussie-store')

class NavMenu(WrappedElement):
	"""In case you need to refer to all of the nav menu elements collectively."""
	about = About
	sales_resources = SalesResources
	training = Training
	news_and_products = NewsAndProducts
	aussie_specialist_club = AussieSpecialistClub
	def __init__(self) -> None:
		self.element = DR.flashy_find_element('#nav-bar-top .nav-bar-left')

	def get_all_links(self) -> set(str):
		"""Gets a set containing the href of each link in the nav menu.
		The Five/Four section panels, that is, not the Icons, or the Sign In thing."""
		return {x.get_attribute('href') for x in DR.flashy_find_elements(\
			'#nav-bar-top .nav-bar-left a:not([href^="#"])', self.element)}

class Footer(WrappedElement):
	"""Represents the global Footer."""
	def __init__(self) -> None:
		self.element = DR.flashy_find_element('footer.main-footer')
		attach_link(self, 'splash')
		attach_link(self, 'facebook', selector='[href*="www.{}.com"]')
		attach_link(self, 'plus.google', selector='[href*="www.{}.com"]')
		attach_link(self, 'youtube', selector='[href*="www.{}.com"]')
		attach_link(self, 'twitter', selector='[href*="{}.com"]')
		attach_link(self, 'instagram', selector='[href*="{}.com"]')
		attach_link(self, 'sitemap')
		attach_link(self, 'privacy-policy')
		attach_link(self, 'terms-and-conditions')
		attach_link(self, 'terms-of-use')
		attach_link(self, 'contact-us')
		attach_link(self, 'australia', selector='[href*="www.{}.com"]')
		attach_link(self, 'tourism.australia', selector='[href*="www.{}.com"]')
		attach_link(self, 'businessevents.australia', selector='[href*="{}.com"]')

class Sitemap(WrappedElement):
	"""Represents the Sitemap link cloud."""
	def __init__(self) -> None:
		self.element = DR.flashy_find_element('.sitemap')
		attach_link(self, 'change')
		attach_link(self, 'newsletter-unsubscribe')
		attach_link(self, 'coming-soon')

	def get_all_links(self) -> set(str):
		"""Gets a set containing the href of each link in the Sitemap link section."""
		return {x.get_attribute('href') for x in DR.flashy_find_elements('a', self.element)}

class FilteredSearch(WrappedElement):
	"""Represents the Itinerary or Fact Sheet Search Components."""
	def __init__(self, fact_sheet_mode: bool=False) -> None:
		self.element = DR.flashy_find_element('.filteredSearch')
		self.fact_sheet_mode = fact_sheet_mode
		# Hold up, have to wait for the initial results to come in first,
		# they'll interrupt if they appear halfway through something else.
		DR.quietly_find_element('.mosic-item')

	class SearchResult(WrappedElement):
		def __init__(self, which: WebElement):
			self.element = which

		def get_title(self) -> str:
			"""Gets the page Title/Name of the result."""
			return DR.flashy_find_element('.line-through-container', self.element).text()

		def view_more_information(self) -> None:
			"""Navigates to the result's main page, clicks the View More Info link."""
			DR.flashy_find_element('.search-results-copy-container a', self.element)

		def add_to_favourites(self) -> None:
			"""Clicks the result's Heart Icon: Add To My Sales Tool Kit."""
			DR.flashy_find_element('.search-favourite a', self.element)

	def load_more(self) -> WrappedElement:
		"""Clicks the Search Component's Load More button."""
		DR.flashy_find_element('#btn-id', self.element).click()
		DR.wait_until_gone('.filteredSearch .preload-image-wrapper img')

	def random_search(self):
		"""Picks random values in each of the search category droplists,
		then clicks the Refresh Results button. Repeats this until results are found."""
		while True:
			for select in DR.quietly_find_elements('select', self.element):
				DR.blip_element(select)
				random.choice(DR.quietly_find_elements('option', select)).click()
			DR.flashy_find_elements('#btn-id', self.element).click()
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
		counter = DR.flashy_find_element('.search-result-count-copy', self.element).text()
		counter = [int(x) for x in re.findall(r'\d+', counter)]
		if counter == []:
			 return None
		# Different languages can show the numbers in different orders.
		counter.sort()
		# The largest number has to be the total results, with the other two being 'this many shown'.
		return (1 + counter[1] - counter[0], counter[2])

	def get_random_result(self) -> WrappedElement:
		"""Picks a random one from the search results."""
		result = SearchResult()
