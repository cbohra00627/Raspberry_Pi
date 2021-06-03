#!/bin/usr/env python3

#This file contains code for the city weather screen (menu no. 2)
import config
import urllib.request
import json
from PIL import Image, ImageDraw, ImageFont

#Function to draw the get codes screen
def get_codes():

  #New canvas to draw the get codes screen
  img = Image.new('RGBA', (config.WIDTH,config.HEIGHT-15), color = (255,255,0))
  draw = ImageDraw.Draw(img)

  #Font Settings
  font = ImageFont.truetype("fonts/OpenSans-Semibold.ttf", 13)
  font_color = (0,0,0)

  #Draw the text
  text = "Please enter the correct\ncountry code and ZIP\ncode on the terminal."
  draw.multiline_text((0,0), text, font = font, spacing = -3,  fill = font_color)

  return img

#Function to get the city longitude and latitude
def get_city_coordinates(country_code, zip_code):

  URL = "http://api.zippopotam.us/" + country_code + "/" + zip_code

  weburl = urllib.request.urlopen(URL)

  #Read raw data from the URL
  raw_data = weburl.read()

  #Convert the raw data to json format
  json_data = json.loads(raw_data)

  longitude = json_data["places"][0]["longitude"]
  latitude = json_data["places"][0]["latitude"]

  return longitude, latitude

#Function to describe weather in city forecast
def des_weather(weather):

  if weather == "clear":
    icon_path = "icons/clear.jpg"
  elif weather == "pcloudy":
    icon_path = "icons/pcloudy.jpg"
  elif weather == "cloudy":
    icon_path = "icons/cloudy.jpg"
  elif weather == "rain":
    icon_path = "icons/rain.jpg"
  elif weather == "snow":
    icon_path = "icons/snow.jpg"
  elif weather == "ts":
    icon_path = "icons/ts.jpg"
  elif weather == "tsrain":
    icon_path = "icons/tsrain.jpg"

  return icon_path

#Function to describe the max wind speed (km/h) in city forecast
def des_wind(wind):

  if wind == 1:
    speed = "<1"
  elif wind == 2:
    speed = "1-12"
  elif wind == 3:
    speed = "12-29"
  elif wind == 4:
    speed = "29-39"
  elif wind == 5:
    speed = "39-62"
  elif wind == 6:
    speed = "62-88"
  elif wind == 7:
    speed = "88-117"
  elif wind == 8:
    speed = ">117"

  return speed

#Function to get the city forecasts
def get_city_forecast(longitude, latitude):

  URL = "https://www.7timer.info/bin/api.pl?lon=" + longitude + "&lat=" + latitude + "&product=civillight&output=json"

  weburl = urllib.request.urlopen(URL)

  #Read the raw data from the URL
  raw_data = weburl.read()

  #Convert the raw data to json format
  json_data = json.loads(raw_data)

  day0 = json_data["dataseries"][0]
  day1 = json_data["dataseries"][1]
  day2 = json_data["dataseries"][2]

  return day0, day1, day2

#Function to draw each day separately
def draw_day(day):

  #Dimensions of a day section
  day_width = 54
  day_height = 65

  #New canvas to draw day sections
  img = Image.new('RGBA', (day_width,day_height), color = (0,0,0,0))
  draw = ImageDraw.Draw(img)

  day_icon_path = des_weather(day["weather"])
  wind_max = des_wind(day["wind10m_max"])

  #Draw the day weather icon
  day_icon = Image.open(day_icon_path)
  img.paste(day_icon, (0,0))

  #Date font settings
  date_font = ImageFont.truetype("fonts/OpenSans-Bold.ttf", 9)
  date_font_color = (255,255,255)

  #Data font settings
  data_font = ImageFont.truetype("fonts/OpenSans-Semibold.ttf", 9)
  data_font_color = (0,0,0)

  #Draw date
  date = str(day["date"])[6:8] + "/" + str(day["date"])[4:6] + "/" + str(day["date"])[0:4]
  (date_x,date_y) = draw.textsize(date, date_font)
  x = int((day_width - date_x)/2)
  y = 0
  draw.text((x,y), date, font = date_font, fill = date_font_color)

  #Draw temperature
  temperature = day["temp2m"]
  temp = "Temp. :\nmax: " + str(temperature["max"]) + "\nmin: " + str(temperature["min"])
  draw.multiline_text((3,10), temp, font = data_font, spacing = -2, fill = data_font_color)

  #Draw wind speed
  speed = des_wind(day["wind10m_max"])
  wind = "Wind\n(km/h):\nmax: " + speed
  draw.multiline_text((3,35), wind, font = data_font, spacing = -2, fill = data_font_color)

  return img

#Function to draw the city forecast screen
def city_forecast(days):

  #Dimensions of the canvas
  size_x = config.WIDTH
  size_y = config.HEIGHT - 15

  #New canvas to draw the get codes screen
  img = Image.new('RGBA', (size_x,size_y), color = (0,0,0,0))
  draw = ImageDraw.Draw(img)

  #Draw each day separately
  img_day0 = draw_day(days[0])
  img_day1 = draw_day(days[1])
  img_day2 = draw_day(days[2])

  #Paste each image to the main canvas
  img.paste(img_day0, (0,0))
  img.paste(img_day1, (54,0))
  img.paste(img_day2, (107,0))

  #Draw sections
  draw.rectangle((0,0,160,size_y), outline = (255,255,255), width = 2)
  draw.line((53,0,53,size_y), fill = (255,255,255), width = 2)
  draw.line((107,0,107,size_y), fill = (255,255,255), width = 2)

  return img
