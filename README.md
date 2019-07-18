# DragNDrop-with-wxPython
An attempt at creating a basic foundation for dragging and dropping dynamically created buttons with wxPython

The current implementation is pretty ugly. When dragged slowly, it looks acceptable, however when dragged too fast, the buttons will briefly leave a trail and/or disappear entirely until the mouse slows down again. I intend to try a different technique next, which will require large alteration to this code, including placing the buttons into their own Frames during dragging, in an effort to smooth the movement.

This repo is mainly for personal reference and intended to eventually be part of a larger project. The (very rough) ideas behind the code:

1) This is intended to become a matching game, where I must eventually check the dragged button to see if it matches against the drop button.
2) The button pairs must be created and added to the parent frame dynamically. I am tentatively anticipating this by making them their own seperate classes that inheret from wx.Button and have their event processing encapsulated.
3) The button pairs will eventually need to communicate their matching status somehow. Potential idea: A seperate class that creates the buttons in pairs as an object with attributes and methods to allow only that pair to communicate with each other, minimizing the need for  too much cross-talk between classes.
