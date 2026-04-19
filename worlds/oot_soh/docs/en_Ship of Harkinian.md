# Ship of Harkinian

## Where is the options page?

An option page will be available on the archipelago.gg website whenever this gets upstreamed. For now, use the .yaml file
to pick your settings.


## What is Ship of Harkinian (SoH)?

Ship of Harkinian is a fanmade PC port of The Legend of Zelda: Ocarina of Time. Due to it being a port, it has access to a ton
of enhancements like native widescreen support, higher framerates, built-in randomizer, built-in
trackers, and too many optional Quality of Life options to name them all here. 
If you're curious about the specifics, please [download SoH](https://www.shipofharkinian.com/) and take a look
through the ESC menu!


## I haven't played Ocarina of Time before.

We recommend to play Ocarina of Time in vanilla first! Preferably to 100% completion. 
Ship of Harkinian has presets for its enhancements, including one for new players. 
You'll have a much better time in the randomizer when you're familiar with the base game. 


## What does randomization do to this game?

Pretty much every item can be randomized: chests, major items, dungeon rewards, shop items, freestanding items, etc. 
There are additional options for the requirements for opening the Rainbow Bridge to Ganon's Castle and for receiving Ganon's Castle Boss Key.
As well as additional shuffle options like Boss Souls, requiring to be found before the respective boss can be fought. 
Most of these are optional and can be viewed within the player options page.


## What is the goal of Ship of Harkinian when randomized?

The standard goal is the same as the vanilla game: find whatever you need to reach and defeat Ganon.
The requirements of which will depend on chosen settings.

There's an alternative goal in Triforce Hunt, where the player has to find the required amount of pieces and will be automatically
warped to the end credits once finding the proper amount of pieces. If this is turned on, Ganon's Castle Boss Key will be granted
after loading back into the savefile if players would like to fight him afterwards.


## Can I play this in co-op with someone else on the same slot?

Yes! It will automatically sync items obtained between everyone that is connected to the same slot. Keep in mind that in-game
events like defeated dungeons, blown up boulders etc *aren't* synced between players. It doesn't matter if players are
connected at the same time. This also means you can make a new savefile yourself on a different machine and pick up where
you left off!


## Can I play this offline?

Yes, for the most part. When creating the savefile you will need to be connected to a slot. Afterwards, you can play offline. Once
you connect again, it will automatically sync all the items you've obtained up to that point. Just remember to save properly when playing
offline! If you're planning on playing a singleplayer Ship of Harkinian seed by yourself, look into generating a randomizer directly 
in Ship of Harkinian instead for a much easier time.


## What items from Ship of Harkinian can appear in another player's world?

Every item has a chance to appear in another player's world.


## How many checks are in Ship of Harkinian?

This depends heavily on the player's chosen settings. By default it's around 370 checks and it goes up to around 1600 checks
when shuffling everything.


## What do items from other worlds look like in Ship of Harkinian?

Ship of Harkinian uses custom models for Archipelago items. Progressive items will show up as coloured orbs with an arrow besides
them. Useful items are the same but without the arrow. Junk items will appear as a grayed out version of this. Items for
yourself will show up just like a regular randomizer, showing the model of whatever item it is.


## Is there a tracker pack?

There are a couple of options for trackers:
* The built in list tracker
* The [Poptracker Pack](https://github.com/Brian0255/ship-of-harkinian-ap-tracker/releases/latest)
* Univeral Tracker (yaml-less support)

## Is there an option for no logic?

Yes there is. There is a two step process to allow for generating a no logic seed.

First the `allow_true_no_logic` option needs to be set to `true` in the hosts `host.yaml`. By default it is disabled. Please only enable this if you understand that it will make all locations and regions in this world accessible from sphere 1 logically. It will majorly affect the entire multiworld.

```yaml
oot_soh_options:
  allow_true_no_logic: true
```

Second, in the players `.yaml` options file add this option somewhere to enable it for their world.

```yaml
Ship of Harkinian:
  true_no_logic: true
```

## Is "X" feature in SoH Archipelago?

If it is not in the `.yaml` file it likely has not been added to our Archipelago implementation yet. A short list of popular features that have yet to be added:

* Entrance Randomization
* Gossip Stone Hints
* Master Quest Dungeons

## Can I use my settings from the original OOT Archipelago?

SoH Archipelago and OOT Archipealgo are two separate implementations of the same game. This means that the two are not compatible and there are very likely differences between the twos logic. 

SoH Archipelago is focused on providing all (or as many as possible) of the features the standalone SoH randomizer has. If you have any feature requests or ideas that aren't already in SoH's standalone randomizer, we ask that you please request them to the [upstream SoH github repository](https://github.com/HarbourMasters/Shipwright). After they are added upstream, we can integrate them into Archipelago.