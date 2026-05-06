from selenium.webdriver.common.by import By
from .base_page import BasePage
import time
from selenium.webdriver.support import expected_conditions as EC

class PaymentPage(BasePage):
    RADIO_QR_CODE = (By.XPATH, "//label[@for='card6']")
    CHK_AGREE = (By.CLASS_NAME, "checkmark")
    BTN_PAY_NOW = (By.ID, "b")
    IMG_QR_CODE = (By.ID, "qrPaymentImage")
    BTN_CANCEL = (By.XPATH, "//a[contains(text(),'HỦY GIAO DỊCH')]")
    BTN_CONFIRM_CANCEL = (By.CLASS_NAME, "btn-confirm")

    def pay_with_qr_code(self):
        self.js_click(self.RADIO_QR_CODE)
        time.sleep(1)
        self.js_click(self.CHK_AGREE)
        time.sleep(1)
        self.js_click(self.BTN_PAY_NOW)
        print("   - Đang đợi hệ thống tạo mã QR...")

    def is_qr_displayed(self):
        try:
            # Đợi tối đa 20 giây cho ảnh QR xuất hiện
            self.wait.until(EC.visibility_of_element_located(self.IMG_QR_CODE))
            return self.driver.find_element(*self.IMG_QR_CODE).is_displayed()
        except:
            return False

    def cancel_and_return(self):
        self.js_click(self.BTN_CANCEL)
        time.sleep(2)
        self.js_click(self.BTN_CONFIRM_CANCEL)
        time.sleep(4)