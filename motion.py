import cv2
import numpy as np
from PIL import Image, ImageGrab

def motion_detector():
  
  frame_count = 0
  previous_frame = None
  prepared_frame = None
  
  while True:
    frame_count += 1
    cam = cv2.VideoCapture(0)
    # 1. Load image; convert to RGB
    img_brg = np.array(ImageGrab.grab())
    img_rgb = cv2.cvtColor(src=img_brg, code=cv2.COLOR_BGR2RGB)

    if ((frame_count % 2) == 0):

      # 2. Prepare image; grayscale and blur
      prepared_frame = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
      prepared_frame = cv2.GaussianBlur(src=prepared_frame, ksize=(5,5), sigmaX=0)
    
    if (previous_frame is None):
  # First frame; there is no previous one yet
      previous_frame = prepared_frame
      continue
  
    # calculate difference and update previous frame
    diff_frame = cv2.absdiff(src1=previous_frame, src2=prepared_frame)
    thresh_frame = cv2.threshold(src=diff_frame, thresh=20, maxval=255, type=cv2.THRESH_BINARY)[1]
    
    
    contours, _ = cv2.findContours(image=thresh_frame, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image=img_rgb, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
    

motion_detector()