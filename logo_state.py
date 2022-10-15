from pico2d import *

logo_image = None
logo_time = 0.0
running = True

def enter():
    global logo_image
    logo_image = load_image('logo.png')

def exit():
    global logo_image
    del logo_image

def update():
    global logo_time
    global running
    if logo_time > 1.0:
        logo_time = 0
        running = False
    delay(0.01)
    logo_time += 0.01

def draw():
    clear_canvas()
    logo_image.draw(600, 350)
    update_canvas()

open_canvas(1200, 700)

while running:
    enter()
    update()
    draw()

close_canvas()


