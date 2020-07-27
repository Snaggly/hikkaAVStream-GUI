#!/usr/bin/python3

#My apologies for terrible coding, this is my very first python script.
#There is yet much to learn and adapt!

import gi, subprocess, os, fileinput, sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import GLib

class ErrorGUI(gtk.Window):
    def __init__(self, text):
        gtk.Window.__init__(self, title="Error")
        dialog = gtk.MessageDialog(self, 0, gtk.MessageType.ERROR, gtk.ButtonsType.OK, "There was an error finding dependencies")
        dialog.format_secondary_text(text + " is missing!")
        dialog.run()
        dialog.destroy()
        exit(0)

class GUI:
    def __init__(self):
        #Building GUI from XML
        gladeFile = "hikkaAVStream-GUI.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(gladeFile)
        self.builder.connect_signals(self)

        self.isRunning = False

        #Getting Monitor and Speaker data - Reading terminal output
        monitors = subprocess.run(['xrandr', '--listactivemonitors'], stdout=subprocess.PIPE).stdout.decode('utf')
        speakers = subprocess.run(['pacmd', 'list-sinks'], stdout=subprocess.PIPE).stdout.decode('utf')
        mics = subprocess.run(['pacmd', 'list-sources'], stdout=subprocess.PIPE).stdout.decode('utf')

        #Getting GUI Objects
        self.monitorComboBoxItems = self.builder.get_object("monitorStore")
        self.speakerComboBoxItems = self.builder.get_object("speakerStore")
        self.microphComboBoxItems = self.builder.get_object("microphStore")

        self.monitorComboBox = self.builder.get_object("MonitorCombBox")
        self.speakerComboBox = self.builder.get_object("SpeakerCombBox")
        self.microphComboBox = self.builder.get_object("MicCombBox")

        self.starterButton = self.builder.get_object("ServiceRunnerButton")
        self.startimg = self.builder.get_object("startimg")
        self.stopimg = self.builder.get_object("stopimg")

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

    def buttonEvent(self, widget):
        if self.isRunning is False:
            self.isRunning = True
            self.starterButton.set_label("Stop Service")
            self.starterButton.set_image(self.stopimg)

            #Collect data from GUI
            device = self.builder.get_object('DevEntry').get_text()
            fps = self.builder.get_object('FPSEntry').get_text()
            res = self.builder.get_object('ResEntry').get_text()
            monitor = self.builder.get_object('MonitorCombBox').get_active()

            speakerIter = self.builder.get_object('SpeakerCombBox').get_active_iter()
            speaker = self.speakerComboBoxItems[speakerIter][0]

            micIter = self.builder.get_object('MicCombBox').get_active_iter()
            microphone = self.microphComboBoxItems[micIter][0]

            horizonal = self.builder.get_object('HorizontalFlipCheck').get_active()
            vertical = self.builder.get_object('VerticallFlipCheck').get_active()
            incldSnd = self.builder.get_object('SoundCheck').get_active()
            
            flip = ''
            if vertical:
                flip = flip + ' -vf'
            if horizonal:
                flip = flip + ' -hf'

            #Search and replace from shell script:
            for line in fileinput.input("havs.sh", inplace=1):
                if line.startswith('RESOLUTION='):
                    line = 'RESOLUTION=\"' + res + '\"\n'
                if line.startswith('MICROPHONE='):
                    line = 'MICROPHONE=\"' + microphone + '\"\n'
                if line.startswith('SPEAKERS='):
                    line = 'SPEAKERS=\"' + speaker + '\"\n'
                if not incldSnd and (line.startswith('pactl') or line.startswith('pacmd')):
                    line = '#' + line
                elif  incldSnd and (line.startswith('#pactl') or line.startswith('#pacmd')):
                    line = line[1:]
                sys.stdout.write(line)
            
            #Start shell script:
            self.havs = subprocess.Popen(['./havs.sh','-f',fps,'-d',device,'-m',str(monitor),flip])
        else:
            #Stop shell script
            self.havs.terminate()
            self.isRunning = False
            self.starterButton.set_label("Start Service")
            self.starterButton.set_image(self.startimg)


def dependcenyCheck(binary):
    whereis = subprocess.run(['whereis', binary], stdout=subprocess.PIPE).stdout.decode('utf')
    return whereis!=binary+':\n'

if not dependcenyCheck('xrandr'):
    main = ErrorGUI("xrandr")
    gtk.main()

if not dependcenyCheck('ffmpeg'):
    main = ErrorGUI("ffmpeg")
    gtk.main()

if __name__ == '__main__':
    main = GUI()
    gtk.main()
