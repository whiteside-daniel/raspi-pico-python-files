#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 23:39:02 2024

@author: Daniel
"""

from PIL import Image
import numpy as np

fileName = input('file name (must be png): ')
firstImage = Image.open(fileName+'.png')
dim1 = np.shape(firstImage)
print(dim1)
print(firstImage)
print(np.array(firstImage))
# Open the file in write mode ('w')
with open(fileName+".py", "w") as f:
  f.write("dataArray=[")
  # Write the text to the file
  for row in range(0,len(np.array(firstImage))):
      if row != 0:
          f.write(",")
      f.write("[")
      for col in range(0,len(np.array(firstImage)[1])):
          if col != 0:
              f.write(",")
          val = 255-int(np.array(firstImage)[row][col])
          if val <= 15:
              val = 0
          else:
              val = 1
          f.write(str(val))
      f.write("]")
  f.write("]")