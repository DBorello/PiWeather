# PiWeather
Analog weather station powered by a Raspberry Pi

## Dependencies
* python-requests
* pigpio

   

### Deployment

    #Install pigpio
    cd ~
    wget abyz.co.uk/rpi/pigpio/pigpio.zip
    unzip pigpio.zip
    cd PIGPIO
    make
    sudo make install
    
    #Pull repository
    cd ~
    git pull https://github.com/DBordello/PiWeather.git
    
    #Setup service
    sudo ln /home/pi/PiWeather/PiWeather.service /etc/systemd/system/PiWeather.service
    sudo systemctl enable PiWeather.service
    sudo ln /home/pi/PiWeather/pigpiod.service /etc/systemd/system/pigpiod.service
    sudo systemctl enable pigpiod.service 

### /boot/PiWeather.ini
    [General]
    LogLevel = INFO

    [WUnderground]
    apiKey = {{apiKey}}
    Station = KORPHILO13