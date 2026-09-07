import bsdiff4
import struct
from typing import TYPE_CHECKING, Dict, List, Tuple

from worlds.Files import APPatchExtension, APProcedurePatch, APTokenMixin, APTokenTypes
from settings import get_settings

from .constants import GAME_NAME, ROM_HASH
from .data import GAME_OPTIONS, GameOptionGroup, data
from .locations import PokemonEmeraldFlitLocation
from .util import BIT_TABLE

if TYPE_CHECKING:
    from . import PokemonEmeraldFlitWorld

class PokemonEmeraldFlitPatchExtension(APPatchExtension):
    game = GAME_NAME

class PokemonEmeraldFlitProcedurePatch(APProcedurePatch, APTokenMixin):
    game = GAME_NAME
    hash = ROM_HASH
    patch_file_ending = ".apemeraldflit"
    result_file_ending = ".gba"

    procedure = [
        ("apply_bsdiff4", ["base_patch.bsdiff4"]),  # first apply the basepatch...
        ("apply_tokens", ["token_data.bin"])  # then the token data, which is created in write_tokens below
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_settings().pokemon_emerald_flit_settings.rom_file, "rb") as infile:
            base_rom_bytes = bytes(infile.read())

        return base_rom_bytes

def write_tokens(world: "PokemonEmeraldFlitWorld", patch: PokemonEmeraldFlitProcedurePatch) -> None:
    location_info: List[Typle[int, int, str]]= []
    for location in world.multiworld.get_locations(world.player):
        assert isinstance(location, PokemonEmeraldFlitLocation)
        if location.address is None:
            continue
        if location.item is None:
            continue

        item_address = location.item_address
        item_id = location.item.code
        #if not world.options.remote_items and location.item.player == world.player:
        #    item_id = location.item.code
        #else:
        #    item_id = data.constants["ITEM_ARCHIPELAGO"]

        if type(item_address) is int:
            patch.write_token(
                APTokenTypes.WRITE,
                item_address,
                struct.pack("<H", item_id)
            )
        elif type(item_address) is list:
            for address in item_address:
                patch.write_token(
                APTokenTypes.WRITE,
                address,
                struct.pack("<H", item_id)
            )

        # create a list of item info to store in tables later. the tables are used to display the item and player name
        # in a text box. in the case of not enough space, the game will default to "found an ARCHIPELAGO ITEM"
        location_info.append((location.address, location.item.player, location.item.name))

    player_name_ids: Dict[str, int] = {world.player_name: 0}
    player_name_address = data.rom_addresses["gArchipelagoPlayerNames"]
    for i, (flag, item_player, item_name) in enumerate(sorted(location_info, key=lambda t: t[0])):
        if item_player == world.player or world.multiworld.is_race:
            patch.write_token(
                APTokenTypes.WRITE,
                data.rom_addresses["gArchipelagoNameTable"] + (i * 5) + 0,
                struct.pack("<H", flag)
            )
            patch.write_token(
                APTokenTypes.WRITE,
                data.rom_addresses["gArchipelagoNameTable"] + (i * 5) + 2,
                struct.pack("<H", flag)
            )
            patch.write_token(
                APTokenTypes.WRITE,
                data.rom_addresses["gArchipelagoNameTable"] + (i * 5) + 4,
                struct.pack("<H", flag)
            )
        else:
            player_name = world.multiworld.get_player_name(item_player)

            if player_name not in player_name_ids:
                # only space for 50 names
                if len(player_name_ids) >= 50:
                    continue

                player_name_ids[player_name] = lenn(player_name_ids)
                for j, b in enumerate(encode_string(player_name, 17)):
                    patch.write_token(
                        APTokenTypes.WRITE,
                        data.rom_addresses["gArchipelagoPlayerNames"] + (player_name_ids[player_name] * 17) + j,
                        struct.pack("<B", b)
                    )

            if item_name not in item_name_offsets:
                if len(item_name) > 35:
                    item_name = item_name[:34] + "…"

                # only 36 * 250 bytes for item names
                if next_item_name_offset + len(item_name) + 1 > 36 * 250:
                    continue

                item_name_offsets[item_name] = next_item_name_offset
                next_item_name_offset += len(item_name) + 1
                patch.write_token(
                    APTokenTypes.WRITE,
                    data.rom_addresses["gArchipelagoItemNames"] + (item_name_offsets[item_name]),
                    encode_string(item_name) + b"\xFF"
                )

            # there should always be enough space for one entry per location
            patch.write_token(
                APTokenTypes.WRITE,
                data.rom_addresses["gArchipelagoNameTable"] + (i * 5) + 0,
                struct.pack("<H", flag)
            )
            patch.write_token(
                APTokenTypes.WRITE,
                data.rom_addresses["gArchipelagoNameTable"] + (i * 5) + 2,
                struct.pack("<H", item_name_offsets[item_name])
            )
            patch.write_token(
                APTokenTypes.WRITE,
                data.rom_addresses["gArchipelagoNameTable"] + (i * 5) + 4,
                struct.pack("<B", player_name_ids[player_name])
            )

    start_inventory = world.options.start_inventory.value.copy()

    badges = (
        "Stone Badge",
        "Knuckle Badge",
        "Dynamo Badge",
        "Heat Badge",
        "Balance Badge",
        "Feather Badge",
        "Mind Badge",
        "Rain Badge"
    )

    starting_badges = 0
    for i, badge in enumerate(badges):
        if start_inventory.pop(badge, 0) > 0:
            starting_badges |= BIT_TABLE[i]

    # TODO: add starting items to bag instead
    pc_slots: List[Tuple[str, int]] = []
    while any(qty > 0 for qty in start_inventory.values()):
        if len(pc_slots) >= 19:
            break

        for i, item_name in enumerate(start_inventory.keys()):
            if len(pc_slots) >= 19:
                break

            quantity = min(start_inventory[item_name], 999)
            if quantity == 0:
                continue

            start_inventory[item_name] -= quantity

            pc_slots.append((item_name, quantity))

    pc_slots.sort(reverse=True)

    for i, slot in enumerate(pc_slots):
        address = data.rom_addresses["sNewGamePCItems"] + (i * 4)
        item = world.item_name_to_id[slot[0]]
        patch.write_token(APTokenTypes.WRITE, address + 0, struct.pack("<H", item))
        patch.write_token(APTokenTypes.WRITE, address + 2, struct.pack("<H", slot[1]))

    # struct ArchipelagoOptions
    # {
    #     /* 0x00 */ u16 introSpecies;
    #     /* 0x02 */ u16 pcItem;
    #     /* 0x04 */ u8 startingLocation;
    #     /* 0x05 */ u8 startingSpawn;
    # 
    #     /* 0x06 */ u16 expPercentMultiplier;
    #     /* 0x08 */ u8 optionsWindowFrameType:5;
    #                u8 normalizeEncounterRates:1;
    #                u8 optionsTextSpeed:2;
    #     /* 0x09 */ u8 optionsTurboButton:2; // 0=off, 1=A, 2=B, 3=A/B
    #                u8 optionsButtonMode:2;
    #                u8 optionsBattleScene:1;
    #                u8 optionsBattleStyle:1;
    #                u8 optionsSound:1; // mono/stereo
    #                u8 optionsSkipFanfares:1;
    #     /* 0x0A */ u8 optionsBikeMusic:1;
    #                u8 optionsSurfMusic:1;
    #                u8 optionsLowHpBeep:1;
    #                u8 optionsSkipNicknames:1;
    #                u8 optionsReceivedItemMessageFilter:2;
    #                u8 optionsReceivedItemSound:1;
    #                u8 optionsGuaranteedCatch:1;
    #     /* 0x0B */ u8 optionsGuaranteedRun:1;
    #                u8 optionsDeathLink:1;
    #                u8 optionsBlindTrainers:1;
    #                u8 optionsAutoRun:1; // automatic running shoes
    #                u8 reusableTms:1;
    #                u8 purgeSpinners:1;
    #                u8 matchTrainerLevels:1;
    #                u8 optionsGuaranteedReelFish:1;
    #     /* 0x0C */ u8 unlockSeenDexInfo;
    #     /* 0x0D */ s8 matchTrainerLevelBonus;
    #     /* 0x0E */ bool8 betterShopsEnabled;
    # 
    #     /* 0x0F */ bool8 eliteFourNeedsGyms;
    #     /* 0x10 */ u8 eliteFourRequiredCount;
    #     /* 0x11 */ bool8 normanNeedsGyms;
    #     /* 0x12 */ u8 normanRequiredCount;
    # 
    #     /* 0x13 */ u8 removeBadgeRequirement;
    #     /* 0x14 */ u8 additionalDarkCaves;
    #     /* 0x15 */ u8 freeFlyHmLocation;
    #     /* 0x16 */ u8 freeFlyPokenavLocation;
    #     /* 0x17 */ u8 terraCaveLocationId:4;
    #     /* 0x18 */ u8 marineCaveLocationId:4;
    # 
    #     /* 0x19 */ bool8 addRoute115Boulders;
    #     /* 0x1A */ bool8 addBumpySlopes;
    #     /* 0x1B */ bool8 modifyRoute118;
    #     /* 0x1C */ u16 removedBlockers;
    #     
    #     /* 0x1E */ bool8 berryTreesRandomized;
    #     /* 0x1F */ bool8 isTrainersanity;
    #     /* 0x20 */ bool8 isDexsanity;
    #     /* 0x21 */ bool8 isShopsanity;
    #     /* 0x22 */ bool8 flyUnlocks;
    #     /* 0x23 */ bool8 extraKeyItems;
    #     /* 0x24 */ bool8 gymKeys;
    #     /* 0x25 */ bool8 shuffleBag;
    #     /* 0x26 */ u8 shufflePokedex; // 0=no, 1=yes, 2=progressive
    #     /* 0x27 */ bool8 shufflePokenav;
    #     /* 0x28 */ bool8 shuffleRunningShoes;
    # 
    #     /* 0x?? */ u32 startingMoney;
    #     /* 0x30 */ u8 startingBadges;
    #     /* 0x31 */ bool8 wonderTradeAllowed;
    #     /* 0x32 */ bool8 remoteItems;
    #     /* 0x33 */ bool8 isChallengeMode;
    # };  // offsets may be incorrect from unlockSeenDexInfo to startingMoney. i'll worry about it as i implement those features...
    options_address = data.rom_addresses["gArchipelagoOptions"]

    # set pokemon in birch intro
    #patch.write_token(
    #    APTokenTypes.WRITE,
    #    options_address + 0x00,
    #    struct.pack("<H", world.random.choice(list(data.species.keys())))
    #)

    # options from 0x08 through 0x0B are bitpacked
    game_options_1: int = 0
    game_options_2: int = 0
    for option_name, option in GAME_OPTIONS.items():
        if option_name.title() in world.options.game_options.value.keys():
            value = option.options[world.options.game_options.value[option_name.title()]]
        else:
            value = option.default

        if option.option_group == GameOptionGroup.GROUP_ONE:
            game_options_1 |= (value << option.option_number)
        elif option.option_group == GameOptionGroup.GROUP_TWO:
            game_options_2 |= (value << option.option_number)
    
    #if world.options.death_link:
    #    game_options_2 |= BIT_TABLE[9]
    
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x08,
        struct.pack("<H", game_options_1)
    )
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x0A,
        struct.pack("<H", game_options_2)
    )

    # set elite four requirement
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x0F,
        struct.pack("<B", world.options.e4_requirement.value)
    )

    # set elite four count
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x0F,
        struct.pack("<B", world.options.e4_count.value)
    )
    
    # set norman requirement
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x11,
        struct.pack("<B", world.options.norman_requirement.value)
    )

    # set norman count
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x12,
        struct.pack("<B", world.options.norman_count.value)
    )

    # set remove badge requirements
    hms = (
        "Cut",
        "Flash",
        "Rock Smash",
        "Strength",
        "Surf",
        "Fly",
        "Dive",
        "Waterfall"
    )

    remove_badge_requirements = 0
    for i, hm in enumerate(hms):
        if hm in world.options.remove_badge_requirement.value:
            remove_badge_requirements |= BIT_TABLE[i]

    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x13,
        struct.pack("<B", remove_badge_requirements)
    )

    # set starting money
    #patch.write_token(
    #    APTokenTypes.WRITE,
    #    options_address + 0x29,
    #    struct.pack("<I", world.options.starting_money.value)
    #)

    # set starting badges
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x30,
        struct.pack("<B", starting_badges)
    )

    # set challenge mode
    patch.write_token(
        APTokenTypes.WRITE,
        options_address + 0x33,
        struct.pack("<B", world.options.challenge_mode.value)
    )

    # set slot auth
    patch.write_token(APTokenTypes.WRITE, data.rom_addresses["gArchipelagoInfo"], world.auth)

    patch.write_file("token_data.bin", patch.get_token_binary())
