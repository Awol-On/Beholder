import win32gui, win32ui, win32con
import numpy as np
import ctypes
import pyautogui
import cv2 as cv

class WindowCapture:

    TRACKBAR_WINDOW = 'Trackbars'

    width = 0
    height = 0
    hwnd = None

    def __init__(self, window_name):
        # Поиск окна по названию
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception(f'Window not found {window_name}')
        
        # Определение размера окна
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        self.width = right - left
        self.height = bottom - top

    def get_frame(self):
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.width, self.height)
        cDC.SelectObject(dataBitMap)
        result = ctypes.windll.user32.PrintWindow(self.hwnd, cDC.GetSafeHdc(), 3)

        # Чтобы не выбрасывало ошибку при сворачивании окна
        if not result:
            result = ctypes.windll.user32.PrintWindow(self.hwnd, cDC.GetSafeHdc(), 1)

        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.frombuffer(signedIntsArray, dtype='uint8')
        img.shape = (self.height, self.width, 4)

        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # Удаление альфа-канала (прозрачности), оставляя RGB
        img = img[...,:3]
        img = np.ascontiguousarray(img)

        return img
    
    # Возвращает список строк с названиями открытых (не обязательно активных) окон
    @staticmethod
    def get_list_window_names():
        list_names = []
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                window = win32gui.GetWindowText(hwnd)
                if window == '':
                    pass
                else:
                    list_names.append(window)
        win32gui.EnumWindows(winEnumHandler, None)
        return list_names

    