"""
Processing Layer - Handles OCR, image processing, and UI detection using AI.
"""

from .ocr_engine import get_ocr_results_from_image, find_text_from_image, get_ocr_results_list_bbox, find_text_from_in_box
# from .image_utils import preprocess_image, crop_image
from .ui_detector import detect_element_by_label, visualize
# from .model_trainer import train_model

# Đổi tên preprocess_image thành preprocess để khớp với __all__
# preprocess = preprocess_image

__all__ = [
    "get_ocr_results_from_image", "find_text_from_image", 
    "get_ocr_results_list_bbox", "find_text_from_in_box"
    # "crop_image",
    "detect_element_by_label", "visualize"
    # "train_model"
]