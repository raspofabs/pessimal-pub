# Engine

- Get sprites working
    - sprite sheet config editor
- Add editing
    - Make it possible to add new entities to the world from the editor
    - Enable saving the world configuration
    - Make the world clone on run so we don't mess up configuration
    - Enable editor for roles / rules
    - Allow entities to have children
    - get the editor working with non-scene data
        - Game data such as acheivements and roles, 
        - game goals and 
        - config for difficulty or settings defaults
- Add audio samples and music systems
- Move to 3D?
    - poetry add assimp-py

# Game

- Make the AIs have resources and work tasks
    - make it so they plan their work and don't start treking to a resource
      centre two minutes before they need to turn back to go to bed.
    - get the other roles working
    - Give them a carry limit.
    - Make them use the roads if it makes sense (change speed and energy consumption?)
- Make the player and given them some tasks to do / achieve (such as hunt down
  better work strategies for the AI workers)
- Make the game have a day-night cycle
- Add some fauna
- Make a simple geometry backdrop system. Roads / paths are higher layer. Ground lower. Water is something else?
- Add some levels / transitions
- Add audio
    - sound effects for actions
    - ambient sound
    - music
- Create some procedural "artists" to generate a lot of content to put the
  engine under normal stress levels.
