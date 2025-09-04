import os
import cv2 as cv
from time import time
from window_capture import WindowCapture
from classification import Classificator
from solving import Solver
from overlay import Overlay
import sys

PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(PATH)


wincap = WindowCapture(window_name='Dota 2')
classificator = Classificator(os.path.join(PATH, 'needle imgs'))
overlay = Overlay(90)

while True:
    frame = wincap.get_frame()
    frame = cv.resize(frame, (1920, 1080), interpolation=cv.INTER_CUBIC)
    cropped_frame = frame[135:855, 225:945]

    classes = classificator.classify(cropped_frame)
    solver = Solver(classes)
    matches, swaps = solver.look_for_solvation()

    overlay.update_frame(matches)
    overlay.update()

    if overlay.close_flag:
        break
    # if cv.waitKey(1) == ord('q'):
    #     cv.destroyAllWindows()
    #     overlay.close()
    #     break
