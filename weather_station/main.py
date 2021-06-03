#!/usr/bin/env python3

#This file contains the code to display various screens on the display
import time
import config
import weather
import world_weather
from datetime import date
from PIL import Image, ImageDraw, ImageFont

#Function to print the welcome screen
def welcome_screen():

  #New canvas to draw welcome screen
  img = Image.new('RGB', (config.WIDTH,config.HEIGHT), color = (255,255,0))
  draw = ImageDraw.Draw(img)

  #Font Settings
  font = ImageFont.truetype("fonts/Pacifico.ttf", 25)
  font_color = (0,0,0)

  #Size of the message
  message = "Weather\nStation!"
  (size_x,size_y) = draw.textsize(message, font)

  #Position of the welcome message
  x = (config.WIDTH - size_x)/2
  y = (config.HEIGHT - size_y)/2

  #Draw the welcome message
  draw.multiline_text((x,y), message, font = font, spacing = -5, align = "center", fill = font_color)

  return img

#Function to print the menu screen
def menu_screen():

  #New canvas to draw the menu screen
  img = Image.new('RGBA', (config.WIDTH,config.HEIGHT-15), (0,0,0,0))
  draw = ImageDraw.Draw(img)

  #Draw a section line
  draw.line((80,0,80,80), fill = (255,255,255), width = 1)

  #Draw the weather and the world icons for the menu
  weather_icon = Image.open("icons/weather.png")
  world_icon = Image.open("icons/world.png")
  img.paste(weather_icon, (15,3), mask = weather_icon)
  img.paste(world_icon, (95,3), mask = world_icon)

  #Menu Font Settings
  menu_font = ImageFont.truetype("fonts/OpenSans-Regular.ttf", 9)
  menu_font_color = (0,0,0)

  #Draw the menu text
  menu_text = "Weather Monitor        City Weather"
  draw.text((5,50), menu_text, font = menu_font, fill = menu_font_color)

  return img


#Function to print the main screen
def main_screen(screen):

  #New canvas to draw the main screen
  img = Image.new('RGB', (config.WIDTH,config.HEIGHT), color = (0,255,255))
  draw = ImageDraw.Draw(img)

  #Header Font Settings
  header_font = ImageFont.truetype("fonts/OpenSans-Semibold.ttf", 13)
  header_font_color = (0,0,0)

  #Drawing the date
  today_date = date.today()
  today_date = today_date.strftime("%d/%m/%Y")
  draw.text((0,-2), today_date, font = header_font, fill = header_font_color)

  #Paste the main screen with menu
  img.paste(screen, (0,15), mask = screen)

  #Draw a section line
  draw.line((0,15,160,15), fill = (255,255,255), width = 2)

  return img


#Iniitalize the display
config.disp.begin()

#Run the code
try:

  #Display the welcome screen
  screen = welcome_screen()
  config.disp.display(screen)

  #Wait 3 seconds for the main screen.
  time.sleep(3.0)

  while True:

    #Display the main screen with the menu
    screen = main_screen(menu_screen())
    config.disp.display(screen)

    #Ask the user for the menu number
    menu_num = str(input("\nEnter the menu number:\n1. Weather Monitor\n2. World Weather\nPress Ctrl C to exit\n"))

    #Code block for the weather screen
    if menu_num == '1':

      try:

        print("\nPress Ctrl C to go back.\n")

        while True:

          #Get and display the weather screen
          weather_screen = weather.weather_screen()
          screen = main_screen(weather_screen)
          config.disp.display(screen)
          time.sleep(1.0)

      except KeyboardInterrupt:
        continue

    #Code block for the world weather screen
    elif menu_num == '2':

      try:

        #Get the display the screen to ask for codes
        codes_screen = world_weather.get_codes()
        screen = main_screen(codes_screen)
        config.disp.display(screen)

        print("\nPress Ctrl C to go back.")

        #Get the codes
        country_code = str(input("Please enter the correct ISO country code in capital letters: "))
        zip_code = str(input("Please enter the correct city code: "))

        print("\nLoading...\n")

        try:

          #Get the city coordinates
          (long, lat) = world_weather.get_city_coordinates(country_code, zip_code)

        except Exception as e:
          print(e)
          continue

        try:

          #Get city weather forecast
          days = world_weather.get_city_forecast(long, lat)

        except Exception as e:
          print(e)
          continue

        #Get the city forecast screen
        forecast_screen = world_weather.city_forecast(days)
        screen = main_screen(forecast_screen)

        print("Press Ctrl C to go back.")

        while True:

          #Display the forecast screen
          config.disp.display(screen)

      except KeyboardInterrupt:
        continue

    else:
      print("\nPlease enter a valid character.\n")
      continue

#When ^C is pressed, the backlight gets set to 0
except KeyboardInterrupt:
  config.disp.set_backlight(0)
