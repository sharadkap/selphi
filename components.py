"""Implements classes wrapping the behaviour for finding and manipulating web elements."""

import re
import time
import json
import random
import hashlib
from types import MethodType
from typing import Set, List, Tuple
from selenium.webdriver.support.select import Select
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException
from drivery import Drivery, SHORT_WAIT

class WrappedElement:
    """Superclass for the various helper classes here."""
    # This is a placeholder, don't actually try this.
    element = WebElement(parent=None, id_=None)
    dr = Drivery(None)

    def click(self) -> 'WrappedElement':
        """Clicks on the element"""
        self.dr.last_link = self.dr.fix_url(self.element.get_attribute('href'))
        self.element.click()
        return self

    def ctrl_click(self) -> 'WrappedElement':
        """Control-clicks on the element"""
        self.dr.last_link = self.dr.fix_url(self.element.get_attribute('href'))
        self.element.ctrl_click()
        return self

    def override_click(self) -> 'WrappedElement':
        """Clicks on the element, even if it is "`'behind'`" another one"""
        self.dr.last_link = self.dr.fix_url(self.element.get_attribute('href'))
        self.dr.override_click(self.element)
        return self

    def point(self) -> 'WrappedElement':
        """Moves the mouse cursor over the element"""
        self.dr.execute_mouse_over(self.element)
        return self

    def is_displayed(self) -> bool:
        """Again, a bit of a formality. Checks whether the element is displayed"""
        return self.element.is_displayed()

    def __getattr__(self, name):
        """Basically just to stop pylint from complaining about dynamic attributes."""
        raise AttributeError('The {0} attribute does not exist on {1}.'.format(name, type(self)))

class MinorElement(WrappedElement):
    """Superclass for all the internally used minor elements; with no unique
    properties, initialised with a css selector instead of self-founding."""
    def __init__(self, dr: Drivery, selector: str, within: WrappedElement) -> None:
        self.dr = dr
        self.element = self.dr.flashy_find_element(selector, within)

class MinorElementParent(WrappedElement):
    """Subclass of the superclass, this one picks up the parent element of the given selector."""
    def __init__(self, dr: Drivery, selector: str, within: WrappedElement) -> None:
        self.dr = dr
        self.element = self.dr.blip_element(self.dr.get_parent_element(
            self.dr.quietly_find_element(selector, within)))

class Page(WrappedElement):
    """Represents the content of an entire page, sans the headers and footers"""
    def __init__(self, dr: Drivery):
        self.dr = dr
        self.element = self.dr.flashy_find_element('#main-content')

    def text(self) -> str:
        """Gets all the text on the page that isn\'t part of the template framing"""
        return self.element.text

class SplashSelect(WrappedElement):
    """Represents the Language Selector on the Splash Page."""
    def __init__(self, dr: Drivery):
        self.dr = dr
        self.element = self.dr.flashy_find_element('.dropdown-select-language1')

    # A Set of the full list of options that should be in the splash page language selector.
    locale_set = {'/en-gb.html', '/en-us.html', '/en-ca.html', '/en-in.html', '/en-my.html',
                  '/en-sg.html', '/id-id.html', '/de-de.html', '/zh-hk.html', '/en-hk.html',
                  '/zh-hk.html', '/en-hk.html', '/ja-jp.html', '/ko-kr.html', '/pt-br.html',
                  '/de-de.html', '/de-de.html', '/fr-fr.html', '/it-it.html', '/es-cl.html',
                  '/en.html', 'https://www.aussiespecialist.cn/zh-cn.html'}
    # A Set of the full list of options that should be in the splash page language selector.
    cn_locale_set = {'https://www.aussiespecialist.com/en-gb.html',
                     'https://www.aussiespecialist.com/en-us.html',
                     'https://www.aussiespecialist.com/en-ca.html',
                     'https://www.aussiespecialist.com/en-in.html',
                     'https://www.aussiespecialist.com/en-my.html',
                     'https://www.aussiespecialist.com/en-sg.html',
                     'https://www.aussiespecialist.com/id-id.html',
                     'https://www.aussiespecialist.com/de-de.html',
                     'https://www.aussiespecialist.com/zh-hk.html',
                     'https://www.aussiespecialist.com/en-hk.html',
                     'https://www.aussiespecialist.com/zh-hk.html',
                     'https://www.aussiespecialist.com/en-hk.html',
                     'https://www.aussiespecialist.com/ja-jp.html',
                     'https://www.aussiespecialist.com/ko-kr.html',
                     'https://www.aussiespecialist.com/pt-br.html',
                     'https://www.aussiespecialist.com/de-de.html',
                     'https://www.aussiespecialist.com/de-de.html',
                     'https://www.aussiespecialist.com/fr-fr.html',
                     'https://www.aussiespecialist.com/it-it.html',
                     'https://www.aussiespecialist.com/es-cl.html',
                     'https://www.aussiespecialist.com/en.html', '/zh-cn.html'}

    def get_values(self) -> Set[str]:
        """Gets a set containing the URLs of all the Language Options."""
        return {self.dr.fix_url(x.get_attribute('value'))
                for x in self.dr.quietly_find_elements('option:not([value="#"])', self.element)}

    def choose_locale(self) -> None:
        """Selects the Language Option representing the current locale."""
        option = self.dr.quietly_find_element(
            'option[value*="{0}"],option[value*="{1}"]'.format(
                self.dr.locale, self.dr.locale.replace('-', '_')), self.element)
        self.dr.last_link = option.get_attribute('value')
        option.click()

class WelcomeVideo(WrappedElement):
    """Represents the main Video on the home page."""
    def __init__(self, dr: Drivery):
        self.dr = dr
        self.element = self.dr.quietly_find_element('.hero')

    def play(self) -> None:
        """Clicks the video's Play button."""
        self.dr.quietly_find_element('.cts-icon-play', self.element).click()
        if self.dr.cn_mode:    # In China, you have to click it twice.
            self.dr.quietly_find_element('.vjs-poster', self.element).click()

    def is_playing(self) -> bool:
        """Checks whether the video is playing."""
        return self.dr.quietly_find_element('.vjs-play-control', self.element).is_displayed()

class Hero(WrappedElement):
    """Represents the Hero Banner of ASP pages, and its Add To Sales Tools button.
    Also represents the Common Hero banner, and its Pin It button. Try not to mix them up."""
    def __init__(self, dr: Drivery):
        self.dr = dr
        self.element = self.dr.flashy_find_element('.hero-video-copy')

    def add(self):
        """Clicks the Add To Sales Tools button, and waits until the animation is done."""
        self.dr.flashy_find_element('#favouriteComp', self.element).click()
        self.dr.wait_until_gone('.is-touched')

    def get_title(self) -> str:
        """Returns the page's title, as shown in the hero banner.
        Only returns the first line, otherwise Dated Events mess with the FAV test."""
        return self.dr.flashy_find_element('.home-hero-title', self.element).text.split('\n')[0]

    def pin_it(self) -> None:
        """Moves the mouse over the hero, triggering the Pin It button to appear, then clicks it"""
        self.point()
        self.dr.flashy_find_element('.social-pinterest--container.social-pinterest--visible',
                                    self.dr.get_parent_element(self.element)).click()

class Video(WrappedElement):
    """Generically represents either a Brightcove Video or a Youku video."""
    def __init__(self, dr: Drivery, which: int = None):
        self.dr = dr
        # Youku has a state holder in the window object, Brightcove loads along with the page.
        if which:
            self.element = self.dr.blip(
                self.dr.quietly_find_elements('.video-js,#youkuplayer')[which])
        else:
            self.element = self.dr.flashy_find_element('.video-js,#youkuplayer')
        self.dr.wait_until(lambda: self.dr.execute_script(
            'return window.YKP===undefined||window.YKP.playerCurrentState==="PLAYER_STATE_READY";'),
                           'Either YKP is undefined, or YKP state = PLAYER_STATE_READY')

    def play(self):
        """Starts up the video. Probably."""
        # This might be necessary, the Youku player is a little ahead of itself.
        def x(): """Maybe"""; self.override_click(); return self.is_playing()
        self.dr.wait_until(x, 'Click it and is it playing now?')

    def is_playing(self) -> bool:
        """Returns true is the video is playing, false if not. Approximately."""
        # Brightcove has a css class when playing, Youku has a js flag set.
        return ('vjs-playing' in self.element.get_attribute('class') or
                self.dr.execute_script(
                    'try{return window.YKP.playerCurrentState=="PLAYER_STATE_PLAYING"}catch(e){}'))

class BodyLoginButton(WrappedElement):
    """Represents the Sign In button that appears in a page's body content when signed out."""
    def __init__(self, dr: Drivery):
        self.dr = dr
        self.element = self.dr.flashy_find_element('#loginCompButton > div > .btn-primary.fancybox')

class BodyRegisterButton(WrappedElement):
    """Represents the Join The Program button that appears on all pages when signed out."""
    def __init__(self, dr: Drivery):
        self.dr = dr
        self.element = self.dr.flashy_find_element('#loginCompButton > div > a:nth-child(2)')

class WhatYouCanSeeMosaic(WrappedElement):
    """Represents the What You Can See Mosaic, however many tiles may appear."""
    def __init__(self, dr: Drivery, which: int = None):
        self.dr = dr
        if which:
            self.element = self.dr.blip_element(
                self.dr.quietly_find_elements('div.whatyoucansee div.mosaic')[which])
        else:
            self.element = self.dr.flashy_find_element('div.whatyoucansee div.mosaic')
        self.tiles = [x for x in self.dr.quietly_find_elements('.mosaic-item') if x.is_displayed()]

    def tile_count(self) -> int:
        """Returns the number of tiles in the mosaic."""
        return len(self.tiles)

    class MosaicTile(WrappedElement):
        """Represents a single Mosaic Tile, including its internal elements.
        Don't instantiate this from the test script directly, it needs a WebElement"""
        def __init__(self, dr: Drivery, element: WebElement):
            self.dr = dr
            self.element = self.dr.blip_element(element)
            self.contentpane = None

        def open(self) -> None:
            """Clicks on the mosaic tile, opening it.
            Panel contents is a bit of a mess though, have to account for responsive design."""
            self.dr.blip_element(self.element).click()
            self.contentpane = [x for x in self.dr.flashy_find_elements(
                '.mosaic-item-detail-container.active') if x.is_displayed()][0]

        def go(self) -> None:
            """Clicks on a tile, navigating to its link.
            Which of these two is correct is left as an exercise to the reader."""
            self.dr.last_link = self.dr.fix_url(self.dr.quietly_find_element(
                '.mosaic-item-detail-container p>a', self.element).get_attribute('href'))
            self.dr.blip_element(self.element).click()
            # External links open in a new tab. No problem if not.
            try:
                self.dr.switch_to_window(1)
            except IndexError:
                pass
            self.dr.wait_for_page()

        def get_title(self) -> str:
            """Returns the title text of a tile's content pane. Has to be open first."""
            return self.dr.flashy_find_element('.line-through-container-biline',
                                               self.contentpane).text

        def get_description(self) -> MinorElement:
            """Returns the description text in a tile's pane. Has to be open."""
            return MinorElement(self.dr, '.l-padding-tb-30-lr-15 p', self.contentpane)

        def get_link(self) -> MinorElement:
            """Returns the More Info link from a tiles pane. Has to be open."""
            return self.dr.quietly_find_element('a:not(.btn-bubble):not([href="#"])',
                                                self.contentpane).get_attribute('href')

        def add_to_favourites(self) -> None:
            """Clicks the Heart button in the tiles content. Has to be open first."""
            self.dr.flashy_find_element('.btn-bubble', self.contentpane).click()

    def random_selection(self, num: int) -> List['MosaicTile']:
        """Given a number, gets that many randomly selected tiles from the mosaic."""
        return [self.MosaicTile(self.dr, tile) for tile in random.sample(self.tiles, num)]

    def __len__(self) -> int:
        """Returns the number of tiles in the mosaic."""
        return len(self.tiles)

    def __getitem__(self, title) -> 'MosaicTile':
        """Select a particular tile by using its title in the [] index accessor. Maybe."""
        if isinstance(title, int):
            return self.MosaicTile(self.dr, self.tiles[title])
        return self.MosaicTile(self.dr, next(
            x for x in self.tiles
            if self.dr.quietly_find_element('.label-destination', x).text == title))

def attach_links(menu: WrappedElement, names: List[str],
                 selector: str = '[href*="{}.html"]') -> None:
    """A function that attaches an attribute that can be called to create a simple link.
    The 'names' arguments should be the bits that .format into the selector"""
    for name in names:
        # Watch out for that closure.
        def link_maker(n):
            """A function that can be called to create a simple link"""
            return lambda: MinorElement(menu.dr, selector.format(n), menu.element)
        menu.__setattr__(name.replace('-', '_').replace('.', '_'), link_maker(name))

def attach_fancy_links(menu: WrappedElement, names: List[str],
                       selector: str = 'a.mosaic-overlay[href*="{}.html"]') -> None:
    """Like attach_links, attaches an attribute that can be called to create a link.
    This one is for those Mosaic-type links, and those need a bit of a workaround
    to deal with element layering."""
    for name in names:
        def link_maker(n):
            """A function that can be called to create a fancy link."""
            return lambda: MinorElementParent(menu.dr, selector.format(n), menu.element)
        menu.__setattr__(name.replace('-', '_').replace('.', '_'), link_maker(name))

class NavSection(WrappedElement):
    """Methods common to the five Nav Menu sections."""
    def open(self) -> WrappedElement:
        """Opens the menu, whether that be by clicking or by pointing."""
        self.point()
        if self.element.get_attribute('class').find('is-open') == -1:
            self.click()
        return self

class NavMenu(WrappedElement):
    """Represents the main Nav Menu."""
    def __init__(self, dr: Drivery):
        self.dr = dr
        self.element = self.dr.flashy_find_element('.navigation')
        attach_links(self, ['profile', 'logout'], selector='#link-{}')
        attach_links(self, ['logo'], selector='.header-masthead a[class*={}-masthead]')
        attach_links(self, ['australia'], selector='[href*="www.australia.c"]')
        attach_links(self, ['investment'], selector='[href*="tourism{}.c"]')
        attach_links(self, ['businessevents'], selector='[href*="{}.australia.c"]')
        attach_links(self, ['corporate'], selector='[href*="www.tourism.australia.c"]')
        attach_links(self, ['current'], selector='li.is-{} a')    # blar. What a hack.
        attach_links(self, ['invcn'], selector='.l-center-1200>.nav-bar-left>li:nth-child(2)')

    # ASP ones.
    class About(NavSection):
        """Represents the About menu in the main nav menu."""
        def __init__(self, dr: Drivery):
            self.dr = dr
            self.element = self.dr.flashy_find_element('#nav-main-panel-1')
            attach_links(self, ['about', 'benefits', 'how-to-use-the-site',
                                'program-faq', 'contact-us'])

    class SalesResources(NavSection):
        """Represents the Sales Resources menu in the main nav menu."""
        def __init__(self, dr: Drivery):
            self.dr = dr
            self.element = self.dr.flashy_find_element('#nav-main-panel-2')
            attach_links(self, ['sales-resources', 'my-sales-tools', 'interactive-map',
                                'itineraries-search-and-feature', 'fact-sheets-overview', 'events',
                                'useful-sites', 'destination-faq', 'image-and-video-galleries'])

    class Training(NavSection):
        """Represents the Training menu in the main nav menu."""
        def __init__(self, dr: Drivery):
            self.dr = dr
            self.element = self.dr.flashy_find_element('#nav-main-panel-3')
            attach_links(self, ['training', 'webinars'])
            attach_links(self, ['training-summary'], '[href*="assignments.html"]') # ehhh, sure.

    class NewsAndProducts(NavSection):
        """Represents the News And Products menu in the main nav menu."""
        def __init__(self, dr: Drivery):
            self.dr = dr
            self.element = self.dr.flashy_find_element('#nav-main-panel-4')
            attach_links(self, ['news-and-product-updates', 'latest-news', 'product-videos'])

    class AussieSpecialistClub(NavSection):
        """Represents the Aussie Specialist Club menu in the main nav menu."""
        def __init__(self, dr: Drivery):
            self.dr = dr
            self.element = self.dr.flashy_find_element('#nav-main-panel-5')
            attach_links(self, ['aussie-specialist-club', 'travel-club', 'famils',
                                'aussie-specialist-photos', 'asp-logo', 'aussie-store'])

        @staticmethod
        def not_present(dr: Drivery) -> bool:
            """Checks that the Aussie Specialist Club menu is not present.
            As such, does not attempt to locate it, and is a static method."""
            return not dr.check_visible_quick('#nav-main-panel-5')

    # AUS.com ones. Also, the menu is built differently, the <a> tag itself is hidden.
    class PlacesToGo(NavSection):
        """Represents the Places To Go section in the nav menu.
        And the 必游胜地 one, they're the same here."""
        def __init__(self, dr: Drivery):
            self.dr = dr
            self.element = self.dr.flashy_find_element('#nav-main-panel-1')
            # This one is the thing that switched between the Cities and States submenus.
            attach_links(self, ['cities', 'states'], selector='[aria-controls={}]')
            attach_links(self, ['adelaide',
                                'alice-springs', 'broome', 'cairns', 'canberra', 'darwin',
                                'gold-coast', 'hobart', 'regional-cities',

                                'blue-mountains', 'byron-bay', 'flinders-ranges',
                                'fraser-island', 'freycinet', 'gippsland', 'kakadu',
                                'namadgi', 'ningaloo', 'tasmanian-wilderness',
                                'australian-alps', 'kimberley', 'margaret-river',

                                'act', 'nsw', 'nt', 'qld', 'sa', 'tas', 'vic', 'wa'],
                         selector='[href*="{0}.html"] p')
            attach_links(self, ['explore'])
            attach_fancy_links(self, ['sydney', 'melbourne', 'brisbane', 'perth', 'red-centre',
                                      'great-barrier-reef', 'great-ocean-road', 'kangaroo-island'])

    class ThingsToDo(NavSection):
        """Represents the Things To Do section in the nav menu."""
        def __init__(self, dr: Drivery):
            self.dr = dr
            self.element = self.dr.flashy_find_element('#nav-main-panel-2')
            attach_links(self, ['aquatic', 'nature-and-wildlife', 'food-and-wine',
                                'outback-australia', 'top-things-to-do',

                                'coastal-journeys', 'holiday-ideas', 'city-journeys',
                                '48-hours-itineraries', 'walking-australia', 'itineraries',

                                'campaigns', 'events', 'news', 'youthful-travellers',
                                'aboriginal-australia'],
                         selector='[href*="{0}.html"] p')
            attach_fancy_links(self, ['things-to-do', 'drive-australia', 'explore'])

    class PlanYourTrip(NavSection):
        """Represents the Plan Your Trip section in the nav menu."""
        def __init__(self, dr: Drivery):
            self.dr = dr
            self.element = self.dr.flashy_find_element('#nav-main-panel-3')
            attach_links(self, ['weather', 'australias-seasons', 'time-zones-in-australia',

                                'visa-information', 'getting-around', 'working-holiday-visa',
                                'customs-quarantine',

                                'find-accommodation', 'find-tours', 'explore'],
                         selector='[href*="{0}.html"] p')
            attach_fancy_links(self, ['facts', 'planning-a-trip', 'find-travel-agent'])

    # And, the AUS.cn last two are a bit different.
    class PracticalInformation(NavSection):
        """Represents the 实用信息 section in the nav menu. A combination of Facts and Planning?"""
        def __init__(self, dr: Drivery):
            self.dr = dr
            self.element = self.dr.flashy_find_element('#nav-main-panel-2')
            attach_links(self, ['australias-seasons', 'cities-states-territories',
                                'australias-animals', 'plants', 'currency', 'time-zones', 'facts'

                                'flight-information', 'planning-a-trip', 'getting-around',
                                'useful-tips', 'planning',

                                'work-study-abroad', 'customs-quarantine', 'healthy-safety'],
                         selector='[href*="{0}.html"] p')
            attach_fancy_links(self, ['weather', 'visa-information', 'embassy'])

    class ExploreAndPlan(NavSection):
        """Represents the 探索及计划行程 section in the nav menu.
        Things to do, Itineraries, Campaigns and some other miscellaniea."""
        def __init__(self, dr: Drivery):
            self.dr = dr
            self.element = self.dr.flashy_find_element('#nav-main-panel-3')
            attach_links(self, ['things-to-do', 'food-and-wine', 'nature-and-wildlife',
                                'aboriginal-australia', 'australian-sport', 'art-music-culture',
                                'outback-australia', 'youthful-travellers',

                                'drive-australia', 'coastal-journeys', '48-hours-itineraries',
                                'walking-australia', 'adventure-journeys', 'outback-journeys',
                                'aboriginal-discovery', 'nature-discovery',

                                'specialoffers', 'hertzselfdriving', 'download', 'follow-us'],
                         selector='[href*="{0}.html"] p')
            attach_fancy_links(self, ['aquatic', 'city-journeys', 'kdp'])

    # INV ones. ALso: gggggggh, no unique classes or ids.
    class WhyAustralia(NavSection):
        """Represents the Why Australia section in the nav menu."""
        def __init__(self, dr: Drivery):
            self.dr = dr
            self.element = self.dr.blip_element(dr.quietly_find_elements('.nav-panel-list-item')[0])
            attach_links(self, [
                'why-australia', 'resilient-growth-economy', 'easy-place-to-do-business',
                'globally-significant-tourism-industry', 'strong-performing-accommodation-sector',
                'aviation-access', 'world-class-tourism-offering', 'strong-events-calendar',
                'tourism-demand-strategy'], selector='[href*="{0}.html"] p')

    class InvestmentOpportunities(NavSection):
        """Represents the Investment Opportunities section in the nav menu."""
        def __init__(self, dr: Drivery):
            self.dr = dr
            self.element = self.dr.blip_element(dr.quietly_find_elements('.nav-panel-list-item')[1])
            attach_links(self, ['investment-opportunities', 'food-and-wine', 'beaches-and-islands',
                                'nature-and-outback', 'cities'], selector='[href*="{0}.html"] p')

    class DataRoom(NavSection):
        """Represents the Investment Opportunities section in the nav menu."""
        def __init__(self, dr: Drivery):
            self.dr = dr
            self.element = self.dr.blip_element(dr.quietly_find_elements('.nav-panel-list-item')[2])
            attach_links(self, ['data-room', 'tourism-performance', 'hotel-performance', 'aviation',
                                'the-markets', 'success-stories',], selector='[href*="{0}.html"] p')

    class AboutUs(NavSection):
        """Represents the About Us section in the nav menu."""
        def __init__(self, dr: Drivery):
            self.dr = dr
            self.element = self.dr.blip_element(dr.quietly_find_elements('.nav-panel-list-item')[3])
            attach_links(self, ['about-us', 'how-we-can-help', 'a-national-priority', 'contact-us',]
                         , selector='[href*="{0}.html"] p')

    def get_all_links(self) -> Set[str]:
        """Gets a set containing the href of each link in the nav menu.
        The Five/Four section panels, that is, not the Icons, or the Sign In thing."""
        return {self.dr.fix_url(x.get_attribute('href')) for x in self.dr.flashy_find_elements(
            '#nav-bar-top .nav-bar-left a[href]:not([href^="#"])', self.element)}

    def user_names(self) -> str:
        """Gets the text displayed in the corner that shows the user names.
        Totally unformatted, so just use the in() function rather than parsing."""
        return self.dr.flashy_find_element('.link-signin-text', self.element).text

class Footer(WrappedElement):
    """Represents the global Footer."""
    def __init__(self, dr: Drivery):
        self.dr = dr
        self.element = self.dr.flashy_find_element('#main-footer')
        attach_links(self, ['splash', 'sitemap', 'privacy-policy', 'terms-and-conditions',
                            'terms-of-use', 'contact-us', 'about-us', 'contact-us',
                            'terms-conditions'])
        attach_links(self, ['facebook', 'plus.google', 'youtube', 'twitter', 'instagram', 'weibo'],
                     selector='[href*="{}.com"]')
        attach_links(self, ['wechat'], selector='[href*="#qr_image"],[href*="#china_qr_image"]')
        attach_links(self, ['australia', 'businessevents.australia'],
                     selector='[href*="www.{}.cn"]')
        attach_links(self, ['australia', 'tourism.australia'], selector='[href*="www.{}.c"]')
        attach_links(self, ['businessevents.australia'], selector='[href*="{}.c"]')
        attach_links(self, ['austrade'], selector='[href*="www.{}.gov.au"]')

    def get_all_links(self) -> Set[str]:
        """Get a list of all of the links on the footer. Won't get the languages dropdown though."""
        return {li.get_attribute('href') for li in
                self.dr.flashy_find_elements('a', self.element) if li.is_displayed()}

    def get_locales(self) -> List[str]:
        """Get a list of the countries available to the footer switcher. '/en-ca.html' format."""
        return [opt.get_attribute('value') for opt in
                self.dr.quietly_find_elements('#dropdown-select-language option', self.element)]

    def pick_locale(self, locale):
        """Selects a value in the Country Selector in the footer. Formatted like /en-ca.html"""
        Select(self.dr.flashy_find_element('#dropdown-select-language', self.element)
              ).select_by_value(locale)

class Sitemap(WrappedElement):
    """Represents the Sitemap link cloud"""
    def __init__(self, dr: Drivery):
        self.dr = dr
        self.element = self.dr.flashy_find_element('.sitemap')
        attach_links(self, ['change', 'newsletter-unsubscribe', 'coming-soon'])

    def get_all_links(self) -> Set[str]:
        """Gets a set containing the href of each link in the Sitemap link section"""
        return {self.dr.fix_url(x.get_attribute('href'))
                for x in self.dr.flashy_find_elements('a', self.element)}

    def get_locales(self) -> Set[str]:
        """Gets a set of the link hrefs, specifically the locale ones, formatted like /en-ca.html"""
        return {'/' + self.dr.fix_url(x.get_attribute('href')).split('/')[-2] + '.html'
                for x in self.dr.flashy_find_elements('a[href*="sitemap.html"]', self.element)}

class FilteredSearch(WrappedElement):
    """Represents the Itinerary or Fact Sheet Search or Generic Filtered Search Components."""
    def __init__(self, dr: Drivery, pdf_mode: bool = False) -> None:
        self.dr = dr
        self.element = self.dr.flashy_find_element('.filteredSearch')
        self.pdf_mode = pdf_mode
        # Hold up, have to wait for the initial results to come in first,
        # they'll interrupt if they appear halfway through something else.
        self.dr.quietly_find_element('.mosaic-item,.filter001')

    class SearchResult(WrappedElement):
        """Represents a Result of a Filtered Search.
        Also handles the Contact Mode stuff, so be careful about which methods you call."""
        def __init__(self, dr: Drivery, which: WebElement):
            self.dr = dr
            self.element = which

        def get_title(self) -> str:
            """Gets the page Title/Name of the result"""
            return self.dr.flashy_find_element('.line-through-container', self.element).text

        def get_summary(self) -> str:
            """Gets the page Description/Summary of the result"""
            return self.dr.flashy_find_element('.mloverflow', self.element).text

        def view_more_information(self, newtab: bool = False) -> None:
            """Navigates to the result's main page, clicks the View More Info link"""
            link = self.dr.flashy_find_element('.search-results-copy-container a', self.element)
            href = self.dr.fix_url(link.get_attribute('href'))
            if newtab:
                link.ctrl_click()
                self.dr.switch_to_window(-1)
            else:
                link.click()
            self.dr.wait_for_page(href)

        def add_to_favourites(self) -> None:
            """Clicks the result's Heart Icon: Add To My Sales Tool Kit"""
            self.dr.flashy_find_element('a.btn-bubble', self.element).click()

        def download_pdf(self) -> None:
            """Clicks the Download PDF link"""
            link = self.dr.flashy_find_element('a.download-pdf', self.element)
            link.click()

        def name(self) -> str:
            """Gets the value of the Name field"""
            return self.dr.flashy_find_element('.icon-company+p', self.element).text

        def email(self) -> str:
            """Gets the destination email of the Email field"""
            return self.dr.flashy_find_element('.icon-email+p a[href^="mailto:"]',
                                               self.element).get_attribute('href')[7:]

        def phone(self) -> str:
            """Gets the number in the Phone field"""
            return self.dr.flashy_find_element('.icon-tel+p a[href^="tel:"]',
                                               self.element).get_attribute('href')[4:]

        class SearchResultPage(WrappedElement):
            """Represents the full More Info page pointed to by a Filtered Search's result."""
            def __init__(self, dr: Drivery):
                self.dr = dr
                self.element = self.dr.flashy_find_element('.home-hero-title')

            def get_title(self) -> None:
                """Returns the title of the page the result was pointing to."""
                return self.element.text.replace('\n', ' ')

    def load_more(self) -> None:
        """Clicks the Search Component's Load More button."""
        self.dr.flashy_find_element('.load-more', self.element).click()
        self.dr.wait_until_gone('.filteredSearch .preload-image-wrapper img')

    def random_search(self) -> None:
        """Picks random values in each of the search category droplists,
        then clicks the Refresh Results button. Repeats this until results are found."""
        while True:
            for select in self.dr.quietly_find_elements('select', self.element):
                self.dr.blip_element(select)
                random.choice(self.dr.quietly_find_elements('option', select)).click()
            self.dr.flashy_find_element('#btn-id,.button-refresh-results', self.element).click()
            self.dr.wait_until_gone('.filteredSearch .preload-image-wrapper img')
            # Check if any results are returned, and if in Fact Sheet Mode, any PDF links.
            if self.dr.check_visible_quick('.mosaic-item,.filter001', self.element):
                # If not in Fact mode, don't need pdf, so done. If in Fact, do need pdf.
                if not self.pdf_mode or (self.dr.check_visible_quick(
                        '.mosaic-item-detail-container .search-favourite a[href$="pdf"]',
                        self.element)):
                    break

    def count_results(self) -> int:
        """Returns the number of search results currently displayed."""
        return len(self.dr.flashy_find_elements('.mosaic-item,filter001', self.element))

    def read_results_counter(self) -> (int, int) or None:
        """Returns the number of results the 'Showing X-Y of Z results' thing says there are:
        A tuple as (shown, total), or a None if it's not shown, such as with Travel Club."""
        counter = self.dr.flashy_find_element('.search-result-count-copy', self.element).text
        counter = [int(x) for x in re.findall(r'\d+', counter)]
        if counter == []:
            return None
        # Different languages can show the numbers in different orders.
        counter.sort()
        # The largest number must be the total results, with the other two being 'this many shown'.
        return (1 + counter[1] - counter[0], counter[2])

    def get_all_results(self) -> List['SearchResult']:
        """Gets all of the search results."""
        return [self.SearchResult(self.dr, e)
                for e in self.dr.flashy_find_elements('.mosaic-item,.filter001')]

    def get_random_result(self) -> WrappedElement:
        """Picks a random one from the search results."""
        result = self.SearchResult(
            self.dr, self.dr.blip_element(
                random.choice(self.dr.quietly_find_elements('.mosaic-item,.filter001'))))
        return result

class ItineraryDay(WrappedElement):
    """Represents the Itinerary Day Links component, the anchor navigation link list."""
    def __init__(self, dr: Drivery, which: int = None):
        self.dr = dr
        if which:
            self.element = self.dr.blip(self.dr.quietly_find_elements('.itinerary-day-nav')[which])
        else:
            self.element = self.dr.flashy_find_element('.itinerary-day-nav')


    def back_to_top(self):
        """Clicks the Back To Top link."""
        self.dr.flashy_find_element('li>a[href="#"]', self.element).click()

    def random_link(self):
        """Clicks a random non-back-to-top, non-current-section link."""
        self.dr.flashy_find_element('li>a:not([href="#"]):not(.active)', self.element).click()
        self.dr.wait_until(lambda: self.dr.execute_script(
            'return $("body:animated").length') == 0, '$(body:animated).length equals zero.')

class PDFPage(WrappedElement):
    """Represents a PDF file viewed within the browser.
    As a PDF embed is not a web page, this class doesn't do much."""
    def __init__(self, dr: Drivery):
        self.dr = dr
        self.element = self.dr.quietly_find_element('embed[type="application/pdf"],.pdfViewer')

class HeaderMapIcon(WrappedElement):
    """Represents the Icon in the Header linking to the Interactive Map."""
    def __init__(self, dr: Drivery):
        self.dr = dr
        self.element = self.dr.flashy_find_element('.link-map a')

class HeaderHeartIcon(WrappedElement):
    """Represents the Heart Icon in the Header. Complete with favourites count."""
    def __init__(self, dr: Drivery):
        self.dr = dr
        self.element = self.dr.flashy_find_element('.favourite-summary')

    def favourites_count(self) -> int:
        """Returns the number of favourites as indicated by the icon subtitle."""
        anim = self.dr.quietly_find_element('.icon-heart-animate', self.element)
        self.dr.wait_until(lambda: anim.get_attribute('style') == '' or
                           anim.get_attribute('style').find('opacity: 0;') != -1,
                           "anim's style is blank, or has an opacity of 0.")
        try:
            return int(self.dr.flashy_find_element('.my-trip-count', self.element).text)
        except ValueError:
            return 0

class HeaderSearch(WrappedElement):
    """Represents the Site Search form in the header."""
    def __init__(self, dr: Drivery):
        self.dr = dr
        self.element = self.dr.flashy_find_element('#nav-main-panel-search')

    def open(self):
        """Opens the main Search Form area."""
        self.dr.blip_element(self.element).click()
        return self

    @staticmethod
    def popular_searches(dr: Drivery, num: int):
        """Returns a generator function of a number of the suggested search buttons."""
        def search(i):
            """Opens a given search key."""
            hs = HeaderSearch(dr).open()
            dr.blip_element(dr.quietly_find_elements('.nav-pills a', hs.element)[i]).click()
        # Gets the number of search terms, picks up to num of them at random.
        keyl = len(dr.quietly_find_elements('.nav-pills a'))
        num = min(keyl, num)
        return (search(y) for y in random.sample(range(keyl), num))

    def search(self, term: str):
        """Enters the given term into the search bar and clicks the Search button."""
        self.dr.flashy_find_element('input.select2-input', self.element).send_keys(term)
        self.dr.flashy_find_element('.nav-search-button', self.element).click()

class InteractiveMap(WrappedElement):
    """Represents the Interactive Map.
    Use in a with statement to switch WebDriver focus into the map's iframe."""
    def __init__(self, dr: Drivery):
        self.dr = dr

    def __enter__(self):
        self.dr.switch_to_frame('#interactiveMapId')
        return self

    def __exit__(self, *args):
        self.dr.switch_to_frame(None)

    class Controls(WrappedElement):
        """Represents the menu to the left of the map area."""
        def __init__(self, dr: Drivery):
            self.dr = dr
            self.element = self.dr.flashy_find_element('.controls-wrapper')

        def open_menu(self) -> None:
            """Opens a menu, and waits until it is open, too."""
            self.dr.blip_element(self.element).click()
            self.dr.wait_until(lambda: self.element.get_attribute('class') == 'active',
                               "self.element's class is active.")

        def pick_random(self) -> None:
            """Picks a random entry from the menu."""
            city = random.choice(self.dr.quietly_find_element('li a', self.element))
            self.dr.blip_element(city).click()

        class Cities(WrappedElement):
            """Represents the Cities Menu."""
            def __init__(self, dr: Drivery):
                self.dr = dr
                self.element = self.dr.flashy_find_element('#cities')
                self.open_menu = MethodType(InteractiveMap.Controls.open_menu, self)
                self.pick_random = MethodType(InteractiveMap.Controls.pick_random, self)

        class IconicDestinations(WrappedElement):
            """Represents the Iconic Destinations Menu."""
            def __init__(self, dr: Drivery):
                self.dr = dr
                self.element = self.dr.flashy_find_element('#icons')
                self.open_menu = MethodType(InteractiveMap.Controls.open_menu, self)
                self.pick_random = MethodType(InteractiveMap.Controls.pick_random, self)

        class Itineraries(WrappedElement):
            """Represents the Itineraries Menu."""
            def __init__(self, dr: Drivery):
                self.dr = dr
                self.element = self.dr.flashy_find_element('#itinerarytypes')
                self.open_menu = MethodType(InteractiveMap.Controls.open_menu, self)
                self.pick_random = MethodType(InteractiveMap.Controls.pick_random, self)

        class FlyingTimes(WrappedElement):
            """Represents the Flying Times Menu."""
            def __init__(self, dr: Drivery):
                self.dr = dr
                self.element = self.dr.flashy_find_element('#flights')
                self.open_menu = MethodType(InteractiveMap.Controls.open_menu, self)

            def choose_from(self) -> str:
                """Randomly chooses a city from the From field."""
                select = self.dr.flashy_find_element('#flightFrom', self.element)
                opt = random.choice(self.dr.quietly_find_elements('option[id]', select))
                opt.click()
                return opt.text

            def choose_to(self) -> str:
                """Randomly sets a city to the To field."""
                select = self.dr.flashy_find_element('#flightTo', self.element)
                opt = random.choice(self.dr.quietly_find_elements('option[id]', select))
                opt.click()
                return opt.text

            def flight_time(self) -> WrappedElement:
                """Gets a representation of the Flight Time display."""
                return MinorElement(self.dr, '.flight-time', self.element)

            def flight_distance(self) -> WrappedElement:
                """Gets a representation of the Flight Distance display."""
                return MinorElement(self.dr, '.flight-distance', self.element)

        class InfoPanel(WrappedElement):
            """Represents the information panel about a City/Icon/Itinerary."""
            def __init__(self, dr: Drivery):
                self.dr = dr
                self.element = self.dr.flashy_find_element('#info-middle')

            def get_title(self) -> str:
                """Returns the name of the location that the panel describes"""
                return self.dr.flashy_find_element('#info-title', self.element).text

            def back_to_menu(self) -> None:
                """Clicks the BACK TO MENU button at the top, then waits until it stops moving"""
                self.dr.flashy_find_element('#back-to-filter', self.element).click()
                panel = self.dr.get_parent_element(
                    self.dr.get_parent_element(self.dr.quietly_find_element('#map-menu')))
                self.dr.wait_until(lambda: panel.get_attribute('style').find('rotateY(0deg)') != -1,
                                   "panel's style does not contain rotateY(0deg)")

            def find_out_more(self) -> str:
                """Returns the url of the Find Out More link."""
                return self.dr.fix_url(self.dr.get_parent_element(self.dr.flashy_find_element(
                    '#info-mainLink', self.element)).get_attribute('href'))

            def view_highlights(self) -> str:
                """Returns the url of the VIEW HIGHLIGHTS button."""
                return self.dr.fix_url(self.dr.flashy_find_element(
                    '#info-optionalLink', self.element).get_attribute('href'))

            def count_photos(self) -> int:
                """Counts the number of photographs shown for this location."""
                return len(self.dr.quietly_find_elements('#info-carousel img', self.element))

            def open_photos(self) -> WrappedElement:
                """Clicks on one of the photos, opening the image carousel."""
                self.dr.flashy_find_element('#info-carousel img', self.element).click()
                self.dr.wait_until_present("#carousel-lightbox")
                return InteractiveMap.ImageCarousel(self.dr)

            def random_itinerary(self) -> str:
                """Clicks on one of the Itinerary Suggestions links, and returns its title."""
                suges = self.dr.quietly_find_elements('#suggested-itineraries a', self.element)
                try:
                    suge = random.choice(suges)
                    sug = suge.text
                    suge.click()
                    self.dr.wait_until(
                        lambda: self.dr.quietly_find_element('#info-title').text == sug,
                        '#info-title.text == sug')
                    return sug
                except IndexError:    # There can apparently be no suggested itineraries.
                    return ''

    class MapArea(WrappedElement):
        """Just a precaution, preventing searches from overlapping too much?"""
        def __init__(self, dr: Drivery):
            self.dr = dr
            self.element = self.dr.flashy_find_element('#map_canvas')

        class MapPins(WrappedElement):
            """Represents the collection of pins that appear on the map when a menu is opened."""
            def __init__(self, dr: Drivery):
                self.dr = dr
                self.pins = self.dr.flashy_find_elements(
                    '{} div.bulb:not(.Itineraries)'.format(
                        '.MapPushpinBase' if self.dr.cn_mode else '.marker'))
                self.element = self.dr.get_parent_element(self.dr.get_parent_element(self.pins[0]))

            def pick_random(self) -> str:
                """Picks a random pin and clicks it. Returns the name of its destination.
                Also changes the CSS to bring it to the front, in case it's behind another one."""
                pin = random.choice(self.pins)
                self.dr.bring_to_front(pin)
                self.dr.blip_element(pin)
                name = pin.text
                pin.click()
                panel = self.dr.quietly_find_element('#info-box')
                self.dr.wait_until(lambda: panel.is_displayed() and
                                   panel.get_attribute('style').find('rotateY(0deg)') != -1,
                                   'panel is displayed and panel.style has no rotateY')
                return name

            def count(self) -> int:
                """Returns the number of map pins visible."""
                self.dr.blip_element(self.pins)
                return len(self.pins)

            def get_names(self) -> List[str]:
                """Returns a list of the labels on all of the pins"""
                self.dr.blip_element(self.pins)
                return [x.text for x in self.pins]

        class InfoPopup(WrappedElement):
            """Represents the popup window thing that appears from an Itinerary Step Pin."""
            def __init__(self, dr: Drivery):
                self.dr = dr
                self.element = self.dr.flashy_find_element('.gm-style-iw')

    class ImageCarousel(WrappedElement):
        """Represents the Photo Carousel that pops out from a Location Information panel"""
        def __init__(self, dr: Drivery):
            self.dr = dr
            self.element = self.dr.flashy_find_element('#lightbox-inner')

        def current_image_source(self) -> str:
            """Returns the image source of the image currently shown."""
            return self.dr.flashy_find_element(
                '#lightbox-inner-image', self.element).get_attribute('src')

        def next(self) -> None:
            """Clicks the > next button to show the next photo."""
            self.dr.flashy_find_element('#next', self.element).click()

        def close(self) -> None:
            """Clicks the X close button to hide the carousel"""
            self.dr.flashy_find_element('#close-lightbox', self.element).click()
            self.dr.wait_until_gone('#lightbox-inner')

    class ZoomTools(WrappedElement):
        """Represents the Zoom In/Zoom Out button set."""
        def __init__(self, dr: Drivery):
            self.dr = dr
            self.element = self.dr.flashy_find_element('.zoom-wrapper')

        def zoom_in(self) -> None:
            """Clicks the Zoom In button."""
            self.dr.flashy_find_element('#zoomin', self.element).click()
            time.sleep(SHORT_WAIT)

        def zoom_out(self) -> None:
            """Clicks the Zoom Out button."""
            self.dr.flashy_find_element('#zoomout', self.element).click()
            time.sleep(SHORT_WAIT)    # Otherwise it tries to click where the pin *was*.

class ContactUs(WrappedElement):
    """Represents the Contact Us page, which isn't a lot."""
    def __init__(self, dr: Drivery):
        self.dr = dr
        self.element = self.dr.flashy_find_element('a[href*="mailto:"]')

class RegistrationForm(WrappedElement):
     # They aren't instance variables. pylint: disable=R0902
    """Represents the Registration Form"""
    def __init__(self, dr: Drivery):
        self.dr = dr
        self.element = self.dr.flashy_find_element('#registration-form')

    def __getattr__(self, name):
        """If an unknown GET message is received, see if there's a field with that name."""
        return self.dr.flashy_find_element(
            '[name*="{}"]'.format(name.replace('_', '-')), self.element).get_attribute('value')

    def __setattr__(self, name, value):
        """If an unknown SET message is received, see if there's a field with that name."""
        # Really should have seen this coming.
        if name in ('element', 'dr'):
            object.__setattr__(self, name, value)
            return
        elem = self.dr.flashy_find_element(
            '[name="{}"]'.format(name.replace('_', '-')), self.element)
        elem.clear()
        elem.send_keys(value)

    def plain_text_fields(self, value: str = ''):
        """Sets the value of all of the text fields that are mandatory,
        but which don't need any particular value or format."""
        elements = self.dr.quietly_find_elements('[type="text"]', self.element)
        for element in elements:
            self.dr.blip_element(element)
            element.send_keys(value)
    # Deliberately uses the __setattr__, ignore the attribute define warning.
    # pylint: disable=W0201
    def date_of_birth(self, value: str = '//') -> None:
        """Overwrites the Date Of Birth Name field to have the given D/M/Y value. Blank default."""
        value = value.split('/')
        self.birthdayday = value[0]
        self.birthdaymonth = value[1]
        self.birthdayyear = value[2]

    def pick_business_profile(self) -> None:
        """Picks a random option in the Business Profile list."""
        sel = self.dr.flashy_find_element('[name="busprofile"]', self.element)
        random.choice(self.dr.quietly_find_elements('option:not([value=""])', sel)).click()

    def pick_partner(self) -> None:
        """Picks a random option in the PReferred Travel Partners list."""
        sel = self.dr.flashy_find_element('[name="affiliationtype"]', self.element)
        random.choice(self.dr.quietly_find_elements('option:not([value=""])', sel)).click()

    def pick_country(self, value: str = '') -> None:
        """Picks the country with the given abbreviation from the Country list."""
        if value == 'EN':
            value = 'XX'
        sel = self.dr.flashy_find_element('#country_id', self.element)
        self.dr.quietly_find_element('option[value="{0}"]'.format(value), sel).click()
        # Wait for the Country selection to load the State/Lang info.
        self.dr.wait_until_present('[name="language"] :not([value=""])')

    def pick_state(self) -> None:
        """Picks a random option from the State/Province/County field."""
        sel = self.dr.flashy_find_element('#state_list', self.element)
        random.choice(self.dr.quietly_find_elements('option:not([value=""])', sel)).click()

    def pick_language(self, lang: str = '') -> None:
        """Picks a language from the Language field. If in Hong Kong, choose carefully."""
        sel = self.dr.flashy_find_element('#language_id', self.element)
        if lang == 'zh':
            self.dr.quietly_find_element('option[value="8"]', sel).click()
        else:
            self.dr.quietly_find_element('option:not([value=""])', sel).click()

    def email_address(self, value: str = '') -> None:
        """Sets the Email Address and Verify Email fields to the given value. Blank default."""
        self.email = value
        # China does not have this email verification.
        if not self.dr.cn_mode:
            self.verifyemail = value

    def how_many_years(self) -> None:
        """Sets the value of the How Many Years Selling field."""
        sel = self.dr.flashy_find_element('#howmany', self.element)
        self.dr.quietly_find_element('option:not([value=""])', sel).click()

    def how_many_times(self) -> None:
        """Sets the value of the How Many Times Been field."""
        sel = self.dr.flashy_find_element('#how-many-times', self.element)
        self.dr.quietly_find_element('option:not([value=""])', sel).click()

    def how_many_bookings(self) -> None:
        """Sets the value of the How Many Bookings Personally Made field."""
        sel = self.dr.flashy_find_element('#number-of-bookings', self.element)
        self.dr.quietly_find_element('option:not([value=""])', sel).click()

    def standard_categories(self) -> None:
        """Picks a random selection of Categories Of Standard Of Travel"""
        sel = self.dr.quietly_find_elements('[name=travelstandard]', self.element)
        for box in random.sample(sel, len(sel) // 2):
            self.dr.blip_element(box).click()

    def experiences(self) -> None:
        """Picks a random selection of Experiences Asked For"""
        sel = self.dr.quietly_find_elements('[name=custexp]', self.element)
        for box in random.sample(sel, len(sel) // 2):
            self.dr.blip_element(box).click()

    def password(self, value: str = '') -> None:
        """Sets the value of the Create A Password and Re-Enter Password fields. Blank default."""
        self.pwd = value
        self.pwd1 = value

    def terms_and_conditions(self) -> None:
        """Agrees to the Terms And Conditions, without reading them."""
        self.dr.flashy_find_element('#agreement', self.element).click()

    def decaptcha(self) -> None:
        """Calculates the value of the 'captcha' code."""
        def get_time() -> int:
            """Calculates the current time."""
            return (round(time.time() * 1000)) // (60 * 1000)
        def do_it(bits: bytes) -> str:
            """Calculates the MD5 hex of something, in addition to the current time."""
            return hashlib.md5(bits + str(get_time()).encode()).hexdigest()[1:6]
        # It's time sensitive, so refresh the captcha immediately beforehand.
        self.dr.flashy_find_element('a[onclick="captchaRefresh()"]', self.element).click()
        self.captcha = do_it(self.dr.flashy_find_element('#cq_captchakey')
                             .get_attribute('value').encode())

    def submit(self) -> None:
        """Clicks the Create My Account Button, and awaits confirmation."""
        self.dr.flashy_find_element("#register-submit", self.element).click()
        self.dr.wait_until_present('#fancybox-thanks')

    def dismiss_popup(self) -> None:
        """Closes the Thanks For Registering thing."""
        self.dr.flashy_find_element('.fancybox-wrap a.fancybox-close').click()
        self.dr.wait_until_gone('#fancybox-thanks')

class SignIn(WrappedElement):
    """Represents the Sign In panel. Instantiating this class will open said panel."""
    def __init__(self, dr: Drivery):
        self.dr = dr
        self.dr.flashy_find_element('.link-signin-text').click()
        self.element = self.dr.flashy_find_element('.fancybox-wrap')
        attach_links(self, ['forgotten-username', 'forgotten-password', 'resend'])

    def sign_in(self, user: str, passw: str) -> None:
        """Logs in using the given Username and Password."""
        self.dr.flashy_find_element('#j_username', self.element).send_keys(user)
        self.dr.flashy_find_element('[name="j_password"]', self.element).send_keys(passw)
        tmp = self.dr.flashy_find_element('#usersignin', self.element)
        self.dr.wait_until(tmp.is_enabled, 'The sign in button is clickable.')
        tmp.click()
        self.dr.wait_for_page('?cq_ck=')

class ForgottenForm(WrappedElement):
    """Represents the Forgotten Username/Password / Resend Registration form.
    They are the same component."""
    def __init__(self, dr: Drivery):
        self.dr = dr
        self.element = self.dr.flashy_find_element('#forgotform')

    def email(self, email: str) -> None:
        """Enters the given email address into the email address field."""
        self.dr.flashy_find_element('#forgotemail', self.element).send_keys(email)

    def submit(self) -> None:
        """Clicks the Submit button and waits for the confirmation message."""
        self.dr.flashy_find_element('#forgotUser-submit', self.element).click()
        self.dr.wait_until_present('.fancybox-skin')

class ChangePassword(WrappedElement):
    """Represents the Change Password form."""
    def __init__(self, dr: Drivery):
        self.dr = dr
        self.element = self.dr.flashy_find_element('#changepwdform')

    def current_password(self, password: str) -> None:
        """Inputs the given password to the Current Password field."""
        self.dr.flashy_find_element('[name="current"]', self.element).send_keys(password)

    def new_password(self, password: str) -> None:
        """Inputs the given password to the New and Repeat Password fields."""
        self.dr.flashy_find_element('#newpwd', self.element).send_keys(password)
        self.dr.flashy_find_element('[name="confirmnew"]', self.element).send_keys(password)

    def submit(self) -> None:
        """Clicks the Update Password button, and then waits for the redirect."""
        self.dr.flashy_find_element('#changepwd-submit', self.element).click()
        self.dr.wait_until_present('.fancybox-wrap')
        self.dr.last_link = 'profile.html'
        self.dr.wait_for_page()

class MySalesTools(WrappedElement):
    """Represents the My Sales Tools page."""
    def __init__(self, dr: Drivery):
        self.dr = dr
        self.element = self.dr.flashy_find_element('.dreamTrip')

    class SalesTool(WrappedElement):
        """Represents a single favourite entry."""
        def __init__(self, dr: Drivery, element):
            self.dr = dr
            self.element = element

        def get_link(self) -> WrappedElement:
            """Returns the entry's More Info link."""
            return MinorElement(self.dr, 'p > a', self.element)

        def get_title(self) -> str:
            """Returns the title of the entry."""
            return self.dr.flashy_find_element('.search-results-title', self.element).text

        def get_description(self) -> str:
            """Returns the Page Summary of the entry."""
            return self.dr.flashy_find_element('.mloverflow-text', self.element).text

        def close(self) -> None:
            """Clicks the X button, closing the entry."""
            self.dr.flashy_find_element('.icon-close', self.element).click()

    def get_favourites(self) -> List[WrappedElement]:
        """Gets all of the saved sales tools entries."""
        return [self.SalesTool(self.dr, x) for x in
                self.dr.flashy_find_elements('.search-result-row-spacing', self.element)]

    def home_search(self) -> WrappedElement:
        """Gets that Home button Search button pair that appears when the list is empty."""
        return self.dr.wait_until_present('.dreamtrip-cta')

class Profile(WrappedElement):
    """Represents the Profile page form."""
    def __init__(self, dr: Drivery):
        self.dr = dr
        self.element = self.dr.flashy_find_element('#profile-form')
        attach_links(self, ['change'])

    def __getattr__(self, name):
        """If an unknown GET message is received, see if there's a field with that name."""
        return self.dr.flashy_find_element('[name*="{}"]'.format(
            name.replace('_', '-')), self.element).get_attribute('value')

    def __setattr__(self, name, value):
        """If an unknown SET message is received, see if there's a field with that name."""
        # Really should have seen this coming.
        if name in {'dr', 'element', 'change'}:
            object.__setattr__(self, name, value)
            return
        elem = self.dr.flashy_find_element(
            '[name*="{}"]'.format(name.replace('_', '-')), self.element)
        elem.clear()
        elem.send_keys(value)

    def get_partner(self) -> str:
        """Gets the text of the selected Travel Partner option."""
        sel = self.dr.flashy_find_element('[name="affiliationtype"]', self.element)
        return self.dr.quietly_find_element(
            '[value="{0}"]'.format(sel.get_attribute('value')), sel).text

    def set_partner(self) -> None:
        """Randomly sets the value of the Travel Partner field. Returns the chosen value."""
        opt = random.choice(self.dr.flashy_find_element('[name="affiliationtype"]', self.element)
                            .find_elements_by_css_selector('option:not([value=""])'))
        opt.click()
        return opt.text

    def get_state(self) -> str:
        """Gets the text of the selected state option."""
        sel = self.dr.flashy_find_element('[name="state"]', self.element)
        return self.dr.quietly_find_element(
            '[value="{0}"]'.format(sel.get_attribute('value')), sel).text

    def set_state(self) -> str:
        """Randomly sets the value of the State field. Returns the chosen value."""
        opt = random.choice(self.dr.flashy_find_element('[name="state"]', self.element)
                            .find_elements_by_css_selector('option:not([value=""])'))
        opt.click()
        return opt.get_attribute('value')

    def save_changes(self) -> None:
        """Clicks the Save Changes button."""
        self.dr.flashy_find_element('#updateProfileSubmit', self.element).click()
        self.dr.wait_until_present('.fancybox-skin')

    # Enum Hack:
    TRAINEE, QUALIFIED, PREMIER = 'trainee', 'qualified', 'premier'
    def user_level(self) -> str:
        """Checks the Status Badge area, returns a string of the User Level."""
        if self.dr.check_visible_quick('.profile-status img', self.element):
            img = self.dr.flashy_find_element('.profile-status img', self.element)
            return {'2': self.QUALIFIED, '3': self.PREMIER}.get(
                img.get_attribute('src').split('/')[-1].split('_')[0], self.TRAINEE)
        return self.TRAINEE

    def module_badges(self) -> Set[str]:
        """Checks the Recent Achievements section, returns a set of the badges attained."""
        return {x.get_attribute('alt').split('_')[-1] for x in self.dr.flashy_find_elements(
            '.Achievements .profile-status img', self.element)}

    def download_certificate(self) -> None:
        """Clicks the Download Certificate link."""
        link = self.dr.flashy_find_element('a[href*="certificate.pdfgenerator"]', self.element)
        link.click()

class TrainingModule(WrappedElement):
    """Represents a Module. Can be used in a with statement, will execute that inside the frame."""
    def __init__(self, dr: Drivery):
        self.dr = dr
        self.code, self.resname = self.wait_for_module()
        self.id = self.code.split('_')[-1]

    def __enter__(self):
        self.enter()
        return self

    def __exit__(self, *args):
        self.exit()

    def wait_for_module(self) -> Tuple[str, str]:
        """Iframes don't integrate into the DOM ReadyState, so have to check this one explicitly.
        Returns the module code, just to be sure."""
        prop = json.loads(self.dr.quietly_find_element(
            'script[data-scf-json="true"]:not([id*="social"])')
                          .get_attribute('innerText'))['properties']
        self.dr.flashy_find_element('.scf-play-button').click()
        # Temporarily switch into the frame stack
        with self:
            # Then, wait until something is actually present
            self.dr.wait_until_present('[id^="Text_Caption_"]')
            # Then, wait until the loading overlay is gone.
            self.dr.wait_until_gone('#preloaderImage')
            # And then, set the module to slide one, just in case.
            self.dr.execute_script('cpCmndGotoSlide=0')
            # Return the which module it is; nsw, mod1, wine, etc...
            return prop['id'], prop['enablement-resource-name']

    def enter(self):
        """Switches into the Module iFrame.
        Does not 'unwrap' the module though, that happens in the constructor."""
        self.dr.switch_to_frame('iframe[src^="/content/"]')
        self.dr.switch_to_frame('frame#ScormContent')

    def exit(self):
        """Switches out of the Module iFrame.
        Use this after you're finished with module stuff, else you'll crash the test."""
        self.dr.switch_to_frame(None)

    def fast_complete_module(self):
        """Call this method when on a training module page,
        (and in the module frame) to fast-complete the module."""
        # Go do the MOD shortcut, basically. Send the module start event, go to the last slide
        # and tell SCORM that the module is totally finished, no, really, it's all suuper done.
        sll = self.dr.execute_script((
            'var sll;function modgo(n){{cpCmndGotoSlide=sll=cpInfoSlideCount-n;}}updateModuleStatus'
            '(setStatusURL,undefined,"{0}",0,false, 0,getModuleID(),"{1}");switch("{2}"){{case "mod'
            '3":modgo(6);break;default:modgo(4)}};SCORM2004_objAPI.RunTimeData.CompletionStatus="co'
            'mpleted";return sll;').format(self.code, self.resname, self.id)) + 1
        self.dr.wait_until(lambda: self.dr.execute_script('return cpInfoCurrentSlide==='+str(sll)),
                           'Current Slide number being equal to the slide it was just set to')

class TrainingSummary(WrappedElement):
    """Represents the two Training Summary modules list things.
    Only instantiate this on the root assignments page. Not guaranteed to get the order right."""
    def __init__(self, dr: Drivery):
        self.dr = dr
        lis = self.dr.flashy_find_elements('.scf-content-card:not(.disabled-link-card)')
        self.core = lis[0]
        lis = self.dr.flashy_find_elements('.scf-content-card')
        self.optional = lis[1]

    def optional_path(self):
        """Open the optional Modules path."""
        self.dr.blip_element(self.optional).click()

    def module_one(self) -> None:
        """Opens the First Core Module."""
        self.dr.blip_element(self.core).click()
        self.dr.blip_element(self.dr.quietly_find_elements('.scf-content-card')[0]).click()

    def module_two(self) -> None:
        """Opens the Second Core Module."""
        self.dr.blip_element(self.core).click()
        self.dr.blip_element(self.dr.quietly_find_elements('.scf-content-card')[1]).click()

    def module_three(self) -> None:
        """Opens the First Core Module."""
        self.dr.blip_element(self.core).click()
        self.dr.blip_element(self.dr.quietly_find_elements('.scf-content-card')[2]).click()

    def module_nsw(self):
        """Opens the First Optional Module. Returns the module code, just to be sure."""
        self.dr.blip_element(self.optional).click()
        self.dr.blip_element(self.dr.quietly_find_elements('.scf-content-card')[0]).click()

    def module_qld(self):
        """Opens the Second Optional Module Returns the module code, just to be sure.."""
        self.dr.blip_element(self.optional).click()
        self.dr.blip_element(self.dr.quietly_find_elements('.scf-content-card')[1]).click()

    def module_vic(self):
        """Opens the Third Optional Module. Returns the module code, just to be sure."""
        self.dr.blip_element(self.optional).click()
        self.dr.blip_element(self.dr.quietly_find_elements('.scf-content-card')[2]).click()

    def completion_types(self) -> None:
        """Gets all of the Module entries, then checks how complete they are,
        then matches that with a Progress Icon type. Kind of a mess."""
        self.dr.flashy_find_elements('.scf-content-card')
        self.dr.flashy_find_element('.assignment-status-completed')
        self.dr.flashy_find_element('.assignment-status-inprogress')
        self.dr.flashy_find_element('.assignment-status-new')

    @staticmethod
    def fast_complete_five_modules(dr):
        """Tells the site that the user has completed five modules. Use this as a backup.
        Also, this switches the driver back to the default framing, for convenience. Class Method"""
        dr.switch_to_frame(None)
        dr.execute_script((
            'var o=["_core_mod1","_core_mod2","_core_mod3","_sto_vic","_sto_nsw"],f="{0}",e=f.split'
            '("-"),l=[];e="es"==e[0]&&"cl"==e[1]||"pt"==e[0]&&"br"==e[1]?e:e.reverse(),e=e.join("_"'
            ').replace("gb","uk");for(m in o)o.hasOwnProperty(m)&&l.push($.ajax({{url:"/bin/asp/tra'
            'iningModule",type:"POST",cache:!1,dataType:"json",data:{{isComplete:!1,moduleId:e+o[m]'
            ',locale:f}}}}));Promise.all(l).then(()=>{{for(m in o)o.hasOwnProperty(m)&&$.ajax({{url'
            ':"/bin/asp/trainingModule",type:"POST",cache:!1,dataType:"json",data:{{isComplete:!0,m'
            'oduleId:e+o[m],locale:f}}}})}});').format(dr.locale[1:]))

class Famils(WrappedElement):
    """Represents the content of the Famils page."""
    def __init__(self, dr: Drivery):
        self.dr = dr
        self.element = self.dr.flashy_find_elements('.type-body')[0]

class AussieSpecialistPhotos(WrappedElement):
    """Represents the image mosaics on the Aussie Specialist Photos page."""
    def __init__(self, dr: Drivery):
        self.dr = dr
        self.photos = self.dr.flashy_find_elements('.mosaic-item')

    def random_images(self, num: int) -> List[WrappedElement]:
        """Randomly selects num photos."""
        return [self.Photo(self.dr, x) for x in random.sample(self.photos, num)]

    class Photo(WrappedElement):
        """Represents an individual Aussie Specialist Photo.
        Don't instantiate this from the test script directly, it needs a WebElement"""
        def __init__(self, dr: Drivery, element: WebElement):
            self.dr = dr
            self.element = self.dr.get_parent_element(
                self.dr.get_parent_element(self.dr.blip_element(element)))
            self.contentpane = None

        def open(self) -> None:
            """Clicks on the mosaic tile, opening it."""
            MinorElement(self.dr, '.flipper img[src*="image/file.adapt"],'
                         '.flipper img[src*="image.adapt"]', self.element).point()
            self.dr.flashy_find_element('.flipper a', self.element).click()
            self.contentpane = [x for x in self.dr.flashy_find_elements(
                '.mosaic-item-detail-container.active') if x.is_displayed()][0]

        def get_description(self) -> MinorElement:
            """Returns the description text in a tile's pane. Has to be open."""
            return MinorElement(self.dr, 'p', self.contentpane)

        def get_link(self) -> MinorElement:
            """Returns the Instagram link from a tiles pane. Has to be open."""
            return MinorElement(self.dr, 'a[href*="instagram.com/australia"]', self.contentpane)

        def close(self) -> None:
            """Clicks the X button in the tiles content. Has to be open first."""
            close = self.dr.flashy_find_element('.icon-close', self.contentpane)
            close.click()

class SpecialistBadge(WrappedElement):
    """Represents the Aussie Specialist Badge Download page and image. Kinda minimal."""
    def __init__(self, dr: Drivery):
        self.dr = dr
        self.dr.flashy_find_element('a[href*="asp-badge.png"]').click()
        time.sleep(1)
        self.dr.switch_to_window(1)
        # There's no jQuery on a bare image, so can't highlight.
        self.dr.quietly_find_element('img[src*="asp-badge.png"]')

class AussieStore(WrappedElement):
    """Contains representations the various pages of the Aussie Store area.
    Don't bother instantiating this one every time, it doesn't do a lot."""
    def __init__(self, dr: Drivery):
        self.dr = dr
        self.element = self.dr.quietly_find_element('.contentwrapper')

    def my_cart(self) -> None:
        """Clicks on the My Cart icon."""
        self.dr.flashy_find_element('#myCartIcon', self.element).click()

    def empty_cart_notice(self) -> None:
        """Closes the Your Cart Is Empty message. If it's open."""
        self.dr.flashy_find_element('.fancybox-skin')
        self.dr.flashy_find_element('.fancybox-close').click()
        self.dr.wait_until_gone('.fancybox-skin')

    class CategoriesMenu(WrappedElement):
        """Represents the list of store Categories to the left."""
        def __init__(self, dr: Drivery):
            self.dr = dr
            cats = self.dr.flashy_find_elements('.store-categories>div')
            self.element = cats[0] if cats[0].is_displayed() else cats[1]
            self.categories = self.dr.quietly_find_elements('li a', self.element)

        def all_products(self) -> None:
            """Clicks on the All Products link."""
            self.dr.flashy_find_element('li:first', self.element).click()

        def count(self) -> int:
            """Gets the number of categories."""
            return len(self.categories)

        def goto_iteree(self, num: int) -> None:
            """Given an number, clicks on the that-number-th link."""
            self.dr.blip_element(self.categories[num]).click()

    class ProductGrid(WrappedElement):
        """Represents the grid of Products that appears on any Category Page."""
        def __init__(self, dr: Drivery):
            self.dr = dr
            self.element = self.dr.quietly_find_element('.store-products')
            self.products = self.dr.flashy_find_elements('.store-products-item')

        def count(self) -> int:
            """Gets the number of products in this category."""
            return len(self.products)

        def goto_iteree(self, num: int) -> str:
            """Given a number, clicks on the that-number-th link."""
            prod = self.dr.blip_element(self.products[num])
            name = prod.text.casefold()
            prod.click()
            return name

        def random_product(self) -> str:
            """Clicks on a random Product link and returns the product's name."""
            return self.goto_iteree(random.randint(0, len(self.products) - 1))

    class ProductPage(WrappedElement):
        """Represents a Product's Page."""
        def __init__(self, dr: Drivery):
            self.dr = dr
            self.element = self.dr.quietly_find_element('.product')
            self.dr.flashy_find_element('.col-sm-9.col-xs-12')

        def name(self) -> str:
            """Gets the Product name displayed in the product info."""
            return self.dr.flashy_find_element('.product-title', self.element).text.casefold()

        def unique_code(self) -> str:
            """Gets the Product's Unique Code, as displayed in the product info."""
            return self.dr.flashy_find_element('.product-code', self.element).text

        def select_max_quantity(self) -> None:
            """Selects the largest available amount in the quantity selector."""
            sel = self.dr.flashy_find_element('[name="product-quantity"]', self.element)
            self.dr.quietly_find_elements('option', sel)[-1].click()

        def add_to_cart(self) -> bool:
            """Clicks the Add To Cart button.
            Retuns true if successfully added, false if cart was full."""
            self.dr.flashy_find_element('#cart', self.element).click()
            if self.dr.check_visible_quick('.fancybox-skin'):
                self.dr.flashy_find_element('.fancybox-close').click()
                self.dr.wait_until_gone('.fancybox-skin')
                return False
            self.dr.last_link = 'cart.html'
            self.dr.wait_for_page()
            return True

    class CartPage(WrappedElement):
        """Represents the My Cart Page."""
        def __init__(self, dr: Drivery):
            self.dr = dr
            self.element = self.dr.flashy_find_element('.shoppingcart')

        def place_order(self, cartempty: bool = False) -> None:
            """Clicks the Place Order button, and waits until it's finished loading/messaging."""
            self.dr.flashy_find_element('.submit', self.element)
            if not cartempty:
                self.dr.last_link = 'confirmation.html'
                self.dr.wait_for_page()
            else:
                self.dr.flashy_find_element('.fancybox-skin')
                self.dr.flashy_find_element('.fancybox-close').click()
                self.dr.wait_until_gone('.fancybox-skin')

        def contact_details(self) -> str:
            """Gets the contact details shown at the bottom of the Cart page. Tidy up a bit, too."""
            text = self.dr.flashy_find_element(
                '.store-order-box-left p:nth-child(2)', self.element).text
            return '\n'.join([x.strip().replace('  ', ' ') for x in text.split('\n')])

        def get_product_names(self) -> List[str]:
            """Gets a list of the names of all of the Products in the Cart."""
            return [x.text.casefold()
                    for x in self.dr.flashy_find_elements('.cell-title', self.element)]

        def count(self) -> int:
            """Counts the number of Products in the Cart."""
            return len(self.dr.quietly_find_elements('.shoppingcart tr', self.element))

        def remove_random(self) -> str:
            """Clicks the Remove Product button on a random Product. Returns the product's name."""
            count = self.count() - 1
            rei = random.randint(0, self.count() - 1)
            rem = self.dr.blip_element(
                self.dr.quietly_find_elements('.cell-title', self.element)[rei])
            ren = rem.text.casefold()
            self.dr.blip_element(self.dr.quietly_find_elements('.product-remove')[rei]).click()
            self.element = self.dr.quietly_find_element('.shoppingcart')
            self.dr.wait_until(lambda: count == self.count(), 'count equals self.count()')
            return ren

        def remove_all(self) -> None:
            """Removes all Products from the Cart. This may take a minute if there are a lot."""
            count = self.count()
            while count > 0:
                self.dr.flashy_find_element('.product-remove').click()
                count -= 1
                self.element = self.dr.quietly_find_element('.shoppingcart')
                self.dr.wait_until(lambda: self.count() == count, 'count equals self.count()')

#start some AUS.com only components?
class ShareThis(WrappedElement):
    """Represents the ShareThis component, the Add and Share buttons."""
    def __init__(self, dr: Drivery):
        self.dr = dr
        self.element = self.dr.flashy_find_element('div.shareThis,.favourite-share-side-container')

    def add_to_favourites(self):
        """Adds the current page to Dream Trip by clicking the red heart Add button."""
        self.dr.flashy_find_element('.favourite-main-container a', self.element).click()

    def open_share(self):
        """Opens the Share section. Whether this means creates the popup or
        slides out the other two icons depends on the Gl/Cn environment."""
        self.dr.flashy_find_element(
            '.shareThisHolder,.shareicons-container>a>span', self.element).click()
        if self.dr.cn_mode:
            slider = self.dr.quietly_find_element('ul.share2', self.element)
            self.dr.wait_until(lambda: 'display: block;' in slider.get_attribute('style'),
                               'display: block in slider.style')
        else:
            # For whatever reason, the element gets recreated halfway through opening.
            panel = self.dr.quietly_find_element('.at-expanded-menu')
            self.dr.wait_until(lambda: self.dr.quietly_find_element('.at-expanded-menu') != panel,
                               'Share window element to be recreated')
            panel = self.dr.flashy_find_element('.at-expanded-menu')
            return self.dr.quietly_find_element('.at-expanded-menu-page-title', panel).text

    def page_description(self) -> str:
        """Returns the page's Description: The Hero Text and the Summary combined."""
        return '\t'.join([self.dr.quietly_find_element('.hero').text,
                          self.dr.quietly_find_element('.summary').text])

    def page_image(self) -> str:
        """Returns the src of the page's Summary Image, the one in the Hero Banner."""
        return self.dr.quietly_find_element('.hero img').get_attribute('src')

    def open_weibo(self):
        """Opens the Weibo popup window, only do this in CN and after open_share.
        And remember to self.dr.switch_to_window."""
        self.dr.flashy_find_element('#weiboshare', self.element).click()

    def open_wechat(self):
        """Opens the WeChat QR Code panel, only do this in CN and after open_share."""
        self.dr.flashy_find_element('#wechatshare', self.element).click()

class WeiboShare(WrappedElement):
    """Represents the Weibo Share page popup. Dismisses the login overlay first, if applicable."""
    def __init__(self, dr: Drivery):
        self.dr = dr
        if self.dr.check_visible_quick('.ficon_close'):
            self.dr.flashy_find_element('.ficon_close').click()
        self.element = self.dr.flashy_find_element('.wwg_body')

    def page_description(self) -> str:
        """Returns the prefilled text as read from the shared-page-to-be."""
        return self.dr.flashy_find_element('#weiboPublisher').text

    def page_image(self) -> str:
        """Returns the src of the first image pulled from the page, should be the hero one."""
        return self.dr.flashy_find_element('.img_hold img').get_attribute('src')

    def miniurl(self) -> str:
        """Returns the minified URL that should redirect to the page."""
        return self.dr.flashy_find_element('.tag_text').text

class QRCode(WrappedElement):
    """Represents the various QR code popups that can appear in AUS.cn"""
    def __init__(self, dr: Drivery):
        self.dr = dr
        self.element = self.dr.find_visible_element('.fancybox-skin,.modal-content')

    def close(self):
        """Closes the popup, usually via the X button."""
        self.dr.flashy_find_element('.fancybox-close,.close', self.element).click()
        # This one doesn't work too well on non-unique selectors, do them separately.
        self.dr.wait_until_gone('.fancybox-skin')
        self.dr.wait_until_gone('.modal-content')

    def decode(self) -> str:
        """Decodes the QR code image, returns the string it evaluates to."""
        # TODO: Figure this out? Probably requires Linux or something.
        raise NotImplementedError("I assume this must be possible, but I've yet to find out how. "
                                  'Just scan the QR manually?')

class PanoramicCarousel(WrappedElement):
    """Represents the Panoramic Carousel and the 360 Video player."""
    def __init__(self, dr: Drivery):
        self.dr = dr
        self.element = self.dr.flashy_find_element('.panoramicCarousel')

    def watch_video(self) -> Tuple[str, str]:
        """Selects a random video to watch. Returns the video's Title+Description and Image src."""
        # The text and the background images are on separate carousels. For some reason.
        num = len(self.dr.quietly_find_elements('.owl-item', self.element)) / 2
        sliden = random.randint(0, num - 1)
        self.dr.blip_element(self.dr.quietly_find_elements('.owl-page')[sliden]).click()
        slide = self.dr.quietly_find_elements(
            '.carouselcoastal-item-container', self.element)[sliden]
        backslide = self.dr.quietly_find_elements('.carouselcoastal-owl-bg', self.element)[sliden]
        self.dr.wait_until(
            lambda: backslide.get_attribute('style') != '', 'backslide.style not blank')
        btn = self.dr.flashy_find_element('.carouselcoastal-explore-btn', slide)
        desc = '  '.join(
            [self.dr.quietly_find_element('.carouselcoastal-explore-title', slide).text,
             self.dr.quietly_find_element('.carouselcoastal-explore-location', slide).text])
        src = self.dr.base_url + backslide.get_attribute('style').split('"')[1]
        btn.click()
        return desc, src

    def once_off_start_video(self):
        """Clicks that second Watch Video button that appears once per session."""
        self.dr.wait_until_present('#start360VideoButtonDesktop')
        self.dr.flashy_find_element('#start360VideoButtonDesktop', self.element).click()
        # Wait for the once-off-screen to finish fading.
        self.dr.wait_until_gone('#owl-onboarding-360')

    def open_video_menu(self):
        """Opens the sidebar menu on the video player."""
        self.dr.flashy_find_element('#btn-side-menu', self.element).click()

    def weibo(self):
        """Opens the Weibo popup."""
        self.dr.flashy_find_element('.panoramic-weibo-link', self.element).click()

    def wechat(self):
        """Opens the WeChat QR panel."""
        self.dr.flashy_find_element('.panoramic-wechat-link', self.element).click()

class KDPSearch(FilteredSearch):
    """Represents the Key Distribution Partner search."""
    def __init__(self, dr: Drivery): # I did the important bits manually. pylint: disable=W0231
        self.dr = dr
        self.element = self.dr.flashy_find_element('.kdpSearch')
        # Hold up, have to wait for the initial results to come in first,
        # they'll interrupt if they appear halfway through something else.
        self.dr.quietly_find_element('.mosaic-item')

    def total_results(self):
        """Returns the number of total results shown on the component's Count thing."""
        # This really is quite a bother?
        time.sleep(1)
        return self.read_results_counter()[1]

    def lit_icons(self):
        """Gets a string of which of the Region Filters are active. may contain n, e, w, or s.
        In no particular order, of course."""
        result = ''
        for x in self.dr.flashy_find_elements('.desk-cat-switch'):
            if 'is-active' in x.get_attribute('class'): # The region name is in the id value text.
                result += self.dr.quietly_find_element('.type-below-btn', x).get_attribute('id')[49]
        return result

    def __getattr__(self, value):
        """If you tried to access north, east, west, or south, this will switch to that filter.
        Otherwise, that'll be an error. Returns a callable method."""
        def switch_to():
            """Switches to the chosen region filter."""
            self.dr.find_visible_element('img[src*="/content/dam/assets/image/aus-cn/kdp/{}"]'
                                         .format(value), self.element).click()
            self.dr.wait_until_gone('.filteredSearch .preload-image-wrapper img')
        return switch_to

class SiteSearch(FilteredSearch):
    """Represents the Search component on the page that appears when using the Header Search."""
    def __init__(self, dr: Drivery): # I did the important bits manually. pylint: disable=W0231
        self.dr = dr
        self.element = self.dr.flashy_find_element('.search>div.search-component')
        # Hold up, have to wait for the initial results to come in first,
        # they'll interrupt if they appear halfway through something else.
        self.dr.quietly_find_element('.mosaic-item')
        # This one is also a nuisance.
        self.dr.wait_until_present('.btn-list-view')

    def list_mode(self):
        """Sets the results display to List Mode."""
        self.dr.flashy_find_element('.btn-list-view', self.element).click()
        self.dr.wait_until_present('.search-grid-container.mosaic-list-view')

    def grid_mode(self):
        """Sets the results display to Grid Mode."""
        self.dr.flashy_find_element('.btn-grid-view', self.element).click()
        self.dr.wait_until_gone('.search-grid-container.mosaic-list-view')

class SpecialOffer(WrappedElement):
    """Represents the Special Offer component."""
    def __init__(self, dr: Drivery, which: int = None):
        self.dr = dr
        if which:
            self.element = self.dr.blip(self.dr.quietly_find_elements('.specialoffer')[which])
        else:
            self.element = self.dr.flashy_find_element('.specialoffer')

    def view_more_information(self):
        """Clicks the View More Information link, or equivalent."""
        self.dr.flashy_find_element('.specialoffer-links a', self.element).click()

class Explore(WrappedElement):
    """Represents the Explore component. Not the Map, the triple-minimap-flip things."""
    def __init__(self, dr: Drivery, which: int = None):
        self.dr = dr
        if which:
            self.element = self.dr.blip(self.dr.quietly_find_elements('.explore-container')[which])
        else:
            self.element = self.dr.flashy_find_element('.explore-container')
        self.cards = [self.ExploreCard(self.dr, x) for x in self.dr.quietly_find_elements(
            '.explore-item-container', self.element) if x.is_displayed()]

    class ExploreCard(WrappedElement):
        """Represents a card in the Explore component."""
        def __init__(self, dr: Drivery, element: WebElement):
            self.dr = dr
            self.element = element

        def flip(self):
            """Clicks the View On Map button, flipping the card to show the map."""
            self.dr.flashy_find_element('#explore-flip-btn', self.element).click()

        def unflip(self):
            """Clicks the Back To Overview link, returning the card to its original orientation."""
            # Wait until the regular flip is finished before unflipping.
            self.dr.wait_until_present('#explore-flip-back-btn')
            self.dr.flashy_find_element('#explore-flip-back-btn', self.element).click()

        def is_flipped(self) -> bool:
            """Returns true if the map is shown, false if the description is shown."""
            return 'is-flip' in self.element.get_attribute('class')

        def add_to_favourites(self):
            """Clicks the Add To Dream Trip button."""
            self.dr.flashy_find_element('.bubble-colour-favourite', self.element).click()

class Livefyre(WrappedElement):
    """Represents the Livefyre component"""
    def __init__(self, dr: Drivery, which: int = None):
        self.dr = dr
        if which:
            self.element = self.dr.blip(self.dr.quietly_find_elements('.livefyre-container')[which])
        else:
            self.element = self.dr.flashy_find_element('.livefyre-container')
        self.tiles = [self.LivefyreTile(self.dr, e) for e in
                      self.dr.quietly_find_elements('.gallery--open-link')]

    def get_description(self) -> str:
        """Gets the caption/description text above the images area."""
        return self.dr.flashy_find_element('.section-intro .type-intro + p', self.element).text

    def scroll(self) -> None:
        """Clicks the Next Arrow button on the carousel, don't use in Mosaic mode"""
        self.dr.flashy_find_element('.owl-next', self.element).click()
        time.sleep(1)   # Yeah, but there's no real indication as to when the animation is done

    def view_more(self) -> None:
        """Clicks the Load More button under the mosaic, don't try this in Carousel mode"""
        x = len(self.tiles)
        self.dr.flashy_find_element('.livefyre-mosaic--load-more').click()
        self.dr.wait_until(lambda: len(self.dr.quietly_find_elements('.gallery--open-link')) > x,
                           'Number of tiles to have increased')
        self.tiles = [self.LivefyreTile(self.dr, e) for e in
                      self.dr.quietly_find_elements('.gallery--open-link')]


    class LivefyreTile(WrappedElement):
        """Represents the individual tiles of a Livefyre collection. Don't instantiate directly.
        Can be used as a context manager to open and close the tile as needed."""
        def __init__(self, dr: Drivery, element: WebElement):
            self.dr = dr
            self.element = element
            self.telemen = None

        def __enter__(self):
            self.click()
            self.telemen = self.dr.flashy_find_element('.livefyre-lightbox-item')
            return self

        def __exit__(self, *args):
            if self.dr.check_visible_quick('.livefyre-lightbox--container'):
                self.dr.flashy_find_element('.livefyre-lightbox--button-arrow-close').click()

        def get_links(self) -> List[WrappedElement]:
            """Use only if the tile is open, gets a list of all of the @ or # links in the text."""
            return [x for x in
                    self.dr.flashy_find_elements('.livefyre-lightbox-content a', self.telemen)]

        def share(self) -> None:
            """Clicks the Share icon, opens the Share interface"""
            self.dr.flashy_find_element('.shareThis').click()
            self.dr.flashy_find_element('.at-expanded-menu')

        def close_share(self) -> None:
            """Closes the share interface"""
            # This is so dumb you guys i mean for real
            try:
                self.dr.flashy_find_element('.at-expanded-menu-close').click()
            except StaleElementReferenceException:
                self.dr.flashy_find_element('.at-expanded-menu-close').click()

class BackupHrefs:    # It's a namespace, lots of methods is intentional. pylint: disable=R0904
    """Call on this if an important component is missing, it has links to the pages."""
    def __init__(self, dr: Drivery):
        self.dr = dr

    def sitemap(self):
        """Opens the Sitemap page."""
        self.dr.get(self.dr.locale_url + '/sitemap.html')

    def itineraries(self):
        """Opens the Itineraries Search page."""
        self.dr.get(self.dr.locale_url + '/sales-resources/itineraries-search-and-feature.html')

    def factsheets(self):
        """Opens The Fact Sheet Search page."""
        self.dr.get(self.dr.locale_url + '/sales-resources/fact-sheets-overview.html')

    def map(self):
        """Opens the Interactive Map page."""
        self.dr.get(self.dr.locale_url + '/sales-resources/interactive-map.html')

    def contact(self):
        """Opens the ASP Contact Us page."""
        self.dr.get(self.dr.locale_url + '/about/contact-us.html')

    def contact_inv(self):
        """Opens the Investment Site Contact Us page."""
        self.dr.get(self.dr.locale_url + '/about-us/contact-us.html')

    def register(self):
        """Opens the Registration Form page."""
        self.dr.get(self.dr.locale_url + 'about/registration-form.html')

    def about(self):
        """Opens the About Landing Page."""
        self.dr.get(self.dr.locale_url + '/about.html')

    def events(self):
        """Opens the Events page"""
        self.dr.get(self.dr.locale_url + '/sales-resources/events.html')

    def favourites(self):
        """Opens the My Sales Tools page."""
        self.dr.get(self.dr.locale_url + '/secure/sales-resources/my-sales-tools.html')

    def profile(self):
        """Opens the Profile page."""
        self.dr.get(self.dr.locale_url + '/secure/profile.html')

    def training(self):
        """Opens the Assignments page. China has a different format though."""
        self.dr.get((self.dr.base_url + '/content/sites/asp' + self.dr.locale.replace('-', '_') +
                     '/assignments.html') if not self.dr.cn_mode else
                    (self.dr.base_url + '/content/sites/asp-zh-cn/en/assignments.html'))

    def travel(self):
        """Opens the Travel Club page."""
        self.dr.get(self.dr.locale_url + '/secure/aussie-specialist-club/travel-club.html')

    def famils(self):
        """Opens the Famils page."""
        self.dr.get(self.dr.locale_url + '/secure/aussie-specialist-club/famils.html')

    def photos(self):
        """Opens the Aussie Specialist Photos page."""
        self.dr.get(self.dr.locale_url +
                    '/secure/aussie-specialist-club/aussie-specialist-photos.html')

    def store(self):
        """Opens the Aussie Store page."""
        self.dr.get(self.dr.locale_url + '/secure/aussie-specialist-club/aussie-store.html')

    def username(self):
        """Opens the Forgotten Username page."""
        self.dr.get(self.dr.locale_url + '/forgotten-username.html')

    def password(self):
        """Opens the Forgotten Password page."""
        self.dr.get(self.dr.locale_url + '/forgotten-password.html')

    def resend(self):
        """Opens the Resend Verification Email page."""
        self.dr.get(self.dr.locale_url + '/resend-verification-email.html')

    def change(self):
        """Opens the Change Password page."""
        self.dr.get(self.dr.locale_url + '/change.html')

    def getting_around(self):
        """Opens the Getting Around page."""
        self.dr.get(self.dr.locale_url + '/planning/getting-around.html')

    def aquatic(self):
        """Opens the Aquatic And Coastal page."""
        self.dr.get(self.dr.locale_url + '/things-to-do/aquatic.html')

    def kdp(self):
        """Opens the Key Distribution Partner search page."""
        self.dr.get(self.dr.locale_url + '/plan/kdp.html')

    def regional_cities(self):
        """Opens the Regional Cities page."""
        self.dr.get(self.dr.locale_url + '/places/regional-cities.html')

    def australias_animals(self):
        """Opens the Australia's Animals page."""
        self.dr.get(self.dr.locale_url + '/facts/australias-animals.html')

    def whitsundays(self):
        """Opens the Whitsundays Sailing page."""
        self.dr.get(self.dr.locale_url + '/itineraries/qld-whitsundays-sailing.html')

    def city_journeys(self):
        """Opens the Three Day Itineraries: City Journeys page."""
        self.dr.get(self.dr.locale_url + '/itineraries/city-journeys.html')

    def great_barrier_reef(self):
        """Opens the Great Barrier Reef page."""
        self.dr.get(self.dr.locale_url + '/places/great-barrier-reef.html')

    def offers(self):
        """Opens the Special Offers page."""
        self.dr.get(self.dr.locale_url + ('/campaigns.html' if self.dr.cn_mode
                                          else '/campaign/specialoffers.html'))

    def tas(self):
        """Opens the Tasmania page."""
        self.dr.get(self.dr.locale_url + '/places/tas.html')

    def sydney(self):
        """Opens the Tasmania page."""
        self.dr.get(self.dr.locale_url + '/places/sydney.html')

    def why_australia(self):
        """Opens the Why Australia page."""
        self.dr.get(self.dr.locale_url + '/why-australia.html')

    def world_class_tourism_offering(self):
        """Opens the World Class Tourism Offering page."""
        self.dr.get(self.dr.locale_url + '/why-australia/world-class-tourism-offering.html')

    def tourism_demand_strategy(self):
        """Opens the Tourism Demand Strategy page."""
        self.dr.get(self.dr.locale_url + '/why-australia/tourism-demand-strategy.html')

    def data_room(self):
        """Opens the Data Room page."""
        self.dr.get(self.dr.locale_url + '/data-room.html')
