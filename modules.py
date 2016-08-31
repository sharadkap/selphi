"""Automated testing of the Modules"""
import os
import time
from typing import Union, List
import argparse
from multiprocessing import cpu_count
from multiprocessing.pool import Pool
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import Chrome, Firefox, Ie, Safari, Opera, Edge
from selenium.webdriver.remote.command import Command
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from modulescripts import LANGS, LANGS_D, MODULES, MODULES_D, MODULES_C, SCRIPTS, USERS

RESET_MODULE = 'cpCmndGotoSlide=0'
MINIWAIT = 0.5
LIST_STR = List[str]	# pylint: disable-msg=E1126

def do_module(driver: WebDriver, module: str) -> None:
	"""Run this one if this is being imported as part of the Reg tests.
	Be sure to have already navigated to the module page, pass in the driver
	to be used, tell it which module this is and stand back. Names are:
	1, 2, 3, act, qld, nsw, nt, sa, tas, vic, wa, aboriginal, golf, lodges, ra, walks, wine"""
	global DRIVER	# pylint: disable-msg=W0601
	DRIVER = driver
	for elem in SCRIPTS[module]:
		domo(elem)

def parseargs():
	"""Do this bit separately so it can be copied into the new processes."""
	# pylint: disable-msg=W0601
	global IMPLICITLY_WAIT, TIME_FORMAT, MOD_STEM_D, MOD_STEM, \
		MOD_STEM_C, MOD_STEM_C_D, SCREENSHOT_DIR, RESULTS_FILE
	IMPLICITLY_WAIT = ARGS.wait[0]
	TIME_FORMAT = ' '.join(ARGS.timeformat)
	MOD_STEM_D = '{0}/content/asp/captivate/{{0}}_{{1}}/index.html'.format(ARGS.environment[0])
	MOD_STEM = '{0}/{{0}}/secure/training/training-summary/{{1}}.html' \
		.format(ARGS.environment[0])
	MOD_STEM_C_D = '{0}/content/sites/asp-{{0}}/resources/en/{{1}}/\
		assets/asset/{{3}}_{{2}}.zip/output/index_SCORM.html'.format(ARGS.chenvironment[0])
	MOD_STEM_C = '{0}/content/sites/asp-{{0}}/en/assignments.resource.html/\
		content/sites/asp-{{0}}/resources/en/{{1}}'.format(ARGS.chenvironment[0])
	SCREENSHOT_DIR = os.path.join(os.path.split(__file__)[0], 'module_screenshots')
	RESULTS_FILE = os.path.join(SCREENSHOT_DIR, 'module_results.csv')

def main() -> None:
	"""Run this if the modules suite is being executed as itself."""
	# pylint: disable-msg=W0601
	global ARGS, BROWSERS
	BROWSERS = {'chrome': Chrome, 'firefox': Firefox, 'ie': Ie, 'safari': Safari, \
		'opera': Opera, 'edge': Edge}
	# pylint: disable-msg=C0103
	PARSER = argparse.ArgumentParser()
	PARSER.add_argument('-e', '--environment', help='Which environment to test in. \
	Format: the website domain and protocol code (https thing). If the server requires authentication \
	, include it like "https://username:password@server.domain.com". Default is %(default)s.', \
	nargs=1, type=str, default=['https://prod.aussiespecialist.com'], metavar='')
	PARSER.add_argument('-ce', '--chenvironment', help='Which environment to test in if using China. \
	Format: the website domain and protocol code (https thing). Default is %(default)s.', \
	nargs=1, type=str, default=['https://www.aussiespecialist.cn'], metavar='')
	PARSER.add_argument('-m', '--modules', help='Which modules to test. One or more of [%(choices)s]. \
	Default is all.', nargs='+', type=str, choices=MODULES.keys(), metavar='', \
	default=list(MODULES.keys()))
	PARSER.add_argument('-l', '--locales', help='Which locales to test. One or more of [%(choices)s]. \
	Default is all.', nargs='+', type=str, choices=LANGS.keys(), metavar='', \
	default=list(LANGS.keys()))
	PARSER.add_argument('-b', '--browsers', help='Which browser to use. One or more of [%(choices)s]. \
	Default is %(default)s', nargs='+', default=['chrome'], choices=BROWSERS.keys(), metavar='')
	PARSER.add_argument('-d', '--direct', help=os.linesep+'Access the modules Directly.', \
	action='store_true')
	PARSER.add_argument('-w', '--wait', help='Wait this many seconds before deciding \
	an element is missing. Default is %(default)s', default=[20], type=int, nargs=1)
	PARSER.add_argument('-tf', '--timeformat', help='The format to use for writing timestamps. \
	See https://docs.python.org/3/library/time.html#time.strftime for full formatting info. \
	Default is %(default)s', default=['%Y/%m/%d %H:%M'], nargs='+', type=str)
	PARSER.add_argument('-s', '--scorm', help='Force SCORM MODE. Causes the url scheme to use \
	the complex scform, even for non China locales.', action='store_true')
	ARGS = PARSER.parse_args()
	parseargs()
	os.makedirs(SCREENSHOT_DIR, exist_ok=True)

	try:
		full_languages_modules_run(modfilter=ARGS.modules, langfilter=ARGS.locales, brows=ARGS.browsers)
	except Exception:	# Too general is the point, it's a Final Action. pylint: disable-msg=W0703
		with open(RESULTS_FILE, mode='a', encoding='UTF-8') as log:
				log.write('\n"Well, something went wrong. A manual exit, hopefully."')
		raise

def restart_driver(br):
	"""Restarts the DRIVER."""
	global DRIVER
	DRIVER = br()
	DRIVER.implicitly_wait(IMPLICITLY_WAIT)
	DRIVER.maximize_window()

def new_drag_drop(source: str, target: str) -> None:
	"""Like the ActionChains drag and drop,
	but updates the mouse position just after mousedown."""
	# Command.MOVE_TO, desite taking a css id string, does not actually perform a DOM lookup.
	def getid(loc):
		"""Interpret whether input is a locator or a series or alternate locators."""
		if isinstance(loc, str):
			try:
				return DRIVER.find_element_by_id(loc)
			except NoSuchElementException:
				raise NoSuchElementException("Didn't find {0}".format(loc)) from None
		elif isinstance(loc, list):
			return pick_from_possibilities(loc)
		else:
			raise TypeError('You broke it. String, or List only.')
	# IE WHY.
	source,	target = getid(source), getid(target)
	DRIVER.execute_script('a=arguments,h=[a[0],a[1]].map(function(x){return x.getBoundingClientRect() \
		.top;}),wp=window.top;wp.scrollTo(0, (h[0]+h[1])/2 - wp.innerHeight/2)', source, target)
	DRIVER.execute(Command.MOVE_TO, {'element': source.id})
	DRIVER.execute(Command.MOUSE_DOWN, {})
	DRIVER.execute(Command.MOVE_TO, {'xoffset': int(1), 'yoffset': int(1)})
	DRIVER.execute(Command.MOVE_TO, {'element': target.id})
	DRIVER.execute(Command.MOUSE_UP, {})
	time.sleep(MINIWAIT)

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

def click_surely(ele: WebElement) -> None:
	"""When clicking on an element, move it onscreen first. BECAUSE IE.
	If that doesn't work, manual override, it was probably just behind a blank textbox."""
	try:
		DRIVER.execute_script('wp=window.top;wp.scrollTo(0,arguments[0].\
		getBoundingClientRect().top + wp.innerHeight/2)', ele)
		ele.click()
	except WebDriverException:
		DRIVER.execute(Command.MOVE_TO, {'element': ele.id})
		DRIVER.execute(Command.CLICK)

def pick_from_possibilities(locator: str) -> WebElement:
	"""Deal with alternate ids. Use a css selector to get any proposed elements."""
	eles = [e for e in DRIVER.find_elements_by_css_selector("#" + ",#".join(locator))\
	 	if e.is_displayed()]
	if len(eles) == 0:
		raise NoSuchElementException("Didn't find {0}".format(locator))
	return eles[0]

def full_languages_modules_run(langfilter: LIST_STR, modfilter: LIST_STR, brows: LIST_STR) -> None:
	"""Run the selected set of modules and locales, logging results,
	and saving a screenshot in case of failure.	By default, will run all of them."""
	if ARGS.direct:
		ctem = MOD_STEM_C_D
		stem = MOD_STEM_D
		mods = MODULES_D
		langs = LANGS_D
	else:
		ctem = MOD_STEM_C
		stem = MOD_STEM
		mods = MODULES
		langs = LANGS
	output = '\n"START: {0}", {1}\n'.format(get_time(), ','.join(modfilter).upper())	# header row.
	pool = Pool(cpu_count() * 2)
	results = pool.map(do_locale, [(x, langs, ctem, stem, mods, modfilter, b, \
		BROWSERS[b], ARGS) for x in langfilter for b in brows])
	output += '\n'.join(results)	# Each locale's row.
	output += '\n"FINISH: {0}"\n\n'.format(get_time())	# Footer row.

	try:
		with open(RESULTS_FILE, mode='a', encoding='UTF-8') as log:
			log.write(output)
	except PermissionError:
		print('In future, be sure to not leave the log file open.')
		print('That tends to lock it, so now it cannot be written to.')
		print('\n\nNow, you have to try to read raw CSV from a console:\n\n')
		print(output)


def do_locale(args):
	"""The target of a process, go do all the modules in a locale."""
	global ARGS
	# Unpack arguments
	lang, langs, ctem, stem, mods, modfilter, brname, browser, ARGS = args
	parseargs()
	# Reset the driver between rounds
	restart_driver(browser)
	# Start recording results.
	result = '_'.join([lang.upper(), brname.upper()])
	# China is different, of course, of course, watch out for these checks below.
	scorm = (lang == 'cn' or ARGS.scorm)
	for mod in modfilter:
		try:
			# Try to do the module
			if scorm:	# Scorm den.
				DRIVER.get(ctem.format(langs[lang].replace('_', '-'), MODULES_C[mod][0], MODULES_C[mod][1], \
					langs[lang]))
			else:
				DRIVER.get(stem.format(langs[lang], mods[mod]))
			log_in_first(lang, scorm)
			for elem in SCRIPTS[mod]:
				domo(elem)
			result += ',"{0}: PASS"'.format(get_time())
		# Something goes wrong, document it and go to the next module.
		except WebDriverException as ex:
			result += ',"{0}: FAIL: {1}"'.format(get_time(), str(ex).replace('"', '""'))
			draw_failure(lang, mod)
	DRIVER.quit()
	return result

def switch_into_module(driver: WebDriver, cnmode: bool=False) -> None:
	"""Extract the Enter Iframe function just so it can be better exported."""
	if cnmode:	# Scorm's wrapper on the modules needs to be opened first.
		driver.find_element_by_css_selector('.scf-play-button').click()
	iframe = driver.find_element_by_css_selector('iframe[src^="/content/"]')
	driver.switch_to.frame(iframe)
	if cnmode:	# Scorm has TWO layers of framing.
		iframe = driver.find_element_by_css_selector('frame#ScormContent')
		driver.switch_to.frame(iframe)

def log_in_first(lang: str, cnmode: bool=False) -> None:
	"""If testing with login, first, have to go and log in and everything.
	As it happens, restarting the module will also fix the Loading Forever bug."""
	# There's an error in China if you view them directly.
	if ARGS.direct and cnmode:
		try:
			WebDriverWait(DRIVER, timeout=IMPLICITLY_WAIT).until(EC.alert_is_present())
			DRIVER.switch_to.alert.dismiss()
		except TimeoutError:
			print('The Direct View error message didn\'t appear, guess they fixed it?')
	if not ARGS.direct:
		DRIVER.implicitly_wait(MINIWAIT)
		if len(DRIVER.find_elements_by_id('link-logout')) == 0:
			try:
				DRIVER.find_element_by_css_selector('.link-signin-text').click()
				DRIVER.find_element_by_id('j_username').send_keys(USERS[lang])
				DRIVER.find_element_by_css_selector('[name="j_password"]').send_keys('Welcome1')
				DRIVER.find_element_by_id('usersignin').click()
			except NoSuchElementException:
				raise NoSuchElementException('Login failed, something was missing from the login panel.') from None
		DRIVER.implicitly_wait(IMPLICITLY_WAIT)
		try:
			switch_into_module(DRIVER, cnmode)
		except NoSuchElementException:
			raise NoSuchElementException('The module framing is missing something here, look into that.') from None
	# Make sure the module is loaded first. Harder than it looks.
	# First, make sure that something is in the DOM,
	try:
		check = DRIVER.find_element_by_css_selector('[id^="Text_Caption_"]')
	except NoSuchElementException:
		raise NoSuchElementException('Failed to locate initial element. Module may be entirely broken, may have just timed out.') from None
	# Then, wait until it is actually drawn to the screen.
	try:
		WebDriverWait(DRIVER, timeout=IMPLICITLY_WAIT)\
			.until(EC.visibility_of(check))
		# Then, wait until the loading overlay is gone.
		WebDriverWait(DRIVER, timeout=IMPLICITLY_WAIT)\
			.until_not(EC.visibility_of_element_located((By.ID, 'preloaderImage')))
	except TimeoutError:
		raise TimeoutError('Timed out waiting for the module to finish initial loading.') from None
	# THEN, you can run the script that compensates for the loading screen breaking.
	# Or a module being previously completed.
	DRIVER.execute_script(RESET_MODULE)

def get_time() -> str:
	"""Get the time, and formatted as well."""
	return time.strftime(TIME_FORMAT)

def draw_failure(lang: str, mod: str) -> None:
	"""Take a screenshot, save it to the screenshot folder."""
	dirname = os.path.join(SCREENSHOT_DIR, mod)
	filename = dirname + r"\{}.png".format(lang.split('/')[0])
	os.makedirs(dirname, exist_ok=True)
	imgdata = DRIVER.get_screenshot_as_png()
	with open(filename, mode='wb') as fil:
		fil.write(imgdata)

if __name__ == '__main__':
	main()
