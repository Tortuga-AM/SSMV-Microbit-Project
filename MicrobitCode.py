# Python code
#
from microbit import *

active = False
buttons_held = False
start_time = 0
SERVO_PIN = AnalogPin.P0
SERVO_ANGLE = 180
SERVO_IDLE = 90
THRESHOLD = 160
WAKE_TEXT = "WakeInator3000"
strip = neopixel.create(DigitalPin.P2, 12, NeoPixelMode.RGB)

def startup():
  strip.show_rainbow(1, 360)
  basic.show_icon(IconNames.Happy)
  basic.pause(1000)
  basic.show_string(WAKE_TEXT)
  basic.clear_screen()
  strip.clear()
  
def disarmed():
  music.stop_melody(MelodyStopOptions.ALL)
  startup()
  
def button_handler():
  global active, buttons_held
  if buttons_held:
    if (input.running_time() - start_time) >= 10000:
      active = False
      disarmed()
    else:
      basic.show_number(Math.floor((input.running_time() - start_time) / 1000))
def countdown():
    start_time = input.running_time()
    while Math.floor((input.running_time() - start_time) / 1000) < 30:
        basic.show_number(Math.floor((input.running_time() - start_time) / 1000))
        if input.button_is_pressed(Button.AB):
            return 1
    return 0
    
def on_forever():
  global active, buttons_held, start_time
  if (input.sound_level() >= THRESHOLD) and (not active):
    if countdown() == 0:
        active = True
        music.start_melody(music.get_melody(Melodies.RINGTONE), MelodyOptions.FOREVER_IN_BACKGROUND)
    else:
        basic.clear_screen()
        strip.clear()
        strip.show()
  if input.button_is_pressed(Button.AB):
    if not buttons_held:
      start_time = input.running_time()
    buttons_held = True
  else:
    buttons_held = False
  
  if active:
    if buttons_held:
        button_handler()
    pins.servo_write_pin(SERVO_PIN, SERVO_ANGLE)
    strip.set_brightness(255)
    strip.show_color(NeoPixelColors.WHITE)
    strip.show()
  else:
    pins.servo_write_pin(SERVO_PIN, SERVO_IDLE)
    strip.clear()
    strip.show()
  
startup()
basic.forever(on_forever)
