from setuptools import setup, find_packages

setup(
    name="MobileVisionTest",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "Appium-Python-Client>=3.2.0",  # Thư viện cho tự động hóa kiểm thử mobile
        "Pillow>=10.0.0",              # Xử lý hình ảnh
        "opencv-python>=4.8.0",        # Xử lý hình ảnh và video
        "pytesseract>=0.3.10",         # OCR
        "torch>=2.0.0",                # PyTorch cho deep learning
        "yolov5>=7.0.0",               # YOLOv5 cho nhận diện đối tượng
        "easyocr>=1.7.0",              # OCR dễ sử dụng
        "numpy==1.26.4",               # Phiên bản cụ thể của NumPy
        "imutils>=0.5.4",              # Công cụ xử lý hình ảnh
        "transformers==4.46.0",        # Hugging Face Transformers
        "sentencepiece>=0.2.0",        # Tokenizer cho NLP
        "ultralytics>=8.0.0",          # Thư viện YOLO mới hơn
        "inference>=0.9.0",            # Inference cho mô hình
        "supervision>=0.22.0",         # Công cụ giám sát và xử lý kết quả YOLO
    ],
    description="A library for automated mobile testing using OCR and AI-based UI recognition",
    author="Dieuanh",
    author_email="dieuanht29@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)