from ..integration.device_bridge import DeviceBridge
import time


class OCRHandler:
    def __init__(self, driver):
        self.driver = driver
        self.bridge = DeviceBridge(driver)

    def calculate_new_coords(self, coords, direction, ratio):
        """
        Tính toán tọa độ mới sau khi dịch chuyển theo direction và ratio
        
        Args:
            coords (tuple): Tọa độ ban đầu (x, y)
            direction (str): Hướng dịch chuyển ('up', 'down', 'left', 'right')
            ratio (float): Tỷ lệ phần trăm màn hình
        
        Returns:
            tuple: Tọa độ mới (x, y) hoặc None nếu direction không hợp lệ
        """
        # Lấy kích thước màn hình
        try:
            window_size = self.driver.get_window_size()
            screen_width = window_size['width']
            screen_height = window_size['height']
        except Exception as e:
            print(f"Error getting screen size: {e}")
            return None 
        
        x, y = coords
        
        # Tính toán dựa trên direction và ratio
        if direction == "left":
            x -= int(screen_width * (ratio / 100))
        elif direction == "right":
            x += int(screen_width * (ratio / 100))
        elif direction == "up":
            y -= int(screen_height * (ratio / 100))
        elif direction == "down":
            y += int(screen_height * (ratio / 100))
        else:
            return None 
        
        return (x, y)


    def find_and_click(self, text, bounding_box=None, same_screen=False, direction=None, ratio=None, time_wait=3):
        """Nhấn vào văn bản"""
        coords = self.bridge.process_ocr(text, time_wait, bounding_box, same_screen)
        print(f"Đã thực hiện click vào vị trí {coords}")
        if coords:
            if direction and ratio:
               new_coords = self.calculate_new_coords(coords, direction, ratio)
               return self.bridge.execute_action(new_coords, "click")
            else:
                return self.bridge.execute_action(coords, "click")
            
        else:
            return False
        
    def find_and_input(self, field_text, input_text, bounding_box=None, same_screen=False, direction=None, ratio=None, time_wait=3):
        """Nhập text vào ô"""
        coords = self.bridge.process_ocr(field_text, time_wait, bounding_box, same_screen=same_screen)
        if coords:
            if direction and ratio:
                new_coords = self.calculate_new_coords(coords, direction, ratio)
                if new_coords:
                    print(f"Đã thực hiện nhập liệu vào vị trí {coords}")
                    return self.bridge.execute_action(new_coords, "type", input_text)
                else:
                    return False
            else:
                print(f"Đã thực hiện nhập liệu vào vị trí {coords}")
                return self.bridge.execute_action(coords, "type", input_text)
        else:
            return False
    
    def verify_text_display(self, text, same_screen=False, time_wait=3):
        """Xác nhận text hiển thị trên màn hình"""
        coords = self.bridge.process_ocr(text, time_wait, same_screen=same_screen)
        print(f"Text có hiển thị tại vị trí {coords}")
        if coords:
            return True
        else:
            return False

class UIElementRecognizer:
    def __init__(self, driver):
        self.bridge = DeviceBridge(driver)

    def click_element(self, label, wait_time):
        """Nhấn vào phần tử UI"""
        coords = self.bridge.process_ui_recognition(label, wait_time)
        if coords:
            return self.bridge.execute_action(coords, "click")
            
        print("Không tìm thấy {label}")
        return False
    
    def visualize_all_icon(self):
        self.bridge.visualize_ui_recognition()
        
    def find_back_button_and_click(self, wait_time=3):
        return self.click_element("back_icon", wait_time)

    def find_noti_icon_and_click(self, wait_time=3):
        return self.click_element("noti_icon", wait_time)

    def find_search_icon_and_click(self, wait_time=3):
        return self.click_element("search_icon", wait_time)

    def find_setting_icon_and_click(self, wait_time=3):
        return self.click_element("settings_icon", wait_time)

    def find_menu_icon_and_click(self, wait_time=3):
        return self.click_element("menu_icon", wait_time)

    def find_confirm_button_and_click(self, wait_time=3):
        return self.click_element("confirm_button", wait_time)

    def train_element(self, label, image_path, action):
        """Huấn luyện phần tử mới"""
        from core.model_trainer import train_model
        train_model(image_path, label, action)
