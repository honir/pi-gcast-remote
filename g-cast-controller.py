#!/usr/bin/python

import sys
import signal
import buttonshim
import time
import pychromecast

#Enter the names of the Google Cast devices as in the Google App
chromecasts_name=['Living Room Speaker','Living Room TV']

#Values for the skip times when buttons C,D,E are pressed.
# You can enter these on the commandline  e.g. g-cast-controller.py -5 -30 30
#   (note values <5 are  not always obeyed by the Chromcast
skips=[-5,-15,+30]

# overwrite with values from the commandline
if len(sys.argv[1:])>0:
  # todo: some validation of the commandline values
  skips=[]
  skips.append(int(sys.argv[1]))
  skips.append(int(sys.argv[2]))
  skips.append(int(sys.argv[3]))

print("Discovering connected Chromecasts")
devices, browser = pychromecast.get_chromecasts()

selecteddevice=0
cc = []
for device in devices:
  print("Found:",device.cast_info.friendly_name,"at",device.cast_info.host)
  for chromecast_name in chromecasts_name:
    if device.cast_info.friendly_name == chromecast_name:
       cc.append(device)

print("""
Press the buttons to control first cast device, press and hold the buttons to control the second cast device.
Press Ctrl+C to exit.

A = Pause
B = Play
C = Skip """,skips[0],"""seconds
D = Skip""",skips[1],"""seconds
E = Skip """,skips[2],"""seconds

""")

while True:
  if devices==[]:
     print("No Device Online")
     time.sleep(5)
  elif not devices==[]:

    if len(cc) > 1:
      @buttonshim.on_press(None)
      def button_press(button, state):
        # assume any button press is a short press... (device #1)
        buttonshim.set_pixel(0x00, 0x00, 0x00)
        global selecteddevice
        selecteddevice=0

      @buttonshim.on_hold(None)
      def button_hold(button, hold_time=1):
        # ...but then long press on any button = device #2
        # flash the led green to indicate the button's been held long enough
        buttonshim.set_pixel(0x00, 0xFF, 0x00)
        print(buttonshim.NAMES[button],'long pressed')
        global selecteddevice
        selecteddevice=1
        print("Target device",cc[selecteddevice].cast_info.friendly_name)
        # turn off the led
        buttonshim.set_pixel(0x00, 0x00, 0x00)

    @buttonshim.on_release(buttonshim.BUTTON_A)
    def button_a(button, pressed):
       #print('A pressed')
       buttonshim.set_brightness(0.5)
       buttonshim.set_pixel(0xFF, 0x00, 0x00)
       cast=cc[selecteddevice]
       mc=cast.media_controller
       cast.wait()
       time.sleep(1)
       mc.pause()
       #buttonshim.set_pixel(0x00, 0x00, 0x00)
       buttonshim.set_brightness(0.2)    # must set brightness before colour (0.5 is std)
       buttonshim.set_pixel(0xFF, 0x00, 0x00)

    @buttonshim.on_release(buttonshim.BUTTON_B)
    def button_b(button, pressed):
       #print('B pressed')
       buttonshim.set_brightness(0.5)
       buttonshim.set_pixel(0x00, 0xFF, 0x00)
       cast=cc[selecteddevice]
       mc=cast.media_controller
       cast.wait()
       time.sleep(1)
       mc.play()
       buttonshim.set_pixel(0x00, 0x00, 0x00)

    @buttonshim.on_release(buttonshim.BUTTON_C)
    def button_c(button, pressed):
       #print('C pressed')
       buttonshim.set_brightness(0.5)
       buttonshim.set_pixel(0xFF, 0x80, 0xFF)
       cast=cc[selecteddevice]
       mc=cast.media_controller
       cast.wait()
       time.sleep(1)
       skip=skips[0]
       print('Time=',mc.status.current_time)
       print('Skip',skip)
       mc.seek(int(mc.status.current_time) + skip)
       buttonshim.set_pixel(0x00, 0x00, 0x00)

    @buttonshim.on_release(buttonshim.BUTTON_D)
    def button_d(button, pressed):
       #print('D pressed')
       buttonshim.set_brightness(0.5)
       buttonshim.set_pixel(0xFF, 0x80, 0xFF)
       cast=cc[selecteddevice]
       mc=cast.media_controller
       cast.wait()
       time.sleep(1)
       skip=skips[1]
       print('Time=',mc.status.current_time)
       print('Skip',skip)
       mc.seek(int(mc.status.current_time) + skip)
       buttonshim.set_pixel(0x00, 0x00, 0x00)

    @buttonshim.on_release(buttonshim.BUTTON_E)
    def button_e(button, pressed):
       #print('E pressed')
       buttonshim.set_brightness(0.5)
       buttonshim.set_pixel(0xFF, 0x80, 0xFF)
       cast=cc[selecteddevice]
       mc=cast.media_controller
       cast.wait()
       time.sleep(1)
       skip=skips[2]
       print('Time=',mc.status.current_time)
       print('Skip',skip)
       mc.seek(int(mc.status.current_time) + skip)
       buttonshim.set_pixel(0x00, 0x00, 0x00)

