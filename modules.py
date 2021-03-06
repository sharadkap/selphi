"""Automated testing of the Modules"""
import os
import re
import time
import signal
from typing import Union, List
import argparse
from multiprocessing import cpu_count
from multiprocessing.pool import Pool
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import (Chrome, Firefox, Ie, Safari, Opera, Edge,
                                FirefoxProfile, ActionChains)
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from modulescripts import (LANGS, MODULES, SCRIPTS, USER, PASSWORD, ENV, AUTH, TIMEFORMAT, DEBUG)

RESET_MODULE = 'cpCmndGotoSlide=0'
MINIWAIT = 0.5
LIST_STR = List[str]    # pylint: disable=E1126

def do_module(driver: WebDriver, module: str) -> None:
    """Run this one if this is being imported as part of the Reg tests.
    Be sure to have already navigated to the module page, pass in the driver
    to be used, tell it which module this is and stand back. Names are: mod1, mod2, mod3,
    act, qld, nsw, nt, sa, tas, vic, wa, aboriginal, golf, lodges, ra, walks, wine"""
    global DRIVER    # pylint: disable=W0601
    DRIVER = driver
    for elem in SCRIPTS[module]:
        domo(elem)

def parseargs():
    """Do this bit separately so it can be copied into the new processes."""
    # pylint: disable=W0601
    global IMPLICITLY_WAIT, MOD_STEM, CMOD_STEM, SCREENSHOT_DIR, RESULTS_FILE
    IMPLICITLY_WAIT = ARGS.wait[0]
    SCREENSHOT_DIR = os.path.join(os.path.split(__file__)[0], 'module_screenshots')
    RESULTS_FILE = os.path.join(SCREENSHOT_DIR, 'module_results.csv')
    MOD_STEM = ('{0}/content/sites/asp/{{0}}/assignments.resource.html/content/sites/asp'
                '/resources/{{0}}/{{1}}'.format(ENV))
    CMOD_STEM = '{0}/content/sites/asp-zh-cn/en/assignments.resource.html/content/sites/asp-zh-cn/resources/en/{{1}}'.format(ENV)

def main() -> None:
    """Run this if the modules suite is being executed as itself."""
    # pylint: disable=W0601
    global ARGS, BROWSERS
    BROWSERS = {'chrome': Chrome, 'firefox': Firefox, 'ie': Ie,
                'safari': Safari, 'opera': Opera, 'edge': Edge}
    # pylint: disable=C0103
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-m', '--modules', help='Which modules to test. One or more of '
                        '[%(choices)s]. Default is all.', nargs='+', type=str,
                        choices=MODULES.keys(), metavar='', default=list(MODULES.keys()))
    PARSER.add_argument('-l', '--locales', help='Which locales to test. One or more of '
                        '[%(choices)s]. Default is all.', nargs='+', type=str,
                        choices=LANGS.keys(), metavar='', default=list(LANGS.keys()))
    PARSER.add_argument('-b', '--browsers', help='Which browser to use. One or more of '
                        '[%(choices)s]. Default is %(default)s', nargs='+', default=['chrome'],
                        choices=BROWSERS.keys(), metavar='')
    PARSER.add_argument('-w', '--wait', help='Wait this many seconds before deciding an element is '
                        'missing. Default is %(default)s', default=[20], type=int, nargs=1)
    ARGS = PARSER.parse_args()
    parseargs()
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    try:
        full_languages_modules_run(modfilter=ARGS.modules,
                                   langfilter=ARGS.locales, brows=ARGS.browsers)
    except Exception:    # Too general is the point, it's a Final Action. pylint: disable=W0703
        with open(RESULTS_FILE, mode='a', encoding='UTF-8') as log:
            log.write('\n"Well, something went wrong. A manual exit, hopefully:"\n\n' + tidy_error())
        raise

def full_languages_modules_run(langfilter: LIST_STR, modfilter: LIST_STR, brows: LIST_STR) -> None:
    """Run the selected set of modules and locales, logging results,
    and saving a screenshot in case of failure.    By default, will run all of them."""
    output = '\n"START: {0}", {1}\n'.format(get_time(), ','.join(modfilter).upper())   # header row.
    pool = Pool(cpu_count() * 2)
    try:
        asy = pool.map_async(do_locale, [(x, LANGS, MOD_STEM, CMOD_STEM, modfilter, b,
                                          BROWSERS[b], ARGS) for x in langfilter for b in brows])
        while True:
            if asy.ready():
                break
            time.sleep(1)   # Poolmapwaiting blocks KeyboardInterrupts, so don't do that.
    except KeyboardInterrupt:
        pool.terminate()
        raise
    results = asy.get()
    output += '\n'.join(results)    # Each locale's row.
    output += '\n"FINISH: {0}"\n\n'.format(get_time())    # Footer row.
    try:
        with open(RESULTS_FILE, mode='a', encoding='UTF-8') as log:
            log.write(output)
    except PermissionError:
        print('In future, be sure to not leave the log file open.')
        print('That tends to lock it, so now it cannot be written to.')
        print('\n\nNow, you have to try to read raw CSV from a console:\n\n')
        print(output)

def restart_driver(br):
    """Restarts the DRIVER."""
    # Global not defined at module level. Well, whatever. pylint: disable=W0601
    global DRIVER
    if br == Firefox:   # And, a workaround for Firefox's distrust of basic authentication.
        p = FirefoxProfile()
        p.set_preference('network.http.phishy-userpass-length', 255)
        DRIVER = Firefox(p)
    elif br == Chrome:  # Now Chrome doesn't trust it either, bleh.
        c = ChromeOptions()
        c.add_argument('--disable-blink-features=BlockCredentialedSubresources')
        DRIVER = Chrome(chrome_options=c)
    else:
        DRIVER = br()
    DRIVER.implicitly_wait(IMPLICITLY_WAIT)
    DRIVER.maximize_window()

def do_locale(args):
    """The target of a process, go do all the modules in a locale."""
    # Global can't be defined at module level. Processes are wierd. pylint: disable=W0601
    global ARGS
    signal.signal(signal.SIGINT, signal.SIG_IGN)    # Set the workers to ignore KeyboardInterrupts.
    # Unpack arguments
    lang, langs, stem, cstem, modfilter, brname, browser, ARGS = args
    parseargs()
    # A Hack. CN has a different structure, so use a different url form.
    if lang == 'cn':
        stem = cstem
    # Reset the driver between rounds
    restart_driver(browser)
    # Log into the site, so you can access the modules.
    try:
        log_in(lang)
    except Exception:
        DRIVER.quit()
        return '"Login to {0} failed. That breaks the whole locale, look into it:\n{1}"'.format(
            lang, tidy_error().replace('"', '""'))

    # Start recording results.
    result = '_'.join([lang.upper(), brname.upper()])
    for mod in modfilter:
        try:
            # Figure out the locale coding.
            url = stem.format(langs[lang][0].replace('-', '_'), MODULES[mod][lang])
            DRIVER.get(url)
            begin_module()
            # Try to do the module
            for elem in SCRIPTS[mod]:
                domo(elem)
            result += ',"{0}: PASS"'.format(get_time())
        # Something goes wrong, document it and go to the next module.
        except Exception:
            result += ',"{0}: FAIL: {1}"'.format(get_time(), tidy_error().replace('"', '""'))
            draw_failure(lang, mod)
    DRIVER.quit()
    return result

def log_in(lang: str) -> None:
    """If testing with login, first, have to go and log in and everything.
    Log in to ASP and to the server auth."""
    url = '{0}/{1}'.format(ENV, LANGS[lang][0])
    # Deal with Basic Server Authentication
    isie = isinstance(DRIVER, Ie)
    # Chrome and Firefox know how to use http headers.
    if not isie and AUTH:
        url = re.sub('(https?://)', r'\1{0}:{1}@'.format(*AUTH), url)
    # IE knows how to write to popups.
    if isie and AUTH:
        try:
            DRIVER.switch_to.alert.authenticate(*AUTH)
        except WebDriverException:  # If you're already logged in, never mind.
            pass
    DRIVER.get(url)
    # Try to log in
    try:
        DRIVER.find_element_by_css_selector('.link-signin-text').click()
        DRIVER.find_element_by_id('j_username').send_keys(USER)
        DRIVER.find_element_by_css_selector('[name="j_password"]').send_keys(PASSWORD)
        DRIVER.find_element_by_id('usersignin').click()
        WebDriverWait(DRIVER, IMPLICITLY_WAIT).until(lambda _: '/secure' in DRIVER.current_url)
    except NoSuchElementException as ex:
        raise NoSuchElementException('Login failed, something was missing from the '
                                     'login panel.\n\n' + ex.msg) from None

def begin_module():
    """Switch into the module frame, wait for it to load, and reset the module.
    As it happens, restarting the module will also fix the Loading Forever bug."""
    try:
        switch_into_module(DRIVER)
    except NoSuchElementException as ex:
        raise NoSuchElementException('The module framing is missing something here, '
                                     'look into that.' + ex.msg) from None
    # Make sure the module is loaded first. Harder than it looks.
    # First, make sure that something is in the DOM,
    try:
        check = DRIVER.find_element_by_css_selector('[id^="Text_Caption_"]')
    except NoSuchElementException:
        raise NoSuchElementException(
            'Failed to locate initial element. Module may be entirely broken, '
            'may have just timed out.') from None
    # Then, wait until it is actually drawn to the screen.
    try:
        WebDriverWait(DRIVER, timeout=IMPLICITLY_WAIT).until(EC.visibility_of(check))
        # Then, wait until the loading overlay is gone.
        WebDriverWait(DRIVER, timeout=IMPLICITLY_WAIT).until_not(
            EC.visibility_of_element_located((By.ID, 'preloaderImage')))
    except TimeoutError:
        raise TimeoutError('Timed out waiting for the module to finish initial loading.') from None
    # THEN, you can run the script that compensates for the loading screen breaking.
    # Or a module being previously completed.
    DRIVER.execute_script(RESET_MODULE)

def switch_into_module(driver: WebDriver) -> None:
    """Extract the Enter Iframe function just so it can be better exported."""
    # Scorm's wrapper on the modules needs to be opened first.
    click_surely(driver.find_element_by_css_selector('.scf-play-button'), False)
    iframe = driver.find_element_by_css_selector('iframe[src^="/content/"]')
    driver.switch_to.frame(iframe)
    # Scorm has TWO layers of framing.
    iframe = driver.find_element_by_css_selector('frame#ScormContent')
    driver.switch_to.frame(iframe)

def domo(locator: Union[str, tuple, list]) -> None:
    """If locator is a string, clicks on the element with that as an id
    if locator is a tuple, drags the first element to the second one.
    if a list, looks for each of the elements listed, clicks the first one that exists."""
    if isinstance(locator, str):
        try:
            ele = DRIVER.find_element_by_id(locator)
        except NoSuchElementException:
            raise NoSuchElementException("Didn't find {0}".format(locator)) from None
        click_surely(ele)
    elif isinstance(locator, tuple):
        new_drag_drop(locator[0], locator[1])
    elif isinstance(locator, list):
        click_surely(pick_from_possibilities(locator))
    else:
        raise TypeError('You broke it. String, List, or Tuple only.')

def new_drag_drop(source: str, target: str) -> None:
    """Like the ActionChains drag and drop,
    but updates the mouse position just after mousedown."""
    # Command.MOVE_TO, desite taking a css id string, does not actually perform a DOM lookup.
    def getid(loc: str, frame: str='{}') -> WebElement:
        """Interpret whether input is a locator or a series or alternate locators.
        If there is a decorated clone, like in drag-drops, use frame to apply a format string."""
        if isinstance(loc, str):
            loc = frame.format(loc)
            try:
                return DRIVER.find_element_by_id(loc)
            except NoSuchElementException:
                raise NoSuchElementException("Didn't find {0}".format(loc)) from None
        elif isinstance(loc, list):
            loc = [frame.format(l) for l in loc]
            return pick_from_possibilities(loc)
        else:
            raise TypeError('You broke it. String, or List only.')
    # IE WHY.    FIREFOX, ET TU?
    source, fource, target = getid(source), getid(source, 're-{}c'), getid(target)
    # if not isinstance(DRIVER, Firefox):
    DRIVER.execute_script('a=arguments,h=[a[0],a[1]].map(function(x){return '
                          'x.getBoundingClientRect().top;}),wp=window.top;'
                          'wp.scrollTo(0,(h[0]+h[1])/2 - wp.innerHeight/2 + '
                          'wp.$("iframe[src*=\'/content/\']").offset().top)', source, target)
    ActionChains(DRIVER).click_and_hold(source).move_to_element(fource).release(target).perform()
    time.sleep(MINIWAIT)

def click_surely(ele: WebElement, inframe: bool=True) -> None:
    """When clicking on an element, move it onscreen first. BECAUSE IE.
    If that doesn't work, manual override, it was probably just behind a blank textbox."""
    try:
        sc = 'wp=window.top;wp.scrollTo(0,arguments[0].getBoundingClientRect().top-wp.innerHeight/2'
        if inframe:
            sc += '+wp.$("iframe[src*=\'/content/\']").offset().top'
        sc += ')'
        # if not isinstance(DRIVER, Firefox):
        DRIVER.execute_script(sc, ele)
        ele.click()
    except WebDriverException:
        ActionChains(DRIVER).move_to_element(ele).click().perform()

def pick_from_possibilities(locator: str) -> WebElement:
    """Deal with alternate ids. Use a css selector to get any proposed elements."""
    eles = [e for e in DRIVER.find_elements_by_css_selector("#" + ",#".join(locator))
            if e.is_displayed()]
    if len(eles) == 0:
        raise NoSuchElementException("Didn't find {0}".format(locator))
    return eles[0]

def get_time() -> str:
    """Get the time, and formatted as well."""
    return time.strftime(TIMEFORMAT)

def draw_failure(lang: str, mod: str) -> None:
    """Take a screenshot, save it to the screenshot folder."""
    dirname = os.path.join(SCREENSHOT_DIR, mod)
    filename = dirname + r"\{}.png".format(lang.split('/')[0])
    os.makedirs(dirname, exist_ok=True)
    imgdata = DRIVER.get_screenshot_as_png()
    with open(filename, mode='wb') as fil:
        fil.write(imgdata)

def tidy_error(ex=None) -> str:
    """Reads exception info from sys.exc_info and only shows the lines that are from MODULES.PY
    Unless DEBUG is True, in which case, it prints the enrirety of the trace.
    Don't use this like 'except Exception as ex: tidy_error(ex)', has to be the 3-tuple, exc_info-style."""
    from sys import exc_info
    from os.path import join, abspath, dirname
    from traceback import extract_tb, format_list, format_exception_only

    show = join(dirname(abspath(__file__)), '')

    def _check_file(name):
        return name and name.startswith(show)

    def _print(typ, value, tb):     # If not debug, generator expression: filter trace to my files.
        show = extract_tb(tb) if DEBUG else (fs for fs in extract_tb(tb, limit=3) if _check_file(fs.filename))
        fmt = format_list(show) + format_exception_only(typ, value)
        return ''.join((f.strip('"\'').replace('\\n', '') for f in fmt))

    args = ex or exc_info()
    return _print(*args)

if __name__ == '__main__':
    main()
