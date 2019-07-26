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