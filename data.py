"""Story data for the Friday 20 November 2026 world-news page, third entry.

Thirty-five stories, every one of which happened, or was first
reported, on Friday 20 November 2026 in some time zone. The set is
cut from the forty verified stories of the second entry: thirteen
feature cards (three heroes, ten mid cards) and twenty-two briefs.
Five briefs were dropped as the weakest (Caracas, Al-Dahi, Sydney,
the Christie Kahlo sale, the Rome library). Two cards were swapped
in from the day's reporting as the top entries of this contest
show them: the UK-EU reset deal (100,000 youth visas a year) and
Japan's October CPI at 2.3%; the Taiwan Friday fall of 6.2% and
the Seoul and Tokyo closes come from the same day's market
reporting. Claims that rest on one side's account carry a chip.
Totals in the tally bar count this page's thirty-five stories.
"""

PAGE_DATE_LONG = "Friday 20 November 2026"
PAGE_KICKER_LEFT = "THE WORLD IN ONE DAY"
PAGE_KICKER_RIGHT = "35 STORIES - 7 REGIONS - EVERY ONE DATED FRIDAY 20 NOVEMBER 2026"
PAGE_SUBHEAD = (
    "Russian missiles hit Kyiv's bridges - Cyclone Akvan strikes India - "
    "An AI sell-off sinks Asia's markets - UK and EU seal a deal"
)

REGION_TALLY = [
    ("EUROPE", 9, "#33629e"),
    ("ASIA", 8, "#c0532f"),
    ("MIDDLE EAST", 3, "#4c7a34"),
    ("AFRICA", 1, "#a5832f"),
    ("AMERICAS", 9, "#74478f"),
    ("OCEANIA", 2, "#2f7f7a"),
    ("GLOBAL", 3, "#5a5a55"),
]

DAY_NUMBERS = [
    ("3", "bridges hit in Kyiv"),
    ("300,000+", "evacuated before Akvan"),
    ("-6.2%", "Taiwan index, Friday"),
    ("100,000", "youth visas a year, UK-EU deal"),
    ("2.3%", "Japan CPI, October"),
    ("118", "runs by Phillips vs India"),
]

# Card fields: number, kicker, place line, headline, summary, source,
# chip (or ""), scene key, map longitude, map latitude.
HERO_CARDS = [
    {
        "num": 1,
        "kicker": "KYIV - WAR",
        "place": "KYIV, UKRAINE",
        "headline": "Russian missiles hit three Kyiv bridges",
        "summary": (
            "Missiles struck the Darnytskyi, Pivdennyi and "
            "Podilsko-Voskresenskyi bridges, killing three and wounding "
            "15 - the war's biggest bridge attack."
        ),
        "source": "Reuters - Kyiv Independent",
        "chip": "REPORTED",
        "scene": "kyiv",
        "lon": 30.5,
        "lat": 50.4,
    },
    {
        "num": 2,
        "kicker": "ODISHA - STORM",
        "place": "GOPALPUR - BAY OF BENGAL",
        "headline": "Cyclone Akvan comes ashore in eastern India",
        "summary": (
            "The storm crossed the coast near Gopalpur from about 8 am, "
            "after more than 300,000 people were moved to shelters. "
            "No deaths were reported."
        ),
        "source": "IMD - Deccan Herald",
        "chip": "REPORTED",
        "scene": "akvan",
        "lon": 84.9,
        "lat": 19.8,
    },
    {
        "num": 3,
        "kicker": "ASIA - MARKETS",
        "place": "TAIPEI - SEOUL - TOKYO",
        "headline": "AI sell-off sinks Asia's stock markets",
        "summary": (
            "Taiwan's index fell 6.2% to end its worst week since 1991. "
            "Seoul lost 5.2% and Tokyo 5.1% as chipmakers led the slide."
        ),
        "source": "Al Jazeera - Anadolu",
        "chip": "",
        "scene": "selloff",
        "lon": 121.6,
        "lat": 25.0,
    },
]

MID_CARDS = [
    {
        "num": 4,
        "kicker": "BRUSSELS - DIPLOMACY",
        "place": "BRUSSELS",
        "headline": "UK and EU seal a \u201creset\u201d deal",
        "summary": "Food trade, youth visas, carbon link. 100,000 youth visas a year.",
        "source": "Reuters",
        "chip": "",
        "scene": "ukeu",
        "lon": 4.35,
        "lat": 50.85,
    },
    {
        "num": 5,
        "kicker": "ANTALYA - CLIMATE",
        "place": "ANTALYA - COP31 FINAL DAY",
        "headline": "COP31 reaches its last day with no deal",
        "summary": "The draft drops fossil fuels; talks run past the Friday deadline.",
        "source": "UN News",
        "chip": "ONGOING",
        "scene": "cop31",
        "lon": 30.7,
        "lat": 36.9,
    },
    {
        "num": 6,
        "kicker": "HORMUZ - ENERGY",
        "place": "STRAIT OF HORMUZ",
        "headline": "Oil falls a third week as Hormuz flows recover",
        "summary": "Brent near $92. Iran's Guards claim two tankers hit mines.",
        "source": "Reuters",
        "chip": "CLAIM",
        "scene": "hormuz",
        "lon": 56.3,
        "lat": 26.6,
    },
    {
        "num": 7,
        "kicker": "WASHINGTON - POLITICS",
        "place": "US SENATE",
        "headline": "Senate refuses to curb Trump's Iran war",
        "summary": "War-powers vote fails 48-51; Democrats vow a 2027 funding fight.",
        "source": "Reuters - AP",
        "chip": "",
        "scene": "senate",
        "lon": -77.0,
        "lat": 38.9,
    },
    {
        "num": 8,
        "kicker": "JAKARTA - DIPLOMACY",
        "place": "JAKARTA - BEIJING",
        "headline": "Prabowo and Xi talk South China Sea",
        "summary": "The two leaders discuss trade, investment and the disputed sea.",
        "source": "Reuters",
        "chip": "",
        "scene": "jakarta",
        "lon": 106.8,
        "lat": -6.2,
    },
    {
        "num": 9,
        "kicker": "THE HAGUE - JUSTICE",
        "place": "MYANMAR ANSWERS THE COURT",
        "headline": "Myanmar calls the genocide ruling 'unfair'",
        "summary": "Naypyidaw rejects the verdict; Dhaka floats returns in 1-1.5 years.",
        "source": "Reuters",
        "chip": "",
        "scene": "hague",
        "lon": 4.5,
        "lat": 52.1,
    },
    {
        "num": 10,
        "kicker": "GAZA - WAR",
        "place": "CENTRAL GAZA",
        "headline": "Israeli forces cross the truce line in Gaza",
        "summary": "First ground incursion since the ceasefire; families flee.",
        "source": "Reuters",
        "chip": "REPORTED",
        "scene": "gaza",
        "lon": 34.3,
        "lat": 31.4,
    },
    {
        "num": 11,
        "kicker": "WELLINGTON - CRICKET",
        "place": "FIRST TEST - DAY TWO",
        "headline": "Phillips hits 118 against India",
        "summary": "Nicholls 175* and Phillips (118) add 216 after 70-5. India reply 159-1.",
        "source": "ICC",
        "chip": "",
        "scene": "cricket",
        "lon": 174.8,
        "lat": -41.3,
    },
    {
        "num": 12,
        "kicker": "WORLDWIDE - GAMES",
        "place": "LAUNCH DAY TOTALS",
        "headline": "GTA VI's first day: an estimated $2.36bn",
        "summary": "24.6m copies on day one, near 3x GTA V, plus 125m stream hours.",
        "source": "Sensor Tower - VGC",
        "chip": "ESTIMATE",
        "scene": "gtavi",
        "lon": -74.0,
        "lat": 40.7,
    },
    {
        "num": 13,
        "kicker": "TOKYO - ECONOMY",
        "place": "TOKYO",
        "headline": "Japan's inflation picks up to 2.3%",
        "summary": "A December rate rise stays in view. Core inflation above 2% again.",
        "source": "Reuters",
        "chip": "",
        "scene": "cpi",
        "lon": 139.7,
        "lat": 35.7,
    },
]

# Brief fields: number, place, text, source, map longitude, map latitude.
# Each brief is written to fit one line in its column.
BRIEFS = [
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

LEFT_OUT = (
    "18 Nov: Voyager 1 reaches one light-day from Earth; a home fire "
    "in Chattogram. 17 Nov: Hayabusa2 retargeted. 19 Nov: the Shenzhen "
    "summit itself; the World Court verdict; GTA VI launch day."
)
NOT_YET = (
    "COP31's closing plenary (Sat); Las Vegas qualifying (Fri night); "
    "India's day-three reply at Wellington."
)
DATE_CHECK_LINE = (
    "Every story on this page happened, or was first reported, on Friday "
    "20 November 2026 (any time zone)."
)
DISCLAIMER_LINE = "Claims are attributed, not stated as fact."
SOURCES_LINE = (
    "Sources: Reuters, AP, AFP, UN News, IMD, NASA, Sensor Tower, VGC, ICC "
    "- Pictures and map drawn in code - 2026-11-20"
)
