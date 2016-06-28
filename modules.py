"""Automated testing of the Modules"""
import os
import time
import argparse
from selenium.webdriver import Chrome, Firefox, Ie, Safari, Opera, Edge
from selenium.webdriver.remote.command import Command
from selenium.webdriver.remote.webdriver import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from modulescripts import LANGS, LANGS_D, MODULES, MODULES_D, SCRIPTS, USERS

BROWSERS = {'chrome': Chrome, 'firefox': Firefox, 'ie': Ie, 'safari': Safari, \
'opera': Opera, 'edge': Edge}
PARSER = argparse.ArgumentParser()
PARSER.add_argument('-m', '--modules', help='Which modules to test. One or more of [%(choices)s]. \
	Default is all.', nargs='+', type=str, choices=MODULES.keys(), metavar='')
PARSER.add_argument('-l', '--locales', help='Which locales to test. One or more of [%(choices)s]. \
	Default is all.', nargs='+', type=str, choices=LANGS.keys(), metavar='')
PARSER.add_argument('-b', '--browser', help='Which browser to use. One or more of [%(choices)s]. \
	Default is %(default)s', nargs=1, default='chrome', choices=BROWSERS.keys(), metavar='')
PARSER.add_argument('-d', '--direct', help=os.linesep+'Access the modules Directly.', \
	action='store_true')
ARGS = PARSER.parse_args()

MINIWAIT = 0.5
IMPLICITLY_WAIT = 15
DRIVER = BROWSERS[ARGS.browser]()
DRIVER.implicitly_wait(IMPLICITLY_WAIT)
DRIVER.maximize_window()
MOD_STEM_D = 'https://prod.aussiespecialist.com/content/asp/captivate/{0}_{1}/index.html'
MOD_STEM = 'https://prod.aussiespecialist.com/{0}/secure/training/training-summary/{1}.html'
SCREENSHOT_DIR = os.path.join(os.path.split(__file__)[0], 'module_screenshots')
RESULTS_FILE = os.path.join(SCREENSHOT_DIR, 'module_results.txt')
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
RESET_MODULE = 'cpCmndGotoSlide=0'

def new_drag_drop(source: str, target: str):
	"""Like the ActionChains drag and drop,
	but updates the mouse position just after mousedown."""
	# Command.MOVE_TO, desite taking a css id string, does not actually perform a DOM lookup.
	def getid(loc):
		"""Interpret whether input is a locator or a series or alternate locators."""
		if isinstance(loc, str):
			return DRIVER.find_element_by_id(loc).id
		elif isinstance(loc, list):
			return pick_from_possibilities(loc).id
		else:
			raise TypeError('You broke it. String, or List only.')
	source,	target = getid(source), getid(target)
	DRIVER.execute(Command.MOVE_TO, {'element': source})
	DRIVER.execute(Command.MOUSE_DOWN, {})
	DRIVER.execute(Command.MOVE_TO, {'xoffset': int(1), 'yoffset': int(1)})
	DRIVER.execute(Command.MOVE_TO, {'element': target})
	DRIVER.execute(Command.MOUSE_UP, {})
	time.sleep(MINIWAIT)

def domo(locator):
	"""If locator is a string, clicks on the element with that as an id
	if locator is a tuple, drags the first element to the second one.
	if a list, looks for each of the elements listed, clicks the first one that exists."""
	if isinstance(locator, str):
		ele = DRIVER.find_element_by_id(locator)
		click_surely(ele)
	elif isinstance(locator, tuple):
		new_drag_drop(locator[0], locator[1])
	elif isinstance(locator, list):
		click_surely(pick_from_possibilities(locator))
	else:
		raise TypeError('You broke it. String, List, or Tuple only.')

def click_surely(ele):
	"""Click on an element. If that doesn't work, click it again.
	But off to the side a bit, in case there was a slight overlap."""
	try:
		ele.click()
	except WebDriverException as ex:
		del ex
		DRIVER.execute(Command.MOVE_TO, {'element': ele.id, \
			'xoffset': ele.size['width']/4, 'yoffset': ele.size['height']/4})
		DRIVER.execute(Command.CLICK)

def pick_from_possibilities(locator):
	"""Deal with alternate ids. Use a css selector to get any proposed elements."""
	eles = DRIVER.find_elements_by_css_selector("#" + ",#".join(locator))
	return eles[0]

def full_languages_modules_run(langfilter=None, modfilter=None):
	"""Run the selected set of modules and locales, logging results,
	and saving a screenshot in case of failure.	By default, will run all of them."""
	if ARGS.direct:
		stem = MOD_STEM_D
		mods = MODULES_D
		langs = LANGS_D
	else:
		stem = MOD_STEM
		mods = MODULES
		langs = LANGS
	for lang in langfilter or langs.keys():
		# Logout between locales. Turns out, you can't delete PROD cookies while on WWW
		if not ARGS.direct:
			DRIVER.get(stem.split('{0}')[0])
			DRIVER.delete_all_cookies()
		for mod in modfilter or mods.keys():
			try:
				DRIVER.get(stem.format(langs[lang], mods[mod]))
				log_in_first(lang)
				if ARGS.direct:
					log_in_first(lang)
				for elem in SCRIPTS[mod]:
					domo(elem)
				with open(RESULTS_FILE, mode='a') as log:
					log.write('{2}: Module {0} in locale {1} passed without issue.\n'\
						.format(mod, lang, time.asctime()))
			except WebDriverException as ex:
				with open(RESULTS_FILE, mode='a') as log:
					log.write('\n{3}: Module {0} in Locale {1} failed because "{2}".\n'\
						.format(mod, lang, ex.msg, time.asctime()))
				dirname = os.path.join(SCREENSHOT_DIR, mod)
				filename = dirname + r"\{}.png".format(lang.split('/')[0])
				os.makedirs(dirname, exist_ok=True)
				imgdata = DRIVER.get_screenshot_as_png()
				with open(filename, mode='wb') as fil:
					fil.write(imgdata)

def log_in_first(lang):
	"""If testing with login, first, have to go and log in and everything.
	As it happens, restarting the module will also fix the Loading Forever bug."""
	if not ARGS.direct:
		DRIVER.implicitly_wait(MINIWAIT)
		if len(DRIVER.find_elements_by_id('link-logout')) == 0:
			DRIVER.find_element_by_css_selector('.link-signin-text').click()
			DRIVER.find_element_by_id('j_username').send_keys(USERS[lang])
			DRIVER.find_element_by_css_selector('[name="j_password"]').send_keys('Welcome1')
			DRIVER.find_element_by_id('usersignin').click()
		DRIVER.implicitly_wait(IMPLICITLY_WAIT)
		iframe = DRIVER.find_element_by_css_selector('iframe[src^="/content/"]')
		DRIVER.switch_to.frame(iframe)
	# Make sure the module is loaded first. Harder than it looks.
	# First, make sure that something is in the DOM,
	check = DRIVER.find_element_by_css_selector('[id^="Text_Caption_"]')
	# Then, wait until it is actually drawn to the screen.
	WebDriverWait(DRIVER, timeout=IMPLICITLY_WAIT)\
		.until(EC.visibility_of(check))
	# Then, wait until the loading overlay is gone.
	WebDriverWait(DRIVER, timeout=IMPLICITLY_WAIT)\
		.until_not(EC.visibility_of_element_located((By.ID, 'preloaderImage')))
	# THEN, you can run the script that compensates for the loading screen breaking.
	# Or a module being previously completed.
	DRIVER.execute_script(RESET_MODULE)

full_languages_modules_run(modfilter=ARGS.modules, langfilter=ARGS.locales)

# Do remember to do this.
DRIVER.quit()

raise EOFError("This is the end of the file.")
