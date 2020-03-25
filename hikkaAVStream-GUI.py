#!/usr/bin/python

import gi, subprocess
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import GLib

class GUI:
    def __init__(self):
        gladeFile = "hikkaAVStream-GUI.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(gladeFile)
        self.builder.connect_signals(self)

        self.monitors = subprocess.run(['xrandr', '--listactivemonitors'], stdout=subprocess.PIPE).stdout.decode('ascii')
        self.speakers = subprocess.run(['pacmd', 'list-sinks'], stdout=subprocess.PIPE).stdout.decode('ascii')
        self.mics = subprocess.run(['pacmd', 'list-sources'], stdout=subprocess.PIPE).stdout.decode('ascii')

        print(self.monitors)
        print(self.speakers)
        print(self.mics)

        window = self.builder.get_object("Main_Window")
        window.connect("delete-event", gtk.main_quit)
        window.show()

if __name__ == '__main__':
    main = GUI()
    gtk.main()