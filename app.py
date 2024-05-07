import typing
import pygame
from pygame.locals import *

from scripts.frames import Frames
from scripts.playtimer import Playtimer
from scripts import ui

pygame.init()

display_size = pygame.Vector2(1024, 768)
display_size_half = display_size * 0.5
display = pygame.display.set_mode(display_size)
pygame.display.set_caption("Flip Animation")

font = pygame.font.Font("./resources/8514oem.fon", 20)

frame_size = pygame.Vector2(820, 614)
frame_rect = pygame.Rect((0, 0), frame_size)
frame_rect.center = display_size_half

# Create a Frames instance and create one frame
frames = Frames(frame_rect)
frames.new_at(0)

# Create a ui screen
screen = ui.Screen()
screen.add_element(ui.Button("play", (display_size_half.x, 38), (120, 40), text="Play/Pause", font=font))
screen.add_element(ui.Button("frame_new", (display_size_half.x+100*-2, display_size.y-38), (90, 40), text="New", font=font))
screen.add_element(ui.Button("frame_copy", (display_size_half.x+100*-1, display_size.y-38), (90, 40), text="Copy", font=font))
screen.add_element(ui.Button("frame_delete", (display_size_half.x+100*0, display_size.y-38), (90, 40), text="Delete", font=font))
screen.add_element(ui.Button("frame_prev", (display_size_half.x+100*1, display_size.y-38), (90, 40), text="Previous", font=font))
screen.add_element(ui.Button("frame_next", (display_size_half.x+100*2, display_size.y-38), (90, 40), text="Next", font=font))

playtimer = Playtimer()

mouse_position_last = pygame.Vector2(pygame.mouse.get_pos())

clock = pygame.time.Clock()
running = True
while running:
    dt = clock.tick(61)/1000

    for event in pygame.event.get():
        screen.process_event(event)
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                frames.new()
            elif event.key == pygame.K_c:
                frames.copy()
            elif event.key == pygame.K_DELETE:
                frames.delete()
            elif event.key == pygame.K_LEFT:
                frames.goto_previous()
            elif event.key == pygame.K_RIGHT:
                frames.goto_next()
            elif event.key == pygame.K_s:
                pygame.image.save(frames.current(), "frame.png")
            elif event.key == pygame.K_h:
                frames.draw_onion_skin = not frames.draw_onion_skin

            elif event.key == pygame.K_SPACE:
                if playtimer.playing:
                    playtimer.pause()
                else:
                    playtimer.play()
        
        if event.type == pygame.MOUSEBUTTONUP:
            hovered_element = screen.hovered_element
            if hovered_element is not None:

                func = {
                    "frame_new": frames.new,
                    "frame_copy": frames.copy,
                    "frame_delete": frames.delete,
                    "frame_prev": frames.goto_previous,
                    "frame_next": frames.goto_next
                }.get(hovered_element.identifier)

                if func is not None:
                    func()
                elif hovered_element.identifier == "play":
                    if playtimer.playing:
                        playtimer.pause()
                    else:
                        playtimer.play()
    
    mouse_buttons_down = pygame.mouse.get_pressed()

    mouse_position = pygame.Vector2(pygame.mouse.get_pos())
    mouse_in_frame = frame_rect.collidepoint(*mouse_position)
    
    # The mouse is inside the drawing frame
    if mouse_in_frame:
        mouse_position_frame = mouse_position - frame_rect.topleft
        mouse_position_last_frame = mouse_position_last - frame_rect.topleft
        if mouse_buttons_down[0]:
            # Draw line from last to current positions
            pygame.draw.line(frames.current(), (0,0,0), mouse_position_last_frame, mouse_position_frame, 5)
    
    mouse_position_last = mouse_position

    playtimer.update(dt, frames)
    screen.update(mouse_position)
    
    display.fill((25, 25, 35))
    frames.draw(display)

    lines = [
        f"FRAME {frames.index+1} / {len(frames.frames)}"
    ]
    for i, line in enumerate(lines):
        y = i*20+10
        text_surface = font.render(line, True, (255, 255, 255))
        display.blit(text_surface, (10, y))
    
    screen.draw(display)

    pygame.display.flip()

pygame.quit()