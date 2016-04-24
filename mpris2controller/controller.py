# Copyright 2014-2016 icasdri
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

from mpris2controller import log, MPRIS_PATH, MPRIS_INTERFACE, MY_BUS_NAME, MY_PATH, MY_INTERFACE

def is_mpris_player(name):
    return name.startswith("org.mpris.MediaPlayer2")


class Controller(dbus.service.Object):
    def __init__(self, bus, call=None):
        self.bus = bus

        bus_name = dbus.service.BusName(MY_BUS_NAME, bus=self.bus)
        dbus.service.Object.__init__(self, bus_name, MY_PATH)

        self.bus.add_signal_receiver(
            signal_name="PropertiesChanged",
            handler_function=self.handle_signal_properties_changed,
            path=MPRIS_PATH,
            sender_keyword='sender')
        self.bus.add_signal_receiver(
            signal_name="NameOwnerChanged",
            handler_function=self.handle_signal_name_change,
            path=dbus.BUS_DAEMON_PATH,
            bus_name=dbus.BUS_DAEMON_NAME)

        self.playing = set()
        self.not_playing = []

        log.info("Detecting players already on bus...")
        for well_known_name in filter(is_mpris_player, bus.list_names()):
            name = self.bus.get_name_owner(well_known_name)
            if self.bus.get_object(name, MPRIS_PATH).Get(MPRIS_INTERFACE, "PlaybackStatus") == "Playing":
                self.markas_playing(name)
            else:
                self.markas_not_playing(name)

        if call is not None:
            try:
                getattr(self, call)()
            except AttributeError:
                log.error("Method name %s given on start is not valid.", call)

    def handle_signal_properties_changed(self, interface, props, sig, sender=None):
        del sig
        if interface == MPRIS_INTERFACE:
            if "PlaybackStatus" in props:
                log.info("Received PropertiesChanged signal with PlaybackStatus from %s.", sender)
                if props["PlaybackStatus"] == "Playing":
                    self.markas_playing(sender)
                else:
                    self.markas_not_playing(sender)

    def handle_signal_name_change(self, name, old_owner, new_owner):
        if new_owner == "":
            log.info("Received NameOwnerChange signal from bus daemon. Owner of %s lost.", name)
            self.remove(name)
        elif old_owner != "":
            log.info("Received NameOwnerChange signal from bus daemon. %s is now %s.", old_owner, new_owner)
            try:
                player_index = self.not_playing.index(old_owner)
                self.not_playing[player_index] = new_owner
            except ValueError:
                try:
                    self.playing.remove(old_owner)
                    self.playing.add(new_owner)
                except ValueError:
                    # Then this isn't a player we're tracking, and it's not our concern
                    pass


    def markas_playing(self, name):
        # Add to playing
        try:
            self.not_playing.remove(name)
        except ValueError:
            pass
        if name not in self.playing:
            self.playing.add(name)
            log.info("%s marked as playing.", name)

    def markas_not_playing(self, name):
        # Add to back of non-playing
        self.playing.discard(name)
        if name not in self.not_playing:
            self.not_playing.append(name)
            log.info("%s marked as not playing.", name)

    def remove(self, name):
        try:
            self.not_playing.remove(name)
            self.playing.discard(name)
        except ValueError:
            pass

    def _call_on_player(self, player, method_name):
        getattr(dbus.Interface(
            self.bus.get_object(player, MPRIS_PATH),
            dbus_interface=MPRIS_INTERFACE), method_name)()

    def call_on_all_playing(self, method_name):
        # Loops through all in playing and calls method
        for n in self.playing:
            self._call_on_player(n, method_name)

    def call_on_one_playing(self, method_name):
        # Calls on one in playing, only if there is only one playing
        if len(self.playing) == 1:
            self.call_on_all_playing(method_name)

    def call_on_head_not_playing(self, method_name):
        # Pops/peeks first off back of non-playing and calls method
        if len(self.not_playing) > 0:
            self._call_on_player(self.not_playing[-1], method_name)

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


