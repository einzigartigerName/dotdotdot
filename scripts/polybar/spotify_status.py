#!/bin/python

import sys
from gi.repository import GLib
import dbus
from dbus.mainloop.glib import DBusGMainLoop

# corrects encoding for the python version used
def fix_string(string):
    if sys.version_info.major == 3:
        return string
    else:
        return string.encode('utf-8')

def print_status():
    # Output-Format
    output = fix_string(u'{artist}: {song}')

    # Read metadata and print lable for polybar
    bus = dbus.SessionBus()
    spotify_bus = bus.get_object(
        'org.mpris.MediaPlayer2.spotify',
        '/org/mpris/MediaPlayer2'
    )

    spotify_properties = dbus.Interface(
        spotify_bus,
        'org.freedesktop.DBus.Properties'
    )
            
    # All data
    metadata = spotify_properties.Get('org.mpris.MediaPlayer2.Player', 'Metadata')
    # Artist
    artist = fix_string(metadata['xesam:artist'][0]) if metadata['xesam:artist'] else ''
    # Song
    song = fix_string(metadata['xesam:title']) if metadata['xesam:title'] else ''

    if not artist and not song:
        print('')
    else:
        print(output.format(artist=artist, song=song))


def print_notification(bus, message):

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
session_bus.add_message_filter(print_notification)

# run for init print
print_status()

GLib.MainLoop().run()