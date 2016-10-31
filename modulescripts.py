"""Moved all these scripts to a separate file.
Because scrolling through all this really was tiresome.

You can basically treat the first part of this as a properties file.

Legend:
Each new line represents a different slide, unless it is indented, in which case
the line was just too long, and was wrapped to improve readability.
Except those stateblocks in mod2, those aren't all on one slide, it just looked better.
Also, VIC actually comes just after ACT in terms of slide number, but
the NSW complete icon bounding box kind of interferes with it otherwise.

A List, like ['Button_001', 'Button_010', 'Button_100'], is a workaround
for alternate button ids. A css query is created that checks for the presence
of any of the given alternates, and if any are found (there should only be one),
picks the first one and does whatever with it, usually a click.
If the last one is an 'Image_' or something, it means there was an entirely different page,
and this acts as a sort of no-op to assist in regaining synchronisation.
Also, something like that 'Button_2510[style*="z-index: 6"]' option is due to
DE's nasty habit of picking button ids which are the same number as another locale's
Open Menu Button, so the z-index is added to be more specific.
A Tuple, like ('s15_GBR', 'gbr_drop') signifies a Drag And Drop, with the first
one being dragged to the second. Note, Tuples can contain Lists too."""

from collections import OrderedDict

# Editing this is easier than using the command line.

        ### ### ### #### ### ### ###
        ### Begin the Touch Zone ###
        ### ### ### #### ### ### ###

# The website domain to use in testing.
# ENV = 'https://dev-pub-elb-asp.tour-aus.aws.haylix.net'
# ENV = 'https://uat-pub-elb-asp.tour-aus.aws.haylix.net'
ENV = 'https://poc-pub-elb-asp.tour-aus.aws.haylix.net'
# ENV = 'https://stage-pub-elb-asp.tour-aus.aws.haylix.net'
# ENV = 'https:www.aussiespecialist.com'

# The Username and Password to use in the Server Authentication, if necessary.
AUTH = ['dev', 'bclvOP']
# If not necessary, don't remove the entry, just leave the fields blank.
# AUTH = ['', '']

# Ehh, nothing major here, just, if you want differently-shaped timestamps?
TIMEFORMAT = '%Y/%m/%d %H:%M'

# Which users to log in with when testing through site.
USERS = {'ca': 'cadevZXYI', 'in': 'indevKWFR', 'my': 'mydevVOXU', \
'sg': 'sgdevTDBZ', 'gb': 'gbpocuxem', 'us': 'uspocwgau', \
'ehk': 'hkdevXEOS', 'zhk': 'hkprorjyu', 'id': 'idpronqgn', 'jp': 'jpprodqny', 'kr': 'krprovrqf', \
'br': 'brproheby', 'cl': '', 'de': 'deprokirs', 'fr': 'frprodxes', 'it': 'itprotxqb', \
'cn': 'cnwwwAYYC'}
# Backup
# USERS = {'ca': 'caprowtvw', 'in': 'inprontvg', 'my': 'myproqcmc', \
# 'sg': 'sgprodyyw', 'gb': 'gbpoccgvn''gbwwwvjvz', 'us': 'usprokcmi', \
# 'ehk': 'hkproptls', 'zhk': 'hkprorjyu', 'id': 'idpronqgn', 'jp': 'jpprodqny', 'kr': 'krprovrqf', \
# 'br': 'brproheby', 'cl': '', 'de': 'deprokirs', 'fr': 'frprodxes', 'it': 'itprotxqb', \
# 'cn': 'cnwwwAYYC'}

# List of locale codes.
LANGS = {'ca': ('en-ca', 'ca_en'), 'in': ('en-in', 'in_en'), 'my': ('en-my', 'my_en'), \
    'sg': ('en-sg', 'sg_en'), 'gb': ('en-gb', 'uk_en'), 'us': ('en-us', 'us_en'), \
'ehk': ('en-hk', 'hk_en'), 'zhk': ('zh-hk', 'hk_zh'), 'id': ('id-id', 'id_id'), \
    'jp': ('ja-jp', 'jp_ja'), 'kr': ('ko-kr', 'kr_ko'), \
'br': ('pt-br', 'br_pt'), 'cl': ('es-cl', 'cl_es'), 'de': ('de-de', 'de_de'), \
    'fr': ('fr-fr', 'fr_fr'), 'it': ('it-it', 'it_it'), \
'cn': ('zh-cn', 'cn_zh')}

# GB POC
MODULES = OrderedDict([('1', ('res', 'core_mod1_7')), ('2', ('res1', 'core_mod2_7')), \
        ('3', ('res2', 'core_mod3_7')), \
    ('act', ('res13', 'sto_act_0407')), ('nsw', ('res4', 'sto_nsw_ali')), \
        ('nt', ('res12', 'sto_nt_ali')), ('qld', ('res7', 'sto_qld_ali')), \
        ('sa', ('res9', 'sto_sa_ali')), ('tas', ('res10', 'sto_tas_ali0321')), \
        ('vic', ('res8', 'sto_vic_ali')), ('wa', ('res11', 'sto_wa_ali')), \
    ('aboriginal', ('res16', 'Aboriginal_Exp_HO_ali')), \
        ('golf', ('res6', 'niche_golf_ali')), ('lodges', ('res15', 'niche_lodges_ali')), \
        ('ra', ('res14', 'niche_ra_ali')), ('walks', ('res17', 'niche_walks_ali')), \
        ('wine', ('res18', 'niche_wine_ali')), ('aquatic', ('res19', 'niche_coastal_ali'))])

# # US POC
# MODULES = OrderedDict([('1', ('res', 'core_mod1_7')), ('2', ('res7', 'core_mod2_7')), \
#         ('3', ('res8', 'core_mod3_7')), \
#     ('act', ('res3', 'sto_act_0407')), ('nsw', ('res11', 'sto_nsw_ali')), \
#         ('nt', ('res12', 'sto_nt_ali')), ('qld', ('res13', 'sto_qld_ali')), \
#         ('sa', ('res14', 'sto_sa_ali')), ('tas', ('res15', 'sto_tas_ali0321')), \
#         ('vic', ('res16', 'sto_vic_ali')), ('wa', ('res17', 'sto_wa_ali')), \
#     ('aboriginal', ('res1', 'Aboriginal_Exp_HO_ali')), \
#         ('golf', ('res4', 'niche_golf_ali')), ('lodges', ('res6', 'niche_lodges_ali')), \
#         ('ra', ('res9', 'niche_ra_ali')), ('walks', ('res5', 'niche_walks_ali')), \
#         ('wine', ('res10', 'niche_wine_ali')), ('aquatic', ('res2', 'niche_coastal_ali'))])
# MODULES = OrderedDict([('1', ('core_1', 'core_mod1_ali')), ('2', ('_19', 'core_mod2_ali')), \
#         ('3', ('core_3', 'core_mod3_ali')), \
#     ('act', ('_1', 'sto_act_0407')), ('nsw', ('_20', 'sto_nsw_ali')), \
#         ('nt', ('nt', 'sto_nt_ali')), ('qld', ('qld', 'sto_qld_ali')), \
#         ('sa', ('sa', 'sto_sa_ali')), ('tas', ('_18', 'sto_tas_ali0321')), \
#         ('vic', ('_17', 'sto_vic_ali')), ('wa', ('wa', 'sto_wa_ali')), \
#     ('aboriginal', ('niche_aboriginal', 'Aboriginal_Exp_HO_ali')), \
# +5 ('golf', ('niche_golf', 'niche_golf_ali')), ('lodges', ('niche_lodges', 'niche_lodges_ali')), \
# +5 ('ra', ('niche_ra', 'niche_ra_ali')), ('walks', ('niche_walks', 'niche_walks_ali')), \
#+7('wine', ('niche_wine', 'niche_wine_ali')), ('aquatic', ('niche_coastal', 'niche_coastal_ali'))])







        ### ### ### ### ### ### ### ### ###
        ### Begin the Do Not Touch Zone ###
        ### ### ### ### ### ### ### ### ###





MOD_1_SCRIPT = ['Button_728', \
['Button_902', 'Button_903', 'Button_953', 'Button_918', \
    'Button_900[style*="z-index: 15"]', 'Text_Caption_632'], \
    ['Button_887', 'Text_Caption_375'], ['Button_890', 'Text_Caption_375'], \
    ['Button_885', 'Text_Caption_375'], ['Button_889', 'Text_Caption_375'], \
    ['Button_886', 'Text_Caption_375'], ['Button_888', 'Text_Caption_375'], \
    ['Button_891', 'Text_Caption_375'], \
'Button_484', 'Button_485', 'Button_554', \
's4_button2', 's4_button3', 's4_button4', 's4_button5', 'Button_836', 'Button_556', \
('s7Native', 'Image_95'), ('s7Reef', 'Image_95'), ('s7Forrect', 'Image_95'), \
    ('s7Sights', 'Image_95'), ('s7landscape', 'Image_95'), ('s7Fresh', 'Image_94'), \
    ('s7Wine', 'Image_94'), ('s7picnic', 'Image_93'), ('s7Roads', 'Image_91'), \
     'Button_558', \
['expensive_button', 'Button_930', 'Barriers_Singapore_btn2', 'Barriers_Malaysia_btn2'], \
    ['time_button', 'Button_931', 'Barriers_Singapore_btn3', 'Barriers_Malaysia_btn3'], \
    ['Button_560', 'Button_939', 'Button_1009', 'Button_995'], \
's10_btn1', 'Button_650', 'Button_653', 'Button_660', 'Button_564', \
['Button_690', 'Button_914'], ['Button_674', 'Button_902'], \
    ['Button_678', 'Button_905'], ['Button_669', 'Button_916'], \
'radio_btn3', 'Button_826', 'Button_566', \
's10_button2', 's10_button3', 's10_button4', 'Button_806', \
['Button_900', 'WhyIndiansLove_btn2', 'WhyMalaysiansLove_btn2', \
        'WhySingaporeansLove_btn2', 's13_btn2', 'Button_935', 'Image_476'], \
    ['Button_901', 'WhyIndiansLove_btn3', 'WhyMalaysiansLove_btn3', \
        'WhySingaporeansLove_btn3', 's13_btn3', 'Button_936', 'Image_476'], \
    ['Button_908', 'Button_965', 'Button_1021', 'Button_1035', \
        'Button_568', 'Button_943', 'Image_476'], \
('s15_GBR', 'gbr_drop'), ('s15_nt', 'NT_drop'), ('s15_SA', 'SA_drop'), ('s16_vic', 'VIC_drop'), \
    ('s15_WA', 'WA_drop'), ('s15_syd', 'sydney_drop'), 'Button_570', \
'Button_572', \
'Button_799']

MOD_2_SCRIPT = ['P1_btn_LetsStart', \
'Button_2815', 'Button_2816', ['Button_3068', 'Button_945'], \
['map_qld', 'Button_2878'], \
    'Button_1791', \
    'Button_1789', \
    'Button_2617', 'Button_2649', 'Button_1817', \
    'Button_2618', 'Button_2657', 'Button_1961', \
    'Button_2619', 'Button_2658', 'Button_1971', \
    'Button_2620', 'Button_2659', 'Button_2998', 'Button_3000', 'Button_1819', \
    ('Drag_GBR', 'drop_gbr'), ('Drag_Wildlife', 'drop_wild'), \
        ('Drag_IslandsBeaches', 'drop_island'), 'Button_15', 'Button_2688', \
    ('answer_nature', 'drop_nature'), ('answer_events', 'drop_events'), \
        ('answer_southbank', 'drop_southbank'), 'Button_17', 'qld_next', \
['map_vic', 'Button_2874'], \
    'Button_2094', \
    'Button_2083', \
    'Button_2629', 'Button_2668', 'Button_2104', \
    'Button_2630', 'Button_2669', 'Button_2159', \
    'Button_2631', 'Button_2670', 'Button_2169', \
    'Button_2632', 'Button_2671', 'Button_2457', 'Button_2459', 'Button_2455', \
    ('Drag_Yarra', 'drop_yarra'), ('Drag_Phillip', 'drop_phillip'), \
        ('Drag_GOR', 'drop_gor'), 'Button_26', 'Button_2710', \
    ('answer_fitzroy', 'drop_fitzroy'), ('answer_south', 'drop_south'), \
        ('answer_lane', 'drop_lane'), 'Button_50', 'vic_next', \
['map_nsw', 'Button_2873'], \
    'Button_2002', \
    'Button_2077', \
    'Button_2621', 'Button_2660', 'Button_2012', \
    'Button_2622', 'Button_2661', 'Button_2022', \
    'Button_2623', 'Button_2662', 'Button_2471', \
    'Button_2624', 'Button_2663', 'Button_2441', 'Button_2443', 'Button_2439', \
    ('Drag_Byron', 'drop_byron'), ('Drag_Hunter', 'drop_hunter'), \
        ('Drag_BlueMountains', 'drop_blue_mountain'), 'Button_19', 'Button_2702', \
    ('answer_beaches', 'drop_beaches'), ('answer_opera', 'drop_opera'), \
        ('answer_harbour', 'drp_harbour'), 'Button_46', 'nsw_next', \
['map_act', 'Button_2875'], \
    'Button_1892', \
    'Button_1881', \
    'Button_2625', 'Button_2664', 'Button_1902', \
    'Button_2626', 'Button_2665', 'Button_1981', \
    'Button_2627', 'Button_2666', 'Button_1991', \
    'Button_2628', 'Button_2667', 'Button_3004', 'Button_3006', 'Button_1912', \
    ('Drag_Food', 'drop_food'), ('Drag_Family', 'drop_family'), \
        ('Drag_Art', 'drop_art'), 'Button_22', 'Button_2706', \
    ('answer_gallery', 'drop_gallery'), ('answer_museum', 'drop_museum'), \
        ('answer_awm', 'drop_awm'), 'Button_54', 'act_next', \
['map_tas', 'Button_2877'], \
    'Button_2184', \
    'Button_2173', \
    'Button_2633', 'Button_2672', 'Button_2194', \
    'Button_2634', 'Button_2673', 'Button_2234', \
    'Button_2635', 'Button_2674', 'Button_2224', \
    'Button_2636', 'Button_2675', 'Button_3010', 'Button_3012', 'Button_2481', \
    ('Drag_CradleMountain', 'drop_cradle'), ('Drag_Strahan', 'drop_strahan'), \
        ('Drag_Freycinet', 'drop_freycinet'), 'Button_30', 'Button_2714', \
    ('answer_mount', 'drop_mount'), ('answer_market', 'drop_market'), \
        ('answer_mona', 'drop_mona'), 'Button_58', 'tas_next', \
['map_sa', 'Button_2876'], \
    'Button_2249', \
    'Button_2238', \
    'Button_2637', 'Button_2676', 'Button_2259', \
    'Button_2638', 'Button_2677', 'Button_2289', \
    'Button_2639', 'Button_2678', 'Button_2299', \
    'Button_2640', 'Button_2679', 'Button_2508', 'Button_2510', 'Button_2506', \
    ('Drag_Flinders', 'drop_flindert'), ('Drag_KangarooIsland', 'drop_kangaroo'), \
        ('Drag_Barossa', 'drop_barossa'), 'Button_34', 'Button_2718', \
    ('answer_glenelg', 'drop_glenelg'), ('answer_north', 'drop_north'), \
        ('answer_market_ade', 'drop_market_ade'), 'Button_62', 'sa_next', \
['map_wa', 'Button_2880'], \
    'Button_2314', \
    'Button_2303', \
    'Button_2641', 'Button_2680', 'Button_2324', \
    'Button_2642', 'Button_2681', 'Button_2354', \
    'Button_2643', 'Button_2682', 'Button_2364', \
    'Button_2644', 'Button_2683', 'Button_3016', 'Button_3018', 'Button_2538', \
    ('Drag_Margaret', 'drop_margaret'), ('Drag_Ningaloo', 'drop_ningaloo'), \
        ('Drag_Kimberley', 'drop_kimberley'), 'Button_38', 'Button_2722', \
    ('answer_parks', 'drop_parks'), ('answer_rottnest', 'drop_rottnest'), \
        ('answer_fremantle', 'drop_fremantle'), 'Button_66', 'wa_next', \
['map_nt', 'Button_2879'], \
    'Button_2379', \
    'Button_2368', \
    'Button_2645', 'Button_2684', 'Button_2389', \
    'Button_2646', 'Button_2685', 'Button_2419', \
    'Button_2647', 'Button_2686', 'Button_2429', \
    'Button_2648', 'Button_2687', 'Button_2524', 'Button_2526', 'Button_2522', \
    ('Drag_Alice', 'drop_alice'), ('Drag_Kakadu', 'drop_kakadu'), \
        ('Drag_Uluru', 'drop_uluru'), 'Button_42', 'Button_2726', \
    ('answer_waterfront', 'drop_waterfront'), ('answer_market_dar', 'drop_market_dar'), \
        ('answer_croc', 'drop_croc'), 'Button_70', 'nt_next', \
'Button_2881', \
    ('drag_syd', 'drop_sydney'), (['drag_per', 'drag_perth1'], 'drop_perth'), \
        ('drag_melb', 'drop_melbourne'), ('drag_hob', 'drop_hobart'), \
        ('drag_dar', 'drop_darwin'), ('drag_can', 'drop_canberra'), \
        ('drag_bris', 'drop_brisbane'), ('drag_ade', 'drop_adelaide'), 'Button_2854', \
    'Button_2804', \
    'Button_2882']

MOD_3_SCRIPT = ['P1_btn_LetsStart', \
'Button_2051', 'Button_2052', 'Button_2053', 'Button_945', \
'Button_2453', 'Button_2453', 'Button_2453', 'Button_2450', \
['Button_3011', 'Button_2442'], \
['Button_3015', 'Button_2330'], \
's4_true', 'Button_2080', 'Button_2018', \
'europe_button', 'japan_button', 'china_button', 'usa_button', 'Button_2310', \
'Button_3007', \
'Button_2334', \
'rail_but_india', 'rail_but_ghan', 'Button_2349', \
'coach_but_escort', 'Button_2357', \
'car_but_hire', 'car_but_camper', 'car_but_itineries', 'Button_2367', \
's12_radio2', 'Button_2325', 'Button_2322', \
's13_radio3', 'Button_2385', 'Button_2378', \
'Button_1897', 'Button_1898', 'Button_1899', 'Button_1900', 'Button_1901', \
    'Button_1902', 'Button_1903', 'Button_2567', 'Button_1853', \
'Button_3003', \
'climate_but_temperate', 'climate_but_tropical', 'climate_but_guide', 'Button_2095', \
'Button_2409', 'Button_2410', 'Button_2411', 'Button_2412', \
    'Button_2413', 'Button_2414', 'Button_2087', \
'Button_2256', 'Button_2254', ('Sydney_Drag', 'Sydney_Drop'), \
    'Button_2258', 'Button_2266', ('Uluru_Drag', 'Uluru_Drop'), \
    'Button_2259', 'Button_2267', ('Cairns_Drag', 'Cairns_Drop'), \
    'Button_2260', 'Button_2268', ('PortDouglas_Drag', 'PourtDouglas_Drop'), \
    'Button_2261', 'Button_2269', ('KataTjuta_Drag', 'KataTjuta_Drop'), \
    'Button_2262', 'Button_2270', ('HunterValley_Drag', 'Hunter_Blue_Drop1'), \
    'Button_2263', 'Button_2271', ('BlueMountainsDrag', 'Hunter_Blue_Drop2'), \
    'Button_2264', 'Button_2272', ('GreatBarrierReef_Drag', 'GreatBarrierReef_Drop'), \
    'si124915', 'Button_2249', \
'Button_2643', 'Button_2644', 'Button_1971', \
'Button_2792', 'Button_2803', ('kangaroo_drag', 'kangaroo_drop'), \
    'Button_2793', 'Button_2804', ('adelaide_drag', 'adel_drop'), \
    'Button_2794', 'Button_2805', ('hobart_drag', 'hobart_drop'), \
    'Button_2795', 'Button_2806', ('melbourne_drag', 'melbourne_drop'), \
    'Button_2796', 'Button_2807', ('bruny_drag', 'bruny_drop'), \
    'Button_2797', 'Button_2808', ('phillip_drag', 'phillip_drop'), \
    'Button_2798', 'Button_2809', ('barossa_drag', 'bar_drop'), \
    'Button_24', 'Button_2790', \
'Button_2601', 'Button_2600', 'Button_1975', \
'Button_2768', 'Button_2779', ('Drag_Margaret_River', 'drop_Margaret'), \
    'Button_2769', 'Button_2780', ('Drag_Perth', 'drop_perth'), \
    'Button_2770', 'Button_2781', ('Drag_Canberra', 'dropCanberra'), \
    'Button_2771', 'Button_2782', ('Drag_Sydney', 'drop_sydney'), \
    'Button_2787', 'Button_2788', ('Drag_SouthCoast', 'Drop_south'), \
    'Button_2772', 'Button_2783', ('Drag_Dolphin', 'drop_dolphin'), \
    'Button_2773', 'Button_2784', ('Drag_HotAirBalloon', 'drop_hot'), \
    'Button_2774', 'Button_2785', ('Drag_Rottnest', 'drop_rottnest'), \
    'Button_2775', 'Button_2786', (['Drag_SydneyHarbourCruise', \
        'Drag_Sydney_Harbour'], 'drop_harbour'), 'Button_20', 'Button_2766', \
'Button_2718', 'Button_2720', 'Button_2713', \
'Button_2238', \
'Button_2969', 's24_yesSubmit', 'Button_2973', \
'Button_2995']

ACT_SCRIPT = ['Button_2016', \
'Button_2212', 'Button_2213', 'Button_2214', 'Button_2206', \
'Button_2469', \
'Button_1971', 'Button_1966', \
('dd_hobart', 'dd_target'), 'si111288', 'Button_1978', \
'Button_2530', 'Button_2526', \
'Button_2420', \
'Button_2114', 'Button_2175', 'Button_1862', \
'tf1_t', 'tf1_submit', 'Button_2178', \
'Button_2170', 'Button_2167', 'Button_1899', \
'Button_1873', \
'Button_1895', \
'a1_rb3', 'a1_submit', 'Button_2188', \
'Button_1935', \
's15_tf2_t', 'Button_2548', 'Button_2543', \
'Button_2382', \
'Button_1903', \
'Button_1907', \
'Button_2552', 'Button_2551', 'Button_1911', \
'a2_rb2', 'a2_submit', 'Button_2225', \
'Button_2553', 'Button_2623', 'Button_2145', 'Button_2166', 'Button_1919', \
'Button_2560', 'Button_2624', 'Button_2558', 'Button_2561', 'Button_2555', \
's23_tf3_t', 'Button_2569', 'Button_2564', \
'Button_2051', 'Button_2284', 'Button_2292', 'Button_2294', 'Button_2296', 'Button_2049', \
'Button_2573', \
'Button_2505', \
'Button_2580', 'Button_2581', 'Button_2582', 'Button_2583', 'Button_2584', 'Button_2576', \
'ff1_fact1', 'ff1_fiction2', 'ff1_fact3', 'Button_1989', \
'Button_2448', 'Button_2088', \
'Button_2061', \
'Button_2184', \
'Button_2468']

NSW_SCRIPT = ['Button_2016', \
'Button_2212', 'Button_2213', 'Button_2214', 'Button_2206', \
'Button_2474', 'Button_2473', 'Button_2469', \
'Button_1969', 'Button_1966', \
('dd_hobart', 'dd_target'), 'si111288', 'Button_1978', \
'Button_2527', 'Button_2528', 'Button_1981', \
'Button_2114', 'Button_2175', 'Button_1862', \
'Button_2420', \
'Button_1873', \
'Button_1895', \
'Button_2170', 'Button_2167', 'Button_1899', \
'Button_2378', \
'Button_2382', \
'a1_rb2', 'a1_submit', 'Button_2188', \
'Button_2142', 'Button_2174', 'Button_1903', \
'Button_1907', \
'tf1_t', 'tf1_submit', 'Button_2178', \
'Button_2386', 'Button_2387', 'Button_1911', \
'Button_2145', 'Button_2166', 'Button_1919', \
'Button_2169', 'Button_2171', 'Button_1923', \
'a2_rb3', 'a2_submit', 'Button_2225', \
'Button_1927', \
'Button_2388', \
'Button_2403', 'Button_2176', 'Button_1931', \
'a3_rb1', 'a3_submit', 'Button_2192', \
'Button_2404', 'Button_2397', 'Button_2393', \
'Button_2405', 'Button_2402', 'Button_2398', \
'a4_rb1', 'a4_submit', 'Button_2158', \
'Button_2410', 'Button_2411', 'Button_2406', \
'Button_1935', \
'Button_1939', \
'Button_1943', \
'Button_1947', \
'Button_2051', 'Button_2284', 'Button_2292', 'Button_2294', 'Button_2296', 'Button_2049', \
'Button_2505', \
'Button_2530', 'Button_2531', 'Button_2532', 'Button_2533', 'Button_2534', 'Button_2449', \
'ff1_fiction1', 'ff1_fiction2', 'ff1_fact3', 'Button_1989', \
'Button_2448', 'Button_2088', \
'Button_2061', \
'Button_2184', \
'Button_2468']

NT_SCRIPT = ['Button_2016', \
'Button_2212', 'Button_2213', 'Button_2214', 'Button_2206', \
'Button_2493', 'Button_2492', 'Button_1856', \
'Button_1975', 'Button_1966', \
('Image_1288', 'dd_target'), 'si111288', 'Button_1978', \
'Button_1985', 'Button_2461', 'Button_1987', 'Button_1981', \
'Button_2469', 'Button_2468', 'Button_1862', \
'Button_2480', 'Button_2470', 'Button_2139', 'Button_2173', 'Button_1873', \
'Button_2481', 'Button_2471', 'Button_1895', \
'a1_rb1', 'a1_submit', 'Button_2188', \
'Button_2482', 'Button_2472', 'Button_1903', \
'Button_2483', 'Button_2473', 'Button_1907', \
'tf1_t', 'tf1_submit', 'Button_2506', \
'Button_2484', 'Button_2474', 'Button_1911', \
'Button_2144', 'Button_2165', 'Button_1915', \
'Button_2485', 'Button_2475', 'Button_1919', \
'Button_2491', 'Button_2490', 'Button_2169', 'Button_2171', 'Button_1923', \
'a2_rb3', 'a2_submit', 'Button_2225', \
'Button_2486', 'Button_2476', 'Button_1927', \
'Button_2487', 'Button_2477', 'Button_2147', 'Button_2176', 'Button_1931', \
's21_false', 'Button_2438', 'Button_2433', \
'Button_2488', 'Button_2478', 'Button_2441', \
'Button_2489', 'Button_2479', 'Button_2449', 'Button_2452', 'Button_2446', \
'a4_rb2', 'a4_submit', 'Button_2158', \
'Button_2051', 'Button_2284', 'Button_2292', 'Button_2294', 'Button_2296', 'Button_2049', \
'Button_2454', \
'Button_2458', \
'Button_2364', 'Button_2365', 'Button_2366', 'Button_2367', 'Button_2368', 'Button_2360', \
'ff1_fiction1', 'ff1_fact2', 'ff1_fact3', 'Button_1989', \
'Button_2377', 'Button_2088', \
'Button_2061', \
'Button_2184', \
'Button_2383']

QLD_SCRIPT = ['Button_2016', \
'Button_2212', 'Button_2213', 'Button_2214', 'Button_2206', \
'Button_2487', 'Button_2485', 'Button_2631', \
'Button_1973', 'Button_2633', \
('dd_hobart', 'dd_target'), 'si111288', 'Button_2635', \
'Button_2484', 'Button_2482', 'Button_2483', 'Button_2637', \
'Button_2639', \
'Button_2139', 'Button_2173', 'Button_2641', \
'Button_2643', \
'Button_2645', \
'a1_rb1', 'a1_submit', 'Button_2647', \
'Button_2142', 'Button_2174', 'Button_2649', \
'Button_2651', \
'Button_2653', \
'Button_2655', \
'tf1_f', 'tf1_submit', 'Button_2657', \
'Button_2144', 'Button_2165', 'Button_2659', \
'Button_2661', \
'Button_2663', \
'Button_2665', \
'Button_2667', \
'a2_rb3', 'a2_submit', 'Button_2669', \
'Button_2671', \
'Button_2673', \
'Button_2418', 'Button_2420', 'Button_2675', \
'a3_rb3', 'a3_submit', 'Button_2677', \
'Button_2679', \
'Button_2147', 'Button_2176', 'Button_2681', \
'Button_2683', \
'a4_rb2', 'a4_submit', 'Button_2685', \
'Button_2051', 'Button_2284', 'Button_2292', 'Button_2294', 'Button_2296', 'Button_2687', \
'Button_2689', \
'Button_2691', \
'Button_2364', 'Button_2365', 'Button_2366', 'Button_2367', 'Button_2368', 'Button_2693', \
'ff1_fact1', 'ff1_fact2', 'ff1_fact3', 'Button_2695', \
'Button_2462', 'Button_2697', \
'Button_2699', \
'Button_2701', \
'Button_2457']

SA_SCRIPT = ['Button_2016', \
'Button_2212', 'Button_2213', 'Button_2214', 'Button_2206', \
'Button_2503', 'Button_2502', 'Button_1856', \
'Button_1976', 'Button_1966', \
('dd_hobart', 'dd_target'), 'si111288', 'Button_1978', \
'Button_1986', 'Button_1987', 'Button_1981', \
'Button_2522', 'Button_2532', 'Button_2114', 'Button_2175', 'Button_1862', \
'Button_2540', 'Button_2533', 'Button_2444', \
'Button_1873', \
'Button_2451', \
'a1_rb2', 'a1_submit', 'Button_2188', \
'Button_2524', 'Button_2534', 'Button_2433', 'Button_2432', 'Button_1895', \
'Button_2458', \
'Button_2539', 'Button_2535', 'Button_2170', 'Button_2167', 'Button_1899', \
'Button_2465', \
'tf1_t', 'tf1_submit', 'Button_2178', \
'Button_2526', 'Button_2536', 'Button_1903', \
'Button_2472', \
'Button_2143', 'Button_2172', 'Button_1907', \
'Button_2477', \
'a2_rb2', 'a2_submit', 'Button_2225', \
'Button_2528', 'Button_2537', 'Button_1911', \
'Button_2484', \
'Button_2530', 'Button_2538', 'Button_2144', 'Button_2165', 'Button_1915', \
'Button_2489', \
'q2_t', 'Button_2440', 'Button_2435', \
'Button_1919', \
'Button_2496', \
['Button_2507', 'Button_2549'], ['Button_2509', 'Button_2551'], \
    ['Button_2511', 'Button_2553'], ['Button_2513', 'Button_2555'], \
    ['Button_2515', 'Button_2557'], ['Button_2504', 'Button_2560'], \
'Button_2518', \
'Button_2049', \
'Button_2364', 'Button_2365', 'Button_2366', 'Button_2367', 'Button_2368', 'Button_2360', \
'ff1_fiction1', 'ff1_fiction2', 'ff1_fact3', 'Button_1989', \
'Button_2377', 'Button_2088', \
'Button_2061', \
'Button_2184', \
'Button_2383']

TAS_SCRIPT = ['Button_2016', \
'Button_2212', 'Button_2213', 'Button_2214', 'Button_2206', \
'Button_2493', 'Button_2492', 'Button_1856', \
'Button_1972', 'Button_1966', \
('Image_1621', 'dd_target'), 'si138403', 'Button_1978', \
'Button_1986', ['Button_1987', 'Image_1316'], 'Button_1981', \
    ['Button_2504', 'Button_2510[style*="z-index: 6"]', 'Image_1220'], \
'Button_2114', 'Button_2175', 'Button_1862', \
'Button_2139', 'Button_2173', 'Button_1873', \
'Button_2500', 'Button_2501', 'Button_1895', \
'Button_2170', 'Button_2167', 'Button_1899', \
'a1_rb1', 'a1_submit', 'Button_2188', \
'Button_2142', 'Button_2174', 'Button_1903', \
'Button_2143', 'Button_2172', 'Button_1907', \
'tf1_t', 'tf1_submit', 'Button_2178', \
'Button_1911', \
'Button_1915', \
'a2_rb2', 'a2_submit', 'Button_2225', \
'Button_2145', 'Button_2166', 'Button_1919', \
'Button_2169', 'Button_2171', 'Button_1923', \
'a3_rb1', 'a3_submit', 'Button_2192', \
'Button_1927', \
'Button_2147', 'Button_2176', 'Button_1931', \
'a4_rb2', 'a4_submit', 'Button_2158', \
'Button_1935', \
'Button_2149', 'Button_2164', 'Button_1939', \
'Button_1943', \
'Button_1947', \
'Button_2051', 'Button_2284', 'Button_2292', 'Button_2294', 'Button_2296', 'Button_2049', \
'Button_2433', \
'Button_2364', 'Button_2365', 'Button_2366', 'Button_2367', 'Button_2368', 'Button_2360', \
'ff1_fiction1', 'ff1_fact2', 'ff1_fact3', 'Button_1989', \
'Button_2377', 'Button_2088', \
'Button_2061', \
'Button_2184', \
'Button_2383']

VIC_SCRIPT = ['Button_2016', \
'Button_2212', 'Button_2213', 'Button_2214', 'Button_2206', \
'Button_2489', 'Button_2490', 'Button_1856', \
'Button_1970', 'Button_1966', \
('dd_Melbourne', 'dd_target'), 'si111288', 'Button_1978', \
'Button_1986', 'Button_1987', 'Button_1981', \
'Button_2594', 'Button_2590', \
'Button_2114', 'Button_2175', 'Button_1862', \
'Button_2139', 'Button_2173', 'Button_1873', \
'Button_2399', 'Button_2398', 'Button_1895', \
'Button_1903', \
'Button_2527', 'Button_2531', 'Button_2143', 'Button_2172', 'Button_1907', \
'Button_2403', \
'tf1_f', 'tf1_submit', 'Button_2600', \
'Button_2528', 'Button_2536', 'Button_1911', \
'Button_2144', 'Button_2165', 'Button_1915', \
'Button_2543', 'Button_2544', 'Button_2408', \
'a2_rb1', 'a2_submit', 'Button_2225', \
'Button_2529', 'Button_2537', 'Button_2145', 'Button_2166', 'Button_1919', \
'Button_2530', 'Button_2538', 'Button_2169', 'Button_2171', 'Button_1923', \
'Button_2416', 'Button_2419', 'Button_2601', \
'Button_2532', 'Button_2539', 'Button_2425', 'Button_2424', 'Button_1927', \
'Button_2533', 'Button_2540', 'Button_1931', \
'Button_2432', 'Button_2431', 'Button_2426', \
'a4_rb3', 'a4_submit', 'Button_2158', \
'Button_2534', 'Button_2541', 'Button_2438', 'Button_2439', 'Button_2433', \
'Button_2440', \
'Button_2535', 'Button_2542', 'Button_2447', \
'tf3_nm', 'Button_2458', 'Button_2453', \
'Button_2051', 'Button_2284', 'Button_2292', 'Button_2294', 'Button_2296', 'Button_2049', \
'Button_2492', \
'Button_2495', \
'Button_2498', \
'Button_2521', 'Button_2522', 'Button_2523', 'Button_2524', 'Button_2525', 'Button_2501', \
'ff1_fiction1', 'ff1_fact2', 'ff1_fiction3', 'Button_1989', \
'Button_2377', 'Button_2088', \
'Button_2061', \
'Button_2184', \
'Button_2383']

WA_SCRIPT = ['Button_2016', \
'Button_2212', 'Button_2213', 'Button_2214', 'Button_2206', \
'Button_2448', 'Button_2449', 'Button_1856', \
'Button_1974', 'Button_2496', \
('Image_1290', 'dd_target'), 'si111288', 'Button_1978', \
'Button_1986', 'Button_1987', 'Button_1981', \
'Button_2486', 'Button_2488', \
'Button_2114', 'Button_2175', 'Button_1862', \
'Button_2453', 'Button_2499', 'Button_1873', \
'Button_2455', 'Button_2500', 'Button_2170', 'Button_2167', 'Button_1899', \
'a1_rb2', 'a1_submit', 'Button_2188', \
'Button_2457', 'Button_2501', 'Button_2142', 'Button_2174', 'Button_1903', \
'Button_2458', 'Button_2502', 'Button_1907', \
'tf1_f', 'tf1_submit', 'Button_2178', \
'Button_2460', 'Button_2503', 'Button_2144', 'Button_2165', 'Button_1915', \
'Button_2462', 'Button_2504', 'Button_2410', 'Button_2412', 'Button_2407', \
'a2_rb2', 'a2_submit', 'Button_2225', \
'Button_2464', 'Button_2506', 'Button_1919', \
'Button_2465', 'Button_2505', 'Button_2169', 'Button_2171', 'Button_1923', \
'tf2_f_btn', 'Button_2480', 'Button_2475', \
'Button_2466', 'Button_2507', 'Button_2147', 'Button_2176', 'Button_1931', \
'Button_2467', 'Button_2508', 'Button_2417', 'Button_2418', 'Button_2414', \
'Button_2468', 'Button_2509', 'Button_2424', 'Button_2427', 'Button_2421', \
'a4_rb3', 'a4_submit', 'Button_2158', \
'Button_2051', 'Button_2284', 'Button_2292', 'Button_2294', 'Button_2296', 'Button_2049', \
'Button_2550', ['Button_2558', 'tt1_img'], \
'Button_2364', 'Button_2365', 'Button_2366', 'Button_2490', 'Button_2491', 'Button_2360', \
'ff1_fact1', 'ff1_fact2', 'ff1_fact3', 'Button_1989', \
'Button_2377', 'Button_2088', \
'Button_2061', \
'Button_2184', \
['Button_2383', 'Button_2553']]

ABORIGINAL_SCRIPT = ['Button_33', \
'Button_29', 'Button_30', 'Button_31', 'Button_18', \
'Button_195', \
'Button_295', \
'Button_287', 'Button_288', 'Button_283', \
'Button_310', 'Button_311', 'Button_306', \
'Button_300', 'Button_303', 'Button_298', \
'Button_293', 'Button_294', 'Button_289', \
'Button_314', \
('DD1_Drag1', 'DD1_Drop2'), ('DD1_Drag2', 'DD1_Drop1'), \
    ('DD1_Drag3', 'DD1_Drop3'), 'si14422', 'Button_103', \
'Button_602', 'Button_603', 'Button_326', \
'Button_65', \
'Button_335', 'Button_336', 'Button_332', \
('DD2_Drag1', 'DD2_Drop2'), ('DD2_Drag2', 'DD2_Drop1'), \
    ('DD2_Drag3', 'DD2_Drop3'), 'Button_10', 'Button_316', \
'Button_604', 'Button_605', 'Button_341', \
'Button_347', \
'Button_353', \
's13_radio1', 'Button_235', 'Button_230', \
'Button_612', 'Button_613', 'Button_360', \
'Button_366', \
'Button_384', \
'Button_372', \
('DD3_Drag3', 'DD3_Drop1'), ('DD3_Drag2', 'DD3_Drop2'), \
    ('DD3_Drag1', 'DD3_Drop3'), 'Button_12', 'Button_387', \
'Button_614', 'Button_615', 'Button_397', \
'Button_715', 'Button_716', 'Button_403', \
'Button_409', \
'Button_423', 'Button_420', 'Button_415', \
'Button_611', 'Button_610', 'Button_429', \
'Button_435', \
'Button_441', \
's31_r3', 'Button_450', 'Button_445', \
'Button_606', 'Button_607', 'Button_459', \
'Button_465', \
'Button_471', \
'Button_477', \
('DD4_Drag1', 'DD4_Drop1'), ('DD4_Drag2', 'DD4_Drop3'), \
    ('DD4_Drag3', 'DD4_Drop2'), 'Button_14', 'Button_480', \
'Button_608', 'Button_609', 'Button_490', \
'Button_511', 'Button_519', 'Button_502', \
'Button_508', \
'Button_271', 'Button_273', 'Button_268', \
'Button_616', 'Button_617', 'Button_524', \
'Button_530', \
'Button_536', \
('DD5_Drag1', 'DD5_Drop3'), ('DD5_Drag2', 'DD5_Drop1'), \
    ('DD5_Drag3', 'DD5_Drop2'), 'Button_16', 'Button_539', \
'Button_548']

GOLF_SCRIPT = ['Button_866', \
'Button_29', 'Button_30', 'Button_31', 'Button_18', \
'Button_691', 'Button_692', 'Button_688', \
'Button_702', 'Button_701', 'Button_696', \
'Button_325', 'Button_327', 'Button_323', \
'Button_800', 'Button_801', 'Button_802', 'Button_982', \
'Button_810', 'Button_811', 'Button_812', 'Button_806', \
'Button_984', \
'Button_895', 'Button_889', 'Button_884', \
'Button_851', 'Button_850', 'Button_816', \
'Button_839', \
('Text_Caption_1795', 'SmartShape_462'), ('Text_Caption_1796', 'SmartShape_460'), \
    ('Text_Caption_1797', 'SmartShape_461'), 'Button_38', 'Button_846', \
's53_mc1_a', 'Button_662', 'Button_657', \
'Button_548', 'Button_550', 'Button_546', \
'Button_833', \
'Button_257', \
('nswdd1', 'SmartShape_213'), ('nswdd2', 'SmartShape_216'), 'Button_10', 'Button_554', \
'Button_749', 'Button_751', 'Button_746', \
['Button_708', 'Button_988', 'Button_989'], ['Button_710', 'Button_994'], \
    ['Button_706', 'Button_990'], \
'Button_757', \
'Button_767', 'Button_766', 'Button_763', \
('Text_Caption_1612', 'SmartShape_398'), ('Text_Caption_1613', 'SmartShape_397'), \
    'Button_34', 'Button_771', \
'Button_736', 'Button_734', 'Button_729', \
'Button_309', 'Button_311', 'Button_307', \
'Button_779', \
's39_a_mc1', 'Button_637', 'Button_632', \
'Button_295', 'Button_297', 'Button_293', \
'Button_786', \
's32_f_a', 'Button_626', 'Button_621', \
'Button_855', \
'Button_876', 'Button_877', 'Button_873', \
'Button_880', \
'Button_684']

LODGES_SCRIPT = ['Button_33', \
'Button_29', 'Button_30', 'Button_31', 'Button_18', \
'Button_195', \
'Button_569', \
'Button_527', 'Button_528', 'Button_56', \
'Button_65', \
'Button_206', \
'Button_90', \
'Button_526', 'Button_276', 'Button_99', \
('ACT_Drag1', 'ACT_Drop2'), ('ACT_Drag2', 'ACT_Drop1'), \
    ('ACT_Drag3', 'ACT_Drop3'), 'si14422', 'Button_106', \
'Button_270', 'Button_273', 'Button_268', \
'Button_529', 'Button_530', 'Button_244', \
'Button_257', \
'Button_285', 'Button_286', 'Button_282', \
('Text_Caption_613', 'SmartShape_120'), ('Text_Caption_614', 'SmartShape_119'), \
    'Button_10', 'Button_290', \
's13_radio1', 'Button_235', 'Button_230', \
'Button_531', 'Button_532', 'Button_297', \
'Button_305', \
'Button_311', \
'Button_317', \
('Text_Caption_1185', 'SmartShape_263'), ('Text_Caption_1186', 'SmartShape_262'), \
    'Button_23', 'Button_544', \
's21_tf1', 'Button_357', 'Button_352', \
'Button_533', 'Button_534', 'Button_366', \
'Button_374', \
'Button_391', 'Button_392', 'Button_382', \
'Button_388', \
('Text_Caption_1204', 'SmartShape_273'), ('Text_Caption_1205', 'SmartShape_272'), \
    ('Text_Caption_1206', 'SmartShape_275'), 'Button_26', 'Button_550', \
's27_tf2', 'Button_405', 'Button_400', \
'Button_535', 'Button_536', 'Button_414', \
'Button_422', \
'Button_428', \
'Button_434', \
'Button_440', \
'Button_448', \
('Text_Caption_1217', 'SmartShape_282'), ('Text_Caption_1218', 'SmartShape_281'), \
    ('Text_Caption_1219', 'SmartShape_284'), 'Button_28', 'Button_556', \
's35_tf2', 'Button_463', 'Button_458', \
'Button_537', 'Button_538', 'Button_472', \
'Button_480', \
's38_tf1', 'Button_489', 'Button_484', \
'Button_539', 'Button_540', 'Button_498', \
'Button_506', \
'Button_518', 'Button_515', 'Button_510', \
'Button_559', \
'Button_525']

RA_SCRIPT = ['Button_33', \
'Button_29', 'Button_30', 'Button_31', 'Button_18', \
'Button_195', \
'Button_76', 'Button_75', 'Button_56', \
'Button_71', 'Button_74', 'Button_65', \
'Button_206', \
'Button_90', \
'Button_99', \
('Text_Caption_1479', 'SmartShape_360'), ('Text_Caption_1480', 'SmartShape_359'), \
    ('Text_Caption_1481', 'SmartShape_363'), 'Button_28', 'Button_702', \
's13_radio2', 'Button_235', 'Button_230', \
'Button_548', 'Button_550', 'Button_546', \
'Button_156', \
'Button_257', \
'Button_264', \
'Button_177', \
('Text_Caption_1505', 'SmartShape_372'), ('Text_Caption_1506', 'SmartShape_374'), \
    ('Text_Caption_1507', 'SmartShape_373'), 'Button_34', 'Button_708', \
's18_mc1_a', 'Button_538', 'Button_533', \
'Button_281', 'Button_283', 'Button_279', \
'Button_369', 'Button_366', 'Button_287', \
'Button_363', \
'Button_373', \
'Button_379', \
('Text_Caption_1519', 'SmartShape_382'), ('Text_Caption_1520', 'SmartShape_383'), \
    ('Text_Caption_1521', 'SmartShape_381'), 'Button_36', 'Button_715', \
's25_t_a', 'Button_614', 'Button_609', \
'Button_295', 'Button_297', 'Button_293', \
'Button_521', \
'Button_508', \
'Button_301', \
'Button_528', \
('Text_Caption_1539', 'SmartShape_392'), ('Text_Caption_1540', 'SmartShape_394'), \
    ('Text_Caption_1541', 'SmartShape_393'), 'Button_38', 'Button_722', \
's32_t_a', 'Button_626', 'Button_621', \
'Button_309', 'Button_311', 'Button_307', \
'Button_396', 'Button_395', 'Button_339', \
'Button_391', \
'Button_403', 'Button_404', 'Button_400', \
'Button_413', 'Button_412', 'Button_408', \
('Text_Caption_1559', 'SmartShape_404'), ('Text_Caption_1560', 'SmartShape_403'), \
    ('Text_Caption_1561', 'SmartShape_405'), 'Button_40', 'Button_729', \
's39_a_mc1', 'Button_637', 'Button_632', \
'Button_317', 'Button_319', 'Button_315', \
'Button_345', \
'Button_423', \
'Button_417', \
'Button_429', \
('Text_Caption_1579', 'SmartShape_415'), ('Text_Caption_1580', 'SmartShape_416'), \
    ('Text_Caption_1581', 'SmartShape_414'), 'Button_42', 'Button_736', \
's46_mc3_a', 'Button_650', 'Button_645', \
'Button_325', 'Button_327', 'Button_323', \
'Button_432', 'Button_433', 'Button_351', \
'Button_437', \
'Button_446', \
'Button_456', 'Button_457', 'Button_452', \
('Text_Caption_1599', 'SmartShape_427'), ('Text_Caption_1600', 'SmartShape_425'), \
    ('Text_Caption_1601', 'SmartShape_426'), 'Button_44', 'Button_743', \
's53_mc3_a', 'Button_662', 'Button_657', \
'Button_333', 'Button_335', 'Button_331', \
'Button_461', \
'Button_357', \
'Button_474', \
'Button_488', \
('Text_Caption_1613', 'SmartShape_434'), ('Text_Caption_1614', 'SmartShape_436'), \
    ('Text_Caption_1615', 'SmartShape_435'), 'Button_46', 'Button_749', \
's60_mc2_a', 'Button_674', 'Button_669', \
'Button_684']

WALKS_SCRIPT = ['Button_33', \
'Button_29', 'Button_30', 'Button_31', 'Button_18', \
'Button_566', \
'Button_720', \
'Button_724', \
'Button_270', 'Button_273', 'Button_268', \
'Button_533', 'Button_534', 'Button_366', \
'Button_593', \
'Button_731', \
's27_tf1', 'Button_405', 'Button_400', \
'Button_539', 'Button_540', 'Button_498', \
'Button_579', \
'Button_737', \
'Button_743', \
'Button_749', \
'Button_755', \
'Button_761', \
'Button_767', \
'Button_773', \
('ACT_Drag1', 'ACT_Drop2'), ('ACT_Drag2', 'ACT_Drop1'), \
    ('ACT_Drag3', 'ACT_Drop3'), 'si14422', 'Button_106', \
's13_radio3', 'Button_235', 'Button_230', \
'Button_669', 'Button_670', 'Button_666', \
'Button_779', \
'Button_785', \
's21_tf1', 'Button_357', 'Button_352', \
('Text_Caption_1204', 'SmartShape_275'), ('Text_Caption_1205', 'SmartShape_272'), \
    ('Text_Caption_1206', 'SmartShape_273'), 'Button_26', 'Button_550', \
'Button_806', 'Button_807', 'Button_803', \
'Button_791', \
'Button_811', \
's35_tf2', 'Button_463', 'Button_458', \
'Button_821', 'Button_822', 'Button_818', \
'Button_826', \
'Button_832', \
's38_tf1', 'Button_489', 'Button_484', \
'Button_835', \
'Button_859', \
'Button_525']

WINE_SCRIPT = ['Button_33', \
'Button_29', 'Button_30', 'Button_31', 'Button_18', \
'Button_195', \
'Button_566', \
'Button_527', 'Button_528', 'Button_56', \
'Button_573', \
'Button_579', \
'Button_585', \
('ACT_Drag2', 'ACT_Drop1'), ('ACT_Drag1', 'ACT_Drop2'), \
    ('ACT_Drag3', 'ACT_Drop3'), 'si14422', 'Button_106', \
'Button_588', 'Button_273', 'Button_268', \
'Button_533', 'Button_534', 'Button_366', \
'Button_593', \
'Button_599', \
's27_tf1', 'Button_405', 'Button_400', \
's13_radio1', 'Button_235', 'Button_230', \
'Button_609', 'Button_720', 'Button_606', \
'Button_614', \
'Button_620', \
'Button_630', 'Button_721', 'Button_627', \
'Button_647', \
('Text_Caption_1204', 'SmartShape_273'), ('Text_Caption_1205', 'SmartShape_272'), \
    ('Text_Caption_1206', 'SmartShape_275'), 'Button_26', 'Button_550', \
'Button_531', 'Button_532', 'Button_297', \
'Button_653', \
's21_tf1', 'Button_357', 'Button_352', \
'Button_537', 'Button_538', 'Button_472', \
'Button_659', \
'Button_669', 'Button_722', 'Button_666', \
'Button_674', \
'Button_684', 'Button_724', 'Button_681', \
'Button_689', \
('Text_Caption_1218', 'SmartShape_281'), ('Text_Caption_1217', 'SmartShape_282'), \
    ('Text_Caption_1219', 'SmartShape_284'), 'Button_28', 'Button_556', \
's35_tf1', 'Button_463', 'Button_458', \
'Button_539', 'Button_540', 'Button_498', \
'Button_695', \
'Button_705', 'Button_725', 'Button_702', \
'Button_710', \
'Button_716', \
's38_tf2', 'Button_489', 'Button_484', \
'Button_525']

AQUATIC_SCRIPT = ['Button_5', \
'Button_12', 'Button_13', 'Button_14', 'Button_9', \
'Button_20', \
'Button_215', 'Button_731', 'Button_282', 'Button_281', 'Button_212', \
'Button_744', \
'Button_771', 'Button_773', 'Button_770', 'Button_772', 'Button_768', \
'Button_440', 'Button_441', 'Button_409', 'Button_410', 'Button_407', \
'Button_448', 'Button_449', 'Button_415', 'Button_416', 'Button_413', \
'Button_450', 'Button_451', 'Button_421', 'Button_422', 'Button_419', \
'Button_452', 'Button_453', 'Button_433', 'Button_434', 'Button_431', \
('Text_Caption_764', 'SmartShape_178'), ('Text_Caption_765', 'SmartShape_180'), \
    ('Text_Caption_766', 'SmartShape_179'), 'Button_36', 'Button_435', \
'Button_174', 'Button_736', 'Button_299', 'Button_300', 'Button_171', \
'Button_778', \
'Button_302', 'Button_303', 'Button_285', \
'Button_308', 'Button_309', 'Button_306', \
'Button_314', 'Button_315', 'Button_312', \
'Button_320', 'Button_321', 'Button_318', \
('Text_Caption_385', 'SmartShape_120'), ('Text_Caption_386', 'SmartShape_119'), \
    ('Text_Caption_387', 'SmartShape_121'), 'Button_2', 'Button_322', \
'Button_328', 'Button_331', 'Button_326', \
'Button_782', 'Button_783', 'Button_163', 'Button_737', 'Button_337', 'Button_338', 'Button_160', \
'Button_774', \
'Button_343', 'Button_344', 'Button_341', \
'Button_349', 'Button_350', 'Button_347', \
'Button_355', 'Button_356', 'Button_353', \
'Button_361', 'Button_362', 'Button_359', \
('Text_Caption_523', 'SmartShape_149'), ('Text_Caption_524', 'SmartShape_150'), \
    ('Text_Caption_525', 'SmartShape_148'), 'Button_4', 'Button_371', \
'Button_367', 'Button_365', 'Button_363', \
'Button_153', 'Button_738', 'Button_146', \
'Button_502', \
'Button_524', 'Button_525', 'Button_510', 'Button_511', 'Button_508', \
'Button_526', 'Button_527', 'Button_469', 'Button_470', 'Button_467', \
'Button_528', 'Button_529', 'Button_475', 'Button_476', 'Button_473', \
'Button_530', 'Button_531', 'Button_522', 'Button_523', 'Button_520', \
('Text_Caption_876', 'SmartShape_203'), ('Text_Caption_877', 'SmartShape_202'), \
    ('Text_Caption_878', 'SmartShape_201'), 'Button_38', 'Button_489', \
'Button_784', 'Button_785', 'Button_195', 'Button_739', 'Button_191', \
'Button_756', \
'Button_760', 'Button_761', 'Button_762', 'Button_763', 'Button_547', 'Button_548', 'Button_545', \
'Button_764', 'Button_765', 'Button_583', 'Button_584', 'Button_581', \
'Button_589', 'Button_590', 'Button_587', \
'Button_595', 'Button_596', 'Button_593', \
('Text_Caption_1063', 'SmartShape_232'), ('Text_Caption_1064', 'SmartShape_233'), \
    ('Text_Caption_1065', 'SmartShape_234'), 'Button_40', 'Button_567', \
'Button_786', 'Button_787', 'Button_184', 'Button_742', 'Button_670', 'Button_669', 'Button_181', \
'Button_689', \
'Button_717', 'Button_718', 'Button_634', 'Button_635', 'Button_632', \
'Button_719', 'Button_720', 'Button_675', 'Button_676', 'Button_673', \
'Button_721', 'Button_722', 'Button_681', 'Button_682', 'Button_679', \
'Button_723', 'Button_724', 'Button_687', 'Button_688', 'Button_685', \
('Text_Caption_1277', 'SmartShape_275'), ('Text_Caption_1278', 'SmartShape_274'), \
    ('Text_Caption_1279', 'SmartShape_276'), 'Button_42', 'Button_654', \
'Button_788', 'Button_789', 'Button_205', 'Button_741', 'Button_376', 'Button_375', 'Button_202', \
'Button_748', \
'Button_381', 'Button_382', 'Button_379', \
'Button_391', 'Button_392', 'Button_389', \
'Button_397', 'Button_398', 'Button_395', \
'Button_403', 'Button_404', 'Button_401', \
('Text_Caption_577', 'SmartShape_161'), ('Text_Caption_578', 'SmartShape_162'), \
    ('Text_Caption_579', 'SmartShape_160'), 'Button_34', 'Button_383', \
'Button_790', 'Button_791', 'Button_29', 'Button_743', 'Button_693', 'Button_694', 'Button_27', \
'Button_752', \
'Button_699', 'Button_700', 'Button_697', \
'Button_727', 'Button_728', 'Button_705', 'Button_706', 'Button_703', \
'Button_729', 'Button_730', 'Button_711', 'Button_712', 'Button_709', \
('Text_Caption_1433', 'SmartShape_297'), ('Text_Caption_1434', 'SmartShape_299'), \
    ('Text_Caption_1435', 'SmartShape_298'), 'Button_44', 'Button_713', \
'Button_269']

SCRIPTS = {'1': MOD_1_SCRIPT, '2': MOD_2_SCRIPT, '3': MOD_3_SCRIPT, \
'act': ACT_SCRIPT, 'nsw': NSW_SCRIPT, 'nt': NT_SCRIPT, 'qld': QLD_SCRIPT, \
'sa': SA_SCRIPT, 'tas': TAS_SCRIPT, 'vic': VIC_SCRIPT, 'wa': WA_SCRIPT, \
'aboriginal': ABORIGINAL_SCRIPT, 'golf': GOLF_SCRIPT, 'lodges': LODGES_SCRIPT, \
'ra': RA_SCRIPT, 'walks': WALKS_SCRIPT, 'wine': WINE_SCRIPT, 'aquatic': AQUATIC_SCRIPT}
