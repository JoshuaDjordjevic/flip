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
    shadow_rect:pygame.Rect
    
    can_hover:bool = False

    is_hovered:bool = False
    is_enabled:bool = True
    is_clickable:bool = False

    font:pygame.Font

    def __init__(
            self,
            identifier:str,
            center:pygame.Vector2,
            size:pygame.Vector2,
            text:str="",
            font=None):
        self.identifier = identifier
        _rect = pygame.Rect((0, 0), size)
        _rect.center = center
        self.set_rect(_rect)
        self.text = text
        self.font = font
        self.font_color = (255, 255, 255)
    
    def set_rect(self, rect:pygame.Rect):
        self.rect = rect
        self.shadow_rect = pygame.Rect(
            self.rect.left+5,
            self.rect.top+5,
            self.rect.width,
            self.rect.height)
    
    def get_color(self):
        return (50, 50, 75) if not self.is_hovered else (130, 130, 155)
    
    def draw(self, surface:pygame.Surface):
        pygame.draw.rect(surface, (0,0,0), self.shadow_rect, border_radius=10)
        pygame.draw.rect(surface, self.get_color(), self.rect, border_radius=10)
        if self.font is not None and self.text:
            font_surface = self.font.render(self.text, True, self.font_color)
            font_rect = font_surface.get_rect()
            font_rect.center = self.rect.center
            surface.blit(font_surface, font_rect)

    def update(self, dt:float):
        pass
    
    def process_event(self, event:pygame.Event):
        pass

class Button(Element):
    is_clickable:True
    can_hover:True
    on_click:typing.Callable[[pygame.Event], None]

    def __init__(self,
                 identifier:str,
                 center:pygame.Vector2,
                 size:pygame.Vector2,
                 text:str = "",
                 font=None,
                 on_click:typing.Callable[[pygame.Event], None]=None):
        super().__init__(identifier, center, size, text, font)
        self.is_clickable = True
        self.can_hover = True
        self.on_click = on_click
    
    def process_event(self, event: pygame.Event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.on_click is not None:
                self.on_click(event)

class Screen(object):
    elements:typing.List[Element]
    def __init__(self):
        self.elements = []
        self.hovered_element = None
        self.events = []
    
    def process_event(self, event:pygame.Event):
        if self.hovered_element is not None:
            self.hovered_element.process_event(event)
    
    def set_hovered_element(self, element:Element):
        self.hovered_element = element
        self.hovered_element.is_hovered = True
    
    def clear_hovered_element(self):
        if self.hovered_element is None: return
        self.hovered_element.is_hovered = False
        self.hovered_element = None
    
    def add_element(self, element:Element) -> Element:
        self.elements.append(element)
        return element

    def add_and_pack(self,
                     elements:typing.List[Element],
                     anchor:pygame.Vector2,
                     direction:typing.Literal[0, 1],
                     alignment:typing.Literal[-1, 0, 1],
                     spacing:float) -> None:
        direction_vector = pygame.Vector2(1, 0) if direction==0 else pygame.Vector2(0, 1)

        # Calculate total width or height
        total_size = 0

        size_function: typing.Callable[[pygame.Rect], float]
        if direction == 0: size_function = lambda r: r.width
        else: size_function = lambda r: r.height

        for element in elements:
            size = size_function(element.rect)
            total_size += size
        total_size += spacing*(len(elements)-1)

        total_size_vector = direction_vector*total_size

        # Lay out elements side by side or top to bottom
        start_at = anchor.copy()
        if alignment == 1:
            start_at -= total_size_vector
        elif alignment == 0:
            start_at -= total_size_vector*0.5
        
        offset = 0
        for element in elements:
            new_rect = element.rect.copy()
            if direction == 0:
                new_rect.centery = anchor.y
                new_rect.left = (start_at + direction_vector*offset).x
            else:
                new_rect.centerx = anchor.x
                new_rect.top = (start_at + direction_vector*offset).y
            element.set_rect(new_rect)
            offset += size_function(element.rect)
            offset += spacing
            self.add_element(element)
    
    def update(self, mouse_pos:pygame.Vector2):
        self.clear_hovered_element()
        for element in self.elements:
            if not element.is_enabled:
                continue
            if element.can_hover:
                if element.rect.collidepoint(mouse_pos) and self.hovered_element is None:
                    self.set_hovered_element(element)
    
    def draw(self, surface:pygame.Surface):
        for element in self.elements:
            element.draw(surface)