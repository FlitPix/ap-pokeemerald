from typing import TYPE_CHECKING, Dict, FrozenSet, Set, Optional
import logging

from BaseClasses import Item, ItemClassification, LocationProgressType

from .constants import GAME_NAME
from .data import data
from .groups import item_groups
from .locations import PokemonEmeraldFlitLocation, LocationCategory
from .options import ShuffleBadges

if TYPE_CHECKING:
    from . import PokemonEmeraldFlitWorld


class PokemonEmeraldFlitItem(Item):
    game: str = GAME_NAME

    def __init__(self,
        name: str,
        classification: ItemClassification,
        code: Optional[int],
        player: int
    ) -> None:
        super().__init__(name, classification, code, player)

        if code is None:
            self.tags = frozenset(["Event"])
        else:
            self.tags = data.items[code].tags

def create_item_name_to_id_map() -> Dict[str, int]:
    """
    Maps item names to AP item IDs.
    """
    name_to_id_map: Dict[str, int] = {}
    for item_id, item_data in data.items.items():
        name_to_id_map[item_data.name] = item_id
    
    return name_to_id_map

def get_item_classification(item_id: int) -> ItemClassification:
    """
    Returns item classification for given AP item ID.
    """
    return data.items[item_id].classification

def get_random_item(world: "PokemonEmeraldFlitWorld", item_classification: ItemClassification = None) -> str:
    """
    Returns a random item name.
    """
    if item_classification is None:
        item_classification = ItemClassification.useful if world.random.random() < 0.2 else ItemClassification.filler
    items = [item for item in data.items.values()
             if item.classification == item_classification and item.name not in item_groups["Unique Items"]]
    return world.random.choice(items).name

def create_items(world: "PokemonEmeraldFlitWorld") -> None:
    #import logging
    def fill_unrandomized_location(location: PokemonEmeraldFlitLocation, as_event: bool) -> None:
        item = world.create_item_by_id(location.default_item_id)
        # key items considered in access rules but not randomized are converted to events.
        if as_event:
            item.code = None
            location.address = None
            location.show_in_spoiler = False
        location.place_locked_item(item)
        location.progress_type = LocationProgressType.DEFAULT
        #world.item_pool.remove(item)

    item_locations = [
        location
        for location in world.get_locations()
        if location.item is None
    ]

    # filter out progression items that should be replaced with events.
    filter_categories = set()
    if world.options.shuffle_badges == ShuffleBadges.option_vanilla:
        filter_categories.add(LocationCategory.BADGE)
    if not world.options.shuffle_bikes:
        filter_categories.add(LocationCategory.BIKE)
    if not world.options.shuffle_tickets:
        filter_categories.add(LocationCategory.TICKET)

    # if badges are shuffled among gym leaders, still don't add to normal item pool, but do create their items and assign locations now for use in pre fill later.
    #if world.options.shuffle_badges == ShuffleBadges.option_leaders:
    #    world.badge_shuffle_info = [
    #        (location, world.create_item_by_id(location.default_item_id))
    #        for location in [loc for loc in item_locations if loc.category == LocationCategory.BADGE]
    #    ]

    # create events for unrandomized progression items, and place them in vanilla locations
    locations_to_place_events: List[PokemonEmeraldFlitLocation] = [loc for loc in item_locations if loc.category in filter_categories]
    for loc in locations_to_place_events:
        fill_unrandomized_location(loc, True)
    
    # filter down locations to actual items that will be filled, and create the item pool
    item_locations = [loc for loc in item_locations if loc.category not in filter_categories]
    world.item_pool = [world.create_item_by_id(loc.default_item_id) for loc in item_locations]

    # replace copies of unique items placed in starting inventory
    unique_items: Set[str] = set(item_groups["Unique Items"] | item_groups["Progressive Items"])
    for item in world.multiworld.precollected_items[world.player]:
        assert isinstance(item, PokemonEmeraldFlitItem)
        if item.name in unique_items:
            try:
                world.item_pool.remove(item)
                world.item_pool.append(world.create_item(get_random_item(world, ItemClassification.filler)))
            except ValueError:
                continue

    
