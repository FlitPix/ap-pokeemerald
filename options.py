from dataclasses import dataclass
from schema import Schema, And, Optional, Or

from Options import (Choice, DeathLink, DefaultOnToggle, NamedRange, OptionDict, OptionGroup,
                    OptionSet, PerGameCommonOptions, Range, StartInventory, StartInventoryPool, Toggle)

from .data import data, GAME_OPTIONS

### GOAL OPTIONS

class Goals(OptionSet):
    """
    Decide what you must do to goal your game. All selected tasks must be completed to goal.

    - Hall of Fame: Defeat Champion Wallace and enter the Hall of Fame.
    - Steven: Defeat Steven in Meteor Falls. NOTE: Enabling this will also enable Hall of Fame.
    """
    display_name = "Goals"

    valid_keys = {"Hall of Fame", "Steven"}
    default = {"Hall of Fame"}

### GLOBAL OPTIONS

class ShuffleBadges(Choice):
    """
    Adds Gym Badges to the item pool.

    - Vanilla: Gym Leaders give their own badge.
    - Completely Random: Badges can be found anywhere.
    """
    display_name = "Shuffle Badges"
    option_vanilla = 0
    #option_leaders = 1
    option_completely_random = 2
    default = 2

class ShuffleOverworldItems(DefaultOnToggle):
    """
    Adds items on the ground with a Poke Ball sprite to the item pool.
    """
    display_name = "Shuffle Overworld Items"

class ShuffleHiddenItems(Toggle):
    """
    Adds hidden items to the item pool.
    """
    display_name = "Shuffle Hidden Items"

class ShuffleNpcGifts(DefaultOnToggle):
    """
    Adds gifts received from NPCs to the item pool.
    
    Key items, badges, and HMs will always be shuffled regardless of this setting.
    """
    display_name = "Shuffle NPC Gifts"

#class ShuffleRods(DefaultOnToggle):
#    """
#    Adds the Old, Good, and Super Rods to the item pool.
#    """
#    display_name = "Shuffle Rods"

class ShuffleBikes(DefaultOnToggle):
    """
    Adds the Mach Bike and Acro Bike to the item pool.
    """
    display_name = "Shuffle Bikes"

class ShuffleEventTickets(Toggle):
    """
    Adds the event tickets to the item pool, which let you encounter special Pokemon by sailing from any harbor.
    """
    display_name = "Shuffle Event Tickets"

#class ShuffleBag(Toggle):
#    """
#    Adds the bag to the item pool. Until you receive it, you cannot access your bag from the start menu, the PC, or the battle screen (meaning you cannot catch Pokemon or use key items), and you cannot turn in key items to NPCs. You can still receive items.
#    """
#    display_name = "Shuffle Bag"

#class ShufflePokedex(Choice):
#    """
#    Adds the Pokedex and National Pokedex to the item pool. Dexsanity checks cannot be sent until the Pokedex is received. Receiving the National Pokedex now opens the Safari Zone extension, along with other events that normally require it.
#
#    - Disabled: You start with a fully-upgraded Pokedex.
#    - Enabled: Adds the "Pokedex" and "National Pokedex" items to the item pool. You may find the National Pokedex before the Pokedex is unlocked; this will instantly enable events that require the National Pokedex.
#    - Progressive: Adds two "Progressive Pokedex" items to the item pool. You will always receive the Hoenn Pokedex, then the National Pokedex, in order.
#    """
#    display_name = "Shuffle Pokedex"
#    default = 0
#    option_disabled = 0
#    option_enabled = 1
#    option_progressive = 2

#class ShufflePokenav(Toggle):
#    """
#    Adds the Pokenav to the item pool. If disabled, you start with the Pokenav, with Match Call enabled. Some checks require it.
#    """
#    display_name = "Shuffle Pokenav"

#class ShuffleRunningShoes(Toggle):
#    """
#    Adds the Running Shoes to the item pool.
#
#    NOTE: This currently has no logical implications, so the item is considered useful. It isn't recommended to enable it right now, unless you want to walk a lot.
#    """
#    display_name = "Shuffle Running Shoes"

#class Dexsanity(NamedRange):
#    """
#    Adds locations for registering logically-available Pokemon as caught in the Pokedex. This setting decides how many dex entries will have items, chosen randomly.
#    """
#    display_name = "Dexsanity"
#    default = 0
#    range_start = 0
#    range_end = 386
#    special_range_names = {
#        "none": default,
#        "full": range_end
#    }

#class Trainersanity(NamedRange):
#    """
#    Adds locations for defeating logically-available Trainers. This setting decides how many Trainers will have items, chosen randomly.
#    """
#    display_name = "Dexsanity"
#    default = 0
#    range_start = 0
#    range_end = 386 # to change
#    special_range_names = {
#        "none": default,
#        "full": range_end
#    }

class RequireItemfinder(Choice):
    """
    Determines whether the Itemfinder is required to pick up hidden items.

    - Off: Hidden items do not require the Itemfinder at all.
    - Logic: Hidden items will expect you to have the Itemfinder logically, but can be picked up without it.
    """
    display_name = "Require Itemfinder"
    option_off = 0
    option_logic = 1
    default = 1

class RequireFlash(DefaultOnToggle):
    """
    Determines whether HM05 Flash is logically required to navigate dark caves.
    """
    display_name = "Require Flash"

#class RandomStartingTown(Toggle):
#    """
#    Randomly chooses a town to start in. You will start in front of the Pokemon Center, or whatever equivalent, in the chosen town.
#
#    You cannot start at the Hoenn Pokemon League.
#
#    NOTE: If Level Scaling is not enabled, some starting towns may produce difficult starts.
#    """
#    display_name = "Random Starting Town"

#class RandomStartingTownBlacklist(OptionSet):
#    """
#    When Random Starting Town is enabled, specify towns you cannot start in.
#
#    Any variation of "Hoenn Pokemon League" isn't a valid option, as you already can't start there.
#
#    Blocking everything or not enabling Random Starting Town will cause this option to do nothing.
#    """
#    display_name = "Starting Town Blacklist"
#    valid_keys = sorted(town.name for town in data.starting_towns)

class ExcludePostHofLocations(DefaultOnToggle):
    """
    Excludes locations locked behind the Hall of Fame, preventing them from having any important items.
    Disabling this and only selecting the Hall of Fame goal can be interesting in multiworlds where release is disabled.

    This setting is forcibly disabled if Steven is one of your goals.
    """
    display_name = "Exclude Post-Hall of Fame Locations"

class ChallengeMode(Toggle):
    """
    Challenge Mode forcibly disables some QoL options and applies additional restrictions to make the game more challenging.

    The list of restrictions is too big to include here; please refer to its dedicated section in the ROM changes for more information
    (open the APWorld like you would a zip file, and go to docs/ROM Changes.md).

    Not recommended for new players.
    """
    display_name = "Challenge Mode"

class ReusableTms(Toggle):
    """
    Makes TMs reusable, like in Gen 5 and (mostly) onwards.
    Reusable TMs cannot be sold, deposited in the PC, or given to Pokemon.

    NOTE: There is a known issue where you can still purchase multiple TMs if this option is enabled. Don't do that.
    """
    display_name = "Reusable TMs"

#class RemoteItems(Toggle):
#    """
#    When enabled, instead of placing your own items directly into the ROM, all items are received from the server, including items you find for yourself.
#
#    This enables co-op of a single slot, recovering local items if the save data is lost, and better allows others to take over your slot if necessary.
#
#    However, the behavior of finding items is changed slightly, and the game will require a constant connection to the server to receive any items.
#    """
#    display_name = "Remote Items"

class PokemonEmeraldFlitDeathLink(DeathLink):
    __doc__ = DeathLink.__doc__ + "\n\n    In Pokemon Emerald Version, whiting out sends a death, and receiving a death causes you to white out.\n\n    You can always toggle this on and off later in the in-game \"OPTIONS\" menu."

#class WonderTrade(DefaultOnToggle):
#    """
#    Enables the Wonder Trade feature, which allows trading with anyone in the current multiworld who is playing a supported Pokemon game and also has Wonder Trade enabled.
#
#    To start a Wonder Trade, speak with the Direct Corner attendant (far right) on the second floor of any Pokemon Center.
#
#    Pokemon sent or received over Wonder Trade NEVER affect logic.
#    Pokemon received from Wonder Trade are NOT marked as seen or caught in the Pokedex.
#    Trade evolutions will NOT occur.
#
#    You may end up trading with other Pokemon games, or with games that have different Pokemon-related options.
#    Stats (IVs/EVs), types, learnsets, Abilities, Natures, etc. might get changed or removed depending on the game you end up trading with.
#    """
#    display_name = "Wonder Trade"

### HOENN OPTIONS

class NormanRequirement(Choice):
    """
    Determines the requirement for challenging the Petalburg Gym.

    - Badges: Obtain some number of Gym Badges
    - Gyms: Defeat some number of Gym Leaders
    """
    display_name = "Norman Requirement"
    option_badges = 0
    option_gyms = 1
    default = 0

class NormanCount(Range):
    """
    Determines the number of badges/gyms required to challenge the Petalburg Gym.
    """
    display_name = "Norman Count"
    range_start = 0
    range_end = 7
    default = 4

class HoennEliteFourRequirement(Choice):
    """
    Determines the requirement to challenge the Elite Four.

    - Badges: Obtain some number of Gym Badges
    - Gyms: Defeat some number of Gym Leaders
    """
    display_name = "Elite Four Requirement"
    option_badges = 0
    option_gyms = 1
    default = 0

class HoennEliteFourCount(Range):
    """
    Determines the number of badges/gyms required to challenge the Elite Four.
    """
    display_name = "Elite Four Count"
    range_start = 0
    range_end = 8
    default = 8

class HoennRemoveBadgeRequirement(OptionSet):
    """
    Removes the badge requirement to use any of the HMs listed.

    HMs should be listed by the move name ("Cut", "Fly", "Rock Smash", etc).
    """
    display_name = "Remove Badge Requirements"
    valid_keys = {"Cut", "Fly", "Surf", "Strength", "Flash", "Rock Smash", "Waterfall", "Dive"}

#class WorldBlockers(OptionSet):
#    """
#    Adds or removes the listed blockers.
#
#    Valid options and what they do are as follows:
#    - "Add Route 103 Bike Rails": Adds bike rails to Route 103, to require the Acro Bike to cross the water rather than Surf.
#    - "Mr. Briney at Start": Mr. Briney is available immediately without having to meet Mr. Stone.
#    - "Mr. Briney All Destinations at Start": Mr. Briney can take you anywhere regardless of your progress in the Letter quest.
#    - "Remove Route 110 Aqua Grunts": Removes the Aqua Grunts blocking the southern portion of Route 110.
#    - "Remove Route 112 Magma Grunts": Removes the Magma Grunts blocking the entrance to the Cable Car station on Route 112.
#    - "Add Route 115 Boulders": Adds Strength boulders that block access to Meteor Falls from the beach on Route 115.
#    - "Add Route 115 Bumpy Slope": Adds a bumpy slope to Route 115 South, to allow access to the rest of the route from Rustboro.
#    - "Add Route 118 Bike Rails": Adds bike rails to Route 118, to require the Acro Bike to cross the water rather than Surf.
#    - "Remove Route 119 Aqua Grunts": Removes the Aqua Grunts blocking the bridge east of the Weather Institute.
#    - "Remove Route 121 Aqua Grunts": Removes the Aqua Grunts near the Safari Zone, to allow traveling westwards without Cut.
#    - "Remove Safari Zone Workers": Removes the NPCs blocking the Safari Zone extension.
#    - "Remove Lilycove City Wailmer": Removes the Wailmer blocking the east exit from Lilycove City.
#    - "Remove Aqua Hideout Grunts": Removes the Aqua Grunts blocking the initial landing spot in Aqua Hideout.
#    - "Remove Seafloor Cavern Aqua Grunt": Removes the Aqua Grunt blocking the entrance to Seafloor Cavern.
#    - "Alternate Route 132-134 Currents": Redesigns the water currents between Routes 132 through 134, to instead only allow traveling east from Slateport.
#    - "Seal Already Broken": The Legendary giants' seal is already broken.
#    """
#    display_name = "World Blockers"
#    valid_keys = {
#        "Add Route 103 Bike Rails",
#        "Mr. Briney at Start",
#        "Mr. Briney All Destinations at Start",
#        "Remove Route 110 Aqua Grunts",
#        "Remove Route 112 Magma Grunts",
#        "Add Route 115 Boulders",
#        "Add Route 115 Bumpy Slope",
#        "Add Route 118 Bike Rails",
#        "Remove Route 119 Aqua Grunts",
#        "Remove Route 121 Aqua Grunts",
#        "Remove Safari Zone Workers",
#        "Remove Lilycove City Wailmer",
#        "Remove Aqua Hideout Grunts",
#        "Remove Seafloor Cavern Aqua Grunt",
#        "Alternate Route 132-134 Currents",
#        "Seal Already Broken"
#    }

#class EasierCrackedFloors(Toggle):
#    """
#    Determines whether cracked floors in Granite Cave, Mirage Tower and Sky Pillar can be traversed without using the Mach Bike.
#
#    The Mach Bike will not be required at all to traverse these areas if this option is enabled.
#    """
#    display_name = "Easier Cracked Floors"

class GameOptions(OptionDict):
    """
    Set your preferred defaults for the in-game "OPTIONS" menu here.
    The options you can currently set and their allowed values are:

    - Text Speed: Medium, Fast, Instant
    - Battle Scene: Off, On
    - Battle Style: Switch, Set
    - Sound: Mono, Stereo
    - Button Mode: Normal, LR, L=A
    - Frame: 1-20
    - Turbo Button: None, A, B
    - Blind Trainers: Off, On
    - Always Catch: Off, On
    - Always Escape: Off, On
    - AP Messages: Filler, Useful, Progression

    NOTE: In-game options not listed here don't work yet. Sorry!
    """
    display_name = "Game Options"
    schema = Schema({
        Optional("Text Speed"): And(str, lambda s: s in GAME_OPTIONS["text speed"].options.keys()),
        Optional("Battle Scene"): Or(And(str, lambda s: s in GAME_OPTIONS["battle scene"].options.keys()),
                                     And(bool, lambda s: s in GAME_OPTIONS["battle scene"].options.keys()),),
        Optional("Battle Style"): And(str, lambda s: s in GAME_OPTIONS["battle style"].options.keys()),
        Optional("Sound"): And(str, lambda s: s in GAME_OPTIONS["sound"].options.keys()),
        Optional("Button Mode"): And(str, lambda s: s in GAME_OPTIONS["button mode"].options.keys()),
        Optional("Frame"): And(int, lambda i: i in GAME_OPTIONS["frame"].options.keys()),
        Optional("Turbo Button"): Or(And(str, lambda s: s in GAME_OPTIONS["turbo button"].options.keys()),
                                     And(bool, lambda s: s in GAME_OPTIONS["turbo button"].options.keys()),),
        #Optional("Skip Nickname"): Or(And(str, lambda s: s in GAME_OPTIONS["skip nickname"].options.keys()),
        #                               And(bool, lambda s: s in GAME_OPTIONS["skip nickname"].options.keys()),),
        #Optional("Auto Run"): Or(And(str, lambda s: s in GAME_OPTIONS["auto run"].options.keys()),
        #                               And(bool, lambda s: s in GAME_OPTIONS["auto run"].options.keys()),),
        Optional("Bike Music"): Or(And(str, lambda s: s in GAME_OPTIONS["bike music"].options.keys()),
                                       And(bool, lambda s: s in GAME_OPTIONS["bike music"].options.keys()),),
        Optional("Surf Music"): Or(And(str, lambda s: s in GAME_OPTIONS["surf music"].options.keys()),
                                       And(bool, lambda s: s in GAME_OPTIONS["surf music"].options.keys()),),
        Optional("Low HP Beep"): Or(And(str, lambda s: s in GAME_OPTIONS["low hp beep"].options.keys()),
                                       And(bool, lambda s: s in GAME_OPTIONS["low hp beep"].options.keys()),),
        Optional("Blind Trainers"): Or(And(str, lambda s: s in GAME_OPTIONS["blind trainers"].options.keys()),
                                       And(bool, lambda s: s in GAME_OPTIONS["blind trainers"].options.keys()),),
        Optional("Always Catch"): Or(And(str, lambda s: s in GAME_OPTIONS["always catch"].options.keys()),
                                         And(bool, lambda s: s in GAME_OPTIONS["always catch"].options.keys()),),
        Optional("Always Escape"): Or(And(str, lambda s: s in GAME_OPTIONS["always escape"].options.keys()),
                                       And(bool, lambda s: s in GAME_OPTIONS["always escape"].options.keys()),),
        #Optional("Always Reel"): Or(And(str, lambda s: s in GAME_OPTIONS["always reel"].options.keys()),
        #                               And(bool, lambda s: s in GAME_OPTIONS["always reel"].options.keys()),),
        Optional("AP Messages"): And(str, lambda s: s in GAME_OPTIONS["ap messages"].options.keys()),
    })

    default = {
        "Text Speed": "Instant",
        "Battle Scene": "Off",
        "Battle Style": "Set",
        "Sound": "Mono",
        "Button Mode": "LR",
        "Frame": 1,
        "Turbo Button": "A",
        "Bike Music": "On",
        "Surf Music": "On",
        "Low HP Beep": "Off",
        "Blind Trainers": "Off",
        "Always Catch": "Off",
        "Always Escape": "Off",
        "AP Messages": "Progression"
    }

class PokemonEmeraldFlitStartInventory(StartInventory):
    __doc__ = StartInventory.__doc__ + "\n\n    Currently, your starting inventory will be placed in your PC's item storage."

class PokemonEmeraldFlitStartInventoryPool(StartInventoryPool):
    __doc__ = StartInventoryPool.__doc__ + "\n    Currently, your starting inventory will be placed in your PC's item storage."
    

@dataclass
class PokemonEmeraldFlitOptions(PerGameCommonOptions):
    goals: Goals
    #death_link: PokemonEmeraldFlitDeathLink
    game_options: GameOptions
    reusable_tms: ReusableTms
    exclude_postgame_locations: ExcludePostHofLocations
    #remote_items: RemoteItems
    #wonder_trade: WonderTrade
    challenge_mode: ChallengeMode

    shuffle_overworld: ShuffleOverworldItems
    shuffle_hidden: ShuffleHiddenItems
    shuffle_badges: ShuffleBadges
    shuffle_bikes: ShuffleBikes
    shuffle_gifts: ShuffleNpcGifts
    #shuffle_rods: ShuffleRods
    shuffle_tickets: ShuffleEventTickets
    #shuffle_bag: ShuffleBag
    #shuffle_pokedex: ShufflePokedex
    #shuffle_pokenav: ShufflePokenav
    #shuffle_shoes: ShuffleRunningShoes
    #trainersanity: Trainersanity
    #dexsanity: Dexsanity

    require_itemfinder: RequireItemfinder
    require_flash: RequireFlash
    #random_starting_town: RandomStartingTown
    #random_starting_town_blacklist: RandomStartingTownBlacklist
    norman_requirement: NormanRequirement
    norman_count: NormanCount
    e4_requirement: HoennEliteFourRequirement
    e4_count: HoennEliteFourCount
    remove_badge_requirement: HoennRemoveBadgeRequirement
    #easier_cracked_floors: EasierCrackedFloors

    start_inventory: PokemonEmeraldFlitStartInventory
    start_inventory_from_pool: PokemonEmeraldFlitStartInventoryPool

OPTION_GROUPS = [
    OptionGroup(
        "Item & Location Options", [
            PokemonEmeraldFlitStartInventory,
            PokemonEmeraldFlitStartInventoryPool,
        ], True,
    )
]
