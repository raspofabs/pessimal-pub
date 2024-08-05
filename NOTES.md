# Object oriented design vs serialisation

In the first place, the design of the components was simple. Each would take a
configuration dictionary and from it, build themselves. This works okay when
there are reasonable defaults.

Later, when adding the editor, I needed to have a way to inspect a component
for it's properties. Knowing that the reflection capabilities of Python were
very good, I thought about just looking up the current properties in the
component. 

Though reflection would work for editing any values, it would also allow for
editing values that were created dynamically. This might be a problem. Also,
there was no clear path to writing the edited values back out again. The
construction code knew how to read the values from the configuration
dictionary, but the raw object was useless for saving the values out again
because there was no mapping from the configuration data and the final object.

I needed a solution which provided loading, saving, and editing. I thought
about Python dataclasses, and looked at pydantic, but wanted to keep the
solution aligned with what was actually available to object-oriented developers
in other languages such as C++.

Objects have classes and most object-oriented language have, or can emulate,
static members. Keeping a list of fields by name (their type and a default)
made some sense to start with. This way, loading could be handled by a common
function, setting properties by name in Python and by some generated code in
other languages (macros in C++, not sure about the others yet).

Then I was hit by another problem. Including fields like this allows the
components to specify the names and types, but sometimes a type is not enough.
This is a debate point related to Hungarian notation. If the type is a simple
type such as an int, float, or string, it doesn't constrain what values are
valid and which are garbage. 

Moving to more complicated types, such as an angle, a file path, a date
structure, some combinations or values are invalid (720 degrees, C:\D?:\.txt,
and 33rd of February 1960). However, even though some values are invalid, they
still lack context or domain validity. Selecting a valid sprite file for a
reference would require the file be a valid image file.

What I feel I need is something with domain knowledge built-in. This means
adding validation specific to a field or at least a quite narrow type of field.
With such narrow valid options also comes a need for a specialised editor.
Choosing a date with a calendar is a lot easier. Choosing a file with types
already filtered work much better. Selecting from something constrained by the
context is very often much better when the editing tool is also aware of the
constraints. Consider the good password pickers that let you know, as you type,
whether you have fulfilled the password requirements.

So, I need to be able to, per field, specify not only the name and type, but
also the validity checks and also how editing the value works. Some editors can
be simple ints, floats, or strings, with simple, regular constraints such as
ranges or valid characters. These are more generic and so they can be from a
palette of basic editing tools.

It's the possibility of adding, just once, an uncommon editor that worries me.
The need for an editor for something specific ties the component to both the
final running application and the editor of that application's content.
This is a problem of coupling. I cannot see a good way to remove the coupling
here. I can move the coupling from one place to another, but it persists.

In one project, I forced components to use scripts to drive their editors. This
meant that the scripts could inspect the specifics and handle the complexity of
editing. This was a bit of a maintenance headache.

In another project, we put the editor code in the structures, making each
component responsible for loading, saving, editing and versioning all at the
same time.
This approach led to horrible IO performance as the runtime code relied on the
same complex structures the editor needed to define fields and their editing tools.

In yet another project, the editor was extended with new components each time
we needed to add anything non-trivial, and everything used version numbers and
had internal data-migration functions to carry data from older revisions to
newer. This worked well while everyone was on the same version, but fixing bugs
in old data with new tools would update the data so data-patches became
impossible over time.

Another project used text files for everything editable, but baked things down
to runtime assets for releases. Tools worked on the current interpretation of
those files and saved out similar structures. A little bit like how document
store databases work. Schemas were fluid. A bit like how using a config
dictionary works pretty well. The problem with this was, again, how the editing
was coupled to the fields in the components. Context required the fields knew
about how the editor worked.

So, I've not seen a good, decoupled, high performance solution with any OO
engine ever. And, to be clear, I've not see a good, decoupled, high performance
solution with any DOD engine ever either. So, perhaps this is a general problem
in programming, not one specific to object-oriented design.

What do I want? Something where, if I add a new component, it can have a field
of a type. That type should be configurable with some basic data, but should
itself drive the editor. I don't want components to know about editing
facilities. I want the type to know about how it should be edited. I want the
type to obey Liskov so that a simpler type can take its place without affecting
the behaviour of the application, but the more specific type can provide better
context for editing. This way, I would hope the runtime could be decoupled from
the editor's requirements.

So, what I plan to do is to create fields for basic types with basic editing. 
For each specialist area I shall add new field types that can extend the
semantics and provide more contextual editing options. Every field type should
be able to verify the values fall within acceptable ranges. 

To do this, the fields will need to be able to render editing tools themselves,
so they need to be editor aware. I dislike this coupling, but I feel it's
probably the most common place people put the complexity. It was certainly the
most common choice in all the engines I have worked on.
