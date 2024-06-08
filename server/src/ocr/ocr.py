import os

import cv2
import pytesseract

from server.src.logger import logger
from server.src.ocr.preprocessing import get_grayscale, thresholding

# add tesseract path
# pytesseract.pytesseract.tesseract_cmd = TESSERACT_EXECUTABLE_PATH

custom_config = "--oem 3 --psm 6"


def perform_ocr(image_path: str):
    try:
        if not (image_path and os.path.exists(image_path)):
            return ""
        else:
            image = cv2.imread(image_path)
            gray_image = get_grayscale(image)
            threshold = thresholding(gray_image)
            ocr_results = pytesseract.image_to_string(threshold, config=custom_config)
            return ocr_results
    except Exception as e:
        logger.error(f"Error performing OCR {str(e)}", exc_info=True)
