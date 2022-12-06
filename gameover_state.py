from pico2d import *
import play_state
import game_framework
import logo_state

over_image = None
running = True

def enter():
    global over_image
    over_image = load_image('resources\\game_over.png')

def exit():
    global over_image
    del over_image

def draw():
    clear_canvas()
    over_image.draw(400, 300)
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
                game_framework.change_state(logo_state)
                pass

def update():
    pass


