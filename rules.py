from collections import defaultdict
from typing import TYPE_CHECKING

from rule_builder.rules import (Rule, CanReachEntrance, Has, HasAll, HasAny, OptionFilter, True_, False_)

from .data import LocationCategory, data
from .options import Goals, RequireItemfinder
from .locations import PokemonEmeraldFlitLocation
from .logic import HasNBadges, HasNGyms, CanCut, CanFly, CanSurf, CanStrength, CanFlash, CanRockSmash, CanWaterfall, CanDive, HasPetalburgGymRequirements, HasEliteFourRequirements, HasTerraMarineCaveRequirements

if TYPE_CHECKING:
    from . import PokemonEmeraldFlitWorld


def set_rules(world: "PokemonEmeraldFlitWorld") -> None:
    entrance_rules: defaultdict[str, Rule] = defaultdict(True_)
    location_rules: defaultdict[str, Rule] = defaultdict(True_)

    world.set_completion_rule(
        Has(
            "Enter HALL OF FAME",
            options=[OptionFilter(Goals, "Hall of Fame", operator="contains")],
            filtered_resolution=True
        ) &
        Has(
            "Defeat STEVEN",
            options=[OptionFilter(Goals, "Steven", operator="contains")],
            filtered_resolution=True
        )
    )

    # Fly
    entrance_rules["Flying"] = CanFly()
    entrance_rules["LITTLEROOT TOWN Fly Point"] = Has("Visited LITTLEROOT TOWN")
    entrance_rules["OLDALE TOWN Fly Point"] = Has("Visited OLDALE TOWN")
    entrance_rules["PETALBURG CITY Fly Point"] = Has("Visited PETALBURG CITY")
    entrance_rules["RUSTBORO CITY Fly Point"] = Has("Visited RUSTBORO CITY")
    entrance_rules["DEWFORD TOWN Fly Point"] = Has("Visited DEWFORD TOWN")
    entrance_rules["SLATEPORT CITY Fly Point"] = Has("Visited SLATEPORT CITY")
    entrance_rules["MAUVILLE CITY Fly Point"] = Has("Visited MAUVILLE CITY")
    entrance_rules["VERDANTURF TOWN Fly Point"] = Has("Visited VERDANTURF TOWN")
    entrance_rules["FALLARBOR TOWN Fly Point"] = Has("Visited FALLARBOR TOWN")
    entrance_rules["LAVARIDGE TOWN Fly Point"] = Has("Visited LAVARIDGE TOWN")
    entrance_rules["FORTREE CITY Fly Point"] = Has("Visited FORTREE CITY")
    entrance_rules["LILYCOVE CITY Fly Point"] = Has("Visited LILYCOVE CITY")
    entrance_rules["MOSSDEEP CITY Fly Point"] = Has("Visited MOSSDEEP CITY")
    entrance_rules["SOOTOPOLIS CITY Fly Point"] = Has("Visited SOOTOPOLIS CITY")
    entrance_rules["PACIFIDLOG TOWN Fly Point"] = Has("Visited PACIFIDLOG TOWN")
    entrance_rules["EVER GRANDE CITY Fly Point"] = Has("Visited EVER GRANDE CITY")
    entrance_rules["HOENN POKeMON LEAGUE Fly Point"] = Has("Visited HOENN POKeMON LEAGUE")
    entrance_rules["BATTLE FRONTIER Fly Point"] = Has("Visited BATTLE FRONTIER")

    # Littleroot Town
    location_rules["LITTLEROOT TOWN - Gift 1 from NORMAN"] = Has("Enter HALL OF FAME")
    location_rules["LITTLEROOT TOWN - Gift 2 from NORMAN"] = Has("Enter HALL OF FAME")
    location_rules["LITTLEROOT TOWN - Gift 3 from NORMAN"] = Has("Enter HALL OF FAME")
    location_rules["LITTLEROOT TOWN - Gift 4 from NORMAN"] = Has("Enter HALL OF FAME")
    location_rules["LITTLEROOT TOWN - Gift 5 from NORMAN"] = Has("Enter HALL OF FAME")

    # Petalburg City
    location_rules["PETALBURG CITY - Gift from WALLY's Uncle"] = Has("Defeat NORMAN")
    entrance_rules["PETALBURG CITY South Surfing Spot"] = CanSurf()
    entrance_rules["PETALBURG CITY North Surfing Spot"] = CanSurf()
    entrance_rules["Speed Room Door"] = HasPetalburgGymRequirements()
    entrance_rules["Accuracy Room Door"] = HasPetalburgGymRequirements()

    # Dewford Town
    #entrance_rules["MR. BRINEY Sails to SLATEPORT"]
    #entrance_rules["MR. BRINEY Sails Home"]
    entrance_rules["DEWFORD TOWN Surfing Spot"] = CanSurf()

    # Rustboro City
    location_rules["RUSTBORO CITY - Return DEVON GOODS"] = Has("Devon Goods")

    # Devon Corp
    entrance_rules["DEVON CORP. 1F Stairs"] = Has("Meet MR. STONE")

    # Lavaridge Town
    location_rules["LAVARIDGE TOWN - Gift from Rival"] = Has("Defeat FLANNERY")

    # Fortree City
    entrance_rules["FORTREE CITY Before Gym"] = Has("Devon Scope")
    entrance_rules["FORTREE CITY Main"] = Has("Devon Scope")

    # Lilycove City
    entrance_rules["LILYCOVE CITY Surfing Spot"] = CanSurf()
    entrance_rules["LILYCOVE HARBOR Board with S.S. TICKET"] = Has("S.S. Ticket")
    entrance_rules["LILYCOVE HARBOR Board with EON TICKET"] = Has("Eon Ticket")
    entrance_rules["LILYCOVE HARBOR Board with OLD SEA MAP"] = Has("Old Sea Map")
    entrance_rules["LILYCOVE HARBOR Board with AURORATICKET"] = Has("AuroraTicket")
    entrance_rules["LILYCOVE HARBOR Board with MYSTICTICKET"] = Has("MysticTicket")
    entrance_rules["LILYCOVE CITY East Exit"] = (
        #OptionFilter(WorldBlockers, "Remove Lilycove City Wailmer", operator="contains") |
        Has("Clear AQUA HIDEOUT")
    )
    entrance_rules["ROUTE 124 West Exit"] = (
        #OptionFilter(WorldBlockers, "Remove Lilycove City Wailmer", operator="contains") |
        Has("Clear AQUA HIDEOUT")
    )

    # Mossdeep City
    location_rules["MOSSDEEP SPACE STATION 2F - MAXIE Battle"] = Has("Defeat TATE AND LIZA")
    location_rules["MOSSDEEP CITY - STEVEN Gives DIVE"] = Has("Liberate MOSSDEEP SPACE STATION")
    location_rules["MOSSDEEP CITY - Gift from STEVEN"] = Has("Liberate MOSSDEEP SPACE STATION")

    entrance_rules["MOSSDEEP CITY Surfing Spot"] = CanSurf()

    # Sootopolis City
    location_rules["SOOTOPOLIS CITY - Gift from WALLACE"] = Has("RAYQUAZA Stops Fight")
    location_rules["SOOTOPOLIS CITY - RAYQUAZA Stops Fight"] = Has("Release KYOGRE")

    entrance_rules["SOOTOPOLIS CITY Dive Spot"] = CanDive()
    entrance_rules["SOOTOPOLIS CITY East Surfing Spot"] = CanSurf()
    entrance_rules["SOOTOPOLIS CITY West Surfing Spot"] = CanSurf()
    entrance_rules["SOOTOPOLIS CITY KIRI's Island Surfing Spot"] = CanSurf()
    entrance_rules["SOOTOPOLIS CITY GYM Island Surfing Spot"] = CanSurf()
    entrance_rules["CAVE OF ORIGIN"] = Has("Release KYOGRE")
    entrance_rules["SOOTOPOLIS GYM"] = Has("RAYQUAZA Stops Fight")

    # Pacifidlog Town
    entrance_rules["PACIFIDLOG TOWN Surfing Spot"] = CanSurf()

    # Ever Grande City (South)
    # TODO: split into two regions so surf encounters doesn't logically require Waterfall
    entrance_rules["EVER GRANDE CITY Landing Spot"] = CanWaterfall()
    entrance_rules["EVER GRANDE CITY Surfing Spot"] = CanSurf()

    # Ever Grande City (North)
    entrance_rules["HOENN POKeMON LEAGUE Behind Badge Checkers"] = HasEliteFourRequirements()

    # Battle Frontier
    entrance_rules["Board S.S. Tidal from BATTLE FRONTIER"] = Has("S.S. Ticket")
    entrance_rules["BATTLE FRONTIER West Surfing Spot"] = CanSurf()
    entrance_rules["BATTLE FRONTIER After SUDOWOODO"] = Has("Wailmer Pail")
    entrance_rules["BATTLE FRONTIER Before SUDOWOODO"] = Has("Wailmer Pail")
    entrance_rules["BATTLE FRONTIER East Surfing Spot"] = CanSurf()
    entrance_rules["BATTLE FRONTIER Water West to East"] = CanWaterfall()

    # Route 102
    entrance_rules["ROUTE 102 Surfing Spot"] = CanSurf()

    # Route 103
    entrance_rules["ROUTE 103 West Surfing Spot"] = CanSurf()
    entrance_rules["ROUTE 103 East Surfing Spot"] = CanSurf()
    entrance_rules["ROUTE 103 East CUT Tree"] = CanCut()

    # Route 104
    entrance_rules["ROUTE 104 South Surfing Spot"] = CanSurf()
    entrance_rules["ROUTE 104 North Surfing Spot"] = CanSurf()
    entrance_rules["ROUTE 104 North Past CUT Tree"] = CanCut()
    #entrance_rules["MR. BRINEY Sails to DEWFORD from Home"] = (
    #    OptionFilter(WorldBlockers, "Mr. Briney at Start", "contains") |
    #    Has("Meet MR. STONE")
    #)

    # Route 105
    entrance_rules["ROUTE 105 Island Cave"] = Has("Release LEGENDARY GIANTS")
    #entrance_rules["ROUTE 105 North Dive Spot"] = HasTerraMarineCaveRequirements("MARINE CAVE: ROUTE 105 North")
    #entrance_rules["ROUTE 105 North Dive Spot"] = HasTerraMarineCaveRequirements("MARINE CAVE: ROUTE 105 South")

    # Route 106
    entrance_rules["ROUTE 106 Alcove Surfing Spot"] = CanSurf()
    entrance_rules["ROUTE 106 East Surfing Spot"] = CanSurf()

    # Route 107
    entrance_rules["DEWFORD TOWN East Exit"] = CanSurf()

    # Route 109
    #entrance_rules["MR. BRINEY Sails to DEWFORD from SLATEPORT"] = (
    #    OptionsFilter(WorldBlockers, "Mr. Briney All Destinations at Start", operator="contains") |
    #    (
    #        CanReachEntrance("MR. BRINEY Sails to DEWFORD from Home") &
    #        CanReachEntrance("MR. BRINEY Sails to SLATEPORT")
    #    )
    #)
    entrance_rules["ROUTE 109 Surfing Spot"] = CanSurf()

    # Route 110
    entrance_rules["ROUTE 110 South Surfing Spot"] = CanSurf()
    entrance_rules["ROUTE 110 North Surfing Spot"] = CanSurf()
    entrance_rules["HOENN CYCLING ROAD North Entrance West -> East"] = HasAny("Acro Bike", "Mach Bike")
    entrance_rules["HOENN CYCLING ROAD South Entrance West -> East"] = HasAny("Acro Bike", "Mach Bike")
    entrance_rules["ROUTE 110 South -> Main"] = Has("Liberate OCEANIC MUSEUM")
    entrance_rules["ROUTE 110 Main -> South"] = Has("Liberate OCEANIC MUSEUM")

    # Route 111
    entrance_rules["ROUTE 111 Middle -> Desert"] = Has("Go Goggles")
    entrance_rules["ROUTE 111 North -> Desert"] = Has("Go Goggles")
    entrance_rules["ROUTE 111 Up Slope"] = Has("Mach Bike")
    entrance_rules["ROUTE 111 South Past Rocks"] = CanRockSmash()
    entrance_rules["ROUTE 111 South Surfing Spot"] = CanSurf()
    entrance_rules["ROUTE 111 Middle Past Rocks"] = CanRockSmash()
    entrance_rules["TRAINER HILL"] = Has("Enter HALL OF FAME")
    entrance_rules["ROUTE 111 Desert Cave"] = Has("Release LEGENDARY GIANTS")

    # Route 112
    entrance_rules["ROUTE 112 SE Past Fence"] = Has("TEAM MAGMA Steals METEORITE")
    entrance_rules["ROUTE 112 CABLE CAR Station Entrance Past Fence"] = Has("TEAM MAGMA Steals METEORITE")

    # Route 114
    entrance_rules["ROUTE 114 Surfing Spot"] = CanSurf()
    entrance_rules["ROUTE 114 Ascend Waterfall"] = CanWaterfall()
    entrance_rules["FOSSIL MANIAC's Tunnel North Exit"] = Has("Enter HALL OF FAME")
    #entrance_rules["ROUTE 114 North TERRA CAVE Entrance"] = HasTerraMarineCaveRequirements("TERRA CAVE: Route 114 North")
    #entrance_rules["ROUTE 114 South TERRA CAVE Entrance"] = HasTerraMarineCaveRequirements("TERRA CAVE: Route 114 South")

    # Route 115
    entrance_rules["ROUTE 115 South Surfing Spot"] = CanSurf()
    entrance_rules["ROUTE 115 Middle Surfing Spot"] = CanSurf()
    entrance_rules["ROUTE 115 Past Rock"] = CanRockSmash()
    entrance_rules["ROUTE 115 North Surfing Spot"] = CanSurf()
    entrance_rules["ROUTE 115 Up Slope"] = Has("Mach Bike")
    #entrance_rules["ROUTE 115 TERRA CAVE Entrance Below Slope"] = HasTerraMarineCaveRequirements("TERRA CAVE: ROUTE 115 Below Slope")
    # placeholders for world state options
    entrance_rules["ROUTE 115 Middle Beach -> South Above Ledge"] = False_()
    entrance_rules["ROUTE 115 South Above Ledge -> Middle Beach"] = False_()
    entrance_rules["ROUTE 115 South Below Ledge -> Above Ledge"] = False_()

    # Route 116
    entrance_rules["ROUTE 116 Past CUT Tree"] = CanCut()
    #entrance_rules["ROUTE 116 West TERRA CAVE Entrance"] = HasTerraMarineCaveRequirements("TERRA CAVE: ROUTE 116 West")
    #entrance_rules["ROUTE 116 West TERRA CAVE Entrance"] = HasTerraMarineCaveRequirements("TERRA CAVE: ROUTE 116 East")

    # Route 117
    entrance_rules["ROUTE 117 Surfing Spots"] = CanSurf()

    # Route 118
    entrance_rules["ROUTE 118 West Surfing Spot"] = CanSurf()
    entrance_rules["ROUTE 118 East Surfing Spot"] = CanSurf()
    #entrance_rules["ROUTE 118 West TERRA CAVE Entrance"] = HasTerraMarineCaveRequirements("TERRA CAVE: ROUTE 118 West")
    #entrance_rules["ROUTE 118 East TERRA CAVE Entrance"] = HasTerraMarineCaveRequirements("TERRA CAVE: ROUTE 118 East")
    # placeholders for world state options
    entrance_rules["ROUTE 118 West -> East"] = False_()
    entrance_rules["ROUTE 118 East -> West"] = False_()

    # Route 119
    entrance_rules["ROUTE 119 South Surfing Spot"] = CanSurf()
    entrance_rules["ROUTE 119 South Across ACRO Rails"] = Has("Acro Bike")
    entrance_rules["ROUTE 119 South Across ACRO Rails -> South"] = Has("Acro Bike")
    entrance_rules["ROUTE 119 North Surfing Spot"] = CanSurf()
    entrance_rules["ROUTE 119 Ascend Waterfall"] = CanWaterfall()
    entrance_rules["ROUTE 119 Above Waterfall Cross ACRO Rails"] = Has("Acro Bike")
    entrance_rules["ROUTE 119 Above Waterfall Backtrack Across ACRO Rails"] = Has("Acro Bike")
    entrance_rules["ROUTE 119 Middle -> North"] = (
        #OptionFilter(WorldBlockers, "Remove Route 119 Aqua Grunts", operator="contains") |
        Has("Liberate WEATHER INSTITUTE")
    )
    entrance_rules["ROUTE 119 North -> Middle"] = (
        #OptionFilter(WorldBlockers, "Remove Route 119 Aqua Grunts", operator="contains") |
        Has("Liberate WEATHER INSTITUTE")
    )

    # Route 120
    entrance_rules["ROUTE 120 North Down Stairs"] = Has("Devon Scope")
    entrance_rules["ROUTE 120 North Up Stairs"] = Has("Devon Scope")
    entrance_rules["ROUTE 120 North Surfing Spot"] = CanSurf()
    entrance_rules["ROUTE 120 South Past CUT Tree"] = CanCut()
    entrance_rules["ROUTE 120 South Alcove -> South"] = CanCut()
    entrance_rules["ROUTE 120 South Ponds"] = CanSurf()
    entrance_rules["ROUTE 120 South Cave"] = Has("Release LEGENDARY GIANTS")

    # Route 121
    entrance_rules["ROUTE 121 East -> West"] = (
        #OptionFilter(WorldBlockers, "Remove Route 121 Aqua Grunts", operator="contains") |
        CanCut()
    )
    entrance_rules["ROUTE 121 Surfing Spot"] = CanSurf()

    # Route 122
    entrance_rules["ROUTE 122 Surfing Spot"] = CanSurf()

    # Route 123
    entrance_rules["ROUTE 123 Northeast Exit"] = CanSurf()
    entrance_rules["ROUTE 123 East Pond Surfing Spot"] = CanSurf()
    entrance_rules["ROUTE 123 East Past CUT Tree"] = CanCut()

    # Route 124
    entrance_rules["ROUTE 124 Main First Dive Spot Near LILYCOVE"] = CanDive()
    entrance_rules["ROUTE 124 Main Second Dive Spot North of House"] = CanDive()
    entrance_rules["ROUTE 124 Main Dive Spot Closest to House"] = CanDive()
    entrance_rules["ROUTE 124 Main Dive Spot South of House"] = CanDive()
    entrance_rules["ROUTE 124 Main Third Dive Spot Near LILYCOVE"] = CanDive()
    entrance_rules["ROUTE 124 Main Northeast Dive Spot"] = CanDive()
    entrance_rules["ROUTE 124 Main Second Dive Spot Near LILYCOVE"] = CanDive()
    entrance_rules["ROUTE 124 Main Second Dive Spot Southwest of House"] = CanDive()
    entrance_rules["ROUTE 124 North Enclosed Area 1 Dive Spot"] = CanDive()
    entrance_rules["ROUTE 124 North Enclosed Area 2 Dive Spot"] = CanDive()
    entrance_rules["ROUTE 124 North Enclosed Area 3 Dive Spot"] = CanDive()
    entrance_rules["ROUTE 124 South Enclosed Area 1 Dive Spot"] = CanDive()
    entrance_rules["ROUTE 124 South Enclosed Area 2 Dive Spot"] = CanDive()
    entrance_rules["ROUTE 124 South Enclosed Area 3 Dive Spot"] = CanDive()

    # Route 125
    entrance_rules["ROUTE 125 Cave Surfing Spot"] = CanSurf()
    #entrance_rules["ROUTE 125 West Dive Spot"] = HasTerraMarineCaveRequirements("MARINE CAVE: ROUTE 125 West")
    #entrance_rules["ROUTE 125 East Dive Spot"] = HasTerraMarineCaveRequirements("MARINE CAVE: ROUTE 125 East")

    # Route 126
    entrance_rules["ROUTE 126 Main Dive Spot"] = CanDive()
    entrance_rules["ROUTE 126 Southwest Dive Spot"] = CanDive()
    entrance_rules["ROUTE 126 North Dive Spot"] = CanDive()
    entrance_rules["ROUTE 126 Northwest Corner Dive Spot"] = CanDive()
    entrance_rules["ROUTE 126 West South Dive Spot"] = CanDive()
    entrance_rules["ROUTE 126 West North Dive Spot"] = CanDive()

    # Route 127
    entrance_rules["ROUTE 127 Main Dive Spot"] = CanDive()
    entrance_rules["ROUTE 127 Dive Spot Above Southeast Island"] = CanDive()
    entrance_rules["ROUTE 127 Left Dive Spot"] = CanDive()
    entrance_rules["ROUTE 127 Right Dive Spot"] = CanDive()
    entrance_rules["ROUTE 127 Northeast Dive Spot"] = CanDive()
    #entrance_rules["ROUTE 127 Dive Spot Above Northeast Island"] = HasTerraMarineCaveRequirements("MARINE CAVE: ROUTE 127 North")
    entrance_rules["ROUTE 127 South Dive Spot in Enclosed Area"] = CanDive()
    #entrance_rules["ROUTE 127 North Dive Spot in Enclosed Area"] = HasTerraMarineCaveRequirements("MARINE CAVE: ROUTE 127 South")

    # Route 128
    entrance_rules["ROUTE 128 Main Dive Spot"] = CanDive()
    entrance_rules["ROUTE 128 Pupil Dive Spot"] = CanDive()
    entrance_rules["ROUTE 128 East Dive Spot"] = CanDive()

    # Route 129
    #entrance_rules["ROUTE 129 West Dive Spot"] = HasTerraMarineCaveRequirements("MARINE CAVE: ROUTE 129 West")
    #entrance_rules["ROUTE 129 East Dive Spot"] = HasTerraMarineCaveRequirements("MARINE CAVE: ROUTE 129 East")

    # Route 134
    entrance_rules["ROUTE 134 Dive Spot"] = CanDive()

    # Petalburg Woods
    entrance_rules["PETALBURG WOODS MP Past CUT Tree"] = CanCut()
    
    # Rusturf Tunnel
    location_rules["RUSTURF TUNNEL - Gift from Tunneler"] = CanRockSmash()
    location_rules["RUSTURF TUNNEL - Recover DEVON GOODS"] = Has("Defeat ROXANNE")
    entrance_rules["RUSTURF TUNNEL West Past Rocks"] = CanRockSmash()
    entrance_rules["RUSTURF TUNNEL East Past Rocks"] = CanRockSmash()

    # Trick House
    entrance_rules["TRICK HOUSE Complete Puzzle 1"] = CanCut()
    entrance_rules["TRICK HOUSE Begin Puzzle 2"] = HasAll("Dynamo Badge", "Complete TRICK HOUSE Puzzle 1")
    entrance_rules["TRICK HOUSE Begin Puzzle 3"] = HasAll("Heat Badge", "Complete TRICK HOUSE Puzzle 2")
    entrance_rules["TRICK HOUSE Complete Puzzle 3"] = CanRockSmash()
    entrance_rules["TRICK HOUSE Begin Puzzle 4"] = HasAll("Balance Badge", "Complete TRICK HOUSE Puzzle 3")
    entrance_rules["TRICK HOUSE Complete Puzzle 4"] = CanStrength()
    entrance_rules["TRICK HOUSE Begin Puzzle 5"] = HasAll("Feather Badge", "Complete TRICK HOUSE Puzzle 4")
    entrance_rules["TRICK HOUSE Begin Puzzle 6"] = HasAll("Mind Badge", "Complete TRICK HOUSE Puzzle 5")
    entrance_rules["TRICK HOUSE Begin Puzzle 7"] = HasAll("Rain Badge", "Complete TRICK HOUSE Puzzle 6")
    entrance_rules["TRICK HOUSE Begin Puzzle 8"] = HasAll("Enter HALL OF FAME", "Complete TRICK HOUSE Puzzle 7")

    # Desert Ruins
    entrance_rules["DESERT RUINS Cave Entrance"] = CanRockSmash()

    # Fiery Path
    entrance_rules["FIERY PATH Behind Boulder"] = CanStrength()

    # Meteor Falls
    entrance_rules["METEOR FALLS 1F 1R Main Surfing Spot"] = CanSurf()
    entrance_rules["METEOR FALLS 1F 1R Ascend Waterfall"] = CanWaterfall()
    entrance_rules["METEOR FALLS 1F 1R Northwest Platform Exit"] = Has("Enter HALL OF FAME")
    entrance_rules["METEOR FALLS 1F 2R Left Split Surfing Spot"] = CanSurf()
    entrance_rules["METEOR FALLS 1F 2R Right Split Surfing Spot"] = CanSurf()
    entrance_rules["METEOR FALLS B1F 1R Surfing Spot from Ladder"] = CanSurf()
    entrance_rules["METEOR FALLS B1F 1R North Surfing Spot"] = CanSurf()
    entrance_rules["METEOR FALLS B1F 1R South Surfing Spot"] = CanSurf()
    entrance_rules["METEOR FALLS B1F 2R Surfing Spot"] = CanSurf()

    # Jagged Pass
    entrance_rules["JAGGED PASS Bottom -> Middle"] = Has("Acro Bike")
    entrance_rules["JAGGED PASS Middle -> Top"] = Has("Acro Bike")
    entrance_rules["JAGGED PASS Cave"] = Has("Magma Emblem")

    # Mirage Tower
    entrance_rules["MIRAGE TOWER 2F Top Pass Crumble Tiles"] = Has("Mach Bike")
    entrance_rules["MIRAGE TOWER 2F Bottom Pass Crumble Tiles"] = Has("Mach Bike")
    entrance_rules["MIRAGE TOWER 3F Top Past Rocks"] = CanRockSmash()
    entrance_rules["MIRAGE TOWER 3F Bottom Past Rocks"] = CanRockSmash()
    entrance_rules["MIRAGE TOWER 4F FOSSIL Platform"] = CanRockSmash()

    # Abandoned Ship
    entrance_rules["ABANDONED SHIP B1F Bottom-Middle Room Dive Spot"] = (CanSurf() & CanDive())
    entrance_rules["ABANDONED SHIP Hidden Corridors Dive Spot"] = (CanSurf() & CanDive())
    entrance_rules["ABANDONED SHIP Hidden Corridors Bottom-Left Locked Door"] = Has("Room 1 Key")
    entrance_rules["ABANDONED SHIP Hidden Corridors Bottom-Middle Locked Door"] = Has("Room 2 Key")
    entrance_rules["ABANDONED SHIP Hidden Corridors Top-Left Locked Door"] = Has("Room 4 Key")
    entrance_rules["ABANDONED SHIP Hidden Corridors Top-Right Locked Door"] = Has("Room 6 Key")
    entrance_rules["ABANDONED SHIP B1F Corridors Locked Door"] = Has("Storage Key")

    # New Mauville
    entrance_rules["NEW MAUVILLE Entrance North Exit"] = Has("Basement Key")

    # Ancient Tomb
    entrance_rules["ANCIENT TOMB Front North Exit"] = CanFlash()

    # Safari Zone
    entrance_rules["Enter HOENN SAFARI ZONE"] = Has("Pokeblock Case")
    entrance_rules["HOENN SAFARI ZONE South -> North"] = Has("Acro Bike")
    entrance_rules["HOENN SAFARI ZONE Northwest Surfing Spot"] = CanSurf()
    entrance_rules["HOENN SAFARI ZONE Southwest Surfing Spot"] = CanSurf()
    entrance_rules["HOENN SAFARI ZONE Southwest -> Northwest"] = Has("Mach Bike")
    entrance_rules["HOENN SAFARI ZONE South -> Southeast"] = (
        # OptionFilter(WorldBlockers, "Remove Safari Zone Workers", operator="contains") |
        Has("Enter HALL OF FAME")  # change eventually to natdex
    )
    entrance_rules["HOENN SAFARI ZONE Southeast Surfing Spot"] = CanSurf()

    # Magma Hideout
    entrance_rules["MAGMA HIDEOUT 1F Past Entrance Boulders"] = CanStrength()
    entrance_rules["MAGMA HIDEOUT 1F Backtrack to Exit"] = CanStrength()

    # Aqua Hideout
    entrance_rules["AQUA HIDEOUT 1F Landing Spot"] = (
        #OptionFilter(WorldBlockers, "Remove Aqua Hideout Grunts", operator="contains") |
        Has("TEAM AQUA Steals SUBMARINE EXPLORER 1")
    )
    entrance_rules["AQUA HIDEOUT 1F Surfing Spot"] = (
        #OptionFilter(WorldBlockers, "Remove Aqua Hideout Grunts", operator="contains") |
        Has("TEAM AQUA Steals SUBMARINE EXPLORER 1")
    )

    # Shoal Cave
    entrance_rules["SHOAL CAVE High Tide"] = CanSurf()
    entrance_rules["SHOAL CAVE High Tide ER NWC Surfing Spot"] = CanSurf()
    entrance_rules["SHOAL CAVE High Tide ER NEC Surfing Spot"] = CanSurf()
    entrance_rules["SHOAL CAVE High Tide InR EMG South Surfing Spot"] = CanSurf()
    entrance_rules["SHOAL CAVE High Tide InR EMG East Surfing Spot"] = CanSurf()
    entrance_rules["SHOAL CAVE High Tide InR EMG North Surfing Spot"] = CanSurf()
    entrance_rules["SHOAL CAVE High Tide InR SWC Surfing Spot"] = CanSurf()
    entrance_rules["SHOAL CAVE High Tide InR MIP Surfing Spot"] = CanSurf()
    entrance_rules["SHOAL CAVE Low Tide LR NW Past Boulder"] = CanStrength()
    entrance_rules["SHOAL CAVE Low Tide LR East Past Boulder"] = CanStrength()

    # Seafloor Cavern
    entrance_rules["SEAFLOOR CAVERN Entrance Dive Spot"] = CanDive()
    entrance_rules["SEAFLOOR CAVERN Entrance Surfing Spot"] = CanSurf()
    entrance_rules["SEAFLOOR CAVERN Entrance North Exit"] = (
        #OptionFilter(WorldBlockers, "Remove Seafloor Cavern Aqua Grunt", operator="contains") |
        Has("STEVEN Gives DIVE")
    )
    entrance_rules["SEAFLOOR CAVERN R1 South Past Boulder"] = CanRockSmash() & CanStrength()
    entrance_rules["SEAFLOOR CAVERN R1 North Past Boulder"] = CanStrength()
    entrance_rules["SEAFLOOR CAVERN R2 SW -> NW"] = CanStrength()
    entrance_rules["SEAFLOOR CAVERN R2 NW -> SW"] = CanStrength()
    entrance_rules["SEAFLOOR CAVERN R2 SW -> SE"] = CanRockSmash()
    entrance_rules["SEAFLOOR CAVERN R2 SE -> SW"] = CanRockSmash()
    entrance_rules["SEAFLOOR CAVERN R2 NW -> NE"] = CanRockSmash() & CanStrength()
    entrance_rules["SEAFLOOR CAVERN R2 NW -> SE"] = CanRockSmash() & CanStrength()
    entrance_rules["SEAFLOOR CAVERN R5 NW Past Right Boulders"] = CanRockSmash() & CanStrength()
    entrance_rules["SEAFLOOR CAVERN R5 East Past Boulders"] = CanStrength()
    entrance_rules["SEAFLOOR CAVERN R5 NW Past Left Boulders"] = CanRockSmash() & CanStrength()
    entrance_rules["SEAFLOOR CAVERN R5 SW Past Boulders"] = CanRockSmash() & CanStrength()
    entrance_rules["SEAFLOOR CAVERN R6 NW Surfing Spot"] = CanSurf()
    entrance_rules["SEAFLOOR CAVERN R6 South Surfing Spot"] = CanSurf()
    entrance_rules["SEAFLOOR CAVERN R7 North Surfing Spot"] = CanSurf()
    entrance_rules["SEAFLOOR CAVERN R7 South Surfing Spot"] = CanSurf()
    entrance_rules["SEAFLOOR CAVERN STRENGTH Room North Past Boulders"] = CanStrength()
    entrance_rules["SEAFLOOR CAVERN STRENGTH Room South Past Boulders"] = CanStrength()

    # Sky Pillar
    entrance_rules["SKY PILLAR Outside North Exit"] = Has("Release KYOGRE")
    entrance_rules["SKY PILLAR 2F ACT Past Crumble Tiles"] = Has("Mach Bike")
    entrance_rules["SKY PILLAR 2F BCT Past Crumble Tiles"] = Has("Mach Bike")
    entrance_rules["SKY PILLAR 4F BCT Past Crumble Tiles"] = Has("Mach Bike")

    # Sealed Chamber
    entrance_rules["SEALED CHAMBER Outer Room Solve Puzzle"] = Has("Can Learn DIG")

    # Hoenn Victory Road
    entrance_rules["VICTORY ROAD B1F SWP Past Rocks"] = CanRockSmash() & CanStrength()
    entrance_rules["VICTORY ROAD B1F SWPLU Past Rocks"] = CanRockSmash() & CanStrength()
    entrance_rules["VICTORY ROAD B1F MU Ledges"] = CanRockSmash() & CanStrength()
    entrance_rules["VICTORY ROAD B1F MLE Ledge"] = CanRockSmash()
    entrance_rules["VICTORY ROAD B1F MLW Past Lower Rock"] = CanRockSmash() & CanStrength()
    entrance_rules["VICTORY ROAD B1F MLW Past Upper Rocks"] = CanRockSmash() & CanStrength()
    entrance_rules["VICTORY ROAD B2F LW Surfing Spot"] = CanSurf()
    entrance_rules["VICTORY ROAD B2F LWI Surfing Spot"] = CanSurf()
    entrance_rules["VICTORY ROAD B2F LE Surfing Spot"] = CanSurf()
    entrance_rules["VICTORY ROAD B2F LWW Ascend Waterfall"] = CanWaterfall()
    entrance_rules["VICTORY ROAD B2F LEW Ascend Waterfall"] = CanWaterfall()
    entrance_rules["VICTORY ROAD B2F Upper East Surfing Spot"] = CanSurf()
    entrance_rules["VICTORY ROAD B2F Upper West Surfing Spot"] = CanSurf()

    # overworld items
    if world.options.shuffle_overworld:
        # Route 114
        location_rules["ROUTE 114 - Item Behind Smashable Rock"] = CanRockSmash()

        # Route 117
        location_rules["ROUTE 117 - Item Behind Tree"] = CanCut()

        # Victory Road
        location_rules["VICTORY ROAD B1F - Item Behind Boulders"] = CanRockSmash() & CanStrength()
    
    # hidden items
    if world.options.shuffle_hidden:
        # Route 120
        location_rules["ROUTE 120 - Hidden Item Behind Trees"] = CanCut()

        # Route 121
        location_rules["ROUTE 121 - Hidden Item Behind Tree"] = CanCut()
    
    # NPC gifts
    if world.options.shuffle_gifts:
        # Littleroot Town
        location_rules["LITTLEROOT TOWN - Gift from Mom"] = HasAll(
            "Meet MR. STONE",
            "Balance Badge"
        )

        # Devon Corp.
        location_rules["DEVON CORP. 3F - Gift 2 from MR. STONE (Deliver LETTER)"] = Has("Deliver LETTER")

        # Dewford Town
        location_rules["DEWFORD TOWN - Gift from SLUDGE BOMB Man"] = Has("Defeat NORMAN")

        # Slateport City
        location_rules["SLATEPORT CITY - Gift 1 from CAPT. STERN"] = HasAll(
            "TEAM AQUA Steals SUBMARINE EXPLORER 1",
            "Scanner",
            "Mind Badge"
        )
        location_rules["SLATEPORT CITY - Gift 2 from CAPT. STERN"] = HasAll(
            "TEAM AQUA Steals SUBMARINE EXPLORER 1",
            "Scanner",
            "Mind Badge"
        )

        # Mauville City
        location_rules["MAUVILLE CITY - Gift from Wattson (Clear NEW MAUVILLE)"] = HasAll(
            "Defeat NORMAN",
            "Turn Off Generator"
        )

        # Fallarbor Town
        location_rules["FALLARBOR TOWN - Gift from COZMO"] = HasAll(
            "Recover METEORITE",
            "Meteorite"
        )

        # Fortree City
        location_rules["FORTREE CITY - WINGULL Delivery Reward"] = Has("WINGULL Quest Finishes")

        # Route 103
        location_rules["ROUTE 104 - Gift from Lady Near Flower Shop"] = HasAll(
            "Dynamo Badge",
            "Meet FLOWER SHOP Owner"
        )
    
    # add Itemfinder requirement to hidden items
    if world.options.require_itemfinder == RequireItemfinder.option_logic:
        for location in world.multiworld.get_locations(world.player):
            assert isinstance(location, PokemonEmeraldFlitLocation)
            if location.location_id is not None and data.locations[location.location_id].category == LocationCategory.HIDDEN_ITEM:
                location_rules[location.name] &= Has("Itemfinder")
    
    # add Flash requirements to dark caves
    # TODO: convert to and handle OptionSet
    if world.options.require_flash:
        # Granite Cave
        entrance_rules["GRANITE CAVE 1F Lower Ladder"] &= CanFlash()
        entrance_rules["GRANITE CAVE B1F Main Downwards Ladder"] &= CanFlash()

        # Hoenn Victory Road
        entrance_rules["VICTORY ROAD 1F Middle Ladder"] &= CanFlash()
        entrance_rules["VICTORY ROAD 1F Northwest Ladder"] &= CanFlash()
        entrance_rules["VICTORY ROAD 1F Southeast Ladder"] &= CanFlash()
        entrance_rules["VICTORY ROAD B1F Northeast Ladder"] &= CanFlash()
        entrance_rules["VICTORY ROAD B1F SWP Upper Downwards Ladder"] &= CanFlash()
        entrance_rules["VICTORY ROAD B1F SWP Lower Downwards Ladder"] &= CanFlash()
        entrance_rules["VICTORY ROAD B1F Main Downwards Ladder"] &= CanFlash()
        entrance_rules["VICTORY ROAD B2F Southwest Ladder"] &= CanFlash()
        entrance_rules["VICTORY ROAD B2F Center Ladder"] &= CanFlash()
        entrance_rules["VICTORY ROAD B2F Southeast Ladder"] &= CanFlash()
        entrance_rules["VICTORY ROAD B2F Northeast Ladder"] &= CanFlash()

    for name, rule in entrance_rules.items():
        try:
            world.set_rule(world.get_entrance(name), rule)
        except KeyError:
            continue
    
    for name, rule in location_rules.items():
        try:
            world.set_rule(world.get_location(name), rule)
        except KeyError:
            continue
