# mh-z19
Read CO2 concentration from mh-z19 sensor&amp; send to [MONITOR](https://monitor.uedasoft.com) server

![MH-Z19](https://camo.qiitausercontent.com/a270df1162ed5c3bf9968b24064b91eed0dfcc11/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e616d617a6f6e6177732e636f6d2f302f34363534342f31353739663964622d306634302d373665382d303566332d3939336132346334376431382e706e67)

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

Just for reference, mh-z19 use ***UART*** and the way to activate UART is depend on ***the model of RPi***. Sometimes this seems to make some confusion for bigginer.

In this project, these difference is solved by pre required proggram installed by ***setup.sh*** and inner logic on ***mh_z19.py*** which will be described later.

So, You don't need to take care which model of RPi you are useing.

## cabling
Connect RPi & mh-z19 as:

- 5V on RPi and Vin on mh-z19
- GND(0v) on RPi and GND on mh-z19
- TxD and RxD are connect to cross between RPi and mh-z18 

Followings are example of cabling, but you can free to use other 5v and 0v Pin on the RPi. 


![Cabling](https://camo.qiitausercontent.com/112ad5fe41c82a16671d2882070384109c8860cc/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e616d617a6f6e6177732e636f6d2f302f34363534342f30383238333031342d363864322d633364652d313634342d3763386439623762363266642e6a706567)

```
pi@raspberrypi:~/mh-z19 $ gpio readall
 +-----+-----+---------+------+---+---Pi B+--+---+------+---------+-----+-----+
 | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
 +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
 |     |     |    3.3v |      |   |  1 || 2  |   |      | 5v      |     |     |
 |   2 |   8 |   SDA.1 |   IN | 1 |  3 || 4  |   |      | 5v      |     |     |  <---- with Vin on mh-z19
 |   3 |   9 |   SCL.1 |   IN | 1 |  5 || 6  |   |      | 0v      |     |     |  <---- with Gnd on mh-z19
 |   4 |   7 | GPIO. 7 |   IN | 1 |  7 || 8  | 1 | ALT0 | TxD     | 15  | 14  |  <---- with RxD on mh-z19
 |     |     |      0v |      |   |  9 || 10 | 1 | ALT0 | RxD     | 16  | 15  |  <---- with TxD on mh-z19
 |  17 |   0 | GPIO. 0 |   IN | 0 | 11 || 12 | 0 | IN   | GPIO. 1 | 1   | 18  |
 |  27 |   2 | GPIO. 2 |   IN | 0 | 13 || 14 |   |      | 0v      |     |     |
 |  22 |   3 | GPIO. 3 |   IN | 0 | 15 || 16 | 0 | IN   | GPIO. 4 | 4   | 23  |
 |     |     |    3.3v |      |   | 17 || 18 | 0 | IN   | GPIO. 5 | 5   | 24  |
 |  10 |  12 |    MOSI |   IN | 0 | 19 || 20 |   |      | 0v      |     |     |
 |   9 |  13 |    MISO |   IN | 0 | 21 || 22 | 0 | IN   | GPIO. 6 | 6   | 25  |
 |  11 |  14 |    SCLK |   IN | 0 | 23 || 24 | 1 | IN   | CE0     | 10  | 8   |
 |     |     |      0v |      |   | 25 || 26 | 1 | IN   | CE1     | 11  | 7   |
 |   0 |  30 |   SDA.0 |   IN | 1 | 27 || 28 | 1 | IN   | SCL.0   | 31  | 1   |
 |   5 |  21 | GPIO.21 |   IN | 1 | 29 || 30 |   |      | 0v      |     |     |
 |   6 |  22 | GPIO.22 |   IN | 1 | 31 || 32 | 0 | IN   | GPIO.26 | 26  | 12  |
 |  13 |  23 | GPIO.23 |   IN | 0 | 33 || 34 |   |      | 0v      |     |     |
 |  19 |  24 | GPIO.24 |   IN | 0 | 35 || 36 | 0 | IN   | GPIO.27 | 27  | 16  |
 |  26 |  25 | GPIO.25 |   IN | 0 | 37 || 38 | 0 | IN   | GPIO.28 | 28  | 20  |
 |     |     |      0v |      |   | 39 || 40 | 0 | IN   | GPIO.29 | 29  | 21  |
 +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
 | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
 +-----+-----+---------+------+---+---Pi B+--+---+------+---------+-----+-----+
```

## set view_id
Make sure your view_id on your account of the MONITOR, let's say it was ABCDEF, set it by setid.sh as

```
./setid.sh ABCDEF
```

## test for getting CO2 Sensor value

```
sudo python mh_z19.py
```

In case succeeded, espected response is as follows:

```
pi@raspberrypi:~/mh-z19 $ sudo python mh_z19.py
{'co2': 420}
```

In case everything succeeded, expected response is consist of the log of taking photo, sending it, and {"ok":true} as follows:

or, return ```None``` in case 
- Cabling between RPi & sensor is not correct.
- Sensor is no work.
- ***setup*** mentioned before is not finished, or not rebooted after setup.

## test for sending CO2 Sensor value

```
sudo python read.py
```
## setting for automatically run view.sh at 5 minute interval

You can do it both by setting crontab if you're used to do so, or you can use ***autostart.sh*** command as follows:

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
pi@raspberrypi:~/mh-z19-v_1.0.0 $ sudo systemctl status view.service 
● view.service - Take photos & Post to the monitor
   Loaded: loaded (/home/pi/mh-z19-v_1.0.0/mh_z19.service; enabled; vendor preset: e
   Active: active (running) since Thu 2018-08-23 19:07:24 JST; 4min 40s ago
 Main PID: 777 (loop.sh)
   CGroup: /system.slice/view.service
           ├─777 /bin/bash /home/pi/mh-z19-v_1.0.0/loop.sh
           └─820 sleep 5m
```

In case afte service set as off, you can see followings:
```
pi@raspberrypi:~/mh-z19-v_1.0.0 $ sudo systemctl status mh_z19.service 
Unit mh_z19.service could not be found.
```

### Q&A
Any questions, suggestions, reports are welcome! Please make [issue](https://github.com/UedaTakeyuki/mh-z19/issues) without hesitation! 
