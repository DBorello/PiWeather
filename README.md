# PiWeather
Analog weather station powered by a Raspberry Pi

* Write DietPi Image (Directions for v115)
* Edit /boot/dietpi.txt

    Ethernet_Enabled=0
    Wifi_Enabled=1
    Wifi_SSID=FuzonWifi
    Wifi_KEY=MyAccessKey
    Swapfile_Size=0
    AUTO_AutoLogin=1
    AUTO_SkipLicensePrompt=1
    AUTO_DietpiSoftware_SkipUpdateRebootPrompt=1
    AUTO_DietpiSoftware_SkipQuestions=1
    AUTO_DietpiSoftware_SkipUsbDrive=1
    AUTO_DietpiSoftware_IgnoreErrors=1
    AUTO_Install_Index=1
    
    AUTO_Timezone=	America/Los_Angeles
    AUTO_Locale=en_us
    AUTO_KeyboardLayout=us
    
    AUTO_CustomScriptURL=https://raw.githubusercontent.com/DBorello/PiWeather/master/Install.sh

* SSH from local host.  Change /etc/systemd/system/reverse-ssh.service port
* Add cat /root/.ssh/reverse-ssh.pub to reverse host ~/.ssh/authorized_keys
