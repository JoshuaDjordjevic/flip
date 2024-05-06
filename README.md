- [Flip](#flip)
- [Usage](#usage)
  - [Interface Controls](#interface-controls)

# Flip
A simple flipbook-style animation tool, written in Python using Pygame

# Usage
Simply run app.py, and draw away!

## Interface Controls
Currently the software is insanely rudimentory. There's basically no UI.
The keybinds are:
* N: Insert new frame
* C: Copy current frame
* DEL: Delete current frame
* LEFT: Goto previous frame
* RIGHT: Goto next frame
* S: Save current frame as `frame.png` (Used for testing)
* H: Hide/unhide onion skin
* SPACE: Play/pause animation

At the moment the animation is locked to play at 8 frames per second,
but when a UI comes along this will be customizable.