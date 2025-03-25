# Epoc-Bomb-Game-Thing
A game about strategy and placement!


Hello there! Welcome to this project called Epoc Bomb Game Thing(EBGT) A game about strategy and placement!
![Epoc Bomb Game Thing](https://github.com/user-attachments/assets/947a6c0d-1e4e-4546-8e1b-9c1884a65fc6)
## Overview
The goal of this game is to place blue squares called "bombs" in places that would be optimal that would hit the red squares called "targets". What hits the red squares you may ask? The orange squares called "shards" move out up, down, left, right, and diagonally in all directions with 8 coming out from each bomb where they have the ability to hit the targets.
In order to move on to the next round you must remove all the targets from the grid or you will reset back to the beginning of the level! as you pass through more round the more targets there are on the grid thus becoming harder to find out the exact location to hit all the targets so think strategically!
## Controls
There are basic movement controls to this game such as
- **W** (move forward)
- **A** (strafe left)
- **S** (move backwards)
- **D** (strafe right)

And other controls such as
- **Space** (place bomb)

There are also **development** keys in the game where later they would be removed
- **U** (tests shards)
- **K** (places 8 targets)
- **L** (removes all targets)

## Development
This project is currently in active development where after a good foundation for the game has been made I have decided to make a github page to share the code and help with debugging! So please if you have some time please try to break my game and tell me what it is and how to recreate it!

## Information
This is going to be a rapid fire information page so here it is:
- This game is made using Python and the library Pygame.
- This game is inspired by a mini game in Build A Boat for Treasure in Roblox
- This game is the continuation of Epoc Bomb Game Thing on Scratch
- This game is currently in active development

## Important Updates
This section is dedicated to listing major versions that have fundemental aspects of the game completely changed or added.

### Version 0.010
- Adds a round system
- Adds a title screen
- its version 10

### Version 0.016
- Complete overhaul of the title screen
- Complete overhaul of credits tab
- Added a nonfunctional tutorial button
- Overhaul of game design
- New fonts used
- new text used
- improved icon

### Version 0.017
- new secret in the title menu
- minor changes to the title menu

### Version 0.022
- Major backend update
- movement function created
- bombplacement function created
- line generation function made
- delta time introduced

### Version 23, Enlightened Depths Update

#### (Keynotes)
- Updated sprite textures
- Lasers & Diodes added
- Grid Holes added
- New version system

#### (Explanation)
- New sprite textures which enhance visibilty of sprites also they look cool
- Diode sprite added that can summon the Laser sprite
- Laser sprite, when touching the player forces all bombs of the player to drop
- Grid Holes are randomly placed throughout the map preventing player movement
- New version system where instead of the game being tracked by the format Version 0.001, it will now be tracked as Version 23 and the previous versions will apply to the rule, meaning the previous version (Version 0.022) is now treated as Version 22. Any version deemed a major update will be given a designated update name.

### Version 24

#### (Keynotes)
- Standard round system made
- Minor tweaks
- Minor optimizations

#### (Explanation)
- Intended rounds beyond 9 have been made
    - Grid Holes and Laser Diodes have introduction rounds
    - Hard coded rounds now go up to 36
- General code changes to enhance readability, and standardization
- Minor optimizations to improve performance
    - If a laser sprite is found to be out of bounds then it would force further sprites to not generate

#### (Goals)
- Improve performance when creating laser sprites
- Looking to see if any memory leaks have been found
- Possible sprite abstraction to allow for better time reading
- Replaced main theme due to copyright

### Version 25 and 26
Lol forgor to update on 25 but here it is combined with 26

#### (Keynotes)
- Anti aliasing test on title screen
- Clickable buttons on title screen (finally)
- Mouse input capability

#### (Explanation)
- Anti aliased polygons have been added ontop of existing polygon to get an anti aliased lines
- Buttons now turn to a lighter color when the mouse is hovering over it to enhance game accessability (should have been the first thing i done with the buttons but oh well)
- Mouse inputs are now imported so expect more button functionality

#### (Goals)
- More mouse utilization
- More anti aliased lines

### Version 27, Semi Official Release
Ok so I wanted to upload this project to Itch.io, so inorder to do it I would need to make a syncronized version for Mac OS and Windows and get rid of a few bugs so yes, Version 1 is the official release date, but Version 27 is the executable release date.

#### (Keynotes)
- Different sprites based on OS for compatibility
- Functionality to go back to homescreen after tutorial

#### (Explanation)
- A new variable, "os" has been added that checks for the current OS such as darwin for Mac OS and win32 for Windows.
- A new library, sys has been added to help with the checks of operating system.
- The tutorial will now bring you back to the main menu after completion so you don't need to close out the game.
- Start title code moved into the game loop to service the new functionality.

#### (Goals)
- Better tutorial transitions
- Possibly more transitions

### Version 28, Particle Update and Future Direction
Woah! Future direction! Will happen? You may ask. Well I have been thinking about this for a while, and I always want the best for this game which means that I will try my best to watch this game succeed. This vision, has inturn reached to a point where I can no longer support the game in it's current state as despite my numerous attempts to fixing issues that have been plaguing the game for some time such as actually playing the game, using the exe files, and code readibility it has become more of a hassle to maintain overtime thus action will need to be done. **This does NOT mean depreciation of the game!** Instead see this as more of a new beginning. I will work on a complete rewrite of the game on an actual game engine making sure that all of the problems are fixed and the rewrite state is on par with Version 22, so maybe within a week or 2 you will see this vision come to light and if possible I will make the game open source for everyone to see. But for now, without further a do, changelogs for Version 28 Particles Update.

#### (Keynotes)
- Added Laser and Bomb Particles

#### (Explanation)
- New class called particles added
- laser diodes now give off a particle
- bombs when exploded give off a particle

#### (Goals)
- No **g**oals here t**o**night, but only hopes an**d** dreams, **o**nly **t**ime is needed, but it will make a difference.
