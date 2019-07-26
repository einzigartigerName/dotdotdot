#!/bin/python

from gi.repository import GLib
import dbus
from dbus.mainloop.glib import DBusGMainLoop
import os

def print_status():
    os.system("python $HOME/.scripts/polybar/spotify_status/status.py")

def monitor_notification(bus, message):

    # Keys for dictionary
    keys = ["app_name", "replaces_id", "app_icon", "summary", "body", "actions", "hints", "expire_timeout"]

    args = message.get_args_list()
    if len(args) == 8:
        notification = dict([(keys[i], args[i]) for i in range(8)])

        # Check if Spotify
        if notification["app_name"] == "Spotify":
            print_status()


loop = DBusGMainLoop(set_as_default=True)
session_bus = dbus.SessionBus()
session_bus.add_match_string("type='method_call',interface='org.freedesktop.Notifications',member='Notify',eavesdrop=true")
session_bus.add_message_filter(monitor_notification)

# run for init print
print_status()

GLib.MainLoop().run()
