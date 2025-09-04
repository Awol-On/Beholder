import numpy as np
import os
import cv2 as cv


class Classificator:
    cell_w = None
    cell_h = None
    needles = []

    def __init__(self, needle_dir=None):
        if not needle_dir:
            needle_dir = os.path.join(os.path.dirname(__file__), 'needle imgs')
            if not os.path.exists(needle_dir):
                raise Exception('Не найден путь к шаблонным изображениям')
        
        for img in os.listdir(needle_dir):
            img_path = os.path.join(needle_dir, img)
            self.needles.append(cv.imread(img_path, cv.IMREAD_UNCHANGED))
        
    def classify(self, frame, threshold=0.75):
        classes = []
        if not self.cell_h or not self.cell_w:
            self.cell_w = int(frame.shape[0] / 8)
            self.cell_h = int(frame.shape[1] / 8)
        
        rows = [frame[self.cell_h*i:self.cell_h*(i+1), :] for i in range(0, 8)]
        cells = []
        for row in rows:
            cells.append([row[:, self.cell_w*i:self.cell_h*(i+1)] for i in range(0, 8)])

        for row in cells:
            for cell in row:
                for index, needle in enumerate(self.needles):
                    result = cv.matchTemplate(cell, needle, cv.TM_CCOEFF_NORMED)
                    locations = np.where(result >= threshold)
                    if len(locations[0]):
                        classes.append(index)
                        break
                if not len(locations[0]):
                    classes.append(None)
        
        return np.array(classes).reshape((8, 8))
            



        
