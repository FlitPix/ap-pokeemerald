from logging import getLogger
from typing import TYPE_CHECKING, Set, Tuple, Dict

from NetUtils import ClientStatus
from Options import Toggle
from Utils import async_start
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from .constants import GAME_NAME, ROM_NAME
from .data import data
from .options import Goals

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

logger = getLogger("Client")

FLAG_IS_CHAMPION = data.constants["TRAINER_FLAGS_START"] + data.constants["FLAG_IS_CHAMPION"]
FLAG_DEFEATED_STEVEN = data.constants["TRAINER_FLAGS_START"] + data.constants["TRAINER_STEVEN"]

class PokemonEmeraldFlitClient(BizHawkClient):
    game = GAME_NAME
    system = "GBA"
    patch_suffix = ".apemeraldflit"

    local_checked_locations: Set[int]
    goal_flags: Set[str]

    def initialize_client(self):
        self.local_checked_locations = set()
        self.goal_flags = set()
        self.checked_goal_flags = set()

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            rom_name_bytes = ((await bizhawk.read(ctx.bizhawk_ctx, [(0x108, 32, "ROM")]))[0])
            rom_name = bytes([byte for byte in rom_name_bytes if byte != 0]).decode("ascii")
            if not rom_name.startswith("pokemon emerald"):
                return False
            if rom_name == "pokemon emerald version":
                logger.error("ERROR: You seem to be running an unpatched Pokemon Emerald Version ROM. "
                            "You need to generate a patch file and use it to create a patched ROM.")
                return False
            if rom_name != ROM_NAME:
                logger.error("ERROR: The patch file used to create this ROM is not compatible with this client. "
                            "Make sure you're running the same APWorld version as the host/server.")
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False  # try again on next pass

        ctx.game = self.game
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125

        self.initialize_client()

        return True
    
    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        from base64 import b64encode
        auth_raw = (await bizhawk.read(ctx.bizhawk_ctx, [data.rom_addresses["gArchipelagoInfo"], 16, "ROM"]))[0]
        ctx.auth = b64encode(auth_raw).decode("utf-8")

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None:
            return
        
        # set goal flags
        if not bool(self.goal_flags):
            if "Hall of Fame" in ctx.slot_data["goals"]:
                self.goal_flags.add(FLAG_IS_CHAMPION)
            if "Steven" in ctx.slot_data["goals"]:
                self.goal_flags.add(FLAG_DEFEATED_WALLACE)
        
        try:
            guards: Dict[str, Tuple[int, bytes, str]] = {}

            # ensure player is in overworld
            guards["IN OVERWORLD"] = (
                data.ram_addresses["gMain"] + 4,
                (data.ram_addresses["CB2_Overworld"] + 1).to_bytes(4, "little"),
                "System Bus"
            )

            # read save blocks
            read_result = await bizhawk.read(ctx.bizhawk_ctx,
                [
                    (
                        data.ram_addresses["gSaveBlock1Ptr"],
                        4,
                        "System Bus"
                    ),
                    (
                        data.ram_addresses["gSaveBlock2Ptr"],
                        4,
                        "System Bus"
                    )
                ])
            
            # check that save data hasn't moved
            guards["SAVE BLOCK 1"] = (
                data.ram_addresses["gSaveBlock1Ptr"],
                read_result[0],
                "System Bus"
            )
            guards["SAVE BLOCK 2"] = (
                data.ram_addresses["gSaveBlock2Ptr"],
                read_result[1],
                "System Bus"
            )

            sb1_address = int.from_bytes(guards["SAVE BLOCK 1"][1], "little")
            sb2_address = int.from_bytes(guards["SAVE BLOCK 2"][1], "little")

            await self.handle_received_items(ctx, guards)

            # read flags, in two chunks
            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [
                    (sb1_address + 0x1450, 0x96, "System Bus")],  # flags
                [guards["IN OVERWORLD"], guards["SAVE BLOCK 1"]]
            )
            if read_result is None:  # not in overworld, or save block moved
                return
            flag_bytes = read_result[0]

            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [(sb1_address + 0x14E6, 0x96, "System Bus")],  # more flags
                [guards["IN OVERWORLD"], guards["SAVE BLOCK 1"]]
            )
            if read_result is not None:
                flag_bytes += read_result[0]

            local_checked_locations: set[int] = set()

            # check set flags
            for byte_i, byte in enumerate(flag_bytes):
                for i in range(8):
                    if byte & (1 << i) != 0:
                        flag_id = byte_i * 8 + i

                        if flag_id in ctx.server_locations:
                            local_checked_locations.add(flag_id)

                        if flag_id in self.goal_flags and flag_id not in self.checked_goal_flags:
                            self.checked_goal_flags.add(flag_id)
                            #if flag_id == FLAG_IS_CHAMPION:
                            #    logger.info("LEAGUE CHAMPION! CONGRATULATIONS!")
                            #if flag_id == FLAG_DEFEATED_STEVEN:
                            #    logger.info("Player defeated PKMN TRAINER STEVEN!")

            # send locations
            # this check is technically redundant as ctx.check_locations already does it:
            # https://github.com/ArchipelagoMW/Archipelago/blob/main/CommonClient.py#L556
            # but, it may potentially be better to only call ctx.check_locations when actually necessary
            if local_checked_locations != self.local_checked_locations:
                self.local_checked_locations = local_checked_locations
                if local_checked_locations is not None:
                    await ctx.check_locations(local_checked_locations)

            # check for goal
            if not ctx.finished_game and self.goal_flags == self.checked_goal_flags:
                ctx.finished_game = True
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])

        except bizhawk.RequestFailedError:
            # exit handler and return to main loop to reconnect
            pass

    async def handle_received_items(self, ctx: "BizHawkClientContext", guards: Dict[str, Tuple[int, bytes, str]]) -> None:
        """
        Checks the index of the most recently received item and whether the item queue is full. Writes the next item
        into the game if necessary.
        """
        received_item_address = data.ram_addresses["gArchipelagoReceivedItem"]

        sb1_address = int.from_bytes(guards["SAVE BLOCK 1"][1], "little")

        read_result = await bizhawk.guarded_read(
            ctx.bizhawk_ctx,
            [
                (sb1_address + 0x3778, 2, "System Bus"),      # Number of received items
                (received_item_address + 4, 1, "System Bus")  # Received item struct full?
            ],
            [guards["IN OVERWORLD"], guards["SAVE BLOCK 1"]]
        )
        if read_result is None:  # Not in overworld, or save block moved
            return

        num_received_items = int.from_bytes(read_result[0], "little")
        received_item_is_empty = read_result[1][0] == 0

        # If the game hasn't received all items yet and the received item struct doesn't contain an item, then
        # fill it with the next item
        if num_received_items < len(ctx.items_received) and received_item_is_empty:
            next_item = ctx.items_received[num_received_items]
            should_display = 1 if next_item.flags & 1 or next_item.player == ctx.slot else 0
            await bizhawk.write(ctx.bizhawk_ctx, [
                (received_item_address + 0, (next_item.item - BASE_OFFSET).to_bytes(2, "little"), "System Bus"),
                (received_item_address + 2, (num_received_items + 1).to_bytes(2, "little"), "System Bus"),
                (received_item_address + 4, [1], "System Bus"),
                (received_item_address + 5, [should_display], "System Bus"),
            ])
