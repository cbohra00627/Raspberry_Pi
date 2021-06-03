#!/usr/bin/env python3

#This file contains the common variables to all the scripts
import ST7735

#Create a display instance
disp = ST7735.ST7735(
  port = 0,
  cs = 1,
  dc = 9,
  backlight = 12,
  rotation = 270,
  spi_speed_hz = 10000000
)

#Get width and height of the display. Its (160,80) for the enviro display.
WIDTH = disp.width
HEIGHT = disp.height

