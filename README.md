# mpris2controller
**mpris2controller** is a small daemon for the Linux desktop that intelligently controls [MPRIS2](http://specifications.freedesktop.org/mpris-spec/latest/)-compatible media players. It responds to commands via multimedia keys or via a command-line interface, and controls all open media players at once.

* Play/Pause control
    * Plays the most recently paused media player if none are currently playing
    * Pauses all media players if one or more are currently playing
* Next/Previous control
    * Advances to the next or previous song on the media player that is currently playing, or on the most recently _used_ media player if all are paused.

It accomplishes this by keeping track of the playback status of all MPRIS2 players currently active in a user's session, alleviating problems such as only being able to have keybindings for a specific player, having all players start playing at once, etc.

## Installation
**mpris2controller** is written in Python 3, and requires the following dependencies:
* `dbus-python` (packaged as `python-dbus` on some distributions)
* `python-gobject` (for the glib mainloop)

To install, simply place the `mpris2controller` script from this repository somewhere in your `PATH`. For example, place `mpris2controller` in `/usr/local/bin` with

    git clone https://github.com/icasdri/mpris2controller.git
    sudo cp mpris2controller/mpris2controller /usr/local/bin
    sudo chmod +x /usr/local/bin/mpris2controller

For Arch Linux users, [mpris2controller-git](https://aur.archlinux.org/packages/mpris2controller-git/) is available in the AUR.

## Usage
**mpris2controller** allows you to control all of your MPRIS2-compatible multimedia players at once using the `mpris2controller` command.

* `mpris2controller PlayPause` to play the most recently paused media player or pause all media players
* `mpris2controller Next` or `mpris2controller Previous` to advance to the next or previous song on the currently playing media player

On the first run of any of these commands, mpris2controller will attempt start its daemon on-demand and detect running media players. To start the daemon manually, simply run `mpris2controller` (with no arguments) or `mpris2controller --nofork` (which starts the daemon in the foreground). Either of these commands can also be placed in an appropriate autostart system to autostart mpris2controller with a desktop session.

To use mpris2controller via multimedia keys, simply add the desired keyboard shortcuts for the above commands via your desktop environment or window manager. For example, in [GNOME](https://gnome.org), see `gnome-control-center keyboard`.

### DBus
The daemon can also be controlled via methods exposed on the [DBus](http://www.freedesktop.org/wiki/Software/dbus/) session bus.

* *Bus Address*: `org.icasdri.mpris2controller`
* *Interface*: `/org/icasdri/mpris2controller`
* *Methods*:
    * `org.icasdri.mpris2controller.PlayPause`
    * `org.icasdri.mpris2controller.Next`
    * `org.icasdri.mpris2controller.Previous`
    * `org.icasdri.mpris2controller.Quit`
