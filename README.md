# Mehrak
A quick, hacky script for displaying images on an RGB Matrix run by a Raspberry PI.

## Prerequisites
This instructions assume that you have installed, and are able to use, [this library](https://github.com/hzeller/rpi-rgb-led-matrix). It also requires a keyboard (or some other programmable button(s) that are able to send individual characters). By default, this script checks for the letters 'a', 'b', and 'c' for the different operations.

## Configuration
There are multiple ways to get the script proper running on startup by the Raspberry PI; this is what worked for us.

1. Create a file `mehrak.sh` in your user's home directory with following contents:
```
#!/bin/sh
sudo python mehrak.py pixil-layer-0.png pixil-layer-1.png pixil-layer-2.png pixil-layer-3.png pixil-gif-drawing.gif
```
It may be necessary to include the full paths to the images instead, e.g. `/home/<username>/pixil-layer-0.png`.

2. Execute the command `sudo chmod 777 mehrak.sh`.

3. Create the file `mehrak.service` in `/etc/systemd/system/` with the following contents:
```
[Unit]
Description=Mehrak
Conflicts=getty@tty1.service

[Service]
Type=simple
User=<insert your username>
WorkingDirectory=/home/<username>/
StandardInput=ttfy-force
ExecStart=/home/kaveh/mehrak.sh

[Install]
WantedBy=multi-user.target
```

4. Enable Mehrak to auto-start on login with `sudo systemctl enable mehrak.service`.

5. When you're ready to run the program properly, do the following steps:

```
Run: sudo raspi-config
Choose option: 1 System Options
Choose option: S5 Boot / Auto Login
Choose option: B2 Console Autologin
Select Finish, and reboot the Raspberry Pi (sudo reboot).
```
Next time the Raspberry PI turns on, it will boot to just a console (no graphical interface). To return to the graphical interface, you must re-run `sudo raspi-config`, select the appropriate settings, and reboot.
