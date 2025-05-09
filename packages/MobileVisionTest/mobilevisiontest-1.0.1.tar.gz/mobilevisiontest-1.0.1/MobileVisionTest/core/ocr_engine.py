import easyocr
import cv2
from unidecode import unidecode
from .image_utils import crop_image, preprocess_image
from .vie_correct import SpellingCorrector
import time

_OCR_ENGINE = None

def get_ocr_engine(lang='vi', use_gpu=True):
    global _OCR_ENGINE
    if _OCR_ENGINE is None:
        _OCR_ENGINE = OcrEngine(lang=lang, use_gpu=use_gpu)
    return _OCR_ENGINE

class OcrEngine:
    def __init__(self, lang='vi', use_gpu=True):
        self.reader = easyocr.Reader([lang], gpu=use_gpu)
    
    def ocr_image(self, image):
        """OCR trên ảnh gốc."""
        return self.reader.readtext(image, paragraph=False)
    
def calculate_center(bbox):
    """Tính vị trí giữa của bounding box."""
    (top_left, top_right, bottom_right, bottom_left) = bbox
    center_x = (top_left[0] + top_right[0] + bottom_right[0] + bottom_left[0]) / 4
    center_y = (top_left[1] + top_right[1] + bottom_right[1] + bottom_left[1]) / 4
    return [center_x, center_y]

def create_full_bbox(top_left, bottom_right):
    """Tạo bounding box đầy đủ từ tọa độ top-left và bottom-right."""
    x1, y1 = top_left
    x3, y3 = bottom_right
    return [
        (x1, y1),  # top-left
        (x3, y1),  # top-right
        (x3, y3),  # bottom-right
        (x1, y3)   # bottom-left
    ]

def get_ocr_results_from_image(image, lang="vi", gpu=True):
    """
    Thực hiện OCR trên ảnh gốc và các vùng cắt, trả về danh sách tất cả kết quả OCR.
    Args:
        image: Ảnh đầu vào
        lang: Ngôn ngữ OCR.
        gpu: Sử dụng GPU nếu True.
    Returns:
        List of tuples [(bbox, text, prob), ...] chứa bounding box, văn bản, và xác suất.
    """
    ocr = get_ocr_engine(lang=lang, use_gpu=gpu)

    # Bước 1: OCR trên ảnh gốc
    results = ocr.ocr_image(image)
    texts_original = [(bbox, text.lower(), prob) for (bbox, text, prob) in results]
    print(f"Step 1 - Texts from original image: {[text for _, text, _ in texts_original]}")
    return texts_original
    # # Bước 2: Chuyển sang thang xám, lấy bounding box và xử lý hàng loạt
    # texts_process = []
    # if results:
    #     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #     cropped_images = [crop_image(gray, bbox) for (bbox, _, _) in results]
    #     cropped_images = [img for img in cropped_images if img is not None]
    #     if cropped_images:
    #         preprocessed_images = [preprocess_image(img) for img in cropped_images]
    #         preprocessed_images = [img for img in preprocessed_images if img is not None]
    #         if preprocessed_images:
    #             max_height = max(img.shape[0] for img in preprocessed_images)
    #             max_width = max(img.shape[1] for img in preprocessed_images)
    #             preprocessed_images = [
    #                 cv2.resize(img, (max_width, max_height), interpolation=cv2.INTER_NEAREST)
    #                 for img in preprocessed_images
    #             ]
    #             results_batch = ocr.reader.readtext_batched(preprocessed_images, batch_size=4, contrast_ths=0.03)
    #             valid_results = [(bbox, text, prob) for (bbox, text, prob) in results]
    #             for idx, sub_results in enumerate(results_batch):
    #                 if sub_results:
    #                     for (bbox, text, prob) in sub_results:
    #                         orig_bbox = valid_results[idx][0]
    #                         texts_process.append((orig_bbox, text.lower(), prob))

    # # Kết hợp kết quả từ OCR gốc và OCR hàng loạt
    # all_texts_with_bbox = texts_original + texts_process
    # print(f"Danh sách bounding box: {all_texts_with_bbox}")
    # return all_texts_with_bbox

def find_text_from_image(all_texts_with_bbox, initial_text):
    """
    Tìm văn bản khớp trong danh sách kết quả OCR, kiểm tra văn bản gốc, sửa chính tả, bỏ dấu.
    Args:
        all_texts_with_bbox: List of tuples [(bbox, text, prob), ...] từ OCR.
        initial_text: Văn bản cần tìm.
    Returns:
        Tọa độ trung tâm [center_x, center_y] hoặc None nếu không tìm thấy.
    """
    corrector = SpellingCorrector()
    initial_text_lower = initial_text.lower()

    # Bước 1: Kiểm tra initial_text trong danh sách văn bản gốc
    for bbox, text, prob in all_texts_with_bbox:
        if initial_text_lower in text:
            return calculate_center(bbox)

    # Bước 2: Nếu không tìm thấy, gọi sửa chính tả
    if all_texts_with_bbox:
        all_texts = [text for _, text, _ in all_texts_with_bbox]
        corrected_texts = corrector.correct_texts(all_texts)
        corrected_texts = [text.replace(".", "").lower() for text in corrected_texts]
        for idx, corrected_text in enumerate(corrected_texts):
            if initial_text_lower in corrected_text:
                bbox = all_texts_with_bbox[idx][0]
                return calculate_center(bbox)

        # Bước 3: Gọi bỏ accent
        no_accent_texts = corrector.no_accent(all_texts)
        no_accent_texts = [text.lower() for text in no_accent_texts]
        initial_text_no_accents = unidecode(initial_text_lower)
        for idx, no_accent_text in enumerate(no_accent_texts):
            if initial_text_no_accents in no_accent_text:
                bbox = all_texts_with_bbox[idx][0]
                return calculate_center(bbox)

    return None

def get_ocr_results_list_bbox(image, bounding_box, lang="vi", gpu=True):
    """
    Trích xuất danh sách kết quả OCR từ ảnh và danh sách bounding box.
    Trả về danh sách tất cả kết quả OCR từ các bounding box.
    """
    ocr = get_ocr_engine(lang=lang, use_gpu=gpu)
    all_results = []
    
    for bbox in bounding_box:
        if len(bbox) == 2:  
            full_bbox = create_full_bbox(bbox[0], bbox[1])
        elif len(bbox) == 4:
            full_bbox = bbox
        
        # Cắt ảnh theo bounding box đầy đủ
        cropped_image = crop_image(image, full_bbox)
        if cropped_image is not None:
            # Thực hiện OCR trên ảnh cắt
            results = ocr.ocr_image(cropped_image)
            all_results.extend(results)  # Thêm kết quả vào danh sách chung
    print(f"Danh sách bounding box: {all_results}")
    
    return all_results

def find_text_from_in_box(results_ocr, target_text):
    """
    Tìm tọa độ trung tâm của văn bản khớp trong danh sách kết quả OCR.
    """
    corrector = SpellingCorrector()
    target_text_lower = target_text.lower()
    
    # Kiểm tra văn bản gốc
    for bbox, text, prob in results_ocr:
        text_lower = text.lower()
        if target_text_lower in text_lower:
            return calculate_center(bbox)
    
    # Nếu không tìm thấy, thử sửa chính tả
    texts = [text for _, text, _ in results_ocr]
    text_bboxes = [bbox for bbox, _, _ in results_ocr]
    if texts:
        corrected_texts = corrector.correct_texts(texts)
        corrected_texts = [text.replace(".", "").lower() for text in corrected_texts]
        for idx, corrected_text in enumerate(corrected_texts):
            if target_text_lower in corrected_text:
                return calculate_center(text_bboxes[idx])
        
        # Nếu vẫn không thấy, thử bỏ dấu
        no_accent_texts = corrector.no_accent(texts)
        no_accent_texts = [text.lower() for text in no_accent_texts]
        target_text_no_accents = unidecode(target_text_lower)
        for idx, no_accent_text in enumerate(no_accent_texts):
            if target_text_no_accents in no_accent_text:
                return calculate_center(text_bboxes[idx])
    
    return None

def main(image_path, initial_text):
    image = cv2.imread(image_path)
    if image is None:
        return f"Không thể tải ảnh từ {image_path}"
    bounding_box = [
        [(0, 1800), (1440, 2200)]
    ]
    result = find_text_from_in_box(image, initial_text, bounding_box)
    return result

if __name__ == "__main__":
    image_path = "screenshots/Screenshot_1746366988.png"
    initial_text = "Đăng nhập"
    result = main(image_path, initial_text)
    print(f"Tọa độ của {initial_text} trong màn hình là {result}")
