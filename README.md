# mh-z19
Read CO2 concentration from mh-z19 sensor&amp; and handle it.

![MH-Z19](https://camo.qiitausercontent.com/a270df1162ed5c3bf9968b24064b91eed0dfcc11/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e616d617a6f6e6177732e636f6d2f302f34363534342f31353739663964622d306634302d373665382d303566332d3939336132346334376431382e706e67)

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
 |   2 |   8 |   SDA.1 |   IN | 1 |  3 || 4  |   |      | 5v      |     |     |  <---- Vin
 |   3 |   9 |   SCL.1 |   IN | 1 |  5 || 6  |   |      | 0v      |     |     |  <---- Gnd
 |   4 |   7 | GPIO. 7 |   IN | 1 |  7 || 8  | 1 | ALT0 | TxD     | 15  | 14  |  <---- RxD
 |     |     |      0v |      |   |  9 || 10 | 1 | ALT0 | RxD     | 16  | 15  |  <---- TxD
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

## Install & Settup

### Full Set Install
Full Set include followings:

- Setup script: Install & Setup following useful stuffs as:
  - mh-z19:       A python module to read mh-z19 sensor.
  - PondSlider:   A multipurpose versatile sensor handler for python, which read mh-z19 value and handle it.
  - autostart.sh: Utility making mh-z19 as system service to act periodically.

Install Full Set, download from [release](https://github.com/UedaTakeyuki/mh-z19/releases)

or 

```
git clone https://github.com/UedaTakeyuki/mh-z19.git
```

Then, got to the folder and issue ***setup.sh****

```
./setup.sh 
```

### Install only sensor module

```bash:
pip install pip install mh-z19
```

To use mh-z19, once you need to set up enabling serial port device on the Raspbyerr Pi.
Following [Wiki](https://github.com/UedaTakeyuki/mh-z19/wiki/How-to-Enable-Serial-Port-hardware-on-the-Raspberry-Pi) page might be informative.
Also, please refer [PyPi top page](https://pypi.org/project/mh-z19/) for detail.

## read CO2 Sensor value
```
pi@raspberrypi:~ $ sudo python -m mh_z19 
{'co2': 668}
```

As above, ***sudo*** might be necessary because mh-z19 sensor value is read through serial connection and it request root permission in general.

## Handle sensor value by [PondSlider](https://pypi.org/project/pondslider/) multipurpose sensor handler.

The installed ***mh-z19*** module is correspond the [pondslider](https://pypi.org/project/pondslider/) which is multiple & varsataile sensor handler to save, send and to do other necessary ***something*** with the sensor value.

As an example, we introduce following use case:

- How to save sensor value to SD card as .CSV file.
- How to send sensor value to free Remote Monitoring Service.

### A briaf explanation of pondslider
The pondslider read sensorvalue by ***sensor-handler*** specified, and pass the values to ***value-handlers**** which do something with it.

![PondSlider](https://warehouse-camo.cmh1.psfhosted.org/4a74a04ed15e93c05a7c126b59459d98738a62d9/68747470733a2f2f7261772e67697468756275736572636f6e74656e742e636f6d2f5565646154616b6579756b692f706f6e64736c696465722f6d61737465722f706963732f73732e323031382d31312d30332e31332e35362e31312e706e67)

Both sensor and valule handlers are python module. For more detail of handlers, please refer [this](https://pypi.org/project/pondslider/).

### How to use sensor value to send to server, save to strage, and so on.
This modlue correspond the [pondslider](https://pypi.org/project/pondslider/) which is multiple & varsataile sensor handler to save, send and to do other necessary ***something*** with the sensor value.

In case you choiced ***Full Install*** mentioned above, in other words, you've done ***setup.sh***,
the pondslider and there example handler's are already installed & setup.


### How to save CO2 value on a SD card as a .CSV file.
You can do it with ***save2strage*** value handler which is in ***handlers/value/saver/save2strage***, and configration file to read from mh-z19 sensor and save by save2strage is prepared as ***config.save.toml*** on the mh-z19 installed folder.

On the mh-z19 folder By calling pondslider as follows;

```
sudo python -m pondslider --config config.save.toml
```

Then, ***/home/pi/DATA/co2.csv*** shoud be created and new line will be added for each call.

### How to send CO2 Value to the MONITOR™ Service

The MONITOR™ is a free Remote Monitoring Servcie Developped and by ***me***. I'm berry grad if you use MONITOR™ to watching CO2 Value and give me your ***any*** feedback.
<p>
<img src="pic/2018-11-20.11.23.19.png" width="24%">
<img src="pic/ss.2018-11-20.11.25.43.png" width="75%">
</p>
Sign up as [this](https://monitor.uedasoft.com/docs/UserGuide/Signup.html), Activate View element and get a view_id as [this](https://monitor.uedasoft.com/docs/UserGuide/Value.html).

Then, set your view_id to the configration file by issue ***setid.sh*** command in the mh_z19 installed directory. Let's say your view_id is ***vpgpargj***, then issue ***setid.sh*** command as follows:

```
sudo python -m pondslider
```

Your time-series chart on the MONITOR™ display shoud be updated by the latest CO2 concentration value.

### How to set your Raspberry Pi to send CO2 data to MONITOR™ at 5 minute interval.
You can set it by autostart.sh command in the mh_z19 installed directory as follows:

```
./autostart.sh --on
```

Turn off this as follows:

```
./autostart.sh --off
```

Check current status as follows:


```
./autostart.sh --status
```

### How to send CO2 Value to the ATT M2X.

The Pondslider also support ATT M2X. For detail, please refer [this](https://github.com/UedaTakeyuki/handlers/blob/master/value/sender/send2m2x/README.md) document.

### Q&A
Any questions, suggestions, reports are welcome! Please make [issue](https://github.com/UedaTakeyuki/mh-z19/issues) without hesitation! 

## history
- 0.1.0  2018.09.13  first version self-forked from [slider](https://github.com/UedaTakeyuki/slider).
- 0.2.2  2018.11.19  introduce [pondslider](https://pypi.org/project/pondslider/) and separate this [PyPi](https://pypi.org/project/mh-z19/) package.
