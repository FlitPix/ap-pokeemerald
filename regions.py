from typing import TYPE_CHECKING, Dict, List, Tuple

from BaseClasses import ItemClassification, Region

from .data import data
from .items import PokemonEmeraldFlitItem
from .locations import PokemonEmeraldFlitLocation

if TYPE_CHECKING:
    from . import PokemonEmeraldFlitWorld


class PokemonEmeraldFlitRegion(Region):
    def __init(self,
        name: str,
        player: int,
        multiworld
    ):
        super().__init__(name, player, multiworld)

def create_regions(world: "PokemonEmeraldFlitWorld") -> Dict[str, Region]:
    """
    Iterates through regions created from `/data/regions` JSONs to create regions and add them to the multiworld.
    Also creates and places events, and connects regions via warps and the exits defined in JSON.
    """

    regions: Dict[str, Region] = {}
    connections: List[Tuple[str, str, str]] = []
    for region_id, region_data in data.regions.items():
        region_name = region_data.name if region_data.name is not None else region_id
        new_region = PokemonEmeraldFlitRegion(region_name, world.player, world.multiworld)

        for event_id in region_data.events:
            event_data = data.events[event_id]
            event = PokemonEmeraldFlitLocation(world.player,
                                               event_data.name,
                                               None,
                                               event_data.category,
                                               new_region
                                              )
            event.place_locked_item(PokemonEmeraldFlitItem(event_data.item,
                                                           ItemClassification.progression,
                                                           None,
                                                           world.player
                                                          ))
            event.show_in_spoiler = False
            new_region.locations.append(event)

        for exit_region_id, exit_names in region_data.exits.items():
            exit_region_name = data.regions[exit_region_id].name
            if type(exit_names) is list:
                for exit_name in exit_names:
                    connections.append((exit_name, region_name, exit_region_name))
            else:
                connections.append((exit_names, region_name, exit_region_name))

        for warp in region_data.warps:
            source_warp = data.warps[warp]
            dest_warp = data.warps[data.warp_map[warp]]
            if dest_warp.parent_region_id is None:
                continue
            dest_region_name = data.regions[dest_warp.parent_region_id].name
            connections.append((source_warp.name, region_name, dest_region_name))

        regions[region_name] = new_region

    for name, source, dest in connections:
        regions[source].connect(regions[dest], name)
    
    regions["Menu"] = PokemonEmeraldFlitRegion("Menu", world.player, world.multiworld)
    # TODO: use starting town instead
    regions["Menu"].connect(regions["LITTLEROOT TOWN"], "Start Game")

    return regions
