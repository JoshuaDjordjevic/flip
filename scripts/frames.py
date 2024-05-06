import typing
import pygame


class Frames:
    frame_rect: pygame.Rect
    index: int
    frames: typing.List[pygame.Surface]

    def __init__(self, frame_rect:pygame.Rect):
        self.frame_rect = frame_rect
        self.index = 0
        self.frames = []

        self.background_layers = []
        self.background_layer_count = 2

        self.draw_onion_skin = True
    
    def __create_surface(self) -> pygame.Surface:
        surface = pygame.Surface(self.frame_rect.size)
        surface.fill((255, 255, 255))
        surface.set_colorkey((255, 255, 255))
        return surface

    def __refresh_background_layer(self):
        self.background_layers.clear()
        for i in range(self.background_layer_count):
            surface = self.get(self.index-i-1)
            if surface is None:
                break
            alpha_level = 80 // (i+1)
            surface = surface.copy()
            surface.set_alpha(alpha_level)
            self.background_layers.append(surface)
    
    def new_at(self, index:int=-1):
        self.frames.insert(index, self.__create_surface())
        self.__refresh_background_layer()
    
    def new(self):
        self.new_at(self.index+1)
        self.index += 1
        self.__refresh_background_layer()
    
    def copy(self):
        """Copy the current frame.
        """
        current = self.current()
        self.frames.insert(self.index, current.copy())
        self.index += 1
        self.__refresh_background_layer()
    
    def delete(self):
        self.frames.pop(self.index)
        self.index -= 1
        if self.index == -1:
            self.index = 0
            if len(self.frames) == 0:
                self.new_at(0)
        self.__refresh_background_layer()
    
    def get(self, index:int) -> typing.Union[pygame.Surface, None]:
        if index < 0 or index >= len(self.frames):
            return None
        return self.frames[index]
    
    def current(self) -> pygame.Surface:
        return self.frames[self.index]
    
    def goto_previous(self):
        if self.index > 0:
            self.set_index(self.index-1)
            return True
        return False
    
    def goto_next(self):
        if self.index < len(self.frames)-1:
            self.set_index(self.index+1)
            return True
        return False
    
    def set_index(self, index:int) -> None:
        self.index = index
        self.__refresh_background_layer()

    def draw(self, surface:pygame.Surface):
        pygame.draw.rect(surface, (255, 255, 255), self.frame_rect)
        if self.draw_onion_skin:
            for layer in self.background_layers:
                surface.blit(layer, self.frame_rect)
        current_frame = self.get(self.index)
        surface.blit(current_frame, self.frame_rect)