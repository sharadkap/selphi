"""This is where all the specific Webdriver implementation details go."""

import re
import quopri
import imaplib
from typing import List, Set, Union, Any, Callable
from selenium.webdriver import Chrome, Edge, Firefox, Ie, Opera, Safari, FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotVisibleException
from selenium.webdriver.chrome.options import Options as ChromeOptions
import bs4

    ###Some Magic Numbers, default values.###
# """How long, in seconds, to search the DOM before declaring an Element Not Found."""
LONG_WAIT = 30
# """Time in seconds to poll for something that should be absent or already here."""
SHORT_WAIT = 2

# Parameterise this word to remember the spelling.
LATIN_EMAIL_ENCODING = 'windows-1252'

# A mapping of browser names to WebDriver Classes.
BROWSERS = {'chrome': Chrome, 'edge': Edge, 'firefox': Firefox,
            'ie': Ie, 'opera': Opera, 'safari': Safari}

# A script to scroll a single element into view proper, just in case.
SCROLL_SCRIPT = (
    'var w=window.top,a=arguments[0];try{w.scrollTo(0,a.getBoundingClientRect().top-w.innerHeight/'
    '2)}catch(DOMException){w=window;w.scrollTo(0,a.getBoundingClientRect().top-w.innerHeight/2)}')
# """A JS script that applies the 'element-highlighted' animation."""
BLIP_SCRIPT = (
    'try{$("head").append("<style>@keyframes selhian{0%{outline: 0px outset transparent;}50%{outlin'
    'e: 10px outset yellow; background-color: yellow}100%{outline: 0px outset transparent;}} </styl'
    'e>");wp=window.top;b=arguments[0];for(var a=0;a<b.length;a++){var c=b[a];wp.scrollTo(0,c.getBo'
    'undingClientRect().top+wp.pageYOffset-wp.innerHeight/2),c.style.animationDuration="0.5s",c.sty'
    'le.animationName="",setTimeout(function(e){e.style.animationName="selhian"},10,c)}}catch(e){}')
# """Type annotation, referring to either a WebElement, or a list of them."""
ELEMENT_OR_LIST = Union[WebElement, List[WebElement]] # pylint: disable=E1126
ELEMENT_LIST = List[WebElement] # pylint: disable=E1126

def to_list(item) -> list:
    """Wraps the input into a list if it wasn't already one."""
    return item if isinstance(item, list) else [item]

def find_error_improver(func: Callable):
    """A decorator, gets the NoSuchElementException to actually tell you what the problem is."""
    def actually_helpful(self, selector, within=None):
        """Does a thing, and if it didn't work, tells you what was missing from where."""
        try:
            return func(self, selector, within)
        except NoSuchElementException:
            raise NoSuchElementException("Couldn't find selector '{0}' on page {1}".format(
                selector, self.current_url())) from None
    return actually_helpful

class Drivery:  # Don't give me that 'too many public methods' nonsense. pylint: disable=R0904
    """Because Module-Level-State is apparently a terrible idea, have a class singleton.
    Wraps a WebDriver instance, and does a bunch of other useful things."""
    def __init__(self, globs: dict):
        if globs is None: return    # Just to handle the CP thing declaration.
        # To aid in checking for Page Loaded Status, track the last link clicked.
        self.last_link = ''
        self.base_url = globs['base_url']
        self.locale = globs['locale']
        self.locale_url = self.base_url + self.locale
        self.auth = globs['auth']
        self.cn_mode = globs['cn_mode'] # yeah, but CP needs it apparently.
        # A workaround. Firefox gets suspicious when you hide a password in the url.
        if globs['browser'] == 'firefox':
            p = FirefoxProfile()
            p.set_preference('network.http.phishy-userpass-length', 255)
            self.driver = Firefox(p)
        # Chrome, too, just up and decided to stop supporting this one day.
        elif globs['browser'] == 'chrome':
            c = ChromeOptions()
            c.add_argument('--disable-blink-features=BlockCredentialedSubresources')
            self.driver = Chrome(chrome_options=c)
        else:
            self.driver = BROWSERS[globs['browser']]()
        self.driver.implicitly_wait(LONG_WAIT)
        self.driver.maximize_window()

    def set_wait(self, wait: int) -> None:
        """Set the driver's implicit waiting value and the LONG_WAIT value too."""
        global LONG_WAIT
        LONG_WAIT = wait
        self.driver.implicitly_wait(wait)

    def close(self) -> None:
        """The testing bit calls this at the end of each test. Clears the session."""
        self.driver.quit()

    ###Navigation Methods.###

    def splash_page(self) -> None:
        """Navigates to the Splash Page."""
        self.get(self.base_url + '/splash.html')

    def open_home_page(self) -> None:
        """Opens the Welcome Page. Shortcut method."""
        self.get(self.locale_url)

    def current_url(self) -> str:
        """Kind of a technicality. Returns the current url."""
        return self.driver.current_url

    def back(self) -> None:
        """The rule is, only the drivery module is allowed to invoke self.driver directly."""
        self.driver.back()

    def refresh(self) -> None:
        """It's The Rules"""
        self.driver.refresh()

    def page_title(self) -> str:
        """Gets the Page Title.        RULES."""
        return self.driver.title

    def get(self, url: str) -> None:
        """For whatever reason, there is no Basic Authentication that works across all browsers.
        This has workarounds for each. Ironically, only IE supports the correct method."""
        isie = isinstance(self.driver, Ie)
        if not isie and self.auth:
            url = re.sub('(https?://)', r'\1{0}:{1}@'.format(*self.auth), url)
        self.driver.get(url)
        if isie and self.auth:
            self.driver.switch_to.alert.authenticate(*self.auth)

    def close_window(self) -> None:
        """Closes the currently-focused window or tab. Try not to use this when only one is left."""
        self.driver.close()
        self.switch_to_window(0)

    def close_other_windows(self) -> None:
        """Closes all open tabs and windows except for the original one."""
        while len(self.driver.window_handles) != 1:
            self.switch_to_window(1)
            self.close_window()

    def current_scroll(self) -> int:
        """Returns the window's vertical scroll position as stated by javascript's window.scrollY"""
        return self.driver.execute_script('return window.scrollY;')

    def wait_for_page(self, url=None) -> None:
        """Holds up execution until the current page's url contains the Last Link value (or, if
        given, a custom url) and its document.readyState is 'complete'. A decent approximation?"""
        script = 'return document.readyState === "complete";'
        if url is None:
            url = self.last_link
        try:
            WebDriverWait(self.driver, LONG_WAIT).until(
                lambda _: url in self.current_url())
            WebDriverWait(self.driver, LONG_WAIT).until(
                lambda _: self.driver.execute_script(script))
        except TimeoutException:
            raise TimeoutException(
                'Timed out waiting for {0} to load.'.format(url)) from None

    def wait_until_present(self, selector: str) -> WebElement:
        """Holds up execution until the selectored elment is visibly present.
        Use this instead of quietly_find if the target is in the DOM, but hidden."""
        try:
            return WebDriverWait(self.driver, LONG_WAIT).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
        except TimeoutException:
            raise TimeoutException(
                'Timed out waiting for {0} to appear.'.format(selector)) from None

    def wait_until_gone(self, selector: str) -> WebElement:
        """Holds up execution until the selectored element is not visibly present.
        EC doesn't seem to support local searches, so be sure the selector is page-unique."""
        try:
            # The poll_freq value is not the wait-til-fail time. Apparently.
            self.driver.implicitly_wait(0.5)
            ret = WebDriverWait(self.driver, LONG_WAIT).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, selector)))
            self.driver.implicitly_wait(LONG_WAIT)
            return ret
        except TimeoutException:
            raise TimeoutException(
                'Timed out waiting for {0} to disappear.'.format(selector)) from None

    def wait_until(self, condition: Callable, desc: str) -> Any:
        """Holds up execution, repeatedly calling the given function until it returns truthy.
        The given condition lambda should have no inputs.
        desc should explain what the lambda does, as the contents can't really be examined."""
        try:
            return WebDriverWait(self.driver, LONG_WAIT).until(lambda _: condition())
        except TimeoutException:
            raise TimeoutException(
                'Timed out waiting for condition: {0}'.format(desc)) from None

    def switch_to_window(self, window: int) -> None:
        """Switch WebDriver's focus to the given open tab or window. Zero based indexing."""
        self.driver.switch_to.window(self.driver.window_handles[window])

    def switch_to_frame(self, selector: str) -> None:
        """Switches WebDriver's focus into the given iframe.
        Alternatively, set selector to a None to revert to the main window."""
        if selector is None:
            self.driver.switch_to.default_content()
        else:
            self.driver.switch_to.frame(self.flashy_find_element(selector))

    def fix_url(self, url: str) -> str:
        """Use this to remove that /content/asp/ stuff from URLs."""
        return re.sub(r'((/|^)\w\w)_(\w\w(/|$|.))', r'\1-\3',
                      (url or '').replace('/content/asp/', '/'), count=1)

    ###Some methods to shorten Element Manipulation/Verification.###

    def scroll_element(self, elle: WebElement) -> WebElement:
        """Scrolls a single element into view, it wouldn't make sense to do multiple."""
        self.driver.execute_script(SCROLL_SCRIPT, elle)
        return elle

    def blip_element(self, elle: ELEMENT_OR_LIST) -> ELEMENT_OR_LIST:
        """Scrolls (an) element(s) into view, and highlights (i)t(hem).
        Returns the found element(s) as well, just for chaining purposes."""
        # Kick off the highlight animation, list-wrapped for the sake of only writing one handler.
        self.driver.execute_script(BLIP_SCRIPT, to_list(elle))
        return elle

    def check_visible_quick(self, selector: str, within: WebElement = None) -> bool:
        """Check for an element without potentially spending a lot of time polling the DOM.
        Ususally used when asserting an element's absence, saves waiting the full timeout."""
        within = within or self.driver
        self.driver.implicitly_wait(SHORT_WAIT)
        elements = within.find_elements_by_css_selector(selector)
        self.driver.implicitly_wait(LONG_WAIT)
        return len(elements) != 0 and elements[0].is_displayed()

    def execute_mouse_over(self, element: WebElement) -> None:
        """Simulates the mouse moving into an element."""
        ActionChains(self.driver).move_to_element(element).perform()

    def override_click(self, element: WebElement) -> None:
        """Use this if the thing you want to click is ''""'behind''"'" something else."""
        ActionChains(self.driver).move_to_element(element).click().perform()

    @find_error_improver
    def quietly_find_element(self, selector: str, within: WebElement = None) -> WebElement:
        """Finds a single element matching a CSS selector, optionally within a given element."""
        within = within or self.driver
        return within.find_element_by_css_selector(selector)

    @find_error_improver
    def quietly_find_elements(self, selector: str, within: WebElement = None) -> ELEMENT_LIST:
        """Finds multiple elements that match a CSS selector, optionally within a given element."""
        within = within or self.driver
        return to_list(within.find_elements_by_css_selector(selector))

    @find_error_improver
    def flashy_find_element(self, selector: str, within: WebElement = None) -> WebElement:
        """Finds a single element matching a CSS selector, highlights it as well."""
        within = within or self.driver
        return self.blip_element(within.find_element_by_css_selector(selector))

    @find_error_improver
    def flashy_find_elements(self, selector: str, within: WebElement = None) -> ELEMENT_LIST:
        """Finds multiple elements that match a CSS selector, highlights them as well.

        The browser-provided webdriver self.driver implementations seem to not return a
        list when only one element matches, so fixing that here."""
        within = within or self.driver
        return self.blip_element(to_list(within.find_elements_by_css_selector(selector)))

    @find_error_improver
    def find_visible_element(self, selector: str, within: WebElement = None) -> WebElement:
        """Given a selector that could match multiple different elements,
        return the one that is currently visible, not the first one that matches."""
        within = within or self.driver
        return self.blip_element([x for x in within.find_elements_by_css_selector(selector)
                                  if x.is_displayed()][0])

    def get_parent_element(self, element: WebElement) -> WebElement:
        """Gets the immediate parent of the given element."""
        return element.find_element_by_xpath('..')

    def bring_to_front(self, element: WebElement) -> WebElement:
        """Uses a JS to ensure the selected element is at the front.
        Usually in order to properly click() it."""
        self.driver.execute_script('arguments[0].style.zIndex = "10000";', element)

    def execute_script(self, script: str, *args) -> Any:
        """Executes a javascript snippet, returning what the script returns."""
        return self.driver.execute_script(script, *args)

class Email:
    """Handler for the email checks. Due to languages, there's really no way to tell
    which email is which, so to ensure schedule synchronicity, make sure
    get_new_messages is called every time an email is expected."""
    def __init__(self, globs: dict, dr: Drivery, userid: str):
        self.email = globs['email'].format(userid)
        self.cn_mode, self.imapsvr, self.usern, self.passw, self.froms = (
            globs['cn_mode'], globs['test_email_imap_server'], globs['test_email_username'],
            globs['test_email_password'], globs['asp_from_emails'])
        self.dr = dr

    def get_all_locales(self) -> Set[str]:     # pylint: disable=E1126
        """Collects all of the emails received by this email subaddress,
        and returns a set of Locale codes representing each one found."""
        locs = set()
        ems = [bs4.BeautifulSoup(x, 'html.parser')
               for x in self.get_new_messages(really_get_new=False)]
        for ema in ems:
            if self.cn_mode:    # China does not have locale-tagged links.
                links = ema.select('a[href*="t.dpc.rimanggis.com"]')
                hrefs = {x['href'].split('.')[-1] for x in links}
                locs = locs.union({'zh-cn'} if hrefs == {'json'} else hrefs)
            else:
                links = ema.select('a[href*="t.campaign.adobe.com"]')
                hrefs = [re.search(r'p1\=\w\w((-|_)\w\w)?', x['href']) for x in links]
                locs = locs.union({x.group().split('=')[-1] for x in hrefs if x})
        return locs

    def get_new_messages(self, really_get_new: bool = True) -> List[str]: # pylint: disable=E1126
        """Polls the IMAP server untill a (maybe) new email(s) are found, then
        attempts to make sense of their ridiculous transmission formatting."""
        results = []
        with imaplib.IMAP4_SSL(self.imapsvr) as imap:
            imap.login(self.usern, self.passw)
            imap.select()
            nums = self.dr.wait_until(lambda: self.email_loop(imap, really_get_new),
                                      'Waiting for emails to be found, calls self.email_loop.')
            # The Latin Character Set emails have two parts, the second of which is the html part.
            got, ems = imap.fetch(nums, 'body[2]')
            if got == 'NO':    # The others do not have two parts.
                got, ems = imap.fetch(nums, 'body[1]')
            for ema in ems:     # Yeah, the results come back wierd sometimes,
                if isinstance(ema, tuple):  # have to filter out the bits.
                    try:
                        results.append(quopri.decodestring(ema[1]).decode())
                    except UnicodeDecodeError:    # Some quasi-latin languages are different
                        results.append(quopri.decodestring(ema[1]).decode(LATIN_EMAIL_ENCODING))
        return results

    def email_loop(self, imap: imaplib.IMAP4_SSL, really_get_new: bool = True) -> bytes:
        """SEARCHes the server, checking for (maybe) new email. Put this in a wait-until loop."""
        imap.noop()
        # Returns a tuple. (Result_code, Actual_results). Actual_results is also a list.
        # Containing a single bytestring of space-separated return values.
        # And IMAP requires that imput values be comma separated.         Because why not.
        return b','.join(imap.search(     # Search from all addresses, it could be any of them.
            None, ' OR FROM '.join(['', *self.froms[:-1]]).strip(), 'FROM', self.froms[-1],
            'TO', self.email, 'UNSEEN' if really_get_new else 'SEEN')[1][0].split(b' '))

    class LocalizedEmail():    # Oh, whatever. pylint: disable=R0903
        """Superclass for the various emails."""
        def __init__(self, globs: dict, dr: Drivery, userid: str):
            self.email = bs4.BeautifulSoup(
                Email(globs, dr, userid).get_new_messages()[0], 'html.parser')
            self.userid = userid
            self.cn_mode = globs['cn_mode']

    class RegistrationEmail(LocalizedEmail):    # pylint: disable=R0903
        """Represents the Registration Email, if used correctly. Correctly here meaning:
        instantiate this shortly after registering, and be sure to attach it to
        an email sub-address with no existing unread messages."""
        def activation_link(self) -> str:
            """Returns the address of the Click Here To Activate Your Account link."""
            if self.cn_mode:    # China does not have that format of link.
                return self.email.a['href']
            return self.email.select('a[href*="activation"]')[0]['href']

    class ForgottenUsernameEmail(LocalizedEmail):    # pylint: disable=R0903
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
