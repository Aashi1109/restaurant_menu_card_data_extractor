import cv2
import os
import pytesseract

from server.src.config import TESSERACT_EXECUTABLE_PATH
from server.src.ocr.preprocessing import get_grayscale, thresholding

# add teserract path
pytesseract.pytesseract.tesseract_cmd = TESSERACT_EXECUTABLE_PATH

custom_config = "--oem 3 --psm 6"


def perform_ocr(image_path: str):
    if not os.path.exists(image_path):
        return ""
    else:
        image = cv2.imread(image_path)
        gray_image = get_grayscale(image)
        threshold = thresholding(gray_image)
        ocr_results = pytesseract.image_to_string(threshold, config=custom_config)
        return ocr_results
