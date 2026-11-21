# Friday 20 November 2026 — the day in 35 stories.
#
# Each record holds one story that happened, or was first reported, on
# that Friday, in any time zone. Story fields:
#   num      running number on the page, 1 to 35
#   kicker   place and beat, printed above the headline
#   dateline city or cities the story is filed from
#   headline the story in one short line
#   deck     one or two plain sentences, as reported
#   source   newsroom the facts are attributed to
#   chip     REPORTED / ONGOING / CLAIM / ESTIMATE, or blank
#   region   tally bucket for the region bar
#   lon/lat  pin position on the world map
#   scene    which painted scene illustrates the card
#
# Briefs carry a parallel region list, one bucket per brief, in the
# same order as BRIEF_ITEMS. Regions tally to 35: Europe 10, Asia 9,
# Middle East 3, Africa 1, Americas 9, Oceania 2, Global 1.

HERO_STORIES = [
    {
        "num": 1,
        "kicker": "KYIV - WAR",
        "dateline": "KYIV, UKRAINE",
        "headline": "Russian missiles hit three Kyiv bridges",
        "deck": "Missiles struck the Darnytskyi, Pivdennyi and "
        "Podilsko-Voskresenskyi bridges, killing three and wounding 15 "
        "- the war's biggest bridge attack.",
        "source": "REUTERS - KYIV INDEPENDENT",
        "chip": "REPORTED",
        "region": "EUROPE",
        "lon": 30.5,
        "lat": 50.45,
        "scene": "kyiv_bridges",
    },
    {
        "num": 2,
        "kicker": "ODISHA - STORM",
        "dateline": "GOPALPUR - BAY OF BENGAL",
        "headline": "Cyclone Akvan comes ashore in eastern India",
        "deck": "The storm crossed the coast near Gopalpur from about 8 am, "
        "after more than 300,000 people were moved to shelters. "
        "No deaths were reported.",
        "source": "IMD - DECCAN HERALD",
        "chip": "REPORTED",
        "region": "ASIA",
        "lon": 84.9,
        "lat": 19.3,
        "scene": "akvan_spiral",
    },
    {
        "num": 3,
        "kicker": "ASIA - MARKETS",
        "dateline": "TAIPEI - SEOUL - TOKYO",
        "headline": "AI sell-off sinks Asia's stock markets",
        "deck": "Taiwan's index fell 6.2% to end its worst week since 1991. "
        "Seoul lost 5.2% and Tokyo 5.1% as chipmakers led the slide.",
        "source": "AL JAZEERA - ANADOLU",
        "chip": "",
        "region": "ASIA",
        "lon": 121.6,
        "lat": 25.0,
        "scene": "market_slide",
    },
]

MID_STORIES = [
    {
        "num": 4,
        "kicker": "BRUSSELS - DIPLOMACY",
        "dateline": "BRUSSELS",
        "headline": "UK and EU seal a \u201creset\u201d deal",
        "deck": "Food trade, youth visas, carbon link. "
        "100,000 youth visas a year.",
        "source": "REUTERS",
        "chip": "",
        "region": "EUROPE",
        "lon": 4.35,
        "lat": 50.85,
        "scene": "reset_table",
    },
    {
        "num": 5,
        "kicker": "ANTALYA - CLIMATE",
        "dateline": "ANTALYA - COP31 FINAL DAY",
        "headline": "COP31 reaches its last day with no deal",
        "deck": "The draft drops fossil fuels; talks run past "
        "the Friday deadline.",
        "source": "UN NEWS",
        "chip": "ONGOING",
        "region": "EUROPE",
        "lon": 30.7,
        "lat": 36.9,
        "scene": "cop31_hall",
    },
    {
        "num": 6,
        "kicker": "HORMUZ - ENERGY",
        "dateline": "STRAIT OF HORMUZ",
        "headline": "Oil falls a third week as Hormuz flows recover",
        "deck": "Brent near $92. Iran's Guards claim two tankers hit mines.",
        "source": "REUTERS",
        "chip": "CLAIM",
        "region": "MIDDLE EAST",
        "lon": 56.5,
        "lat": 26.6,
        "scene": "hormuz_tanker",
    },
    {
        "num": 7,
        "kicker": "WASHINGTON - POLITICS",
        "dateline": "US SENATE",
        "headline": "Senate refuses to curb Trump's Iran war",
        "deck": "War-powers vote fails 48-51; Democrats vow a 2027 "
        "funding fight.",
        "source": "REUTERS - AP",
        "chip": "",
        "region": "AMERICAS",
        "lon": -77.0,
        "lat": 38.9,
        "scene": "senate_dome",
    },
    {
        "num": 8,
        "kicker": "JAKARTA - DIPLOMACY",
        "dateline": "JAKARTA - BEIJING",
        "headline": "Prabowo and Xi talk South China Sea",
        "deck": "The two leaders discuss trade, investment and "
        "the disputed sea.",
        "source": "REUTERS",
        "chip": "",
        "region": "ASIA",
        "lon": 106.8,
        "lat": -6.2,
        "scene": "jakarta_beijing",
    },
    {
        "num": 9,
        "kicker": "THE HAGUE - JUSTICE",
        "dateline": "MYANMAR ANSWERS THE COURT",
        "headline": "Myanmar calls the genocide ruling \u2018unfair\u2019",
        "deck": "Naypyidaw rejects the verdict; Dhaka floats returns "
        "in 1-1.5 years.",
        "source": "REUTERS",
        "chip": "",
        "region": "ASIA",
        "lon": 4.3,
        "lat": 52.1,
        "scene": "hague_court",
    },
    {
        "num": 10,
        "kicker": "GAZA - WAR",
        "dateline": "CENTRAL GAZA",
        "headline": "Israeli forces cross the truce line in Gaza",
        "deck": "First ground incursion since the ceasefire; families flee.",
        "source": "REUTERS",
        "chip": "REPORTED",
        "region": "MIDDLE EAST",
        "lon": 34.5,
        "lat": 31.5,
        "scene": "gaza_line",
    },
    {
        "num": 11,
        "kicker": "WELLINGTON - CRICKET",
        "dateline": "FIRST TEST - DAY TWO",
        "headline": "Phillips hits 118 against India",
        "deck": "Nicholls 175* and Phillips (118) add 216 after 70-5. "
        "India reply 159-1.",
        "source": "ICC",
        "chip": "",
        "region": "OCEANIA",
        "lon": 174.8,
        "lat": -41.3,
        "scene": "cricket_pitch",
    },
    {
        "num": 12,
        "kicker": "WORLDWIDE - GAMES",
        "dateline": "LAUNCH DAY TOTALS",
        "headline": "GTA VI's first day: an estimated $2.36bn",
        "deck": "24.6m copies on day one, near 3x GTA V, plus 125m "
        "stream hours.",
        "source": "SENSOR TOWER - VGC",
        "chip": "ESTIMATE",
        "region": "GLOBAL",
        "lon": -74.0,
        "lat": 40.7,
        "scene": "gta_city",
    },
    {
        "num": 13,
        "kicker": "TOKYO - ECONOMY",
        "dateline": "TOKYO",
        "headline": "Japan's inflation picks up to 2.3%",
        "deck": "A December rate rise stays in view. Core inflation "
        "above 2% again.",
        "source": "REUTERS",
        "chip": "",
        "region": "ASIA",
        "lon": 139.7,
        "lat": 35.7,
        "scene": "tokyo_yen",
    },
]

# Short items, one line each on the page, numbered 14 to 35.
# Each tuple: number, city, one-line text, source, longitude, latitude.
BRIEF_ITEMS = [
    (14, "Gopalpur", "Odisha assembly adjourns to 23 Nov as Akvan crosses.", "IMD", 86.5, 17.5),
    (15, "Puri", "69 trains cancelled in the cyclone zone; 423 rescue teams out.", "PTI", 85.8, 21.5),
    (16, "Warsaw", "Poland probes objects that fell near the Ukraine border.", "Reuters", 21.0, 52.2),
    (17, "Brussels", "EU summons Russia's envoy over Kyiv embassy damage.", "Euronews", 4.4, 50.9),
    (18, "London", "Britain pledges 1,000+ drones for Ukraine, GBP 260m.", "UK MoD", -0.6, 53.5),
    (19, "Moscow", "Ryabkov rejects NATO-style security guarantees for Ukraine.", "Reuters", 37.6, 55.8),
    (20, "Baghdad", "Iraqi forces to deploy in militia stronghold Jurf al-Sakhar.", "Reuters", 44.4, 33.3),
    (21, "New York", "Dollar index at 103.9, highest since April 2025.", "Reuters", -73.0, 39.0),
    (22, "Cook Islands", "Record November cyclone Xavier weakens near Manihiki.", "NASA", -159.8, -21.2),
    (23, "San Salvador", "President Bukele registers to seek a third term.", "AP", -89.2, 13.7),
    (24, "Buenos Aires", "Senate approves permanent disability framework, 71-0.", "Telam", -58.4, -34.6),
    (25, "Paris", "Kamala Harris meets Macron amid talk of a 2028 bid.", "AFP", 2.4, 48.9),
    (26, "Zurich", "Diallo and Tashima confirmed as FIFA presidency challengers.", "AFP", 8.5, 47.4),
    (27, "Brasilia", "Lula moves to protect Chief Raoni's birthplace.", "AP", -47.9, -15.8),
    (28, "Port-au-Prince", "Heavy fighting for a key corridor as gangs battle forces.", "AP", -72.3, 18.5),
    (29, "New York", "Security Council ballots on Grynspan's UN top-job bid.", "UN News", -75.5, 42.5),
    (30, "Washington", "US sanctions Comancheros, 'Ndrangheta networks.", "US Treasury", -78.5, 37.0),
    (31, "Washington", "Trump announces posthumous pardon for Pete Rose.", "AP", -84.5, 39.1),
    (32, "London", "589m children live in war zones, a record share.", "Save the Children", -1.5, 50.0),
    (33, "Cotonou", "Benin seeks return of artworks looted by France.", "AFP", 2.6, 6.4),
    (34, "Seoul", "Exchange halts trading briefly as Kospi plunges 5.7%.", "Dow Jones", 127.0, 37.6),
    (35, "Tokyo", "Yen steadies near 159.5 after Japanese inflation data.", "Reuters", 138.0, 34.0),
]

# Region bucket for each brief, in the same order as BRIEF_ITEMS.
BRIEF_REGIONS = [
    "ASIA", "ASIA", "EUROPE", "EUROPE", "EUROPE", "EUROPE",
    "MIDDLE EAST", "AMERICAS", "OCEANIA", "AMERICAS", "AMERICAS",
    "EUROPE", "EUROPE", "AMERICAS", "AMERICAS", "AMERICAS",
    "AMERICAS", "AMERICAS", "EUROPE", "AFRICA", "ASIA", "ASIA",
]

# Six big numbers across the top strip: value plus a one-line label.
NUMBER_STRIP = [
    ("3", "bridges hit in Kyiv"),
    ("300,000+", "evacuated before Akvan"),
    ("-6.2%", "Taiwan index, Friday"),
    ("100,000", "youth visas a year, UK-EU deal"),
    ("2.3%", "Japan CPI, October"),
    ("118", "runs by Phillips vs India"),
]

# Region bar order and paint, left to right across the page.
REGION_ORDER = ["EUROPE", "ASIA", "MIDDLE EAST", "AFRICA", "AMERICAS", "OCEANIA", "GLOBAL"]
REGION_PAINT = {
    "EUROPE": (31, 93, 140),
    "ASIA": (176, 58, 32),
    "MIDDLE EAST": (120, 90, 40),
    "AFRICA": (90, 110, 60),
    "AMERICAS": (96, 60, 130),
    "OCEANIA": (30, 120, 130),
    "GLOBAL": (90, 90, 90),
}

MASTHEAD_KICKER_LEFT = "THE WORLD IN ONE DAY"
MASTHEAD_KICKER_RIGHT = "35 STORIES - 7 REGIONS - EVERY ONE DATED FRIDAY 20 NOVEMBER 2026"
MASTHEAD_DATE = "Friday 20 November 2026"
SUBHEAD_LINE = (
    "Russian missiles hit Kyiv's bridges - Cyclone Akvan strikes India - "
    "An AI sell-off sinks Asia's markets - UK and EU seal a deal"
)

DATE_CHECK_TITLE = "DATE CHECK"
DATE_CHECK_LINES = [
    "Every story on this page happened, or was first reported, on Friday 20 November 2026, in any time zone.",
    "Claims are attributed as reported; figures marked ESTIMATE, CLAIM or ONGOING are not yet settled.",
]

MAP_CAPTION = "Each number is the story with that number on this page."
FOOTER_LINE = (
    "Sources: Reuters, AP, AFP, UN News, IMD, NASA, Sensor Tower, VGC, ICC "
    "- Pictures and map drawn in code - 2026-11-20"
)
BRIEFS_HEADING = "ALSO ON FRIDAY 20 NOVEMBER 2026 - 22 MORE STORIES"
MAP_HEADING = "WHERE IT HAPPENED"
