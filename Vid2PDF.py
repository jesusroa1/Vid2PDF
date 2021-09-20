# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 13:01:42 2020

@author: Lenovo


Full Program
Select a video and take screenshots at a zoomed in level
Then delete duplicate screenshots 
"""

import ctypes  # An included library with Python install.
"""
	Styles:
	0 : OK
	1 : OK | Cancel
	2 : Abort | Retry | Ignore
	3 : Yes | No | Cancel
	4 : Yes | No
	5 : Retry | No 
	6 : Cancel | Try Again | Continue
"""
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory

import cv2
import numpy as np
from skimage.measure import compare_ssim

from os import walk

import os
import img2pdf

import ocrmypdf
#import PyPDF2
#import pypdfocr



def main():
    test = 1
    if test == 0:
        vid = \
            'C:/Users/Lenovo/Desktop/Rutgers Fall 2020/Sustainable Energy/Video2PPT/SE-9-22.mp4'
        destination = \
            'C:/Users/Lenovo/Desktop/Rutgers Fall 2020/Sustainable Energy/Video2PPT/FrameCaptures/Output_Lec8_9-29'
        '''    
        pdfPath = choosePDF()
        print(pdfPath)
        ocrmypdf.ocr(pdfPath, 'output_OCR.pdf', deskew=True)
        '''
        fileName = vid[-15:]
        print(fileName)
        
        
    else:
        MboxOut = Mbox('Directions',
                       'Select video, then select destination folder',
                       0)
        vid = chooseVid()
        destination = chooseDestination()
    
    r = [200, 1050, 400, 1500]
    t = (0.85 * 1)
    
    TakeScreenShots(vid, destination, 5, r, t)
    createPDF(destination)
    print(vid)
    
    

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

def chooseVid():
	Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
	filename = askopenfilename(filetypes=[("Select Video", "*.mp4"), ("All Files", "*.*")]) # show an "Open" dialog box and return the path to the selected file
	return(filename)
    
def choosePDF():
	Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
	filename = askopenfilename(filetypes=[("Select PDF", "*.pdf"), ("All Files", "*.*")]) # show an "Open" dialog box and return the path to the selected file
	return(filename)

def chooseDestination():
	Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
	filename = askdirectory() # show an "Open" dialog box and return the path to the selected file
	return(filename)

def TakeScreenShots(vidPath,outPath,Frequency,resizeArray,threshold):
    '''
....Takes a screenshot every FREQUENCY seconds, resizes
....the screenshot to RESIZEARRAY

....vidPath: Path to the video
    outPath: Where to put all the screenshots
....Frequency: Time between screenshots
....reizeArray: [Left, Right, Bottom, Top] in pixels. Ideally resize
................to point where vid only shows the 'screenshare'.
    threshold: decimal up to 1 determining how similar the images can be to count them as unique
....'''


    vidcap = cv2.VideoCapture(vidPath)
    count = 0
    success = True
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    
    while success:
        (success, newImage) = vidcap.read()
        if count % (Frequency * fps) == 0:
            newImage = newImage[resizeArray[0]:resizeArray[1],
                                resizeArray[2]:resizeArray[3]]
            newImage_grey = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
            if count == 0:
                oldImage = newImage_grey
            (score, diff) = compare_ssim(oldImage, newImage_grey,full=True)
            oldImage = newImage_grey
            print(score)
            print(count)
            if score <= threshold:
                cv2.imwrite(outPath + '/frame%d.jpg' % count, newImage)
                #oldImage = newImage.copy
                print('written frame #' + str(count))
        count += 1
             # success = False
             
    
                # vidcap.set(cv2.CAP_PROP_POS_MSEC,690000) Skip ahead in vid X frames
 
def pullFrameList(mypath):
    f = []
    for (dirpath, dirnames, filenames) in walk(mypath):
        f.extend(filenames)
        break    
    return f

def createPDF(mypath):
    os.chdir(mypath)
    with open("output.pdf", "wb") as f:
        f.write(img2pdf.convert([i for i in os.listdir(os.getcwd()) if i.endswith(".jpg")]))

#def addTextLayer(pdfPath):
        

if __name__ == "__main__":
    main()
	#This snippets makes the whole script jump straight to main()
