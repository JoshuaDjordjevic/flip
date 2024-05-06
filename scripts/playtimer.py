from .frames import Frames


class Playtimer(object):
    def __init__(self):
        self.set_framerate(8)
        self.timer = 0.0
        self.playing = False
        self.loop = True
    
    def set_framerate(self, framerate:float):
        self.framerate = framerate
        self.frametime = 1 / framerate
    
    def play(self):
        self.playing = True
    
    def pause(self):
        self.playing = False

    def update(self, dt:float, frames:Frames):
        if self.playing:
            self.timer += dt
            if self.timer > self.frametime:
                self.timer = 0.0
                if not frames.goto_next():
                    if self.loop:
                        frames.set_index(0)
                    else:
                        frames.set_index(0)
                        self.playing = False