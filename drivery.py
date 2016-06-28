"""This is where all the specific Webdriver implementation details go."""

import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

	###Some Magic Numbers, default values.###
# """Time, in seconds, for an element to remain highlighted when hit with blip()."""
BLINK_TIME = 0.5
# """The default time, in seconds, to search the DOM before declaring an Element Not Found."""
LONG_WAIT = 30
# """Time in seconds to poll for something that should be absent or already here."""
SHORT_WAIT = 3

# """The root website domain to access."""
BASE_URL = "https://www.aussiespecialist.cn"
# """The Language-Country Code of the locale to test. Format: /\\w\\w-\\w\\w"""
LOCALE = '/zh-cn'
# """To aid in checking for Page Loaded Status, note the last link clicked.
	# TODO: Add a property to this?"""
LAST_LINK = ''

# """The Username with which to perform the test."""
USERNAME = 'zhprozxcv'
# """The password used with the given user."""
PASSWORD = 'Welcome1'
# """The email address associated with the given user."""
EMAIL = 'testeratta@gmail.com'

# """The main WebDriver runner reference."""
DRIVER = webdriver.Firefox()

# """A Set of the full list of options in the splash page language selector."""
LOCALE_SET = {"/en-gb.html", "/en-us.html", "/en-ca.html", "/en-in.html", \
	"/en-my.html", "/en-sg.html", "/id-id.html", "/de-de.html", "/zh-hk.html", \
	"/en-hk.html", "/zh-hk.html", "/en-hk.html", "/ja-jp.html", "/ko-kr.html", \
	"/pt-br.html", "/de-de.html", "/de-de.html", "/fr-fr.html", "/it-it.html", \
	"https://www.aussiespecialist.cn/zh-cn"}
# """A CSS description of the 'element-highlighted' style."""
HIGHLIGHT_STYLE = 'background: yellow; border: 2px solid red; color: black;'

def to_singleton(item) -> list:
	"""This thing. Makes a thing into a list if it isn't already one."""
	return item if isinstance(item, list) else [item]

def begin() -> None:
	"""The test part calls this at the beginning of each test. Sets up DRIVER."""
	global DRIVER	#This is fine. The AUS.com tests use Global State. Static instance reference anyway.
	DRIVER = webdriver.Firefox()
	DRIVER.implicitly_wait(LONG_WAIT)

def close() -> None:
	"""The testing bit calls this at the end of each test. Clears the session."""
	DRIVER.quit()
	time.sleep(SHORT_WAIT)

###Navigation Methods.###

def splash_page() -> None:
	"""Navigates to the Splash Page.

	Or the url set as BASE_URL, rather. But those should be the same."""
	DRIVER.get(BASE_URL)

def open_home_page() -> None:
	"""Opens the Welcome Page. Shortcut method."""
	DRIVER.get(BASE_URL + LOCALE)

def current_url() -> str:
	"""Kind of a technicality. Returns the current url."""
	return DRIVER.current_url

def wait_for_page() -> None:
	"""Holds up execution until the current page's url ~= the Last Link value
	and its	document.readyState is 'complete'. A decent approximation?"""
	script = 'return document.readyState === "complete";'
	docpl = lambda: DRIVER.execute_script(script)
	WebDriverWait(DRIVER, LONG_WAIT).until(EC.title_contains(LAST_LINK))
	WebDriverWait(DRIVER, LONG_WAIT).until(docpl)

###Some methods to shorten Element Manipulation/Verification.###

def scroll_to(element: WebElement) -> None:
	"""Uses javascript to scroll the given element into view."""
	DRIVER.execute_script("window.scrollTo(0,arguments[0].\
	getBoundingClientRect().top + window.pageYOffset - \
	(window.innerHeight / 2));", element)

def blip_element(elle: 'WebElement or [WebElements]') -> 'WebElement or [WebElements]':
	"""Scrolls (an) element(s) into view, and highlights (i)t(hem).

	Returns the found element(s) as well, just for chaining purposes."""
	# Treat everything as a list for the sake of only writing one handler.
	if not isinstance(elle, list):
		elle = [elle]
	def apse(styl: str) -> None:
		"""Blip + Scrollto the element(s) given."""
		DRIVER.execute_script("for(var i = 0; i < arguments[0].length; i++) \
		{var a = arguments[0][i]; window.scrollTo(0, a.getBoundingClientRect()\
		.top + window.pageYOffset - (window.innerHeight / 2)); a.setAttribute(\
		'style', arguments[1][i])}", elle, styl)
	# Keep a record of the elements' original styles.
	ost = [x.get_attribute('style') for x in elle]
	# And also a record of the highlighted style.
	est = [x + HIGHLIGHT_STYLE for x in ost]
	# Apply the highlight, wait a bit, then remove it.
	apse(est)
	time.sleep(BLINK_TIME)
	apse(ost)
	# Then return the element(s).
	return elle[0] if len(elle) == 1 else elle

def blip_function(fiel: 'function -> WebElement') -> 'function -> WebElement':
	"""Adds scrollto and highlight effects to an Element Finding method."""
	# Create a function that will do the following.
	def reul(*parg, **karg) -> WebElement:
		"""Some kind of Element Finding method, now with highlighting."""
		# Call the given Find Element Method.
		elle = fiel(*parg, **karg)
		# Highlight the found element.
		blip_element(elle)
		# And return the element.
		return elle
	# And return that new function.
	return reul

def check_visible_quick(selector: str) -> bool:
	"""Look for an element without spending a lot of time polling the DOM.

	Ususally used when asserting an element's absence, saves waiting the full timeout."""
	DRIVER.implicitly_wait(SHORT_WAIT)
	try:
		element = DRIVER.find_element(by=By.CSS_SELECTOR, value=selector)
	except NoSuchElementException:
		DRIVER.implicitly_wait(LONG_WAIT)
		return False
	DRIVER.implicitly_wait(LONG_WAIT)
	return element.is_displayed()

def execute_mouse_over(element: WebElement) -> None:
	"""Simulates the mouse moving into an element."""
	ActionChains(DRIVER).move_to_element(element).perform()

def flashy_find_element(selector: str, within: WebElement=DRIVER) -> WebElement:
	"""Finds a single element matching a CSS selector, highlights it as well."""
	return blip_element(within.find_element_by_css_selector(selector))

def flashy_find_elements(selector: str, within: WebElement=DRIVER) -> [WebElement]:
	"""Finds multiple elements that match a CSS selector, highlights them as well.

	The browser-provided webdriver driver implementations seem to not return a
	list when only one element matches, so fixing that here."""
	return blip_element(to_singleton(within.find_elements_by_css_selector(selector)))
