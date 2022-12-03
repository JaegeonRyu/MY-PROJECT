from pico2d import *
import play_state
import game_framework

logo_image = None

def enter():
    global logo_image
    logo_image = load_image('resources\\game_start.png')

def exit():
    global logo_image
    del logo_image

def draw():
    clear_canvas()
    logo_image.draw(400, 300)
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            if event.key == SDLK_SPACE:
                game_framework.change_state(play_state)

def update():
    pass



