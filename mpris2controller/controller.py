# Copyright 2014 icasdri
#
# This file is part of mpris2controller.
#
# mpris2controller is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# mpris2controller is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
__author__ = "icasdri"

import dbus
import dbus.service
import sys
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

VERSION = 0.3
DESCRIPTION = "A small user daemon for GNU/Linux that intelligently controls MPRIS2-compatible media players"

MY_PATH = "/org/icasdri/mpris2controller"
MY_INTERFACE = "org.icasdri.mpris2controller"

MPRIS_PATH = "/org/mpris/MediaPlayer2"
MPRIS_INTERFACE = "org.mpris.MediaPlayer2.Player"

def is_mpris_player(name):
    return name.find("org.mpris.MediaPlayer2") == 0


class Controller(dbus.service.Object):
    def __init__(self, bus):
        self.bus = bus
        bus_name = dbus.service.BusName(MY_INTERFACE, bus=self.bus)

        dbus.service.Object.__init__(self, bus_name, MY_PATH)

        self.bus.add_signal_receiver(
            signal_name="PropertiesChanged",
            handler_function=self.handle_signal_properties_changed,
            path=MPRIS_PATH,
            #dbus_interface=MPRIS_INTERFACE, # This doesn't seem to work for some reason
            sender_keyword='sender')
        self.bus.add_signal_receiver(
            signal_name="NameOwnerChanged",
            handler_function=self.handle_signal_name_change,
            path=dbus.BUS_DAEMON_PATH,
            bus_name=dbus.BUS_DAEMON_NAME,
            sender_keyword='sender')

        self.playing = set()
        self.not_playing = []

        log.info("Detecting players already on bus...")
        for well_known_name in filter(is_mpris_player, bus.list_names()):
            name = self.bus.get_name_owner(well_known_name)
            if self.bus.get_object(name, MPRIS_PATH).Get(MPRIS_INTERFACE, "PlaybackStatus") == "Playing":
                self.markas_playing(name)
            else:
                self.markas_not_playing(name)

    def handle_signal_properties_changed(self, interface, props, sig, sender=None):
        if interface == MPRIS_INTERFACE:
            if "PlaybackStatus" in props:
                log.info("Received PropertiesChanged signal with PlaybackStatus from {}.".format(sender))
                if props["PlaybackStatus"] == "Playing":
                    self.markas_playing(sender)
                else:
                    self.markas_not_playing(sender)

    def handle_signal_name_change(self, name, old_name, new_name, sender=None):
        #if self.players.has(name) and self.players.has(old_name) and new_name == "":
        #print(name, ":", old_name, "is now", new_name)
        if new_name == "":
            log.info("Received NameOwnerChange signal from bus daemon. Owner of {} lost.".format(name))
            self.remove(name)

    def markas_playing(self, name):
        # Add to playing
        try:
            self.not_playing.remove(name)
        except ValueError:
            pass
        if name not in self.playing:
            self.playing.add(name)
            log.info("{} marked as playing".format(name))

    def markas_not_playing(self, name):
        # Add to back of non-playing
        self.playing.discard(name)
        if name not in self.not_playing:
            self.not_playing.append(name)
            log.info("{} marked as not playing".format(name))

    def remove(self, name):
        try:
            self.not_playing.remove(name)
            self.playing.discard(name)
        except ValueError:
            pass

    def call_on_all_playing(self, method_name):
        # Loops through all in playing and calls method
        for n in self.playing:
            self.bus.get_object(n, MPRIS_PATH).__getattr__(method_name)()

    def call_on_one_playing(self, method_name):
        # Calls on one in playing, only if there is only one playing
        if len(self.playing) == 1:
            self.call_on_all_playing(method_name)

    def call_on_head_not_playing(self, method_name):
        # Pops/peeks first off back of non-playing and calls method
        if len(self.not_playing) > 0:
            self.bus.get_object(self.not_playing[-1], MPRIS_PATH).__getattr__(method_name)()

    @dbus.service.method(dbus_interface=MY_INTERFACE)
    def PlayPause(self):
        log.info("Method call for PlayPause!")
        if len(self.playing) > 0:
            self.call_on_all_playing("Pause")
        else:
            self.call_on_head_not_playing("Play")

    @dbus.service.method(dbus_interface=MY_INTERFACE)
    def Next(self):
        log.info("Method call for Next!")
        self.call_on_one_playing("Next")

    @dbus.service.method(dbus_interface=MY_INTERFACE)
    def Previous(self):
        log.info("Method call for Previous!")
        self.call_on_one_playing("Previous")

def _parse_args(options=None):
    import argparse
    a_parser = argparse.ArgumentParser(prog="mpris2controller",
                                       description=DESCRIPTION)
    a_parser.add_argument("--version", action='version', version="%(prog)s v{}".format(VERSION))
    a_parser.add_argument("--debug", action='store_true')

    if options is None:
        args = a_parser.parse_args()
    else:
        args = a_parser.parse_args(options)

    if args.debug:
        log.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        log.addHandler(handler)
    else:
        log.setLevel(logging.WARNING)
        error_handler = logging.StreamHandler(sys.stderr)
        log.addHandler(error_handler)

def entry_point(options=None):
    _parse_args(options)
    Controller(dbus.SessionBus())

def main():
    from dbus.mainloop.glib import DBusGMainLoop
    from gobject import MainLoop
    DBusGMainLoop(set_as_default=True)
    entry_point()
    MainLoop().run()

if __name__ == "__main__":
    main()

