# Setup guide for Pokémon Emerald Version (Flit's ver.)

## Important note

As we are using BizHawk, this guide is only applicable to Windows and Linux systems.

## Required software

- The latest version of [BizHawk](<https://tasvideos.org/BizHawk/ReleaseHistory>)
    - Alternatively, you can use the latest version of [mGBA](https://mgba.io/downloads.html),
    AND the [mGBA connector script](https://github.com/Zunawe/bhc-substitutes/tree/main/mgba).
- The latest version of [upstream Archipelago](<https://github.com/ArchipelagoMW/Archipelago/releases/latest>) (or any desired fork),
AND the latest version of the [Pokémon Emerald Version (Flit's ver.) APWorld](<https://github.com/FlitPix/ap-pokeemerald/releases/latest>)
    - Some Archipelago forks may already include the APWorld. In this case, you don't need to download it.
- Your legally-obtained English Pokémon Emerald Version ROM for Nintendo Game Boy Advance.
This cannot be provided by Flit or the Archipelago community.
    - MD5 hash: `605b89b67018abcea91e693a4dd25be3`

## Installing the APWorld

If you're playing on a fork that already includes this APWorld, you should skip this section.

Follow the [instructions](/tutorial/Archipelago/setup_en#playing-with-custom-worlds) to install the APWorld.
(If you're not viewing this on an Archipelago webhost, see [here](<https://archipelago.gg/tutorial/Archipelago/setup_en#playing-with-custom-worlds>).)

If you previously placed it in the `lib/worlds` subdirectory, delete it from there.

## Generating a game

Follow the [instructions](/tutorial/Archipelago/setup_en#generating-a-game) to generate a game locally on your device.
(If you're not viewing this on an Archipelago webhost, see [here](<https://archipelago.gg/tutorial/Archipelago/setup_en#generating-a-game>).)

If you're playing on a fork that already includes this APWorld, different instructions may apply.
Please refer to that fork's documentation.

## Obtaining your patch file

If the multiworld is being hosted on the website, your patch file will be located on the room page. Click on the
`Download Patch File...` link to download it.

If the link isn't there, or if the multiworld isn't being hosted on the website, the host can find the patch file in the
output .zip file.

Ensure that the patch file ends with the `.apemeraldflit` extension.

## Installing and configuring your preferred emulator

### BizHawk

Follow [TASVideos's instructions](https://tasvideos.org/BizHawk) to install and configure BizHawk.
This is not in the scope of this setup guide.

### mGBA

If you wish to instead use [mGBA](https://mgba.io/downloads.html),
you can use the [mGBA connector script](https://github.com/Zunawe/bhc-substitutes/tree/main/mgba).

Using the mGBA connector script is not in the scope of this setup guide. To use it, please follow its instructions.

Note that some Archipelago forks may already include the connector script.

## Patching the ROM and automatically connecting to the multiworld

These steps will only fully work when using BizHawk. If you want to use mGBA, you'll need to follow the
"Manually connecting to the multiworld" section below.

1. In the Launcher, search for `Open Patch` and click its Open button.
2. Select the `.apemeraldflit` patch file.
3. If prompted, select your Pokémon Emerald Version ROM file.
4. If prompted, select the path to `EmuHawk.exe`.

BizHawk will automatically open with your patched ROM and with the connector script loaded.
The BizHawk Client should also open and automatically connect you to the multiworld.

If this is the case, congratulations! You can now select "NEW GAME" from the main menu and start playing. Have fun!

### Help! BizHawk didn't open / gives a ROM error!

You may have selected the wrong ROM and/or EmuHawk files.
Archipelago will not allow you to choose again without some text editing.

1. Go to your Archipelago folder, look for `host.yaml`, and open it in a text editor.
2. Use Ctrl-F (or similar) to search for `bizhawkclient_options`.
3. Delete the line with `bizhawkclient_options`, as well as the next six lines.
This should include `emuhawk_path` and `rom_start`.
4. Use Ctrl-F (or similar) to search for `pokemon_emerald_settings`.
5. Underneath `pokemon_emerald_settings`, you will find `rom_file`. Delete this line.
6. Make sure you save the file.

Now, when using `Open Patch`, you should be prompted for your ROM and EmuHawk files again. If this didn't work,
feel free to [ask for help](#i-need-help).

## Manually connecting to the multiworld

If the above steps didn't fully work, or you are using mGBA, follow the steps below.

1. If your emulator didn't automatically open with your patched ROM in the Patching the ROM section, open it now.
2. If you haven't already done so, open the **BizHawk Client**, by doing one of the following:
    - Searching for "BizHawk Client" in the Launcher, and clicking its Open button
    - Opening `ArchipelagoBizHawkClient.exe` / `ArchipelagoBizHawkClient` (or equivalent name on forks)
    from the Archipelago folder
3. This step depends on the emulator you're using.
    - In **BizHawk**, *only if this did not happen automatically in the Patching the ROM section*, go to Tools > Lua Console.
    Then, go to Script > Open Script, and look for this file: `<Archipelago folder>/data/lua/connector_bizhawk_generic.lua`
    - To use **mGBA**, follow the mGBA connector script's included instructions.
4. In BizHawk Client, ensure the message `Running handler for Pokemon Emerald Version - Flit's ver.` appears.
    - If it does not appear, verify you opened the *patched ROM*. You know the ROM is patched if the "OPTIONS" menu
    has been overhauled.
    - If an error message appears instead, heed its advice.
5. In BizHawk Client, enter the connection info using the connect textbox at the top of the window, then click Connect.
6. When prompted, enter your slot name. If prompted, enter the room password.

Congratulations! You have connected to the multiworld. You can now select "NEW GAME" from the main menu and start playing.
Have fun!

## Optional: Universal Tracker

Universal Tracker lists what checks are in logic at any given moment, making it great for checking
what you might have missed.

Follow the [instructions](<https://github.com/FarisTheAncient/Archipelago/blob/tracker/worlds/tracker/docs/setup.md>) to
install and use Universal Tracker.

While Pokémon Emerald Version (Flit's ver.) doesn't support Universal Tracker yet without having your game YAML file
in the Players folder, this is planned for the future.

## I need help!



If that doesn't help, you can get help in the following places:

- GitHub Issues:
    - [FlitPix/pokeemerald](https://github.com/FlitPix/pokeemerald/issues/new?template=bug_reports_emerald.yaml),
    for *in-game* issues (crashes, visual quirks, etc)
    - [FlitPix/ap-pokeemerald](https://github.com/FlitPix/ap-pokeemerald/issues/new?template=bug_reports_emerald.yaml),
    for *APWorld* issues (logic, ROM patching, etc)
- The [AP: Pokemon Emerald Version (Flit's ver.)](https://forum.flitpix.net/board/viewforum.php?f=44) subforum,
on my personal forums
- The [#Pokemon Emerald Version (Flit's ver.)](https://discord.com/channels/1345801058609270794/1482906015677681924) thread,
in the [Archipelago Unofficial Discord server](https://discord.gg/Nu4X9gmGDR)
