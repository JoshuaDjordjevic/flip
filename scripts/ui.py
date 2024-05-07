import typing
import pygame


def lerp(a:float, b:float, amount:float) -> float:
    return a + (b-a)*amount

def lerp_color(color1, color2, amount:float):
    return (
        max(min(int(lerp(color1[0], color2[0], amount)), 255), 0),
        max(min(int(lerp(color1[1], color2[1], amount)), 255), 0),
        max(min(int(lerp(color1[2], color2[2], amount)), 255), 0))


class Element(object):
    rect:pygame.Rect
    is_focused:bool = False

    font:pygame.Font

    def __init__(
            self,
            identifier:str,
            center:pygame.Vector2,
            size:pygame.Vector2,
            text:str="",
            font=None):
        self.identifier = identifier
        rect = pygame.Rect((0, 0), size)
        rect.center = center
        self.rect = rect
        self.text = text
        self.font = font
        self.font_color = (255, 255, 255)
    
    def get_color(self):
        return (50, 50, 75) if not self.is_focused else (130, 130, 155)

    def update(self, dt:float):
        pass
    
    def draw(self, surface:pygame.Surface):
        pygame.draw.rect(surface, (0,0,0), pygame.Rect(self.rect.left+5, self.rect.top+5, self.rect.width, self.rect.height), border_radius=10)
        pygame.draw.rect(surface, self.get_color(), self.rect, border_radius=10)
        if self.font is not None and self.text:
            font_surface = self.font.render(self.text, True, self.font_color)
            font_rect = font_surface.get_rect()
            font_rect.center = self.rect.center
            surface.blit(font_surface, font_rect)

class Screen(object):
    elements:typing.List[Element]
    def __init__(self):
        self.elements = []
        self.focused_element = None
    
    def set_focused_element(self, element:Element):
        self.focused_element = element
        self.focused_element.is_focused = True
    
    def clear_focused_element(self):
        if self.focused_element is None: return
        self.focused_element.is_focused = False
        self.focused_element = None
    
    def add_element(self, element:Element) -> Element:
        self.elements.append(element)
        return element
    
    def update(self, mouse_pos:pygame.Vector2):
        self.clear_focused_element()
        for element in self.elements:
            if element.rect.collidepoint(mouse_pos) and self.focused_element is None:
                self.set_focused_element(element)
    
    def draw(self, surface:pygame.Surface):
        for element in self.elements:
            element.draw(surface)