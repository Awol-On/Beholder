import cv2 as cv
import numpy as np

class Detector:
    needle_img = None
    needle_w = None
    needle_h = None
    line_color = (0, 255, 0)
    line_type = cv.LINE_4

    def __init__(self, needle_path):
        self.needle_img = cv.imread(needle_path, cv.IMREAD_UNCHANGED)
        self.needle_w = self.needle_img.shape[1]
        self.needle_h = self.needle_img.shape[0]

    def paint_match_rectangles(self, haystack_img, threshold=0.80):
        result = cv.matchTemplate(haystack_img, self.needle_img, cv.TM_CCOEFF_NORMED)
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        rectangles = []
        for loc in locations:
            rect = [loc[0], loc[1], self.needle_w, self.needle_h]
            rectangles.append(rect)
            rectangles.append(rect)

        # rectangles, _ = cv.groupRectangles(rectangles, 1, 0.5)

        if len(rectangles):
            for (x, y, w, h) in rectangles:
                # Позиция квадратов
                top_left = (x, y)
                bottom_right = (x + w, y + h)
                # Зарисовка
                cv.rectangle(haystack_img, top_left, bottom_right, self.line_color, self.line_type)

        return haystack_img
