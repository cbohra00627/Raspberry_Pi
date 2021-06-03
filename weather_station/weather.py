#!/usr/bin/env python3

#This file contains the code to draw the weather screen (menu no. 1)
import time
import config

from PIL import Image, ImageDraw, ImageFont
from bme280 import BME280

try:
  from smbus2 import SMBus
except ImportError:
  from smbus import SMBus

try:
  from ltr559 import LTR559
  ltr559 = LTR559()
except ImportError:
  import ltr559

#Set up BME280 weather sensor
bus = SMBus(1)
bme280 = BME280(i2c_dev = bus)

#Function to get the CPU temperature
def get_cpu_temp():

  #Open the file to read temperature
  with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
    temp = f.read()
    temp = int(temp)/1000.0

  return temp

#Function to get the correct temperature of the environment
def get_temp():

  temp = bme280.get_temperature()
  cpu_temp = get_cpu_temp()

  #Calculate the correct temperature
  factor = 2.25
  temp = temp - (cpu_temp - temp)/factor

  return round(temp, 1)

#Function to get the correct relative humidity in the  environment
def get_humidity():

  raw_temp = bme280.get_temperature()
  raw_humidity = bme280.get_humidity()
  corr_temp = get_temp()

  #Calculate the correct humidity
  dewpoint = raw_temp - (100 - raw_humidity)/5
  corr_humidity = 100 - 5*(corr_temp - dewpoint)

  return min(100, round(corr_humidity, 1))

#Function to describe temperature
def des_temperature(temperature):

  if temperature > 35:
    description = "HOT"
    icon_path = "icons/hot.png"
    color = (255,0,0)
  elif temperature <= 35 and temperature > 25:
    description = "NORMAL"
    icon_path = "icons/normal.png"
    color = (255,265,0)
  else:
    description = "COLD"
    icon_path = "icons/cold.png"
    color = (0,255,255)

  unit = "C"

  return description, icon_path, unit, color

#Function to describe pressure
def des_pressure(pressure):

  if pressure < 970:
    description = "STORM"
    icon_path = "icons/storm.png"
    color = (139,0,139)
  elif pressure >= 970 and pressure < 990:
    description = "RAIN"
    icon_path = "icons/rain.png"
    color = (0,0,255)
  elif pressure >= 990 and pressure < 1010:
    description = "CHANGE"
    icon_path = "icons/change.png"
    color = (65,105,225)
  elif pressure >= 1010 and pressure < 1030:
    description = "FAIR"
    icon_path = "icons/fair.png"
    color = (123,104,238)
  else:
    description = "DRY"
    icon_path = "icons/dry.png"
    color = (255,215,0)

  unit = "hPa"

  return description, icon_path, unit, color

#Function to describe relative humidity
def des_humidity(humidity):

  if humidity > 40 and humidity < 60:
    description = "GOOD"
    icon_path = "icons/good.png"
    color = (65,105,225)
  else:
    description = "BAD"
    icon_path = "icons/bad.png"
    color = (0,0,0)

  unit = "%"

  return description, icon_path, unit, color

#Function to describe light intensity
def des_light(light):

  if light < 50:
    description = "DARK"
    icon_path = "icons/dark.png"
    color = (0,0,0)
  elif light >= 50 and light < 100:
    description = "DIM"
    icon_path = "icons/dim.png"
    color = (184,134,11)
  elif light >= 100 and light < 500:
    description = "LIGHT"
    icon_path = "icons/light.png"
    color = (255,215,0)
  else:
    description = "BRIGHT"
    icon_path = "icons/bright.png"
    color = (255,255,0)

  unit = "Lux"

  return description, icon_path, unit, color

#Function to draw the weather screen
def weather_screen():

  #New canvas to draw weather screen
  img = Image.new('RGBA', (config.WIDTH,config.HEIGHT-15), (240,230,140))
  draw = ImageDraw.Draw(img)

  #Get the data
  temperature = get_temp()
  humidity = get_humidity()
  pressure = int(bme280.get_pressure())
  light = int(ltr559.get_lux())

  details = {"temperature": des_temperature(temperature), "humidity": des_humidity(humidity), "pressure": des_pressure(pressure), "light": des_light(light)}


  #FONTS
  #For values
  value_font = ImageFont.truetype("fonts/OpenSans-Regular.ttf", 9)
  value_font_color = (0,0,0)

  #For units
  unit_font = ImageFont.truetype("fonts/OpenSans-Semibold.ttf", 9)
  unit_font_color = (0,0,0)

  #For descriptions
  des_font = ImageFont.truetype("fonts/OpenSans-Bold.ttf", 9)
  des_font_color = (255,255,255)


  #Size for the sections canvas
  canvas_x = 66
  canvas_y = 30

  #TEMPERATURE
  #New canvas for the temperature section
  img_temp = Image.new('RGBA', (canvas_x, canvas_y), (0,0,0,0))
  draw_temp = ImageDraw.Draw(img_temp)

  #Paste the temperature icon
  temp_icon = Image.open(details["temperature"][1])
  img_temp.paste(temp_icon, (0,0), mask = temp_icon)

  #Temperature Value
  temp_value = str(temperature)
  (temp_value_x, temp_value_y) = draw.textsize(temp_value, value_font)
  draw_temp.text((canvas_x-temp_value_x, 0), temp_value, font = value_font, fill = value_font_color)

  #Temperature unit
  (temp_unit_x, temp_unit_y) = draw_temp.textsize(details["temperature"][2], unit_font)
  draw_temp.text((canvas_x-temp_unit_x, 10), details["temperature"][2], font = unit_font, fill = unit_font_color)

  #Temperature description
  (temp_des_x, temp_des_y) = draw_temp.textsize(details["temperature"][0], des_font)
  draw_temp.rectangle((canvas_x-temp_des_x, 20+1, canvas_x, 30), fill = details["temperature"][3])
  draw_temp.text((canvas_x-temp_des_x, 20), details["temperature"][0], font = des_font, fill = des_font_color)

  #HUMIDITY
  #New canvas for the humidity section
  img_humidity = Image.new('RGBA', (80,30), (0,0,0,0))
  draw_humidity = ImageDraw.Draw(img_humidity)

  #Paste the humidity icon
  humidity_icon = Image.open(details["humidity"][1])
  img_humidity.paste(humidity_icon, (0,0), mask = humidity_icon)

  #Humidity Value
  humidity_value = str(humidity)
  (humidity_value_x, humidity_value_y) = draw_humidity.textsize(humidity_value, value_font)
  draw_humidity.text((canvas_x-humidity_value_x, 0), humidity_value, font = value_font, fill = value_font_color)

  #Humidity unit
  (humidity_unit_x, humidity_unit_y) = draw_humidity.textsize(details["humidity"][2], unit_font)
  draw_humidity.text((canvas_x-humidity_unit_x, 10), details["humidity"][2], font = unit_font, fill = unit_font_color)

  #Humidity description
  (humidity_des_x, humidity_des_y) = draw_humidity.textsize(details["humidity"][0], des_font)
  draw_humidity.rectangle((canvas_x-humidity_des_x, 20+1, canvas_x, 30), fill = details["humidity"][3])
  draw_humidity.text((canvas_x-humidity_des_x, 20), details["humidity"][0], font = des_font, fill = des_font_color)

  #PRESSURE
  #New canvas for the pressure section
  img_pressure = Image.new('RGBA', (80,30), (0,0,0,0))
  draw_pressure = ImageDraw.Draw(img_pressure)

  #Paste the temperature icon
  pressure_icon = Image.open(details["pressure"][1])
  img_pressure.paste(pressure_icon, (0,0), mask = pressure_icon)

  #Pressure Value
  pressure_value = str(pressure)
  (pressure_value_x, pressure_value_y) = draw_pressure.textsize(pressure_value, value_font)
  draw_pressure.text((canvas_x-pressure_value_x, 0), pressure_value, font = value_font, fill = value_font_color)

  #Pressure unit
  (pressure_unit_x, pressure_unit_y) = draw_pressure.textsize(details["pressure"][2], unit_font)
  draw_pressure.text((canvas_x-pressure_unit_x, 10), details["pressure"][2], font = unit_font, fill = unit_font_color)

  #Pressure description
  (pressure_des_x, pressure_des_y) = draw_pressure.textsize(details["pressure"][0], des_font)
  draw_pressure.rectangle((canvas_x-pressure_des_x, 20+1, canvas_x, 30), fill = details["pressure"][3])
  draw_pressure.text((canvas_x-pressure_des_x, 20), details["pressure"][0], font = des_font, fill = des_font_color)

  #LIGHT
  #New canvas for the light section
  img_light = Image.new('RGBA', (80,30), (0,0,0,0))
  draw_light = ImageDraw.Draw(img_light)

  #Paste the light icon
  light_icon = Image.open(details["light"][1])
  img_light.paste(light_icon, (0,0), mask = light_icon)

  #Light Value
  light_value = str(light)
  (light_value_x, light_value_y) = draw_light.textsize(light_value, value_font)
  draw_light.text((canvas_x-light_value_x, 0), light_value, font = value_font, fill = value_font_color)

  #Light unit
  (light_unit_x, light_unit_y) = draw_light.textsize(details["light"][2], unit_font)
  draw_light.text((canvas_x-light_unit_x, 10), details["light"][2], font = unit_font, fill = unit_font_color)

  #Light description
  (light_des_x, light_des_y) = draw_light.textsize(details["light"][0], des_font)
  draw_light.rectangle((canvas_x-light_des_x, 20+1, canvas_x, 30), fill = details["light"][3])
  draw_light.text((canvas_x-light_des_x, 20), details["light"][0], font = des_font, fill = des_font_color)

  #Paste all the images on the main image
  img.paste(img_temp, (8,1), mask = img_temp)
  img.paste(img_humidity, (82,1), mask = img_humidity)
  img.paste(img_pressure, (8,33), mask = img_pressure)
  img.paste(img_light, (82,33), mask = img_light)

  return img
