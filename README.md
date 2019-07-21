# DragNDrop-with-wxPython
####Latest####

--2019-07-21--
Major refinement of function.
Several superfluous classes have been removed and integrated into a single class called MatchPair. DDEngine module just serves as a basic base for launching a bare bones GUI and running main

MatchPair's functionality:
1)Allows dynamic insertion of matching pairs of buttons into a parent Frame
  *Achieved by creating instances of MatchPair that receive a parent Frame parameter
2)Facilitates a custom drag and drop cycle
  *uses a separate Frame to visually represent dragging without actually affecting the position of the buttons in the parent Frame
  *This achieves far smoother movement during dragging than trying to change the position of just the original button
  *However, this also requires handing events off from the original button object to events bound to the new Frame's child button
  *Concerns: there can be glitchy behavior when the Frame's focus is unexpectedly pulled away by the host OS's GUI. There are some WIP events handlers to assuage the worst of these issues
2)Completely encapsulated checking of matching pairs of draggable buttons and their drop targets
  *Checking for matches between the buttons being dragged and their target buttons is integrated into the drag and drop event cycle. Because all of this is instanced when a MatchPair object is created, the correct pairs of buttons will always only enter a matched state with each other, meaning checking for matches is achievable entirely within a single object without requiring cross-talk between non-matching pairs.
__UP NEXT__: The match checking cycle can be greatly simplified and refined. Should add parameters to explicitly pass sizers and other key members of parent Frame to MatchPair object, in order to adapt MatchPair to other parent GUI structures.

####Original README####
An attempt at creating a basic foundation for dragging and dropping dynamically created buttons with wxPython

The current implementation is pretty ugly. When dragged slowly, it looks acceptable, however when dragged too fast, the buttons will briefly leave a trail and/or disappear entirely until the mouse slows down again. I intend to try a different technique next, which will require large alteration to this code, including placing the buttons into their own Frames during dragging, in an effort to smooth the movement.

This repo is mainly for personal reference and intended to eventually be part of a larger project. The (very rough) ideas behind the code:

1) This is intended to become a matching game, where I must eventually check the dragged button to see if it matches against the drop button.
2) The button pairs must be created and added to the parent frame dynamically. I am tentatively anticipating this by making them their own seperate classes that inheret from wx.Button and have their event processing encapsulated.
3) The button pairs will eventually need to communicate their matching status somehow. Potential idea: A seperate class that creates the buttons in pairs as an object with attributes and methods to allow only that pair to communicate with each other, minimizing the need for  too much cross-talk between classes.
