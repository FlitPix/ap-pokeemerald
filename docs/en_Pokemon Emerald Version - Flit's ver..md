# Pokémon Emerald Version (Flit's ver.)

## Where is the options page?

You can read through all the options and generate a game YAML file [here](../player-options).

## What does randomization do to this game?

This randomizer handles both item and Pokémon randomization. Badges, HMs, gifts from NPCs, and items on the ground can
all be randomized. There are also many options for randomizing wild Pokémon, starters, Trainers' Pokémon, Abilities,
Types, etc.

<!-- Unlike most other Pokémon Archipelago implementations, the Pokémon GBA Combo Randomizer also allows you to travel between
regions for supported and enabled games, and shuffle items between them, for one large multi-region Pokémon adventure. -->

Check the [options page](../player-options) for a more comprehensive list of what can be changed.

## What items and locations get randomized?

The most interesting items that can be added to the item pool are Badges and Key Items, which most affect what locations
you can access. Key items like the Go-Goggles or Bicycles can also be randomized, as well as the many Potions, Revives,
TMs, and other items that you can find on the ground or be given from NPCs.

<!-- HMs, as well as Key Items that appear in multiple regions (Coin Case, rods, Itemfinder, etc), will only be placed once
in the item pool. -->

Some items have been moved around. See [here](/tutorial/Pokemon%20GBA%20Combo%20Randomizer/rom_changes/en) for a full list of changes.

## Where should I go next? / How do I go here?

**It is very heavily recommended that you play the original Pokémon games before playing
Pokémon Emerald Version (Flit's ver.), including any postgame content and events.**

It will generally be assumed that you've played the original games before; therefore, there's no need to answer this
question.

## What other changes are made to the game?

There are many quality of life improvements meant to speed up the game and improve the experience of playing a randomizer.
Here are some of the more important ones:

- Trade evolutions have been changed to item evolutions
- You can run or bike (almost) anywhere
- Many cutscenes are skipped, including catching tutorials

A full list of changes, both minor and major, can be found [here](/tutorial/Pokemon%20GBA%20Combo%20Randomizer/rom_changes/en).

## What does another world's item look like?

It looks the same as any other item. When picked up, you will see the item's name and its owner: `"BRENDAN found Player2's Item!"`

## When the player receives an item, what happens?

Currently, you will only receive items while in the overworld, not during battles.
Depending on your `Receive Item Messages` option, the received item will either be silently added to your bag,
or you will be shown a text box with fanfare, as if you picked up the item.

## Can I use save editing tools like PKHeX?

Almost certainly not, as the save structure has been modified. However, this hasn't been tested. As you already should,
back up your save file before using these tools.

## Support

If you have any questions or need technical support, and it isn't covered by this page, feel free to ask at the following
places:

- The [AP: Pokemon Emerald Version (Flit's ver.)](https://forum.flitpix.net/board/viewforum.php?f=44) subforum,
on my personal forums
- The [#Pokemon Emerald Version (Flit's ver.)](https://discord.com/channels/1345801058609270794/1482906015677681924) thread,
in the [Archipelago Unofficial Discord server](https://discord.gg/Nu4X9gmGDR)

To report bugs, you can let me know in the above places, or on GitHub Issues:
- [FlitPix/pokeemerald](https://github.com/FlitPix/pokeemerald/issues/new?template=bug_reports_emerald.yaml),
for *in-game* issues (crashes, visual quirks, etc)
- [FlitPix/ap-pokeemerald](https://github.com/FlitPix/ap-pokeemerald/issues/new?template=bug_reports_emerald.yaml),
for *APWorld* issues (logic, ROM patching, etc)

I am not in the official Archipelago Discord server and cannot provide support there.
