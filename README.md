# mpris2controller
**mpris2controller** is a small daemon for the Linux desktop written in python that intelligently controls [MPRIS2](http://specifications.freedesktop.org/mpris-spec/latest/)-compatible media players. It responds to commands via multimedia keys or via a command-line interface, and controls all open media players at once.

* Play/Pause control
    * Plays the most recently paused media player if none are currently playing
    * Pauses all media players if one or more are currently playing
* Next/Previous control
    * Advances to the next or previous song only on the media player that is currently playing.

This is accomplished by keeping track of the playback status of all MPRIS2 players currently active in a user's session, alleviating problems such as only being able to have keybindings for a specific player, having all players start playing at once, etc.

## Installation
**mpris2controller** is writen in Python 3, and has the following dependencies:
* `dbus-python` (packaged as `python-dbus` on some distributions)
* `python-gobject` (for the glib mainloop)

To install, simply place the `mpris2controller` script from this repo somewhere in your `PATH`. For example (placing `mpris2controller` in `/usr/local/bin`):

    git clone https://github.com/icasdri/mpris2controller.git
    sudo cp mpris2controller /usr/local/bin
    sudo chmod +x /usr/local/bin/mpris2controller

For Arch Linux users, [mpris2controller-git](https://aur.archlinux.org/packages/mpris2controller-git/) is available in the AUR.

## Usage
**mpris2controller** allows you to control all your MPRIS2-compatible multimedia players at once using the `mpris2controller` command.

* `mpris2controller PlayPause` to play the most recently paused media player or pause all media players
* `mpris2controller Next` or `mpris2controller Previous` to advance to the next or previous song on the currently playing media player

On the first run of any of these commands, mpris2controller will attempt start its daemon on-demand and detect running media players. To start the daemon manually, simply run `mpris2controller` (with no arguments) or `mpris2controller --nofork` (which starts the daemon in the foreground). Either of these commands can also be placed in an appropriate autostart system to autostart mpris2controller with a desktop session.

### Multimedia keys

To use mpris2controller via mutlimedia keys, add keyboard shortcuts for multimedia keys that run the commands listed above.

Detailed instructions for [GNOME](http://gnome.org), [i3](http://i3wm.org), and [XFCE](http://xfce.org) are provided below for convenience. For users of other Desktop Environments or Window Managers, follow your DE or WM's documentation for adding keyboard shortcuts.

##### GNOME
For [GNOME](http://gnome.org) useres, open GNOME Control Center, go to Keyboard, then Shortcuts. Or execute `gnome-control-center keyboard shortcuts`. Then scroll to the bottom and click the "+" sign. Enter any descriptive name and then enter one of the commands listed above. Finally, click "Set Shortcut" and press your respective multimedia key.

Note: mpris2controller works with the [Media Player Indicator](https://extensions.gnome.org/extension/55/media-player-indicator/) GNOME Shell Extension. GNOME will simply prompt you to override its keybindings when adding the custom shortcuts.

##### i3
For [i3](http://i3wm.org) users, add the following to your i3 config.

    bindsym XF86AudioPlay exec mpris2controller PlayPause
    bindsym XF86AudioPrev exec mpris2controller Previous
    bindsym XF86AudioNext exec mpris2controller Next

##### XFCE
For [XFCE](http://xfce.org) users, open the XFCE Settings Manager from the panel menu. Then click on Keyboard and navigate to the Application Shortcuts tab. Click on the Add button towards the bottom, enter one of the commands listed above, press OK, and finally press your respective multimedia key.

### DBus
The daemon can also be controlled via methods exposed on the [DBus](http://www.freedesktop.org/wiki/Software/dbus/) session bus.

* *Bus Address*: `org.icasdri.mpris2controller`
* *Interface*: `/org/icasdri/mpris2controller`
* *Methods*:
    * `org.icasdri.mpris2controller.PlayPause`
    * `org.icasdri.mpris2controller.Next`
    * `org.icasdri.mpris2controller.Previous`
    * `org.icasdri.mpris2controller.Quit`
