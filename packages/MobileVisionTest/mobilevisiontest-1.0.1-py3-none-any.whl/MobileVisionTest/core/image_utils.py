import cv2
import numpy as np

def preprocess_image(image):
    """Tiền xử lý ảnh: resize, tăng tương phản, ngưỡng thích ứng (ảnh đã là thang xám)."""
    # Resize ảnh
    gray = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    cv2.imwrite("pre_gray.png", gray)
    # Tăng độ tương phản
    gray = cv2.convertScaleAbs(gray, alpha=1.0, beta=20)  # Giữ tham số như cách tiếp cận đầu tiên
    cv2.imwrite("pre_converts.png", gray)
    # Ngưỡng thích ứng
    binary = cv2.adaptiveThreshold(
        gray, 255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 
        11, 1
    )
    cv2.imwrite("pre_threshold.png", binary)
    return binary

def crop_image(image, bbox):
    """Cắt vùng ảnh từ bounding box với padding (ảnh đã là thang xám)."""
    (top_left, top_right, bottom_right, bottom_left) = bbox
    x_min = int(min(top_left[0], bottom_left[0]))
    x_max = int(max(top_right[0], bottom_right[0]))
    y_min = int(min(top_left[1], top_right[1]))
    y_max = int(max(bottom_left[1], bottom_right[1]))
    
    padding = 5
    x_min = max(0, x_min - padding)
    x_max = min(image.shape[1], x_max + padding)
    y_min = max(0, y_min - padding)
    y_max = min(image.shape[0], y_max + padding)
    
    cropped = image[y_min:y_max, x_min:x_max]

    cv2.imwrite("111111.png", cropped)

    return cropped


# if __name__ == "__main__":
#     image_path = "screenshots/ui_element_20250429_151306.png"
#     image = cv2.imread(image_path)
#     gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     cv2.imwrite("gray.png", gray_image)
#     binary_image = preprocess_image(gray_image)
