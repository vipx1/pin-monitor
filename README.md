pin-monitor
===========

Monitor GPIO on Rasberry Pi and send an email when GPIO goes low.

I wrote this to because: 
 1. I wanted to try writing something in Python 
 2. because I wanted to build something on the Raspberry Pi.

Anyway, first program in Python so if I made some fundamental mistakes or if it looks awfully like C# in places, so be it.

Note: I tested this on Arch linux ARM 

After installing Arch on your SD card:

pacman -Sy base-devel python pip

pip install RPi.GPIO 

You will also want to configure the NTP using timedatectl like so :

timedatectl set-timezone Europe/Dublin 

nano /etc/ntp.conf 

timedatectl set-ntp yes 

Using the RPi.GPIO library the service monitors a given pin on the Pi. When that pin goes low for more than 1 second then an email will be sent using the values obtained from a configuration file (emailer.conf), i.e. host,sender,recipients etc. Depending on the use_camera value in the emailer.conf file the email cam also include a JPEG from an IP camera which is attached to the email. The IP address of the camera is also taken from the email.conf as is the unique url used to request the JPEG.
A sample emailer.conf file is included in the repo and is called demo_emailer.conf.
