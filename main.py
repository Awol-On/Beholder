import numpy as np
import os
import cv2 as cv
from time import time
from window_capture import WindowCapture
from classification import Classificator
from solving import Solver
from overlay import Overlay

PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(PATH)


# wincap = WindowCapture(window_name='Dota 2')
# wincap = WindowCapture(window_name='1920x1080.jpg')
classificator = Classificator(os.path.join(PATH, 'needle imgs'))
overlay = Overlay(90)

while True:
    # Временное чтение картинки вместо экрана
    frame = cv.imread('1920x1080.jpg', cv.IMREAD_UNCHANGED)
    # frame = wincap.get_frame()
    frame = cv.resize(frame, (1920, 1080), interpolation=cv.INTER_CUBIC)
    cropped_frame = frame[135:855, 225:945]

    classes = classificator.classify(cropped_frame)

    solver = Solver(classes)
    matches, swaps = solver.look_for_solvation()

    overlay.update(matches)

    cv.imshow('Computer Vision', cropped_frame)

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        overlay.close()
        break
