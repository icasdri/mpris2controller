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

from contextlib import suppress

import dbus
import dbus.service
from dbus.exceptions import DBusException

from mpris2controller import (log, MPRIS_PATH, MPRIS_INTERFACE,
                              MY_BUS_NAME, MY_PATH, MY_INTERFACE)

remove_if_there = suppress(ValueError)


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
            status = self._get_player(name).Get(MPRIS_INTERFACE,
                                                "PlaybackStatus")
            if status == "Playing":
                self.markas_playing(name)
            else:
                self.markas_not_playing(name)

        if call is not None:
            try:
                getattr(self, call)()
            except AttributeError:
                log.error("Method name %s given on start is not valid.", call)

    def handle_signal_properties_changed(self, interface, props,
                                         sig, sender=None):
        del sig
        if interface == MPRIS_INTERFACE:
            if "PlaybackStatus" in props:
                log.info("PlaybackStatus PropertiesChanged from %s.", sender)
                if props["PlaybackStatus"] == "Playing":
                    self.markas_playing(sender)
                else:
                    self.markas_not_playing(sender)

    def handle_signal_name_change(self, name, old_owner, new_owner):
        if new_owner == "":
            log.info("NameOwnerChange: Owner of %s lost.", name)
            self.remove(name)
        elif old_owner != "":
            log.info("NameOwnerChange: %s is now %s.", old_owner, new_owner)
            try:
                player_index = self.not_playing.index(old_owner)
                self.not_playing[player_index] = new_owner
            except ValueError:
                with remove_if_there:
                    self.playing.remove(old_owner)
                    self.playing.add(new_owner)

    def markas_playing(self, name):
        # Add to playing
        with remove_if_there:
            self.not_playing.remove(name)
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
        with remove_if_there:
            self.playing.discard(name)
            self.not_playing.remove(name)

    def _get_player(self, player):
        return dbus.Interface(
                    self.bus.get_object(player, MPRIS_PATH),
                    dbus_interface=MPRIS_INTERFACE)

    def _call_on_player(self, player, method_name):
        try:
            getattr(self._get_player(player), method_name)()
            return True
        except DBusException as e:
            if e.get_dbus_name() == \
                    "org.freedesktop.DBus.Error.ServiceUnknown":
                log.info("ServiceUnknown: %s expired", player)
                return False
            else:
                raise

    def call_on_all_playing(self, method_name):
        # Loops through all in playing and calls method
        expired = set()
        for n in self.playing:
            if not self._call_on_player(n, method_name):
                expired.add(n)

        # Not all clients correctly deregister, so we have to manually cleanup
        for player in expired:
            self.remove(player)

    def call_on_one_playing(self, method_name):
        # Calls on one in playing, only if there is only one playing
        if len(self.playing) == 1:
            self.call_on_all_playing(method_name)

    def call_on_head_not_playing(self, method_name):
        # Pops/peeks first off back of non-playing and calls method
        while len(self.not_playing) > 0:
            cur = self.not_playing[-1]
            if self._call_on_player(cur, method_name):
                return
            else:
                self.remove(cur)

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
