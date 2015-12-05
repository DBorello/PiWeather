# PiWeather
Analog weather station powered by a Raspberry Pi

## Dependencies
* python3
* python-requests
* pigpio

   

### Deployment
    #Write DietPi Image, edit dietpi.txt
    Ethernet_Enabled=0
    Wifi_Enabled=1
    Wifi_SSID=FuzonWifi
    Wifi_KEY=MyAccessKey

    #Login as root
    #Advanced -> Swap -> Disable

    #Install dependencies
    apt-get -y install build-essential git python3 python3-requests

    #Install pigpio
    cd ~
    wget abyz.co.uk/rpi/pigpio/pigpio.zip
    unzip pigpio.zip
    cd PIGPIO
    make
    make install
    
    #Pull repository
    cd ~
    git clone https://github.com/DBordello/PiWeather.git
    
    #Setup service 
    cp /root/PiWeather/PiWeather.service /etc/systemd/system/PiWeather.service
    systemctl enable PiWeather.service
    cp /root/PiWeather/pigpiod.service /etc/systemd/system/pigpiod.service
    systemctl enable pigpiod.service
    cp /root/PiWeather/reverse-ssh.service /etc/systemd/system/reverse-ssh.service
    systemctl enable reverse-ssh.service

    #Setup remote access
    ssh-keygen -t rsa -N '' -f /root/.ssh/reverse-ssh
    nano -w /etc/systemd/system/reverse-ssh.service# Edit ssh port in /etc/systemd/system/reverse-ssh.service
    cat /root/.ssh/reverse-ssh.pub
    #Copy key to reverse /home/vmuser/.ssh/authorized_keys
    echo "ssh-rsa AAAAB3NzaC1yc2EAAAABJQAAAIEAyktApU0/6Ny9pUj3hcOeacVl29yjIaLjPx+R+PPhy/cv9fsnRTj16Vrayfsf78OlBoz+YMSPLSuAMolZiP1leb7RsA2WR3MaSIHtxplatwjNJ84pfAkwbKQPmBRdunPZSis2lkRs64dutiD9m0oPgn1cOO0e8Eh1QSc5ThT6Nyc= VM Key" >> /root/.ssh/authorized_keys

    #Setup FS for read-only
    echo "wc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=noop rootwait fastboot noswap ro" > /boot/cmdline.txt
    rm -rf /var/lib/dhcp/ /var/run /var/spool /var/lock
    ln -s /tmp /var/lib/dhcp; ln -s /tmp /var/run; ln -s /tmp /var/spool; ln -s /tmp /var/lock
    sed -ie '/^\/dev\/mmcblk0p/ s/defaults,noatime/defaults,noatime,ro/' /etc/fstab
    echo "alias ro='mount -o remount,ro /'" >> /etc/bash.bashrc
    echo "alias rw='mount -o remount,rw /'" >> /etc/bash.bashrc
    echo "alias rob='mount -o remount,ro /boot'" >> /etc/bash.bashrc
    echo "alias rwb='mount -o remount,rw /boot'" >> /etc/bash.bashrc

### /boot/PiWeather.ini
    [General]
    LogLevel = INFO

    [WUnderground]
    apiKey = {{apiKey}}
    Station = KORPHILO13