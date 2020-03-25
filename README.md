# hikkaAVStream-GUI
Allows you to bypass discords' limitations on streaming with linux. With hikkaAVStream you can stream one of your monitors if you have dual screen setup, while also streaming audio. 

Originally made by the users mentioned below. I'm only contributing a GTK GUI to it.

Dependencies:
-
- xrandr
- ffmpeg
- v4l2loopback
- pulseaudio

Note to ubuntu users:
-
I wasn't able to use v4l2loopback provided by ubuntu's repository. I don't exactly know why, but with v4l2loopback installed with apt, ffmpeg just spits out error. I provided kernel module for Linux 5.0.0-25, but if you'll ever need to use this utility on newer version of linux, please compile v4l2loopback yourself. 

Instructions:
-
- Install dependencies
- Clone repo
- Start the python script and hit start
- Follow prompt
- Switch discord webcam to dummy device (Must be running)
- Switch discord microphone to "Input" device monitor. (This could be done using pavucontrol)
- Switch output device in your aplication to "OutputInputSpeakers"

```
./havs.sh - Monitor to Camera

./havs.sh [option] [value]

options:
-h, --help                show help
-f, --framerate=FPS       set framerate
-d, --device-number=NUM   set device number
-m, --monitor-number=NUM  set monitor number
```

```
Monitors: 2
 0: +*DP-0 1920/531x1080/299+0+0  DP-0
 1: +HDMI-0 1366/410x768/230+1920+0  HDMI-0
Which monitor: 0
CTRL + C to stop
```


Mentions
- [Mon2Cam](https://github.com/ShayBox/Mon2Cam) for foundation and video.
- [pulseaudio-config](https://github.com/toadjaune/pulseaudio-config) for audio.
- [v4l2loopback](https://github.com/umlaeute/v4l2loopback) for making this work. 
- [hikkaAVStream](https://github.com/hikkamorii/hikkaAVStream) which I forked from.
