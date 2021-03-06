import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# required library
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from os.path import splitext,basename
from keras.models import model_from_json
import glob

def sort_contours(cnts,reverse = False):
    i = 0
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))
    return cnts

def crop(img):
    plate_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #plate_image = plate_image / 255
    # convert to grayscale and blur the image
    gray = cv2.cvtColor(plate_image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)

    # Applied inversed thresh_binary
    binary = cv2.threshold(gray, 160, 255,
                           cv2.THRESH_BINARY)[1]

    kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    thre_mor = cv2.morphologyEx(binary, cv2.MORPH_DILATE, kernel3)

    fig = plt.figure(figsize=(12,7))
    plt.rcParams.update({"font.size":18})
    grid = gridspec.GridSpec(ncols=2,nrows=3,figure = fig)
    plot_image = [plate_image, gray, blur, binary,thre_mor]
    plot_name = ["plate_image","gray","blur","binary","dilation"]

    for i in range(len(plot_image)):
        fig.add_subplot(grid[i])
        # plt.axis(False)
        plt.title(plot_name[i])
        if i ==0:
            plt.imshow(plot_image[i])
        else:
            plt.imshow(plot_image[i],cmap="gray")

    plt.savefig("threshding.png", dpi=300)

    cont, _  = cv2.findContours(thre_mor, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # creat a copy version "test_roi" of plat_image to draw bounding box
    test_roi = plate_image.copy()

    # Initialize a list which will be used to append charater image
    crop_characters = []

    # define standard width and height of character
    digit_w, digit_h = 32, 40

    for c in sort_contours(cont):
        (x, y, w, h) = cv2.boundingRect(c)
        ratio = h/w
        if 1<=ratio<=3.5: # Only select contour with defined ratio
            if h/plate_image.shape[0]>=0.5: # Select contour which has the height larger than 50% of the plate
                # Draw bounding box arroung digit number
                cv2.rectangle(test_roi, (x, y), (x + w, y + h), (0, 255,0), 2)

                # Sperate number and gibe prediction
                curr_num = binary[y:y + h, x:x + w]
                crop_characters.append(curr_num)
                # curr_num = thre_mor[y:y+h,x:x+w]
                # curr_num = cv2.resize(curr_num, dsize=(digit_w, digit_h))
                # _, curr_num = cv2.threshold(curr_num, 220, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)


    print("Detect {} letters...".format(len(crop_characters)))
    fig = plt.figure(figsize=(10,6))
    # plt.axis(False)
    plt.imshow(test_roi)
    plt.savefig('grab_digit_contour.png',dpi=300)
    return crop_characters

