# ROM Changes

## System

- An error screen was added on boot, for when the incorrect save type configuration is set (usually an emulator setting or bad flashcart). (In vanilla, this is just a white screen.)
- RNG seeding has been fixed, and now works like it did in Ruby and Sapphire Versions.
- The Bag's Items pocket can now hold 90 unique items, rather than 30.
- Searching for Pokemon in the Pokedex will now return Pokemon marked as seen, as well as owned.
- You can run and cycle in many more places, notably indoors.
    - You can now run on the Fortree and Pacifidlog bridges, though note that there may be minor graphical issues as a result.
    - You can now run in very tall grass.
    - You still cannot cycle on the Fortree or Pacifidlog bridges, or in very tall grass.
- The Pokémon Center Nurse will immediately heal your Pokémon when spoken to, and you will automatically turn away when they're done.
- When a Repel runs out, and you have another (regardless of tier), you will be asked if you want to use another. If you have the same tier of Repel on hand as what was used last, it will be used; otherwise, the lowest tier on hand will be used.
- Evolutions have been changed to be possible in a singleplayer setting: **(each method is tentative)**
    - Kadabra evolves into Alakazam when a Link Cable is used on it.
    - Machoke evolves into Machamp when a Link Cable is used on it.
    - Graveler evolves into Golem when a Link Cable is used on it.
    - Haunter evolves into Gengar when a Link Cable is used on it.
    - Poliwhirl evolves into Politoed when a King's Rock is used on it.
    - Slowpoke evolves into Slowking when a King's Rock is used on it.
    - Onix evolves into Steelix when a Metal Coat is used on it.
    - Scyther evolves into Scizor when a Metal Coat is used on it.
    - Seadra evolves into Kingdra when a Dragon Scale is used on it.
    - Porygon evolves into Porygon2 when an Up-Grade is used on it.
    - Clamperl evolves into Huntail when a DeepSeaTooth is used on it.
    - Clamperl evolves into Gorebyss when a DeepSeaScale is used on it.
    - Feebas evolves into Milotic when a Blue Scarf is used on it.
- HM moves can be forgotten without having to use the Move Deleter.
- Pokémon always obey you, regardless of badge count.
- Battles are faster in general:
    - The sliding animation for Trainers and wild Pokémon at the start of a battle runs at double speed.
    - Pauses between actions are shortened.
    - The animation for using held items is sped up.
- During a Single Battle, the Pokémon menu will display the opponent's current Pokémon, or the Pokémon that's about to be sent out if playing with the Switch Battle Style.
- When playing with the Switch Battle Style, the prompt to switch Pokémon has been shortened so you can still see what Pokémon your opponent is about to send out while on the YES/NO box.
- You can run from Trainer Battles, but doing so will cause you to white out.
- The [formula from FireRed and LeafGreen Versions](https://bulbapedia.bulbagarden.net/wiki/Black_out#Formula_for_money_lost) is used for money lost when whiting out.

## Progression

- Many introductory and tutorial scenes have been removed or altered:
    - You now start in your bedroom in Littleroot Town, with all cutscenes up to and including receiving the Running Shoes removed.
        - The RTC is set during the intro speech.
        - Your starter Pokémon is decided during the intro speech.
        <!-- - If the Pokedex is shuffled, Prof. Birch will give it to you when spoken to. -->
        - Brendan/May can still be fought on Route 103. After defeating them<!-- and obtaining the Pokedex-->, you can return to Birch's Lab and speak to them to receive one Poké Ball.
    - The cutscenes and catch tutorial that start when first visiting Petalburg Gym have been removed.
    - The Match Call tutorial after leaving Devon Corp has been removed.
    - Triggers in Rustboro, Route 104, and Route 116 West have been removed. This means you must talk to the Devon employee in Rustboro to deliver the Devon Goods.
- The Oldale Poké Mart sells Poké Balls at the start of the game.
- Mr. Briney never disappears or stops letting you use his ferry.
    - **Tentatively,** he is available from the start.
- In Granite Cave, Steven cuts the conversation short if you don't have the Letter.
- Route 9's Seashore House only rewards you with one Soda Pop instead of six.
- Dock checks whether you have the Devon Goods before asking you to deliver them (and therefore opening the museum).
- The woman in Slateport who gives you the Soothe Bell will do so regardless of your Pokémon's friendship.
<!-- - The chairman of the Pokémon Fan Club will give you all five scarves regardless of your Pokémon's contest stats. **(tentative)** -->
- Rydel gives you both Bikes at once. This also means you can no longer swap them at the shop.
- Mirage Tower always has the Claw Fossil. Desert Underpass always has the Root Fossil.
- The Safari Zone's step limit was increased to 50,000.
- A Team Aqua grunt on the summit of Mt. Pyre was moved to ensure a hidden Rare Candy is always available.
- A ledge on Route 123 was removed to allow every item to be collected without backtracking.
- Shoal Cave changes tide every time you enter, and is no longer tied to the RTC.
- The man in Pacifidlog who gives you the TMs for Frustration and Return will give you both at the same time, won't check friendship first, and won't care what time it is.
- The S.S. Tidal is always available once you have the S.S. Ticket.
- All time-based Berry gifts are changed to a one-time gift of a specific Berry.
- When trading the Scanner with Captain Stern, you will receive both the DeepSeaTooth and DeepSeaScale.
- When Kyogre is released, Sootopolis and Sky Pillar will be advanced to after Rayquaza has been awakened, skipping the Wallace and Rayquaza fetch quest.
- When entering the Hall of Fame, you will receive all of the event tickets.

### Battle Frontier

- Scott always gives 4 BP when spoken to in his house, regardless of how many times he was interacted with throughout the game.

## Challenge Mode

Challenge Mode is available as a game YAML option, disabled by default. Those very familiar with Gen 3 and looking for an extra challenge may be interested in it. Here is what it does (more effects will be added in the future):

- Forcibly changes the following options, and locks them in the OPTIONS menu if applicable:
    - Battle Style is set to Set
    - Blind Trainers is disabled
    - Always Catch is disabled
    - Always Escape is disabled
    - Always Reel is disabled
    - EXP. Multiplier is set to 1x
    - Reusable TMs is disabled
- Disables [badge boosts](https://bulbapedia.bulbagarden.net/wiki/Badge#Stat_boost).
- Improves enemy Trainer AI:
    - When switching in, they will use the Pokémon that will deal the *most* damage, rather than the *least* damage.
