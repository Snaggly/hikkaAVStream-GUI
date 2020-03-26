#!/usr/bin/python

import gi, subprocess
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import GLib

class GUI:
    def __init__(self):
        #Building GUI from XML
        gladeFile = "hikkaAVStream-GUI.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(gladeFile)
        self.builder.connect_signals(self)

        #Getting Monitor and Speaker data - Reading terminal output
        monitors = subprocess.run(['xrandr', '--listactivemonitors'], stdout=subprocess.PIPE).stdout.decode('ascii')
        speakers = subprocess.run(['pacmd', 'list-sinks'], stdout=subprocess.PIPE).stdout.decode('ascii')
        mics = subprocess.run(['pacmd', 'list-sources'], stdout=subprocess.PIPE).stdout.decode('ascii')

        #Getting GUI Objects
        self.monitorComboBoxItems = self.builder.get_object("monitorStore")
        self.speakerComboBoxItems = self.builder.get_object("speakerStore")
        self.microphComboBoxItems = self.builder.get_object("microphStore")

        self.monitorComboBox = self.builder.get_object("MonitorCombBox")
        self.speakerComboBox = self.builder.get_object("SpeakerCombBox")
        self.microphComboBox = self.builder.get_object("MicCombBox")
        
        #Filling Monitor combobox
        i = 1
        while i <= len(monitors.split('\n')) - 2:
            line = monitors.split('\n')[i].strip()
            self.monitorComboBoxItems.append([line])
            i = i + 1

        #Filling Speaker combobox
        for line in speakers.split('\n'):
            line = line.strip()
            if line.startswith('name:'):
                line = line.replace("name: <", "").replace(">", "")
                self.speakerComboBoxItems.append([line])

        #Filling Microphone combobox
        for line in mics.split('\n'):
            line = line.strip()
            if line.startswith('name:'):
                line = line.replace("name: <", "").replace(">", "")
                self.microphComboBoxItems.append([line])
        
        #To do: Read from the shell script later which item was chosen....
        self.monitorComboBox.set_active(0)
        self.speakerComboBox.set_active(0)
        self.microphComboBox.set_active(0)

        window = self.builder.get_object("Main_Window")
        window.connect("delete-event", gtk.main_quit)
        window.show()

if __name__ == '__main__':
    main = GUI()
    gtk.main()