import allure
import pytest
import time
import json
import os
from pages.login_page import LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException, TimeoutException

def load_login_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    data_path = os.path.normpath(os.path.join(project_root, "data", "login_data.json"))
    with open(data_path, encoding='utf-8') as f:
        data = json.load(f)
        print(f"\n[HỆ THỐNG] Đã tìm thấy {len(data)} kịch bản.")
        return data

@allure.feature("Beta Cinemas - POM Login")
@pytest.mark.parametrize("data", load_login_data())
def test_beta_login_scenarios(driver, data):
    login_page = LoginPage(driver)
    allure.dynamic.title(f"{data['tc_id']}: {data['description']}")

    with allure.step("1. Mở trang và dọn dẹp"):
        login_page.open()
        time.sleep(2)
        login_page.clean_popup()

    with allure.step(f"2. Nhập thông tin: {data['email']}"):
        login_page.fill_login_form(data['email'], data['pass'])

    with allure.step("3. Xử lý Captcha"):
        login_page.prepare_captcha()
        print(f"\n>>> ĐANG CHẠY: {data['tc_id']} | KỲ VỌNG: {data['expected_result']}")
        input(">>> Nhập Captcha rồi nhấn ENTER tại Terminal...")

    with allure.step("4. Kiểm tra kết quả"):
        login_page.click_login()
        time.sleep(4)
        
        actual_res = ""
        try:
            # Ưu tiên kiểm tra Alert (Mã xác thực không đúng, v.v.)
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            actual_res = alert.text
            alert.accept()
        except:
            # Nếu không có Alert, kiểm tra chuyển hướng
            cur_url = driver.current_url
            # Đăng ký thành công khi URL KHÔNG còn chứa login.htm (Về trang chủ)
            # Hoặc trang chủ hiển thị chữ Chúc mừng
            if "login.htm" not in cur_url or "home.htm" in cur_url:
                actual_res = "Trang chủ"
            else:
                # Tìm các lỗi màu đỏ trên màn hình
                try:
                    # Beta Cinemas báo lỗi bằng các thẻ span/label màu đỏ
                    errors = driver.find_elements(By.XPATH, "//*[contains(@class, 'error') or contains(@class, 'danger')]")
                    msgs = [e.text for e in errors if e.is_displayed() and len(e.text) > 2]
                    actual_res = msgs[0] if msgs else "Đăng nhập thất bại (Dữ liệu sai)"
                except:
                    actual_res = "Không xác định"

        print(f"[KẾT QUẢ THỰC TẾ]: {actual_res}")
        allure.attach(driver.get_screenshot_as_png(), name="Result", attachment_type=allure.attachment_type.PNG)
        
        # So sánh với mong đợi trong JSON
        assert data['expected_result'].lower() in actual_res.lower(), \
            f"FAIL! Mong đợi '{data['expected_result']}', Thực tế báo '{actual_res}'"