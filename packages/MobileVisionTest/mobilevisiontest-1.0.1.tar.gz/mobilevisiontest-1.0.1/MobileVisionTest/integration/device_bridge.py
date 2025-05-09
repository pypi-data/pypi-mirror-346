from ..core import get_ocr_results_from_image, find_text_from_image, get_ocr_results_list_bbox, find_text_from_in_box, detect_element_by_label, visualize
import cv2
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput


import os
from datetime import datetime
import time

class DeviceBridge:
    def __init__(self, driver):
        self.driver = driver
        self._BBOX_IN_SCREEN = None

    def capture_screen(self, test_name):
        # Tạo thư mục screenshots nếu chưa tồn tại
        screenshot_dir = "screenshots"
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        
        # Tạo tên file với timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_file = f"{screenshot_dir}/{test_name}_{timestamp}.png"
        
        # Chụp màn hình và lưu vào file
        self.driver.get_screenshot_as_file(screenshot_file)
        return screenshot_file
    
    def process_ocr(self, target_text, time_wait, bounding_box=None, same_screen=False):
        """Nhận diện văn bản"""
        # Get bounding box nếu không cùng màn hình hoặc chưa có list bbox trước đó
        if not same_screen or self._BBOX_IN_SCREEN is None:
            time.sleep(time_wait)
            screen_path = self.capture_screen("test")

            if bounding_box:
                self._BBOX_IN_SCREEN = get_ocr_results_list_bbox(cv2.imread(screen_path), bounding_box)
            else:
                self._BBOX_IN_SCREEN = get_ocr_results_from_image(cv2.imread(screen_path))
        
        # Tìm target_text từ list bounding box
        if bounding_box:
            return find_text_from_in_box(self._BBOX_IN_SCREEN, target_text)
        else:
            return find_text_from_image(self._BBOX_IN_SCREEN, target_text)

    def execute_action(self, coords, action_type, input_text=None):
        """
        Thực hiện hành động click, type hoặc verify tại tọa độ coords bằng Appium.
        
        Args:
            coords (list): Tọa độ [x, y] để thực hiện hành động.
            action_type (str): Loại hành động ('tap', 'type', 'verify').
            input_text (str, optional): Văn bản để nhập nếu action_type='type'.
        """
        x, y = coords
        action_type = action_type.lower()

        if action_type == "click":
            actions = ActionChains(self.driver)
            actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(x, y)
            actions.w3c_actions.pointer_action.click()
            actions.w3c_actions.perform()
            # print(f"Đã thực hiện tap tại vị trí {coords}")
            return True
        
        elif action_type == "type":
            # Tap vào tọa độ để focus (giả định là trường nhập liệu)
            actions = ActionChains(self.driver)
            actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(x, y)
            actions.w3c_actions.pointer_action.click()
            actions.w3c_actions.perform()
            # Sử dụng execute_script để gửi văn bản qua lệnh mobile: type
            self.driver.execute_script('mobile: type', {'text': input_text})
            # print(f"Đã thực hiện type '{input_text}' tại vị trí {coords}")
            return True
           
        elif action_type == "verify":
            if coords:
                return True

    def process_ui_recognition(self, label, wait_time):
        """Nhận diện phần tử UI"""
        time.sleep(wait_time)
        screen = self.capture_screen("ui_element")
        return detect_element_by_label(cv2.imread(screen), label)
    
    def visualize_ui_recognition(self, wait_time=0):
        """Vẽ phần tử UI, lưu ảnh với tên giống ảnh chụp màn hình trong thư mục output_dir"""
        time.sleep(wait_time)
        screen = self.capture_screen("ui_element")
    
        screen_filename = os.path.basename(screen)

        os.makedirs("screen_output", exist_ok=True)
        output_path = os.path.join("screen_output", screen_filename)

        return visualize(cv2.imread(screen), output_path)