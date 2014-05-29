#coding:utf8
#!/usr/bin/python
# vim: set ts=2 expandtab:
"""
Module: LocateText
Desc:
Author: John O'Neil
Email: oneil.john@gmail.com
DATE: Saturday, Sept 14th 2013

  Setment raw manga scan and output image
  with text areas outlined in red.
  
"""
#import clean_page as clean
import connected_components as cc
import run_length_smoothing as rls
import clean_page as clean
import ocr
import segmentation as seg
import furigana
import arg
import defaults
from scipy.misc import imsave

import numpy as np
import cv2
import sys
import argparse
import os
import scipy.ndimage
import datetime


if __name__ == '__main__':
    
    print 'start....'
    
    
    proc_start_time = datetime.datetime.now()
    
    
    '''
    parser = arg.parser
    parser = argparse.ArgumentParser(description='Generate HTML annotation for raw manga scan with detected OCR\'d text.')
    parser.add_argument('infile', help='Input (color) raw Manga scan image to annoate.')
    parser.add_argument('-o','--output', dest='outfile', help='Output html file.')
    parser.add_argument('-v','--verbose', help='Verbose operation. Print status messages during processing', action="store_true")
    parser.add_argument('--display', help='Display output using OPENCV api and block program exit.', action="store_true")
    parser.add_argument('--furigana', help='Attempt to suppress furigana characters which interfere with OCR.', action="store_true")
    #parser.add_argument('-d','--debug', help='Overlay input image into output.', action="store_true")
    parser.add_argument('--sigma', help='Std Dev of gaussian preprocesing filter.',type=float,default=None)
    parser.add_argument('--binary_threshold', help='Binarization threshold value from 0 to 255.',type=int,default=defaults.BINARY_THRESHOLD)
    #parser.add_argument('--segment_threshold', help='Threshold for nonzero pixels to separete vert/horiz text lines.',type=int,default=1)
    parser.add_argument('--additional_filtering', help='Attempt to filter false text positives by histogram processing.', action="store_true")
    arg.value = parser.parse_args()
    '''
    


    #infile = arg.string_value('infile')
    infile = r'img/same_text.png'
    #outfile = arg.string_value('outfile',default_value=infile + '.text_areas.png')
    
    
    if not os.path.isfile(infile):
        print 'Please provide a regular existing input file. Use -h option for help.'
        sys.exit(-1)
        
    img = cv2.imread(infile)
    cv2.imshow('srcimg', img)
    
    
    gray = clean.grayscale(img)
    
    

    binary_threshold = arg.integer_value('binary_threshold', default_value=defaults.BINARY_THRESHOLD)
    if arg.boolean_value('verbose'):
        print 'Binarizing with threshold value of ' + str(binary_threshold)
        
    
    
    inv_binary = cv2.bitwise_not(clean.binarize(gray, threshold=binary_threshold))
    #cv2.imshow('inv_binary', inv_binary)
    
    
    binary = clean.binarize(gray, threshold=binary_threshold)
    #cv2.imshow('binary', binary)
    
    
    segmented_image = seg.segment_image(gray)
    cv2.imshow('segmented_image', segmented_image)
    
    
    segmented_image = segmented_image[:,:,2]
    components = cc.get_connected_components(segmented_image)
    
    cc.draw_bounding_boxes(img,components,color=(255,0,0),line_size=2)
    
    
    outfile = 'img/no_equalizeHist.png'
    #imsave(outfile, img)
    
    
    cv2.imshow('result',img)
    #cv2.imshow('segmented_image',segmented_image)
    
    cv2.waitKey()
    cv2.destroyAllWindows()
    
    
    '''
    if arg.boolean_value('display'):
        cv2.imshow('segmented_image',segmented_image)
    
    if cv2.waitKey(0) == 27:
        cv2.destroyAllWindows()
        cv2.destroyAllWindows()
    '''
        
        
        
        
        
