# mpris2controller
**mpris2controller** is a small user daemon for GNU/Linux written in python that intelligently controls [MPRIS2](http://specifications.freedesktop.org/mpris-spec/latest/)-compatible media players.

Users call the daemon (via multimedia keys or otherwise) to control all their media players at once.

When called, the daemon does what the user expects:
* When called to Play or Pause, the daemon either
	* Pauses all players if one or more are currently playing, OR
    * Plays the most recently paused player if none are currently playing
* When the user directs the daemon to advance to the next of previous song, the daemon calls Next or Previous only on the player that is playing.

The daemon accomplishes this by keeping track of the playback status of all MPRIS2 players currently active in the user's session.

No more hitting the PlayPause multimedia key and having all your players start playing at once! And no more having to control only one specific player when using a Desktop Environment that does not have builtin support.

## Installation
**mpris2controller** is composed of a single python .py file, and requires the following dependencies:
* `python3`
* `dbus`
* `dbus-python` (packaged as `python-dbus` on some distributions)
* `python3-gobject` (for the glib mainloop)

To install, simply plop the file `mpris2controller` somewhere in your `$PATH` and mark it as executable.

For Arch Linux users, [mpris2controller-git](https://aur.archlinux.org/packages/mpris2controller-git/) is available in the AUR.

## Usage
**mpris2controller** is controlled via methods `PlayPause`, `Next`, and `Previous` exposed on [DBus](http://www.freedesktop.org/wiki/Software/dbus/) at bus address `org.icasdri.mpris2controller` and interface `/org/icasdri/mpris2controller`

These methods can be called from a terminal using the following commands (provided by DBus):

###### PlayPause
	dbus-send --session --type=method_call --dest=org.icasdri.mpris2controller /org/icasdri/mpris2controller org.icasdri.mpris2controller.PlayPause

###### Next
	dbus-send --session --type=method_call --dest=org.icasdri.mpris2controller /org/icasdri/mpris2controller org.icasdri.mpris2controller.Next

###### Previous
	dbus-send --session --type=method_call --dest=org.icasdri.mpris2controller /org/icasdri/mpris2controller org.icasdri.mpris2controller.Previous

### Autostart

The daemon must be started for it to work. Simply have `mpris2controller` autostart with your desktop session.

Detailed instructions for [i3](http://i3wm.org) and [XFCE](http://xfce.org) are provided below for convenience. For users of other Desktop Environments or Window Managers, follow your DE or WM's documentation for autostarting applications.

##### i3
For [i3](http://i3wm.org) users, add the following to your i3 config.

	exec --no-startup-id mpris2controller

##### XFCE
For [XFCE](http://xfce.org) users, open the XFCE Settings Manager from the panel menu. Then click on Session and Startup and navigate to the Application Autostart tab.

Click on the Add button towards the bottom, fill in any Name and Description, then put `mpris2controller` as the Command, and finally press OK.

### Multimedia keys

To control the daemon via mutlimedia keys add keyboard shortcuts that bind your multimedia keys to the commands listed at the beginning of the Usage section. 

Detailed instructions for [i3](http://i3wm.org) and [XFCE](http://xfce.org) are provided below for convenience. For users of other Desktop Environments or Window Managers, follow your DE or WM's documentation for adding keyboard shortcuts.

##### i3
For [i3](http://i3wm.org) users, add the following to your i3 config.

	bindsym XF86AudioPlay exec dbus-send --session --type=method_call --dest=org.icasdri.mpris2controller /org/icasdri/mpris2controller org.icasdri.mpris2controller.PlayPause
    bindsym XF86AudioPrev exec dbus-send --session --type=method_call --dest=org.icasdri.mpris2controller /org/icasdri/mpris2controller org.icasdri.mpris2controller.Previous
    bindsym XF86AudioNext exec dbus-send --session --type=method_call --dest=org.icasdri.mpris2controller /org/icasdri/mpris2controller org.icasdri.mpris2controller.Next

##### XFCE
For [XFCE](http://xfce.org) users, open the XFCE Settings Manager from the panel menu. Then click on Keyboard and navigate to the Application Shortcuts tab.

Click on the Add button towards the bottom, enter one of the commands listed at the beginning of the Usage section, press OK, and finally press your respective multimedia key.