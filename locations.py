from typing import TYPE_CHECKING, Optional, Dict, List, Set

from BaseClasses import Location, Region, ItemClassification, LocationProgressType

from .constants import GAME_NAME
from .data import LocationCategory, data
from .options import Goals, ShuffleBadges, ShuffleBikes

if TYPE_CHECKING:
    from . import PokemonEmeraldFlitWorld


class PokemonEmeraldFlitLocation(Location):
    game: str = GAME_NAME
    item_address: Optional[int]
    default_item_id: Optional[int]
    category: LocationCategory
    location_id: Optional[str] = None

    def __init__(self,
        player: int,
        name: str,
        address: Optional[int],
        category: LocationCategory,
        parent: Optional[Region] = None,
        item_address: Optional[int] = None,
        default_item_id: Optional[int] = None,
        location_id: Optional[str] = None
    ) -> None:
        super().__init__(player, name, address, parent)
        self.item_address = item_address
        self.default_item_id = default_item_id
        self.category = category
        self.location_id = location_id

def create_location_name_to_id_map() -> Dict[str, int]:
    """
    maps location names to their AP location IDs
    """
    name_to_id_map: Dict[str, int] = {}
    for region_data in data.regions.values():
        for location_id in region_data.locations:
            location_data = data.locations[location_id]
            name_to_id_map[location_data.name] = location_data.flag

    return name_to_id_map

def create_locations(world: "PokemonEmeraldFlitWorld", regions: Dict[str, Region]) -> None:
    def create_location(location_id: str) -> PokemonEmeraldFlitLocation:
        location_data = data.locations[location_id]

        if location_data.default_item == data.constants["ITEM_NONE"]:
            default_item = world.item_name_to_id[get_random_item(world, ItemClassification.filler)]
        else:
            default_item = location_data.default_item
        
        return PokemonEmeraldFlitLocation(
            world.player,
            location_data.name,
            location_data.flag,
            location_data.category,
            region,
            location_data.address,
            default_item,
            location_id
        )

    # these locations are always created. if their options are disabled, events are placed on them later.
    included_categories: Set[str] = {
        LocationCategory.BADGE,
        LocationCategory.HM,
        LocationCategory.KEY,
        LocationCategory.ROD,
        LocationCategory.BIKE,
        LocationCategory.TICKET
    }
    #included_tags: Set[str] = {}

    # these locations are only created if enabled by the player.
    if world.options.shuffle_overworld:
        included_categories.add(LocationCategory.OVERWORLD_ITEM)
    if world.options.shuffle_hidden:
        included_categories.add(LocationCategory.HIDDEN_ITEM)
    if world.options.shuffle_gifts:
        included_categories.add(LocationCategory.NPC_GIFT)

    for region_data in data.regions.values():
        if region_data.name not in regions:
            continue

        region = regions[region_data.name]
        included_locations = [loc for loc in region_data.locations
                              if data.locations[loc].category in included_categories]

        for location_name in included_locations:
            region.locations.append(create_location(location_name))

def exclude_locations(world: "PokemonEmeraldFlitWorld") -> None:
    POST_HALL_OF_FAME_LOCATIONS = [
        "LITTLEROOT TOWN - Gift 1 from NORMAN",
        "LITTLEROOT TOWN - Gift 2 from NORMAN",
        "LITTLEROOT TOWN - Gift 3 from NORMAN",
        "LITTLEROOT TOWN - Gift 4 from NORMAN",
        "LITTLEROOT TOWN - Gift 5 from NORMAN",
        "TRICK HOUSE Puzzle 8 - Item",
        # TEMPORARY: for now, the Safari Zone construction workers don't move until post-HoF.
        # TODO: split into separate list? after pokedex shuffle is fully implemented.
        "SAFARI ZONE NE - Item on Ledge",
        "SAFARI ZONE NE - Hidden Item North",
        "SAFARI ZONE NE - Hidden Item East",
        "SAFARI ZONE SE - Item in Grass",
        "SAFARI ZONE SE - Hidden Item in South Grass 1",
        "SAFARI ZONE SE - Hidden Item in South Grass 2",
    ]

    locations_to_exclude = []

    # exclude post-HoF locations if HoF is the only goal.
    if all(goal == "Hall of Fame" for goal in world.options.goals):
        locations_to_exclude.extend(POST_HALL_OF_FAME_LOCATIONS)

        # Navel Rock can only be accessed with the MysticTicket, so if tickets aren't shuffled, its hidden item is also post-HoF.
        if not world.options.shuffle_tickets:
            locations_to_exclude.append("NAVEL ROCK Summit - Hidden Item Near HO-OH")
    
    for location_name in locations_to_exclude:
        try:
            world.multiworld.get_location(location_name, world.player).progress_type = LocationProgressType.EXCLUDED
        except KeyError:
            continue  # location doesn't exist in this multiworld
