#!/bin/python

from gi.repository import GLib
import dbus
from dbus.mainloop.glib import DBusGMainLoop
import os

# Max brightness for panel
MAX_BRIGHTNESS = "/sys/class/backlight/intel_backlight/max_brightness"
m_file = open(MAX_BRIGHTNESS)
max = int(m_file.read())
m_file.close()

ACTUAL_BRIGHTNESS = "/sys/class/backlight/intel_backlight/actual_brightness"

def print_status():
    # actual value
    a_file = open(ACTUAL_BRIGHTNESS)
    actual = int(a_file.read())
    a_file.close()

    # calc brightness value
    percent = int((actual * 100) / max)

    # print
    os.system("echo {}%".format(percent))
    
    

def monitor_notification(bus, message):

    # Keys for dictionary
    keys = ["app_name", "replaces_id", "app_icon", "summary", "body", "actions", "hints", "expire_timeout"]

    args = message.get_args_list()
    if len(args) == 8:
        notification = dict([(keys[i], args[i]) for i in range(8)])

        # Check if Spotify
        if notification["app_name"] == "BRIGHTNESS":
            print_status()


loop = DBusGMainLoop(set_as_default=True)
session_bus = dbus.SessionBus()
session_bus.add_match_string("type='method_call',interface='org.freedesktop.Notifications',member='Notify',eavesdrop=true")
session_bus.add_message_filter(monitor_notification)

print_status()

GLib.MainLoop().run()
