"""Implements classes wrapping the behaviour for finding and manipulating web elements."""

from selenium.webdriver.remote.webelement import WebElement
import drivery as DR

class WrappedElement:
	"""Superclass for the various helper classes here."""
	# This is a placeholder, don't actually try this.
	element = WebElement(parent=None, id_=None)

	def click(self) -> None:
		"""Clicks on the element."""
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
		return {x.get_attribute('value') for x in self.element.find_elements_by_tag_name('option')}

	def choose_locale(self) -> None:
		"""Selects the Language Option representing the current locale."""
		option = self.element.find_element_by_css_selector('option[value*="{}"]'.format(DR.LOCALE))
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
		return self.element.find_element_by_css_selector('.vjs-play-control').is_displayed()

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
		return len(self.element.find_elements_by_css_selector('div.mosaic-item'))

class About(WrappedElement):
	"""Represents the About menu in the main nav menu."""
	def __init__(self) -> None:
		self.element = DR.flashy_find_element('#nav-main-panel-1')

	def about(self) -> WrappedElement:
		"""Creates the About/About link representation."""
		return self.About(self.element)

	class About(WrappedElement):
		"""Represents the About/About link"""
		def __init__(self, parel) -> None:
			self.element = DR.flashy_find_element('[href*="about.html"]', parel)

class SalesResources(WrappedElement):
	"""Represents the Sales Resources menu in the main nav menu."""
	def __init__(self) -> None:
		self.element = DR.flashy_find_element('#nav-main-panel-2')

class Training(WrappedElement):
	"""Represents the Training menu in the main nav menu."""
	def __init__(self) -> None:
		self.element = DR.flashy_find_element('#nav-main-panel-3')

class NewsAndProducts(WrappedElement):
	"""Represents the News And Products menu in the main nav menu."""
	def __init__(self) -> None:
		self.element = DR.flashy_find_element('#nav-main-panel-4')

class AussieSpecialistClub(WrappedElement):
	"""Represents the Aussie Specialist Club menu in the main nav menu."""
	def __init__(self) -> None:
		self.element = DR.flashy_find_element('#nav-main-panel-5')
