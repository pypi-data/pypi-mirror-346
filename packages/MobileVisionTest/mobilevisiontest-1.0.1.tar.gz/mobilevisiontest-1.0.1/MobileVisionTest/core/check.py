import cv2
import easyocr
import numpy as np

if __name__ == "__main__":
    # Đường dẫn tới ảnh
    image_path = "lib/MobileVisionTest/image/start1.jpg"
    
    # Đọc ảnh bằng OpenCV
    image = cv2.imread(image_path)
    image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    # Kiểm tra xem ảnh có được tải thành công không
    if image is None:
        print(f"Không thể tải ảnh từ đường dẫn: {image_path}. Vui lòng kiểm tra lại đường dẫn.")
    else:
        try:
            # Chạy OCR trên ảnh gốc (không xử lý)
            print("=== OCR trên ảnh gốc ===")
            reader = easyocr.Reader(['vi'], gpu=False)
            results_original = reader.readtext(image, paragraph=False, contrast_ths=0.05, adjust_contrast=0.7)
            if results_original:
                for (bbox, text, prob) in results_original:
                    print(f"Text: {text} (Confidence: {prob:.2f})")
            else:
                print("Không phát hiện được văn bản nào trong ảnh gốc.")

            # Xử lý ảnh
            print("\n=== OCR trên ảnh đã xử lý ===")
            # Chuyển ảnh sang thang xám
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Tăng độ tương phản nhẹ hơn
            gray = cv2.convertScaleAbs(gray, alpha=1.0, beta=18)  # Giảm alpha, thêm beta để tăng sáng
        
            
            # Dùng ngưỡng thích ứng với tham số nhẹ hơn
            binary = cv2.adaptiveThreshold(
                gray, 255, 
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY_INV, 
                11, 1  # Giảm blockSize và C để giữ chi tiết
            )
            
            
            # Lưu ảnh đã xử lý để kiểm tra
            cv2.imwrite("processed_image.jpg", binary)
            
            # Chạy OCR trên ảnh đã xử lý
            results_processed = reader.readtext(binary, paragraph=False, contrast_ths=0.05, adjust_contrast=0.7)
            if results_processed:
                for (bbox, text, prob) in results_processed:
                    print(f"Text: {text} (Confidence: {prob:.2f})")
            else:
                print("Không phát hiện được văn bản nào trong ảnh đã xử lý.")
                
        except Exception as e:
            print(f"Đã xảy ra lỗi: {str(e)}. Vui lòng kiểm tra cài đặt thư viện hoặc file ảnh.")

