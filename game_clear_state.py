from pico2d import *
import play_state
import game_framework

image = None
running = True

def enter():
    global image
    image = load_image('resources\\game_clear.png')

def exit():
    global image
    del image

def draw():
    clear_canvas()
    image.draw(400, 300)
    update_canvas()

def handle_events():
    events = get_events()
    global running
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            if event.key == SDLK_r:
                game_framework.change_state(play_state)
                pass

def update():
    pass
