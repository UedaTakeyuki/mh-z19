# mh-z19
Read CO2 concentration from mh-z19 sensor&amp; send to [MONITOR](https://monitor.uedasoft.com) server

![Monitor](pic/スクリーンショット 2015-12-22 19.02.07.png)

## install
download from [release](https://github.com/UedaTakeyuki/mh-z19/releases)

or 

```
git clone https://github.com/UedaTakeyuki/mh-z19.git
```

## setup
Setup environment & install prerequired modules by

```
./setup.sh 
```

## set view_id
Make sure your view_id on your account of the MONITOR, let's say it was ABCDEF, set it by setid.sh as

```
./setid.sh ABCDEF
```

## test

```
./view.sh
```

In case everything succeeded, expected response is consist of the log of taking photo, sending it, and {"ok":true} as follows:

```
--- Opening /dev/video0...
Trying source module v4l2...
/dev/video0 opened.
No input was specified, using the first.
Delaying 1 seconds.
--- Capturing frame...
Skipping 20 frames...
Capturing 1 frames...
Captured 21 frames in 0.67 seconds. (31 fps)
--- Processing captured image...
Writing JPEG image to '/tmp/20180823190339.jpg'.
{"ok":true}
```

In case something wrong, response finished with {"ok":false,"reason":"XXX"}. For Example:

```
{"ok":false,"reason":"ViewID not valid"}
```

In case, you should make sure if correct view_is was set by setid.sh command.

## setting for automatically run view.sh at 5 minute interval

You can do it both by setting crontab if you're used to do so, or you can use autostart.sh command as follows:

```
# set autostart on
./autostart.sh --on

# set autostart off
./autostart.sh --off
```

Tecknically speaking, autostart.sh doesn't use crontab, instead, prepare service for interval running of view.sh named view.service .
You can confirm current status of view.service with following command:

```
sudo systemctl status view.service
```

In case view.service is running, you can see the log of current status and taking & sending photo as follows:
```
pi@raspberrypi:~/view-v_1.1.1 $ sudo systemctl status view.service 
● view.service - Take photos & Post to the monitor
   Loaded: loaded (/home/pi/view-v_1.1.1/view.service; enabled; vendor preset: e
   Active: active (running) since Thu 2018-08-23 19:07:24 JST; 4min 40s ago
 Main PID: 777 (loop.sh)
   CGroup: /system.slice/view.service
           ├─777 /bin/bash /home/pi/view-v_1.1.1/loop.sh
           └─820 sleep 5m

Aug 23 19:07:26 raspberrypi loop.sh[777]: --- Capturing frame...
Aug 23 19:07:26 raspberrypi loop.sh[777]: Skipping 20 frames...
Aug 23 19:07:28 raspberrypi loop.sh[777]: Capturing 1 frames...
Aug 23 19:07:28 raspberrypi loop.sh[777]: Captured 21 frames in 1.73 seconds. (1
Aug 23 19:07:28 raspberrypi loop.sh[777]: --- Processing captured image...
Aug 23 19:07:29 raspberrypi loop.sh[777]: Writing JPEG image to '/tmp/2018082319
Aug 23 19:07:29 raspberrypi loop.sh[777]:   % Total    % Received % Xferd  Avera
Aug 23 19:07:29 raspberrypi loop.sh[777]:                                  Dload
Aug 23 19:07:53 raspberrypi loop.sh[777]: [2.0K blob data]
Aug 23 19:07:53 raspberrypi loop.sh[777]:      0
lines 1-18/18 (END)
```

In case afte service set as off, you can see followings:
```
pi@raspberrypi:~/view-v_1.1.1 $ sudo systemctl status view.service 
Unit view.service could not be found.
```

### Q&A
Any questions, suggestions, reports are welcome! Please make [issue](https://github.com/UedaTakeyuki/view/issues) without hesitation! 
