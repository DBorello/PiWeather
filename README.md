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
    AutoSkip* = 1

    #Login as root
    #Advanced -> Swap -> Disable

    bash <(curl -s https://raw.githubusercontent.com/DBorello/PiWeather/master/Install.sh)
