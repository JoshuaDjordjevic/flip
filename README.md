- [Flip](#flip)
- [Usage](#usage)
  - [Interface Controls](#interface-controls)

# Flip
A simple flipbook-style animation tool, written in Python using Pygame

# Usage
Simply run app.py, and draw your animation!

## Interface Controls
We've got a ui now! But here are the existing keyboard shortcuts if you'd like to use
those instead, as it allows for a faster workflow:
* N: Insert new frame
* C: Copy current frame
* DEL: Delete current frame
* LEFT: Goto previous frame
* RIGHT: Goto next frame
* S: Save current frame as `frame.png` (Used for testing)
* H: Hide/unhide onion skin
* SPACE: Play/pause animation

At the moment the animation is locked to play at 8 frames per second. Hang tight while I make that customizable.