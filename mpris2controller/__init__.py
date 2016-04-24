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
__author__ = 'icasdri'

import logging
log = logging.getLogger("mpris2controller")

VERSION = "0.6"
DESCRIPTION = "A small user daemon for GNU/Linux that intelligently controls MPRIS2-compatible media players"

MY_BUS_NAME = "org.icasdri.mpris2controller"
MY_PATH = "/org/icasdri/mpris2controller"
MY_INTERFACE = MY_BUS_NAME

MPRIS_PATH = "/org/mpris/MediaPlayer2"
MPRIS_INTERFACE = "org.mpris.MediaPlayer2.Player"


