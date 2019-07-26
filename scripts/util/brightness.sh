#!/usr/bin/env zsh

usage () {
    echo -e "Usage:\n\tup\traises the display brightness\n\tdown\tlowers the display brightness\n"
    exit
}

update_bar () {
    MAX=$(cat /sys/class/backlight/intel_backlight/max_brightness)
    ACT=$(cat /sys/class/backlight/intel_backlight/actual_brightness)

    percent=$(($ACT * 100))
    percent=$(($percent / $MAX))

    notify-send -a "BRIGHTNESS" "$percent"
}

case $1 in
    "up" )
        xbright +75
        update_bar;;
    "down" )
        xbright -75
        update_bar;;
    *)          usage;;
esac