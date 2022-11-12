import pico2d
import logo_state
import play_state
import game_framework
WinW = 800
WinH = 600

pico2d.open_canvas(WinW, WinH)
game_framework.run(play_state)
pico2d.close_canvas()

####
# start_state = logo_state
#
# start_state.enter()
# while start_state.running:
#     start_state.handle_events()
#     start_state.draw()
# start_state.exit()
#
# start_state = play_state
#
# start_state.enter()
# while start_state.running:
#     start_state.handle_events()
#     start_state.update()
#     start_state.draw()
# start_state.exit()
#
# pico2d.close_canvas()
