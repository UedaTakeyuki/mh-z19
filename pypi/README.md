# mh-z19
Read CO2 concentration from mh-z19 sensor

![MH-Z19](https://camo.githubusercontent.com/8456a67ab97a13866d928d3a14dff59a57cdeccb/68747470733a2f2f63616d6f2e716969746175736572636f6e74656e742e636f6d2f613237306466313136326564356333626639393638623234303634623931656564306466636331312f3638373437343730373333613266326637313639363937343631326436393664363136373635326437333734366637323635326537333333326536313664363137613666366536313737373332653633366636643266333032663334333633353334333432663331333533373339363633393634363232643330363633343330326433373336363533383264333033353636333332643339333933333631333233343633333433373634333133383265373036653637)

## install
```
pip install mh-z19
```
## installs
[![Downloads](https://pepy.tech/badge/mh-z19)](https://pepy.tech/project/mh-z19)
[![Downloads](https://pepy.tech/badge/mh-z19/month)](https://pepy.tech/project/mh-z19)
[![Downloads](https://pepy.tech/badge/mh-z19/week)](https://pepy.tech/project/mh-z19)

## how to use
Use as python script.
```
pi@raspberrypi:~/mh-z19/pypi $ sudo python -m mh_z19
{'co2': 500}
```

Import module and call read()
```
pi@raspberrypi:~/mh-z19/pypi $ sudo python
Python 2.7.13 (default, Nov 24 2017, 17:33:09) 
[GCC 6.3.0 20170516] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import mh_z19
>>> mh_z19.read()
{'co2': 477}
>>> 
```

The ***sudo*** might be necessary because mh_z19 module use Serial.

The differences of the interface between each Raspberry Pi model are resolved inside this module. For example, serial device name is difference between Raspberry Pi 3 and older model, but mh-z19 module automatically detect the model and read from appropriate serial device.

To use mh-z19, once you need to set up enabling serial port device on the Raspberry Pi.
Following [Wiki](https://github.com/UedaTakeyuki/mh-z19/wiki/How-to-Enable-Serial-Port-hardware-on-the-Raspberry-Pi) page might be informative.

## cabling
Connect RPi & mh-z19 as:

- 5V on RPi and Vin on mh-z19
- GND(0v) on RPi and GND on mh-z19
- TxD and RxD are connected to cross between RPi and mh-z18 

Followings are example of cabling, but you can free to use other 5v and 0v Pin on the RPi. 

![Cabling](https://camo.githubusercontent.com/3cd4c1b482ea902b7e66dca13d4260193c831a63/68747470733a2f2f63616d6f2e716969746175736572636f6e74656e742e636f6d2f313132616435666534316338326131363637316432383832303730333834313039633838363063632f36383734373437303733336132663266373136393639373436313264363936643631363736353264373337343666373236353265373333333265363136643631376136663665363137373733326536333666366432663330326633343336333533343334326633303338333233383333333033313334326433363338363433323264363333333634363532643331333633343334326433373633333836343339363233373632333633323636363432653661373036353637)

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

## Watch CO2 concentration on your browser 
<img src="https://github.com/UedaTakeyuki/mh-z19/raw/master/pic/2018-11-20.11.23.19.png" width="24%">

[MONITOR™](https://monitor3.uedasoft.com) is a free Remote Monitoring Service to show latest data on the web. You can see the current CO2 concentration value measured by your MH-Z19 device on your smartphone. For detail, please refer this [blog](https://monitorserviceatelierueda.blogspot.com/2018/11/how-to-measure-room-co2-concentration.html). 


## Calibration, Detection range settings, and ABC(Automatic Baseline Correction) logic on/off.
Features about calibration (both MH-Z19 & MH-Z19B), detection range change (MH-Z19B) and ABC logic on/off(MH-Z19B) are implemented at version 0.2.1 or later.

I'm afraid I've just only implemented these without test due to lack necessary devices and apparatus for the test, fx: standard concentration CO2 gas, also MH-Z19B module.
If you have these devices or apparatus and try to use these functions generously, I'm really appreciate your [issue report](https://github.com/UedaTakeyuki/mh-z19/issues) regardless result were positive or negative.

For detail please refer this [wiki](https://github.com/UedaTakeyuki/mh-z19/wiki/CALIBRATION-&-detection-range).

## Undocumented response values of 0x86 command.
The [Revspace/MHZ19](https://revspace.nl/MHZ19#Command_0x86_.28read_concentration.29) shows values undocumented on the official datasheets([MH-Z19](https://www.winsen-sensor.com/d/files/PDF/Infrared%20Gas%20Sensor/NDIR%20CO2%20SENSOR/MH-Z19%20CO2%20Ver1.0.pdf), [MH-Z19B](https://www.winsen-sensor.com/d/files/MH-Z19B.pdf)). In accordance with this, **--all** option add these values in the return json value as follows:

```bash:
sudo python -m mh_z19 --all
{"SS": 232, "UhUl": 10752, "TT": 61, "co2": 818, "temperature": 21}

sudo python3 -m mh_z19 --all
{"TT": 61, "co2": 807, "SS": 232, "temperature": 21, "UhUl": 10752}
```

or call **read_all()** function as follows:

```
>>> import mh_z19
>>> mh_z19.read_all()
{'SS': 232, 'UhUl': 10738, 'TT': 61, 'co2': 734, 'temperature': 21}
>>> 
```

## Use specific serial device.
In case you should use specific serial device insted of Raspberry Pi default serial device which this library automatically select, for example in case to need to use /dev/ttyUSB0 for **FT232 usb-serial converter** as [issue#12](https://github.com/UedaTakeyuki/mh-z19/issues/12), you can specify serial device by **--serial_device** option as follows:

```
sudo python -m mh_z19 --serial_device /dev/ttyUSB0
```

## How to use without root permission.
See this [wiki](https://github.com/UedaTakeyuki/mh-z19/wiki/How-to-use-without-root-permission.).

## How to use in your program.
See this [wiki](https://github.com/UedaTakeyuki/mh-z19/wiki/How-to-use-in-your-program.).

## PWM support.
See this [wiki](https://github.com/UedaTakeyuki/mh-z19/wiki/PWM-support.).

## In case you can't get the value.
Even if cabling seems no problem and uart seems to be prepateted well but you can't get sensor value. As [nincube8](https://github.com/nincube8) suggested that the [pull up](https://github.com/UedaTakeyuki/mh-z19/issues/22#issuecomment-683393350) by [1-5kΩ register](https://github.com/UedaTakeyuki/mh-z19/issues/26#issuecomment-744039360) can be working solution. Thank you [nincube8](https://github.com/nincube8)!

## Q&A
The forum is avai at [here](https://groups.google.com/g/mh_z19-users). Any questions, suggestions, reports are welcome!

## Blog
- [How to Measure ROOM CO2 concentration with 20$ sensor "MH-Z19" and Raspberry Pi.](https://monitorserviceatelierueda.blogspot.com/2018/11/how-to-measure-room-co2-concentration.html)
- [Monitoring all over the world with 3G Network for not more than 10$ monthly payment.](https://monitorserviceatelierueda.blogspot.com/2018/10/continuous-monitoring-all-over-world.html)
- [How to make shareable SD card by Raspberry Pi & PC.](https://monitorserviceatelierueda.blogspot.com/2018/09/how-to-make-shareable-sd-card-by.html)

## References

- [MH-H19B DataSheet version 1.5](https://www.winsen-sensor.com/d/files/MH-Z19B.pdf)
- [MH-H19 DataSheet version 1.0](https://www.winsen-sensor.com/d/files/PDF/Infrared%20Gas%20Sensor/NDIR%20CO2%20SENSOR/MH-Z19%20CO2%20Ver1.0.pdf)
- [MH-H19B DataSheet version 1.0](https://www.winsen-sensor.com/d/files/infrared-gas-sensor/mh-z19b-co2-ver1_0.pdf)
- [RevSpace](https://revspace.nl/MHZ19#Setting_the_measurement_range)

## history
- 0.1.1  2018.11.05  first version self-forked from [slider](https://github.com/UedaTakeyuki/slider).
- 0.1.3  2018.11.06  fix Readme.
- 0.1.4  2018.11.15  revise Readme.
- 0.1.6  2018.11.29  revise Readme.
- 0.2.1  2019.01.18  add followings without test (sorry)
                       abc_on(), abc_off(), span_point_calibration(),
											 xero_point_calibration(), detection_range_5000(),
											 detection_range_2000(), checksum()
- 0.3.5  2019.01.22  Both Python2 & Python3 support
- 0.3.6  2019.01.22  Merge [Pull Request #3](https://github.com/UedaTakeyuki/mh-z19/pull/3) & [Pull Request #4](https://github.com/UedaTakeyuki/mh-z19/pull/4). Thanks [David](https://github.com/kostaldavid8)!
- 0.3.7  2019.02.25  Add --all option which requested as [issue#5](https://github.com/UedaTakeyuki/mh-z19/issues/5), thanks [Rafał](https://github.com/rzarajczyk)!
- 0.3.8  2019.04.16  Merge [Pull Request #7](https://github.com/UedaTakeyuki/mh-z19/pull/7). Thanks [Alexander](https://github.com/belibak)!
- 0.3.8.5  2019.04.21  Merge [Pull Request #9](https://github.com/UedaTakeyuki/mh-z19/pull/9). Thanks [WO15](https://github.com/WO15)!
- 0.3.9  2019.05.06  Revise the serial port selection logic. Support using **PL011** uart on Raspberry Pi **Model 3 and Zero W** which is selected by setting dtoverlay=**pi3-miniuart-bt** or dtoverlay=**pi3-disable-bt**. Thanks **片岡さん** for your kindly [report](https://qiita.com/yukataoka/items/a3b4065e8210b8f372ff) including this issue!
- 0.4.1 2019.08.11 Add --serial_device option as solution of [issue#12](https://github.com/UedaTakeyuki/mh-z19/issues/12). Thanks [Actpohomoc](https://github.com/Actpohomoc) and [TBR-BRD](https://github.com/TBR-BRD)!
- 0.5.1 2020.05.16 Add **--serial_console_untouched** option to support **execution without sudo** asked as [issue#17](https://github.com/UedaTakeyuki/mh-z19/issues/17). Thanks [ralphbe91](https://github.com/ralphbe91)!
- 0.5.2 2020.06.30 Update the link for datasheet of MH-Z19B from version 1.0 to version 1.5 based be pointed it out as [issue#18](https://github.com/UedaTakeyuki/mh-z19/issues/18). Thanks [WO15](https://github.com/WO15)!
- 0.6.1 2020.07.07 Add **--detection_range_10000** option to support **Set 0~10000ppm detection range** asked as [issue#19](https://github.com/UedaTakeyuki/mh-z19/issues/19). Thanks [WO15](https://github.com/WO15)!
- 0.6.3 2020.08.27 Fix [issue#21](https://github.com/UedaTakeyuki/mh-z19/issues/21). Thanks [idegre](https://github.com/idegre)!
- 3.0.0 2021.02.05 [PWM support](https://github.com/UedaTakeyuki/mh-z19/wiki/PWM-support.).
- 3.0.1 2021.02.17 Fix a degradation of not running with python3. Thank you **Masahiko OHKUBO** san for your report.
- 3.0.2 2021.03.25 Fix to support RPi4 correctly as [issue#29](https://github.com/UedaTakeyuki/mh-z19/issues/29). Thanks [iperniaf](https://github.com/iperniaf)!
- 3.0.3 2021.11.08 Fix [issue#35](https://github.com/UedaTakeyuki/mh-z19/issues/35). Thanks [false](https://github.com/false-git)!