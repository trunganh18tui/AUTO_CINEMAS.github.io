from selenium.webdriver.common.by import By
from .base_page import BasePage
import time
from selenium.webdriver.support import expected_conditions as EC

class BookingPage(BasePage):
    # Locators
    def MOVIE_LINK(self, name): return (By.XPATH, f"//a[contains(text(),'{name}')]")
    def TIME_SLOT(self, time_val): return (By.XPATH, f"//div[text()='{time_val}']")
    BTN_CONFIRM_MODAL = (By.ID, "btndatve")
    def SEAT_BY_NAME(self, name): return (By.XPATH, f"//div[@data-seat-name='{name}']")
    BTN_PROCEED_SEAT = (By.CSS_SELECTOR, "button.btn-thanh-toan")
    BTN_ADD_COMBO = (By.CLASS_NAME, "btn-plus")
    BTN_PROCEED_COMBO = (By.CLASS_NAME, "dieu-khoan-pop-up")
    
    # Thêm locator để kiểm tra bắp nước
    LBL_COMBO_QUANTITY = (By.XPATH, "//span[contains(@class,'combo-quantity')]")

    def select_movie_and_time(self, movie, time_val):
        self.driver.execute_script("window.scrollTo(0, 600);")
        self.js_click(self.MOVIE_LINK(movie))
        time.sleep(2)
        # Kiểm tra xem đã vào trang chi tiết chưa
        detail_status = "chi-tiet-phim" in self.driver.current_url
        
        self.js_click(self.TIME_SLOT(time_val))
        time.sleep(1)
        self.js_click(self.BTN_CONFIRM_MODAL)
        time.sleep(4)
        return detail_status

    def select_seat(self, seat):
        self.js_click(self.SEAT_BY_NAME(seat))
        time.sleep(1)
        self.js_click(self.BTN_PROCEED_SEAT)
        time.sleep(3)

    def increase_combo(self):
        # Lấy số lượng trước khi tăng
        self.js_click(self.BTN_ADD_COMBO)
        time.sleep(1)
        # Lấy số lượng sau khi tăng
        qty = self.driver.find_element(*self.LBL_COMBO_QUANTITY).text
        self.js_click(self.BTN_PROCEED_COMBO)
        return qty