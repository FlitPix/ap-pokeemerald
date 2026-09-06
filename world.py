import logging
import pkgutil
import os
from typing import ClassVar, Dict, Any, List, Tuple, Optional

from settings import Group, UserFilePath
from worlds.AutoWorld import WebWorld, World
from BaseClasses import Tutorial, MultiWorld, ItemClassification

from .constants import GAME_NAME
from .items import PokemonEmeraldFlitItem, create_items, create_item_name_to_id_map, get_item_classification, get_random_item
from .locations import PokemonEmeraldFlitLocation, create_location_name_to_id_map, create_locations, exclude_locations
from .groups import item_groups, location_groups
from .options import Goals, ExcludePostHofLocations, HoennRemoveBadgeRequirement, PokemonEmeraldFlitOptions, ShuffleBadges, NormanRequirement, OPTION_GROUPS
from .rom import PokemonEmeraldFlitProcedurePatch, write_tokens
from .sanity_check import validate_regions

class PokemonEmeraldFlitWebWorld(WebWorld):
    theme = "ocean"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Pokémon Emerald Version with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Flit"]
    )

    tutorials = [setup_en]
    option_groups = OPTION_GROUPS

class PokemonEmeraldFlitSettings(Group):
    class PokemonEmeraldFlitRomFile(UserFilePath):
        """
        File name of your English Pokémon Emerald Version ROM.
        """
        description = "Pokemon Emerald ROM File"
        copy_to = "Pokemon - Emerald Version (USA, Europe).gba"
        md5s = [PokemonEmeraldFlitProcedurePatch.hash]

    rom_file: PokemonEmeraldFlitRomFile = PokemonEmeraldFlitRomFile(PokemonEmeraldFlitRomFile.copy_to)

class PokemonEmeraldFlitWorld(World):
    """
    Pokémon Emerald Version is an enhanced version of Ruby and Sapphire, and widely considered to be one of the best
    games in the series. Catch, train, and battle Pokémon, stop the plans of Teams Magma and Aqua, and defeat the
    Elite Four to enter the Hall of Fame! Do you have what it takes to become a Pokémon Master?

    This is Flit's version, with many differences.
    """
    game = GAME_NAME
    web = PokemonEmeraldFlitWebWorld()
    topology_present = True

    settings_key = "pokemon_emerald_flit_settings"
    settings: ClassVar[PokemonEmeraldFlitSettings]

    options_dataclass = PokemonEmeraldFlitOptions
    options: PokemonEmeraldFlitOptions

    item_name_to_id = create_item_name_to_id_map()
    location_name_to_id = create_location_name_to_id_map()
    item_name_groups = item_groups
    location_name_groups = location_groups

    #required_client_version = (0, 6, 7)

    item_pool: List[PokemonEmeraldFlitItem]
    badge_shuffle_info: Optional[List[Tuple[PokemonEmeraldFlitLocation, PokemonEmeraldFlitItem]]]
    auth: bytes

    def __init__(self, multiworld, player):
        super(PokemonEmeraldFlitWorld, self).__init__(multiworld, player)
        self.badge_shuffle_info = None
    
    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        assert validate_regions()

    def get_filler_item_name(self) -> str:
        return get_random_item(self, ItemClassification.filler)

    def generate_early(self) -> None:
        # handle local items
        #if self.options.shuffle_badges == ShuffleBadges.option_leaders:
        #    self.options.local_items.value.update(item_groups["Badges"])
        if not self.options.shuffle_bikes:
            self.options.local_items.value.update(item_groups["Bike"])
        if not self.options.shuffle_tickets:
            self.options.local_items.value.update(item_groups["Event Tickets"])

        if self.options.exclude_postgame_locations and "Steven" in self.options.goals:
            logging.warning(f"Flit's Pokemon Emerald: Including postgame locations for player %s (%s), since Steven is set as a goal condition.",
                            self.player, self.player_name)
            self.options.exclude_postgame_locations = ExcludePostHofLocations.option_false

    def create_regions(self) -> None:
        from .regions import create_regions

        regions = create_regions(self)
        create_locations(self, regions)
        self.multiworld.regions.extend(regions.values())
        if self.options.exclude_postgame_locations:
            exclude_locations(self)

    def create_items(self) -> None:
        create_items(self)
        self.multiworld.itempool += self.item_pool

    def set_rules(self) -> None:
        from .rules import set_rules
        set_rules(self)

    def create_item(self, name: str) -> PokemonEmeraldFlitItem:
        return self.create_item_by_id(self.item_name_to_id[name])

    def create_item_by_id(self, item_id: int):
        return PokemonEmeraldFlitItem(
            self.item_id_to_name[item_id],
            get_item_classification(item_id),
            item_id,
            self.player
        )

    def generate_basic(self) -> None:
        self.auth = self.random.getrandbits(16 * 8).to_bytes(16, "little")

    def generate_output(self, output_directory: str) -> None:
        patch = PokemonEmeraldFlitProcedurePatch(player=self.player, player_name=self.player_name)
        patch.write_file("base_patch.bsdiff4", pkgutil.get_data(__name__, "data/base_patch.bsdiff4"))
        write_tokens(self, patch)

        out_file_name = self.multiworld.get_out_file_name_base(self.player)
        patch.write(os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}"))

    def fill_slot_data(self) -> Dict[str, Any]:
        # TODO: add most options to slot data for trackers to use
        slot_data = self.options.as_dict(
            "goals"
        )

        return slot_data
