import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def highlight_and_scroll(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.driver.execute_script("arguments[0].setAttribute('style', 'border: 3px solid red; background: #ffff0033;');", element)
        time.sleep(0.3)

    def send_keys_for_validation(self, locator, text):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.highlight_and_scroll(element)
        self.driver.execute_script("arguments[0].click();", element)
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.BACKSPACE)
        for char in text:
            element.send_keys(char)
            time.sleep(0.05)
        self.driver.execute_script("""
            var el = arguments[0];
            var events = ['input', 'change', 'blur'];
            events.forEach(function(e) { el.dispatchEvent(new Event(e, { bubbles: true })); });
        """, element)
        time.sleep(0.2)

    def js_click(self, locator):
        # Đợi phần tử xuất hiện trong DOM trước khi click
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.highlight_and_scroll(element)
        self.driver.execute_script("arguments[0].click();", element)
        time.sleep(0.5)