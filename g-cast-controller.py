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

A = Pause/Play
B = Mute/Unmute
C = Skip """,skips[0],"""seconds
D = Skip""",skips[1],"""seconds
E = Skip """,skips[2],"""seconds

""")

while True:
  if devices==[]:
     print("No Device Online")
     time.sleep(5)
  elif not devices==[]:

    def button_led(buttonshim, cast):
      # if pause/play is set to play we should check state of mute/unmute and set led appropriately
      # if mute/unmute is set to unmute we should check state of pause/play and set led appropriately
      #
      time.sleep(0.3)                               # give some time for status to be updated
      if cast.media_controller.status.player_state=="PAUSED":
        buttonshim.set_brightness(0.2)
        buttonshim.set_pixel(0xFF, 0x00, 0x00)      # red = paused
        buttonshim.set_brightness(0.5)
      else:
        if cast.status.volume_muted==True:
          buttonshim.set_brightness(0.2)
          buttonshim.set_pixel(0x00, 0x00, 0xFF)    # blue = muted
          buttonshim.set_brightness(0.5)
        else:
          # leave led alone
          pass

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
       cast.wait()                                  # wait for device to be ready
       mc=cast.media_controller
       time.sleep(0.3)                              # wait short time for media controller to activate (strictly only needed on first pass)
       if mc.status.player_state=="PLAYING":
         mc.pause()
         buttonshim.set_brightness(0.2)             # must set brightness before colour (0.5 is std)
         buttonshim.set_pixel(0xFF, 0x00, 0x00)
       else :                                       # "PAUSED"
         mc.play()
         buttonshim.set_brightness(0.5)
         buttonshim.set_pixel(0x00, 0x00, 0x00)
       time.sleep(0.3)                              # give some time for status to be updated
       button_led(buttonshim, cast)                 # check for mute/unmute status
       print('State=',mc.status.player_state)       # debug

    @buttonshim.on_release(buttonshim.BUTTON_B)
    def button_b(button, pressed):
       #print('B pressed')
       buttonshim.set_brightness(0.5)
       buttonshim.set_pixel(0x00, 0x00, 0xFF)
       cast=cc[selecteddevice]
       cast.wait()
       cast.set_volume_muted(not cast.status.volume_muted)
       time.sleep(0.3)                              # give some time for status to be updated
       if cast.status.volume_muted==True:
         buttonshim.set_pixel(0x00, 0x00, 0xFF)     # blue = muted
       else:
         buttonshim.set_pixel(0x00, 0x00, 0x00)     # off = not muted
       button_led(buttonshim, cast)                 # check for pause/play status
       print('Muted=',cast.status.volume_muted)     # debug

    @buttonshim.on_release(buttonshim.BUTTON_C)
    def button_c(button, pressed):
       #print('C pressed')
       buttonshim.set_brightness(0.5)
       buttonshim.set_pixel(0xFF, 0x80, 0xFF)
       cast=cc[selecteddevice]
       cast.wait()
       mc=cast.media_controller
       time.sleep(0.3)
       skip=skips[0]
       print('Time=',mc.status.current_time)
       print('Skip',skip)
       mc.seek(int(mc.status.current_time) + skip)
       buttonshim.set_pixel(0x00, 0x00, 0x00)
       button_led(buttonshim, cast)                 # check for mute/unmute status

    @buttonshim.on_release(buttonshim.BUTTON_D)
    def button_d(button, pressed):
       #print('D pressed')
       buttonshim.set_brightness(0.5)
       buttonshim.set_pixel(0xFF, 0x80, 0xFF)
       cast=cc[selecteddevice]
       cast.wait()
       mc=cast.media_controller
       time.sleep(0.3)
       skip=skips[1]
       #print(mc.status)
       print('Time=',mc.status.current_time)
       print('Skip',skip)
       mc.seek(int(mc.status.current_time) + skip)
       buttonshim.set_pixel(0x00, 0x00, 0x00)
       button_led(buttonshim, cast)                 # check for mute/unmute status

    @buttonshim.on_release(buttonshim.BUTTON_E)
    def button_e(button, pressed):
       #print('E pressed')
       buttonshim.set_brightness(0.5)
       buttonshim.set_pixel(0xFF, 0x80, 0xFF)
       cast=cc[selecteddevice]
       cast.wait()
       mc=cast.media_controller
       time.sleep(0.3)
       skip=skips[2]
       print('Time=',mc.status.current_time)
       print('Skip',skip)
       mc.seek(int(mc.status.current_time) + skip)
       buttonshim.set_pixel(0x00, 0x00, 0x00)
       button_led(buttonshim, cast)                 # check for mute/unmute status

