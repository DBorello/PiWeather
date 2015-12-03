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
    
### /boot/PiWeather.ini
    [WUnderground]
    apiKey = {{apiKey}}
    Station = KORPHILO13