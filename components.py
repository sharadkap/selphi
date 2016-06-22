"""Implements classes wrapping the behaviour for finding and manipulating web elements."""

from selenium.webdriver.remote.webelement import WebElement
import drivery as DR

class SplashSelect:
	"""Represents the Language Selector on the Splash Page."""
	def __init__(self) -> None:
		self.element = DR.flashy_find_element('.dropdown-select-language')

	def get_values(self) -> set(str):
		"""Gets a set containing the URLs of all the Language Options."""
		return {x.get_attribute('value') for x in self.element.find_elements_by_tag_name('option')}

	def choose_locale(self) -> None:
		option = self.element.find_element_by_css_selector('option[value*="{}"]'.format(DR.LOCALE))
		DR.LAST_LINK = option.get_attribute('value')
		option.click()

class WelcomeVideo:
	"""Represents the main Video on the home page."""
	def __init__(self) -> None:
		self.element = DR.flashy_find_element('#hero-player')
