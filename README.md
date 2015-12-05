# PiWeather
Analog weather station powered by a Raspberry Pi

## Dependencies
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
    ln /root/PiWeather/PiWeather.service /etc/systemd/system/PiWeather.service
    systemctl enable PiWeather.service
    ln /root/PiWeather/pigpiod.service /etc/systemd/system/pigpiod.service
    systemctl enable pigpiod.service

### /boot/PiWeather.ini
    [General]
    LogLevel = INFO

    [WUnderground]
    apiKey = {{apiKey}}
    Station = KORPHILO13