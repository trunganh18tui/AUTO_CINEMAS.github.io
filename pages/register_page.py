from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from .base_page import BasePage
import time

class RegisterPage(BasePage):
    URL = "https://www.betacinemas.vn/login.htm#register"
    TXT_NAME = (By.ID, "txtName")
    TXT_EMAIL = (By.ID, "txtEmail")
    TXT_PASS = (By.ID, "txtMatKhau")
    TXT_CONFIRM_PASS = (By.XPATH, "//input[@placeholder='Xác nhận lại mật khẩu']")
    TXT_BIRTHDAY = (By.ID, "txtNgaySinh")
    CBO_GENDER = (By.ID, "cboSex")
    TXT_PHONE = (By.ID, "txtDienThoai")
    CHK_AGREE = (By.ID, "chk")
    BTN_REGISTER = (By.CSS_SELECTOR, "button.btn-mua-ve")
    IMG_CAPTCHA = (By.ID, "captcharegister")
    TXT_CAPTCHA_INPUT = (By.ID, "txtMaXacThuc")

    def open(self):
        self.driver.get(self.URL)

    def clean_popup(self):
        # Thêm lệnh ẩn thanh Menu nếu nó quá phiền phức (Tùy chọn)
        js = """
            var p = document.getElementById('popup_choosecinema'); if(p) p.remove();
            document.querySelectorAll('.fancybox-overlay, .fancybox-container').forEach(el => el.remove());
            document.body.classList.remove('fancybox-active');
            document.body.style.overflow = 'auto';
        """
        self.driver.execute_script(js)

    def fill_form(self, data, email, phone):
        self.send_keys_and_validate(self.TXT_NAME, data['name'])
        self.send_keys_and_validate(self.TXT_EMAIL, email)
        self.send_keys_and_validate(self.TXT_PASS, data['pass'])
        self.send_keys_and_validate(self.TXT_CONFIRM_PASS, data['confirm_pass'])
        self.fill_date_by_js(self.TXT_BIRTHDAY, data['birth'])
        
        gender = self.driver.find_element(*self.CBO_GENDER)
        self.highlight_and_scroll(gender)
        Select(gender).select_by_index(1)
        
        self.send_keys_and_validate(self.TXT_PHONE, phone)
        if data['agree']: self.js_click(self.CHK_AGREE)

    def get_ready_for_captcha(self):
        self.highlight_and_scroll(self.driver.find_element(*self.IMG_CAPTCHA))
        self.highlight_and_scroll(self.driver.find_element(*self.TXT_CAPTCHA_INPUT))

    def click_register(self):
        self.js_click(self.BTN_REGISTER)