"""This is where all the specific Webdriver implementation details go."""

import time
import email
import quopri
import imaplib
from types import FunctionType
from typing import List, Union, Any
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException

	###Some Magic Numbers, default values.###
# """The default time, in seconds, to search the DOM before declaring an Element Not Found."""
LONG_WAIT = 30
# """Time in seconds to poll for something that should be absent or already here."""
SHORT_WAIT = 2

# """The root website domain to access."""
BASE_URL = "https://www.aussiespecialist.com"
# """The Language-Country Code of the locale to test.
LOCALE = '/en-gb'
# """To aid in checking for Page Loaded Status, note the last link clicked.
	# TODO: Add a property to this?"""
LAST_LINK = ''

# """The Username with which to perform the test."""
USERNAME = 'gbpwwwvjvz'
# """The password used with the given user."""
PASSWORD = 'Welcome1'
# """The email address associated with the given user."""
EMAIL = 'testeratta@gmail.com'
EMAIL_PASSWORD = 'WelcomeTest'

# """The main WebDriver runner reference."""
DRIVER = webdriver.Chrome()

# """A Set of the full list of options that should be in the splash page language selector."""
LOCALE_SET = {"/en-gb.html", "/en-us.html", "/en-ca.html", "/en-in.html", \
	"/en-my.html", "/en-sg.html", "/id-id.html", "/de-de.html", "/zh-hk.html", \
	"/en-hk.html", "/zh-hk.html", "/en-hk.html", "/ja-jp.html", "/ko-kr.html", \
	"/pt-br.html", "/de-de.html", "/de-de.html", "/fr-fr.html", "/it-it.html", \
	"https://www.aussiespecialist.cn/zh-cn"}
# """A JS script that applies the 'element-highlighted' animation."""
BLIP_SCRIPT = '$("head").append("<style>@keyframes selhian{0%{outline: 0px outset transparent;}\
    50%{outline: 10px outset yellow; background-color: yellow}100%{outline: 0px outset transparent;}}\
	</style>");for(a of arguments[0]){window.scrollTo(0,a.getBoundingClientRect()\
	.top+window.pageYOffset-window.innerHeight/2),a.style.animationDuration="0.5s",\
	a.style.animationName="",setTimeout(function(e){e.style.animationName="selhian"}, 10, a)}'

# """Type annotation, referring to either a WebElement, or a list of them."""
ELEMENT_OR_LIST = Union[WebElement, List[WebElement]] # pylint: disable-msg=E1126
ELEMENT_LIST = List[WebElement] # pylint: disable-msg=E1126

def to_list(item) -> list:
	"""Wraps the input into a list if it wasn't already one."""
	return item if isinstance(item, list) else [item]

def begin() -> None:
	"""The test part calls this at the beginning of each test. Sets up DRIVER."""
	global DRIVER	#It's fine, the AUS.com tests use Global State. Static instance reference anyway.
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

def back() -> None:
	"""The rule is, only the drivery module is allowed to invoke DRIVER."""
	DRIVER.back()

def refresh() -> None:
	"""It's The Rules"""
	DRIVER.refresh()

def wait_for_page() -> None:
	"""Holds up execution until the current page's url contains the Last Link value
	and its	document.readyState is 'complete'. A decent approximation?"""
	script = 'return document.readyState === "complete";'
	WebDriverWait(DRIVER, LONG_WAIT).until(lambda d: LAST_LINK in d.current_url)
	WebDriverWait(DRIVER, LONG_WAIT).until(lambda d: d.execute_script(script))

def wait_until_present(selector: str) -> None:
	"""Holds up execution until the selectored elment is visibly present.
	Use this instead of quietly_find if the target is in the DOM, but hidden."""
	WebDriverWait(DRIVER, LONG_WAIT).until(EC.visibility_of_element_located(selector))

def wait_until_gone(selector: str) -> None:
	"""Holds up execution until the selectored element is not visibly present.
	EC doesn't seem to support local searches, so be sure the selector is page-unique."""
	WebDriverWait(DRIVER, LONG_WAIT).until(EC.invisibility_of_element_located(selector))

def wait_until(condition: FunctionType) -> None:
	"""Holds up execution, repeatedly calling the given function until it returns true."""
	WebDriverWait(DRIVER, LONG_WAIT).until(condition())

def switch_to_window(window: int) -> None:
	"""Switch WebDriver's focus to the second open tab or window."""
	DRIVER.switch_to.window(DRIVER.window_handles()[window])

def switch_to_frame(selector: str) -> None:
	"""Switches WebDriver's focus into the given iframe."""
	DRIVER.switch_to.frame(flashy_find_element(selector))

###Some methods to shorten Element Manipulation/Verification.###

def blip_element(elle: ELEMENT_OR_LIST) -> ELEMENT_OR_LIST:
	"""Scrolls (an) element(s) into view, and highlights (i)t(hem).
	Returns the found element(s) as well, just for chaining purposes."""
	# Kick off the highlight animation, list-wrapped for the sake of only writing one handler.
	DRIVER.execute_script(BLIP_SCRIPT, to_list(elle))
	return elle

def check_visible_quick(selector: str, within: WebElement=DRIVER) -> bool:
	"""Check for an element without potentially spending a lot of time polling the DOM.
	Ususally used when asserting an element's absence, saves waiting the full timeout."""
	DRIVER.implicitly_wait(SHORT_WAIT)
	elements = within.find_elements_by_css_selector(selector)
	DRIVER.implicitly_wait(LONG_WAIT)
	return len(elements) != 0 and elements[0].is_displayed()

def execute_mouse_over(element: WebElement) -> None:
	"""Simulates the mouse moving into an element."""
	ActionChains(DRIVER).move_to_element(element).perform()

def quietly_find_element(selector: str, within: WebElement=DRIVER) -> WebElement:
	"""Finds a single element matching a CSS selector, optionally within a given element."""
	return within.find_element_by_css_selector(selector)

def quietly_find_elements(selector: str, within: WebElement=DRIVER) -> ELEMENT_LIST:
	"""Finds multiple elements that match a CSS selector, optionally within a given element."""
	return to_list(within.find_elements_by_css_selector(selector))

def flashy_find_element(selector: str, within: WebElement=DRIVER) -> WebElement:
	"""Finds a single element matching a CSS selector, highlights it as well."""
	return blip_element(within.find_element_by_css_selector(selector))

def flashy_find_elements(selector: str, within: WebElement=DRIVER) -> ELEMENT_LIST:
	"""Finds multiple elements that match a CSS selector, highlights them as well.

	The browser-provided webdriver driver implementations seem to not return a
	list when only one element matches, so fixing that here."""
	return blip_element(to_list(within.find_elements_by_css_selector(selector)))

def get_parent_element(element: WebElement) -> WebElement:
	"""Gets the immediate parent of the given element."""
	return element.find_element_by_xpath('..')

def bring_to_front(element: WebElement) -> WebElement:
	"""Uses a JS to ensure the selected element is at the front.
	Usually in order to properly click() it."""
	DRIVER.execute_script('arguments[0].style.zIndex = "10000");', element)

def execute_script(script: str, *args) -> Any:
	"""Executes a javascript snippet, returning what the script returns."""
	return DRIVER.execute_script(script, args)

### Guess who learned how to read emails! ###
def check_email(my_email: str, plain: bool=True) -> List[str]: # pylint: disable-msg=E1126
	"""Given a recipient email address to check, get all of the emails it has recently received."""
	results = []
	with imaplib.IMAP4_SSL('imap.gmail.com') as imap:
		imap.login('testeratta@gmail.com', 'WelcomeTest')
		imap.select()
		wait_until(lambda: email_loop(imap, my_email, ''))
		_, nums = imap.search(None, \
			'FROM', EMAIL, 'TO', my_email)
		_, ems = imap.fetch(nums, 'BODY[1]' if plain else 'BODY[2]')
		for em in ems[::2]:	# Yeah, the results come back wierd.
			if plain:
				results.append(em[1].decode())
			else:
				results.append(email.message_from_bytes(quopri.decodestring(em[1])).as_string())

def email_loop(imap: imaplib.IMAP4_SSL, my_email: str, target: str) -> bool:
	"""SEARCHes and FETCHes emails, looking for a certain string to be present.
	Basically, put this in a wait-until loop."""
	imap.search(None, 'FROM', EMAIL, 'TO', my_email)
