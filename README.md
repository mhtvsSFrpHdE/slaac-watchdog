# slaac-watchdog
![IPv6_one_does_not_simply](https://github.com/user-attachments/assets/8948e7a6-1c3a-4c29-aa8f-4bb0573b844c)
## How to use
### Windows
1. Install Python for example `3.10.11`, it's not necessary to add to PATH
1. Run `windows\install.bat`, follow instructions on screen
### Linux
1. Install Python 3, and `python3` available as a command
1. `cd slaac-watchdog/linux`
1. Use text editor open `slaac-watchdog.service`
1. Edit `ExecStart=` to full path of `slaac-watchdog/linux/daemon.sh`
1. Edit `WorkingDirectory` to full path of directory where `daemon.sh` is stored
1. Save file
1. `sudo cp slaac-watchdog.service /etc/systemd/system/slaac-watchdog.service`
1. `sudo systemctl enable slaac-watchdog.service`
1. `sudo systemctl start slaac-watchdog.service`
1. `sudo systemctl status slaac-watchdog.service`
## What is this
Each time a device connected to a SLAAC IPv6 network, it will request a subnet prefix from router,  
then generate its own address with in this subnet range.  
However, if later router send another subnet prefix to device,  
and this subnet prefix is different from previous one, things becomes struggle.  
Mainstream operating systems (Windows, Linux) will not consider previous subnet prefix as obsolete,  
the result is you have multiple IPv6 address in different subnet prefix.

This situation often happens on manually reconnecting to ISP, like reboot your router.  
Certain ISP don't consider your obsolete IPv6 address is valid,  
you can't use them to browse internet, or receive incoming connections.  
The worse is they also allocate you different subnet prefix on each reconnect.

With Windows as an example, now router is just rebooted,  
device will have 4 IPv6 address, two for SLAAC (RFC 4862),  
two for Privacy Extension (RFC 4941).  
2 of 4 are belongs to previous subnet, which is obsolete of your ISP.  
If you try to browse internet and Windows picked obsolete IPv6 address as outgoing,  
the connection will fail, and you may lose IPv6 internet for a while,  
until your obsolete address naturally disappears.

This will also confuse your DDNS software because they may also pick obsolete IPv6 address  
and set to domain name, but these addresses are not able to receive incoming connections.

slaac-watchdog provide you tools to automatically remove obsolete IPv6 address  
on subnet prefix change, to improve overall network stability for  
browse internet, receive incoming connections, or DDNS your IPv6 address to domain.
