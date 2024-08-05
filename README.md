# The migration project

Pessimal is the base example. It's a Python game developed as a basis for
showing how to migrate from an object-oriented design to a data-oriented
design. The name was chosen to remind people that this is not how you should
write code, but how it often is.

The overall plan is to make this game / engine combo in one languge, then
others, then show how to migrate in each. Python to start with, then C++, then
others. I would like to rewrite the project in Rust, C#, and Java. However, I'm
not sure about the value in them as my own level of competence in each of
language will likely lead to poor examples.

Once the starting points are available, I plan to apply my migration strategy
to each as a sequence of tagged steps so people can see the changes and the
impact.

# Notes

During the creation of the base project, I had a revelation about OO
design. In case I have more, I'm going to keep notes in [NOTES.md] in case I
have other thoughts inspired by the process of creation.

# Todo list

- Finish making the base game
- get the editor working with non-scene data too (e.g., game data such as
  acheivements and roles, game goals and config for difficulty or settings
  defaults)
- get the other roles working
- make the player and given them some tasks to do / achieve (such as hunt down
  better work strategies for the AI workers)
- add some fauna
- add some levels / transitions
- add audio
- Create some procedural "artists" to generate a lot of content to put the
  engine under normal stress levels.
- Review the state and decide what is left to do.

- Rewrite in other languages.
- Ensure the games / engines have good profiling tools available to give some
  good quality baselines for the costs of each area of the runtime.
- Perform the migration.
