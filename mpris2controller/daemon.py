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

import argparse
import logging
import sys
import os

import dbus
from dbus.exceptions import DBusException

from mpris2controller import log, MY_BUS_NAME, MY_PATH, VERSION, DESCRIPTION
from mpris2controller.controller import Controller

def _parse_args(options=None):
    a_parser = argparse.ArgumentParser(prog="mpris2controller",
                                       description=DESCRIPTION)
    a_parser.add_argument('call', nargs='?', metavar='METHOD',
                          help="calls method (PlayPause, Next, or Previous) on daemon, starting it if necessary"
                               "(note: cannot be used with --no-fork)")
    a_parser.add_argument('--no-fork', '--nofork', '--foreground', action='store_true',
                          help="prevent daemon from forking to background")
    a_parser.add_argument('--version', action='version', version="%(prog)s v{}".format(VERSION))
    a_parser.add_argument('--debug', action='store_true')

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

    return args


def _start_daemon(call=None):
    from gi.repository.GLib import MainLoop
    loop = MainLoop()
    log.info("Starting the daemon.")
    Controller(dbus.SessionBus(), loop=loop, call=call)
    loop.run()


def _fork_daemon(debug=False, call=None):
    log.info("Forking to new process.")
    child_1 = os.fork()
    if child_1 == 0:
        os.umask(0)
        os.chdir(r'/')
        if not debug:
            os.close(0)
            os.close(1)
            os.close(2)
        _start_daemon(call=call)
        exit(1)  # Do not continue running non-daemon code if mainloop exits


def _daemon_up():
    return dbus.SessionBus().name_has_owner(MY_BUS_NAME)


def _call_method(method_name):
    try:
        log.info("Calling method %s on daemon.", method_name)
        getattr(dbus.SessionBus().get_object(MY_BUS_NAME, MY_PATH), method_name)()
    except DBusException as ex:
        log.error("%s\nFailed to call method %s. Check that the method name "
                  "is spelled correctly.\n", ex, method_name)


def entry_point(options=None):
    args = _parse_args(options)
    Controller(dbus.SessionBus(), call=args.call)


def main():
    args = _parse_args()

    from dbus.mainloop.glib import DBusGMainLoop
    DBusGMainLoop(set_as_default=True)

    if not _daemon_up():
        if args.no_fork:
            _start_daemon(call=args.call)
        else:
            _fork_daemon(debug=args.debug, call=args.call)
    else:
        log.info("Daemon already running.")
        if args.call is not None:
            _call_method(args.call)
        else:
            # Notify user with message that daemon is already running
            print("Daemon is already running.")

    log.info("Exiting.")
    exit()


if __name__ == "__main__":
    main()
