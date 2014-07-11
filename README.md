pin-monitor
===========

Monitor GPIO on Raspberry Pi and send an email when GPIO goes low.

I wrote this to because: 
 1. I wanted to try writing something in Python 
 2. because I wanted to build something on the Raspberry Pi.

Anyway, first program in Python so if I made some fundamental mistakes or if it looks awfully like C# in places, so be it.

Note: I tested this on Arch linux ARM 
      
       After installing Arch on your SD card:
         1. pacman -Sy base-devel python pip
         2. pip install RPi.GPIO 
       
       You will also want to configure the NTP using timedatectl like so (using your time zone):
         1. timedatectl set-timezone Europe/Dublin
         2. nano /etc/ntp.conf
             server 0.ie.pool.ntp.org
             server 1.ie.pool.ntp.org
             server 2.ie.pool.ntp.org
         3. timedatectl set-ntp yes 

Using the RPi.GPIO library the service monitors a given pin on the Pi.
When that pin goes low for more than 1 second then an email will be sent using the values obtained from a configuration file
(pin-monitor.conf), i.e. host,sender,recipients etc. Depending on the use_camera value in the config file the email cam also
include a JPEG from an IP camera which is attached to the email.
The IP address of the camera is also taken from the config file as is the unique url used to request the JPEG.
A sample pin-monitor.conf file is included in the repo and is called demo_pin-monitor.conf.

       To run the service copy the pin-monitor.service file into the /usr/lib/systemd/system directory as root and then type
         1. systemctl start pin-monitor
         2. systemctl enable pin-monitor (To have service start a boot)
         3. systemctl status pin-moniotr (to see if service is running and/or if it has thrown any errors)
