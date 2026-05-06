from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    URL = "https://www.betacinemas.vn/login.htm"
    TXT_EMAIL = (By.ID, "txtLoginName")
    TXT_PASS = (By.ID, "txtLoginPassword")
    IMG_CAPTCHA = (By.ID, "captchalogin")
    TXT_CAPTCHA_INPUT = (By.ID, "txtLoginCaptcha")
    BTN_LOGIN = (By.ID, "btnLogin")

    def open(self):
        self.driver.get(self.URL)

    def clean_popup(self):
        js = "var p = document.getElementById('popup_choosecinema'); if(p) p.remove();" \
             "document.querySelectorAll('.fancybox-overlay, .fancybox-container').forEach(el => el.remove());" \
             "document.body.classList.remove('fancybox-active'); document.body.style.overflow = 'auto';"
        self.driver.execute_script(js)

    def fill_login_form(self, email, password):
        if email: self.send_keys_for_validation(self.TXT_EMAIL, email)
        if password: self.send_keys_for_validation(self.TXT_PASS, password)

    def prepare_captcha(self):
        self.highlight_and_scroll(self.driver.find_element(*self.IMG_CAPTCHA))
        self.highlight_and_scroll(self.driver.find_element(*self.TXT_CAPTCHA_INPUT))

    def click_login(self):
        self.js_click(self.BTN_LOGIN)