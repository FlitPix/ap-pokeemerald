import orjson
import pkgutil
from dataclasses import dataclass
from enum import IntEnum
from pkg_resources import resource_listdir, resource_isdir
from typing import Dict, FrozenSet, List, Optional, Union, Tuple, NamedTuple, Any

from BaseClasses import ItemClassification

IGNORABLE_MAPS = {
    "MAP_ALTERING_CAVE",
    "MAP_CAVE_OF_ORIGIN_UNUSED_RUBY_SAPPHIRE_MAP1",
    "MAP_CAVE_OF_ORIGIN_UNUSED_RUBY_SAPPHIRE_MAP2",
    "MAP_CAVE_OF_ORIGIN_UNUSED_RUBY_SAPPHIRE_MAP3",
}
"""These maps exist but don't show up in the rando or are unused, and so should be discarded."""

class GameOptionGroup(IntEnum):
    """
    Represents a group of options, for bitpacking into chars or shorts.
    """
    GROUP_ONE = 0
    GROUP_TWO = 1

class GameOption:
    """
    Represents a setting in the in-game "OPTIONS" menu, to be bitpacked into chars or shorts.

    option_group: the char/word that the option will be packed into
    option_number: the option's position in the char/word
    """
    default: int
    options: Dict[str | int | bool, int]
    option_group: GameOptionGroup
    option_number: int

    def __init__(self,
        default: int,
        options: Dict[str | int | bool, int],
        option_group: int,
        option_number: int
    ):
        self.default = default
        self.options = options
        self.option_group = option_group
        self.option_number = option_number

GAME_OPTIONS = {
    "text speed": GameOption(2, {"Medium": 0, "Fast": 1, "Instant": 2}, GameOptionGroup.GROUP_ONE, 6),
    "battle scene": GameOption(0, {"Off": 0, False: 0, "On": 1, True: 1}, GameOptionGroup.GROUP_ONE, 12),
    "battle style": GameOption(1, {"Switch": 0, "Set": 1}, GameOptionGroup.GROUP_ONE, 13),
    "sound": GameOption(0, {"Mono": 0, "Stereo": 1}, GameOptionGroup.GROUP_ONE, 14),
    "button mode": GameOption(1, {"Normal": 0, "LR": 1, "L=A": 2}, GameOptionGroup.GROUP_ONE, 10),
    "frame": GameOption(0, dict(zip(range(1, 21), range(20))), GameOptionGroup.GROUP_ONE, 0),
    "turbo button": GameOption(0, {"None": 0, False: 0, "A": 1, "B": 2}, GameOptionGroup.GROUP_ONE, 8),
    "skip nickname": GameOption(0, {"Off": 0, False: 0, "On": 1, True: 1}, GameOptionGroup.GROUP_TWO, 3),
    "auto run": GameOption(0, {"Off": 0, False: 0, "On": 1, True: 1}, GameOptionGroup.GROUP_TWO, 11),
    "bike music": GameOption(1, {"Off": 0, False: 0, "On": 1, True: 1}, GameOptionGroup.GROUP_TWO, 0),
    "surf music": GameOption(1, {"Off": 0, False: 0, "On": 1, True: 1}, GameOptionGroup.GROUP_TWO, 1),
    "low hp beep": GameOption(0, {"Off": 0, False: 0, "On": 1, True: 1}, GameOptionGroup.GROUP_TWO, 2),
    "blind trainers": GameOption(0, {"Off": 0, False: 0, "On": 1, True: 1}, GameOptionGroup.GROUP_TWO, 10),
    "always catch": GameOption(0, {"Off": 0, False: 0, "On": 1, True: 1}, GameOptionGroup.GROUP_TWO, 7),
    "always escape": GameOption(0, {"Off": 0, False: 0, "On": 1, True: 1}, GameOptionGroup.GROUP_TWO, 8),
    "always reel": GameOption(0, {"Off": 0, False: 0, "On": 1, True: 1}, GameOptionGroup.GROUP_TWO, 15),
    "ap messages": GameOption(2, {"Filler": 0, "Fill": 0, "Useful": 1, "Progression": 2, "Prog": 2}, GameOptionGroup.GROUP_TWO, 4),
}

class Warp:
    """
    Represents warp events in the game, like doorways or warp pads.
    """
    is_one_way: bool
    source_map: str
    source_ids: List[int]
    dest_map: str
    dest_ids: List[int]
    name: Optional[str]
    parent_region_id: Optional[str]

    def __init__(self,
                 encoded_string: Optional[str] = None,
                 name: Optional[str] = None,
                 parent_region_id: Optional[str] = None) -> None:
        if encoded_string is not None:
            decoded_warp = Warp.decode(encoded_string)
            self.is_one_way = decoded_warp.is_one_way
            self.source_map = decoded_warp.source_map
            self.source_ids = decoded_warp.source_ids
            self.dest_map = decoded_warp.dest_map
            self.dest_ids = decoded_warp.dest_ids
        self.name = name
        self.parent_region_id = parent_region_id

    def connects_to(self, other: "Warp") -> bool:
        """
        Returns true if this warp sends the player to `other`
        """
        return self.dest_map == other.source_map and set(self.dest_ids) <= set(other.source_ids)

    @staticmethod
    def decode(encoded_string: str) -> "Warp":
        """
        Create a Warp object from an encoded string
        """
        warp = Warp()
        warp.is_one_way = encoded_string.endswith("!")
        if warp.is_one_way:
            encoded_string = encoded_string[:-1]

        warp_source, warp_dest = encoded_string.split("/")
        warp_source_map, warp_source_indices = warp_source.split(":")
        warp_dest_map, warp_dest_indices = warp_dest.split(":")

        warp.source_map = warp_source_map
        warp.dest_map = warp_dest_map

        warp.source_ids = [int(index) for index in warp_source_indices.split(",")]
        warp.dest_ids = [int(index) for index in warp_dest_indices.split(",")]

        return warp

class ItemData(NamedTuple):
    name: str
    item_id: int
    classification: ItemClassification
    tags: FrozenSet[str]

class LocationCategory(IntEnum):
    BADGE = 0
    HM = 1
    KEY = 2
    ROD = 3
    BIKE = 4
    TICKET = 5
    OVERWORLD_ITEM = 6
    HIDDEN_ITEM = 7
    NPC_GIFT = 8
    EVENT = 9

class LocationData(NamedTuple):
    id: str
    name: str
    parent_region_id: str
    default_item: int
    address: Union[int, List[int]]
    flag: int
    category: LocationCategory
    tags: FrozenSet[str]

@dataclass
class MapData:
    id: str
    name: str
    header_address: int

class EventData(NamedTuple):
    id: str
    name: str
    item: str
    parent_region_id: str
    category: LocationCategory

class RegionData:
    id: str
    name: str
    parent_map: MapData
    exits: Dict[str, str | List[str]]
    warps: List[str]
    locations: List[str]
    events: List[EventData]

    def __init__(self,
        id: str,
        name: str,
        parent_map: MapData
    ):
        self.id = id
        self.name = name
        self.parent_map = parent_map
        self.exits = {}
        self.warps = []
        self.locations = []
        self.events = []

class PokemonEmeraldFlitData:
    ram_addresses: Dict[str, int]
    rom_addresses: Dict[str, int]
    regions: Dict[str, RegionData]
    locations: Dict[str, LocationData]
    events: Dict[str, EventData]
    items: Dict[int, ItemData]
    maps: Dict[str, MapData]
    warps: Dict[str, Warp]
    warp_map: Dict[str, Optional[str]]

    def __init__(self) -> None:
        self.ram_addresses = {}
        self.rom_addresses = {}
        self.regions = {}
        self.locations = {}
        self.events = {}
        self.items = {}
        self.maps = {}
        self.warps = {}
        self.warp_map = {}

# excludes extras like copies of Unown and special species values like SPECIES_EGG
ALL_SPECIES: List[Tuple[str, str, int]] = [
    ("SPECIES_BULBASAUR", "Bulbasaur", 1),
    ("SPECIES_IVYSAUR", "Ivysaur", 2),
    ("SPECIES_VENUSAUR", "Venusaur", 3),
    ("SPECIES_CHARMANDER", "Charmander", 4),
    ("SPECIES_CHARMELEON", "Charmeleon", 5),
    ("SPECIES_CHARIZARD", "Charizard", 6),
    ("SPECIES_SQUIRTLE", "Squirtle", 7),
    ("SPECIES_WARTORTLE", "Wartortle", 8),
    ("SPECIES_BLASTOISE", "Blastoise", 9),
    ("SPECIES_CATERPIE", "Caterpie", 10),
    ("SPECIES_METAPOD", "Metapod", 11),
    ("SPECIES_BUTTERFREE", "Butterfree", 12),
    ("SPECIES_WEEDLE", "Weedle", 13),
    ("SPECIES_KAKUNA", "Kakuna", 14),
    ("SPECIES_BEEDRILL", "Beedrill", 15),
    ("SPECIES_PIDGEY", "Pidgey", 16),
    ("SPECIES_PIDGEOTTO", "Pidgeotto", 17),
    ("SPECIES_PIDGEOT", "Pidgeot", 18),
    ("SPECIES_RATTATA", "Rattata", 19),
    ("SPECIES_RATICATE", "Raticate", 20),
    ("SPECIES_SPEAROW", "Spearow", 21),
    ("SPECIES_FEAROW", "Fearow", 22),
    ("SPECIES_EKANS", "Ekans", 23),
    ("SPECIES_ARBOK", "Arbok", 24),
    ("SPECIES_PIKACHU", "Pikachu", 25),
    ("SPECIES_RAICHU", "Raichu", 26),
    ("SPECIES_SANDSHREW", "Sandshrew", 27),
    ("SPECIES_SANDSLASH", "Sandslash", 28),
    ("SPECIES_NIDORAN_F", "Nidoran F", 29),
    ("SPECIES_NIDORINA", "Nidorina", 30),
    ("SPECIES_NIDOQUEEN", "Nidoqueen", 31),
    ("SPECIES_NIDORAN_M", "Nidoran M", 32),
    ("SPECIES_NIDORINO", "Nidorino", 33),
    ("SPECIES_NIDOKING", "Nidoking", 34),
    ("SPECIES_CLEFAIRY", "Clefairy", 35),
    ("SPECIES_CLEFABLE", "Clefable", 36),
    ("SPECIES_VULPIX", "Vulpix", 37),
    ("SPECIES_NINETALES", "Ninetales", 38),
    ("SPECIES_JIGGLYPUFF", "Jigglypuff", 39),
    ("SPECIES_WIGGLYTUFF", "Wigglytuff", 40),
    ("SPECIES_ZUBAT", "Zubat", 41),
    ("SPECIES_GOLBAT", "Golbat", 42),
    ("SPECIES_ODDISH", "Oddish", 43),
    ("SPECIES_GLOOM", "Gloom", 44),
    ("SPECIES_VILEPLUME", "Vileplume", 45),
    ("SPECIES_PARAS", "Paras", 46),
    ("SPECIES_PARASECT", "Parasect", 47),
    ("SPECIES_VENONAT", "Venonat", 48),
    ("SPECIES_VENOMOTH", "Venomoth", 49),
    ("SPECIES_DIGLETT", "Diglett", 50),
    ("SPECIES_DUGTRIO", "Dugtrio", 51),
    ("SPECIES_MEOWTH", "Meowth", 52),
    ("SPECIES_PERSIAN", "Persian", 53),
    ("SPECIES_PSYDUCK", "Psyduck", 54),
    ("SPECIES_GOLDUCK", "Golduck", 55),
    ("SPECIES_MANKEY", "Mankey", 56),
    ("SPECIES_PRIMEAPE", "Primeape", 57),
    ("SPECIES_GROWLITHE", "Growlithe", 58),
    ("SPECIES_ARCANINE", "Arcanine", 59),
    ("SPECIES_POLIWAG", "Poliwag", 60),
    ("SPECIES_POLIWHIRL", "Poliwhirl", 61),
    ("SPECIES_POLIWRATH", "Poliwrath", 62),
    ("SPECIES_ABRA", "Abra", 63),
    ("SPECIES_KADABRA", "Kadabra", 64),
    ("SPECIES_ALAKAZAM", "Alakazam", 65),
    ("SPECIES_MACHOP", "Machop", 66),
    ("SPECIES_MACHOKE", "Machoke", 67),
    ("SPECIES_MACHAMP", "Machamp", 68),
    ("SPECIES_BELLSPROUT", "Bellsprout", 69),
    ("SPECIES_WEEPINBELL", "Weepinbell", 70),
    ("SPECIES_VICTREEBEL", "Victreebel", 71),
    ("SPECIES_TENTACOOL", "Tentacool", 72),
    ("SPECIES_TENTACRUEL", "Tentacruel", 73),
    ("SPECIES_GEODUDE", "Geodude", 74),
    ("SPECIES_GRAVELER", "Graveler", 75),
    ("SPECIES_GOLEM", "Golem", 76),
    ("SPECIES_PONYTA", "Ponyta", 77),
    ("SPECIES_RAPIDASH", "Rapidash", 78),
    ("SPECIES_SLOWPOKE", "Slowpoke", 79),
    ("SPECIES_SLOWBRO", "Slowbro", 80),
    ("SPECIES_MAGNEMITE", "Magnemite", 81),
    ("SPECIES_MAGNETON", "Magneton", 82),
    ("SPECIES_FARFETCHD", "Farfetch'd", 83),
    ("SPECIES_DODUO", "Doduo", 84),
    ("SPECIES_DODRIO", "Dodrio", 85),
    ("SPECIES_SEEL", "Seel", 86),
    ("SPECIES_DEWGONG", "Dewgong", 87),
    ("SPECIES_GRIMER", "Grimer", 88),
    ("SPECIES_MUK", "Muk", 89),
    ("SPECIES_SHELLDER", "Shellder", 90),
    ("SPECIES_CLOYSTER", "Cloyster", 91),
    ("SPECIES_GASTLY", "Gastly", 92),
    ("SPECIES_HAUNTER", "Haunter", 93),
    ("SPECIES_GENGAR", "Gengar", 94),
    ("SPECIES_ONIX", "Onix", 95),
    ("SPECIES_DROWZEE", "Drowzee", 96),
    ("SPECIES_HYPNO", "Hypno", 97),
    ("SPECIES_KRABBY", "Krabby", 98),
    ("SPECIES_KINGLER", "Kingler", 99),
    ("SPECIES_VOLTORB", "Voltorb", 100),
    ("SPECIES_ELECTRODE", "Electrode", 101),
    ("SPECIES_EXEGGCUTE", "Exeggcute", 102),
    ("SPECIES_EXEGGUTOR", "Exeggutor", 103),
    ("SPECIES_CUBONE", "Cubone", 104),
    ("SPECIES_MAROWAK", "Marowak", 105),
    ("SPECIES_HITMONLEE", "Hitmonlee", 106),
    ("SPECIES_HITMONCHAN", "Hitmonchan", 107),
    ("SPECIES_LICKITUNG", "Lickitung", 108),
    ("SPECIES_KOFFING", "Koffing", 109),
    ("SPECIES_WEEZING", "Weezing", 110),
    ("SPECIES_RHYHORN", "Rhyhorn", 111),
    ("SPECIES_RHYDON", "Rhydon", 112),
    ("SPECIES_CHANSEY", "Chansey", 113),
    ("SPECIES_TANGELA", "Tangela", 114),
    ("SPECIES_KANGASKHAN", "Kangaskhan", 115),
    ("SPECIES_HORSEA", "Horsea", 116),
    ("SPECIES_SEADRA", "Seadra", 117),
    ("SPECIES_GOLDEEN", "Goldeen", 118),
    ("SPECIES_SEAKING", "Seaking", 119),
    ("SPECIES_STARYU", "Staryu", 120),
    ("SPECIES_STARMIE", "Starmie", 121),
    ("SPECIES_MR_MIME", "Mr. Mime", 122),
    ("SPECIES_SCYTHER", "Scyther", 123),
    ("SPECIES_JYNX", "Jynx", 124),
    ("SPECIES_ELECTABUZZ", "Electabuzz", 125),
    ("SPECIES_MAGMAR", "Magmar", 126),
    ("SPECIES_PINSIR", "Pinsir", 127),
    ("SPECIES_TAUROS", "Tauros", 128),
    ("SPECIES_MAGIKARP", "Magikarp", 129),
    ("SPECIES_GYARADOS", "Gyarados", 130),
    ("SPECIES_LAPRAS", "Lapras", 131),
    ("SPECIES_DITTO", "Ditto", 132),
    ("SPECIES_EEVEE", "Eevee", 133),
    ("SPECIES_VAPOREON", "Vaporeon", 134),
    ("SPECIES_JOLTEON", "Jolteon", 135),
    ("SPECIES_FLAREON", "Flareon", 136),
    ("SPECIES_PORYGON", "Porygon", 137),
    ("SPECIES_OMANYTE", "Omanyte", 138),
    ("SPECIES_OMASTAR", "Omastar", 139),
    ("SPECIES_KABUTO", "Kabuto", 140),
    ("SPECIES_KABUTOPS", "Kabutops", 141),
    ("SPECIES_AERODACTYL", "Aerodactyl", 142),
    ("SPECIES_SNORLAX", "Snorlax", 143),
    ("SPECIES_ARTICUNO", "Articuno", 144),
    ("SPECIES_ZAPDOS", "Zapdos", 145),
    ("SPECIES_MOLTRES", "Moltres", 146),
    ("SPECIES_DRATINI", "Dratini", 147),
    ("SPECIES_DRAGONAIR", "Dragonair", 148),
    ("SPECIES_DRAGONITE", "Dragonite", 149),
    ("SPECIES_MEWTWO", "Mewtwo", 150),
    ("SPECIES_MEW", "Mew", 151),
    ("SPECIES_CHIKORITA", "Chikorita", 152),
    ("SPECIES_BAYLEEF", "Bayleef", 153),
    ("SPECIES_MEGANIUM", "Meganium", 154),
    ("SPECIES_CYNDAQUIL", "Cyndaquil", 155),
    ("SPECIES_QUILAVA", "Quilava", 156),
    ("SPECIES_TYPHLOSION", "Typhlosion", 157),
    ("SPECIES_TOTODILE", "Totodile", 158),
    ("SPECIES_CROCONAW", "Croconaw", 159),
    ("SPECIES_FERALIGATR", "Feraligatr", 160),
    ("SPECIES_SENTRET", "Sentret", 161),
    ("SPECIES_FURRET", "Furret", 162),
    ("SPECIES_HOOTHOOT", "Hoothoot", 163),
    ("SPECIES_NOCTOWL", "Noctowl", 164),
    ("SPECIES_LEDYBA", "Ledyba", 165),
    ("SPECIES_LEDIAN", "Ledian", 166),
    ("SPECIES_SPINARAK", "Spinarak", 167),
    ("SPECIES_ARIADOS", "Ariados", 168),
    ("SPECIES_CROBAT", "Crobat", 169),
    ("SPECIES_CHINCHOU", "Chinchou", 170),
    ("SPECIES_LANTURN", "Lanturn", 171),
    ("SPECIES_PICHU", "Pichu", 172),
    ("SPECIES_CLEFFA", "Cleffa", 173),
    ("SPECIES_IGGLYBUFF", "Igglybuff", 174),
    ("SPECIES_TOGEPI", "Togepi", 175),
    ("SPECIES_TOGETIC", "Togetic", 176),
    ("SPECIES_NATU", "Natu", 177),
    ("SPECIES_XATU", "Xatu", 178),
    ("SPECIES_MAREEP", "Mareep", 179),
    ("SPECIES_FLAAFFY", "Flaaffy", 180),
    ("SPECIES_AMPHAROS", "Ampharos", 181),
    ("SPECIES_BELLOSSOM", "Bellossom", 182),
    ("SPECIES_MARILL", "Marill", 183),
    ("SPECIES_AZUMARILL", "Azumarill", 184),
    ("SPECIES_SUDOWOODO", "Sudowoodo", 185),
    ("SPECIES_POLITOED", "Politoed", 186),
    ("SPECIES_HOPPIP", "Hoppip", 187),
    ("SPECIES_SKIPLOOM", "Skiploom", 188),
    ("SPECIES_JUMPLUFF", "Jumpluff", 189),
    ("SPECIES_AIPOM", "Aipom", 190),
    ("SPECIES_SUNKERN", "Sunkern", 191),
    ("SPECIES_SUNFLORA", "Sunflora", 192),
    ("SPECIES_YANMA", "Yanma", 193),
    ("SPECIES_WOOPER", "Wooper", 194),
    ("SPECIES_QUAGSIRE", "Quagsire", 195),
    ("SPECIES_ESPEON", "Espeon", 196),
    ("SPECIES_UMBREON", "Umbreon", 197),
    ("SPECIES_MURKROW", "Murkrow", 198),
    ("SPECIES_SLOWKING", "Slowking", 199),
    ("SPECIES_MISDREAVUS", "Misdreavus", 200),
    ("SPECIES_UNOWN", "Unown", 201),
    ("SPECIES_WOBBUFFET", "Wobbuffet", 202),
    ("SPECIES_GIRAFARIG", "Girafarig", 203),
    ("SPECIES_PINECO", "Pineco", 204),
    ("SPECIES_FORRETRESS", "Forretress", 205),
    ("SPECIES_DUNSPARCE", "Dunsparce", 206),
    ("SPECIES_GLIGAR", "Gligar", 207),
    ("SPECIES_STEELIX", "Steelix", 208),
    ("SPECIES_SNUBBULL", "Snubbull", 209),
    ("SPECIES_GRANBULL", "Granbull", 210),
    ("SPECIES_QWILFISH", "Qwilfish", 211),
    ("SPECIES_SCIZOR", "Scizor", 212),
    ("SPECIES_SHUCKLE", "Shuckle", 213),
    ("SPECIES_HERACROSS", "Heracross", 214),
    ("SPECIES_SNEASEL", "Sneasel", 215),
    ("SPECIES_TEDDIURSA", "Teddiursa", 216),
    ("SPECIES_URSARING", "Ursaring", 217),
    ("SPECIES_SLUGMA", "Slugma", 218),
    ("SPECIES_MAGCARGO", "Magcargo", 219),
    ("SPECIES_SWINUB", "Swinub", 220),
    ("SPECIES_PILOSWINE", "Piloswine", 221),
    ("SPECIES_CORSOLA", "Corsola", 222),
    ("SPECIES_REMORAID", "Remoraid", 223),
    ("SPECIES_OCTILLERY", "Octillery", 224),
    ("SPECIES_DELIBIRD", "Delibird", 225),
    ("SPECIES_MANTINE", "Mantine", 226),
    ("SPECIES_SKARMORY", "Skarmory", 227),
    ("SPECIES_HOUNDOUR", "Houndour", 228),
    ("SPECIES_HOUNDOOM", "Houndoom", 229),
    ("SPECIES_KINGDRA", "Kingdra", 230),
    ("SPECIES_PHANPY", "Phanpy", 231),
    ("SPECIES_DONPHAN", "Donphan", 232),
    ("SPECIES_PORYGON2", "Porygon2", 233),
    ("SPECIES_STANTLER", "Stantler", 234),
    ("SPECIES_SMEARGLE", "Smeargle", 235),
    ("SPECIES_TYROGUE", "Tyrogue", 236),
    ("SPECIES_HITMONTOP", "Hitmontop", 237),
    ("SPECIES_SMOOCHUM", "Smoochum", 238),
    ("SPECIES_ELEKID", "Elekid", 239),
    ("SPECIES_MAGBY", "Magby", 240),
    ("SPECIES_MILTANK", "Miltank", 241),
    ("SPECIES_BLISSEY", "Blissey", 242),
    ("SPECIES_RAIKOU", "Raikou", 243),
    ("SPECIES_ENTEI", "Entei", 244),
    ("SPECIES_SUICUNE", "Suicune", 245),
    ("SPECIES_LARVITAR", "Larvitar", 246),
    ("SPECIES_PUPITAR", "Pupitar", 247),
    ("SPECIES_TYRANITAR", "Tyranitar", 248),
    ("SPECIES_LUGIA", "Lugia", 249),
    ("SPECIES_HO_OH", "Ho-Oh", 250),
    ("SPECIES_CELEBI", "Celebi", 251),
    ("SPECIES_TREECKO", "Treecko", 252),
    ("SPECIES_GROVYLE", "Grovyle", 253),
    ("SPECIES_SCEPTILE", "Sceptile", 254),
    ("SPECIES_TORCHIC", "Torchic", 255),
    ("SPECIES_COMBUSKEN", "Combusken", 256),
    ("SPECIES_BLAZIKEN", "Blaziken", 257),
    ("SPECIES_MUDKIP", "Mudkip", 258),
    ("SPECIES_MARSHTOMP", "Marshtomp", 259),
    ("SPECIES_SWAMPERT", "Swampert", 260),
    ("SPECIES_POOCHYENA", "Poochyena", 261),
    ("SPECIES_MIGHTYENA", "Mightyena", 262),
    ("SPECIES_ZIGZAGOON", "Zigzagoon", 263),
    ("SPECIES_LINOONE", "Linoone", 264),
    ("SPECIES_WURMPLE", "Wurmple", 265),
    ("SPECIES_SILCOON", "Silcoon", 266),
    ("SPECIES_BEAUTIFLY", "Beautifly", 267),
    ("SPECIES_CASCOON", "Cascoon", 268),
    ("SPECIES_DUSTOX", "Dustox", 269),
    ("SPECIES_LOTAD", "Lotad", 270),
    ("SPECIES_LOMBRE", "Lombre", 271),
    ("SPECIES_LUDICOLO", "Ludicolo", 272),
    ("SPECIES_SEEDOT", "Seedot", 273),
    ("SPECIES_NUZLEAF", "Nuzleaf", 274),
    ("SPECIES_SHIFTRY", "Shiftry", 275),
    ("SPECIES_NINCADA", "Nincada", 290),
    ("SPECIES_NINJASK", "Ninjask", 291),
    ("SPECIES_SHEDINJA", "Shedinja", 292),
    ("SPECIES_TAILLOW", "Taillow", 276),
    ("SPECIES_SWELLOW", "Swellow", 277),
    ("SPECIES_SHROOMISH", "Shroomish", 285),
    ("SPECIES_BRELOOM", "Breloom", 286),
    ("SPECIES_SPINDA", "Spinda", 327),
    ("SPECIES_WINGULL", "Wingull", 278),
    ("SPECIES_PELIPPER", "Pelipper", 279),
    ("SPECIES_SURSKIT", "Surskit", 283),
    ("SPECIES_MASQUERAIN", "Masquerain", 284),
    ("SPECIES_WAILMER", "Wailmer", 320),
    ("SPECIES_WAILORD", "Wailord", 321),
    ("SPECIES_SKITTY", "Skitty", 300),
    ("SPECIES_DELCATTY", "Delcatty", 301),
    ("SPECIES_KECLEON", "Kecleon", 352),
    ("SPECIES_BALTOY", "Baltoy", 343),
    ("SPECIES_CLAYDOL", "Claydol", 344),
    ("SPECIES_NOSEPASS", "Nosepass", 299),
    ("SPECIES_TORKOAL", "Torkoal", 324),
    ("SPECIES_SABLEYE", "Sableye", 302),
    ("SPECIES_BARBOACH", "Barboach", 339),
    ("SPECIES_WHISCASH", "Whiscash", 340),
    ("SPECIES_LUVDISC", "Luvdisc", 370),
    ("SPECIES_CORPHISH", "Corphish", 341),
    ("SPECIES_CRAWDAUNT", "Crawdaunt", 342),
    ("SPECIES_FEEBAS", "Feebas", 349),
    ("SPECIES_MILOTIC", "Milotic", 350),
    ("SPECIES_CARVANHA", "Carvanha", 318),
    ("SPECIES_SHARPEDO", "Sharpedo", 319),
    ("SPECIES_TRAPINCH", "Trapinch", 328),
    ("SPECIES_VIBRAVA", "Vibrava", 329),
    ("SPECIES_FLYGON", "Flygon", 330),
    ("SPECIES_MAKUHITA", "Makuhita", 296),
    ("SPECIES_HARIYAMA", "Hariyama", 297),
    ("SPECIES_ELECTRIKE", "Electrike", 309),
    ("SPECIES_MANECTRIC", "Manectric", 310),
    ("SPECIES_NUMEL", "Numel", 322),
    ("SPECIES_CAMERUPT", "Camerupt", 323),
    ("SPECIES_SPHEAL", "Spheal", 363),
    ("SPECIES_SEALEO", "Sealeo", 364),
    ("SPECIES_WALREIN", "Walrein", 365),
    ("SPECIES_CACNEA", "Cacnea", 331),
    ("SPECIES_CACTURNE", "Cacturne", 332),
    ("SPECIES_SNORUNT", "Snorunt", 361),
    ("SPECIES_GLALIE", "Glalie", 362),
    ("SPECIES_LUNATONE", "Lunatone", 337),
    ("SPECIES_SOLROCK", "Solrock", 338),
    ("SPECIES_AZURILL", "Azurill", 298),
    ("SPECIES_SPOINK", "Spoink", 325),
    ("SPECIES_GRUMPIG", "Grumpig", 326),
    ("SPECIES_PLUSLE", "Plusle", 311),
    ("SPECIES_MINUN", "Minun", 312),
    ("SPECIES_MAWILE", "Mawile", 303),
    ("SPECIES_MEDITITE", "Meditite", 307),
    ("SPECIES_MEDICHAM", "Medicham", 308),
    ("SPECIES_SWABLU", "Swablu", 333),
    ("SPECIES_ALTARIA", "Altaria", 334),
    ("SPECIES_WYNAUT", "Wynaut", 360),
    ("SPECIES_DUSKULL", "Duskull", 355),
    ("SPECIES_DUSCLOPS", "Dusclops", 356),
    ("SPECIES_ROSELIA", "Roselia", 315),
    ("SPECIES_SLAKOTH", "Slakoth", 287),
    ("SPECIES_VIGOROTH", "Vigoroth", 288),
    ("SPECIES_SLAKING", "Slaking", 289),
    ("SPECIES_GULPIN", "Gulpin", 316),
    ("SPECIES_SWALOT", "Swalot", 317),
    ("SPECIES_TROPIUS", "Tropius", 357),
    ("SPECIES_WHISMUR", "Whismur", 293),
    ("SPECIES_LOUDRED", "Loudred", 294),
    ("SPECIES_EXPLOUD", "Exploud", 295),
    ("SPECIES_CLAMPERL", "Clamperl", 366),
    ("SPECIES_HUNTAIL", "Huntail", 367),
    ("SPECIES_GOREBYSS", "Gorebyss", 368),
    ("SPECIES_ABSOL", "Absol", 359),
    ("SPECIES_SHUPPET", "Shuppet", 353),
    ("SPECIES_BANETTE", "Banette", 354),
    ("SPECIES_SEVIPER", "Seviper", 336),
    ("SPECIES_ZANGOOSE", "Zangoose", 335),
    ("SPECIES_RELICANTH", "Relicanth", 369),
    ("SPECIES_ARON", "Aron", 304),
    ("SPECIES_LAIRON", "Lairon", 305),
    ("SPECIES_AGGRON", "Aggron", 306),
    ("SPECIES_CASTFORM", "Castform", 351),
    ("SPECIES_VOLBEAT", "Volbeat", 313),
    ("SPECIES_ILLUMISE", "Illumise", 314),
    ("SPECIES_LILEEP", "Lileep", 345),
    ("SPECIES_CRADILY", "Cradily", 346),
    ("SPECIES_ANORITH", "Anorith", 347),
    ("SPECIES_ARMALDO", "Armaldo", 348),
    ("SPECIES_RALTS", "Ralts", 280),
    ("SPECIES_KIRLIA", "Kirlia", 281),
    ("SPECIES_GARDEVOIR", "Gardevoir", 282),
    ("SPECIES_BAGON", "Bagon", 371),
    ("SPECIES_SHELGON", "Shelgon", 372),
    ("SPECIES_SALAMENCE", "Salamence", 373),
    ("SPECIES_BELDUM", "Beldum", 374),
    ("SPECIES_METANG", "Metang", 375),
    ("SPECIES_METAGROSS", "Metagross", 376),
    ("SPECIES_REGIROCK", "Regirock", 377),
    ("SPECIES_REGICE", "Regice", 378),
    ("SPECIES_REGISTEEL", "Registeel", 379),
    ("SPECIES_KYOGRE", "Kyogre", 382),
    ("SPECIES_GROUDON", "Groudon", 383),
    ("SPECIES_RAYQUAZA", "Rayquaza", 384),
    ("SPECIES_LATIAS", "Latias", 380),
    ("SPECIES_LATIOS", "Latios", 381),
    ("SPECIES_JIRACHI", "Jirachi", 385),
    ("SPECIES_DEOXYS", "Deoxys", 386),
    ("SPECIES_CHIMECHO", "Chimecho", 358),
]

def load_json_data(data_name: str) -> Union[List[Any], Dict[str, Any]]:
    return orjson.loads(pkgutil.get_data(__name__, "data/" + data_name).decode("utf-8-sig"))

def init() -> None:
    import re

    extracted_data: Dict[str, Any] = load_json_data("extracted_data.json")
    data.constants = extracted_data["constants"]
    data.ram_addresses = extracted_data["misc_ram_addresses"]
    data.rom_addresses = extracted_data["misc_rom_addresses"]

    location_data = load_json_data("locations.json")
    event_data = load_json_data("events.json")
    item_data = load_json_data("items.json")

    # Create map data
    for map_id, map_json in extracted_data["maps"].items():
        assert isinstance(map_id, str)
        if map_id in IGNORABLE_MAPS:
            continue

        # derive a user-facing name
        name = []
        for word in map_id[4:].split("_"):
            # 1F, B1F, 2R, etc.
            re_match = re.match(r"^B?\d+[FRP]$", word)
            if re_match:
                name.append(word)
                continue

            # Route 103, Hall 1, House 5, etc.
            re_match = re.match(r"^([A-Z]+)(\d+)$", word)
            if re_match:
                name.append(re_match.group(1).capitalize())
                name.append(re_match.group(2).lstrip("0"))
                continue

            if word == "OF":
                name.append("of")
                continue

            if word == "SS":
                name.append("S.S.")
                continue

            name.append(word.capitalize())

        data.maps[map_id] = MapData(
            map_id,
            " ".join(name),
            map_json["header_address"]
        )

    # load and merge region json files
    region_json_list = []
    for file in resource_listdir(__name__, "data/regions"):
        if not resource_isdir(__name__, "data/regions/" + file):
            region_json_list.append(load_json_data("regions/" + file))
    
    regions_json = {}
    for region_subset in region_json_list:
        for region_id, region_json in region_subset.items():
            if region_id in regions_json:
                raise AssertionError("Flit's Pokemon Emerald: region [{region_id}] was defined multiple times")
            regions_json[region_id] = region_json
    
    # create region data
    claimed_locations: Set[str] = set()
    claimed_warps: Set[str] = set()

    data.regions = {}
    for region_id, region_json in regions_json.items():
        new_region = RegionData(
            region_id,
            region_json["name"],
            data.maps[region_json["parent_map"]],
            #region_json["has_grass"],
            #region_json["has_water"],
            #region_json["has_fishing"]
        )

        # locations
        for location_id in region_json["locations"]:
            if location_id in claimed_locations:
                raise AssertionError(f"Flit's Pokemon Emerald: Location [{location_id}] was claimed by multiple regions")
            
            # for now, skip unimplemented location types
            if location_id.startswith(("BERRY_TREE_", "TRAINER_")):
                continue

            location_json = extracted_data["locations"][location_id]
            if location_id.startswith("TRAINER_BRENDAN_") or location_id.startswith("TRAINER_MAY_"):
                import re
                locale = re.match("TRAINER_BRENDAN_([A-Z0-9_]+)_MUDKIP_REWARD", location_id).group(1)
                alternate_rival_jsons = [extracted_data["locations"][alternate] for alternate in [
                    f"TRAINER_BRENDAN_{locale}_TORCHIC_REWARD",
                    f"TRAINER_BRENDAN_{locale}_TREECKO_REWARD",
                    f"TRAINER_MAY_{locale}_MUDKIP_REWARD",
                    f"TRAINER_MAY_{locale}_TORCHIC_REWARD",
                    f"TRAINER_MAY_{locale}_TREECKO_REWARD",
                ]]
                new_location = LocationData(
                    location_id,
                    location_data[location_id]["name"],
                    region_id,
                    location_json["default_item"],
                    [location_json["address"]] + [j["address"] for j in alternate_rival_jsons],
                    location_json["flag"],
                    LocationCategory[location_data[location_id]["category"]],
                    frozenset(location_data[location_id]["tags"])
                )
            else:
                new_location = LocationData(
                    location_id,
                    location_data[location_id]["name"],
                    region_id,
                    location_json["default_item"],
                    location_json["address"],
                    location_json["flag"],
                    LocationCategory[location_data[location_id]["category"]],
                    frozenset(location_data[location_id]["tags"])
                )
            new_region.locations.append(location_id)
            data.locations[location_id] = new_location
            claimed_locations.add(location_id)

        new_region.locations.sort()

        # events
        for event_id in region_json["events"]:
            # for now, skip unimplemented event types
            if event_id.startswith(("EVENT_ENCOUNTER_")):
                continue

            new_event = EventData(
                event_id,
                event_data[event_id]["name"],
                event_data[event_id]["item"],
                region_id,
                LocationCategory[event_data[event_id]["category"]]
            )
            new_region.events.append(event_id)
            data.events[event_id] = new_event

        # exits
        new_region.exits = region_json["exits"]

        # warps
        for encoded_warp, name in region_json["warps"].items():
            if encoded_warp in claimed_warps:
                raise AssertionError(f"Flit's Pokemon Emerald: Warp [{encoded_warp}] was claimed by multiple regions")
            new_region.warps.append(encoded_warp)
            data.warps[encoded_warp] = Warp(encoded_warp, name, region_id)
            claimed_warps.add(encoded_warp)

        new_region.warps.sort()

        data.regions[region_id] = new_region
    
    # create warp map
    for warp, destination in extracted_data["warps"].items():
        data.warp_map[warp] = None if destination == "" else destination

    # create item data
    data.items = {}
    for item_id_name, attributes in item_data.items():
        item_classification = None
        if attributes["classification"] == "PROGRESSION":
            item_classification = ItemClassification.progression
        elif attributes["classification"] == "USEFUL":
            item_classification = ItemClassification.useful
        elif attributes["classification"] == "FILLER":
            item_classification = ItemClassification.filler
        elif attributes["classification"] == "TRAP":
            item_classification = ItemClassification.trap
        else:
            raise ValueError(f"Flit's Pokemon Emerald: Unknown classification {attributes['classification']} for item {item_id_name}")

        data.items[data.constants[item_id_name]] = ItemData(
            attributes["name"],
            data.constants[item_id_name],
            item_classification,
            frozenset(attributes["tags"])
        )

data = PokemonEmeraldFlitData()
init()
