#!/usr/bin/python
# vim: set ts=2 expandtab:
"""
Module: connected_components.py
Desc:
Author: John O'Neil
Email: oneil.john@gmail.com
DATE: Saturday, August 10th 2013
      Revision: Thursday, August 15th 2013

  Connected component generation and manipulation
  utility functions.
  
"""
import numpy as np
import scipy.ndimage
from pylab import zeros,amax,median
import cv2

def area_bb(a):
  return np.prod([max(x.stop-x.start,0) for x in a[:2]])

def area_nz(slice, image):
  return np.count_nonzero(image[slice])

def get_connected_components(image):
  s = scipy.ndimage.morphology.generate_binary_structure(2,2)
  labels,n = scipy.ndimage.measurements.label(image)#,structure=s)
  objects = scipy.ndimage.measurements.find_objects(labels)
  return objects  

def bounding_boxes(image,connected_components,max_size,min_size):
  mask = np.zeros(image.shape,'B')#np.uint8)#'B')
  for component in connected_components:
    if area_bb(component)**.5<min_size: continue
    if area_bb(component)**.5>max_size: continue
    #a = area_nz(component,image)
    #if a<min_size: continue
    #if a>max_size: continue
    mask[component] = 1#255
  return mask

def masks(image,connected_components,max_size,min_size):
  mask = zeros(image.shape,np.uint8)#,'B')
  for component in connected_components:
    if area_bb(component)**.5<min_size: continue
    if area_bb(component)**.5>max_size: continue
    #a = area_nz(component,image)
    #if a<min_size: continue
    #if a>max_size: continue
    #print str(image[component])
    mask[component] = image[component]>0
    #print str(mask[component])
  return mask

def draw_bounding_boxes(img,connected_components,max_size=0,min_size=0,color=(0,0,255),line_size=2):
  for component in connected_components:
    if min_size > 0 and area_bb(component)**0.5<min_size: continue
    if max_size > 0 and area_bb(component)**0.5>max_size: continue
    #a = area_nz(component,img)
    #if a<min_size: continue
    #if a>max_size: continue
    (ys,xs)=component[:2]
    cv2.rectangle(img,(xs.start,ys.start),(xs.stop,ys.stop),color,line_size)

def filter_by_size(image,connected_components,max_size,min_size):
  filtered = []
  for cc in connected_components:
    if area_bb(cc)**0.5<min_size: continue
    if area_bb(cc)**0.5>max_size: continue
    filtered.append(cc)
  return filtered

def filter_by_black_white_ratio(img,connected_components,maximum=1.0,minimum=0.0):
  filtered = []
  for component in connected_components:
    black = area_nz(component,img)
    a = area_bb(component) 
    percent_black = float(black)/float(a)
    if percent_black < minimum or percent_black > maximum:
      #print 'component removed for percent ' + str(percent_black)
      continue
    filtered.append(component)
  return filtered

def average_size(img):
  components = get_connected_components(img)
  sorted_components = sorted(components,key=area_bb)
  #sorted_components = sorted(components,key=lambda x:area_nz(x,binary))
  areas = zeros(img.shape)
  for component in sorted_components:
    if amax(areas[component])>0: continue
    areas[component] = area_bb(component)**0.5
    #areas[component]=area_nz(component,binary)
  average_size = median(areas[(areas>3)&(areas<100)])
  return average_size

def form_mask(img, max_size, min_size):
  components = get_connected_components(img)
  sorted_components = sorted(components,key=area_bb)
  #mask = bounding_boxes(img,sorted_components,max_size,min_size)
  mask = masks(img,sorted_components,max_size,min_size)
  return mask

