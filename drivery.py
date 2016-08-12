"""This is where all the specific Webdriver implementation details go."""

import re
import quopri
import imaplib
from types import FunctionType
from typing import List, Set, Union, Any
import bs4
from selenium.webdriver import Chrome, Edge, Firefox, Ie, Opera, Safari
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException

	###Some Magic Numbers, default values.###
def reset_globals():
	"""Call this to reset all of the globals that can get overwritten to their default values."""
	# pylint: disable-msg=W0603
	global LONG_WAIT, SHORT_WAIT, CN_MODE, BASE_URL, CN_BASE_URL, LOCALE, EMAIL, BROWSER_TYPE
	LONG_WAIT, SHORT_WAIT, CN_MODE, BASE_URL, CN_BASE_URL, LOCALE, EMAIL, BROWSER_TYPE = \
		30, 2, False, 'https://www.aussiespecialist.com', 'https://www.aussiespecialist.cn', \
		'/en-gb', 'testeratta+{}@gmail.com', Chrome
# """The default time, in seconds, to search the DOM before declaring an Element Not Found."""
LONG_WAIT = 30
# """Time in seconds to poll for something that should be absent or already here."""
SHORT_WAIT = 2

CN_MODE = False
# """The root website domain to access."""
BASE_URL = 'https://www.aussiespecialist.com'
CN_BASE_URL = 'https://www.aussiespecialist.cn'
# """The Language-Country Code of the locale to test.
LOCALE = '/en-gb'
CN_LOCALE = '/zh-cn'
LOCALES = {'ca': '/en-ca', 'in': '/en-in', 'my': '/en-my', 'sg': '/en-sg', \
'gb': '/en-gb', 'us': '/en-us', \
'ehk': '/en-hk', 'zhk': '/zh-hk', 'id': '/id-id', 'jp': '/ja-jp', 'kr': '/ko-kr', \
'br': '/pt-br', 'cl': '/es-cl', 'de': '/de-de', 'fr': '/fr-fr', 'it': '/it-it', \
'cn': CN_LOCALE}
# """To aid in checking for Page Loaded Status, note the last link clicked.
LAST_LINK = ''

# """The generic standard Test Account Password."""
PASSWORD = 'Welcome1'
# """The email address to be associated with the given user."""
EMAIL = 'testeratta+{}@gmail.com'
# Login details for the gmail IMAP server, if that ever becomes a thing.
TEST_EMAIL_IMAP_SERVER = 'imap.gmail.com'
TEST_EMAIL_USERNAME = 'testeratta@gmail.com'
TEST_EMAIL_PASSWORD = 'WelcomeTest'
ASP_EMAIL = 'tourism-au@updates.tourism.australia.com'
ASP_CN_EMAIL = 'asp-cn@tourism.australia.com'
LATIN_EMAIL_ENCODING = 'windows-1252'

# """The main WebDriver runner reference."""
BROWSER_TYPE = Chrome	# Not really a Class, just a reference to one. pylint: disable-msg=C0103
BROWSERS = {'chrome': Chrome, 'edge': Edge, 'firefox': Firefox, \
	'ie': Ie, 'opera': Opera, 'safari': Safari}
DRIVER = Chrome		# Global variable placeholder

# """A Set of the full list of options that should be in the splash page language selector."""
LOCALE_SET = {"/en-gb.html", "/en-us.html", "/en-ca.html", "/en-in.html", \
	"/en-my.html", "/en-sg.html", "/id-id.html", "/de-de.html", "/zh-hk.html", \
	"/en-hk.html", "/zh-hk.html", "/en-hk.html", "/ja-jp.html", "/ko-kr.html", \
	"/pt-br.html", "/de-de.html", "/de-de.html", "/fr-fr.html", "/it-it.html", \
	"https://www.aussiespecialist.cn/zh-cn"}
# A script to scroll a single element into view proper, just in case. Parent chain handles modules.
SCROLL_SCRIPT = 'wp=window.parent.parent.parent;wp.scrollTo(0,\
	arguments[0].getBoundingClientRect().top+wp.pageYOffset-wp.innerHeight/2)'
# """A JS script that applies the 'element-highlighted' animation."""
BLIP_SCRIPT = '$("head").append("<style>@keyframes selhian{0%{outline: 0px outset transparent;} \
50%{outline: 10px outset yellow; background-color: yellow}100%{outline: 0px outset transparent;}} \
</style>");wp=window.parent.parent.parent;b=arguments[0];for(var a=0;a<b.length;a++) \
{var c=b[a];wp.scrollTo(0,c.getBoundingClientRect().top+wp.pageYOffset-wp.innerHeight/2), \
c.style.animationDuration="0.5s",c.style.animationName="",setTimeout(function(e) \
{e.style.animationName="selhian"}, 10, c)}'

# """Type annotation, referring to either a WebElement, or a list of them."""
ELEMENT_OR_LIST = Union[WebElement, List[WebElement]] # pylint: disable-msg=E1126
ELEMENT_LIST = List[WebElement] # pylint: disable-msg=E1126

def to_list(item) -> list:
	"""Wraps the input into a list if it wasn't already one."""
	return item if isinstance(item, list) else [item]

def begin() -> None:
	"""The test part calls this at the beginning of each test. Sets up DRIVER."""
	global DRIVER	# pylint: disable-msg=W0603
	# It's fine, the AUS.com tests use Global State. Static instance reference anyway.
	DRIVER = BROWSER_TYPE()
	DRIVER.implicitly_wait(LONG_WAIT)
	DRIVER.maximize_window()

def close() -> None:
	"""The testing bit calls this at the end of each test. Clears the session."""
	DRIVER.quit()

###Navigation Methods.###

def splash_page() -> None:
	"""Navigates to the Splash Page."""
	DRIVER.get(BASE_URL + '/splash.html')

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

def get(url: str) -> None:
	"""RULES."""
	DRIVER.get(url)

def wait_for_page() -> None:
	"""Holds up execution until the current page's url contains the Last Link value
	and its	document.readyState is 'complete'. A decent approximation?"""
	script = 'return document.readyState === "complete";'
	try:
		WebDriverWait(DRIVER, LONG_WAIT).until(lambda d: LAST_LINK in d.current_url)
		WebDriverWait(DRIVER, LONG_WAIT).until(lambda d: d.execute_script(script))
	except TimeoutException:
		raise TimeoutException('Timed out waiting for {0} to load.'.format(LAST_LINK))

def wait_until_present(selector: str) -> WebElement:
	"""Holds up execution until the selectored elment is visibly present.
	Use this instead of quietly_find if the target is in the DOM, but hidden."""
	try:
		return WebDriverWait(DRIVER, LONG_WAIT).until(\
			EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
	except TimeoutException:
		raise TimeoutException('Timed out waiting for {0} to appear.'.format(selector))

def wait_until_gone(selector: str) -> WebElement:
	"""Holds up execution until the selectored element is not visibly present.
	EC doesn't seem to support local searches, so be sure the selector is page-unique."""
	try:
		DRIVER.implicitly_wait(0.5)	# The poll_freq value is not, in fact, the wait-til-fail time.
		ret = WebDriverWait(DRIVER, LONG_WAIT).until(\
			EC.invisibility_of_element_located((By.CSS_SELECTOR, selector)))
		DRIVER.implicitly_wait(LONG_WAIT)
		return ret
	except TimeoutException:
		raise TimeoutException('Timed out waiting for {0} to disappear.'.format(selector))

def wait_until(condition: FunctionType) -> Any:
	"""Holds up execution, repeatedly calling the given function until it returns truthy."""
	try:
		return WebDriverWait(DRIVER, LONG_WAIT).until(condition)
	except TimeoutException:
		raise TimeoutException('Timed out waiting for method {0} to be true.'.format(condition))

def switch_to_window(window: int) -> None:
	"""Switch WebDriver's focus to the second open tab or window."""
	DRIVER.switch_to.window(DRIVER.window_handles[window])	# Yes it does. pylint: disable-msg=E1101

def switch_to_frame(selector: str) -> None:
	"""Switches WebDriver's focus into the given iframe."""
	DRIVER.switch_to.frame(flashy_find_element(selector))	# Yes it does. pylint: disable-msg=E1101

def fix_url(url: str) -> str:
	"""Use this to remove that /content/asp/ stuff from URLs."""
	return re.sub(r'(/\w\w)_(\w\w/)', r'\1-\2', (url or '').replace('/content/asp/', '/'), count=1)

###Some methods to shorten Element Manipulation/Verification.###

def scroll_element(elle: WebElement) -> WebElement:
	"""Scrolls a single element into view, it wouldn't make sense to do multiple."""
	DRIVER.execute_script(SCROLL_SCRIPT, elle)
	return elle

def blip_element(elle: ELEMENT_OR_LIST) -> ELEMENT_OR_LIST:
	"""Scrolls (an) element(s) into view, and highlights (i)t(hem).
	Returns the found element(s) as well, just for chaining purposes."""
	# Kick off the highlight animation, list-wrapped for the sake of only writing one handler.
	DRIVER.execute_script(BLIP_SCRIPT, to_list(elle))
	return elle

def check_visible_quick(selector: str, within: WebElement=None) -> bool:
	"""Check for an element without potentially spending a lot of time polling the DOM.
	Ususally used when asserting an element's absence, saves waiting the full timeout."""
	within = within or DRIVER
	DRIVER.implicitly_wait(SHORT_WAIT)
	elements = within.find_elements_by_css_selector(selector)
	DRIVER.implicitly_wait(LONG_WAIT)
	return len(elements) != 0 and elements[0].is_displayed()

def execute_mouse_over(element: WebElement) -> None:
	"""Simulates the mouse moving into an element."""
	ActionChains(DRIVER).move_to_element(element).perform()

def find_error_improver(func):
	"""A decorator to get the NoSuchElementException to actually tell you what the problem is."""
	def actually_helpful(selector, within=None):
		"""Does a thing, and if it didn't work, tells you what was missing from where."""
		try:
			return func(selector, within)
		except NoSuchElementException:
			raise NoSuchElementException("Couldn't find selector '{0}' on page {1}".format(selector, \
				current_url()))
	return actually_helpful

@find_error_improver
def quietly_find_element(selector: str, within: WebElement=None) -> WebElement:
	"""Finds a single element matching a CSS selector, optionally within a given element."""
	within = within or DRIVER
	return within.find_element_by_css_selector(selector)

@find_error_improver
def quietly_find_elements(selector: str, within: WebElement=None) -> ELEMENT_LIST:
	"""Finds multiple elements that match a CSS selector, optionally within a given element."""
	within = within or DRIVER
	return to_list(within.find_elements_by_css_selector(selector))

@find_error_improver
def flashy_find_element(selector: str, within: WebElement=None) -> WebElement:
	"""Finds a single element matching a CSS selector, highlights it as well."""
	within = within or DRIVER
	return blip_element(within.find_element_by_css_selector(selector))

@find_error_improver
def flashy_find_elements(selector: str, within: WebElement=None) -> ELEMENT_LIST:
	"""Finds multiple elements that match a CSS selector, highlights them as well.

	The browser-provided webdriver driver implementations seem to not return a
	list when only one element matches, so fixing that here."""
	within = within or DRIVER
	return blip_element(to_list(within.find_elements_by_css_selector(selector)))

def get_parent_element(element: WebElement) -> WebElement:
	"""Gets the immediate parent of the given element."""
	return element.find_element_by_xpath('..')

def bring_to_front(element: WebElement) -> WebElement:
	"""Uses a JS to ensure the selected element is at the front.
	Usually in order to properly click() it."""
	DRIVER.execute_script('arguments[0].style.zIndex = "10000";', element)

def execute_script(script: str, *args) -> Any:
	"""Executes a javascript snippet, returning what the script returns."""
	return DRIVER.execute_script(script, *args)

class Email:
	"""Handler for the email checks. Due to languages, there's really no way to tell
	which email is which, so to ensure schedule synchronicity, make sure
	get_new_messages is called every time an email is expected."""
	def __init__(self, userid):
		self.email = EMAIL.format(userid)

	def get_all_locales(self) -> Set[str]: 	# pylint: disable-msg=E1126
		"""Collects all of the emails received by this email subaddress,
		and returns a set of Locale codes representing each one found."""
		locs = set()
		ems = [bs4.BeautifulSoup(x, 'html.parser') for x in self.get_new_messages(really_get_new=False)]
		for ema in ems:
			if CN_MODE:	# China does not have locale-tagged links.
				links = ema.select('a[href*="t.dpc.rimanggis.com"]')
				hrefs = {x['href'].split('.')[-1] for x in links}
				locs = locs.union({'zh-cn'} if hrefs == {'json'} else hrefs)
			else:
				links = ema.select('a[href*="t.updates.tourism.australia.com"]')
				hrefs = [re.search(r'p1\=\w\w((-|_)\w\w)?', x['href']) for x in links]
				locs = locs.union({x.group().split('=')[-1] for x in hrefs if x})
		return locs

	def get_new_messages(self, really_get_new: bool=True) -> List[str]: # pylint: disable-msg=E1126
		"""Polls the IMAP server untill a (maybe) new email(s) are found, then
		attempts to make sense of their ridiculous transmission formatting."""
		results = []
		with imaplib.IMAP4_SSL(TEST_EMAIL_IMAP_SERVER) as imap:
			imap.login(TEST_EMAIL_USERNAME, TEST_EMAIL_PASSWORD)
			imap.select()
			nums = wait_until(lambda _: self.email_loop(imap, really_get_new))
			# The Latin Character Set emails have two parts, the second of which is the one you want.
			got, ems = imap.fetch(nums, 'body[2]')
			if got == 'NO':	# The others do not have two parts.
				got, ems = imap.fetch(nums, 'body[1]')
			for ema in ems[::2]:	# Yeah, the results come back wierd.
				try:
					results.append(quopri.decodestring(ema[1]).decode())
				except UnicodeDecodeError:	# Some quasi-latin languages are different
					results.append(quopri.decodestring(ema[1]).decode(LATIN_EMAIL_ENCODING))
		return results

	def email_loop(self, imap: imaplib.IMAP4_SSL, really_get_new: bool=True) -> bytes:
		"""SEARCHes the server, checking for (maybe) new email. Put this in a wait-until loop."""
		imap.noop()
		# Returns a tuple. (Result_code, Actual_results). Actual_results is also a list.
		# Containing a single bytestring of space-separated return values.
		# And IMAP requires that imput values be comma separated. 		Because why not.
		return b','.join(imap.search(None, 'FROM', ASP_CN_EMAIL if CN_MODE else ASP_EMAIL, \
			'TO', self.email, 'UNSEEN' if really_get_new else 'SEEN')[1][0].split(b' '))

	class LocalizedEmail():	# Oh, whatever. pylint: disable-msg=R0903
		"""Superclass for the various emails."""
		def __init__(self, userid: str):
			self.email = bs4.BeautifulSoup(Email(userid).get_new_messages()[0], 'html.parser')
			self.userid = userid

	class RegistrationEmail(LocalizedEmail):	# pylint: disable-msg=R0903
		"""Represents the Registration Email, if used correctly. Correctly here meaning:
		instantiate this shortly after registering, and be sure to attach it to
		an email sub-address with no existing unread messages."""
		def activation_link(self) -> str:
			"""Returns the address of the Click Here To Activate Your Account link."""
			if CN_MODE:	# China does not have that format of link.
				return self.email.a['href']
			else:
				return self.email.select('a[href*="activation"]')[0]['href']

	class ForgottenUsernameEmail(LocalizedEmail):	# pylint: disable-msg=R0903
		"""Represents the Forgotten Username Email.
		If it is called at the right time, of course."""
		def get_username(self) -> str:
			"""Returns the Username that the email is trying to remind you of."""
			return self.email.find('td', string=re.compile(self.userid)).string


	class ForgottenPasswordEmail(LocalizedEmail):
		"""Represents the Forgotten Password Email.
		If it is called at the right time, of course."""
		def get_username(self) -> str:
			"""Forgotten Password email also contains your Username, returns that."""
			return self.email.find('td', string=re.compile(self.userid)).string

		def get_password(self) -> str:
			"""Returns the new temporary password from the email."""
			# No idea what the new password will look like, so use a relative search.
			ustd = self.email.find('td', string=re.compile(self.userid))
			# Get the Username cell, then wander through the tree a bit.
			return ustd.parent.next_sibling.next_sibling.contents[3].string

class Backup:
	"""A context handler, put this around a step that could fail, and which counts as a fail, \
	but whose failure does not actually prevent further testing if you know what you're doing. \
	The onfail argument is what you know that you're doing."""
	def __init__(self, onfail: FunctionType) -> None:
		self.onfail = onfail

	def __enter__(self) -> None:
		pass

	def __exit__(self, extype, exinst, extrace) -> Any:
		self.onfail()
		return True
