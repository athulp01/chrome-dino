import cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from matplotlib import pyplot as plt


def find_cactus(img):
    img = cv2.resize(img,(200,100))
    img = img[20:60,:]
    ret, thresh = cv2.threshold(img, 127, 255, 0)
    for i in thresh[13:14,25:]:
        for dist,j in enumerate(i):
            if j == 0:
                return(dist)
                break


browser = webdriver.Chrome()
browser.get("chrome://dino")
canvas = browser.find_element_by_id('t')
canvas.send_keys(Keys.SPACE)
time.sleep(2)
canvas.send_keys(Keys.SPACE)
while(1):
    browser.save_screenshot('screenshot.png')
    img = cv2.imread('screenshot.png',0)
    if find_cactus(img) is not None:
        print(find_cactus(img))
        if find_cactus(img) < 20 :
            canvas.send_keys(Keys.SPACE)        


