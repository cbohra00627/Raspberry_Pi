# Weather Station  
It is a Raspberry Pi based weather station. It shows the basic parameters of environment like the temperature (C), relative humidity (%), pressure (hPa) and light intensity (Lux). This project uses Pimoroni Enviro board for this purpose. It is basically designed for indoor monitoring. It has various onboard sensors:
1. BME280 temperature, pressure and humidity sensor
2. LTR559 light and proximity sensor
3. MEMS I2S digital microphone
4. 0.96'' color LCD (160x80)  
  
![Enviro Front View](https://github.com/cbohra00627/Images/blob/main/weather_station/phatfront.jpg) 
![Enviro Back View](https://github.com/cbohra00627/Images/blob/main/weather_station/phatback.jpg)  
  
## Installing the libraries
To install the required python libraries for the enviro board, visit this [page](https://github.com/pimoroni/enviroplus-python).  
Or simply just run the following command from the terminal:  
```curl -sSL https://get.pimoroni.com/enviroplus | bash```  
It will insatll all the necesarry required to run the board and some examples with it.  

  
The Board can directly be stacked on the Raspberry Pi  
  
![Enviro Board stacked over Raspberry Pi showing 'Hellow World!'](https://github.com/cbohra00627/Images/blob/main/weather_station/hello.jpg)  
  
Run the "lcd.py" file from Pimoroni/enviroplus/examples to check if the board is working or not.  
  
## Running the project
To run this project just download this folder to your Raspberry Pi.  
Stack the Enviro Board on the Raspberry Pi as shown above.  
Then run the "main.py" file using the following command:  
```python3 -B main.py```  
It is necessary to use Python version 3 for this project otherwise it will not work.  
  
After running the above given command, the screen will turn on and it will show the following on the screen:  
  
![Main Screen](https://github.com/cbohra00627/Images/blob/main/weather_station/mainscreen.jpg)  
  
There are two options on this screen:  
1. Weather Station - It shows the readings from the on-board sensors.
2. World Weather - It uses APIs to fetch 3 day weather forecast of any place if it is provided the ISO country code and the zip code of that place. After giving the information, it will show the weather data (max and min temperatures and max wind speed) of that place.
  
It uses the APIs offered by [Zippopotamus](http://www.zippopotam.us/) to get the longitude and the latitude of the place using the country code and the zip code. To see the supported countries, visit the site.  
Enter the desired option number on the terminal and hit enter.  
  
1. Weather Station  
  
![Weather Station Screen](https://github.com/cbohra00627/Images/blob/main/weather_station/screen1.jpg)  
  
2. World Weather  
  
![World Weather Screen](https://github.com/cbohra00627/Images/blob/main/weather_station/screen2.jpg)  
  
Here is a video of the hardware working (Click the link to go to youtube):  
  
[![Youtube Video Link (https://youtu.be/nrshD7Tk3fY)](https://github.com/cbohra00627/Images/blob/main/weather_station/video.jpg)](https://youtu.be/nrshD7Tk3fY)
